import pytest
from pydantic import ValidationError

from app.vnext.gyroos_consumption import (
    GyroOSConsumptionRequest,
    GyroOSConsumptionSettings,
    GyroOSExperimentalRecordReference,
    GyroOSExperimentalRecordSnapshot,
    GyroOSHttpTransportSettings,
)


def test_settings_reject_non_positive_limits() -> None:
    with pytest.raises(ValueError):
        GyroOSConsumptionSettings(max_payload_bytes=0)


def test_reference_and_snapshot_are_closed_models() -> None:
    with pytest.raises(ValidationError):
        GyroOSExperimentalRecordReference(record_id="record-001", canonical=True)

    with pytest.raises(ValidationError):
        GyroOSExperimentalRecordSnapshot(
            record_id="record-001",
            process_id="process-001",
            record_type="TrajectoryGraph",
            payload={},
            auth_state="AUTH_STABLE",
        )


def test_consumption_request_requires_explicit_reference_and_snapshot() -> None:
    request = GyroOSConsumptionRequest(
        reference=GyroOSExperimentalRecordReference(
            record_id="record-001",
            expected_process_id="process-001",
            expected_record_type="TrajectoryGraph",
        ),
        snapshot=GyroOSExperimentalRecordSnapshot(
            record_id="record-001",
            process_id="process-001",
            record_type="TrajectoryGraph",
            payload={"trajectory_node_refs": []},
        ),
    )

    assert request.reference.record_id == request.snapshot.record_id


def test_http_settings_normalize_base_url() -> None:
    settings = GyroOSHttpTransportSettings(base_url="https://gyroos.example/")

    assert settings.base_url == "https://gyroos.example"


def test_http_settings_reject_invalid_scheme_and_timeout() -> None:
    with pytest.raises(ValidationError):
        GyroOSHttpTransportSettings(base_url="gyroos.example")

    with pytest.raises(ValidationError):
        GyroOSHttpTransportSettings(base_url="https://gyroos.example", timeout_seconds=0)


def test_models_do_not_define_authentication_decision_fields() -> None:
    fields = GyroOSExperimentalRecordSnapshot.model_fields

    assert "auth_state" not in fields
    assert "auth_score" not in fields
    assert "next_action" not in fields
    assert "trajectory_continuity" not in fields
