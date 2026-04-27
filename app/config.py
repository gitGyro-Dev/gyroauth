from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    stable_threshold: float = 0.85
    recover_threshold: float = 0.70
    critical_fail_threshold: float = 0.45


settings = Settings()
