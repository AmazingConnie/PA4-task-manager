Rohan Mallu
COMP.5300: AI Agents With Claude Code
4 October 2026

# PA4 Reflection

## Commands
For commands I added the install, test, and lint commands to run the project. The project needed Flask and pytest to work properly since it is an API project. The lint command was added to check for code style errors. Despite adding lint to the project, very little linting was needed for this project.

## Architecture
For the architecture of this project, I listed the three main folders (routes, services, and tests) and described what each of them do. I wrote it that way so that the user could understand how the app works, what it is supposed to do, and how a user could add onto it. 

I added 'Follow the service pattern in services/users.py for all services' because Claude created a service named services/products.py but did not include a function on how to retrieve a product. The initial implementation of services/products.py led to type hints and docstrings being written with it everywhere it was called, including routes/api.py. 

I added a rule for the program to use AppError subclasses so that the program did not raise a raw exception or crash. If I had to shorten this section, I would have shortened the rule I wrote for routes/ as the description takes up two lines.

## Conventions
For conventions in this project, I wrote two rules to make sure all functions in services/ used error handling from utils/errors.py along with type hints and docstrings. This is because tasks.py lacked docstrings, type hints, and proper error handling before starting Session 1. 

I also wrote a rule asking Claude to follow the style of services/users.py when creating a new endpoint. When I asked Claude to create an endpoint for products in Session 2, it created the endpoint for me. But it did not have a function for retrieving information from a user, which is information needed by the user.

For testing, I wrote two rules; one rule requiring every endpoint to have a test in tests/ and another rule encouraging Claude to run the test command after making changes. The endpoint testing rule came about as a result of services/tasks.py being the only endpoint with a test file in tests/. This is something I observed after I concluded Session 3. The test command rule was implemented so that I did not have to write 'Run pytest -v when done.' after every prompt. If I had to shorten this section, I would have combined the two rules I wrote about error handling since the two rules are very similar.

## Do Not Touch
For constraints, I wrote rules to restrict Claude from modifying existing tests in tests/ without user permission and restricting it from installing new packages without updating requirements.txt Originally, the first rule was meant to prevent Claude from directly changing the tests/ folder to prevent unnecessary test cases. However, this original rule prevented Claude from adding tests to the tests/ folder despite generating the cases during Sessions 1-3. After session 3, I modified this rule to allow Claude to add new test files. But I restricted Claude from adding new tests to existing test files without my permission. This was to prevent Claude from completely overhauling test files in the case of refactoring a section of the code.

I wrote a rule to restrict installation of new packages without updating so that a new user cloning the repository did not have to run into problems with missing and outdated dependencies.

## Team Project Changes
The first important change I would make to CLAUDE.md in a team context would be creating and committing a standardized CLAUDE.md. A shared, standardized CLAUDE.md would allow all developers on the team to get the same behavior from Claude Code for the project. The shared CLAUDE.md would prevent a developer from getting Claude-generated code that is not consistent with the rules layed out in the shared CLAUDE.md.

The second important change I would make to CLAUDE.md in a team is to establish a shared protocol for reviewing PRs, testing requirements, and making revisions to CLAUDE.md. This type of documentation is important in a real team development environment as it allows new developers to understand the codebase efficiently and set common expectations among developers who contribute code to the project.