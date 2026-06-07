"""Tests for the pure core preview report runner."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from sandbox_runner.run_core_preview import run_preview


class RunCorePreviewTest(unittest.TestCase):
    def test_default_run_creates_manifest(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_preview(base_dir=tmp_dir)

            self.assertEqual(result["exit_code"], 0)
            self.assertTrue((Path(tmp_dir) / "preview" / "manifest.json").exists())

    def test_default_manifest_status_is_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_preview(base_dir=tmp_dir)

            self.assertEqual(result["manifest"]["status"], "success")

    def test_custom_input_updates_resolved_inputs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_preview(
                input_text="width=1500 height=8000 levels=30 twist_degrees=180",
                base_dir=tmp_dir,
            )

            resolved = result["manifest"]["resolved_inputs"]
            self.assertEqual(resolved["width"], 1500.0)
            self.assertEqual(resolved["height"], 8000.0)
            self.assertEqual(resolved["levels"], 30)
            self.assertEqual(resolved["twist_degrees"], 180.0)

    def test_manifest_includes_stats(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_preview(base_dir=tmp_dir)

            self.assertIn("stats", result["manifest"])
            self.assertEqual(result["manifest"]["stats"]["level_count"], 20)

    def test_manifest_includes_bounding_box(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_preview(base_dir=tmp_dir)

            bounding_box = result["manifest"]["bounding_box"]
            self.assertIn("min", bounding_box)
            self.assertIn("max", bounding_box)
            self.assertEqual(len(bounding_box["min"]), 3)
            self.assertEqual(len(bounding_box["max"]), 3)

    def test_invalid_input_records_error_and_returns_non_zero(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_preview(input_text="width=0", base_dir=tmp_dir)
            manifest_path = Path(tmp_dir) / "preview" / "manifest.json"
            log_path = Path(tmp_dir) / "logs" / "last_run.log"

            self.assertNotEqual(result["exit_code"], 0)
            self.assertEqual(result["manifest"]["status"], "error")
            self.assertTrue(manifest_path.exists())
            self.assertTrue(log_path.exists())
            self.assertIn("width must be greater than 0", result["manifest"]["error"])
            self.assertIn("Traceback", log_path.read_text(encoding="utf-8"))

    def test_success_writes_full_data_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            run_preview(base_dir=tmp_dir)
            data_path = Path(tmp_dir) / "preview" / "twist_tower_data.json"

            self.assertTrue(data_path.exists())
            payload = json.loads(data_path.read_text(encoding="utf-8"))
            self.assertIn("vertices", payload)
            self.assertIn("faces", payload)


if __name__ == "__main__":
    unittest.main()
