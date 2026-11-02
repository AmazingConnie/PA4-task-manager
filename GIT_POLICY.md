# Git Policy: task-manager (Generated with Claude Code)

Claude Code hooks bind only Claude. People are bound by the `commit-msg` git hook and human review. "To add" marks a rule that `CLAUDE.md` does not contain yet.

## Branches and commits

| Rule | Mechanism |
| --- | --- |
| Name branches `feat/*`, `fix/*` or `docs/*`. Rename Claude's default `worktree-<name>` before pushing. | `CLAUDE.md`; human review |
| Write subjects as `type(scope): subject` or `type: subject`, up to 72 characters. Types: feat, fix, docs, refactor, test, chore. | Git hook: `.githooks/commit-msg` |
| Use scopes services, routes or tests, and the imperative mood. | `CLAUDE.md`; human review |
| Run `pytest -q` before every commit. Claude commits through `/ship`, which waits for approval. | `CLAUDE.md`; slash command: `/ship` |
| Never skip hooks with `--no-verify`. | Claude Code hook: `guard_git.py`; `CLAUDE.md` for people |

## Attribution

Keep the `Co-Authored-By` trailer, so reviewers can see which commits Claude made. A missing trailer does not prove that no AI was involved.

| Rule | Mechanism |
| --- | --- |
| The trailer stays on. It is configured by the `attribution` key in `.claude/settings.json`, which is unset, so the default applies. | Claude Code setting |
| Only a person changes that file, through a PR. | Claude Code hook: `guard_writes.py`; human review |
| Do not override the key in `.claude/settings.local.json`. | `CLAUDE.md` (to add) |

## Parallel or sequential

| Rule | Mechanism |
| --- | --- |
| Use parallel worktrees only when tasks have different service files. They may overlap only by adding lines to `routes/api.py` or shared test files. | Human decision at planning; `CLAUDE.md` (to add) |
| Work sequentially when tasks share a service file or records, or depend on each other. Also work sequentially on `CLAUDE.md`, `.claude/`, `.githooks/` and `requirements.txt`. | Human decision at planning; `CLAUDE.md` (to add) |
| Merge worktrees one at a time. Merge `main` into the next branch and rerun `pytest -q`. Do not rebase a pushed branch. | Human review; `guard_git.py` blocks Claude's force-pushes |

## Review and merge

Every change to `main` gets a PR and one human reviewer who did not run its Claude session. Passing tests are not enough: the merge that changed `search_tasks` passed all 99 tests.

| Change | Reviewer must | Mechanism |
| --- | --- | --- |
| Any code | Approve, run `pytest -q`, and have a person push or merge to `main`. | Human review; `guard_git.py` blocks Claude's pushes to `main` |
| Conflict resolution | Read `git show --cc <merge>`, where `++` lines are in neither parent. Check that the PR lists each conflict and its resolution. | Human review |
| Changed or removed tests | Read `git diff main...HEAD -- tests/`. Require a reason for each removed line, and the test count must not drop. | `CLAUDE.md`; human review |
| `utils/errors.py`, `migrations/`, `.env`, `.claude/settings.json` | Confirm a person made the edit, and why. | `guard_writes.py`; human review |
| `.claude/hooks/`, `.claude/commands/`, `.githooks/`, `CLAUDE.md` | Read the whole diff. | Human review |
| Force-push to `main` | Never allow it. | `guard_git.py` and `guard_writes.py` for Claude; `CLAUDE.md` for people |

## Setup

- [ ] Each teammate runs `git config core.hooksPath .githooks` after cloning.
- [ ] Add the "to add" rules and the review rules to `CLAUDE.md`.
- [ ] Check GitHub branch protection on `main`, since no hook binds a person's own push.
