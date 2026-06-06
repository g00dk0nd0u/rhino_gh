# Grasshopper Python Script runner

Use the Grasshopper Python Script node only as a thin runner. Keep all actual tool logic in Python modules under `tools/*.py`. Keep the runner minimal for the current single active tool workflow.

The canonical Grasshopper runner file is assumed to be saved at:

```text
grasshopper/rhino_gh_runner.gh
```

The Python Script node must use this input/output contract:

- Input `x`: command text from a Panel or other Grasshopper input.
- Input `y`: run toggle.
- Output `a`: geometry/result returned by the active tool workflow.
- Default output `out`: printed execution log.

Do not use a hard-coded local repository path. Do not require a `repo_path` Panel. Do not add input `z`, output `b`, Value Lists, dropdowns, tool discovery, or tool selection mechanisms. The script below automatically detects the repository root from the saved `.gh` file location.

## Canonical runner code

Paste this exact code into the Grasshopper Python Script node:

```python
import sys
import os
import importlib

command = str(x).strip() if x else ""
run_flag = bool(y)

gh_doc = ghenv.Component.OnPingDocument()
gh_file = gh_doc.FilePath

if not gh_file:
    a = None
    log = "Grasshopper file is not saved. Save rhino_gh_runner.gh first."

else:
    grasshopper_dir = os.path.dirname(gh_file)
    repo_path = os.path.dirname(grasshopper_dir)

    if repo_path not in sys.path:
        sys.path.insert(0, repo_path)

    if not run_flag:
        a = None
        log = "Waiting. Set run=True."

    elif not command:
        a = None
        log = "command is empty."

    else:
        import gh_loader
        importlib.reload(gh_loader)

        a, log = gh_loader.run_command(command)

print(log)
```

## Example command input

```text
test_line length=1000 count=5
```
