# Sandbox Runner

`sandbox_runner/` will contain the future agent-executable preview runner for Rhino tools.

The runner should execute Rhino tool code without using Grasshopper. It should run in a Rhino-capable environment, such as Rhino Python, Rhino.Compute, or a local Rhino worker.

Preview execution must be non-destructive. The runner must not modify the active Rhino document during preview.

Expected outputs include:

- `logs/last_run.log`
- `preview/manifest.json`
- Optional preview geometry files
- Optional screenshots

The sandbox runner should support agent PDCD iteration by giving Codex clear logs, errors, preview artifacts, and validation data after each run.
