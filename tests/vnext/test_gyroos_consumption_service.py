import pytest

from app.vnext.gyroos_consumption import (
    GyroOSConsumptionRequest,
    GyroOSExperimentalRecordReference,
)
from app.vnext.gyroos_consumption_service import (
    CallerSuppliedGyroOSEnvelopeAdapter,
    GyroOSExperimentalRecordConsumer,
    GyroOSProcessMismatchError,
    GyroOSRecordIdentityMismatchError,
    GyroOSRecordTypeMismatchError,
)


def make_envelope() -> dict:
    return {
        "record": {
            "record_id": "record-001",
            "process_id": "process-001",
            "record_type": "TrajectoryGraph",
            "payload": {"trajectory_node_refs": ["node-001"]},
            "provisional": True,
            "metadata": {"source": "gyroos-api"},
        }
    }


def test_adapter_accepts_wrapped_api_record() -> None:
    snapshot = CallerSuppliedGyroOSEnvelopeAdapter().adapt(make_envelope())

    assert snapshot.record_id == "record-001"
    assert snapshot.payload == {"trajectory_node_refs": ["node-001"]}


def test_adapter_deep_copies_caller_payload() -> None:
    envelope = make_envelope()
    snapshot = CallerSuppliedGyroOSEnvelopeAdapter().adapt(envelope)

    envelope["record"]["payload"]["trajectory_node_refs"].append("node-002")

    assert snapshot.payload == {"trajectory_node_refs": ["node-001"]}


def test_consumer_accepts_only_for_inspection() -> None:
    snapshot = CallerSuppliedGyroOSEnvelopeAdapter().adapt(make_envelope())
    result = GyroOSExperimentalRecordConsumer().consume(
        GyroOSConsumptionRequest(
            reference=GyroOSExperimentalRecordReference(
                record_id="record-001",
                expected_process_id="process-001",
                expected_record_type="TrajectoryGraph",
            ),
            snapshot=snapshot,
        )
    )

    assert result.accepted_for_inspection is True
    assert result.warnings == ["source_record_is_provisional"]
    assert "auth_state" not in result.model_fields
    assert "auth_score" not in result.model_fields
    assert "next_action" not in result.model_fields


def test_consumer_rejects_record_identity_mismatch() -> None:
    snapshot = CallerSuppliedGyroOSEnvelopeAdapter().adapt(make_envelope())

    with pytest.raises(GyroOSRecordIdentityMismatchError):
        GyroOSExperimentalRecordConsumer().consume(
            GyroOSConsumptionRequest(
                reference=GyroOSExperimentalRecordReference(record_id="other-record"),
                snapshot=snapshot,
            )
        )


def test_consumer_rejects_process_mismatch() -> None:
    snapshot = CallerSuppliedGyroOSEnvelopeAdapter().adapt(make_envelope())

    with pytest.raises(GyroOSProcessMismatchError):
        GyroOSExperimentalRecordConsumer().consume(
            GyroOSConsumptionRequest(
                reference=GyroOSExperimentalRecordReference(
                    record_id="record-001",
                    expected_process_id="other-process",
                ),
                snapshot=snapshot,
            )
        )


def test_consumer_rejects_record_type_mismatch() -> None:
    snapshot = CallerSuppliedGyroOSEnvelopeAdapter().adapt(make_envelope())

    with pytest.raises(GyroOSRecordTypeMismatchError):
        GyroOSExperimentalRecordConsumer().consume(
            GyroOSConsumptionRequest(
                reference=GyroOSExperimentalRecordReference(
                    record_id="record-001",
                    expected_record_type="StabilityScene",
                ),
                snapshot=snapshot,
            )
        )


def test_consumer_result_is_independent_from_snapshot_mutation() -> None:
    snapshot = CallerSuppliedGyroOSEnvelopeAdapter().adapt(make_envelope())
    result = GyroOSExperimentalRecordConsumer().consume(
        GyroOSConsumptionRequest(
            reference=GyroOSExperimentalRecordReference(record_id="record-001"),
            snapshot=snapshot,
        )
    )

    snapshot.payload["trajectory_node_refs"].append("node-002")

    assert result.snapshot.payload == {"trajectory_node_refs": ["node-001"]}
