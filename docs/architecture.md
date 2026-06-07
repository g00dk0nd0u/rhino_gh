# Agent-driven Rhino Sandbox Architecture

## Purpose

This repository is intended to support agent-driven Rhino tool development. Codex should be able to modify Python tool code, run safe previews, inspect logs and artifacts, and iterate without placing generated geometry into an active Rhino model automatically.

The main code should remain external to Rhino and Grasshopper UI files, version controlled, reviewable, and testable. Business logic should live in Python modules that can be edited safely and reused by future preview runners and plugin workflows.

## Target workflow

The target workflow is:

1. Codex modifies Python tool code.
2. Codex runs the tool in a safe Rhino preview or sandbox runtime.
3. The sandbox generates logs, errors, preview geometry, and validation artifacts.
4. Codex iterates based on those artifacts.
5. The change is reviewed through the normal PR and merge process.
6. A Rhino plugin presents the preview result to a human user.
7. The human user presses an Import or Commit button.
8. Only then is approved geometry added to the active Rhino document.

## Preview vs Commit

Preview is non-destructive, temporary, and isolated. Preview runs must not modify the active Rhino document. They may generate logs, manifests, screenshots, validation data, or preview geometry files that can be inspected by Codex and the human user.

Commit is an explicit human-approved import into the active Rhino model. Commit should happen only through the future Rhino plugin workflow, after the preview result has been reviewed and accepted.

## Why not Grasshopper

Grasshopper was useful for the early proof of concept because it provided a quick Rhino-capable runner. It is not the final UI or runtime for agent-driven PDCD iteration.

Binary UI files are not suitable as the primary place for agent-generated logic. They are harder to diff, review, test, and safely modify. Main logic should live in Python modules, with Grasshopper files kept only as thin runners or reference assets while the repository evolves toward the sandbox and plugin workflow.

## Target components

- `core/`: pure or mostly pure reusable logic that can be tested without Rhino where possible.
- `tools/`: Rhino-facing tool entry points that expose `run(inputs, logger)`.
- `sandbox_runner/`: agent-executable preview runner for non-destructive Rhino-capable runs.
- `plugin/`: final Rhino plugin UI and human-approved Import or Commit workflow.
- `preview/`: generated preview artifacts such as manifests, geometry files, and screenshots.
- `logs/`: run logs and error traces.
- `tests/`: automated tests where possible.

## Non-destructive rule

Sandbox preview code must not write to the active Rhino document. Committing or importing geometry into the active Rhino model requires explicit human action in the plugin.
