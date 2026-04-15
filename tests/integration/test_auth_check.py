def test_auth_check_returns_200_for_valid_api_key(client, api_headers):
    response = client.get("/api/v1/auth/check", headers=api_headers)

    assert response.status_code == 200
    assert response.json() == {"authenticated": True}


def test_auth_check_returns_401_without_api_key(client):
    response = client.get("/api/v1/auth/check")

    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "UNAUTHORIZED"
