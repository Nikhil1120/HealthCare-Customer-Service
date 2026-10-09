"""Application-specific exceptions and structured error payloads."""

from typing import Any


class RecordNotFoundError(Exception):
    """Raised when a requested mock record does not exist."""

    def __init__(self, resource: str, record_id: str) -> None:
        self.resource = resource
        self.record_id = record_id
        super().__init__(f"{resource} '{record_id}' was not found.")


def error_payload(code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build the consistent JSON error envelope used by all HTTP errors."""
    payload: dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if details:
        payload["error"]["details"] = details
    return payload
