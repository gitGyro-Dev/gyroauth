from __future__ import annotations

from typing import Dict, Tuple

from fastapi import FastAPI, HTTPException

from .auth_engine import auth_score, decide_auth, trajectory_similarity
from .config import settings
from .models import (
    AuthenticateRequest,
    AuthenticateResponse,
    EnrollRequest,
    EnrollResponse,
    ObserveResponse,
    RawState,
    ReconvergeRequest,
    ReconvergeResponse,
    SessionDump,
    StabilityResponse,
)
from .slice_engine import slice_state
from .stability import stability
from .trajectory import Trajectory

app = FastAPI(
    title="GyroAuth PoC",
    version="0.1.0",
    description="Minimal proof-of-concept for authentication as state convergence.",
)

SESSIONS: Dict[str, Trajectory] = {}
REFERENCES: Dict[Tuple[str, str], list[list[float]]] = {}


def get_session(session_id: str) -> Trajectory:
    if session_id not in SESSIONS:
        SESSIONS[session_id] = Trajectory()
    return SESSIONS[session_id]


@app.get("/")
def root():
    return {"message": "GyroAuth PoC is running.", "docs": "/docs"}


@app.post("/observe", response_model=ObserveResponse)
def observe(state: RawState):
    session = get_session(state.session_id)
    x = slice_state(state)
    recent_history = session.features[-20:]
    stab = stability(x, recent_history, alpha=settings.alpha)
    session.add(state, x, max_len=settings.max_history_per_session)

    return ObserveResponse(
        session_id=state.session_id,
        user_id=state.user_id,
        feature_vector=x,
        stability=stab,
        history_size=len(session.features),
    )


@app.get("/stability/{session_id}", response_model=StabilityResponse)
def get_stability(session_id: str):
    session = get_session(session_id)
    current = session.last()
    if current is None:
        return StabilityResponse(
            session_id=session_id,
            user_id=session.user_id or "",
            stability=None,
            history_size=0,
            threshold=settings.stability_threshold,
            stable=False,
        )

    hist = session.features[:-1][-20:]
    stab = stability(current, hist, alpha=settings.alpha)
    stable_flag = False if stab is None else stab >= settings.stability_threshold

    return StabilityResponse(
        session_id=session_id,
        user_id=session.user_id or "",
        stability=stab,
        history_size=len(session.features),
        threshold=settings.stability_threshold,
        stable=stable_flag,
    )


@app.post("/enroll", response_model=EnrollResponse)
def enroll(req: EnrollRequest):
    session = get_session(req.session_id)
    if len(session.features) < settings.min_auth_history:
        raise HTTPException(
            status_code=400,
            detail=f"Need at least {settings.min_auth_history} observations to enroll.",
        )

    REFERENCES[(req.user_id, req.label)] = list(session.features)
    return EnrollResponse(
        user_id=req.user_id,
        label=req.label,
        reference_length=len(session.features),
    )


@app.post("/authenticate", response_model=AuthenticateResponse)
def authenticate(req: AuthenticateRequest):
    session = get_session(req.session_id)
    if len(session.features) < settings.min_auth_history:
        return AuthenticateResponse(
            user_id=req.user_id,
            session_id=req.session_id,
            label=req.label,
            stability=None,
            similarity=None,
            auth_score=None,
            authenticated=False,
            reason=f"Need at least {settings.min_auth_history} observations in current session.",
        )

    reference = REFERENCES.get((req.user_id, req.label))
    if reference is None:
        return AuthenticateResponse(
            user_id=req.user_id,
            session_id=req.session_id,
            label=req.label,
            stability=None,
            similarity=None,
            auth_score=None,
            authenticated=False,
            reason="Reference trajectory not enrolled.",
        )

    current = session.last()
    hist = session.features[:-1][-20:]
    stab = stability(current, hist, alpha=settings.alpha) if current is not None else None
    sim = trajectory_similarity(session.features, reference, max_points=20)
    score = auth_score(stab, sim, session.features)

    ok, reason = decide_auth(
        stability_score=stab,
        similarity_score=sim,
        combined_score=score,
        min_stability=settings.stability_threshold,
        min_similarity=settings.similarity_threshold,
    )

    return AuthenticateResponse(
        user_id=req.user_id,
        session_id=req.session_id,
        label=req.label,
        stability=stab,
        similarity=sim,
        auth_score=score,
        authenticated=ok,
        reason=reason,
    )


@app.post("/reconverge", response_model=ReconvergeResponse)
def reconverge(req: ReconvergeRequest):
    session = get_session(req.session_id)
    remaining = session.clear(keep_last_n=req.keep_last_n)
    return ReconvergeResponse(session_id=req.session_id, remaining=remaining)


@app.get("/session/{session_id}", response_model=SessionDump)
def session_dump(session_id: str):
    session = get_session(session_id)
    return SessionDump(
        session_id=session_id,
        user_id=session.user_id,
        feature_history=session.features,
        raw_count=len(session.raw_states),
    )
