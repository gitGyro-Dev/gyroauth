from __future__ import annotations

from typing import Dict, Tuple

from app.config import settings
from app.domain.auth_state import AuthState, RiskLevel


def decide_auth(gyroos_result: Dict) -> Tuple[AuthState, RiskLevel]:
    stability = float(gyroos_result.get("stability", 0.0))
    events = gyroos_result.get("events", [])

    if "critical_deviation_detected" in events:
        return AuthState.AUTH_FAIL, RiskLevel.HIGH

    if stability >= settings.stable_threshold:
        return AuthState.AUTH_STABLE, RiskLevel.LOW

    if stability >= settings.recover_threshold:
        return AuthState.RECONVERGING, RiskLevel.MEDIUM

    return AuthState.AUTH_FAIL, RiskLevel.HIGH
