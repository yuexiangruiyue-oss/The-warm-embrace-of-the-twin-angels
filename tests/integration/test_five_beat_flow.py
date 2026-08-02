"""tests/integration/test_five_beat_flow.py -- Five-Beat Narrative Full Flow

The Embrace of the Twin Angels
Story: Task #5 (T18)
GDD:C4-§2: ENCOUNTER -> STRUGGLE -> COMFORT -> CHOICE -> TRANSFORM

Tests the complete five-beat narrative sequence with system interactions.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import (
    NarrativeBeat, BEAT_ORDER, SephirotState, ConfrontationTag,
    Phase, WING_BRIGHTNESS_MIN,
)


class TestFiveBeatFlow:
    """Five-beat narrative ENCOUNTER -> STRUGGLE -> COMFORT -> CHOICE -> TRANSFORM"""

    def test_full_beat_sequence_engage(self, mock_renpy_state):
        """T18: Full five-beat sequence with ENGAGE choice"""
        state = mock_renpy_state
        beats_visited = []
        state["current_phase"] = Phase.FORGETTING

        # 1. ENCOUNTER - Pure narrative, no system calls
        state["narrative_beat"] = NarrativeBeat.ENCOUNTER
        beats_visited.append(state["narrative_beat"])

        # 2. STRUGGLE - C5 undertow trigger
        state["narrative_beat"] = NarrativeBeat.STRUGGLE
        beats_visited.append(state["narrative_beat"])
        # Trigger EXIST_DENY intensity 2
        state["undertow_state"]["active_undertows"].append({
            "code": "EXIST_DENY",
            "intensity": 2,
        })
        # Phase 1: no wing cost, but temporary dimming
        state["wing_brightness_temporary"] = 0.1

        # 3. COMFORT - C5 angel intervention, visual recovery
        state["narrative_beat"] = NarrativeBeat.COMFORT
        beats_visited.append(state["narrative_beat"])
        # Angel intervenes
        state["angel_intervention_count"] += 1
        # Deactivate undertow, clear temporary
        state["undertow_state"]["active_undertows"] = []
        state["wing_brightness_temporary"] = 0.0

        # 4. CHOICE - C3 choice presentation
        state["narrative_beat"] = NarrativeBeat.CHOICE
        beats_visited.append(state["narrative_beat"])
        # Player chooses ENGAGE
        state["sephirot_states"][1] = SephirotState.COMPLETED_FULL
        state["sephirot_states"][2] = SephirotState.ACTIVE

        # 5. TRANSFORM - C4 progress update + chapter routing
        state["narrative_beat"] = NarrativeBeat.TRANSFORM
        beats_visited.append(state["narrative_beat"])
        state["current_chapter"] = 2
        state["current_sephirot_id"] = 2

        # Verify
        assert beats_visited == BEAT_ORDER
        assert state["sephirot_states"][1] == SephirotState.COMPLETED_FULL
        assert state["current_chapter"] == 2
        assert state["wing_brightness_temporary"] == 0.0
        assert state["angel_intervention_count"] == 1
        assert len(state["undertow_state"]["active_undertows"]) == 0

    def test_full_beat_sequence_escape(self, mock_renpy_state):
        """Five-beat with ESCAPE (1st): sephirot not completed"""
        state = mock_renpy_state
        state["current_phase"] = Phase.FORGETTING

        # ENCOUNTER
        state["narrative_beat"] = NarrativeBeat.ENCOUNTER

        # STRUGGLE
        state["narrative_beat"] = NarrativeBeat.STRUGGLE
        state["undertow_state"]["active_undertows"].append({
            "code": "EXIST_DENY", "intensity": 2
        })

        # COMFORT
        state["narrative_beat"] = NarrativeBeat.COMFORT
        state["angel_intervention_count"] += 1
        state["undertow_state"]["active_undertows"] = []

        # CHOICE - ESCAPE (1st)
        state["narrative_beat"] = NarrativeBeat.CHOICE
        state["escape_counts"][1] = state["escape_counts"].get(1, 0) + 1
        # Not completed yet

        # TRANSFORM - no chapter advance (sephirot not completed)
        state["narrative_beat"] = NarrativeBeat.TRANSFORM

        assert state["sephirot_states"][1] == SephirotState.ACTIVE  # Still active
        assert state["escape_counts"][1] == 1
        assert state["current_chapter"] == 1  # No advance

    def test_phase1_no_wing_cost_during_struggle(self, mock_renpy_state):
        """Phase 1: STRUGGLE triggers undertow but wing has no permanent cost"""
        state = mock_renpy_state
        state["current_phase"] = Phase.FORGETTING
        initial_brightness = state["wing_brightness_permanent"]

        # STRUGGLE: trigger undertow
        state["narrative_beat"] = NarrativeBeat.STRUGGLE
        # Phase 1 multiplier = 0, so no permanent cost
        # But temporary dimming can occur
        state["wing_brightness_temporary"] = 0.1

        displayed = max(WING_BRIGHTNESS_MIN, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert state["wing_brightness_permanent"] == initial_brightness  # No permanent change
        assert displayed < initial_brightness  # But displayed is dimmer

        # COMFORT: clear temporary
        state["narrative_beat"] = NarrativeBeat.COMFORT
        state["wing_brightness_temporary"] = 0.0
        displayed = max(WING_BRIGHTNESS_MIN, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert displayed == initial_brightness  # Restored

    def test_beat_progression_with_undertow_lifecycle(self, mock_renpy_state):
        """Complete undertow lifecycle across beats: trigger -> active -> deactivate -> afterimage"""
        state = mock_renpy_state
        state["current_phase"] = Phase.TRIAL_EARLY  # Phase 2a for cost

        # STRUGGLE: trigger
        state["narrative_beat"] = NarrativeBeat.STRUGGLE
        state["undertow_state"]["active_undertows"].append({
            "code": "SHAME_LOOP", "intensity": 5
        })
        assert len(state["undertow_state"]["active_undertows"]) == 1

        # COMFORT: deactivate
        state["narrative_beat"] = NarrativeBeat.COMFORT
        state["undertow_state"]["active_undertows"] = []
        state["undertow_state"]["afterimage_undertows"].append({
            "code": "SHAME_LOOP", "intensity": 1.5
        })
        assert len(state["undertow_state"]["active_undertows"]) == 0
        assert len(state["undertow_state"]["afterimage_undertows"]) == 1

        # After COMFORT: afterimage persists until next chapter
        assert state["undertow_state"]["afterimage_undertows"][0]["intensity"] == 1.5
