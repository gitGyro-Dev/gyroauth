from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import csv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class ObserveRequest(BaseModel):
    session_id: str
    timestamp: float
    slices: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


class AuthenticateRequest(BaseModel):
    session_id: str


class AuthResponse(BaseModel):
    session_id: str
    auth_state: str
    stability: float
    events: List[str]


class SessionResponse(BaseModel):
    session_id: str
    auth_state: Optional[str]
    stability: Optional[float]
    observation_count: int
    events: List[str]


app = FastAPI(
    title="GyroAuth v2 Realtime Graph PoC",
    version="2.0.0-realtime-minimal",
    description="Minimal API that writes authentication history for live graph visualization.",
)

SESSIONS: Dict[str, Dict[str, Any]] = {}
OUTPUT_DIR = Path("outputs")
HISTORY_CSV = OUTPUT_DIR / "auth_history.csv"


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_session(session_id: str) -> Dict[str, Any]:
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "observations": [],
            "auth_state": None,
            "stability": None,
            "events": [],
        }
    return SESSIONS[session_id]


def evaluate_latest(observations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Minimal GyroOS-like evaluation boundary.

    This is intentionally simple:
    - Slice-level stability is provided in request JSON
    - Session stability is average slice stability
    - Critical low slices force AUTH_FAIL

    Later, replace this with real GyroOS Deviation / Stability / Selection output.
    """

    if not observations:
        return {"stability": 0.0, "auth_state": "AUTH_FAIL", "events": ["no_observation"]}

    latest = observations[-1]
    slices = latest.get("slices", {})

    values = []
    events = []

    for name in ["device", "behavior", "time", "space", "network", "motion"]:
        score = float(slices.get(name, {}).get("stability", 0.90))
        score = max(0.0, min(1.0, score))
        values.append(score)

        if score < 0.45:
            events.append(f"{name}_critical")
        elif score < 0.70:
            events.append(f"{name}_warning")
        elif score < 0.85:
            events.append(f"{name}_drift")

    stability = round(sum(values) / len(values), 4)

    if any(v < 0.45 for v in values):
        auth_state = "AUTH_FAIL"
        stability = min(stability, 0.40)
        events.append("critical_deviation_detected")
    elif stability >= 0.85:
        auth_state = "AUTH_STABLE"
    elif stability >= 0.70:
        auth_state = "RECONVERGING"
    else:
        auth_state = "AUTH_FAIL"

    return {"stability": round(stability, 4), "auth_state": auth_state, "events": events}


def append_history(session_id: str, timestamp: float, stability: float, auth_state: str, event: str) -> None:
    ensure_output_dir()

    exists = HISTORY_CSV.exists()

    with HISTORY_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(["session_id", "timestamp", "stability", "auth_state", "event"])

        writer.writerow([session_id, timestamp, stability, auth_state, event])


@app.get("/")
def root():
    return {
        "name": "GyroAuth v2 Realtime Graph PoC",
        "docs": "/docs",
        "history_csv": str(HISTORY_CSV),
    }


@app.post("/observe")
def observe(req: ObserveRequest):
    session = get_session(req.session_id)

    session["observations"].append(
        {
            "timestamp": req.timestamp,
            "slices": req.slices,
        }
    )
    session["events"].append("observation_received")

    return {
        "session_id": req.session_id,
        "status": "ok",
        "observation_count": len(session["observations"]),
    }


@app.post("/authenticate", response_model=AuthResponse)
def authenticate(req: AuthenticateRequest):
    session = get_session(req.session_id)

    if not session["observations"]:
        raise HTTPException(status_code=400, detail="INSUFFICIENT_OBSERVATION")

    result = evaluate_latest(session["observations"])

    latest_timestamp = float(session["observations"][-1]["timestamp"])
    auth_state = result["auth_state"]
    stability = result["stability"]
    events = result["events"]

    session["auth_state"] = auth_state
    session["stability"] = stability
    session["events"].extend(events)
    session["events"].append(f"auth_state:{auth_state}")

    append_history(
        session_id=req.session_id,
        timestamp=latest_timestamp,
        stability=stability,
        auth_state=auth_state,
        event=";".join(events) if events else "normal",
    )

    return AuthResponse(
        session_id=req.session_id,
        auth_state=auth_state,
        stability=stability,
        events=session["events"][-20:],
    )


@app.get("/session/{session_id}", response_model=SessionResponse)
def session_status(session_id: str):
    session = get_session(session_id)

    return SessionResponse(
        session_id=session_id,
        auth_state=session["auth_state"],
        stability=session["stability"],
        observation_count=len(session["observations"]),
        events=session["events"][-20:],
    )
