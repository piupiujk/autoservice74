from fastapi.testclient import TestClient
from hamcrest import assert_that, equal_to, has_entries


class TestAPI:
    def test_ping(self, http_client: TestClient) -> None:
        """Тест эндпоинта проверки работоспособности сервиса.

        Args:
            http_client: Тестовый клиент FastAPI
        """
        response = http_client.get('/ping')
        assert_that(
            actual_or_assertion=response.status_code,
            matcher=equal_to(200),
        )
        assert_that(
            actual_or_assertion=response.json(),
            matcher=has_entries({'status': 'ok'}),
        )
