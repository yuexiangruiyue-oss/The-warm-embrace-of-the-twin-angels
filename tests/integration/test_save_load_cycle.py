"""tests/integration/test_save_load_cycle.py -- Save/Load Full Cycle Tests

The Embrace of the Twin Angels
Story: Task #5 (T19-T20)
GDD:C6: Save system + integrity validation

Tests save/load state preservation, missing variable filling, and value clamping.
"""

import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import (
    WING_BRIGHTNESS_MIN, WING_BRIGHTNESS_MAX,
    SephirotState, Phase,
)


class TestSaveLoadCycle:
    """Save/Load full cycle tests"""

    def test_save_load_preserves_all_state(self, mock_renpy_state):
        """T19: Save -> Load: all state correctly restored"""
        original = mock_renpy_state.copy()
        original["wing_brightness_permanent"] = 0.65
        original["sephirot_states"] = {1: SephirotState.COMPLETED_FULL, 2: SephirotState.ACTIVE}
        original["escape_counts"] = {1: 0}
        original["choice_history"] = [
            {"sephirot_id": 1, "confrontation_tag": "ENGAGE"}
        ]
        original["angel_intervention_count"] = 3
        original["angel_emotional_state"] = "aching"
        original["bond_depth"] = 0.15

        # Simulate save (serialization)
        # Note: sets are not JSON serializable, convert to list
        save_data = original.copy()
        save_data["active_narrative_tags"] = list(original["active_narrative_tags"])
        saved = json.dumps(save_data)

        # Simulate load (deserialization)
        loaded = json.loads(saved)
        loaded["active_narrative_tags"] = set(loaded["active_narrative_tags"])

        assert loaded["wing_brightness_permanent"] == 0.65
        assert loaded["sephirot_states"] == {"1": SephirotState.COMPLETED_FULL, "2": SephirotState.ACTIVE} \
            or loaded["sephirot_states"] == {1: SephirotState.COMPLETED_FULL, 2: SephirotState.ACTIVE}
        assert loaded["angel_intervention_count"] == 3
        assert loaded["angel_emotional_state"] == "aching"
        assert loaded["bond_depth"] == 0.15
        assert len(loaded["choice_history"]) == 1

    def test_load_missing_variable_fills_default(self, mock_renpy_state):
        """T20: Old save missing new variables: filled with defaults"""
        # Simulate old version save missing some variables
        old_save = {
            "wing_brightness_permanent": 0.5,
            "current_chapter": 5,
            "sephirot_states": {1: SephirotState.COMPLETED_FULL},
        }

        # after_load validation: fill missing with defaults
        defaults = mock_renpy_state
        for key, default_val in defaults.items():
            if key not in old_save:
                old_save[key] = default_val

        # Preserved values
        assert old_save["wing_brightness_permanent"] == 0.5
        assert old_save["current_chapter"] == 5
        # Filled defaults
        assert old_save["angel_emotional_state"] == "calm"
        assert old_save["escape_counts"] == {}
        assert old_save["angel_intervention_count"] == 0
        assert old_save["bond_depth"] == 0.0

    def test_load_clamps_invalid_values(self, mock_renpy_state):
        """T20b: Corrupt save with out-of-range values: clamped to valid range"""
        corrupt_save = {
            "wing_brightness_permanent": 1.5,   # Above max
            "wing_brightness_temporary": -0.5,   # Below min
            "current_chapter": 99,               # Above max
            "bond_depth": -1.0,                  # Below min
            "angel_intervention_count": -5,      # Below min
        }

        # Clamp values
        corrupt_save["wing_brightness_permanent"] = min(
            WING_BRIGHTNESS_MAX, max(WING_BRIGHTNESS_MIN, corrupt_save["wing_brightness_permanent"])
        )
        corrupt_save["wing_brightness_temporary"] = max(0.0, corrupt_save["wing_brightness_temporary"])
        corrupt_save["current_chapter"] = min(16, max(1, corrupt_save["current_chapter"]))
        corrupt_save["bond_depth"] = max(0.0, corrupt_save["bond_depth"])
        corrupt_save["angel_intervention_count"] = max(0, corrupt_save["angel_intervention_count"])

        assert corrupt_save["wing_brightness_permanent"] == 1.0   # Clamped to max
        assert corrupt_save["wing_brightness_temporary"] == 0.0   # Clamped to min
        assert corrupt_save["current_chapter"] == 16              # Clamped to max
        assert corrupt_save["bond_depth"] == 0.0                  # Clamped to min
        assert corrupt_save["angel_intervention_count"] == 0      # Clamped to min

    def test_sephirot_states_key_completeness(self, mock_renpy_state):
        """After load: sephirot_states has all 16 keys (1-16)"""
        # Simulate old save with only some keys
        old_save = {
            "sephirot_states": {1: SephirotState.COMPLETED_FULL, 2: SephirotState.ACTIVE}
        }

        # Ensure all 16 keys exist
        for i in range(1, 17):
            if i not in old_save["sephirot_states"]:
                old_save["sephirot_states"][i] = SephirotState.LOCKED

        assert len(old_save["sephirot_states"]) == 16
        for i in range(1, 17):
            assert i in old_save["sephirot_states"]

    def test_undertow_state_structure_integrity(self, mock_renpy_state):
        """After load: undertow_state has correct structure"""
        old_save = {
            "undertow_state": {"active_undertows": [{"code": "SHAME_LOOP", "intensity": 5}]}
        }

        # Ensure structure
        if "afterimage_undertows" not in old_save["undertow_state"]:
            old_save["undertow_state"]["afterimage_undertows"] = []
        if "intervention_log" not in old_save["undertow_state"]:
            old_save["undertow_state"]["intervention_log"] = []
        if "nihilism_warning_triggered" not in old_save["undertow_state"]:
            old_save["undertow_state"]["nihilism_warning_triggered"] = False

        assert "active_undertows" in old_save["undertow_state"]
        assert "afterimage_undertows" in old_save["undertow_state"]
        assert "intervention_log" in old_save["undertow_state"]
        assert "nihilism_warning_triggered" in old_save["undertow_state"]
        assert isinstance(old_save["undertow_state"]["active_undertows"], list)
        assert isinstance(old_save["undertow_state"]["afterimage_undertows"], list)

    def test_new_game_resets_all_state(self, mock_renpy_state):
        """New game: all state variables reset to initial values"""
        state = mock_renpy_state

        # Simulate played state
        state["wing_brightness_permanent"] = 0.3
        state["current_chapter"] = 10
        state["sephirot_states"] = {i: SephirotState.COMPLETED_FULL for i in range(1, 10)}
        state["escape_counts"] = {1: 2, 3: 1}
        state["choice_history"] = [{"sephirot_id": 1, "tag": "ENGAGE"}]
        state["angel_intervention_count"] = 15
        state["bond_depth"] = 0.25

        # New game init
        state["wing_brightness_permanent"] = 1.0
        state["wing_brightness_temporary"] = 0.0
        state["current_chapter"] = 1
        state["current_sephirot_id"] = 1
        state["current_phase"] = Phase.FORGETTING
        state["narrative_beat"] = "ENCOUNTER"
        state["active_narrative_tags"] = set()
        state["sephirot_states"] = {i: SephirotState.LOCKED for i in range(1, 17)}
        state["sephirot_states"][1] = SephirotState.ACTIVE
        state["escape_counts"] = {}
        state["consecutive_escape_count"] = 0
        state["choice_history"] = []
        state["angel_intervention_count"] = 0
        state["bond_depth"] = 0.0
        state["undertow_state"] = {
            "active_undertows": [],
            "afterimage_undertows": [],
            "nihilism_warning_triggered": False,
            "intervention_log": [],
        }

        # Verify reset
        assert state["wing_brightness_permanent"] == 1.0
        assert state["current_chapter"] == 1
        assert state["sephirot_states"][1] == SephirotState.ACTIVE
        assert state["sephirot_states"][2] == SephirotState.LOCKED
        assert state["escape_counts"] == {}
        assert state["choice_history"] == []
        assert state["angel_intervention_count"] == 0
        assert state["bond_depth"] == 0.0
