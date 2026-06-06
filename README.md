# rhino_gh

Python tools for Rhino 8 / Grasshopper Python 3.9.

## Purpose

Grasshopper Python Script nodes should contain only thin runner code. All substantial processing should live in Python modules in this repository so the logic can be edited, reviewed, tested, and versioned outside binary Grasshopper files.

## Usage

Use the Grasshopper file at `grasshopper/rhino_gh_runner.gh` as the runner, or paste the minimal runner snippet from [`docs/grasshopper_runner.md`](docs/grasshopper_runner.md) into a Python Script node.

The runner calls:

```python
result, log = gh_loader.run_command(command)
```

`gh_loader.run_command(command)` always returns `result, log_text`.

## Adding tools

Add new tools under `tools/*.py`. Each tool module must expose:

```python
def run(inputs, logger):
    ...
```

Write meaningful log messages with `logger.info()` and `logger.error()`. The collected log text is returned to Grasshopper as the `log` output.

Avoid external pip packages unless they are explicitly approved. Prefer `Rhino.Geometry` and built-in Python modules so tools run in the standard Rhino 8 / Grasshopper Python 3.9 environment.

## Command syntax

Commands use a simple format:

```text
tool_name key=value key=value
```

Example:

```text
test_line length=1000 count=5
```

The first token, `test_line`, maps to `tools/test_line.py`. Remaining `key=value` tokens are parsed into the `inputs` dictionary passed to the tool.

## Updating code

After updating this repository with `git pull` or local edits, rerun the Grasshopper Python Script node. The runner reloads `gh_loader`, and `gh_loader` reloads the selected tool module before running it.
