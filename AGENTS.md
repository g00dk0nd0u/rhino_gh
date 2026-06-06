# Agent Guidelines

This repository targets Rhino 8 / Grasshopper Python 3.9.

## Architecture

- Grasshopper files are runners only; avoid putting business logic inside `.gh` files.
- Implement tools under `tools/*.py`.
- Each tool module must expose:

```python
def run(inputs, logger):
    ...
```

- Keep tools small, focused, and easy to test.
- Prefer Rhino.Geometry and built-in Python modules.
- Do not use external pip packages unless explicitly approved.
- Avoid hard-coded user-specific paths inside tool modules.

## Runner contract

- Keep command syntax simple:

```text
tool_name key=value key=value
```

- `gh_loader.run_command(command)` must always return:

```python
result, log_text
```

- Errors must be caught and returned as full traceback logs.
- Every tool must write meaningful logs through `logger.info()` and `logger.error()`.

## Grasshopper files

- Do not edit binary Grasshopper files unless specifically requested.
- The canonical Grasshopper runner file is `grasshopper/rhino_gh_runner.gh`.
- The canonical Grasshopper Python Script code is stored in `docs/grasshopper_runner.md`.
- Keep `gh_loader.py` compatible with that script.
- Do not change the input/output contract without explicit approval.
- Do not add hard-coded local paths to the Grasshopper runner.
- The Grasshopper file should remain a thin runner only.

## Repository hygiene

- Do not commit secrets, tokens, local caches, or generated temporary files.
- Prefer small PRs with clear commit messages.
