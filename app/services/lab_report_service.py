"""Lab report availability lookup. Administrative status only — no clinical interpretation."""

from app.data import LAB_REPORTS
from app.exceptions import RecordNotFoundError
from app.models import LabReportStatusResponse


def get_lab_report_status(report_id: str) -> LabReportStatusResponse:
    record = LAB_REPORTS.get(report_id)
    if record is None:
        raise RecordNotFoundError("lab report", report_id)
    return LabReportStatusResponse.model_validate(record)
