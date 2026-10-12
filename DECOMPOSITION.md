# DECOMPOSITION — Notification Preferences

## Feature spec
- A user can set a notification preference: email, sms, or none (default: none) 

- Preference is stored on the User model (new nullable column: notification_pref) 

- PATCH /users/{id}/notifications — update preference; reject invalid values with ValidationError 

- GET /users/{id}/notifications — return current preference 

- The existing user list and user detail endpoints must include notification_pref in their response 

### SA-1: Data layer

| Field | Value |
|---|---|
| Input | `services/users.py`, `CLAUDE.md` |
| Task | Add nullable `notification_pref` column (email / sms / none, default none) and validation to the User model |
| Output | `services/users.py` with new `notification_pref` parameter in the Users model |
| Constraint | Do not touch any other files in `services/` , `routes/`, or `tests`|
| Hand-off | `notification_pref` field and modified User model in `services/users.py` for SA-2 |

### SA-2: Service layer

| Field | Value |
|---|---|
| Input | `services/users.py`, `CLAUDE.md` |
| Task | Add functions `update_pref(user_id, notification_pref)` and `return_pref(user_id)`.  |
| Output | Revised `services/users.py` with type hints and docstrings for both functions |
| Constraint | Use AppError subclasses when implementing `update_pref` for invalid `notification_pref`. Do not touch tests/, routes/, or utils/.|
| Hand-off | Two new functions in `services/users.py` for SA-3 |

### SA-3: API layer

| Field | Value |
|---|---|
| Input | `services/users.py`, `routes/api.py`, `CLAUDE.md` |
| Task | Add `PATCH /users/{id}/notifications` and `GET /users/{id}/notifications`that call only the two functions created in SA-2.  |
| Output | `routes/users.py` with new routes for `PATCH` and `GET /users{id}/notifications` |
| Constraint | Do not touch services/, tests/, or errors/. No typechecking or docstrings in `routes/users.py` |
| Hand-off | Working endpoints with their URLs, request body shape, and error status codes for invalid values for SA-4.  |

### SA-4: Tests

| Field | Value |
|---|---|
| Input | `services/users.py`, `tests/test_users.py`, `conftest.py`, and `CLAUDE.md` |
| Task | Add tests for the default value 'none', a valid update, invalid value rejection, creating users with non-default notification_pref, and getting users with a notification_pref.|
| Output | `tests/test_users.py` |
| Constraint | Do not touch anything outside of tests/. If there is a bug, ask for permission before fixing it. |
| Hand-off | `pytest -q` runs successfully.|


## Prompts

### SA-1
SA-1: Data layer

Input: Current Users model in @services/users.py.

Task: Add a notification_pref field to the User model in @services/users.py. notification_pref is a string that is either 'email', 'sms', or 'none'. notification_pref is optional on creation where it defaults to 'none'. Raise a ValidationError if user inputs a string that does not match any of the three preferences. 

Constraints:
- Do not touch any other file in services/, routes/, or utils/.
- Do not write any API endpoints.
- Do not write tests yet.

Output: Updated Users model with notification_pref field in @services/users.py.

Follow all conventions in CLAUDE.md.

### SA-2
SA-2: Service layer

Input: Functions in @services/users.py.

Task: Add functions update_pref(user_id: int, notification_pref: str) and get_pref(user_id: int). update_pref returns user record from the Users model with the new notification pref. get_pref returns the user's current notification_pref based on their id. Raise errors for update_pref if user_id or notification_pref is invalid. Raise errors for get_pref if user_id is invalid. Add notification_pref as an optional parameter that defaults to 'none' in create_user(name: str, email: str).

Constraints:
- Use AppError subclasses when implementing update_pref and get_pref for invalid inputs
- Do not touch any other file in services/.
- Do not touch utils/.
- Do not write any API endpoints.
- Do not write tests yet.

Output: Updated functions with type hints and Google-style docstrings in @services/users.py.

Follow all conventions in CLAUDE.md.

### SA-3
SA-3: API layer

Inputs: Functions in @services/users.py and Routes in @routes/api.py
Task:  In @routes/api.py, add routes for PATCH /users/{id}/notifications and GET /users/{id}/notifications, which calls functions update_pref(user_id: int, notification_pref: str) and get_pref(user_id: int) respectively. Update get_user_route() to return a notification_pref in its response.

Constraints:
 - Do not touch any other files in services/ or errors/. 
 - No typechecking or docstrings in @routes/users.py.
 - Do not write tests yet.
 
Output: Updated @routes/api.py, with working endpoints and their URLs, request body shape, and error status codes for invalid values.

Follow all conventions in CLAUDE.md.

### SA-4
SA-4: Tests

Inputs: Functions in @services/users.py, Test cases in @tests/test_users.py, and @conftest.py

Task: In @tests/test_users.py, add at least four tests for update_pref() and get_pref(), including tests for valid and invalid inputs. Also add tests for create_user() and get_user() when notification_pref is 'email' or 'sms'.

Constraints:
 - Do not modify existing test cases in @tests/test_users.py
 - Do not modify any other files in tests/, routes/, services/, or utils/
 - Run 'pytest -q' before and after adding the test cases.
 - If there is a bug in a test case or a test case fails, ask for permission before fixing it.
 
Output: All tests in @tests/test_users.py pass successfully with 'pytest -q'.

Follow all conventions in CLAUDE.md.

## Divergence

**Did Claude follow the constraint field for every subagent?**
Claude followed the constraint field for every subagent, though many of the constraints listed
were already present in CLAUDE.md.

**Did any subagent's output break the next subagent's assumption? How did you recover?**
SA-1's output partially broke SA-2's assumption as it had modified create_user to include notification_pref, which defaults to 'none'. I did not have to recover for this as SA-2 was still able to implement the other two functions needed for updating and retrieving notification preferences.

**Would you write the decomposition differently a second time? What would you change?**
If I wrote the decomposition differently a second time, I would have cut down on the amount of constraints listed
for each subagent. For example, I repeatedly added 'Do not modify any other files in tests/, routes/, services/, or utils/', a line that could be added to CLAUDE.md instead.