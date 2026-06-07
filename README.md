# rhino_gh

Python tools for Rhino 8, moving from a Grasshopper runner prototype toward an agent-driven Rhino sandbox and future Rhino plugin workflow.

## Purpose

This repository started with a Grasshopper Python Script runner prototype. The target direction is now an Agent-driven Rhino Sandbox Preview platform: Codex modifies Python tool code, runs it in a safe preview runtime, inspects logs and artifacts, and iterates before a human approves any import into the active Rhino model.

All substantial processing should live in Python modules in this repository so the logic can be edited, reviewed, tested, and versioned outside binary UI files.

## Current status

The current active sample tool is `twist_tower`. It creates a closed mesh tower from square horizontal floor sections that rotate gradually as they rise. By default, it also returns the section curves.

The pure generation logic lives in `core/twist_tower_core.py`. The Rhino-facing adapter lives in `tools/twist_tower.py` and converts core data into `Rhino.Geometry`. Pure Python coverage for the generator lives in `tests/test_twist_tower_core.py`.

Phase 3 adds `sandbox_runner/run_core_preview.py`, a non-visual agent feedback runner that executes the pure core logic without Rhino and writes `preview/manifest.json`, `preview/twist_tower_data.json`, and `logs/last_run.log`. These runtime artifacts are generated locally and ignored by git.

Phase 4 adds `plugin/rhino_preview_session.py`, a Rhino-side visual preview prototype. It displays `twist_tower` geometry through a Rhino DisplayConduit without writing preview geometry to the active Rhino document. `commit_preview()` is the explicit human-approved import step that adds the current preview geometry to the model.

Phase 5 adds command-style Rhino Python scripts under `plugin/commands/` for `AgentPreviewRun`, `AgentPreviewClear`, `AgentPreviewZoom`, and `AgentPreviewCommit`. These wrappers make the preview workflow easier to launch from Rhino ScriptEditor or `RunPythonScript`, while still keeping the real preview logic in Python modules. This is still not a packaged `.rhp` plugin. The command scripts are a bridge between ScriptEditor testing and future plugin or UI packaging.

Grasshopper files are retained as prototype and reference assets only. They are not the final UI or agent runtime.

Future work will turn the preview prototype into a full packaged Rhino plugin UI with explicit Import or Commit controls.

## Prototype Grasshopper usage

Use the Grasshopper file at `grasshopper/rhino_gh_runner.gh` as the runner, or paste the minimal runner snippet from [`docs/grasshopper_runner.md`](docs/grasshopper_runner.md) into a Python Script node.

The runner calls the single active tool configured by `gh_loader.ACTIVE_TOOL`:

```python
result, log = gh_loader.run_active_tool(user_input)
```

`gh_loader.run_active_tool(user_input)` always returns `result, log_text`. Input `x` is optional user input for the active tool. Leave `x` empty to run the active tool with its defaults.

## Active tool: twist_tower

Example `x` values:

- Empty input

```text
twist_degrees=120
```

```text
width=1500 height=8000 levels=30 twist_degrees=180
```

A numeric `x` value also overrides `twist_degrees` directly.

## Adding tools

Add new tools under `tools/*.py`. Each tool module must expose:

```python
def run(inputs, logger):
    ...
```

Write meaningful log messages with `logger.info()` and `logger.error()`. The collected log text is returned to Grasshopper as the printed log.

Avoid external pip packages unless they are explicitly approved. Prefer `Rhino.Geometry` and built-in Python modules so tools run in the standard Rhino 8 / Grasshopper Python 3.9 environment.

## Command syntax

The active Grasshopper workflow uses `run_active_tool(user_input)`, so users do not need to type a tool name in Grasshopper. `run_command(command)` remains available for backward-compatible direct command use with this simple format:

```text
tool_name key=value key=value
```

Example:

```text
twist_tower width=1500 height=8000 levels=30 twist_degrees=180
```

The first token, `twist_tower`, maps to `tools/twist_tower.py`. Remaining `key=value` tokens are parsed into the `inputs` dictionary passed to the tool.

## Updating code

After updating this repository with `git pull` or local edits, rerun the Grasshopper Python Script node. The runner reloads `gh_loader`, and `gh_loader` reloads the selected tool module before running it.
