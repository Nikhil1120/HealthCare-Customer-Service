"""Insurance eligibility lookup. Never reports VERIFIED when manual verification is required."""

from app.data import INSURANCE_RECORDS
from app.exceptions import RecordNotFoundError
from app.models import EligibilityStatus, InsuranceEligibility, VerificationStatus


def get_insurance_eligibility(member_id: str) -> InsuranceEligibility:
    record = INSURANCE_RECORDS.get(member_id)
    if record is None:
        raise RecordNotFoundError("insurance member", member_id)

    eligibility = InsuranceEligibility.model_validate(record)

    # Guardrail: VERIFICATION_REQUIRED must never be paired with VERIFIED.
    if (
        eligibility.eligibilityStatus == EligibilityStatus.VERIFICATION_REQUIRED
        and eligibility.verificationStatus == VerificationStatus.VERIFIED
    ):
        raise RuntimeError("Insurance mock data is inconsistent: verification required but marked verified.")

    return eligibility
