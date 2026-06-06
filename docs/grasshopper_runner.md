# Grasshopper Python Script runner

Use the Grasshopper Python Script node only as a thin runner. Keep all actual tool logic in Python modules under `tools/*.py`. The current workflow uses one active tool configured in `gh_loader.py`, so users do not need to type the tool name in Grasshopper.

The canonical Grasshopper runner file is assumed to be saved at:

```text
grasshopper/rhino_gh_runner.gh
```

The Python Script node must use this input/output contract:

- Input `x`: optional user input from a Panel or other Grasshopper input. It may be empty.
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

user_input = x
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

    else:
        import gh_loader
        importlib.reload(gh_loader)

        a, log = gh_loader.run_active_tool(user_input)

print(log)
```

## Example optional input

Input `x` can be empty to run the active tool with its defaults. For `test_line`, these examples are also supported:

```text
length=500 count=4
```

or a numeric input such as `500` to set the line length while keeping the default count.
