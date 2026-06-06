# rhino_gh

Python tools for Rhino 8 / Grasshopper Python 3.9.

## Purpose

Grasshopper Python Script nodes should contain only thin runner code. All substantial processing should live in Python modules in this repository so the logic can be edited, reviewed, tested, and versioned outside binary Grasshopper files.

## Usage

Use the Grasshopper file at `grasshopper/rhino_gh_runner.gh` as the runner, or paste the minimal runner snippet from [`docs/grasshopper_runner.md`](docs/grasshopper_runner.md) into a Python Script node.

The runner calls the single active tool configured by `gh_loader.ACTIVE_TOOL`:

```python
result, log = gh_loader.run_active_tool(user_input)
```

`gh_loader.run_active_tool(user_input)` always returns `result, log_text`. Input `x` is optional user input for the active tool. Leave `x` empty to run the active tool with its defaults.

## Active tool: twisted tower

The current active tool is `twist_tower`. It creates a closed mesh tower from square horizontal floor sections that rotate gradually as they rise. By default, it also returns the section curves.

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
