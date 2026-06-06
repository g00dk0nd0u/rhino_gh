"""Sample Grasshopper tool that creates multiple Rhino.Geometry.Line objects."""

from __future__ import annotations


def run(inputs, logger):
    """Create parallel lines using Rhino.Geometry.

    Expected inputs:
        length: line length in model units (default: 1000)
        count: number of lines to create (default: 5)
    """
    import Rhino.Geometry as rg

    length = float(inputs.get("length", 1000))
    count = int(inputs.get("count", 5))

    if count < 0:
        raise ValueError("count must be 0 or greater")

    lines = []
    spacing = length * 0.1 if length else 100.0
    for index in range(count):
        start = rg.Point3d(0, index * spacing, 0)
        end = rg.Point3d(length, index * spacing, 0)
        lines.append(rg.Line(start, end))

    logger.info("Created {} line(s).".format(len(lines)))
    return lines
