# Rhino Plugin

`plugin/` contains the current Rhino-side preview prototype and will later
contain the final user-facing Rhino plugin UI.

Phase 4 adds `rhino_preview_session.py`, a Rhino Python module/command
prototype. It displays `twist_tower` geometry in Rhino viewports through a
DisplayConduit without adding preview geometry to the active Rhino document.

This is not a packaged `.rhp` plugin yet. There is no Eto UI, no buttons, and
no plugin installer in this phase.

## Rhino preview usage

1. Pull the latest repo.
2. Open Rhino.
3. Open the Rhino Python editor or script runner.
4. Add the repo root to `sys.path` if needed.
5. Run:

```python
from plugin import rhino_preview_session as preview
preview.run_preview("width=1500 height=8000 levels=30 twist_degrees=180")
```

To clear the temporary viewport preview:

```python
preview.clear_preview()
```

To commit the current preview into the actual Rhino model:

```python
preview.commit_preview()
```

`run_preview()` is non-destructive. It draws temporary geometry through the
viewport conduit and does not call `sc.doc.Objects.Add...`.

`commit_preview()` is the explicit destructive/import action. It is the only
function in this prototype that adds approved preview geometry to the active
Rhino document.
