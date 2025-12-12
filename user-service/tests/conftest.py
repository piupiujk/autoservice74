import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def http_client() -> TestClient:
    """Фикстура для тестового клиента FastAPI.

    Returns:
        TestClient: Клиент для тестирования FastAPI приложений.
    """
    return TestClient(app)
