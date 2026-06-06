"""Twisted tower Grasshopper tool using Rhino.Geometry."""

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


def _resolve_inputs(inputs):
    resolved = dict(DEFAULT_INPUTS)
    resolved.update(inputs or {})

    items = resolved.get("items")
    if isinstance(items, (list, tuple)):
        for index, key in enumerate(_LIST_INPUT_KEYS):
            if len(items) > index:
                resolved[key] = items[index]

    value = resolved.get("value")
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


def _section_points(rg, width, center_x, center_y, z, angle_radians):
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
        points.append(rg.Point3d(center_x + rotated_x, center_y + rotated_y, z))
    return points


def _build_mesh(rg, sections):
    mesh = rg.Mesh()

    for section in sections:
        for point in section:
            mesh.Vertices.Add(point)

    level_count = len(sections)
    corner_count = len(sections[0])

    for level_index in range(level_count - 1):
        lower_start = level_index * corner_count
        upper_start = (level_index + 1) * corner_count
        for corner_index in range(corner_count):
            next_corner_index = (corner_index + 1) % corner_count
            mesh.Faces.AddFace(
                lower_start + corner_index,
                lower_start + next_corner_index,
                upper_start + next_corner_index,
                upper_start + corner_index,
            )

    mesh.Faces.AddFace(3, 2, 1, 0)
    top_start = (level_count - 1) * corner_count
    mesh.Faces.AddFace(top_start, top_start + 1, top_start + 2, top_start + 3)

    mesh.Normals.ComputeNormals()
    mesh.Compact()
    return mesh


def _build_section_curves(rg, sections):
    curves = []
    for section in sections:
        polyline = rg.Polyline(list(section) + [section[0]])
        curves.append(polyline.ToNurbsCurve())
    return curves


def run(inputs, logger):
    """Create a square-section twisted tower mesh and optional section curves.

    Supported inputs:
        No input: use DEFAULT_INPUTS.
        Numeric value: twist_degrees.
        Text value: key=value pairs, such as "width=1500 twist_degrees=120".
        Dict input: matching keys override DEFAULT_INPUTS.
        List input: [width, height, levels, twist_degrees].
    """
    import Rhino.Geometry as rg

    resolved = _resolve_inputs(inputs)
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
        logger.error("Invalid width: {}".format(width))
        raise ValueError("width must be greater than 0")
    if height <= 0:
        logger.error("Invalid height: {}".format(height))
        raise ValueError("height must be greater than 0")
    if levels < 2:
        logger.error("Invalid levels: {}".format(levels))
        raise ValueError("levels must be 2 or greater")

    logger.info("Resolved width: {}".format(width))
    logger.info("Resolved height: {}".format(height))
    logger.info("Resolved levels: {}".format(levels))
    logger.info("Resolved twist_degrees: {}".format(twist_degrees))

    sections = []
    for level_index in range(levels):
        parameter = float(level_index) / float(levels - 1)
        z = base_z + height * parameter
        angle_radians = math.radians(twist_degrees * parameter)
        sections.append(_section_points(rg, width, center_x, center_y, z, angle_radians))

    mesh = _build_mesh(rg, sections) if make_faces else None
    section_curves = _build_section_curves(rg, sections) if make_section_curves else []

    vertex_count = mesh.Vertices.Count if mesh is not None else 0
    face_count = mesh.Faces.Count if mesh is not None else 0
    logger.info("Mesh vertices: {}".format(vertex_count))
    logger.info("Mesh faces: {}".format(face_count))
    logger.info("Section curves: {}".format(len(section_curves)))
    logger.info("Twisted tower created successfully.")

    if mesh is not None:
        return [mesh, section_curves]
    return section_curves
