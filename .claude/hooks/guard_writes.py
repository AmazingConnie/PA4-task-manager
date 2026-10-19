#!/usr/bin/env python3
"""PreToolUse hook: blocks writes to protected files and
directories, destructive Bash commands, and hardcoded connection strings."""
import json, sys, os, re
# ── Paths this project must never let Claude write to

# Populate from your CLAUDE.md Do-not-touch section and Week 5
# DECOMPOSITION.md constraint fields.
BLOCKED_PATHS = [
 "utils/errors.py", # AppError hierarchy — never modified by agents
 "migrations/", # Migrations require human review
 ".env", # Secrets — hard block
 ".claude/settings.json", # Hook config — agents must not self-modify
]

# Token-level regexes (word boundaries), matched case-insensitively
BASH_BLOCKED_PATHS = [
 r"\b(?:DROP|TRUNCATE)\s+TABLE\b", # SQL destructive operations
 r"\brm\s+-(?:[a-z]*r[a-z]*f|[a-z]*f[a-z]*r)[a-z]*\b", # rm -rf / -fr / -Rf
 r"\bgit\s+push\b.*\s(?:--force|-f)(?=\s|$)", # Force-push rewrites shared history
]

# Shell operations that write to a file (redirects, tee, in-place edits, copies, moves)
BASH_WRITE_OPS_RE = re.compile(r">>?|\btee\b|\bsed\s+-i|\bcp\b|\bmv\b|\btruncate\b|\bdd\b|open\(.*['\"][wa]")

# File Claude may write, but whose content is inspected first
CONTENT_GUARDED_FILE = "services/tasks.py"
CONNECTION_STRING_RE = re.compile(r"postgresql://|sqlite:///")

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

def is_blocked(file_path: str) -> tuple[bool, str]:
    """Return (blocked, reason) for the given file path."""
    norm = os.path.relpath(os.path.abspath(file_path), PROJECT_DIR)
    for pattern in BLOCKED_PATHS:
        if norm == os.path.normpath(pattern):
            return True, f"Protected file: {pattern}"
        if pattern.endswith("/") and norm.startswith(os.path.normpath(pattern)):
            return True, f"Protected directory: {pattern}"
    return False, ""



def main():
    payload = json.loads(sys.stdin.read())
    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})
    # Only inspect file-write tools and Bash
    if tool not in ("Write", "Edit", "MultiEdit", "Bash"):
        sys.exit(0)
    # Bash branch: block destructive commands
    if tool == "Bash":
        command = tool_input.get("command", "")
        for pattern in BASH_BLOCKED_PATHS:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                print(f"BLOCKED: '{match.group(0)}' matches a prohibited command pattern.", file=sys.stderr)
                print("Destructive commands must be run manually after team review.", file=sys.stderr)
                sys.exit(2)
        # Block shell writes to protected paths (e.g. cat >> utils/errors.py)
        if BASH_WRITE_OPS_RE.search(command):
            for pattern in BLOCKED_PATHS:
                # Match the path as a whole token so ".env" doesn't hit "os.environ"
                if re.search(rf"(?<![\w.]){re.escape(pattern.rstrip('/'))}(?![\w.-])", command):
                    print(f"BLOCKED: Bash command writes to protected path {pattern}.", file=sys.stderr)
                    print("This file is protected by project policy.", file=sys.stderr)
                    sys.exit(2)
        sys.exit(0)
    file_path = tool_input.get("file_path") or tool_input.get("path", "")
    blocked, reason = is_blocked(file_path)
    if blocked:
        print(f"BLOCKED: {reason}. This file is protected by project policy.", file=sys.stderr)
        print(f"To modify {file_path}, update CLAUDE.md and remove the", file=sys.stderr)
        print("protection after team review.", file=sys.stderr)
        sys.exit(2)
    # Content guard: no hardcoded connection strings in the guarded file
    if os.path.relpath(os.path.abspath(file_path), PROJECT_DIR) == os.path.normpath(CONTENT_GUARDED_FILE):
        new_text = tool_input.get("content") or tool_input.get("new_string") or ""
        new_text += "".join(e.get("new_string", "") for e in tool_input.get("edits", []))
        if CONNECTION_STRING_RE.search(new_text):
            print(f"BLOCKED: hardcoded database connection string in {CONTENT_GUARDED_FILE}.", file=sys.stderr)
            print("Connection strings must come from environment variables (e.g. os.environ['DATABASE_URL']).", file=sys.stderr)
            sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
