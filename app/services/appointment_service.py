"""Appointment lookup logic. This module is retrieve-only; no reschedule or cancel mutations."""

from app.data import APPOINTMENTS
from app.exceptions import RecordNotFoundError
from app.models import AppointmentDetails


def get_appointment_details(appointment_id: str) -> AppointmentDetails:
    record = APPOINTMENTS.get(appointment_id)
    if record is None:
        raise RecordNotFoundError("appointment", appointment_id)
    return AppointmentDetails.model_validate(record)
