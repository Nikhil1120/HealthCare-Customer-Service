"""
FastAPI entry point for the Healthcare Customer Service Automation API.

Start locally:
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import RecordNotFoundError, error_payload
from app.routers import appointments, insurance, lab_reports

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("healthcare-customer-service")

app = FastAPI(
    title="Healthcare Customer Service Automation API",
    description=(
        "Administrative backend for Kore.ai XO 11. "
        "Supports appointment details, insurance eligibility, and lab-report availability. "
        "Uses fictional mock data only. Deploy to a public HTTPS URL before connecting Kore.ai."
    ),
    version="1.0.0",
)


@app.exception_handler(RecordNotFoundError)
async def not_found_handler(request: Request, exc: RecordNotFoundError) -> JSONResponse:
    # Business NOT_FOUND: HTTP 404 so Kore.ai can tell it apart from HTTP 200 outcomes.
    logger.info("Record not found for path %s", request.url.path)
    return JSONResponse(
        status_code=404,
        content=error_payload(
            "NOT_FOUND",
            "The requested record could not be found.",
            {"resource": exc.resource},
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.info("Invalid request for path %s", request.url.path)
    return JSONResponse(
        status_code=422,
        content=error_payload(
            "INVALID_INPUT",
            "The request could not be validated. Check the ID format and try again.",
        ),
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    # Do not include stack traces, secrets, or internal details in the response.
    logger.exception("Unexpected server error for path %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content=error_payload(
            "INTERNAL_ERROR",
            "An unexpected error occurred. Please try again or request a human representative.",
        ),
    )


app.include_router(appointments.router)
app.include_router(insurance.router)
app.include_router(lab_reports.router)


@app.get("/health", tags=["Health"], operation_id="healthCheck")
def health_check() -> dict[str, str]:
    """Simple liveness check for local runs and later HTTPS deployments."""
    return {"status": "ok"}


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent
