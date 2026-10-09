# Healthcare Customer Service Automation API

Python FastAPI backend for the **Pronix Kore.ai XO 11 Junior Developer Assignment**.

This service provides administrative customer-service data for three use cases:

1. Appointment Management
2. Insurance Eligibility and Coverage Status
3. Lab Report Status

The API uses **fictional mock data only**. It does not connect to hospital systems, paid services, or real patient records.

Kore.ai XO 11 should treat this API as the source of truth and choose the next conversational action from the returned **business status**. Transfer wording stays in Kore.ai. This backend returns structured statuses, eligibility flags, and a `handoffRecommended` hint.

## Project layout

```
healthcare-customer-service/
  app/
    main.py                 # FastAPI app, logging, error handlers
    models.py               # Pydantic response models
    data.py                 # In-memory mock records
    exceptions.py           # NOT_FOUND and error envelope
    services/               # Business logic (no HTTP)
    routers/                # REST endpoints
  tests/                    # pytest + TestClient
  requirements.txt
  README.md
  .env.example
  .gitignore
```

## 1. Install Python (Windows)

1. Install Python 3.11 or newer from https://www.python.org/downloads/
2. During setup, check **Add python.exe to PATH**.
3. Open **PowerShell** and verify:

```powershell
python --version
```

You should see `Python 3.11.x` or higher.

## 2. Create and activate a virtual environment

In PowerShell, go to this folder:

```powershell
cd "a:\assignment projects\pronix\healthcare-customer-service"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Windows blocks the activate script, run this once for your user, then try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Your prompt should show `(.venv)`.

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Optional local settings:

```powershell
Copy-Item .env.example .env
```

## 4. Start the FastAPI server

From `healthcare-customer-service` with the venv active:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Leave this window open while you test.

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

## 5. Open Swagger UI

In a browser, open:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

OpenAPI JSON is at [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

## 6. Test all three endpoints in Swagger

1. Expand **Appointments** → `GET /appointments/{appointmentId}` (`getAppointmentDetails`).
2. Click **Try it out**, enter `APT1001`, click **Execute**. Expect HTTP 200 and `CONFIRMED`.
3. Repeat with `APT9999`. Expect HTTP 404 and `error.code = NOT_FOUND`.
4. Expand **Insurance** → `GET /insurance/{memberId}` (`getInsuranceEligibility`). Try `INS1001`.
5. Expand **Lab Reports** → `GET /lab-reports/{reportId}` (`getLabReportStatus`). Try `LAB1001`.

PowerShell examples:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/appointments/APT1001
Invoke-RestMethod http://127.0.0.1:8000/insurance/INS1001
Invoke-RestMethod http://127.0.0.1:8000/lab-reports/LAB1001
```

## 7. Run pytest

In a **second** PowerShell window (venv activated, same folder):

```powershell
pytest
```

Verbose:

```powershell
pytest -v
```

## Mock IDs (fictional)

### Appointments — `GET /appointments/{appointmentId}`

| Sample ID | HTTP | Business outcome | Notes |
|-----------|------|------------------|--------|
| APT1001 | 200 | CONFIRMED | Reschedule and cancel allowed (TC01, TC02) |
| APT1002 | 200 | RESCHEDULED | Updated date/time already applied |
| APT1003 | 200 | CANCELLED | No further self-service change |
| APT1004 | 200 | RESCHEDULE_NOT_ALLOWED | Restriction + handoff hint (TC03) |
| APT9999 | 404 | NOT_FOUND | Unknown ID (TC04) |

This endpoint is **retrieve-only**. It does not reschedule or cancel appointments.

### Insurance — `GET /insurance/{memberId}`

| Sample ID | HTTP | eligibilityStatus | verificationStatus | Notes |
|-----------|------|-------------------|--------------------|--------|
| INS1001 | 200 | ACTIVE | VERIFIED | TC05 |
| INS1002 | 200 | INACTIVE | VERIFIED | Coverage dates expired (TC06) |
| INS1003 | 200 | VERIFICATION_REQUIRED | PENDING | Never claimed as verified (TC07) |
| INS1004 | 200 | PAYER_MISMATCH | FAILED | Human assistance recommended |
| INS9999 | 404 | — | — | NOT_FOUND |

### Lab reports — `GET /lab-reports/{reportId}`

Administrative availability only. **No clinical values, diagnoses, or treatment advice.**

| Sample ID | HTTP | reportStatus | reportAvailable | Notes |
|-----------|------|--------------|-----------------|--------|
| LAB1001 | 200 | PROCESSING | false | TC08 |
| LAB1002 | 200 | AVAILABLE | true | TC09 |
| LAB1003 | 200 | DELAYED | false | Handoff recommended (TC10) |
| LAB1004 | 200 | ACCESS_ERROR | false | Handoff recommended |
| LAB9999 | 404 | — | — | NOT_FOUND |

## HTTP vs business outcomes

Kore.ai must distinguish **business outcomes** (usually HTTP 200 with a status field) from **technical errors**.

| Situation | HTTP | Body |
|-----------|------|------|
| Known record, any business status | 200 | Resource JSON |
| Unknown ID | 404 | `{ "error": { "code": "NOT_FOUND", "message": "..." } }` |
| Invalid ID format (spaces, symbols) | 422 | `{ "error": { "code": "INVALID_INPUT", "message": "..." } }` |
| Unexpected server failure | 500 | `{ "error": { "code": "INTERNAL_ERROR", "message": "..." } }` |

HTTP 200 is **not** used for missing records.

### Error envelope example

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "The requested record could not be found.",
    "details": {
      "resource": "appointment"
    }
  }
}
```

500 responses never include stack traces or internal exception text.

## Operation contracts for Kore.ai

Do not hard-code `localhost` in a cloud-hosted Kore.ai bot. Deploy first, then paste the **public HTTPS** base URL.

Tool-compatible operation names:

- `getAppointmentDetails`
- `getInsuranceEligibility`
- `getLabReportStatus`

### getAppointmentDetails

- **Method:** GET
- **Path:** `/appointments/{appointmentId}`
- **Example:** `GET https://YOUR-HTTPS-HOST/appointments/APT1001`
- **Success:** 200
- **Not found:** 404

Sample 200 body (`APT1001`):

```json
{
  "appointmentId": "APT1001",
  "appointmentStatus": "CONFIRMED",
  "appointmentDate": "2026-10-15",
  "appointmentTime": "09:30",
  "providerName": "Dr. Maya Chen",
  "appointmentType": "Primary care follow-up",
  "rescheduleEligible": true,
  "cancellationEligible": true,
  "nextAdministrativeStep": "Share the confirmed date, time, and provider. Offer reschedule or cancel if the caller asks.",
  "handoffRecommended": false
}
```

### getInsuranceEligibility

- **Method:** GET
- **Path:** `/insurance/{memberId}`
- **Example:** `GET https://YOUR-HTTPS-HOST/insurance/INS1001`
- **Success:** 200
- **Not found:** 404

Sample 200 body (`INS1001`):

```json
{
  "memberId": "INS1001",
  "eligibilityStatus": "ACTIVE",
  "payerName": "Northwind Health",
  "planName": "Northwind PPO Gold",
  "effectiveDate": "2026-01-01",
  "expirationDate": "2026-12-31",
  "verificationStatus": "VERIFIED",
  "nextAdministrativeStep": "Eligibility is active and verified. Share payer, plan, and effective dates only.",
  "handoffRecommended": false
}
```

### getLabReportStatus

- **Method:** GET
- **Path:** `/lab-reports/{reportId}`
- **Example:** `GET https://YOUR-HTTPS-HOST/lab-reports/LAB1001`
- **Success:** 200
- **Not found:** 404

Sample 200 body (`LAB1001`):

```json
{
  "reportId": "LAB1001",
  "reportStatus": "PROCESSING",
  "testName": "Routine blood panel",
  "collectionDate": "2026-10-06",
  "expectedAvailableDate": "2026-10-09",
  "reportAvailable": false,
  "deliveryMethod": "Patient portal",
  "nextAdministrativeStep": "The report is still processing. Share the expected available date. Do not discuss results.",
  "handoffRecommended": false
}
```

## 8. Expose the backend over HTTPS for Kore.ai

A Kore.ai cloud bot **cannot** call `http://127.0.0.1:8000` on your PC.

After local tests pass:

1. Deploy this FastAPI app to a host you control (for example Azure App Service, AWS, or a VM behind a reverse proxy).
2. Serve it on **HTTPS** with a valid certificate.
3. Confirm the public URL, for example `https://api.example.com/health`, returns `{ "status": "ok" }`.
4. Restrict who can call the API if your assignment allows it (IP allowlist, API key header, or similar). This mock version does not ship authentication.
5. Do not put real PHI, credentials, or clinical results in this mock service.

Local tunnel tools (ngrok, Cloudflare Tunnel, and similar) can expose HTTPS for a demo. Use them only with mock IDs, and stop the tunnel when you finish.

## 9. Configure Kore.ai XO 11 REST Service nodes

Configure these **after** the public HTTPS URL works.

In Kore.ai XO 11, create three **Service** (Custom Service / REST) nodes. Use GET and a **path parameter**. Map the entity the bot collected to the path.

| Operation | Method | URL template |
|-----------|--------|----------------|
| getAppointmentDetails | GET | `https://YOUR-HTTPS-HOST/appointments/{{context.appointmentId}}` |
| getInsuranceEligibility | GET | `https://YOUR-HTTPS-HOST/insurance/{{context.memberId}}` |
| getLabReportStatus | GET | `https://YOUR-HTTPS-HOST/lab-reports/{{context.reportId}}` |

Use the actual variable names from your bot. Timeout should be long enough for a normal GET (for example 10 seconds).

### Suggested bot branching (implemented in Kore.ai, not in Python)

**Appointments**

- `appointmentStatus = CONFIRMED` and `rescheduleEligible = true` → share details; allow reschedule/cancel talk tracks.
- `RESCHEDULED` → share updated date/time.
- `CANCELLED` → explain cancelled status.
- `RESCHEDULE_NOT_ALLOWED` or `handoffRecommended = true` → scheduling handoff.
- HTTP 404 / `NOT_FOUND` → ask the user to verify the appointment ID, then retry or escalate.
- HTTP 5xx or backend failure → representative handoff.

**Insurance**

- `ACTIVE` + `VERIFIED` → share administrative eligibility only.
- `INACTIVE` → human assistance.
- `VERIFICATION_REQUIRED` → **do not** say coverage is verified; transfer.
- `PAYER_MISMATCH` → transfer.
- HTTP 404 → verify member ID, retry, then escalate.
- HTTP 5xx → transfer.

**Lab reports**

- `PROCESSING` → share expected date only. No results.
- `AVAILABLE` → point to `deliveryMethod`. No interpretation.
- `DELAYED` or `ACCESS_ERROR` → lab-support handoff.
- HTTP 404 → verify report ID, retry, then escalate.
- HTTP 5xx → transfer.

**Handoff context (administrative only)**

Pass IDs, statuses, the issue reported, and `nextAdministrativeStep`. Do **not** pass clinical values, diagnoses, passwords, or extra identity documents.

**Explicit “talk to a person”** is a Kore.ai intent (TC11), not a Python endpoint.

**Context retention across turns** (TC12) is bot dialog context, not this API.

## Automated tests vs Kore.ai tests

| ID | Scenario | Where it is tested |
|----|----------|--------------------|
| TC01 | Appointment CONFIRMED | `tests/test_appointments.py` |
| TC02 | Reschedule request for an eligible appointment | Backend flags on APT1001; bot must still implement the reschedule dialog |
| TC03 | Rescheduling restricted | APT1004 |
| TC04 | Appointment NOT_FOUND | APT9999 |
| TC05 | Insurance ACTIVE and VERIFIED | INS1001 |
| TC06 | Insurance INACTIVE | INS1002 |
| TC07 | Insurance VERIFICATION_REQUIRED | INS1003 |
| TC08 | Lab PROCESSING | LAB1001 |
| TC09 | Lab AVAILABLE | LAB1002 |
| TC10 | Lab DELAYED | LAB1003 |
| TC11 | Explicit request for a human representative | **Kore.ai conversation test only** |
| TC12 | Context retention across turns | **Kore.ai conversation test only** |

Extra backend coverage: payer mismatch, lab access error, malformed IDs (422), unexpected errors (500).

**TC11 and TC12 are not fully tested by backend unit tests.**

## Remaining Kore.ai work (checklist)

Use this after the local API and pytest are green.

- [ ] Deploy API to a public HTTPS URL
- [ ] Confirm `/health`, `/docs`, and the three GET operations on the deployed host
- [ ] Create REST Service nodes for the three operation names
- [ ] Map path parameters from bot entities
- [ ] Branch on HTTP status **and** business status fields
- [ ] Appointment restriction / exception / 5xx / “representative” → scheduling transfer
- [ ] Insurance verification failure, payer mismatch, 5xx, “representative” → insurance transfer
- [ ] Lab delay, access error, identity/access issue, 5xx, “representative” → lab transfer
- [ ] NOT_FOUND → verify ID, retry, then escalate
- [ ] Keep clinical interpretation out of bot replies
- [ ] Handoff payload: IDs, statuses, issue only
- [ ] Conversation tests for TC11 and TC12
- [ ] End-to-end tests with the sample IDs above
- [ ] 15-minute walkthrough: start API (or open deployed URL), show Swagger, show pytest, show one Kore.ai path per use case, show one handoff

## 15-minute walkthrough outline

1. Show `python --version`, venv, `pip install -r requirements.txt`.
2. Start uvicorn and open Swagger.
3. Call APT1001, APT1004, APT9999.
4. Call INS1001, INS1003, INS1004.
5. Call LAB1001, LAB1002, LAB1003, LAB1004.
6. Run `pytest -v`.
7. Show the deployed HTTPS URL (when ready) and one Kore.ai Service node.
8. Demo one happy path and one transfer path in the bot.

## License / data notice

Mock names and IDs are invented for this assignment. Do not replace them with real patient data.
