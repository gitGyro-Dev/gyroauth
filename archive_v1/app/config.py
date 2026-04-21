from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    alpha: float = 1.0
    min_stability_history: int = 3
    min_auth_history: int = 5
    stability_threshold: float = 0.55
    similarity_threshold: float = 0.70
    max_history_per_session: int = 200


settings = Settings()
