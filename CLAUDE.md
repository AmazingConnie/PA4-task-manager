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
- Do not modify existing tests/ files without asking for permission first 
- Do not add new packages without updating requirements.txt
- Do not add error handling inside routes in @routes/api.py
- Do not modify existing test cases for each test file in tests/
- Do not touch utils/
- Do not add type hints or docstrings to routes in @routes/api.py

