"""Commit the active Rhino preview into the document."""

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


def main():
    committed_count, log_text = preview.commit_preview()

    print("AgentPreviewCommit: this adds preview geometry to the active Rhino document.")
    print("AgentPreviewCommit: committed objects = {}".format(committed_count))
    print("AgentPreviewCommit: commit log")
    print(log_text)


if __name__ == "__main__":
    main()
