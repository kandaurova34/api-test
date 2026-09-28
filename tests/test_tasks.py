import pytest

@pytest.mark.tasks
def test_create_task(tasks_client, auth_token):
    resp = tasks_client.create("Test task", auth_token, status="TODO", priority="HIGH")
    assert resp.status_code == 201

@pytest.mark.tasks
def test_get_task_by_id(tasks_client, auth_token):
    created = tasks_client.create("Test task", auth_token, status="TODO", priority="HIGH")
    assert created.status_code == 201, created.text
    task_id = created.json()["id"]

    resp = tasks_client.get_by_id(task_id, auth_token)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Test task"

@pytest.mark.tasks
def test_get_tasks_list(tasks_client, auth_token):
    tasks_client.create("List task A", auth_token, status="TODO", priority="HIGH")
    tasks_client.create("List task B", auth_token, status="TODO", priority="LOW")

    resp = tasks_client.get_list(auth_token)
    body = resp.json()
    items = body["items"] if isinstance(body, dict) else body

    assert len(items) >= 2, f"Ожидали минимум 2 задачи, получили {len(items)}"

@pytest.mark.tasks
def test_delete_task(tasks_client, auth_token):
    created = tasks_client.create(
        "To delete", auth_token, status="TODO", priority="HIGH"
    )
    task_id = created.json()["id"]
    deleted = tasks_client.delete(task_id, auth_token)
    assert deleted.status_code in (200, 204)

    resp = tasks_client.get_by_id(task_id, auth_token)
    assert resp.status_code == 404, (
        f"Ожидали 404 после удаления, получили {resp.status_code} — {resp.text}"
    )