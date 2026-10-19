## Goal
Parse $ARGUMENTS as a lowercase value named SERVICE. Compare @services/<SERVICE>.py and 
@tests/test_<SERVICE>.py. For every untested function in @services/<SERVICE>.py, update 
@tests/test_<SERVICE>.py with pytest cases related to those functions.

If the value is missing, stop and ask the user for the correct argument. Do not guess. If the name of the <SERVICE> does not exist raise a NotFoundError from @util/errors.py.

**This command should only be used for modifying test files in tests/**

Example: /fill-tests tasks -> SERVICE=tasks 
## Context
- Every file in services/ should have a corresponding test file in tests/ 
- Follow the pattern in @tests/test_users.py for creating new test cases
- Name of service should correspond to a file in services/<SERVICE>.py. 
- If the <SERVICE> does not exist, raise a NotFoundError from @utils/errors.py.
- Name of service should also have a test file in tests/test_<SERVICE>.py. 
- If the file in tests/ does not exist, raise a NotFoundError from @utils/errors.py

## Constraints 
- Do not modify any file that is not tests/test_<SERVICE>.py
- Do not add new subclasses to @utils/errors.py
- Do not add error handling to tests/test_<SERVICE>.py.
- Do not add type hints and docstrings to pytest cases in tests/test_<SERVICE>.py

## Verification
- Run pytest -q before and after updating tests/test_<SERVICE>.py. If a test fails, do not 
fix the cause without permission. Report the final pytest output when done. 