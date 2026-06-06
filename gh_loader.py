"""Grasshopper runner loader for Rhino 8 Python 3.9.

Grasshopper Python Script nodes should call :func:`run_active_tool` for the
current single active tool workflow. :func:`run_command` remains available for
older runner scripts and command-panel workflows.
"""

from __future__ import annotations

import importlib
import shlex
import traceback
from typing import Any, Dict, List, Tuple


ACTIVE_TOOL = "test_line"


class Logger:
    """Small in-memory logger whose contents can be returned to Grasshopper."""

    def __init__(self) -> None:
        self._lines: List[str] = []

    def write(self, message: Any) -> None:
        self._lines.append(str(message))

    def log(self, message: Any) -> None:
        self.write(message)

    def info(self, message: Any) -> None:
        self.write(message)

    def error(self, message: Any) -> None:
        self.write(message)

    def text(self) -> str:
        return "\n".join(self._lines)


def _coerce_value(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in ("none", "null"):
        return None

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        return value


def _parse_command(command: str) -> Tuple[str, Dict[str, Any]]:
    parts = shlex.split(command or "")
    if not parts:
        raise ValueError("Command is empty. Example: test_line length=1000 count=5")

    tool_name = parts[0]
    inputs: Dict[str, Any] = {}
    for token in parts[1:]:
        if "=" not in token:
            raise ValueError("Invalid argument '{}'. Use key=value format.".format(token))
        key, value = token.split("=", 1)
        if not key:
            raise ValueError("Invalid argument '{}'. Key is empty.".format(token))
        inputs[key] = _coerce_value(value)

    return tool_name, inputs


def _normalize_user_input(user_input: Any) -> Dict[str, Any]:
    if user_input is None:
        return {}
    if isinstance(user_input, str) and not user_input.strip():
        return {}
    if isinstance(user_input, dict):
        return user_input
    if isinstance(user_input, (int, float, bool, str)):
        return {"value": user_input}
    if isinstance(user_input, (list, tuple)):
        return {"items": list(user_input)}
    return {"value": user_input}


def _load_tool(tool_name: str):
    module = importlib.import_module("tools.{}".format(tool_name))
    module = importlib.reload(module)
    run_func = getattr(module, "run", None)
    if run_func is None or not callable(run_func):
        raise AttributeError("tools.{} must define run(inputs, logger)".format(tool_name))
    return module, run_func


def _merge_default_inputs(module: Any, inputs: Dict[str, Any]) -> Dict[str, Any]:
    default_inputs = getattr(module, "DEFAULT_INPUTS", None)
    if not default_inputs:
        return dict(inputs)

    merged = dict(default_inputs)
    merged.update(inputs)
    return merged


def run_active_tool(user_input=None):
    """Run the configured active tool and return ``(result, log_text)``.

    ``user_input`` is optional Grasshopper input from ``x``. Empty input runs
    the active tool with its ``DEFAULT_INPUTS`` when provided by the tool.
    """
    logger = Logger()
    result = None

    try:
        logger.info("Active tool: {}".format(ACTIVE_TOOL))
        module, run_func = _load_tool(ACTIVE_TOOL)
        inputs = _normalize_user_input(user_input)
        inputs = _merge_default_inputs(module, inputs)
        logger.info("Inputs: {}".format(inputs))

        result = run_func(inputs, logger)
        logger.info("Status: success")
    except Exception:
        logger.error("Status: error")
        logger.error(traceback.format_exc())

    log_text = logger.text()
    return result, log_text


def run_command(command: str):
    """Run a tool command and return ``(result, log_text)``.

    The command format is ``tool_name key=value key=value``. The first token is
    imported as ``tools.{tool_name}``, and the module must expose
    ``run(inputs, logger)``.
    """
    logger = Logger()
    result = None

    try:
        logger.info("Command: {}".format(command))
        tool_name, inputs = _parse_command(command)
        logger.info("Tool: {}".format(tool_name))

        module, run_func = _load_tool(tool_name)
        inputs = _merge_default_inputs(module, inputs)
        logger.info("Inputs: {}".format(inputs))

        result = run_func(inputs, logger)
        logger.info("Status: success")
    except Exception:
        logger.error("Status: error")
        logger.error(traceback.format_exc())

    log_text = logger.text()
    return result, log_text
