Parse $ARGUMENTS as two separate values for creating a new endpoint:
1. RESOURCE - the resource name, in lowercase
2. METHOD - the HTTP method (e.g. GET, POST, PUT, PATCH, DELETE), in uppercase

If either value is missing or METHOD is none of the above, stop and ask the user for the correct arguments. Do not guess.

Example: /scaffold-endpoints tags POST -> RESOURCE=tags,METHOD=POST

## Goal
Add a METHOD for the corresponding RESOURCE by creating 
services/<RESOURCE>.py and tests/test_<RESOURCE>.py. Update
routes/api.py to include the new endpoint based on the <RESOURCE>.

## Context 
- Routes call services; services call repositories; never skip layers
- Follow the service pattern established by @services/users.py for all new services
- Ensure that all functions in services/<RESOURCE>.py use type hints and Google-style docstrings
- Use AppError subclasses from @utils/errors.py when raising errors in services/<RESOURCE>.py
- Follow the pattern in @services/users.py as an example for error handling

## Constraints
- Do not write business logic to routes in @routes/api.py 
- Do not modify existing endpoints in @routes/api.py
- Do not add error handling inside routes in @routes/api.py
- Do not add type hints or docstrings to routes in @routes/api.py
- Do not add new AppError classes to @utils/errors.py
- Do not modify existing test files in tests/ except @tests/conftest.py for resetting data

## Verification
- Follow the pattern in by @tests/test_users.py when creating tests/test_<RESOURCE>.py
- Add a happy path test in tests/test_<RESOURCE>.py that calls the endpoint 
with the correct status code
    - POST -> 201
    - GET, PUT, PATCH -> 200
    - DELETE -> 204
- Run pytest -v on tests/test_<RESOURCE>.py to ensure the new endpoint's tests pass
- Run pytest -q to ensure all tests pass
- Output a short summary: what files were created or updated, the endpoints added to routes/,
the status code tested, and the pytest result.