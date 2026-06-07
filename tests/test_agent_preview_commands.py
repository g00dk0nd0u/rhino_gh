"""Pure Python tests for AgentPreview command wrapper scripts."""

from __future__ import annotations

import importlib
import io
import sys
import types
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


COMMAND_MODULE_NAMES = [
    "plugin.commands.AgentPreviewRun",
    "plugin.commands.AgentPreviewClear",
    "plugin.commands.AgentPreviewZoom",
    "plugin.commands.AgentPreviewCommit",
]


class AgentPreviewCommandsTest(unittest.TestCase):
    def test_command_modules_import_without_rhino(self):
        for module_name in COMMAND_MODULE_NAMES:
            with self.subTest(module_name=module_name):
                module = importlib.import_module(module_name)
                self.assertTrue(callable(module.main))

    def test_command_sources_include_main_footer(self):
        for module_name in COMMAND_MODULE_NAMES:
            with self.subTest(module_name=module_name):
                module = importlib.import_module(module_name)
                source_text = Path(module.__file__).read_text(encoding="utf-8")
                self.assertIn('if __name__ == "__main__":', source_text)

    def test_command_module_names_and_sources_do_not_contain_ryo(self):
        commands_dir = Path(__file__).resolve().parents[1] / "plugin" / "commands"

        for path in sorted(commands_dir.glob("*.py")):
            with self.subTest(path=path.name):
                self.assertNotIn("Ryo", path.name)
                self.assertNotIn("Ryo", path.read_text(encoding="utf-8"))

    def test_agent_preview_run_cancel_does_not_call_preview(self):
        module = importlib.import_module("plugin.commands.AgentPreviewRun")
        fake_rs = types.ModuleType("rhinoscriptsyntax")
        fake_rs.GetString = lambda prompt, default=None: None

        with (
            mock.patch.dict(sys.modules, {"rhinoscriptsyntax": fake_rs}),
            mock.patch.object(module.preview, "run_preview") as run_preview,
            mock.patch.object(module.preview, "zoom_to_preview") as zoom_to_preview,
            redirect_stdout(io.StringIO()) as stdout,
        ):
            module.main()

        self.assertIn("canceled", stdout.getvalue())
        run_preview.assert_not_called()
        zoom_to_preview.assert_not_called()

    def test_agent_preview_run_calls_preview_and_zoom(self):
        module = importlib.import_module("plugin.commands.AgentPreviewRun")
        fake_rs = types.ModuleType("rhinoscriptsyntax")
        fake_rs.GetString = lambda prompt, default=None: default

        with (
            mock.patch.dict(sys.modules, {"rhinoscriptsyntax": fake_rs}),
            mock.patch.object(module.preview, "run_preview", return_value="preview ok") as run_preview,
            mock.patch.object(module.preview, "zoom_to_preview", return_value="zoom ok") as zoom_to_preview,
            redirect_stdout(io.StringIO()) as stdout,
        ):
            module.main()

        run_preview.assert_called_once_with(module.DEFAULT_INPUT)
        zoom_to_preview.assert_called_once_with()
        output = stdout.getvalue()
        self.assertIn("preview ok", output)
        self.assertIn("zoom ok", output)

    def test_other_commands_call_matching_preview_functions(self):
        scenarios = [
            ("plugin.commands.AgentPreviewClear", "clear_preview", ("clear ok",)),
            ("plugin.commands.AgentPreviewZoom", "zoom_to_preview", ("zoom ok",)),
            ("plugin.commands.AgentPreviewCommit", "commit_preview", ((3, "commit ok"),)),
        ]

        for module_name, function_name, return_values in scenarios:
            with self.subTest(module_name=module_name):
                module = importlib.import_module(module_name)
                with (
                    mock.patch.object(
                        module.preview,
                        function_name,
                        return_value=return_values[0],
                    ) as preview_function,
                    redirect_stdout(io.StringIO()) as stdout,
                ):
                    module.main()

                preview_function.assert_called_once_with()
                self.assertIn("ok", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
