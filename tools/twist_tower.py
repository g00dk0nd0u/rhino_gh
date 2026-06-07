"""Rhino adapter for the twisted tower tool."""

from __future__ import annotations

from core import twist_tower_core


DEFAULT_INPUTS = twist_tower_core.DEFAULT_INPUTS


def _to_point3d(rg, point):
    return rg.Point3d(point[0], point[1], point[2])


def _build_mesh(rg, data):
    mesh = rg.Mesh()

    for point in data["vertices"]:
        mesh.Vertices.Add(_to_point3d(rg, point))

    for face in data["faces"]:
        mesh.Faces.AddFace(face[0], face[1], face[2], face[3])

    mesh.Normals.ComputeNormals()
    mesh.Compact()
    return mesh


def _build_section_curves(rg, data):
    curves = []
    for section in data["section_polylines"]:
        polyline = rg.Polyline([_to_point3d(rg, point) for point in section])
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

    data = twist_tower_core.generate_twist_tower_data(inputs)
    resolved = data["resolved_inputs"]
    make_faces = resolved["make_faces"]
    make_section_curves = resolved["make_section_curves"]

    logger.info("Resolved width: {}".format(resolved["width"]))
    logger.info("Resolved height: {}".format(resolved["height"]))
    logger.info("Resolved levels: {}".format(resolved["levels"]))
    logger.info("Resolved twist_degrees: {}".format(resolved["twist_degrees"]))

    mesh = _build_mesh(rg, data) if make_faces else None
    section_curves = _build_section_curves(rg, data) if make_section_curves else []

    vertex_count = mesh.Vertices.Count if mesh else 0
    face_count = mesh.Faces.Count if mesh else 0
    logger.info("Mesh vertices: {}".format(vertex_count))
    logger.info("Mesh faces: {}".format(face_count))
    logger.info("Section curves: {}".format(len(section_curves)))
    logger.info("Twisted tower created successfully.")

    if mesh is not None:
        return [mesh] + section_curves
    return section_curves
