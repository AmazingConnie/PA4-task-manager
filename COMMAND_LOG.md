1. Command Invoked: /audit_errors;
    - $ARGUMENTS$: services/tasks.py 
    - Did Claude stay within its scope?: Yes
    - What worked: Claude scanned the file to fix any raw errors, but none were found. 
      All tests passed as well. However, Claude brought up the possibility of raw errors being raised through improper arguments such as the wrong type or argument not being iterable.
    - Lesson: /audit-errors can help you check for any raw errors present in your services without having to edit it out manually file by file.

2. /scaffold-endpoints
   - $ARGUMENTS$: tags POST
   - Did Claude stay within its scope?: Yes
   - What worked: Claude created the new endpoint for tags and added the corresponding test file.
   - What changed: tests/conftests.py contains functions to reset the data. But since Claude
     was not allowed to modify any files in tests/, it did not reset the data for tags in tests/conftests.py, but in its test file tests/test_tags.py. As a result, I added an exception for Claude to modify tests/conftests.py for data resets in /scaffold-endpoints.
   - Problem: I did not have routes/tasks.py or a schema file but I assume those are meant to be
     services/tasks.py and routes/api.py respectively.
    - Lesson: /scaffold-endpoints can help you create a new endpoint without having to create all of the functions needed for the service

3. /fill-tests 
   - $ARGUMENTS$: tasks
   - Did Claude stay within its scope?: Yes
   - What worked: Claude added pytests for the untested function update_task() in 
     services/tasks.py. Claude ran the new tests with pytest -q and they passed.
   - Lesson: /fill-tests can help you add test cases for untested functions without having to prompt Claude to do it each time.

