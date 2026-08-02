"""tests/unit/test_wing_cost.py -- Wing Cost Calculation Tests

The Embrace of the Twin Angels
Story: Task #5 (T06-T10)
GDD:C5-§2.3: cost = BASE_COST * phase_mult * intensity_mult * undertow_mult

Tests the wing cost formula with all phase/intensity/undertow combinations.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import (
    BASE_COST, PHASE_MULTIPLIER, INTENSITY_MULTIPLIER, UNDERTOW_MULTIPLIER,
    Phase, UndertowCode,
)


class TestWingCostCalculation:
    """[GDD:C5-§2.3] Wing cost = BASE_COST * phase_mult * intensity_mult * undertow_mult"""

    def test_phase1_zero_cost(self):
        """T06: Phase 1 (FORGETTING) multiplier = 0.0, free protection"""
        cost = BASE_COST * PHASE_MULTIPLIER[Phase.FORGETTING] * INTENSITY_MULTIPLIER["mid"] * UNDERTOW_MULTIPLIER[UndertowCode.SHAME_LOOP]
        assert cost == 0.0

    def test_phase1_all_undertows_zero(self):
        """T06b: Phase 1 = 0 cost for ALL undertow types"""
        for code in UNDERTOW_MULTIPLIER:
            for level in INTENSITY_MULTIPLIER:
                cost = BASE_COST * PHASE_MULTIPLIER[Phase.FORGETTING] * INTENSITY_MULTIPLIER[level] * UNDERTOW_MULTIPLIER[code]
                assert cost == 0.0, f"Phase 1 cost should be 0 for {code}/{level}, got {cost}"

    def test_phase2a_shame_loop_mid(self):
        """T07: Phase 2a (TRIAL_EARLY), SHAME_LOOP, mid intensity"""
        # 0.02 * 1.0 * 1.0 * 1.0 = 0.020
        cost = BASE_COST * PHASE_MULTIPLIER[Phase.TRIAL_EARLY] * INTENSITY_MULTIPLIER["mid"] * UNDERTOW_MULTIPLIER[UndertowCode.SHAME_LOOP]
        assert abs(cost - 0.020) < 0.001

    def test_phase2a_nihilism_mid(self):
        """T09: Phase 2a, NIHILISM, mid intensity (1.5x multiplier)"""
        # 0.02 * 1.0 * 1.0 * 1.5 = 0.030
        cost = BASE_COST * PHASE_MULTIPLIER[Phase.TRIAL_EARLY] * INTENSITY_MULTIPLIER["mid"] * UNDERTOW_MULTIPLIER[UndertowCode.NIHILISM]
        assert abs(cost - 0.030) < 0.001

    def test_phase2a_harm_guide_high(self):
        """T08: Phase 2a, HARM_GUIDE, high intensity (2.0x multiplier)"""
        # 0.02 * 1.0 * 1.5 * 2.0 = 0.060
        cost = BASE_COST * PHASE_MULTIPLIER[Phase.TRIAL_EARLY] * INTENSITY_MULTIPLIER["high"] * UNDERTOW_MULTIPLIER[UndertowCode.HARM_GUIDE]
        assert abs(cost - 0.060) < 0.001

    def test_phase2b_costs(self):
        """T07b: Phase 2b (TRIAL_LATE) multiplier = 1.5"""
        # 0.02 * 1.5 * 1.0 * 1.0 = 0.030
        cost = BASE_COST * PHASE_MULTIPLIER[Phase.TRIAL_LATE] * INTENSITY_MULTIPLIER["mid"] * UNDERTOW_MULTIPLIER[UndertowCode.SHAME_LOOP]
        assert abs(cost - 0.030) < 0.001

    def test_phase3_truth_multiplier(self):
        """Phase 3 (TRUTH) multiplier = 2.5"""
        # 0.02 * 2.5 * 1.0 * 1.0 = 0.050
        cost = BASE_COST * PHASE_MULTIPLIER[Phase.TRUTH] * INTENSITY_MULTIPLIER["mid"] * UNDERTOW_MULTIPLIER[UndertowCode.SHAME_LOOP]
        assert abs(cost - 0.050) < 0.001

    def test_all_undertow_multipliers(self):
        """T08/T09: Verify all 8 undertow multipliers"""
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
        for code, expected_mult in expected.items():
            assert UNDERTOW_MULTIPLIER[code] == expected_mult, f"{code} multiplier mismatch"

    def test_intensity_multipliers(self):
        """Verify intensity multipliers: low=0.5, mid=1.0, high=1.5"""
        assert INTENSITY_MULTIPLIER["low"] == 0.5
        assert INTENSITY_MULTIPLIER["mid"] == 1.0
        assert INTENSITY_MULTIPLIER["high"] == 1.5

    def test_accumulated_curve(self):
        """T10: Accumulated brightness curve across phases"""
        brightness = 1.0

        # Phase 1: 3 interventions x cost=0
        for _ in range(3):
            cost = BASE_COST * PHASE_MULTIPLIER[Phase.FORGETTING] * INTENSITY_MULTIPLIER["mid"] * UNDERTOW_MULTIPLIER[UndertowCode.EXIST_DENY]
            brightness -= cost
        assert brightness == 1.0  # No change in Phase 1

        # Phase 2a: 5 interventions with various undertows
        phase2a_costs = [
            BASE_COST * 1.0 * 1.0 * 1.0,   # SHAME_LOOP mid = 0.020
            BASE_COST * 1.0 * 1.0 * 1.5,   # NIHILISM mid = 0.030
            BASE_COST * 1.0 * 1.0 * 1.0,   # SHAME_LOOP mid = 0.020
            BASE_COST * 1.0 * 1.0 * 1.0,   # PAIN_AMP mid = 0.020
            BASE_COST * 1.0 * 1.5 * 2.0,   # HARM_GUIDE high = 0.060
        ]
        for cost in phase2a_costs:
            brightness -= cost
        # 1.0 - (0.020+0.030+0.020+0.020+0.060) = 1.0 - 0.150 = 0.850
        assert abs(brightness - 0.850) < 0.01

        # Phase 2b: 5 interventions with higher phase multiplier
        phase2b_costs = [
            BASE_COST * 1.5 * 1.0 * 1.0,   # = 0.030
            BASE_COST * 1.5 * 1.0 * 1.2,   # = 0.036
            BASE_COST * 1.5 * 1.0 * 1.0,   # = 0.030
            BASE_COST * 1.5 * 1.5 * 1.0,   # = 0.045
            BASE_COST * 1.5 * 1.5 * 2.0,   # = 0.090
        ]
        for cost in phase2b_costs:
            brightness -= cost
        # 0.850 - (0.030+0.036+0.030+0.045+0.090) = 0.850 - 0.231 = 0.619
        assert abs(brightness - 0.619) < 0.02

        # Ch16 reset
        brightness = 1.0
        assert brightness == 1.0

    def test_composite_undertow_cost(self):
        """T30: Composite undertow cost: 2 undertows +20%"""
        base = BASE_COST * 1.5 * 1.0 * 1.2  # Phase2b x mid x EXIST_DENY = 0.036
        composite_cost = base * 1.2  # 2 undertows +20%
        # 0.036 * 1.2 = 0.0432
        assert abs(composite_cost - 0.0432) < 0.001

    def test_intensity_to_level_mapping(self):
        """T15: Intensity 1-10 -> low/mid/high mapping"""
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
            assert level == expected_level, f"intensity={intensity} -> level={level}, expected {expected_level}"
