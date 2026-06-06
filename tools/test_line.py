"""Sample Grasshopper tool that creates multiple Rhino.Geometry.Line objects."""

from __future__ import annotations

import shlex


DEFAULT_INPUTS = {"length": 1000, "count": 5}


def _coerce_value(value):
    if isinstance(value, str):
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

    return value


def _parse_key_value_text(text):
    parsed = {}
    for token in shlex.split(text):
        if "=" not in token:
            return {}
        key, value = token.split("=", 1)
        if not key:
            return {}
        parsed[key] = _coerce_value(value)
    return parsed


def _resolve_inputs(inputs):
    resolved = dict(DEFAULT_INPUTS)
    resolved.update(inputs or {})

    items = resolved.get("items")
    if isinstance(items, (list, tuple)):
        if len(items) > 0:
            resolved["length"] = items[0]
        if len(items) > 1:
            resolved["count"] = items[1]

    value = resolved.get("value")
    if isinstance(value, str):
        key_value_inputs = _parse_key_value_text(value.strip())
        if key_value_inputs:
            resolved.update(key_value_inputs)
        elif value.strip():
            resolved["length"] = _coerce_value(value.strip())
    elif value is not None:
        resolved["length"] = value

    return resolved


def run(inputs, logger):
    """Create parallel lines using Rhino.Geometry.

    Supported inputs:
        No input: use DEFAULT_INPUTS.
        value: line length, or command-like text such as "length=500 count=4".
        items: [length, count].
        length: line length in model units.
        count: number of lines to create.
    """
    import Rhino.Geometry as rg

    resolved = _resolve_inputs(inputs)
    length = float(resolved.get("length"))
    count = int(resolved.get("count"))

    if count < 0:
        logger.error("Invalid count: {}".format(count))
        raise ValueError("count must be 0 or greater")

    logger.info("Resolved length: {}".format(length))
    logger.info("Resolved count: {}".format(count))

    lines = []
    spacing = length * 0.1 if length else 100.0
    for index in range(count):
        start = rg.Point3d(0, index * spacing, 0)
        end = rg.Point3d(length, index * spacing, 0)
        lines.append(rg.Line(start, end))

    logger.info("Created {} line(s).".format(len(lines)))
    return lines
