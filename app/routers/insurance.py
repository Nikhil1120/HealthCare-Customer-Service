"""Insurance eligibility endpoints for Kore.ai Custom Service nodes."""

import logging

from fastapi import APIRouter, Path

from app.exceptions import RecordNotFoundError
from app.models import ErrorResponse, InsuranceEligibility
from app.services import insurance_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/insurance", tags=["Insurance"])


@router.get(
    "/{memberId}",
    response_model=InsuranceEligibility,
    responses={
        404: {"model": ErrorResponse, "description": "Member ID was not found."},
        422: {"model": ErrorResponse, "description": "The member ID format is invalid."},
        500: {"model": ErrorResponse, "description": "Unexpected server error."},
    },
    operation_id="getInsuranceEligibility",
    summary="Get insurance eligibility",
)
def get_insurance_eligibility(
    memberId: str = Path(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[A-Za-z0-9_-]+$",
        description="Fictional member ID, for example INS1001.",
    ),
) -> InsuranceEligibility:
    """Retrieve administrative eligibility. Does not confirm clinical coverage decisions."""
    try:
        return insurance_service.get_insurance_eligibility(memberId)
    except RecordNotFoundError:
        raise
    except Exception:
        logger.exception("Unexpected error while retrieving insurance eligibility.")
        raise
