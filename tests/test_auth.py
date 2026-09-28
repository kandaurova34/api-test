import pytest
import uuid

@pytest.mark.auth
def test_register_new_user(auth_client, unique_user_data):
    response = auth_client.register(**unique_user_data)
    assert response.status_code == 201
    assert "email" in response.json()["user"]

@pytest.mark.negative
def test_register_duplicate_email(auth_client, unique_user_data):
    """Повторная регистрация с тем же email возвращает ошибку."""
    origin = auth_client.register(**unique_user_data)
    assert origin.status_code == 201

    duplicate = {**unique_user_data, "username": unique_user_data["username"] + "_2"}
    response = auth_client.register(**duplicate)

    assert response.status_code in (400, 409, 422), (
        f"Ожидали ошибку 400/409/422, получили {response.status_code}"
    )

@pytest.mark.auth
def test_login_success(auth_client, unique_user_data):
    auth_client.register(**unique_user_data)
    login_resp = auth_client.login(unique_user_data["username"], unique_user_data["password"])
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

@pytest.mark.negative
def test_login_wrong_password(unique_user_data, auth_client):
    auth_client.register(**unique_user_data)
    response = auth_client.login(unique_user_data["username"], "WrongPass999!")
    assert response.status_code == 401

@pytest.mark.negative
def test_login_nonexistent_user(auth_client):
    nonexistent = f"nonexistent_{uuid.uuid4().hex[:8]}"
    response = auth_client.login(nonexistent, "SomePass123!")
    assert response.status_code == 401

@pytest.mark.negative
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
        {"email": "a@b.com", "password": "12"},
        422,
        id="missing_username"
    ),
    pytest.param(
        {"email": "a@b.com", "username": "u2"},
        422,
        id="missing_password"
    ),
    pytest.param(
        {},
        422,
        id="empty_body"
    ),
])
def test_register_validation(auth_client, payload, expected_status):
    response = auth_client.register_raw(payload)
    assert response.status_code == expected_status, (
        f"Payload: {payload}, получили {response.status_code}"
    )