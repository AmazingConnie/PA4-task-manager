# Flask API

An API made with Flask(Python) to manage tasks and users.

## Commands
- Install: pip install -r requirements.txt
- Test: pytest -v
- Lint: ruff check .
- Test quickly: pytest -q

## Architecture
- Routes call services; services call repositories; never skip layers
- Use AppError subclasses from @utils/errors.py
- Follow the service pattern in @services/users.py for all new services

## Conventions
- Ensure that all functions in services/ use type hints and Google-style docstrings
- Follow the pattern in @services/users.py as an example for error handling
- Ensure that all functions in services/ use error handling from @util/errors.py
- Every endpoint should have a corresponding test in tests/

## Do Not Touch
- Do not add new packages without updating requirements.txt
- Do not modify existing test cases for each test file in tests/

## Hooks
The purpose of guard_writes.py is to ensure that a user does not execute a dangerous command that can compromise the entire repository. The file also protects sensitive files such as @utils/errors.py and .env (secrets) from being modified. Bash commands such as dropping the database table, git push --force, and rm -rf are blocked from being executed through regex patterns that scan command input. 

A new team member would add a rule to it by adding a new sensitive file path in BLOCKED_PATHS and new sensitive regex pattern in BASH_BLOCKED_PATHS.

## Commands
- /audit-errors: This command helps you look for any raw errors in a service file and replaces them with errors from the AppError subclass. Only use for files in services/
- /scaffold-endpoints: This command helps you create a new endpoint by passing in the name of the new service and the HTTP method you want for that service's endpoint.
- /fill-tests: This command helps you add pytest cases for untested functions in a services/ file.