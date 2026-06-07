"""Tests for pure twisted tower generation."""

from __future__ import annotations

import unittest

from core.twist_tower_core import generate_twist_tower_data, resolve_inputs


class TwistTowerCoreTest(unittest.TestCase):
    def test_empty_input_uses_defaults(self):
        resolved = resolve_inputs({})

        self.assertEqual(resolved["width"], 1000)
        self.assertEqual(resolved["height"], 5000)
        self.assertEqual(resolved["twist_degrees"], 90)

    def test_default_levels_is_20(self):
        data = generate_twist_tower_data({})

        self.assertEqual(data["resolved_inputs"]["levels"], 20)
        self.assertEqual(data["stats"]["level_count"], 20)

    def test_vertex_count_is_levels_times_four(self):
        data = generate_twist_tower_data({"levels": 7})

        self.assertEqual(data["stats"]["vertex_count"], 7 * 4)
        self.assertEqual(len(data["vertices"]), 7 * 4)

    def test_face_count_is_side_faces_plus_caps(self):
        levels = 7
        data = generate_twist_tower_data({"levels": levels})

        self.assertEqual(data["stats"]["face_count"], (levels - 1) * 4 + 2)
        self.assertEqual(len(data["faces"]), (levels - 1) * 4 + 2)

    def test_numeric_value_overrides_twist_degrees(self):
        data = generate_twist_tower_data({"value": 135})

        self.assertEqual(data["resolved_inputs"]["twist_degrees"], 135.0)

    def test_key_value_text_overrides_inputs(self):
        data = generate_twist_tower_data(
            {"value": "width=1500 height=8000 levels=30 twist_degrees=180"}
        )

        resolved = data["resolved_inputs"]
        self.assertEqual(resolved["width"], 1500.0)
        self.assertEqual(resolved["height"], 8000.0)
        self.assertEqual(resolved["levels"], 30)
        self.assertEqual(resolved["twist_degrees"], 180.0)

    def test_list_input_maps_to_main_values(self):
        data = generate_twist_tower_data([1500, 8000, 30, 180])

        resolved = data["resolved_inputs"]
        self.assertEqual(resolved["width"], 1500.0)
        self.assertEqual(resolved["height"], 8000.0)
        self.assertEqual(resolved["levels"], 30)
        self.assertEqual(resolved["twist_degrees"], 180.0)

    def test_invalid_width_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "width must be greater than 0"):
            generate_twist_tower_data({"width": 0})

    def test_invalid_height_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "height must be greater than 0"):
            generate_twist_tower_data({"height": 0})

    def test_levels_less_than_two_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "levels must be 2 or greater"):
            generate_twist_tower_data({"levels": 1})


if __name__ == "__main__":
    unittest.main()
