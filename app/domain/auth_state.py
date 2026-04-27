from enum import Enum


class AuthState(str, Enum):
    AUTH_STABLE = "AUTH_STABLE"
    RECONVERGING = "RECONVERGING"
    AUTH_FAIL = "AUTH_FAIL"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
