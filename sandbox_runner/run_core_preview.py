"""Agent-readable core preview report runner for twist_tower."""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path

TOOL_NAME = "twist_tower"
RUNNER_NAME = "core_preview"


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


REPO_ROOT = _repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from core.twist_tower_core import generate_twist_tower_data


def _ensure_output_dirs(base_dir: Path) -> tuple[Path, Path]:
    logs_dir = base_dir / "logs"
    preview_dir = base_dir / "preview"
    logs_dir.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir, preview_dir


def _compute_bounding_box(vertices):
    xs = [point[0] for point in vertices]
    ys = [point[1] for point in vertices]
    zs = [point[2] for point in vertices]
    return {
        "min": [min(xs), min(ys), min(zs)],
        "max": [max(xs), max(ys), max(zs)],
    }


def _write_json(path: Path, payload) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def run_preview(input_text=None, base_dir=None):
    """Run the pure core preview and write PDCD report artifacts."""
    root_dir = Path(base_dir) if base_dir is not None else REPO_ROOT
    logs_dir, preview_dir = _ensure_output_dirs(root_dir)
    log_path = logs_dir / "last_run.log"
    manifest_path = preview_dir / "manifest.json"
    data_path = preview_dir / "twist_tower_data.json"

    log_lines = ["Runner start"]
    if input_text is None:
        log_lines.append("Input text: <defaults>")
        core_inputs = {}
    else:
        log_lines.append("Input text: {}".format(input_text))
        core_inputs = {"value": input_text}

    try:
        data = generate_twist_tower_data(core_inputs)
        bounding_box = _compute_bounding_box(data["vertices"])
        manifest = {
            "tool": TOOL_NAME,
            "runner": RUNNER_NAME,
            "status": "success",
            "resolved_inputs": data["resolved_inputs"],
            "stats": data["stats"],
            "bounding_box": bounding_box,
            "outputs": {
                "data": "preview/twist_tower_data.json",
                "log": "logs/last_run.log",
            },
        }
        _write_json(data_path, data)
        _write_json(manifest_path, manifest)
        log_lines.append("Resolved inputs: {}".format(data["resolved_inputs"]))
        log_lines.append("Stats: {}".format(data["stats"]))
        log_lines.append("Bounding box: {}".format(bounding_box))
        exit_code = 0
    except Exception as exc:
        manifest = {
            "tool": TOOL_NAME,
            "runner": RUNNER_NAME,
            "status": "error",
            "error": str(exc),
            "outputs": {
                "log": "logs/last_run.log",
            },
        }
        _write_json(manifest_path, manifest)
        log_lines.append("Error: {}".format(exc))
        log_lines.append(traceback.format_exc().rstrip())
        exit_code = 1
    finally:
        log_lines.append("Runner end")
        log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    return {
        "exit_code": exit_code,
        "manifest": manifest,
        "log_path": log_path,
        "manifest_path": manifest_path,
        "data_path": data_path,
    }


def main(argv=None):
    """Parse CLI arguments and run the core preview report."""
    parser = argparse.ArgumentParser(description="Run the pure twist_tower core preview.")
    parser.add_argument("--input", dest="input_text", help="Optional key=value style input text.")
    args = parser.parse_args(argv)
    result = run_preview(input_text=args.input_text)
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
