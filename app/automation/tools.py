import json

from app.automation.basic import run_command

Tools = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a command in the terminal and return the output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to run.",
                    }
                },
                "required": ["command"],
            },
        },
    }
]

_TOOL_FUNCTIONS = {
    "run_command": run_command,
}


def _normalize_tool_name(name: str | None) -> str:
    if not name:
        return ""

    normalized = name.strip().lower().replace(" ", "_")
    aliases = {
        "run_a_command": "run_command",
        "run-command": "run_command",
    }
    return aliases.get(normalized, normalized)


def execute_tool(name: str, arguments: dict | None = None) -> str:
    name = _normalize_tool_name(name)

    if name not in _TOOL_FUNCTIONS:
        return f"Error: Unknown tool '{name}'."

    arguments = arguments or {}
    if "parameters" in arguments and isinstance(arguments["parameters"], dict):
        arguments = arguments["parameters"]

    try:
        result = _TOOL_FUNCTIONS[name](**arguments)
    except TypeError as exc:
        return f"Error: Invalid arguments for '{name}': {exc}"
    except Exception as exc:
        return f"Error running '{name}': {exc}"

    return str(result)


def execute_tool_call(tool_call: dict) -> str:
    function_payload = tool_call.get("function", {})
    name = function_payload.get("name") or tool_call.get("name")
    arguments = function_payload.get("arguments")
    if arguments is None:
        arguments = tool_call.get("arguments")
    if arguments is None:
        arguments = function_payload.get("parameters")
    if arguments is None:
        arguments = tool_call.get("parameters", {})

    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except json.JSONDecodeError:
            return "Error: Tool arguments must be valid JSON."

    if not isinstance(arguments, dict):
        return "Error: Tool arguments must be a JSON object."

    if not name:
        return "Error: Missing tool name."

    return execute_tool(name, arguments)