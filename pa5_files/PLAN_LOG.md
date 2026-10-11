# PLAN_LOG
Full feature: 
Add a priority field to the Task model. Priority is an integer 1–5 (1 = urgent, 5 = low). It is optional on creation(defaults to 3). The API must accept priority on POST /tasks and PATCH /tasks/{id}, return it in all task responses, and support GET /tasks?priority={n} for filtering.

| Session # | Prompt summary (≤15 words) | Did you amend the plan? | What you changed | Did output match amended plan? |
|---|---|---|---|---|
| 1 | Add `priority` field and validation to tasks.py. (1-5, default 3)  |Yes | Asked Claude to run `pytest -q` after making the change| Yes  |
| 2 | Accept `priority` on POST and PATCH, return it in responses| Yes |Asked Claude to not use error checking in the PATCH route. Also asked CLAUDE to run pytest -q before and after implementing the endpoints. Although Claude handled error checking for creating and updating tasks by priority in the service functions, it used the isInstance function to check for an invalid priority value instead of 'not in range(1,6)', I think it diverged this way because I did not tell it to follow the error handling form used for task_id | Partially |
| 3 |Add filtering for `GET /tasks?priority={n}`| Yes  |  Match the pattern set by get_tasks_by_id for get_tasks_by_priority.| Yes |
| 4 | Add new tests for priority fltering.  |No |  |Yes |

## Prompt 1:
Add an priority field to the Task model in @services/tasks.py. Priority is an integer from 1 to 5 (1 = urgent and 5 = low), and is optional on creation where it defaults to 3. Raise a ValidationError if user inputs a value less than 1 or greater than 5. Don't modify any other files.

## Prompt 2:
The API in @routes/api.py must accept Priority on POST/ tasks and PATCH /tasks/{id}. The API should return Priority in all task responses. Do not modify other files. Follow conventions in CLAUDE.md.

## Prompt 3:
The API in @routes/api.py must support GET /tasks?priority={n} for filtering. Add a service in @services/tasks.py to implement this endpoint. Do not modify other files. Follow conventions in CLAUDE.md. Run pytest -q before and after adding the endpoint in @routes/api.py.

## Prompt 4:
Add at least 2 new tests for priority filtering in @tests/test_tasks.py. The tests must cover the default priority of 3, other values from 1 to 5 inclusive, and out of bounds cases. Do not modify any other files. Do not modify existing test cases. Run pytest -q before and after adding the test cases.

## Prompt 4:
Add at least 2 new tests for priority filtering in @tests/test_tasks.py. The tests must cover the default priority of 3, other values from 1 to 5 inclusive, and out of bounds cases. Do not modify any other files. Do not modify existing test cases. Run pytest -q before and after adding the test cases.