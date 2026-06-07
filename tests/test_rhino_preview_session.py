"""Pure Python tests for the Rhino preview session module."""

from __future__ import annotations

import unittest

from plugin import rhino_preview_session


class RhinoPreviewSessionTest(unittest.TestCase):
    def test_module_imports_without_rhino(self):
        self.assertTrue(hasattr(rhino_preview_session, "run_preview"))
        self.assertTrue(hasattr(rhino_preview_session, "commit_preview"))

    def test_normalize_none_returns_empty_dict(self):
        self.assertEqual(rhino_preview_session._normalize_input(None), {})

    def test_normalize_empty_string_returns_empty_dict(self):
        self.assertEqual(rhino_preview_session._normalize_input(""), {})
        self.assertEqual(rhino_preview_session._normalize_input("   "), {})

    def test_normalize_non_empty_string_returns_value_dict(self):
        self.assertEqual(
            rhino_preview_session._normalize_input("width=1500"),
            {"value": "width=1500"},
        )

    def test_logger_collects_info_and_error_text(self):
        logger = rhino_preview_session.Logger()

        logger.info("hello")
        logger.error("problem")

        self.assertEqual(logger.text(), "hello\nproblem")


if __name__ == "__main__":
    unittest.main()
