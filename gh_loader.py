"""Grasshopper runner loader for Rhino 8 Python 3.9.

Grasshopper Python Script nodes should call :func:`run_command` and keep all
substantial tool logic in modules under ``tools/``.
"""

from __future__ import annotations

import importlib
import shlex
import traceback
from typing import Any, Dict, List, Tuple


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
        logger.info("Inputs: {}".format(inputs))

        module = importlib.import_module("tools.{}".format(tool_name))
        module = importlib.reload(module)
        run_func = getattr(module, "run", None)
        if run_func is None or not callable(run_func):
            raise AttributeError("tools.{} must define run(inputs, logger)".format(tool_name))

        result = run_func(inputs, logger)
        logger.info("Status: success")
    except Exception:
        logger.error("Status: error")
        logger.error(traceback.format_exc())

    log_text = logger.text()
    return result, log_text
