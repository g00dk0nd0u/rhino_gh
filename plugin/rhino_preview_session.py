"""Rhino viewport preview session for the active twist_tower prototype.

This module is intentionally importable outside Rhino. Rhino-specific modules
are imported only inside functions that need the Rhino runtime.
"""

from __future__ import annotations

import traceback


_preview_geometry = []
_preview_conduit = None
_last_log = ""


class Logger:
    """Small in-memory logger compatible with Rhino tool modules."""

    def __init__(self):
        self._lines = []

    def write(self, message):
        self._lines.append(str(message))

    def log(self, message):
        self.write(message)

    def info(self, message):
        self.write(message)

    def error(self, message):
        self.write(message)

    def text(self):
        return "\n".join(self._lines)


def _normalize_input(input_text):
    if input_text is None:
        return {}
    if isinstance(input_text, str) and not input_text.strip():
        return {}
    if isinstance(input_text, str):
        return {"value": input_text}
    return {"value": input_text}


def _set_last_log(log_text):
    global _last_log
    _last_log = log_text
    return _last_log


def _redraw_views():
    import scriptcontext as sc

    if sc.doc is not None:
        sc.doc.Views.Redraw()


def _disable_preview_conduit():
    global _preview_conduit

    if _preview_conduit is not None:
        _preview_conduit.Enabled = False
        _preview_conduit = None


def _clear_preview_state(redraw):
    global _preview_geometry

    _disable_preview_conduit()
    _preview_geometry = []
    if redraw:
        _redraw_views()


def _as_geometry_list(result):
    if result is None:
        return []
    if isinstance(result, (list, tuple)):
        return list(result)
    return [result]


def _create_preview_conduit(geometry):
    import Rhino.Display as rd
    import Rhino.Geometry as rg
    from System.Drawing import Color

    class PreviewConduit(rd.DisplayConduit):
        def __init__(self, preview_geometry):
            rd.DisplayConduit.__init__(self)
            self._geometry = list(preview_geometry)
            self._mesh_color = Color.FromArgb(90, 74, 144, 226)
            self._wire_color = Color.FromArgb(220, 32, 96, 150)
            self._curve_color = Color.FromArgb(240, 230, 126, 34)
            self._material = rd.DisplayMaterial(self._mesh_color)

        def DrawForeground(self, event_args):
            display = event_args.Display
            for obj in self._geometry:
                if isinstance(obj, rg.Mesh):
                    display.DrawMeshShaded(obj, self._material)
                    display.DrawMeshWires(obj, self._wire_color)
                elif isinstance(obj, rg.Curve):
                    display.DrawCurve(obj, self._curve_color, 2)

    return PreviewConduit(geometry)


def run_preview(input_text=None):
    """Generate and display a non-destructive Rhino viewport preview."""
    global _preview_geometry, _preview_conduit

    logger = Logger()

    try:
        _clear_preview_state(redraw=True)
        logger.info("Preview start")
        inputs = _normalize_input(input_text)
        logger.info("Inputs: {}".format(inputs))

        from tools import twist_tower

        result = twist_tower.run(inputs, logger)
        _preview_geometry = _as_geometry_list(result)
        logger.info("Preview objects: {}".format(len(_preview_geometry)))

        _preview_conduit = _create_preview_conduit(_preview_geometry)
        _preview_conduit.Enabled = True
        _redraw_views()
        logger.info("Status: success")
    except Exception:
        try:
            _clear_preview_state(redraw=True)
        except Exception:
            pass
        logger.error("Status: error")
        logger.error(traceback.format_exc())

    return _set_last_log(logger.text())


def clear_preview():
    """Clear the active non-destructive preview from Rhino viewports."""
    logger = Logger()
    _clear_preview_state(redraw=True)
    logger.info("Preview cleared.")
    return _set_last_log(logger.text())


def commit_preview():
    """Commit the current preview geometry into the active Rhino document."""
    logger = Logger()

    if not _preview_geometry:
        logger.info("Committed objects: 0")
        return 0, _set_last_log(logger.text())

    try:
        import Rhino.Geometry as rg
        import scriptcontext as sc

        committed_count = 0
        for obj in list(_preview_geometry):
            if isinstance(obj, rg.Mesh):
                object_id = sc.doc.Objects.AddMesh(obj)
            elif isinstance(obj, rg.Curve):
                object_id = sc.doc.Objects.AddCurve(obj)
            else:
                object_id = sc.doc.Objects.Add(obj)

            if object_id:
                committed_count += 1

        _clear_preview_state(redraw=True)
        logger.info("Committed objects: {}".format(committed_count))
        return committed_count, _set_last_log(logger.text())
    except Exception:
        logger.error("Status: error")
        logger.error(traceback.format_exc())
        return 0, _set_last_log(logger.text())


def get_last_log():
    return _last_log
