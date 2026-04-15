# AI Health Monitor Backend

FastAPI backend for patient registration, vitals ingestion and anomaly analysis consumed by the `ai-health-frontend` app.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- SQLite (local/dev)
- Pydantic v2
- Uvicorn
- Pytest

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- Health: `http://localhost:8000/health`

## Authentication

All business endpoints require API key header:

`X-API-Key: <your_key>`

Configure key(s) via `.env` (`API_KEYS=dev-api-key,another-key`).

## Environment variables

- `DATABASE_URL` (default `sqlite:///./data/health.db`)
- `ENVIRONMENT` (`development` | `production`)
- `API_KEYS` (comma-separated)
- `CORS_ORIGINS` (comma-separated)
- `RATE_LIMIT_REQUESTS`
- `RATE_LIMIT_WINDOW_SECONDS`

## Contracted endpoints (`/api/v1`)

- `POST /patients`
  - body: `{ "name": "...", "email": "..." }`
  - returns `201` with patient object
- `POST /heart-rate`
  - body: `{ "patient_id": "uuid", "value": 72, "timestamp": "2026-01-30T10:15:00Z" }`
  - returns `201`
- `POST /steps`
  - body: `{ "patient_id": "uuid", "total": 8450, "date": "2026-01-30T00:00:00Z" }`
  - returns `201`
- `GET /analysis/{patient_id}?window_hours=24`
  - returns `200` with alerts

## Error format

Errors are standardized:

```json
{
  "detail": "Validation failed",
  "code": "VALIDATION_ERROR",
  "errors": [{"field": "value", "message": "Input should be less than or equal to 220"}]
}
```

Other errors:

```json
{
  "detail": "Patient not found",
  "code": "NOT_FOUND",
  "field": "patient_id"
}
```

## Tests

```bash
pytest
```

Includes unit, integration and e2e test flow:

1. create patient
2. send heart-rate and steps
3. fetch analysis

## Frontend integration flow

1. Create patient once in `POST /api/v1/patients`
2. Sync each pending local record to:
   - `POST /api/v1/heart-rate`
   - `POST /api/v1/steps`
3. Read alerts in `GET /api/v1/analysis/{patient_id}`

Swagger is the source-of-truth contract used by frontend integration.
