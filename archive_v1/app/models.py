from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class RawState(BaseModel):
    timestamp: float = Field(..., description="Unix timestamp or monotonic time")
    user_id: str = Field(..., description="Logical user identifier")
    session_id: str = Field(..., description="Session identifier")
    device_id: str = Field(..., description="Device identifier")
    x: float = Field(..., description="Abstract position x")
    y: float = Field(..., description="Abstract position y")
    velocity: float = Field(..., description="Estimated motion speed")
    interaction: float = Field(..., description="Interaction intensity or gesture score")
    touch_pressure: float = Field(0.0, description="Optional touch pressure")
    typing_rhythm: float = Field(0.0, description="Optional typing rhythm score")


class ObserveResponse(BaseModel):
    session_id: str
    user_id: str
    feature_vector: List[float]
    stability: Optional[float]
    history_size: int


class StabilityResponse(BaseModel):
    session_id: str
    user_id: str
    stability: Optional[float]
    history_size: int
    threshold: float
    stable: bool


class EnrollRequest(BaseModel):
    user_id: str
    session_id: str
    label: str = Field("default", description="Reference label")


class EnrollResponse(BaseModel):
    user_id: str
    label: str
    reference_length: int


class AuthenticateRequest(BaseModel):
    user_id: str
    session_id: str
    label: str = Field("default", description="Reference label")


class AuthenticateResponse(BaseModel):
    user_id: str
    session_id: str
    label: str
    stability: Optional[float]
    similarity: Optional[float]
    auth_score: Optional[float]
    authenticated: bool
    reason: str


class ReconvergeRequest(BaseModel):
    session_id: str
    keep_last_n: int = 0


class ReconvergeResponse(BaseModel):
    session_id: str
    remaining: int


class SessionDump(BaseModel):
    session_id: str
    user_id: Optional[str]
    feature_history: List[List[float]]
    raw_count: int
