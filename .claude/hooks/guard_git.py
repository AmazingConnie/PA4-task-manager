#!/usr/bin/env python3
"""PreToolUse hook: blocks pushes to main/master, force-pushes, and --no-verify.

Reads the tool call as JSON on stdin and inspects tool_input.command. Exits 2
with a one-line reason on stderr to block, or 0 to let the command through.

Commands are tokenized rather than regex-matched, so text that merely mentions
a flag, such as git commit -m "docs: explain --no-verify", is not blocked.
"""
import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass

PROTECTED_BRANCHES = ("main", "master")

# Words that may precede the real command, e.g. "sudo git push" or "if git push".
PREFIX_WORDS = {
    "sudo", "env", "command", "builtin", "exec", "time", "nohup", "nice",
    "timeout", "xargs", "{", "!", "if", "then", "elif", "else", "while",
    "until", "do",
}
SHELLS = {"sh", "bash", "zsh", "dash"}
ASSIGNMENT_RE = re.compile(r"[A-Za-z_]\w*=.*", re.DOTALL)
DURATION_RE = re.compile(r"[\d.]+[smhd]?")

# Git options placed before the subcommand that take a separate value.
GIT_VALUE_OPTIONS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
PUSH_VALUE_OPTIONS = {
    "-o", "--push-option", "--repo", "--receive-pack", "--exec",
}
PUSH_ALL_BRANCHES_OPTIONS = {"--all", "--branches", "--mirror"}
# Short "git commit" options that consume the rest of their cluster as a value,
# so that -mn is a message and -uno is an untracked-files mode, not -n.
COMMIT_VALUE_LETTERS = "mFcCtuS"
COMMIT_MESSAGE_OPTIONS = {"--message", "--file"}

HEREDOC_RE = re.compile(
    r"<<-?\s*(['\"]?)(\w+)\1([^\n]*)\n.*?^\s*\2[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
COMMENT_LINE_RE = re.compile(r"^\s*#.*$", re.MULTILINE)
SUBSTITUTION_RE = re.compile(r"\$\(([^()]*)\)|`([^`]*)`")


@dataclass
class ShellState:
    """What is known about the shell as a compound command progresses."""

    cwd: str
    branch: str | None = None  # Set once the command itself switches branch.


def run_git(cwd: str, *args: str) -> subprocess.CompletedProcess | None:
    """Run a read-only git query, returning None if git cannot be run."""
    try:
        return subprocess.run(
            ["git", "-C", cwd, *args],
            capture_output=True, text=True, timeout=5, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None


def current_branch(cwd: str) -> str:
    """Return the branch checked out in cwd, or "" if it cannot be determined."""
    result = run_git(cwd, "branch", "--show-current")
    return result.stdout.strip() if result and result.returncode == 0 else ""


def is_abbreviation(option: str, full_name: str, shortest: str) -> bool:
    """Git accepts unambiguous prefixes of long options, e.g. --no-verif."""
    name = option.split("=", 1)[0]
    return name.startswith(shortest) and full_name.startswith(name)


def split_segments(command: str) -> list[list[str]]:
    """Tokenize a command into simple commands, dropping redirections.

    Raises:
        ValueError: If the command has unbalanced quotes.
    """
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""

    segments: list[list[str]] = [[]]
    skip_redirect_target = False
    for token in lexer:
        if token and set(token) <= set(";&|()<>\n"):
            if "<" in token or ">" in token:
                # The "2" in "2>&1" and the target are not command arguments.
                if segments[-1] and segments[-1][-1].isdigit():
                    segments[-1].pop()
                skip_redirect_target = True
            else:
                segments.append([])
        elif skip_redirect_target:
            skip_redirect_target = False
        else:
            segments[-1].append(token)
    return [segment for segment in segments if segment]


def strip_prefix(words: list[str]) -> list[str]:
    """Remove env assignments and wrappers such as sudo from a simple command."""
    index = 0
    after_wrapper = False
    while index < len(words):
        word = words[index]
        if ASSIGNMENT_RE.fullmatch(word):
            index += 1
        elif os.path.basename(word) in PREFIX_WORDS:
            after_wrapper = True
            index += 1
        elif after_wrapper and (
            word.startswith("-") or DURATION_RE.fullmatch(word)
        ):
            index += 1
        else:
            break
    return words[index:]


def split_git_args(args: list[str]) -> tuple[str | None, str, list[str]]:
    """Split arguments after "git" into (-C directory, subcommand, the rest)."""
    directory = None
    index = 0
    while index < len(args) and args[index].startswith("-"):
        if args[index] in GIT_VALUE_OPTIONS:
            if args[index] == "-C" and index + 1 < len(args):
                directory = args[index + 1]
            index += 1
        index += 1
    if index >= len(args):
        return directory, "", []
    return directory, args[index], args[index + 1:]


def options_before_separator(args: list[str]) -> list[str]:
    """Return the arguments before a bare "--"."""
    return args[: args.index("--")] if "--" in args else args


def commit_skips_hooks(args: list[str]) -> bool:
    """Return True if "git commit" arguments include the short form -n."""
    options = options_before_separator(args)
    index = 0
    while index < len(options):
        option = options[index]
        index += 1
        if option in COMMIT_MESSAGE_OPTIONS:
            index += 1
        elif option.startswith("-") and not option.startswith("--"):
            for position, letter in enumerate(option[1:], start=1):
                if letter == "n":
                    return True
                if letter in COMMIT_VALUE_LETTERS:
                    if position == len(option) - 1 and letter in "mFcCt":
                        index += 1
                    break
    return False


def refspec_target(refspec: str, branch: str) -> str:
    """Return the branch a refspec updates on the remote."""
    source, _, destination = refspec.lstrip("+").rpartition(":")
    target = destination or source
    if target in ("HEAD", "@"):
        target = branch
    return re.sub(r"^(?:refs/)?heads/", "", target)


def check_push(args: list[str], branch: str) -> str | None:
    """Return a reason to block a "git push", or None to allow it."""
    positionals: list[str] = []
    explicit_repo = False
    pushes_all = False
    tags_only = False
    after_separator = False
    index = 0
    while index < len(args):
        arg = args[index]
        index += 1
        if after_separator or not arg.startswith("-") or arg == "-":
            positionals.append(arg)
        elif arg == "--":
            after_separator = True
        elif arg.startswith("--"):
            if is_abbreviation(arg, "--force-with-lease", "--for"):
                return "force-pushing is not allowed"
            name = arg.split("=", 1)[0]
            if name == "--repo":
                explicit_repo = True
            if name in PUSH_ALL_BRANCHES_OPTIONS:
                pushes_all = True
            if name == "--tags":
                tags_only = True
            if arg in PUSH_VALUE_OPTIONS:
                index += 1
        else:
            for position, letter in enumerate(arg[1:], start=1):
                if letter == "f":
                    return "force-pushing is not allowed"
                if letter == "o":
                    if position == len(arg) - 1:
                        index += 1
                    break

    refspecs = positionals if explicit_repo else positionals[1:]
    if any(refspec.startswith("+") for refspec in refspecs):
        return "force-pushing is not allowed (a leading + forces the refspec)"
    if pushes_all:
        return "pushing all branches includes main/master"
    if not refspecs and not tags_only and branch in PROTECTED_BRANCHES:
        return f"this would push the current branch, {branch}"
    for refspec in refspecs:
        if "$" in refspec or "`" in refspec:
            return (
                f"cannot verify the push target {refspec!r}; "
                "name the branch explicitly"
            )
        target = refspec_target(refspec, branch)
        for protected in PROTECTED_BRANCHES:
            if fnmatch.fnmatchcase(protected, target):
                return f"pushing to {protected} is not allowed"
    return None


def track_branch_switch(args: list[str], cwd: str, state: ShellState) -> None:
    """Record a "git checkout" or "git switch" so a later bare push is judged right."""
    options = options_before_separator(args)
    targets = [arg for arg in options if not arg.startswith("-")]
    if not targets:
        return
    creates_branch = any(arg in ("-b", "-B", "-c", "-C") for arg in options)
    # "git checkout app.py" restores a file, so confirm the name is a branch.
    exists = run_git(cwd, "show-ref", "--verify", "--quiet", f"refs/heads/{targets[0]}")
    if (
        creates_branch
        or targets[0] in PROTECTED_BRANCHES
        or (exists is not None and exists.returncode == 0)
    ):
        state.branch = targets[0]


def check_git(args: list[str], state: ShellState) -> str | None:
    """Return a reason to block a git invocation, or None to allow it."""
    directory, subcommand, rest = split_git_args(args)
    cwd = os.path.join(state.cwd, directory) if directory else state.cwd

    if any(
        is_abbreviation(arg, "--no-verify", "--no-v")
        for arg in options_before_separator(rest)
    ):
        return "--no-verify would skip the commit-msg hook"
    if subcommand == "commit" and commit_skips_hooks(rest):
        return "git commit -n is --no-verify and would skip the commit-msg hook"
    if subcommand in ("checkout", "switch") and not directory:
        track_branch_switch(rest, cwd, state)
    if subcommand == "push":
        branch = state.branch if state.branch and not directory else current_branch(cwd)
        return check_push(rest, branch)
    return None


def check_command(command: str, state: ShellState) -> str | None:
    """Return a reason to block a shell command, or None to allow it."""
    # Heredoc bodies are data, such as a multi-line commit message.
    command = HEREDOC_RE.sub(r"\3", command)
    command = command.replace("\\\n", "")
    command = COMMENT_LINE_RE.sub("", command)

    # Replace each $(...) and `...` with "$" so "git push origin $(x)" reads as
    # an unverifiable target, and check the substituted commands separately.
    substitutions: list[str] = []

    def collect(match: re.Match) -> str:
        substitutions.append(match.group(1) or match.group(2) or "")
        return "$"

    pending = 1
    while pending:
        command, pending = SUBSTITUTION_RE.subn(collect, command)
    for substitution in substitutions:
        reason = check_command(substitution, ShellState(state.cwd, state.branch))
        if reason:
            return reason

    try:
        segments = split_segments(command)
    except ValueError:
        # Quoting we cannot parse: fail closed only if git could be involved.
        if re.search(r"\bgit\b", command) and re.search(r"\bpush\b|--no-v", command):
            return "could not parse this git command to verify it is safe"
        return None

    for segment in segments:
        words = strip_prefix(segment)
        if not words:
            continue
        program, args = os.path.basename(words[0]), words[1:]
        reason = None
        if program == "git":
            reason = check_git(args, state)
        elif program == "cd" and args:
            state.cwd = os.path.join(state.cwd, os.path.expanduser(args[-1]))
            state.branch = None
        elif program == "eval":
            reason = check_command(" ".join(args), state)
        elif program in SHELLS:
            for index, arg in enumerate(args[:-1]):
                if re.fullmatch(r"-[a-z]*c[a-z]*", arg):
                    reason = check_command(args[index + 1], state)
                    break
        if reason:
            return reason
    return None


def main() -> int:
    """Run the hook and return its exit code."""
    try:
        payload = json.loads(sys.stdin.read())
        command = payload.get("tool_input", {}).get("command", "")
        cwd = payload.get("cwd") or os.getcwd()
    except (json.JSONDecodeError, AttributeError):
        print("BLOCKED: guard_git could not read the tool call.", file=sys.stderr)
        return 2

    reason = check_command(command, ShellState(cwd)) if command else None
    if reason:
        print(f"BLOCKED: {reason}.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
