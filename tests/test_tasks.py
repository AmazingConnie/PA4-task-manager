import pytest
from app import app
from services.tasks import process_order, get_task, get_tasks_by_user, create_task
from services.tasks import archive_task, get_tasks_by_priority, update_task
from utils.errors import NotFoundError, ValidationError


@pytest.fixture
def client():
    return app.test_client()

def test_process_order_valid():
    result = process_order(1)
    assert result["done"] is True

def test_process_order_invalid():
    with pytest.raises(Exception):
        process_order(999)

def test_get_task_valid():
    result = get_task(2)
    assert result["title"] == "Write report"

def test_get_task_invalid():
    with pytest.raises(Exception):
        get_task(999)

def test_get_tasks_by_user_valid():
    result = get_tasks_by_user(1)
    assert [t["id"] for t in result] == [1, 2]

def test_get_tasks_by_user_invalid():
    with pytest.raises(Exception):
        get_tasks_by_user(999)

def test_create_task_valid():
    result = create_task("Clean desk", 2)
    assert result["title"] == "Clean desk"
    assert result["user_id"] == 2
    assert result["done"] is False

def test_create_task_invalid():
    with pytest.raises(Exception):
        create_task("Clean desk", 999)

def test_get_tasks_by_priority_default():
    task = create_task("Default priority", 1)
    assert task["priority"] == 3
    assert task["id"] in [t["id"] for t in get_tasks_by_priority(3)]

@pytest.mark.parametrize("priority", [1, 2, 3, 4, 5])
def test_get_tasks_by_priority_valid(priority):
    task = create_task(f"Priority {priority}", 1, priority)
    result = get_tasks_by_priority(priority)
    assert task["id"] in [t["id"] for t in result]
    assert all(t["priority"] == priority for t in result)

@pytest.mark.parametrize("priority", [0, 6, -1, 100])
def test_get_tasks_by_priority_invalid(priority):
    with pytest.raises(ValidationError):
        get_tasks_by_priority(priority)

@pytest.mark.parametrize("priority", [1, 2, 3, 4, 5])
def test_update_task_valid(priority):
    result = update_task(1, priority)
    assert result["priority"] == priority
    assert get_task(1)["priority"] == priority

def test_update_task_invalid_task():
    with pytest.raises(NotFoundError) as exc_info:
        update_task(999, 1)
    assert exc_info.value.status_code == 404

@pytest.mark.parametrize("priority", [0, 6, -1, None, "2", 2.0, True])
def test_update_task_invalid_priority(priority):
    with pytest.raises(ValidationError) as exc_info:
        update_task(1, priority)
    assert exc_info.value.status_code == 422
    assert get_task(1)["priority"] == 3

def test_archive_task_valid():
    result = archive_task(1)
    assert result["id"] == 1
    assert result["archived"] is True
    assert get_task(1)["archived"] is True

def test_archive_task_invalid():
    with pytest.raises(NotFoundError) as exc_info:
        archive_task(999)
    assert exc_info.value.status_code == 404

def test_archive_task_already_archived():
    archive_task(1)
    result = archive_task(1)
    assert result["archived"] is True

@pytest.mark.parametrize("task_id", [1, 2, 3])
def test_seeded_tasks_not_archived(task_id):
    assert get_task(task_id)["archived"] is False

def test_create_task_not_archived():
    assert create_task("Clean desk", 2)["archived"] is False

def test_get_tasks_by_priority_hides_archived():
    archive_task(1)
    assert [t["id"] for t in get_tasks_by_priority(3)] == [2, 3]

def test_get_tasks_by_priority_include_archived():
    archive_task(1)
    result = get_tasks_by_priority(3, include_archived=True)
    assert [t["id"] for t in result] == [1, 2, 3]

def test_archive_task_route_valid(client):
    response = client.post("/api/tasks/1/archive")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1
    assert response.get_json()["archived"] is True

def test_archive_task_route_invalid(client):
    response = client.post("/api/tasks/999/archive")
    assert response.status_code == 404

def test_list_tasks_route_hides_archived(client):
    client.post("/api/tasks/1/archive")
    response = client.get("/api/tasks?priority=3")
    assert response.status_code == 200
    assert [t["id"] for t in response.get_json()] == [2, 3]

def test_list_tasks_route_include_archived_true(client):
    client.post("/api/tasks/1/archive")
    response = client.get("/api/tasks?priority=3&include_archived=true")
    assert response.status_code == 200
    assert [t["id"] for t in response.get_json()] == [1, 2, 3]

def test_list_tasks_route_include_archived_false(client):
    client.post("/api/tasks/1/archive")
    response = client.get("/api/tasks?priority=3&include_archived=false")
    assert response.status_code == 200
    assert [t["id"] for t in response.get_json()] == [2, 3]

def test_list_tasks_route_include_archived_requires_priority(client):
    response = client.get("/api/tasks?include_archived=true")
    assert response.status_code == 422
