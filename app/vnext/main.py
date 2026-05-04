from __future__ import annotations

from typing import Any, Dict, List, Optional
from enum import Enum
from pathlib import Path
import csv
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class AuthState(str, Enum):
    AUTH_STABLE = "AUTH_STABLE"
    RECONVERGING = "RECONVERGING"
    REAUTH_REQUIRED = "REAUTH_REQUIRED"
    AUTH_FAIL = "AUTH_FAIL"


class LoopResult(BaseModel):
    process_id: str
    slice_done: Dict[str, Any]
    stability: float
    operator_response: str
    history: Dict[str, List[Any]] = Field(default_factory=dict)
    next_orientation: Optional[Dict[str, Any]] = None


class AuthStepRequest(BaseModel):
    session_id: str
    user_id: str
    timestamp: float = Field(default_factory=lambda: time.time())
    loop_result: LoopResult
    risk_context: Dict[str, Any] = Field(default_factory=dict)


class AuthStepResponse(BaseModel):
    session_id: str
    auth_state: AuthState
    auth_score: float
    stability: float
    deviation_risk: float
    operator_response: str
    trajectory_continuity: float
    response_confidence: float
    context_risk: float
    next_action: str
    events: List[str]


class SessionResponse(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    auth_state: Optional[AuthState] = None
    auth_score: Optional[float] = None
    stability: Optional[float] = None
    deviation_risk: Optional[float] = None
    operator_response: Optional[str] = None
    next_action: Optional[str] = None
    events: List[str] = Field(default_factory=list)


class HistoryResponse(BaseModel):
    session_id: str
    stability_history: List[float]
    deviation_history: List[float]
    response_history: List[str]
    auth_state_history: List[str]
    auth_score_history: List[float]


app = FastAPI(
    title="GyroAuth vNext Loop-aligned PoC",
    version="2.1.0-vnext-loop",
    description=(
        "Loop-aligned GyroAuth PoC. "
        "This mock interprets GyroOS /loop/step outputs and maps them to Auth Decisions."
    ),
)

SESSIONS: Dict[str, Dict[str, Any]] = {}

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
VNEXT_HISTORY_CSV = OUTPUT_DIR / "vnext_auth_history.csv"


def clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def avg(values: List[float], default: float = 0.0) -> float:
    return sum(values) / len(values) if values else default


def compute_deviation_risk(delta: Dict[str, Any]) -> float:
    values = [clamp(v) for v in delta.values() if isinstance(v, (int, float))]
    return round(avg(values, default=0.0), 4)


def compute_trajectory_continuity(history: Dict[str, List[Any]], stability: float, deviation_risk: float) -> float:
    stability_history = [clamp(x) for x in history.get("stability_history", []) if isinstance(x, (int, float))]
    deviation_history = [clamp(x) for x in history.get("deviation_history", []) if isinstance(x, (int, float))]

    stability_component = avg(stability_history, default=stability)
    deviation_component = 1.0 - avg(deviation_history, default=deviation_risk)

    return round(clamp(0.55 * stability_component + 0.45 * deviation_component), 4)


def compute_response_confidence(operator_response: str, history: Dict[str, List[Any]]) -> float:
    base = {
        "Continue": 1.00,
        "Adjust": 0.76,
        "Hold": 0.70,
        "Re-auth": 0.58,
        "Escalate": 0.48,
        "Fail": 0.00,
    }.get(operator_response, 0.50)

    response_history = history.get("response_history", [])
    if response_history:
        # Penalize repeated high-friction responses, but do not collapse Re-auth into Fail.
        recent = response_history[-3:]
        fail_count = sum(1 for r in recent if r == "Fail")
        reauth_count = sum(1 for r in recent if r in ("Re-auth", "Escalate"))
        base -= 0.18 * fail_count
        base -= 0.05 * max(0, reauth_count - 1)

    return round(clamp(base), 4)


def compute_context_risk(risk_context: Dict[str, Any]) -> float:
    risk = 0.0

    if risk_context.get("ip_reputation") in ("suspicious", "bad", "unknown"):
        risk += 0.25
    if risk_context.get("geo_change") is True:
        risk += 0.20
    if risk_context.get("new_device") is True:
        risk += 0.20
    if risk_context.get("suspicious_flow") is True:
        risk += 0.25
    if risk_context.get("high_value_action") is True:
        risk += 0.10

    return round(clamp(risk), 4)


def compute_auth_score(
    stability: float,
    deviation_risk: float,
    trajectory_continuity: float,
    response_confidence: float,
    context_risk: float,
) -> float:
    positive_score = (
        0.40 * stability
        + 0.25 * trajectory_continuity
        + 0.20 * response_confidence
        + 0.15 * (1.0 - context_risk)
    )
    score = positive_score - 0.20 * deviation_risk
    return round(clamp(score), 4)


def decide_auth_state(
    auth_score: float,
    stability: float,
    deviation_risk: float,
    operator_response: str,
    context_risk: float,
) -> AuthState:
    """
    vNext decision priority.

    Important:
    - Operator Response = Re-auth does NOT mean failure.
    - Re-auth means explicit verification is required unless the state has actually collapsed.
    - Fail is the only operator response that directly forces AUTH_FAIL.
    """

    if operator_response == "Fail":
        return AuthState.AUTH_FAIL

    # Explicit re-authentication is a separate state, not a failed state.
    if operator_response in ("Re-auth", "Escalate"):
        if stability < 0.45 or auth_score < 0.30 or deviation_risk >= 0.60:
            return AuthState.AUTH_FAIL
        return AuthState.REAUTH_REQUIRED

    if auth_score >= 0.85:
        return AuthState.AUTH_STABLE
    if auth_score >= 0.70:
        return AuthState.RECONVERGING
    if auth_score >= 0.55:
        return AuthState.REAUTH_REQUIRED

    # If the state is weak but not collapsed, prefer REAUTH_REQUIRED over AUTH_FAIL.
    if stability >= 0.55 and deviation_risk < 0.45 and context_risk < 0.60:
        return AuthState.REAUTH_REQUIRED

    return AuthState.AUTH_FAIL


def next_action_for(auth_state: AuthState) -> str:
    return {
        AuthState.AUTH_STABLE: "continue_session",
        AuthState.RECONVERGING: "collect_additional_signal",
        AuthState.REAUTH_REQUIRED: "request_explicit_verification",
        AuthState.AUTH_FAIL: "terminate_or_block_session",
    }[auth_state]


def get_session(session_id: str) -> Dict[str, Any]:
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "session_id": session_id,
            "user_id": None,
            "auth_state": None,
            "auth_score": None,
            "stability": None,
            "deviation_risk": None,
            "operator_response": None,
            "next_action": None,
            "events": [],
            "stability_history": [],
            "deviation_history": [],
            "response_history": [],
            "auth_state_history": [],
            "auth_score_history": [],
        }
    return SESSIONS[session_id]


def append_csv(session_id: str, timestamp: float, stability: float, deviation_risk: float, operator_response: str, auth_score: float, auth_state: str) -> None:
    exists = VNEXT_HISTORY_CSV.exists()
    with VNEXT_HISTORY_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow([
                "session_id",
                "timestamp",
                "stability",
                "deviation_risk",
                "operator_response",
                "auth_score",
                "auth_state",
            ])
        writer.writerow([session_id, timestamp, stability, deviation_risk, operator_response, auth_score, auth_state])


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "name": "GyroAuth vNext Loop-aligned PoC",
        "docs": "/docs",
        "main_endpoint": "POST /auth/step",
    }


@app.post("/auth/step", response_model=AuthStepResponse)
def auth_step(req: AuthStepRequest) -> AuthStepResponse:
    session = get_session(req.session_id)
    session["user_id"] = req.user_id

    loop = req.loop_result
    slice_done = loop.slice_done
    delta = slice_done.get("delta", {}) if isinstance(slice_done, dict) else {}

    stability = clamp(loop.stability)
    deviation_risk = compute_deviation_risk(delta)
    operator_response = loop.operator_response
    trajectory_continuity = compute_trajectory_continuity(loop.history, stability, deviation_risk)
    response_confidence = compute_response_confidence(operator_response, loop.history)
    context_risk = compute_context_risk(req.risk_context)

    auth_score = compute_auth_score(
        stability=stability,
        deviation_risk=deviation_risk,
        trajectory_continuity=trajectory_continuity,
        response_confidence=response_confidence,
        context_risk=context_risk,
    )

    auth_state = decide_auth_state(
        auth_score=auth_score,
        stability=stability,
        deviation_risk=deviation_risk,
        operator_response=operator_response,
        context_risk=context_risk,
    )
    next_action = next_action_for(auth_state)

    session["auth_state"] = auth_state
    session["auth_score"] = auth_score
    session["stability"] = stability
    session["deviation_risk"] = deviation_risk
    session["operator_response"] = operator_response
    session["next_action"] = next_action

    session["stability_history"].append(stability)
    session["deviation_history"].append(deviation_risk)
    session["response_history"].append(operator_response)
    session["auth_state_history"].append(auth_state.value)
    session["auth_score_history"].append(auth_score)

    events = [
        "loop_result_received",
        f"operator_response:{operator_response}",
        f"auth_state:{auth_state.value}",
    ]
    session["events"].extend(events)

    append_csv(
        session_id=req.session_id,
        timestamp=req.timestamp,
        stability=stability,
        deviation_risk=deviation_risk,
        operator_response=operator_response,
        auth_score=auth_score,
        auth_state=auth_state.value,
    )

    return AuthStepResponse(
        session_id=req.session_id,
        auth_state=auth_state,
        auth_score=auth_score,
        stability=round(stability, 4),
        deviation_risk=deviation_risk,
        operator_response=operator_response,
        trajectory_continuity=trajectory_continuity,
        response_confidence=response_confidence,
        context_risk=context_risk,
        next_action=next_action,
        events=session["events"][-20:],
    )


@app.get("/auth/session/{session_id}", response_model=SessionResponse)
def get_auth_session(session_id: str) -> SessionResponse:
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="SESSION_NOT_FOUND")
    s = SESSIONS[session_id]
    return SessionResponse(
        session_id=session_id,
        user_id=s["user_id"],
        auth_state=s["auth_state"],
        auth_score=s["auth_score"],
        stability=s["stability"],
        deviation_risk=s["deviation_risk"],
        operator_response=s["operator_response"],
        next_action=s["next_action"],
        events=s["events"][-20:],
    )


@app.get("/auth/history/{session_id}", response_model=HistoryResponse)
def get_auth_history(session_id: str) -> HistoryResponse:
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="SESSION_NOT_FOUND")
    s = SESSIONS[session_id]
    return HistoryResponse(
        session_id=session_id,
        stability_history=s["stability_history"],
        deviation_history=s["deviation_history"],
        response_history=s["response_history"],
        auth_state_history=s["auth_state_history"],
        auth_score_history=s["auth_score_history"],
    )


@app.post("/auth/reset/{session_id}")
def reset_session(session_id: str) -> Dict[str, str]:
    if session_id in SESSIONS:
        del SESSIONS[session_id]
    return {"session_id": session_id, "status": "reset"}
