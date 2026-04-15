def test_invalid_heart_rate_payload_returns_422(client, api_headers):
    patient_res = client.post(
        "/api/v1/patients",
        json={"name": "Validation User", "email": "validation@example.com"},
        headers=api_headers,
    )
    patient_id = patient_res.json()["id"]

    response = client.post(
        "/api/v1/heart-rate",
        json={"patient_id": patient_id, "value": 400, "timestamp": "2026-04-15T12:00:00Z"},
        headers=api_headers,
    )

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert body["errors"][0]["field"] == "value"


def test_unknown_patient_returns_404(client, api_headers):
    response = client.post(
        "/api/v1/steps",
        json={
            "patient_id": "00000000-0000-0000-0000-000000000000",
            "total": 100,
            "date": "2026-04-15T00:00:00Z",
        },
        headers=api_headers,
    )

    assert response.status_code == 404
    assert response.json()["code"] == "NOT_FOUND"
