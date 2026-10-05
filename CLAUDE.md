# Flask API

An API made with Flask(Python) to manage tasks and users.

## Commands
- Install: pip install -r requirements.txt
- Test: pytest -v
- Lint: ruff check .

## Architecture
- routes/ -- contains the route handlers needed for the API to process HTTP requests and return HTTP responses
- services/ -- contains the business logic 
- tests/ -- contains tests for each service
- Use AppError subclasses from @utils/errors.py
- Follow the service pattern in @services/users.py for all services

## Conventions
- Ensure that all functions in services/ use type hints and Google-style docstrings
- Follow the pattern in @services/users.py as an example for error handling
- Ensure that all functions in services/ use error handling from @util/errors.py
- Every endpoint should have a corresponding test in tests/
- Run pytest -v after every change made during a code session

## Do Not Touch
- Do not modify existing tests/ files without asking for permission first 
- Do not add new packages without updating requirements.txt
