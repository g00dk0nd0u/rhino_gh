# Agent-driven Rhino Sandbox Architecture

## Purpose

This repository is intended to support agent-driven Rhino tool development. Codex should be able to modify Python tool code, run safe previews, inspect logs and artifacts, and iterate without placing generated geometry into an active Rhino model automatically.

The main code should remain external to Rhino and Grasshopper UI files, version controlled, reviewable, and testable. Business logic should live in Python modules that can be edited safely and reused by future preview runners and plugin workflows.

Phase 2 separates pure twisted tower generation from Rhino adapter code. The `core/` package can be tested without Rhino, while `tools/` remains the Rhino-facing layer that converts core data into `Rhino.Geometry` objects.

Phase 3 adds a pure Python core preview report runner under `sandbox_runner/`. This runner does not display geometry visually. It executes `core/` logic, writes agent-readable JSON and log artifacts, and supports Codex PDCD feedback without Rhino.

Phase 4 adds a Rhino-side non-destructive visual preview prototype under `plugin/`. It uses a Rhino DisplayConduit or equivalent viewport drawing layer to show `twist_tower` geometry without writing preview objects to the active document. `commit_preview()` remains the explicit human-approved import step.

## Target workflow

The target workflow is:

1. Codex modifies Python tool code.
2. Codex runs the tool in a safe Rhino preview or sandbox runtime.
3. The sandbox generates logs, errors, preview reports, and validation artifacts.
4. Codex iterates based on those artifacts.
5. The change is reviewed through the normal PR and merge process.
6. A Rhino plugin presents the preview result to a human user.
7. The human user presses an Import or Commit button.
8. Only then is approved geometry added to the active Rhino document.

## Preview vs Commit

Preview is non-destructive, temporary, and isolated. Preview runs must not modify the active Rhino document. They may generate logs, manifests, validation data, report artifacts, or preview geometry files that can be inspected by Codex and the human user.

Commit is an explicit human-approved import into the active Rhino model. In the Phase 4 prototype, `commit_preview()` is the import action. In the future packaged plugin, Commit should happen only through the Rhino plugin workflow after the preview result has been reviewed and accepted.

## Why not Grasshopper

Grasshopper was useful for the early proof of concept because it provided a quick Rhino-capable runner. It is not the final UI or runtime for agent-driven PDCD iteration.

Binary UI files are not suitable as the primary place for agent-generated logic. They are harder to diff, review, test, and safely modify. Main logic should live in Python modules, with Grasshopper files kept only as thin runners or reference assets while the repository evolves toward the sandbox and plugin workflow.

## Target components

- `core/`: pure or mostly pure reusable logic that can be tested without Rhino where possible.
- `tools/`: Rhino-facing tool entry points that expose `run(inputs, logger)`.
- `sandbox_runner/`: agent-executable non-destructive report and preview runners. The current Phase 3 runner is a pure Python artifact generator for PDCD, not a visual Rhino preview.
- `plugin/`: Rhino-side preview prototype now; future final Rhino plugin UI and human-approved Import or Commit workflow.
- `preview/`: generated preview artifacts such as manifests, geometry files, and screenshots.
- `logs/`: run logs and error traces.
- `tests/`: automated tests where possible.

## Non-destructive rule

Sandbox preview code must not write to the active Rhino document. Rhino-side viewport previews must use DisplayConduit or equivalent temporary drawing rather than document object creation. Committing or importing geometry into the active Rhino model requires explicit human action through `commit_preview()` now and through the packaged plugin later.
