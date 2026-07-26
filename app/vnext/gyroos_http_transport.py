from __future__ import annotations

import json
import ssl
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .gyroos_consumption import (
    GyroOSExperimentalRecordSnapshot,
    GyroOSHttpTransportSettings,
)
from .gyroos_consumption_service import CallerSuppliedGyroOSEnvelopeAdapter


class GyroOSHttpTransportError(RuntimeError):
    """Base error for optional read-only GyroOS HTTP transport."""


class GyroOSHttpNotFoundError(GyroOSHttpTransportError):
    """Raised when the requested experimental record does not exist."""


class GyroOSHttpResponseError(GyroOSHttpTransportError):
    """Raised when GyroOS returns a non-success response."""


class GyroOSHttpDecodeError(GyroOSHttpTransportError):
    """Raised when the response cannot be decoded as the expected JSON envelope."""


@dataclass(frozen=True, slots=True)
class GyroOSHttpResponse:
    status_code: int
    body: bytes
    content_type: str | None = None


class GyroOSReadOnlyHttpClient:
    """Minimal injectable GET-only client used by the optional transport adapter."""

    def get(self, *, url: str, headers: dict[str, str], timeout_seconds: float,
            verify_tls: bool) -> GyroOSHttpResponse:
        request = Request(url=url, headers=headers, method="GET")
        context = None if verify_tls else ssl._create_unverified_context()
        try:
            with urlopen(request, timeout=timeout_seconds, context=context) as response:
                return GyroOSHttpResponse(
                    status_code=response.status,
                    body=response.read(),
                    content_type=response.headers.get("content-type"),
                )
        except HTTPError as exc:
            body = exc.read() if exc.fp is not None else b""
            return GyroOSHttpResponse(
                status_code=exc.code,
                body=body,
                content_type=exc.headers.get("content-type") if exc.headers else None,
            )
        except (URLError, TimeoutError, OSError) as exc:
            raise GyroOSHttpTransportError("GyroOS HTTP transport failed") from exc


class GyroOSExperimentalRecordHttpAdapter:
    """Fetch one GyroOS experimental record through the verified read-only API."""

    def __init__(
        self,
        settings: GyroOSHttpTransportSettings,
        client: GyroOSReadOnlyHttpClient | None = None,
        envelope_adapter: CallerSuppliedGyroOSEnvelopeAdapter | None = None,
    ) -> None:
        self._settings = settings
        self._client = client or GyroOSReadOnlyHttpClient()
        self._envelope_adapter = envelope_adapter or CallerSuppliedGyroOSEnvelopeAdapter()

    def fetch_record(self, record_id: str) -> GyroOSExperimentalRecordSnapshot:
        url = f"{self._settings.base_url}/vnext/experimental/records/{record_id}"
        headers = {"Accept": "application/json"}
        if self._settings.bearer_token:
            headers["Authorization"] = f"Bearer {self._settings.bearer_token}"

        response = self._client.get(
            url=url,
            headers=headers,
            timeout_seconds=self._settings.timeout_seconds,
            verify_tls=self._settings.verify_tls,
        )
        if response.status_code == 404:
            raise GyroOSHttpNotFoundError(f"GyroOS experimental record not found: {record_id}")
        if response.status_code < 200 or response.status_code >= 300:
            raise GyroOSHttpResponseError(
                f"GyroOS experimental record request failed with status {response.status_code}"
            )

        try:
            payload: Any = json.loads(response.body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise GyroOSHttpDecodeError("GyroOS response is not valid UTF-8 JSON") from exc
        if not isinstance(payload, dict):
            raise GyroOSHttpDecodeError("GyroOS response JSON must be an object")

        try:
            return self._envelope_adapter.adapt(payload)
        except (ValueError, TypeError) as exc:
            raise GyroOSHttpDecodeError(
                "GyroOS response does not match the experimental record envelope"
            ) from exc
