"""Backend tests for Lab Report Status.

These tests cover administrative availability only. They never assert clinical values.
Kore.ai conversation tests TC11 and TC12 are NOT covered here. See README.md.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.models import LabReportStatus


def test_tc08_lab_report_processing(client: TestClient) -> None:
    response = client.get("/lab-reports/LAB1001")
    assert response.status_code == 200
    body = response.json()
    assert body["reportId"] == "LAB1001"
    assert body["reportStatus"] == LabReportStatus.PROCESSING.value
    assert body["reportAvailable"] is False
    assert body["handoffRecommended"] is False


def test_tc09_lab_report_available(client: TestClient) -> None:
    response = client.get("/lab-reports/LAB1002")
    assert response.status_code == 200
    body = response.json()
    assert body["reportStatus"] == LabReportStatus.AVAILABLE.value
    assert body["reportAvailable"] is True
    assert "result" not in body
    assert "diagnosis" not in body


def test_tc10_lab_report_delayed(client: TestClient) -> None:
    response = client.get("/lab-reports/LAB1003")
    assert response.status_code == 200
    body = response.json()
    assert body["reportStatus"] == LabReportStatus.DELAYED.value
    assert body["reportAvailable"] is False
    assert body["handoffRecommended"] is True


def test_lab_report_access_error(client: TestClient) -> None:
    response = client.get("/lab-reports/LAB1004")
    assert response.status_code == 200
    body = response.json()
    assert body["reportStatus"] == LabReportStatus.ACCESS_ERROR.value
    assert body["reportAvailable"] is False
    assert body["handoffRecommended"] is True


def test_lab_report_not_found(client: TestClient) -> None:
    response = client.get("/lab-reports/LAB9999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_malformed_report_id_returns_422(client: TestClient) -> None:
    response = client.get("/lab-reports/LAB!!1")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_INPUT"


def test_unexpected_lab_report_error_returns_500(client: TestClient) -> None:
    with patch(
        "app.routers.lab_reports.lab_report_service.get_lab_report_status",
        side_effect=RuntimeError("simulated failure"),
    ):
        response = client.get("/lab-reports/LAB1001")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_ERROR"
    assert "simulated failure" not in response.text


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
