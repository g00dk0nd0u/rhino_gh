# Rhino Plugin

`plugin/` contains the current Rhino-side preview prototype and will later
contain the final user-facing Rhino plugin UI.

Phase 4 adds `rhino_preview_session.py`, a Rhino Python module/command
prototype. It displays `twist_tower` geometry in Rhino viewports through a
DisplayConduit without adding preview geometry to the active Rhino document.

Phase 5 adds command-style Rhino Python scripts under `plugin/commands/`.
These scripts are a bridge between ScriptEditor testing and future plugin or
UI packaging. They are still not a packaged `.rhp` plugin.

This is not a packaged `.rhp` plugin yet. There is no Eto UI, no buttons, and
no plugin installer in this phase.

## Rhino preview usage

### Option A: Run command scripts directly

Run each script from Rhino ScriptEditor or `RunPythonScript`:

- `plugin/commands/AgentPreviewRun.py`
- `plugin/commands/AgentPreviewClear.py`
- `plugin/commands/AgentPreviewZoom.py`
- `plugin/commands/AgentPreviewCommit.py`

Each command script must end with:

```python
if __name__ == "__main__":
    main()
```

This footer is required so `RunPythonScript` executes the command body instead
of only loading the function definitions.

- `AgentPreviewRun` prompts for input, shows a temporary non-selectable
  preview, and zooms to it.
- `AgentPreviewClear` removes the temporary preview.
- `AgentPreviewZoom` zooms to the current preview.
- `AgentPreviewCommit` adds the current preview geometry to the Rhino
  document.

### Option B: Create Rhino aliases manually

Create aliases named:

- `AgentPreviewRun`
- `AgentPreviewClear`
- `AgentPreviewZoom`
- `AgentPreviewCommit`

Each alias should call the corresponding script through `RunPythonScript`
using your local repo path to the matching file under `plugin/commands/`.

### Direct module usage

1. Pull the latest repo.
2. Open Rhino.
3. Open the Rhino Python editor or script runner.
4. Add the repo root to `sys.path` if needed.
5. Run:

```python
from plugin import rhino_preview_session as preview
preview.run_preview("width=1500 height=8000 levels=30 twist_degrees=180")
```

To zoom the active Rhino view to the temporary preview:

```python
preview.zoom_to_preview()
```

To clear the temporary viewport preview:

```python
preview.clear_preview()
```

To commit the current preview into the actual Rhino model:

```python
preview.commit_preview()
```

`run_preview()` is non-destructive. It draws temporary viewport geometry
through the conduit and does not call `sc.doc.Objects.Add...`. The preview is
not part of the Rhino document until it is committed.

`commit_preview()` is the explicit destructive/import action. It is the only
function in this prototype that adds approved preview geometry to the active
Rhino document.
