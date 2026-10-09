"""Backend tests for Insurance Eligibility.

Kore.ai conversation tests TC11 and TC12 are NOT covered here. See README.md.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.models import EligibilityStatus, VerificationStatus


def test_tc05_insurance_active_and_verified(client: TestClient) -> None:
    response = client.get("/insurance/INS1001")
    assert response.status_code == 200
    body = response.json()
    assert body["memberId"] == "INS1001"
    assert body["eligibilityStatus"] == EligibilityStatus.ACTIVE.value
    assert body["verificationStatus"] == VerificationStatus.VERIFIED.value
    assert body["payerName"] == "Northwind Health"
    assert body["planName"] == "Northwind PPO Gold"
    assert body["handoffRecommended"] is False


def test_tc06_insurance_inactive(client: TestClient) -> None:
    response = client.get("/insurance/INS1002")
    assert response.status_code == 200
    body = response.json()
    assert body["eligibilityStatus"] == EligibilityStatus.INACTIVE.value
    assert body["handoffRecommended"] is True


def test_tc07_insurance_verification_required(client: TestClient) -> None:
    response = client.get("/insurance/INS1003")
    assert response.status_code == 200
    body = response.json()
    assert body["eligibilityStatus"] == EligibilityStatus.VERIFICATION_REQUIRED.value
    assert body["verificationStatus"] != VerificationStatus.VERIFIED.value
    assert body["handoffRecommended"] is True


def test_payer_mismatch(client: TestClient) -> None:
    response = client.get("/insurance/INS1004")
    assert response.status_code == 200
    body = response.json()
    assert body["eligibilityStatus"] == EligibilityStatus.PAYER_MISMATCH.value
    assert body["verificationStatus"] == VerificationStatus.FAILED.value
    assert body["handoffRecommended"] is True


def test_insurance_not_found(client: TestClient) -> None:
    response = client.get("/insurance/INS9999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_malformed_member_id_returns_422(client: TestClient) -> None:
    response = client.get("/insurance/INS*1001")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_INPUT"


def test_unexpected_insurance_error_returns_500(client: TestClient) -> None:
    with patch(
        "app.routers.insurance.insurance_service.get_insurance_eligibility",
        side_effect=RuntimeError("simulated failure"),
    ):
        response = client.get("/insurance/INS1001")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_ERROR"
    assert "simulated failure" not in response.text
