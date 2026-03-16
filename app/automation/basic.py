import subprocess
import sys


def _normalize_command(command: str) -> str:
    normalized = command.strip()

    if sys.platform.startswith("win"):
        lowered = normalized.lower()
        if lowered in {"ls", "ls -l", "ls -la", "ls -al", "ls -lah", "ls -lh"}:
            return "dir"

    return normalized

def run_command(command: str) -> str:
    command = _normalize_command(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr.strip()}"
    return result.stdout.strip() if result.stdout else "(no output)"