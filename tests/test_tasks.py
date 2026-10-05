import pytest
from services.tasks import process_order, get_task, get_tasks_by_user, create_task

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
