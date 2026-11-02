import pytest
from services.tasks import process_order, get_task, get_tasks_by_user, create_task
from services.tasks import get_tasks_by_priority, update_task
from services.tasks import search_tasks
from app import app
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

def test_search_tasks_case_insensitive():
    result = search_tasks("GROCERIES")
    assert [t["id"] for t in result] == [1]

def test_search_tasks_partial_match():
    result = search_tasks("report")
    assert [t["id"] for t in result] == [2]

def test_search_tasks_no_match():
    assert search_tasks("zzz") == []

@pytest.mark.parametrize("query", ["", "   ", None])
def test_search_tasks_invalid(query):
    with pytest.raises(ValidationError) as exc_info:
        search_tasks(query)
    assert exc_info.value.status_code == 422

def test_search_tasks_route_valid(client):
    response = client.get("/api/tasks/search?q=groceries")
    assert response.status_code == 200
    assert [t["id"] for t in response.get_json()] == [1]

def test_search_tasks_route_no_match(client):
    response = client.get("/api/tasks/search?q=zzz")
    assert response.status_code == 200
    assert response.get_json() == []

def test_search_tasks_route_empty_query(client):
    response = client.get("/api/tasks/search?q=")
    assert response.status_code == 422
    assert "error" in response.get_json()

def test_search_tasks_route_missing_query(client):
    response = client.get("/api/tasks/search")
    assert response.status_code == 422
    assert "error" in response.get_json()

def test_list_tasks_by_priority_route_unaffected(client):
    response = client.get("/api/tasks?priority=3")
    assert response.status_code == 200
    assert all(t["priority"] == 3 for t in response.get_json())

def test_get_task_route_unaffected(client):
    response = client.get("/api/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1
