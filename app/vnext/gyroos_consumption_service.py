from __future__ import annotations

from copy import deepcopy
from typing import Any

from .gyroos_consumption import (
    GyroOSConsumptionRequest,
    GyroOSConsumptionResult,
    GyroOSConsumptionSettings,
    GyroOSConsumptionValidatedSnapshot,
    GyroOSExperimentalRecordReference,
    GyroOSExperimentalRecordSnapshot,
)


class GyroOSConsumptionError(ValueError):
    """Base error for GyroAuth-side GyroOS record consumption."""


class GyroOSRecordIdentityMismatchError(GyroOSConsumptionError):
    """Raised when explicit reference identity does not match the supplied snapshot."""


class GyroOSProcessMismatchError(GyroOSConsumptionError):
    """Raised when expected process scope does not match the supplied snapshot."""


class GyroOSRecordTypeMismatchError(GyroOSConsumptionError):
    """Raised when expected record type does not match the supplied snapshot."""


class CallerSuppliedGyroOSEnvelopeAdapter:
    """Adapt a caller-supplied GyroOS experimental API record to a consumer snapshot.

    The adapter validates only the envelope shape needed by GyroAuth consumption.
    It does not reconstruct GyroOS typed records or infer authentication semantics.
    """

    def adapt(self, envelope: dict[str, Any]) -> GyroOSExperimentalRecordSnapshot:
        record = envelope.get("record", envelope)
        if not isinstance(record, dict):
            raise GyroOSConsumptionError("caller-supplied envelope must contain an object record")

        return GyroOSConsumptionValidatedSnapshot.model_validate(deepcopy(record))


class GyroOSExperimentalRecordConsumer:
    """Inspect one explicit GyroOS experimental record without auth-state mapping."""

    def __init__(self, settings: GyroOSConsumptionSettings | None = None) -> None:
        self._settings = settings or GyroOSConsumptionSettings()

    def consume(self, request: GyroOSConsumptionRequest) -> GyroOSConsumptionResult:
        reference: GyroOSExperimentalRecordReference = request.reference
        snapshot = request.snapshot.model_copy(deep=True)

        if reference.record_id != snapshot.record_id:
            raise GyroOSRecordIdentityMismatchError(
                "reference record_id must match supplied snapshot record_id"
            )
        if (
            reference.expected_process_id is not None
            and reference.expected_process_id != snapshot.process_id
        ):
            raise GyroOSProcessMismatchError(
                "expected_process_id must match supplied snapshot process_id"
            )
        if (
            reference.expected_record_type is not None
            and reference.expected_record_type != snapshot.record_type
        ):
            raise GyroOSRecordTypeMismatchError(
                "expected_record_type must match supplied snapshot record_type"
            )

        warnings: list[str] = []
        if snapshot.provisional:
            warnings.append("source_record_is_provisional")
        if not snapshot.payload:
            warnings.append("source_payload_is_empty")
        if len(warnings) > self._settings.max_warning_count:
            warnings = warnings[: self._settings.max_warning_count]

        copied_snapshot = GyroOSExperimentalRecordSnapshot.model_validate(
            snapshot.model_dump(mode="python")
        )
        return GyroOSConsumptionResult(
            record_id=copied_snapshot.record_id,
            process_id=copied_snapshot.process_id,
            record_type=copied_snapshot.record_type,
            accepted_for_inspection=True,
            warnings=list(warnings),
            snapshot=copied_snapshot,
        )
