"""Appointment Management endpoints for Kore.ai Custom Service nodes."""

import logging

from fastapi import APIRouter, Path

from app.exceptions import RecordNotFoundError
from app.models import AppointmentDetails, ErrorResponse
from app.services import appointment_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get(
    "/{appointmentId}",
    response_model=AppointmentDetails,
    responses={
        404: {"model": ErrorResponse, "description": "Appointment ID was not found."},
        422: {"model": ErrorResponse, "description": "The appointment ID format is invalid."},
        500: {"model": ErrorResponse, "description": "Unexpected server error."},
    },
    operation_id="getAppointmentDetails",
    summary="Get appointment details",
)
def get_appointment_details(
    appointmentId: str = Path(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[A-Za-z0-9_-]+$",
        description="Fictional appointment ID, for example APT1001.",
    ),
) -> AppointmentDetails:
    """Retrieve administrative appointment details. Does not reschedule or cancel."""
    try:
        return appointment_service.get_appointment_details(appointmentId)
    except RecordNotFoundError:
        raise
    except Exception:
        logger.exception("Unexpected error while retrieving appointment details.")
        raise
