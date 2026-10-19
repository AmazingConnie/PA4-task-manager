## Goal
Audit $ARGUMENTS for missing AppError handling. For every
function that raises a raw exception (ValueError, TypeError,
SQLAlchemyError, etc.), replace it with the appropriate 
AppError subclass from utils/errors.py.

## Context
- All services should match the canonical error-handling pattern in @services/users.py
- AppError hierarchy: utils/errors.py (AppError, NotFoundError, ValidationError)
- This file follows the repository pattern: no HTTP logic, no direct DB calls 
outside the repository layer.

## Constraints
- Do not modify @utils/errors.py or any file outside $ARGUMENTS.
- Do not add new AppError subclasses — use only existing ones.
- Preserve all existing function signatures.
- If a function already uses AppError correctly, do not rewrite it.
- Do not touch @routes/api.py 
- Do not touch any file in tests/

## Verification
Run pytest -q after every function you update. All existing tests 
must still pass before you move to the next function. Report the
final pytest output when done.
