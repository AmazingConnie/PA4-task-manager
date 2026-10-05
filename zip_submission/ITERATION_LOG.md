## Session 1 — 10/4/2026
### Prompt used
Add error handling to the get_task function in @services/tasks.py. Do not change the function signature. Run pytest -v when done.

### What Claude did
[describe what Claude produced — include what was correct and what was wrong]
Claude correctly added error handling to the get_task function in @services/tasks.py using the AppError subclasses in @utils/errors.py. However, Claude asked me questions on whether it should add error handling to functions process_order and create_task, which I agreed to.

### Observation
[which rule in CLAUDE.md governed this? was it followed? if not, why not?]
The 'custom errors only' rule in CLAUDE.md was responsible for this prompted change. Claude was able to follow this rule as it implemented the custom AppError classes such as ValidationError when adding error handling to get_task and other functions in tasks.py.

### CLAUDE.md update (if any)
[paste the exact line(s) you added or changed, and one sentence explaining why]
Example: 'I added X because Claude did Y in this session'
- Follow the pattern in @services/users.py as an example for error handling
    - I added 'example for error handling' to this line to show Claude how to implement error    handling the right way in Session 1
- Ensure that all functions in services/ use error handling from @util/errors.py
    - I added this line because Claude asked me to implement error handling for every function in  services/tasks.py in Session 1
- Run pytest -v after every change made during a code session
    - I added this line because Claude did not run tests after running each prompt in Session 1

## Session 2 — 10/04/2026
### Prompt used
Add a new endpoint to create a product. Do not change any existing endpoints. Run pytest -v when done.

### What Claude did
Claude correctly added a new endpoint named products.py to the list of services. However, it did not follow the common service pattern that services/user.py had until I told it to. Additionally, the products.py functions called in routes/api.py had type hints and docstrings on them, even though API calls in api.py are not supposed to have any comments. 

### Observation
[which rule in CLAUDE.md governed this? was it followed? if not, why not?]
No specific rules governed the creation of a new service and a test for that service. The only rule
governing services/ in CLAUDE.md was the type hints and docstrings rule under the conventions section, which was followed, but added comments in the wrong files.

### CLAUDE.md update (if any)
[paste the exact line(s) you added or changed, and one sentence explaining why]
- Ensure that all functions in services/ use type hints and Google-style docstrings
    - I modified this line in conventions because Claude added type hints and docstrings for products.py functions in routes/api.py in Session 2, which it was not supposed to do.
- Follow the service pattern in @services/users.py for all services
    - I added this line because the initial version of products.py only had a create function in Session 2. It did not follow the example pattern shown in services/users.py 

## Session 3 - 10/4/2026
### Prompt used
Add a new function to @services/tasks.py that returns all tasks for a given user_id. Follow the same pattern as the existing functions. Add a test for it. Run pytest -v when done.

### What Claude did
[describe what Claude produced — include what was correct and what was wrong]
Claude correctly added a function named get_tasks_by_user() in @services/tasks.py. However, it hesitated to add a test for it and run the tests. This is because one of the rules in the 'Do Not Touch' said not to modify the tests/ directory directly. 

### Observation
[which rule in CLAUDE.md governed this? was it followed? if not, why not?]
The 'service pattern' rule in the 'architecture' section was responsible for this prompted change. Claude was able to follow this rule as it implemented the custom AppError classes such as ValidationError when adding error handling to get_task and other functions in tasks.py.

### CLAUDE.md update (if any)
[paste the exact line(s) you added or changed, and one sentence explaining why]
Example: 'I added X because Claude did Y in this session'
- Do not modify tests/ files directly without asking for permission first
    - I modified this line because Claude refused to add and run new test cases in Session 3
- Every endpoint should have a corresponding test in tests/ in Session 2
    - I added this rule to the conventions section because only tasks.py had test cases in tests/ in Session 3

## Session 4 - 10/4/2026 (FINAL)
### Prompt used
For each defined service in services/, add a test file in tests/. Follow the pattern given in @tests/test_tasks.py for each test file. Run pytest -v when done.

### What Claude did
Claude produced working test files for @tests/products.py and @tests/users.py. However, it asked me for permission to add new test cases for the create task functions, which I allowed it to. It also asked me if it can add tests/conftest.py for resetting data, which I agreed to.

### Observation
[which rule in CLAUDE.md governed this? was it followed? if not, why not?]
The "every endpoint should have a corresponding test in tests/" rule governed this session. It was followed completely, but hesitated on modifying tests/test_tasks.py.

### CLAUDE.md update (if any)
[paste the exact line(s) you added or changed, and one sentence explaining why]
Example: 'I added X because Claude did Y in this session'
- Do not modify existing tests/ files without asking for permission first
    - I changed this rule because Claude was refusing to add and run tests in sessions 1, 2, and 3.

## Constant Failures:
Throughout my runs, Claude refused to add and run new test cases when I created a new service or added a new function to a service. This was because one of my original rules in the "Do Not Touch" section was "Do not modify tests/ directly", a rule I borrowed from one of the in-class drills. I did not want Claude to add too many test cases without my permission. Unfortunately, I did not completely understand this rule.

By the end of session 3, Claude generated a test case for a new case named get_tasks_by_user(). But because of the strict definition of the rule, it did not add the test case to test_tasks.py. When I asked Claude to add test cases for all services in Session 4, it did so, but it hesitated to add new test cases to test_tasks.py because of the existing rule. I did grant it permission to add the new test cases for creating tasks to test_tasks.py. I eventually changed the rule to 'Do not modify existing tests/ files without asking for permission first' in my CLAUDE.md, ending any confusion Claude had about adding new tests.