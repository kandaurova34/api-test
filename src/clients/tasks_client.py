from src.clients.base_client import BaseClient

class TasksClient(BaseClient):
    """Клиент для работы с задачами."""

    PREFIX = "/api/v1/tasks"

    def create(self, title: str, token: str, **kwargs):
        """Создать задачу."""
        payload = {"title": title}
        payload.update(kwargs)  # description, status, priority, due_date...
        return self.post(
            self.PREFIX + "/",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )

    def get_list(self, token: str, **params):
        """Получить список задач с фильтрацией."""
        return self.get(
            self.PREFIX + "/",
            params=params,
            headers={"Authorization": f"Bearer {token}"}
        )

    def get_by_id(self, task_id: str, token: str):
        """Получить задачу по ID."""
        return self.get(
            f"{self.PREFIX}/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

    def update(self, task_id: str, token: str, **fields):
        """Обновить задачу."""
        return self.put(
            f"{self.PREFIX}/{task_id}",
            json=fields,
            headers={"Authorization": f"Bearer {token}"}
        )

    def delete(self, task_id: str, token: str):
        """Удалить задачу."""
        return super().delete(
            f"{self.PREFIX}/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )