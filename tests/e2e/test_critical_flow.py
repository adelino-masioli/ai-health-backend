def test_critical_flow_patient_vitals_analysis(client, api_headers):
    patient_payload = {"name": "Adelino Masioli", "email": "adelino@example.com"}
    patient_res = client.post("/api/v1/patients", json=patient_payload, headers=api_headers)
    assert patient_res.status_code == 201
    patient_id = patient_res.json()["id"]

    hr_payload = {
        "patient_id": patient_id,
        "value": 130,
        "timestamp": "2026-04-15T12:00:00Z",
    }
    hr_res = client.post("/api/v1/heart-rate", json=hr_payload, headers=api_headers)
    assert hr_res.status_code == 201

    steps_payload = {
        "patient_id": patient_id,
        "total": 120,
        "date": "2026-04-15T00:00:00Z",
    }
    steps_res = client.post("/api/v1/steps", json=steps_payload, headers=api_headers)
    assert steps_res.status_code == 201

    analysis_res = client.get(f"/api/v1/analysis/{patient_id}", headers=api_headers)
    assert analysis_res.status_code == 200
    body = analysis_res.json()
    assert body["patient_id"] == patient_id
    codes = {x["code"] for x in body["alerts"]}
    assert "tachycardia" in codes


def test_missing_api_key_returns_401(client):
    response = client.post(
        "/api/v1/patients",
        json={"name": "No Key", "email": "nokey@example.com"},
    )
    assert response.status_code == 401
    assert response.json()["code"] == "UNAUTHORIZED"
