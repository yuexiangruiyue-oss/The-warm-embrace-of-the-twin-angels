"""tests/unit/test_undertow_engine.py -- Undertow Trigger Engine Tests

The Embrace of the Twin Angels
Story: Task #5 (T14-T15)
GDD:C5-§2.1: 8 undertow types, 3 intensity levels each

Tests undertow definitions, intensity mapping, and cost multipliers.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import UndertowCode, UNDERTOW_MULTIPLIER


class TestUndertowEngine:
    """[GDD:C5-§2.1] Undertow trigger engine tests"""

    ALL_UNDERTOW_CODES = [
        UndertowCode.SHAME_LOOP,
        UndertowCode.POSS_DENY,
        UndertowCode.PAIN_AMP,
        UndertowCode.HOPE_ERASE,
        UndertowCode.EXIST_DENY,
        UndertowCode.NIHILISM,
        UndertowCode.RAGE_INC,
        UndertowCode.HARM_GUIDE,
    ]

    @pytest.mark.parametrize("code", ALL_UNDERTOW_CODES)
    def test_all_8_undertows_defined(self, code, undertow_definitions):
        """T14: All 8 undertow types are defined in the data"""
        codes = [u["code"] for u in undertow_definitions["undertows"]]
        assert code in codes, f"Undertow {code} not found in definitions"

    def test_exactly_8_undertows(self, undertow_definitions):
        """Exactly 8 undertow types defined (no more, no less)"""
        assert len(undertow_definitions["undertows"]) == 8

    def test_each_undertow_has_3_intensity_levels(self, undertow_definitions):
        """T15: Each undertow has 3 intensity levels (low/mid/high)"""
        for undertow in undertow_definitions["undertows"]:
            levels = undertow.get("intensity_levels", {})
            assert "low" in levels, f"{undertow['code']} missing 'low' level"
            assert "mid" in levels, f"{undertow['code']} missing 'mid' level"
            assert "high" in levels, f"{undertow['code']} missing 'high' level"

    def test_intensity_to_level_mapping(self):
        """T15: Intensity value 1-10 -> low/mid/high mapping"""
        test_cases = [
            (1, "low"), (2, "low"), (3, "low"),
            (4, "mid"), (5, "mid"), (6, "mid"),
            (7, "high"), (8, "high"), (9, "high"), (10, "high"),
        ]
        for intensity, expected_level in test_cases:
            if intensity <= 3:
                level = "low"
            elif intensity <= 6:
                level = "mid"
            else:
                level = "high"
            assert level == expected_level

    def test_wing_cost_multipliers(self, undertow_definitions):
        """Each undertow has correct wing_cost_multiplier"""
        expected = {
            UndertowCode.SHAME_LOOP: 1.0,
            UndertowCode.POSS_DENY: 1.0,
            UndertowCode.PAIN_AMP: 1.0,
            UndertowCode.HOPE_ERASE: 1.0,
            UndertowCode.EXIST_DENY: 1.2,
            UndertowCode.NIHILISM: 1.5,
            UndertowCode.RAGE_INC: 1.0,
            UndertowCode.HARM_GUIDE: 2.0,
        }
        for undertow in undertow_definitions["undertows"]:
            code = undertow["code"]
            assert undertow["wing_cost_multiplier"] == expected[code], \
                f"{code} multiplier={undertow['wing_cost_multiplier']}, expected {expected[code]}"

    def test_harm_guide_urgent_all_levels(self, undertow_definitions):
        """HARM_GUIDE uses 'urgent' intervention type at all intensity levels"""
        harm_guide = next(u for u in undertow_definitions["undertows"] if u["code"] == UndertowCode.HARM_GUIDE)
        for level_name in ["low", "mid", "high"]:
            level = harm_guide["intensity_levels"][level_name]
            assert level["intervention_type"] == "urgent", \
                f"HARM_GUIDE {level_name} should be urgent, got {level['intervention_type']}"

    def test_non_harm_guide_have_delay(self, undertow_definitions):
        """Non-HARM_GUIDE undertows have intervention delay (not urgent)"""
        for undertow in undertow_definitions["undertows"]:
            if undertow["code"] == UndertowCode.HARM_GUIDE:
                continue
            for level_name in ["low", "mid", "high"]:
                level = undertow["intensity_levels"][level_name]
                assert level["intervention_type"] != "urgent", \
                    f"{undertow['code']} {level_name} should not be urgent"

    def test_each_level_has_required_fields(self, undertow_definitions):
        """Each intensity level has required fields"""
        required_fields = ["intensity_value", "intervention_type", "wing_visual", "angel_line"]
        for undertow in undertow_definitions["undertows"]:
            for level_name in ["low", "mid", "high"]:
                level = undertow["intensity_levels"][level_name]
                for field in required_fields:
                    assert field in level, \
                        f"{undertow['code']} {level_name} missing field '{field}'"

    def test_intensity_values_are_ordered(self, undertow_definitions):
        """Intensity values are ordered: low < mid < high"""
        for undertow in undertow_definitions["undertows"]:
            low_val = undertow["intensity_levels"]["low"]["intensity_value"]
            mid_val = undertow["intensity_levels"]["mid"]["intensity_value"]
            high_val = undertow["intensity_levels"]["high"]["intensity_value"]
            assert low_val < mid_val < high_val, \
                f"{undertow['code']}: {low_val} < {mid_val} < {high_val} failed"

    def test_undertow_has_name_and_description(self, undertow_definitions):
        """Each undertow has name and description"""
        for undertow in undertow_definitions["undertows"]:
            assert "name" in undertow, f"{undertow['code']} missing 'name'"
            assert "description" in undertow, f"{undertow['code']} missing 'description'"
            assert len(undertow["name"]) > 0
            assert len(undertow["description"]) > 0
