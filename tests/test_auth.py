import pytest
import requests

@pytest.mark.auth
def test_register_new_user(unique_user_data, base_url):
    response = requests.post(f"{base_url}/api/v1/auth/register", json=unique_user_data, timeout=10)
    assert response.status_code == 201
    assert "email" in response.json()["user"]

@pytest.mark.negative
def test_register_duplicate_email():
    """Повторная регистрация с тем же email возвращает ошибку."""
    payload = {
        "email": "duplicate@example.com",
        "username": "user_one",
        "password": "securepass123"
    }

    # Первый раз — регистрация проходит
    requests.post(
        "http://localhost:8000/api/v1/auth/register",
        json=payload,
        timeout=5
    )

    # Второй раз — ожидаем ошибку
    payload["username"] = "user_two"  # другой username, но тот же email
    response = requests.post(
        "http://localhost:8000/api/v1/auth/register",
        json=payload,
        timeout=5
    )

    assert response.status_code in (400, 409, 422), (
        f"Ожидали ошибку 400/409/422, получили {response.status_code}"
    )

@pytest.mark.auth
def test_login_success(unique_user_data, base_url):
    response = requests.post(f"{base_url}/api/v1/auth/register", json=unique_user_data, timeout=10)
    response = requests.post(f"{base_url}/api/v1/auth/login", json=unique_user_data, timeout=10)
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.negative
def test_login_wrong_password(unique_user_data, base_url):
    payload = {
        "email": "duplicate@example.com",
        "username": "user_one",
        "password": "securepass123"
    }
    invalid_payload = {
        "email": "duplicate@example.com",
        "username": "user_one",
        "password": "wrongpass123"
    }
    response = requests.post(f"{base_url}/api/v1/auth/register", json=payload, timeout=10)
    response = requests.post(f"{base_url}/api/v1/auth/login", json=invalid_payload, timeout=10)
    assert response.status_code == 401

@pytest.mark.negative
def test_login_nonexistent_user(base_url):
    payload = {
        "email": "wrong@example.com",
        "username": "user_wrong",
        "password": "securepass123"
    }
    response = requests.post(f"{base_url}/api/v1/auth/login", json=payload, timeout=10)
    assert response.status_code == 401

@pytest.mark.parametrize("payload, expected_status", [
    pytest.param(
        {"email": "", "username": "u1", "password": "Pass123!"},
        422,
        id="empty_email"
    ),
    pytest.param(
        {"email": "not-an-email", "username": "u2", "password": "Pass123!"},
        422,
        id="invalid_email_format"
    ),
    pytest.param(
        {"email": "a@b.com", "username": "", "password": "12"},
        422,
        id="missing_username"
    ),
    pytest.param(
        {"email": "a@b.com", "username": "u2", "password": ""},
        422,
        id="missing_password"
    ),
    pytest.param(
        {},
        422,
        id="empty_body"
    ),
])

@pytest.mark.negative
def test_register_validation(api_session, base_url, payload, expected_status):
    response = api_session.post(
        f"{base_url}/api/v1/auth/register",
        json=payload,
        timeout=5
    )
    assert response.status_code == expected_status, f"Payload: {payload}, получили {response.status_code}"