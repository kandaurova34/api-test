from src.clients.base_client import BaseClient

class AuthClient(BaseClient):
    """Клиент для эндпоинтов авторизации."""

    PREFIX = "/api/v1/auth"

    def register(self, email: str, username: str, password: str, **kwargs):
        """Регистрация нового пользователя."""
        payload = {
            "email": email,
            "username": username,
            "password": password,
        }
        payload.update(kwargs)  # для дополнительных полей (full_name и т.д.)
        return self.post(f"{self.PREFIX}/register", json=payload)

    def register_raw(self, payload: dict):
        """Отправляет payload без обязательных полей - для тестов валидации."""
        return self.post(f"{self.PREFIX}/register", json=payload)

    def login(self, username: str, password: str):
        """Логин пользователя. Возвращает ответ с access_token."""
        return self.post(
            f"{self.PREFIX}/login",
            json={"username": username, "password": password}
        )

    def get_me(self, token: str):
        """Получить данные текущего пользователя."""
        return self.get(
            f"{self.PREFIX}/me",
            headers={"Authorization": f"Bearer {token}"}
        )

