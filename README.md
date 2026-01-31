# AI Health Monitor Backend

REST API to receive, validate and store health data sent from the Flutter mobile app (AI Health Monitor).

## Stack

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- SQLite
- Pydantic 2.x

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. (Optional) Environment variables:

   - `DATABASE_URL`: SQLite database path (default: `sqlite:///./data/health.db`)
   - `ENVIRONMENT`: `development` or `production` (default: `development`)

   Create a `.env` file in the project root if needed.

## Run

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/v1/heart-rate` | Create heart rate record. Body: `{ "value": int (30-220), "timestamp": "ISO8601" }` |
| GET    | `/api/v1/heart-rate` | List heart rate records. Query: `limit`, `offset` |
| POST   | `/api/v1/steps`      | Create steps record. Body: `{ "total": int (0-100000), "date": "YYYY-MM-DD" }` |
| GET    | `/api/v1/steps`      | List steps records. Query: `limit`, `offset` |

Invalid payloads (out of range, missing fields, invalid date format) return **422** with a clear message.

## Testing with curl

```bash
# Heart rate
curl -X POST http://localhost:8000/api/v1/heart-rate \
  -H "Content-Type: application/json" \
  -d '{"value": 72, "timestamp": "2026-01-30T10:15:00"}'

# Steps
curl -X POST http://localhost:8000/api/v1/steps \
  -H "Content-Type: application/json" \
  -d '{"total": 8450, "date": "2026-01-30"}'

# List
curl http://localhost:8000/api/v1/heart-rate
curl http://localhost:8000/api/v1/steps
```

## Frontend integration

The mobile app currently sends data to a single `POST /health` endpoint with an aggregated payload. This API exposes separate endpoints:

- `POST /api/v1/heart-rate` — one request per heart rate record
- `POST /api/v1/steps` — one request per steps record

To integrate the Flutter app with this backend:

1. Set the API base URL (e.g. `http://localhost:8000` for dev, or your deployed URL).
2. Update the app's API client to call `POST /api/v1/heart-rate` with `{ "value", "timestamp" }` and `POST /api/v1/steps` with `{ "total", "date" }` instead of a single `POST /health` with a combined body.

After that, the existing sync flow (sending pending local records one by one) will work against this API.
