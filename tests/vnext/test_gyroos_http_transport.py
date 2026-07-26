import json

import pytest

from app.vnext.gyroos_consumption import GyroOSHttpTransportSettings
from app.vnext.gyroos_http_transport import (
    GyroOSExperimentalRecordHttpAdapter,
    GyroOSHttpDecodeError,
    GyroOSHttpNotFoundError,
    GyroOSHttpResponse,
    GyroOSHttpResponseError,
)


class StubClient:
    def __init__(self, response: GyroOSHttpResponse) -> None:
        self.response = response
        self.calls: list[dict] = []

    def get(self, *, url: str, headers: dict[str, str], timeout_seconds: float,
            verify_tls: bool) -> GyroOSHttpResponse:
        self.calls.append(
            {
                "url": url,
                "headers": headers,
                "timeout_seconds": timeout_seconds,
                "verify_tls": verify_tls,
            }
        )
        return self.response


def make_success_response() -> GyroOSHttpResponse:
    body = json.dumps(
        {
            "record": {
                "record_id": "record-001",
                "process_id": "process-001",
                "record_type": "TrajectoryGraph",
                "payload": {"trajectory_node_refs": []},
                "provisional": True,
                "metadata": {},
            }
        }
    ).encode("utf-8")
    return GyroOSHttpResponse(status_code=200, body=body, content_type="application/json")


def test_fetch_record_uses_get_only_endpoint_and_bearer_header() -> None:
    client = StubClient(make_success_response())
    adapter = GyroOSExperimentalRecordHttpAdapter(
        GyroOSHttpTransportSettings(
            base_url="https://gyroos.example",
            bearer_token="secret-token",
            timeout_seconds=3.0,
            verify_tls=True,
        ),
        client=client,
    )

    snapshot = adapter.fetch_record("record-001")

    assert snapshot.record_id == "record-001"
    assert client.calls == [
        {
            "url": "https://gyroos.example/vnext/experimental/records/record-001",
            "headers": {
                "Accept": "application/json",
                "Authorization": "Bearer secret-token",
            },
            "timeout_seconds": 3.0,
            "verify_tls": True,
        }
    ]


def test_fetch_record_raises_explicit_not_found_error() -> None:
    adapter = GyroOSExperimentalRecordHttpAdapter(
        GyroOSHttpTransportSettings(base_url="https://gyroos.example"),
        client=StubClient(GyroOSHttpResponse(status_code=404, body=b"{}")),
    )

    with pytest.raises(GyroOSHttpNotFoundError):
        adapter.fetch_record("missing")


def test_fetch_record_raises_for_other_non_success_status() -> None:
    adapter = GyroOSExperimentalRecordHttpAdapter(
        GyroOSHttpTransportSettings(base_url="https://gyroos.example"),
        client=StubClient(GyroOSHttpResponse(status_code=503, body=b"{}")),
    )

    with pytest.raises(GyroOSHttpResponseError):
        adapter.fetch_record("record-001")


def test_fetch_record_rejects_invalid_json() -> None:
    adapter = GyroOSExperimentalRecordHttpAdapter(
        GyroOSHttpTransportSettings(base_url="https://gyroos.example"),
        client=StubClient(GyroOSHttpResponse(status_code=200, body=b"not-json")),
    )

    with pytest.raises(GyroOSHttpDecodeError):
        adapter.fetch_record("record-001")


def test_fetch_record_rejects_invalid_envelope_shape() -> None:
    adapter = GyroOSExperimentalRecordHttpAdapter(
        GyroOSHttpTransportSettings(base_url="https://gyroos.example"),
        client=StubClient(
            GyroOSHttpResponse(
                status_code=200,
                body=json.dumps({"record": "invalid"}).encode("utf-8"),
            )
        ),
    )

    with pytest.raises(GyroOSHttpDecodeError):
        adapter.fetch_record("record-001")


def test_transport_models_do_not_define_authentication_outcomes() -> None:
    response_fields = set(GyroOSHttpResponse.__dataclass_fields__)

    assert "auth_state" not in response_fields
    assert "auth_score" not in response_fields
    assert "next_action" not in response_fields
