from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


@dataclass(frozen=True, slots=True)
class GyroOSConsumptionSettings:
    """Resource limits for isolated GyroOS experimental-record consumption."""

    max_payload_bytes: int = 262_144
    max_metadata_bytes: int = 65_536
    max_record_id_length: int = 256
    max_record_type_length: int = 128
    max_warning_count: int = 32

    def __post_init__(self) -> None:
        for name, value in (
            ("max_payload_bytes", self.max_payload_bytes),
            ("max_metadata_bytes", self.max_metadata_bytes),
            ("max_record_id_length", self.max_record_id_length),
            ("max_record_type_length", self.max_record_type_length),
            ("max_warning_count", self.max_warning_count),
        ):
            if value <= 0:
                raise ValueError(f"{name} must be greater than zero")


class GyroOSConsumptionModel(BaseModel):
    """Closed public model boundary for GyroOS record consumption only."""

    model_config = ConfigDict(extra="forbid")


class GyroOSExperimentalRecordReference(GyroOSConsumptionModel):
    record_id: str
    expected_process_id: str | None = None
    expected_record_type: str | None = None


class GyroOSExperimentalRecordSnapshot(GyroOSConsumptionModel):
    record_id: str
    process_id: str
    record_type: str
    payload: dict[str, Any]
    source_ref: str | None = None
    provisional: bool = True
    stored_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class GyroOSConsumptionRequest(GyroOSConsumptionModel):
    reference: GyroOSExperimentalRecordReference
    snapshot: GyroOSExperimentalRecordSnapshot


class GyroOSConsumptionResult(GyroOSConsumptionModel):
    record_id: str
    process_id: str
    record_type: str
    accepted_for_inspection: bool
    warnings: list[str] = Field(default_factory=list)
    snapshot: GyroOSExperimentalRecordSnapshot


class GyroOSHttpTransportSettings(GyroOSConsumptionModel):
    base_url: str
    bearer_token: str | None = None
    timeout_seconds: float = 5.0
    verify_tls: bool = True

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, value: str) -> str:
        normalized = value.strip().rstrip("/")
        if not normalized.startswith(("http://", "https://")):
            raise ValueError("base_url must begin with http:// or https://")
        return normalized

    @field_validator("timeout_seconds")
    @classmethod
    def validate_timeout(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        return value


class GyroOSConsumptionValidatedSnapshot(GyroOSExperimentalRecordSnapshot):
    """Snapshot with consumer-side size validation applied."""

    @model_validator(mode="after")
    def validate_default_limits(self) -> "GyroOSConsumptionValidatedSnapshot":
        settings = GyroOSConsumptionSettings()
        if len(self.record_id) > settings.max_record_id_length:
            raise ValueError("record_id exceeds consumer limit")
        if len(self.record_type) > settings.max_record_type_length:
            raise ValueError("record_type exceeds consumer limit")
        payload_size = len(json.dumps(self.payload, ensure_ascii=False).encode("utf-8"))
        metadata_size = len(json.dumps(self.metadata, ensure_ascii=False).encode("utf-8"))
        if payload_size > settings.max_payload_bytes:
            raise ValueError("payload exceeds consumer limit")
        if metadata_size > settings.max_metadata_bytes:
            raise ValueError("metadata exceeds consumer limit")
        return self
