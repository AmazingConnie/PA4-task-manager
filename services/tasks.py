from services.users import USERS
from utils.errors import NotFoundError, ValidationError

TASKS: dict[int, dict] = {
    1: {"id": 1, "title": "Buy groceries",  "done": False, "user_id": 1},
    2: {"id": 2, "title": "Write report",   "done": False, "user_id": 1},
    3: {"id": 3, "title": "Call dentist",   "done": True,  "user_id": 2},
}

def process_order(task_id: int) -> dict:
    """Mark a task as done.

    Args:
        task_id: The unique identifier for the task.

    Returns:
        The updated task record.

    Raises:
        NotFoundError: If no task exists with the given ID.
    """
    if task_id not in TASKS:
        raise NotFoundError("Task")
    task = TASKS[task_id]
    task["done"] = True
    return task

def get_task(task_id: int) -> dict:
    """Retrieve a task by ID.

    Args:
        task_id: The unique identifier for the task.

    Returns:
        The task record as a dictionary.

    Raises:
        NotFoundError: If no task exists with the given ID.
    """
    if task_id not in TASKS:
        raise NotFoundError("Task")
    return TASKS[task_id]

def get_tasks_by_user(user_id: int) -> list[dict]:
    """Retrieve all tasks belonging to a user.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        A list of task records owned by the user. Empty if the user has no tasks.

    Raises:
        NotFoundError: If no user exists with the given ID.
    """
    if user_id not in USERS:
        raise NotFoundError("User")
    return [task for task in TASKS.values() if task["user_id"] == user_id]

def create_task(title: str, user_id: int) -> dict:
    """Create a new task.

    Args:
        title: The task's title.
        user_id: The ID of the user who owns the task.

    Returns:
        The newly created task record.

    Raises:
        ValidationError: If title is empty or user_id does not match an existing user.
    """
    if not title or not title.strip():
        raise ValidationError("title", "cannot be empty")
    if user_id not in USERS:
        raise ValidationError("user_id", "must reference an existing user")
    new_id = max(TASKS.keys()) + 1
    TASKS[new_id] = {"id": new_id, "title": title,
                     "done": False, "user_id": user_id}
    return TASKS[new_id]
