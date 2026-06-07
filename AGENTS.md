# Agent Guidelines

This repository targets Rhino 8 / Grasshopper Python 3.9 today, and is being
reframed as an Agent-driven Rhino Sandbox Preview platform.

## Architecture

- The target workflow is an Agent-driven Rhino Sandbox Preview platform.
- Grasshopper was an early prototype runner. It is not the final workflow, UI,
  or agent PDCD runtime.
- Do not add new Grasshopper-specific dependencies unless explicitly requested.
- Grasshopper files are runners only; avoid putting business logic inside `.gh` files.
- Keep the Grasshopper runner minimal.
- The current Grasshopper workflow is a single active tool with optional user input and one run toggle.
- Do not introduce tool selection unless explicitly requested.
- Tool discovery and dropdown selection are out of scope for now.
- Main logic must live in reusable Python modules, not binary UI files.
- Implement Rhino-facing tools under `tools/*.py`.
- Each tool module must expose:

```python
def run(inputs, logger):
    ...
```

- Keep tools small, focused, and easy to test.
- Prefer Rhino.Geometry and built-in Python modules.
- Do not use external pip packages unless explicitly approved.
- Avoid hard-coded user-specific paths inside tool modules.
- Sandbox execution must be non-destructive and must not write to the active
  Rhino document during preview.
- Preview output should include logs and machine-readable artifacts where
  possible.
- Import or Commit into the active Rhino document must require explicit human
  action in the future Rhino plugin.

## Runner contract

- `gh_loader.ACTIVE_TOOL` identifies the single active Grasshopper tool.
- `gh_loader.run_active_tool(user_input=None)` is the canonical runner entry point for Grasshopper.
- Input `x` is optional user input for the active tool, not a tool name.
- If `x` is empty, the active tool should run with default values.
- Tools should provide `DEFAULT_INPUTS` where possible so empty `x` has useful behavior.
- Keep backward-compatible command syntax simple when using `run_command(command)` directly:

```text
tool_name key=value key=value
```

- `gh_loader.run_active_tool(user_input=None)` and `gh_loader.run_command(command)` must always return:

```python
result, log_text
```

- Errors must be caught and returned as full traceback logs.
- Every tool must write meaningful logs through `logger.info()` and `logger.error()`.

## Grasshopper files

- Grasshopper contract: `x` = optional user input, `y` = run toggle, `a` = result/geometry, `out` = printed log.
- Do not add input `z`, output `b`, Value Lists, dropdowns, or other tool selection mechanisms unless explicitly requested.
- Do not edit binary Grasshopper files unless specifically requested.
- Existing Grasshopper files are retained as prototype and reference assets.
- The canonical Grasshopper runner file is `grasshopper/rhino_gh_runner.gh`.
- The canonical Grasshopper Python Script code is stored in `docs/grasshopper_runner.md`.
- Keep `gh_loader.py` compatible with that script.
- Do not change the input/output contract without explicit approval.
- Do not add hard-coded local paths to the Grasshopper runner.
- The Grasshopper file should remain a thin runner only.

## Repository hygiene

- Do not commit secrets, tokens, local caches, or generated temporary files.
- Prefer small PRs with clear commit messages.
- Keep code comments, docstrings, and Markdown in English.
