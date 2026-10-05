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

## Conventions
- Ensure that all functions use type hints and Google-style docstrings
- Follow the pattern in @services/users.py as an example

## Do Not Touch
- Do not modify tests/ files directly
- Do not add new packages without updating requirements.txt