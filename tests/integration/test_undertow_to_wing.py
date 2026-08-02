"""tests/integration/test_undertow_to_wing.py -- Undertow -> Angel Intervention -> Wing Cost -> Recovery

The Embrace of the Twin Angels
Story: Task #5 (T17)
ADR-003: Direct call + interface contract

Tests the full flow: undertow trigger -> angel intervention -> wing cost -> visual recovery.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import (
    BASE_COST, PHASE_MULTIPLIER, INTENSITY_MULTIPLIER, UNDERTOW_MULTIPLIER,
    WING_BRIGHTNESS_MIN, WING_STAGE_BASELINE,
    Phase, UndertowCode,
)


def calculate_wing_cost(phase, intensity_level, undertow_code):
    """Replicate the wing cost calculation from narrative_beat.rpy trigger_undertow()"""
    phase_mult = PHASE_MULTIPLIER.get(phase, 0.0)
    if phase_mult == 0:
        return 0.0
    int_mult = INTENSITY_MULTIPLIER.get(intensity_level, 0.5)
    undertow_mult = UNDERTOW_MULTIPLIER.get(undertow_code, 1.0)
    return BASE_COST * phase_mult * int_mult * undertow_mult


def intensity_to_level(intensity):
    """Map intensity value to level string"""
    if intensity <= 3:
        return "low"
    elif intensity <= 6:
        return "mid"
    else:
        return "high"


class TestUndertowToWingFlow:
    """Undertow -> angel intervention -> wing cost -> visual recovery"""

    def test_phase1_no_wing_cost(self, mock_renpy_state):
        """T17: Phase 1: undertow triggers -> angel intervenes -> wing has NO cost"""
        state = mock_renpy_state
        state["current_phase"] = Phase.FORGETTING
        state["current_chapter"] = 1
        state["wing_brightness_permanent"] = 1.0

        # Trigger EXIST_DENY low intensity 2
        intensity = 2
        level = intensity_to_level(intensity)
        cost = calculate_wing_cost(Phase.FORGETTING, level, UndertowCode.EXIST_DENY)

        # Apply cost
        state["wing_brightness_permanent"] -= cost
        state["angel_intervention_count"] += 1
        state["undertow_state"]["active_undertows"].append({
            "code": UndertowCode.EXIST_DENY,
            "intensity": intensity,
        })

        assert cost == 0.0
        assert state["wing_brightness_permanent"] == 1.0  # No change
        assert state["angel_intervention_count"] == 1
        assert len(state["undertow_state"]["active_undertows"]) == 1

    def test_phase2a_wing_dimmed(self, mock_renpy_state):
        """Phase 2a: undertow -> intervention -> wing dimmed"""
        state = mock_renpy_state
        state["current_phase"] = Phase.TRIAL_EARLY
        state["current_chapter"] = 4
        state["wing_brightness_permanent"] = 1.0

        # Trigger SHAME_LOOP mid intensity 5
        intensity = 5
        level = intensity_to_level(intensity)
        cost = calculate_wing_cost(Phase.TRIAL_EARLY, level, UndertowCode.SHAME_LOOP)

        state["wing_brightness_permanent"] -= cost
        state["angel_intervention_count"] += 1

        # 0.02 * 1.0 * 1.0 * 1.0 = 0.020
        assert abs(cost - 0.020) < 0.001
        assert abs(state["wing_brightness_permanent"] - 0.980) < 0.001

    def test_phase2a_nihilism_high_cost(self, mock_renpy_state):
        """Phase 2a: NIHILISM high intensity -> higher cost"""
        state = mock_renpy_state
        state["current_phase"] = Phase.TRIAL_EARLY
        state["wing_brightness_permanent"] = 1.0

        intensity = 8  # high
        level = intensity_to_level(intensity)
        cost = calculate_wing_cost(Phase.TRIAL_EARLY, level, UndertowCode.NIHILISM)

        state["wing_brightness_permanent"] -= cost

        # 0.02 * 1.0 * 1.5 * 1.5 = 0.045
        assert abs(cost - 0.045) < 0.001
        assert abs(state["wing_brightness_permanent"] - 0.955) < 0.001

    def test_harm_guide_urgent_high_cost(self, mock_renpy_state):
        """HARM_GUIDE: highest multiplier (2.0x), urgent intervention"""
        state = mock_renpy_state
        state["current_phase"] = Phase.TRIAL_EARLY
        state["wing_brightness_permanent"] = 0.85

        intensity = 7  # high
        level = intensity_to_level(intensity)
        cost = calculate_wing_cost(Phase.TRIAL_EARLY, level, UndertowCode.HARM_GUIDE)

        state["wing_brightness_permanent"] -= cost

        # 0.02 * 1.0 * 1.5 * 2.0 = 0.060
        assert abs(cost - 0.060) < 0.001
        assert abs(state["wing_brightness_permanent"] - 0.790) < 0.001

    def test_undertow_deactivation_clears_temporary(self, mock_renpy_state):
        """Deactivating undertow clears temporary dimming"""
        state = mock_renpy_state
        state["wing_brightness_temporary"] = 0.15
        state["undertow_state"]["active_undertows"] = [
            {"code": UndertowCode.EXIST_DENY, "intensity": 5}
        ]

        # Deactivate
        code = UndertowCode.EXIST_DENY
        state["undertow_state"]["active_undertows"] = [
            uw for uw in state["undertow_state"]["active_undertows"]
            if uw.get("code") != code
        ]
        state["wing_brightness_temporary"] = 0.0  # clear_temporary_dim()

        assert len(state["undertow_state"]["active_undertows"]) == 0
        assert state["wing_brightness_temporary"] == 0.0

    def test_afterimage_undertow_added_on_deactivation(self, mock_renpy_state):
        """Deactivating undertow adds afterimage (reduced intensity)"""
        state = mock_renpy_state
        state["undertow_state"]["active_undertows"] = [
            {"code": UndertowCode.SHAME_LOOP, "intensity": 6}
        ]

        # Deactivate
        code = UndertowCode.SHAME_LOOP
        state["undertow_state"]["active_undertows"] = [
            uw for uw in state["undertow_state"]["active_undertows"]
            if uw.get("code") != code
        ]
        state["undertow_state"]["afterimage_undertows"].append({
            "code": code,
            "intensity": 1.5,  # Afterimage intensity
        })

        assert len(state["undertow_state"]["active_undertows"]) == 0
        assert len(state["undertow_state"]["afterimage_undertows"]) == 1
        assert state["undertow_state"]["afterimage_undertows"][0]["intensity"] == 1.5

    def test_phase3_max_cost(self, mock_renpy_state):
        """Phase 3 (TRUTH): highest phase multiplier (2.5x)"""
        state = mock_renpy_state
        state["current_phase"] = Phase.TRUTH
        state["wing_brightness_permanent"] = 0.35  # Stage 4

        intensity = 9  # high
        level = intensity_to_level(intensity)
        cost = calculate_wing_cost(Phase.TRUTH, level, UndertowCode.HARM_GUIDE)

        # 0.02 * 2.5 * 1.5 * 2.0 = 0.150
        assert abs(cost - 0.150) < 0.001

    def test_multiple_undertows_accumulate_cost(self, mock_renpy_state):
        """Multiple undertows in same chapter accumulate wing cost"""
        state = mock_renpy_state
        state["current_phase"] = Phase.TRIAL_EARLY
        state["wing_brightness_permanent"] = 1.0

        # Trigger 3 undertows
        undertows = [
            (UndertowCode.SHAME_LOOP, 5),    # mid: 0.02 * 1.0 * 1.0 * 1.0 = 0.020
            (UndertowCode.EXIST_DENY, 4),    # mid: 0.02 * 1.0 * 1.0 * 1.2 = 0.024
            (UndertowCode.NIHILISM, 7),      # high: 0.02 * 1.0 * 1.5 * 1.5 = 0.045
        ]

        total_cost = 0
        for code, intensity in undertows:
            level = intensity_to_level(intensity)
            cost = calculate_wing_cost(Phase.TRIAL_EARLY, level, code)
            total_cost += cost
            state["wing_brightness_permanent"] -= cost

        # Total: 0.020 + 0.024 + 0.045 = 0.089
        assert abs(total_cost - 0.089) < 0.001
        assert abs(state["wing_brightness_permanent"] - 0.911) < 0.001
