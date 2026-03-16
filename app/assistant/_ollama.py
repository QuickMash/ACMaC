from pathlib import Path
import json
import re
import ollama # AI

from app.assistant import history
from app.automation import tools
from app.backend.system import os

os = os.get_os()

system = "The user is on a " + os + " system."

model_tools = tools.Tools

hist = history.History(Path("data/history.json"))
last_suggested_command: str | None = None


def _extract_tool_call_from_content(content: str) -> dict | None:
    if not content:
        return None

    raw = content.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].startswith("```"):
            raw = "\n".join(lines[1:-1]).strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None

    if not isinstance(parsed, dict):
        return None

    if "name" in parsed and "parameters" in parsed:
        return {"name": parsed.get("name"), "arguments": parsed.get("parameters")}

    if "function" in parsed or "name" in parsed:
        return parsed

    return None


def _extract_command_from_content(content: str) -> str | None:
    if not content:
        return None

    fenced_match = re.search(r"```(?:\w+)?\s*\n(.*?)```", content, re.DOTALL)
    if fenced_match:
        block = fenced_match.group(1).strip()
        if "\n" not in block and block:
            return block

    inline_match = re.search(r"`([^`\n]+)`", content)
    if inline_match:
        return inline_match.group(1).strip()

    return None


def _is_run_previous_command_prompt(prompt: str) -> bool:
    prompt_lower = prompt.strip().lower()
    triggers = {
        "run the command",
        "run command",
        "run it",
        "execute the command",
        "execute it",
    }
    return prompt_lower in triggers

def generate(prompt: str, model: str = "acmac") -> str:
    global last_suggested_command

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    try:
        response = ollama.chat(
            model=model,
            messages=messages,
            tools=model_tools,
            stream=False,
        )

        message = response.get("message", {})
        tool_calls = message.get("tool_calls") or []

        if not tool_calls:
            parsed_tool = _extract_tool_call_from_content(message.get("content", ""))
            if parsed_tool:
                tool_calls = [parsed_tool]

        if not tool_calls and _is_run_previous_command_prompt(prompt) and last_suggested_command:
            tool_calls = [{"name": "run_command", "arguments": {"command": last_suggested_command}}]

        if not tool_calls:
            inferred_command = _extract_command_from_content(message.get("content", ""))
            if inferred_command:
                last_suggested_command = inferred_command
                tool_calls = [{"name": "run_command", "arguments": {"command": inferred_command}}]

        if tool_calls:
            messages.append(message)

            for tool_call in tool_calls:
                tool_name = (
                    tool_call.get("function", {}).get("name")
                    or tool_call.get("name")
                    or "unknown_tool"
                )
                tool_output = tools.execute_tool_call(tool_call)
                messages.append(
                    {
                        "role": "tool",
                        "name": tool_name,
                        "content": tool_output,
                    }
                )

            final_response = ollama.chat(model=model, messages=messages, stream=False)
            content = final_response.get("message", {}).get("content", "")
        else:
            content = message.get("content", "")

        hist.add_entry({"prompt": prompt, "response": content})
        return content
    except Exception:
        fallback = ollama.generate(model=model, prompt=prompt, stream=False)
        content = fallback.get("response", "")
        hist.add_entry({"prompt": prompt, "response": content})
        return content

# TODO: REMOVE, only for testing to see if it works:
if __name__ == "__main__":
    print(generate("What is the best way to learn Python?"))