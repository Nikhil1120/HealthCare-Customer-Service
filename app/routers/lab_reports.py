"""Lab report status endpoints for Kore.ai Custom Service nodes."""

import logging

from fastapi import APIRouter, Path

from app.exceptions import RecordNotFoundError
from app.models import ErrorResponse, LabReportStatusResponse
from app.services import lab_report_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lab-reports", tags=["Lab Reports"])


@router.get(
    "/{reportId}",
    response_model=LabReportStatusResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Report ID was not found."},
        422: {"model": ErrorResponse, "description": "The report ID format is invalid."},
        500: {"model": ErrorResponse, "description": "Unexpected server error."},
    },
    operation_id="getLabReportStatus",
    summary="Get lab report status",
)
def get_lab_report_status(
    reportId: str = Path(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[A-Za-z0-9_-]+$",
        description="Fictional report ID, for example LAB1001.",
    ),
) -> LabReportStatusResponse:
    """Retrieve administrative availability only. Never returns clinical values or diagnoses."""
    try:
        return lab_report_service.get_lab_report_status(reportId)
    except RecordNotFoundError:
        raise
    except Exception:
        logger.exception("Unexpected error while retrieving lab report status.")
        raise
