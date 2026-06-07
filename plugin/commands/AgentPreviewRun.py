"""Run the active Rhino preview command workflow."""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_repo_root_on_path():
    repo_root = Path(__file__).resolve().parents[2]
    repo_root_text = str(repo_root)
    if repo_root_text not in sys.path:
        sys.path.insert(0, repo_root_text)
    return repo_root


_ensure_repo_root_on_path()

from plugin import rhino_preview_session as preview


DEFAULT_INPUT = "width=100 height=500 levels=20 twist_degrees=180"


def main():
    import rhinoscriptsyntax as rs

    input_text = rs.GetString(
        "AgentPreviewRun input",
        DEFAULT_INPUT,
    )
    if input_text is None:
        print("AgentPreviewRun canceled.")
        return

    preview_log = preview.run_preview(input_text)
    zoom_log = preview.zoom_to_preview()

    print("AgentPreviewRun: preview log")
    print(preview_log)
    print("AgentPreviewRun: zoom log")
    print(zoom_log)


if __name__ == "__main__":
    main()
