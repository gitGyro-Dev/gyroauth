from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .domain.auth_state import AuthState, RiskLevel


class ObserveRequest(BaseModel):
    session_id: str
    timestamp: float
    slices: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


class ObserveResponse(BaseModel):
    session_id: str
    status: str
    observation_count: int


class AuthenticateRequest(BaseModel):
    session_id: str


class SliceScore(BaseModel):
    name: str
    stability: float
    status: str


class AuthenticateResponse(BaseModel):
    session_id: str
    auth_state: AuthState
    stability: float
    risk_level: RiskLevel
    slice_scores: List[SliceScore]
    events: List[str]


class ReconvergeRequest(BaseModel):
    session_id: str
    reason: str = "automatic"


class ReconvergeResponse(BaseModel):
    session_id: str
    auth_state: AuthState
    message: str


class SessionResponse(BaseModel):
    session_id: str
    auth_state: Optional[AuthState]
    stability: Optional[float]
    observation_count: int
    events: List[str]
