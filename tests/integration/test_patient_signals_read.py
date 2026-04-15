def test_list_heart_rates_returns_patient_records(client, api_headers):
    patient = client.post(
        "/api/v1/patients",
        json={"name": "Signal User", "email": "signals@example.com"},
        headers=api_headers,
    ).json()

    client.post(
        "/api/v1/heart-rate",
        json={"patient_id": patient["id"], "value": 72, "timestamp": "2026-04-15T12:00:00Z"},
        headers=api_headers,
    )

    response = client.get(f"/api/v1/heart-rate/{patient['id']}", headers=api_headers)

    assert response.status_code == 200
    assert response.json()[0]["value"] == 72


def test_list_steps_returns_patient_records(client, api_headers):
    patient = client.post(
        "/api/v1/patients",
        json={"name": "Steps User", "email": "steps@example.com"},
        headers=api_headers,
    ).json()

    client.post(
        "/api/v1/steps",
        json={"patient_id": patient["id"], "total": 8450, "date": "2026-04-15T00:00:00Z"},
        headers=api_headers,
    )

    response = client.get(f"/api/v1/steps/{patient['id']}", headers=api_headers)

    assert response.status_code == 200
    assert response.json()[0]["total"] == 8450
