"""
In-memory mock data for local development.

All IDs are fictional. Do not use real patient, member, or provider information.
Sample IDs are documented in README.md so Kore.ai and pytest can reuse the same records.
"""

from datetime import date

from app.models import (
    AppointmentStatus,
    EligibilityStatus,
    LabReportStatus,
    VerificationStatus,
)

# Appointment samples
# APT1001 CONFIRMED, reschedule and cancel allowed  (TC01, TC02)
# APT1002 RESCHEDULED — details already updated
# APT1003 CANCELLED
# APT1004 RESCHEDULE_NOT_ALLOWED (TC03)
# Unknown IDs such as APT9999 return NOT_FOUND (TC04)
APPOINTMENTS: dict[str, dict] = {
    "APT1001": {
        "appointmentId": "APT1001",
        "appointmentStatus": AppointmentStatus.CONFIRMED,
        "appointmentDate": date(2026, 10, 15),
        "appointmentTime": "09:30",
        "providerName": "Dr. Maya Chen",
        "appointmentType": "Primary care follow-up",
        "rescheduleEligible": True,
        "cancellationEligible": True,
        "nextAdministrativeStep": "Share the confirmed date, time, and provider. Offer reschedule or cancel if the caller asks.",
        "handoffRecommended": False,
    },
    "APT1002": {
        "appointmentId": "APT1002",
        "appointmentStatus": AppointmentStatus.RESCHEDULED,
        "appointmentDate": date(2026, 10, 22),
        "appointmentTime": "14:00",
        "providerName": "Dr. Maya Chen",
        "appointmentType": "Primary care follow-up",
        "rescheduleEligible": True,
        "cancellationEligible": True,
        "nextAdministrativeStep": "Share the updated date and time. Confirm the caller has the new details.",
        "handoffRecommended": False,
    },
    "APT1003": {
        "appointmentId": "APT1003",
        "appointmentStatus": AppointmentStatus.CANCELLED,
        "appointmentDate": date(2026, 10, 10),
        "appointmentTime": "11:00",
        "providerName": "Dr. Luis Ortega",
        "appointmentType": "Annual wellness visit",
        "rescheduleEligible": False,
        "cancellationEligible": False,
        "nextAdministrativeStep": "Inform the caller that this appointment is cancelled. Offer to help them book a new visit if they ask.",
        "handoffRecommended": False,
    },
    "APT1004": {
        "appointmentId": "APT1004",
        "appointmentStatus": AppointmentStatus.RESCHEDULE_NOT_ALLOWED,
        "appointmentDate": date(2026, 10, 18),
        "appointmentTime": "08:00",
        "providerName": "Dr. Priya Nair",
        "appointmentType": "Procedure pre-check",
        "rescheduleEligible": False,
        "cancellationEligible": False,
        "nextAdministrativeStep": "Self-service reschedule is not allowed. Transfer to a scheduling representative.",
        "handoffRecommended": True,
    },
}

# Insurance samples
# INS1001 ACTIVE + VERIFIED (TC05)
# INS1002 INACTIVE (TC06)
# INS1003 VERIFICATION_REQUIRED — verificationStatus is never VERIFIED (TC07)
# INS1004 PAYER_MISMATCH
# Unknown IDs such as INS9999 return NOT_FOUND
INSURANCE_RECORDS: dict[str, dict] = {
    "INS1001": {
        "memberId": "INS1001",
        "eligibilityStatus": EligibilityStatus.ACTIVE,
        "payerName": "Northwind Health",
        "planName": "Northwind PPO Gold",
        "effectiveDate": date(2026, 1, 1),
        "expirationDate": date(2026, 12, 31),
        "verificationStatus": VerificationStatus.VERIFIED,
        "nextAdministrativeStep": "Eligibility is active and verified. Share payer, plan, and effective dates only.",
        "handoffRecommended": False,
    },
    "INS1002": {
        "memberId": "INS1002",
        "eligibilityStatus": EligibilityStatus.INACTIVE,
        "payerName": "Northwind Health",
        "planName": "Northwind PPO Gold",
        "effectiveDate": date(2025, 1, 1),
        "expirationDate": date(2025, 12, 31),
        "verificationStatus": VerificationStatus.VERIFIED,
        "nextAdministrativeStep": "Coverage is inactive. Offer a billing or insurance representative for next steps.",
        "handoffRecommended": True,
    },
    "INS1003": {
        "memberId": "INS1003",
        "eligibilityStatus": EligibilityStatus.VERIFICATION_REQUIRED,
        "payerName": "Summit Care",
        "planName": "Summit HMO Standard",
        "effectiveDate": date(2026, 3, 1),
        "expirationDate": date(2026, 12, 31),
        "verificationStatus": VerificationStatus.PENDING,
        "nextAdministrativeStep": "Do not state that coverage is verified. Transfer to an insurance verification representative.",
        "handoffRecommended": True,
    },
    "INS1004": {
        "memberId": "INS1004",
        "eligibilityStatus": EligibilityStatus.PAYER_MISMATCH,
        "payerName": "Lakeside Mutual",
        "planName": "Lakeside Choice Plus",
        "effectiveDate": date(2026, 1, 1),
        "expirationDate": date(2026, 12, 31),
        "verificationStatus": VerificationStatus.FAILED,
        "nextAdministrativeStep": "The payer on file does not match the caller details. Transfer to insurance support.",
        "handoffRecommended": True,
    },
}

# Lab report samples — administrative availability only
# LAB1001 PROCESSING (TC08)
# LAB1002 AVAILABLE (TC09)
# LAB1003 DELAYED (TC10)
# LAB1004 ACCESS_ERROR
# Unknown IDs such as LAB9999 return NOT_FOUND
LAB_REPORTS: dict[str, dict] = {
    "LAB1001": {
        "reportId": "LAB1001",
        "reportStatus": LabReportStatus.PROCESSING,
        "testName": "Routine blood panel",
        "collectionDate": date(2026, 10, 6),
        "expectedAvailableDate": date(2026, 10, 9),
        "reportAvailable": False,
        "deliveryMethod": "Patient portal",
        "nextAdministrativeStep": "The report is still processing. Share the expected available date. Do not discuss results.",
        "handoffRecommended": False,
    },
    "LAB1002": {
        "reportId": "LAB1002",
        "reportStatus": LabReportStatus.AVAILABLE,
        "testName": "Routine blood panel",
        "collectionDate": date(2026, 10, 1),
        "expectedAvailableDate": date(2026, 10, 4),
        "reportAvailable": True,
        "deliveryMethod": "Patient portal",
        "nextAdministrativeStep": "The report is available through the stated delivery method. Do not interpret results.",
        "handoffRecommended": False,
    },
    "LAB1003": {
        "reportId": "LAB1003",
        "reportStatus": LabReportStatus.DELAYED,
        "testName": "Imaging follow-up",
        "collectionDate": date(2026, 9, 28),
        "expectedAvailableDate": date(2026, 10, 12),
        "reportAvailable": False,
        "deliveryMethod": "Mail and patient portal",
        "nextAdministrativeStep": "The report is delayed. Transfer to a lab-support representative if the caller needs more help.",
        "handoffRecommended": True,
    },
    "LAB1004": {
        "reportId": "LAB1004",
        "reportStatus": LabReportStatus.ACCESS_ERROR,
        "testName": "Routine blood panel",
        "collectionDate": date(2026, 10, 3),
        "expectedAvailableDate": date(2026, 10, 6),
        "reportAvailable": False,
        "deliveryMethod": None,
        "nextAdministrativeStep": "There is an access problem. Transfer to a representative. Do not attempt identity workarounds.",
        "handoffRecommended": True,
    },
}
