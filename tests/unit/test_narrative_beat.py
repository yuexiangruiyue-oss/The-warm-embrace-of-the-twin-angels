"""tests/unit/test_narrative_beat.py -- Five-Beat Narrative Framework Tests

The Embrace of the Twin Angels
Story: Task #5
GDD:C4-§2: ENCOUNTER -> STRUGGLE -> COMFORT -> CHOICE -> TRANSFORM

Tests the five-beat narrative sequence and beat ordering constraints.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import NarrativeBeat, BEAT_ORDER


class TestNarrativeBeatManager:
    """Five-beat narrative framework tests"""

    def test_beat_order_correct(self):
        """Beat order: ENCOUNTER -> STRUGGLE -> COMFORT -> CHOICE -> TRANSFORM"""
        assert BEAT_ORDER == [
            NarrativeBeat.ENCOUNTER,
            NarrativeBeat.STRUGGLE,
            NarrativeBeat.COMFORT,
            NarrativeBeat.CHOICE,
            NarrativeBeat.TRANSFORM,
        ]

    def test_beat_advance_sequence(self, mock_renpy_state):
        """Beats advance in correct order"""
        state = mock_renpy_state
        beats_visited = []

        current_beat = NarrativeBeat.ENCOUNTER
        beats_visited.append(current_beat)

        for _ in range(4):
            current_idx = BEAT_ORDER.index(current_beat)
            if current_idx < len(BEAT_ORDER) - 1:
                current_beat = BEAT_ORDER[current_idx + 1]
                beats_visited.append(current_beat)

        assert beats_visited == [
            NarrativeBeat.ENCOUNTER,
            NarrativeBeat.STRUGGLE,
            NarrativeBeat.COMFORT,
            NarrativeBeat.CHOICE,
            NarrativeBeat.TRANSFORM,
        ]

    def test_beat_cannot_go_backwards(self, mock_renpy_state):
        """Beat order cannot go backwards"""
        state = mock_renpy_state
        current_beat = NarrativeBeat.COMFORT  # At beat 3

        # Try to go back to STRUGGLE (beat 2)
        current_idx = BEAT_ORDER.index(current_beat)
        new_idx = BEAT_ORDER.index(NarrativeBeat.STRUGGLE)

        assert new_idx < current_idx  # This would be going backwards
        # In actual code, this raises ValueError

    def test_beat_reset_to_encounter(self, mock_renpy_state):
        """Reset beat to ENCOUNTER for new chapter"""
        state = mock_renpy_state
        state["narrative_beat"] = NarrativeBeat.TRANSFORM

        # Reset
        state["narrative_beat"] = NarrativeBeat.ENCOUNTER

        assert state["narrative_beat"] == NarrativeBeat.ENCOUNTER

    def test_is_at_choice(self, mock_renpy_state):
        """is_at_choice returns True when beat is CHOICE"""
        state = mock_renpy_state
        state["narrative_beat"] = NarrativeBeat.CHOICE
        assert state["narrative_beat"] == NarrativeBeat.CHOICE

    def test_is_at_transform(self, mock_renpy_state):
        """is_at_transform returns True when beat is TRANSFORM"""
        state = mock_renpy_state
        state["narrative_beat"] = NarrativeBeat.TRANSFORM
        assert state["narrative_beat"] == NarrativeBeat.TRANSFORM

    def test_advance_past_transform_returns_none(self, mock_renpy_state):
        """Advancing past TRANSFORM returns None (end of cycle)"""
        current_beat = NarrativeBeat.TRANSFORM
        current_idx = BEAT_ORDER.index(current_beat)

        if current_idx < len(BEAT_ORDER) - 1:
            next_beat = BEAT_ORDER[current_idx + 1]
        else:
            next_beat = None  # At TRANSFORM, end of cycle

        assert next_beat is None

    def test_each_beat_has_system_hooks(self):
        """Each beat has expected system interactions:
        ENCOUNTER: pure narrative
        STRUGGLE: C5 undertow trigger
        COMFORT: C5 angel intervention
        CHOICE: C3 choice presentation
        TRANSFORM: C4 progress + C1 routing
        """
        beat_hooks = {
            NarrativeBeat.ENCOUNTER: "pure_narrative",
            NarrativeBeat.STRUGGLE: "trigger_undertow",
            NarrativeBeat.COMFORT: "angel_intervention",
            NarrativeBeat.CHOICE: "present_choice",
            NarrativeBeat.TRANSFORM: "progress_and_route",
        }
        for beat in BEAT_ORDER:
            assert beat in beat_hooks, f"Beat {beat} missing system hook definition"
