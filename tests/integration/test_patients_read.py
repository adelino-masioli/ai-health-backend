def test_list_patients_returns_created_records_in_desc_order(client, api_headers):
    first = client.post(
        "/api/v1/patients",
        json={"name": "Maria Silva", "email": "maria@example.com"},
        headers=api_headers,
    )
    second = client.post(
        "/api/v1/patients",
        json={"name": "Arthur Sterling", "email": "arthur@example.com"},
        headers=api_headers,
    )

    response = client.get("/api/v1/patients", headers=api_headers)

    assert response.status_code == 200
    body = response.json()
    assert [item["id"] for item in body] == [second.json()["id"], first.json()["id"]]


def test_list_patients_requires_api_key(client):
    response = client.get("/api/v1/patients")

    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "UNAUTHORIZED"


def test_get_patient_returns_patient_by_id(client, api_headers):
    created = client.post(
        "/api/v1/patients",
        json={"name": "Julianne Abernathy", "email": "julianne@example.com"},
        headers=api_headers,
    )

    response = client.get(f"/api/v1/patients/{created.json()['id']}", headers=api_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "julianne@example.com"


def test_get_patient_returns_404_for_unknown_id(client, api_headers):
    response = client.get(
        "/api/v1/patients/00000000-0000-0000-0000-000000000000",
        headers=api_headers,
    )

    assert response.status_code == 404
    assert response.json()["code"] == "NOT_FOUND"
