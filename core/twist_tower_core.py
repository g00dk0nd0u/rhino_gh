"""Pure Python twisted tower geometry data generation."""

from __future__ import annotations

import math
import shlex


DEFAULT_INPUTS = {
    "width": 1000,
    "height": 5000,
    "levels": 20,
    "twist_degrees": 90,
    "center_x": 0,
    "center_y": 0,
    "base_z": 0,
    "make_faces": True,
    "make_section_curves": True,
}


_LIST_INPUT_KEYS = ("width", "height", "levels", "twist_degrees")


def _coerce_value(value):
    if isinstance(value, str):
        lowered = value.strip().lower()
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


def _apply_list_inputs(resolved, items):
    if isinstance(items, (list, tuple)):
        for index, key in enumerate(_LIST_INPUT_KEYS):
            if len(items) > index:
                resolved[key] = items[index]


def _apply_value_input(resolved, value):
    if isinstance(value, str):
        stripped = value.strip()
        if stripped:
            key_value_inputs = _parse_key_value_text(stripped)
            if key_value_inputs:
                resolved.update(key_value_inputs)
            else:
                resolved["twist_degrees"] = _coerce_value(stripped)
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        resolved["twist_degrees"] = value


def resolve_inputs(inputs):
    """Resolve user input into a complete twisted tower input dictionary."""
    resolved = dict(DEFAULT_INPUTS)

    if inputs is None:
        return resolved
    if isinstance(inputs, str) and not inputs.strip():
        return resolved
    if isinstance(inputs, dict):
        resolved.update(inputs)
        _apply_list_inputs(resolved, resolved.get("items"))
        _apply_value_input(resolved, resolved.get("value"))
        return resolved
    if isinstance(inputs, (list, tuple)):
        _apply_list_inputs(resolved, inputs)
        return resolved

    _apply_value_input(resolved, inputs)
    return resolved


def _as_bool(value):
    value = _coerce_value(value)
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return bool(value.strip())
    return bool(value)


def _validate_and_cast_inputs(resolved):
    width = float(resolved.get("width"))
    height = float(resolved.get("height"))
    levels = int(resolved.get("levels"))
    twist_degrees = float(resolved.get("twist_degrees"))
    center_x = float(resolved.get("center_x"))
    center_y = float(resolved.get("center_y"))
    base_z = float(resolved.get("base_z"))
    make_faces = _as_bool(resolved.get("make_faces"))
    make_section_curves = _as_bool(resolved.get("make_section_curves"))

    if width <= 0:
        raise ValueError("width must be greater than 0")
    if height <= 0:
        raise ValueError("height must be greater than 0")
    if levels < 2:
        raise ValueError("levels must be 2 or greater")

    casted = dict(resolved)
    casted.update(
        {
            "width": width,
            "height": height,
            "levels": levels,
            "twist_degrees": twist_degrees,
            "center_x": center_x,
            "center_y": center_y,
            "base_z": base_z,
            "make_faces": make_faces,
            "make_section_curves": make_section_curves,
        }
    )
    return casted


def _section_points(width, center_x, center_y, z, angle_radians):
    half_width = width * 0.5
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    local_corners = (
        (-half_width, -half_width),
        (half_width, -half_width),
        (half_width, half_width),
        (-half_width, half_width),
    )

    points = []
    for x, y in local_corners:
        rotated_x = x * cos_angle - y * sin_angle
        rotated_y = x * sin_angle + y * cos_angle
        points.append((center_x + rotated_x, center_y + rotated_y, z))
    return points


def _build_sections(resolved):
    sections = []
    for level_index in range(resolved["levels"]):
        parameter = float(level_index) / float(resolved["levels"] - 1)
        z = resolved["base_z"] + resolved["height"] * parameter
        angle_radians = math.radians(resolved["twist_degrees"] * parameter)
        sections.append(
            _section_points(
                resolved["width"],
                resolved["center_x"],
                resolved["center_y"],
                z,
                angle_radians,
            )
        )
    return sections


def _build_faces(level_count, corner_count):
    faces = []
    for level_index in range(level_count - 1):
        lower_start = level_index * corner_count
        upper_start = (level_index + 1) * corner_count
        for corner_index in range(corner_count):
            next_corner_index = (corner_index + 1) % corner_count
            faces.append(
                (
                    lower_start + corner_index,
                    lower_start + next_corner_index,
                    upper_start + next_corner_index,
                    upper_start + corner_index,
                )
            )

    faces.append((3, 2, 1, 0))
    top_start = (level_count - 1) * corner_count
    faces.append((top_start, top_start + 1, top_start + 2, top_start + 3))
    return faces


def generate_twist_tower_data(inputs):
    """Generate pure twisted tower geometry data from user inputs."""
    resolved = _validate_and_cast_inputs(resolve_inputs(inputs))
    sections = _build_sections(resolved)
    vertices = [point for section in sections for point in section]
    faces = _build_faces(len(sections), len(sections[0]))
    section_polylines = [list(section) + [section[0]] for section in sections]

    return {
        "resolved_inputs": resolved,
        "sections": sections,
        "vertices": vertices,
        "faces": faces,
        "section_polylines": section_polylines,
        "stats": {
            "level_count": len(sections),
            "vertex_count": len(vertices),
            "face_count": len(faces),
            "section_curve_count": len(section_polylines),
        },
    }
