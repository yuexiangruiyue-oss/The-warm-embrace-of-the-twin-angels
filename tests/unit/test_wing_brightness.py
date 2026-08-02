"""tests/unit/test_wing_brightness.py -- Wing Brightness Dual-Layer Model Tests

The Embrace of the Twin Angels
Story: Task #5 (T01-T05)
ADR-004: permanent + temporary -> displayed

Tests the mathematical logic of the wing brightness model
outside of Ren'Py runtime by replicating the formulas.
"""

import pytest
import sys
from pathlib import Path

# Add tests directory to path for constants import
sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import (
    WING_BRIGHTNESS_MIN, WING_STAGE_BASELINE,
    Phase, NarrativeBeat,
)


class TestWingBrightnessModel:
    """[ADR-004] Wing Brightness Dual-Layer Model Tests"""

    def test_initial_state(self, mock_renpy_state):
        """T01: Initial state permanent=1.0, temporary=0, displayed=1.0"""
        state = mock_renpy_state
        assert state["wing_brightness_permanent"] == 1.0
        assert state["wing_brightness_temporary"] == 0.0
        displayed = max(WING_BRIGHTNESS_MIN, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert displayed == 1.0

    def test_apply_permanent_dim(self, mock_renpy_state):
        """T02: Permanent deduction reduces permanent brightness"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] -= 0.15  # Simulate C5 cost
        displayed = max(WING_BRIGHTNESS_MIN, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert state["wing_brightness_permanent"] == 0.85
        assert displayed == 0.85

    def test_apply_temporary_dim(self, mock_renpy_state):
        """T03: Temporary dimming increases temporary, lowers displayed"""
        state = mock_renpy_state
        state["wing_brightness_temporary"] = 0.2  # High-intensity undertow instant effect
        displayed = max(WING_BRIGHTNESS_MIN, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert displayed == 0.8

    def test_clear_temporary(self, mock_renpy_state):
        """T03b: Scene end clears temporary dimming"""
        state = mock_renpy_state
        state["wing_brightness_temporary"] = 0.2
        state["wing_brightness_temporary"] = 0.0  # clear_temporary_dim()
        displayed = max(WING_BRIGHTNESS_MIN, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert displayed == 1.0  # Restored to permanent

    def test_dynamic_floor(self, mock_renpy_state):
        """T04: Brightness does not go below dynamic floor"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] = 0.15  # Stage 5 baseline
        state["wing_brightness_temporary"] = 0.1   # Temporary dimming
        # Dynamic floor = max(0.05, 0.15 * 0.15) = max(0.05, 0.0225) = 0.05
        dynamic_floor = max(WING_BRIGHTNESS_MIN, WING_STAGE_BASELINE[5] * 0.15)
        displayed = max(dynamic_floor, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        # max(0.05, 0.15 - 0.1) = max(0.05, 0.05) = 0.05
        assert displayed == 0.05

    def test_dynamic_floor_stage1(self, mock_renpy_state):
        """T04b: Dynamic floor for Stage 1 = max(0.05, 1.0*0.15) = 0.15"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] = 0.2  # Below stage 1 baseline
        state["wing_brightness_temporary"] = 0.1
        dynamic_floor = max(WING_BRIGHTNESS_MIN, WING_STAGE_BASELINE[1] * 0.15)
        assert dynamic_floor == 0.15
        displayed = max(dynamic_floor, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        # max(0.15, 0.2 - 0.1) = max(0.15, 0.1) = 0.15
        assert displayed == 0.15

    def test_stage_mapping(self, mock_renpy_state):
        """T05: permanent brightness -> wing stage (1-5) mapping"""
        test_cases = [
            (1.0, 1), (0.85, 1), (0.8, 1),
            (0.79, 2), (0.65, 2), (0.6, 2),
            (0.59, 3), (0.4, 3),
            (0.39, 4), (0.2, 4),
            (0.19, 5), (0.05, 5),
        ]
        for brightness, expected_stage in test_cases:
            # Replicate get_stage() logic from wing_brightness.rpy
            if brightness >= 0.8:
                stage = 1
            elif brightness >= 0.6:
                stage = 2
            elif brightness >= 0.4:
                stage = 3
            elif brightness >= 0.2:
                stage = 4
            else:
                stage = 5
            assert stage == expected_stage, f"brightness={brightness} -> stage={stage}, expected {expected_stage}"

    def test_stage_baseline_set(self, mock_renpy_state):
        """Setting stage baseline resets permanent to baseline and clears temporary"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] = 0.5
        state["wing_brightness_temporary"] = 0.2

        # Simulate set_stage_baseline(3)
        stage = 3
        state["wing_brightness_permanent"] = WING_STAGE_BASELINE[stage]
        state["wing_brightness_temporary"] = 0.0

        assert state["wing_brightness_permanent"] == 0.65
        assert state["wing_brightness_temporary"] == 0.0

    def test_ch16_reset(self, mock_renpy_state):
        """Ch16 reset: permanent -> 1.0, temporary -> 0.0"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] = 0.15  # Stage 5, darkest
        state["wing_brightness_temporary"] = 0.05

        # Simulate reset_for_ch16()
        state["wing_brightness_permanent"] = 1.0
        state["wing_brightness_temporary"] = 0.0

        assert state["wing_brightness_permanent"] == 1.0
        assert state["wing_brightness_temporary"] == 0.0

    def test_permanent_dim_clamped_to_floor(self, mock_renpy_state):
        """Permanent dim cannot go below dynamic floor"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] = 0.15  # Stage 5
        # Dynamic floor for stage 5 = max(0.05, 0.15*0.15) = 0.05
        floor = max(WING_BRIGHTNESS_MIN, WING_STAGE_BASELINE[5] * 0.15)
        # Apply dim of 0.2 (more than available)
        state["wing_brightness_permanent"] = max(floor, state["wing_brightness_permanent"] - 0.2)
        assert state["wing_brightness_permanent"] == 0.05  # Clamped to floor

    def test_temporary_dim_clamped(self, mock_renpy_state):
        """Temporary dim cannot make displayed go below MIN"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] = 0.3
        # Temporary can be at most (permanent - MIN) = 0.3 - 0.05 = 0.25
        max_temp = state["wing_brightness_permanent"] - WING_BRIGHTNESS_MIN
        state["wing_brightness_temporary"] = min(max_temp, 0.5)  # Try to set 0.5
        assert state["wing_brightness_temporary"] == 0.25
        displayed = max(WING_BRIGHTNESS_MIN, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert displayed == 0.05  # At MIN
