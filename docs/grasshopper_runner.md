# Grasshopper Python Script runner

Use the Grasshopper Python Script node only as a thin runner. Keep all actual tool logic in Python modules under `tools/*.py`.

Paste a minimal runner like this into the Grasshopper Python Script node:

```python
import sys
import importlib

repo_path = r"C:\path\to\rhino_gh"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import gh_loader
importlib.reload(gh_loader)

result, log = gh_loader.run_command(command)
```

## Node inputs and outputs

- Input `command`: command text from a Panel or other Grasshopper input.
- Output `result`: Rhino / Grasshopper data returned by the selected tool.
- Output `log`: execution log returned on both success and failure.

Example input:

```text
test_line length=1000 count=5
```
