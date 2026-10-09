"""Backend tests for Appointment Management.

Kore.ai conversation tests TC11 (explicit human request) and TC12 (context retention)
are NOT covered here. See README.md.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient


def test_tc01_appointment_confirmed(client: TestClient) -> None:
    response = client.get("/appointments/APT1001")
    assert response.status_code == 200
    body = response.json()
    assert body["appointmentId"] == "APT1001"
    assert body["appointmentStatus"] == "CONFIRMED"
    assert body["appointmentDate"] == "2026-10-15"
    assert body["appointmentTime"] == "09:30"
    assert body["providerName"] == "Dr. Maya Chen"
    assert body["appointmentType"] == "Primary care follow-up"
    assert body["rescheduleEligible"] is True
    assert body["cancellationEligible"] is True
    assert body["handoffRecommended"] is False


def test_tc02_reschedule_eligible_appointment(client: TestClient) -> None:
    """Eligible appointment returns flags the bot can use for a reschedule request."""
    response = client.get("/appointments/APT1001")
    assert response.status_code == 200
    body = response.json()
    assert body["rescheduleEligible"] is True
    assert body["appointmentStatus"] == "CONFIRMED"


def test_tc03_appointment_reschedule_restricted(client: TestClient) -> None:
    response = client.get("/appointments/APT1004")
    assert response.status_code == 200
    body = response.json()
    assert body["appointmentStatus"] == "RESCHEDULE_NOT_ALLOWED"
    assert body["rescheduleEligible"] is False
    assert body["cancellationEligible"] is False
    assert body["handoffRecommended"] is True
    assert "representative" in body["nextAdministrativeStep"].lower()


def test_tc04_appointment_not_found(client: TestClient) -> None:
    response = client.get("/appointments/APT9999")
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "NOT_FOUND"


def test_rescheduled_appointment_returns_updated_details(client: TestClient) -> None:
    response = client.get("/appointments/APT1002")
    assert response.status_code == 200
    body = response.json()
    assert body["appointmentStatus"] == "RESCHEDULED"
    assert body["appointmentDate"] == "2026-10-22"
    assert body["appointmentTime"] == "14:00"


def test_cancelled_appointment(client: TestClient) -> None:
    response = client.get("/appointments/APT1003")
    assert response.status_code == 200
    body = response.json()
    assert body["appointmentStatus"] == "CANCELLED"
    assert body["rescheduleEligible"] is False
    assert body["cancellationEligible"] is False


def test_malformed_appointment_id_returns_422(client: TestClient) -> None:
    response = client.get("/appointments/APT@INVALID")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_INPUT"


def test_unexpected_appointment_error_returns_500(client: TestClient) -> None:
    with patch(
        "app.routers.appointments.appointment_service.get_appointment_details",
        side_effect=RuntimeError("simulated failure"),
    ):
        response = client.get("/appointments/APT1001")
    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "INTERNAL_ERROR"
    assert "simulated failure" not in response.text
    assert "traceback" not in response.text.lower()
