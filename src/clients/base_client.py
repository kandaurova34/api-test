import requests
import logging

logger = logging.getLogger(__name__)

class BaseClient:
    """Базовый HTTP-клиент для API-тестов."""

    def __init__(self, base_url: str, session: requests.Session | None = None, timeout: int = 5):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.timeout = timeout

    def _url(self, path: str) -> str:
        """Формирует полный URL из относительного пути."""
        return f"{self.base_url}{path}"

    def get(self, path: str, **kwargs) -> requests.Response:
        """GET-запрос с дефолтным таймаутом."""
        kwargs.setdefault("timeout", self.timeout)
        return self.session.get(self._url(path), **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        """POST-запрос с дефолтным таймаутом."""
        kwargs.setdefault("timeout", self.timeout)
        return self.session.post(self._url(path), **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        """PUT-запрос с дефолтным таймаутом."""
        kwargs.setdefault("timeout", self.timeout)
        return self.session.put(self._url(path), **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        """PATCH-запрос с дефолтным таймаутом."""
        kwargs.setdefault("timeout", self.timeout)
        return self.session.patch(self._url(path), **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """DELETE-запрос с дефолтным таймаутом."""
        kwargs.setdefault("timeout", self.timeout)
        return self.session.delete(self._url(path), **kwargs)

    def _log_response(self, response: requests.Response):
        """Логируем запрос и ответ для дебага."""
        logger.debug(
            "%s %s → %s (%0.3fs)",
            response.request.method,
            response.request.url,
            response.status_code,
            response.elapsed.total_seconds()
        )