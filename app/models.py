"""Pydantic request and response models shared by routers and services."""

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AppointmentStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    RESCHEDULED = "RESCHEDULED"
    CANCELLED = "CANCELLED"
    RESCHEDULE_NOT_ALLOWED = "RESCHEDULE_NOT_ALLOWED"


class EligibilityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    VERIFICATION_REQUIRED = "VERIFICATION_REQUIRED"
    PAYER_MISMATCH = "PAYER_MISMATCH"


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    PENDING = "PENDING"
    FAILED = "FAILED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class LabReportStatus(str, Enum):
    PROCESSING = "PROCESSING"
    AVAILABLE = "AVAILABLE"
    DELAYED = "DELAYED"
    ACCESS_ERROR = "ACCESS_ERROR"


class AppointmentDetails(BaseModel):
    """Administrative appointment details returned to Kore.ai."""

    appointmentId: str
    appointmentStatus: AppointmentStatus
    appointmentDate: Optional[date] = None
    appointmentTime: Optional[str] = Field(
        default=None,
        description="Local appointment time in 24-hour HH:MM format.",
    )
    providerName: Optional[str] = None
    appointmentType: Optional[str] = None
    rescheduleEligible: bool
    cancellationEligible: bool
    nextAdministrativeStep: str = Field(
        ...,
        description="Suggested next administrative action for the bot. Not clinical advice.",
    )
    handoffRecommended: bool = Field(
        ...,
        description="True when Kore.ai should consider a human-representative transfer.",
    )


class InsuranceEligibility(BaseModel):
    """Administrative insurance eligibility details. Never claims coverage is verified when it is not."""

    memberId: str
    eligibilityStatus: EligibilityStatus
    payerName: Optional[str] = None
    planName: Optional[str] = None
    effectiveDate: Optional[date] = None
    expirationDate: Optional[date] = None
    verificationStatus: VerificationStatus
    nextAdministrativeStep: str
    handoffRecommended: bool


class LabReportStatusResponse(BaseModel):
    """Administrative lab-report availability only. No clinical values or diagnoses."""

    reportId: str
    reportStatus: LabReportStatus
    testName: Optional[str] = None
    collectionDate: Optional[date] = None
    expectedAvailableDate: Optional[date] = None
    reportAvailable: bool
    deliveryMethod: Optional[str] = None
    nextAdministrativeStep: str
    handoffRecommended: bool


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
