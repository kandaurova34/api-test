import pytest
import requests
import uuid
import sys
from pathlib import Path
from src.config import Config
from src.clients.auth_client import AuthClient
from src.clients.tasks_client import TasksClient

SRC_DIR = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

@pytest.fixture(scope="session")
def config():
    return Config()

@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    yield session
    session.close()

@pytest.fixture(scope="session")
def auth_client(config, api_session):
    return AuthClient(base_url=config.BASE_URL, session=api_session, timeout=config.API_TIMEOUT)

@pytest.fixture(scope="session")
def tasks_client(config, api_session):
    return TasksClient(base_url=config.BASE_URL, session=api_session, timeout=config.API_TIMEOUT)

@pytest.fixture
def unique_user_data():
    unique_id = uuid.uuid4().hex[:8]
    return {
        "email": f"test_{unique_id}@example.com",
        "username": f"user_{unique_id}",
        "password": "TestPass123!"
    }

@pytest.fixture(scope="session", autouse=True)
def check_api_available(config):
    try:
        response = requests.get(f"{config.BASE_URL}/health", timeout=10)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.exit("API недоступен. Запусти: docker-compose up -d")

@pytest.fixture(scope="session")
def registered_user(auth_client):
    """Один раз за сессию регистрирует пользователя. 1 auth-запрос."""
    uid = uuid.uuid4().hex[:8]
    data = {
        "email": f"test_{uid}@example.com",
        "username": f"user_{uid}",
        "password": "TestPass123!",
    }
    reg = auth_client.register(**data)
    assert reg.status_code in (200, 201), f"Register: {reg.status_code} — {reg.text}"
    return data


@pytest.fixture(scope="session")
def auth_token(auth_client, registered_user):
    """Один раз за сессию логинится. 1 auth-запрос."""
    login = auth_client.login(
        registered_user["username"], registered_user["password"]
    )
    assert login.status_code == 200, f"Login: {login.status_code} — {login.text}"
    return login.json()["access_token"]