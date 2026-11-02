# ADD TASKS
- Plan change I requested: Create a separate endpoint for search instead of adding onto the endpoint for querying. list_tasks_by_priority_route() already lists tasks by querying them. I also asked Claude to write failing tests first before implementing to match the assignment requirements.

Failing tests output:
● Update(services/tasks.py)
Added 18 lines
        raise ValidationError("priority", "must be an integer bet
ween 1 and 5")
    return [task for task in TASKS.values() if task["priority"] =
= priority]

def search_tasks(query: str) -> list[dict]:
    """Retrieve all tasks whose title contains a search term.

    Args:
        query: The text to look for, matched case-insensitively.

    Returns:
        A list of task records whose title contains the query.
        Empty if no tasks match.

    Raises:
        ValidationError: If query is empty.
    """
    if not query or not query.strip():
        raise Val be empty")
    term = query.lower()
    return [task  term in task["titl
e"].lower()]

def create_task(title: str, user_id: int, priority: int = 3) -> d
ict:
    """Create a new task.


  Ran 1 shell command
The service tests pass, astill fail, each with a404. Now the route.

Review: Nothing corrected or rewound. Tests implemented along with function and route.

# ARCHIVE TASKS
Plan change I requested: I called Claude to create a separate endpoint for archiving tasks and making include_archived an optional parameter. I did this so that the current route for fetching tasks by priority calls the correct return code.

Failing tests output:
 Update(tests/test_tasks.py)
Added 64 lines
        update_task(1, priority)
    assert exc_info.value.status_code == 422
    assert get_task(1)["priority"] == 3

def test_archive_task_valid():
    result = archive_task(1)
    assert result["id"] == 1
    assert result["archived"] is True
    assert get_task(1)["archived"] is True

def test_archive_task_invalid():
    with as exc_info:
        archive_task(999)
    asser== 404

def test_():
    archive_task(1)
    resul
    assert result["archived"] is True

@pytest.mark.parametrize("task_id", [1, 2, 3])
def test_k_id):
    assert get_task(task_id)["archived"] is False

def test_create_task_not_archived():
    asser)["archived"
] is False

def test_get_tasks_by_priority_hides_archived():
    archi
    assert [t["id"] for t in get_tasks_by_priority
(3)] == [

def test__archived():
    archive_task(1)
    resulinclude_arch
ived=True)
    asser= [1, 2, 3]

def test_nt):
    response = client.post("/api/tasks/1/archive")
    asser
    assert response.get_json()["id"] == 1
    assered"] is True

def test_ient):
    response = client.post("/api/tasks/999/archive
")
    assert response.status_code == 404

def test_list_tasks_route_hides_archived(client):
    clien)
    response = client.get("/api/tasks?priority=3")
    asser
    assert [t["id"] for t in response.get_json()]
== [2, 3]

def test_ived_true(cl
ient):
    clien)
    response = client.get("/api/tasks?priority=3&i
nclude_ar
    assert response.status_code == 200
    asserget_json()]
== [1, 2, 3]

def test_list_tasks_route_include_archived_false(c
lient):
    client.post("/api/tasks/1/archive")
    respopriority=3&i
nclude_archived=false")
    asser
    assert [t["id"] for t in response.get_json()]
== [2, 3]

def test_ived_require
s_priority(client):
    respoinclude_arch
ived=true")
    asser

The baseline is 66e in, so I'mrunning them to confirm they fail before I write any code.

  Ran 1 shell command

The tests fail as expected: archive_task doesn't exist yet, so test_tasks.py stoper files pass. Next up are the service and route changes.

Review: Nothing corrected or rewound. Tests implemented along with function and route.