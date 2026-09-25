import pytest
import requests

@pytest.mark.smoke
def test_health(base_url):
    response = requests.get(f"{base_url}/health",  timeout=5)
    assert response.status_code == 200

@pytest.mark.smoke
def test_health_status_code(base_url):
    response = requests.get(f"{base_url}/health",  timeout=5)
    assert "status" in response.json(), f"Нет ключа 'status'. Ключи: {list(response.json().keys())}"

@pytest.mark.smoke
def test_health_response_headers(base_url):
    response = requests.get(f"{base_url}/health",  timeout=5)
    assert "application/json" in response.headers["content-type"]

@pytest.mark.smoke
def test_health_response_time(base_url):
    response = requests.get(f"{base_url}/health", timeout=5)
    assert response.elapsed.total_seconds() < 1