# Sandbox Runner

`sandbox_runner/` contains agent-executable preview runners for Codex PDCD workflows.

Phase 3 adds `run_core_preview.py`, which is not a visual preview. It is a pure Python report runner that executes core geometry logic without Rhino, Grasshopper, or a plugin.

The current runner is intended for agent-readable feedback. It writes machine-readable artifacts and logs so Codex can inspect resolved inputs, stats, bounding boxes, and failures during PDCD iteration.

Current outputs include:

- `logs/last_run.log`
- `preview/manifest.json`
- `preview/twist_tower_data.json`

This runner is non-destructive and does not modify any active Rhino document. Rhino visual preview, screenshots, and plugin-based Import or Commit behavior come later.
