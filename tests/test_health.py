import pytest

@pytest.mark.smoke
def test_health_status_code(api_session, config):
    response = api_session.get(f"{config.BASE_URL}/health", timeout=5)
    assert response.status_code == 200

@pytest.mark.smoke
def test_health_response_body(api_session, config):
    response = api_session.get(f"{config.BASE_URL}/health", timeout=5)
    assert "status" in response.json(), f"Нет ключа 'status'. Ключи: {list(response.json().keys())}"

@pytest.mark.smoke
def test_health_response_headers(api_session, config):
    response = api_session.get(f"{config.BASE_URL}/health", timeout=5)
    assert "application/json" in response.headers["content-type"]

@pytest.mark.smoke
def test_health_response_time(api_session, config):
    response = api_session.get(f"{config.BASE_URL}/health", timeout=5)
    assert response.elapsed.total_seconds() < 1