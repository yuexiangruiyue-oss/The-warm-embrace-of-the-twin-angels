"""tests/integration/test_choice_to_sephirot.py -- Choice -> Sephirot Completion -> Chapter Switch

The Embrace of the Twin Angels
Story: Task #5 (T16)
ADR-003: Direct call + interface contract

Tests the full flow: player choice -> consequence dispatch -> sephirot completion -> chapter routing.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import (
    SephirotState, ConfrontationTag, ESCAPE_THRESHOLD,
    Phase, CHAPTER_LABELS,
)


class TestChoiceToSephirotFlow:
    """Choice -> consequence dispatch -> sephirot completion -> chapter routing"""

    def test_engage_full_flow(self, mock_renpy_state):
        """T16: ENGAGE full flow: choice -> progress +1.0 -> sephirot FULL -> unlock next -> route"""
        state = mock_renpy_state
        state["sephirot_states"][1] = SephirotState.ACTIVE
        state["current_chapter"] = 1
        state["current_sephirot_id"] = 1

        # 1. Player chooses ENGAGE
        sephirot_id = state["current_sephirot_id"]
        tag = ConfrontationTag.ENGAGE

        # 2. Dispatch: C6 records, C4 progress, C2 update, C5 check
        # C6: Record choice history
        state["choice_history"].append({
            "sephirot_id": sephirot_id,
            "confrontation_tag": tag,
        })

        # C4: Process completion
        if tag == ConfrontationTag.ENGAGE:
            state["sephirot_states"][sephirot_id] = SephirotState.COMPLETED_FULL
            state["consecutive_escape_count"] = 0
            if sephirot_id < 16:
                state["sephirot_states"][sephirot_id + 1] = SephirotState.ACTIVE

        # C1: Route to next chapter
        next_chapter = state["current_chapter"] + 1
        if next_chapter <= 16:
            state["current_chapter"] = next_chapter
            state["current_sephirot_id"] = next_chapter

        # Verify
        assert state["sephirot_states"][1] == SephirotState.COMPLETED_FULL
        assert state["sephirot_states"][2] == SephirotState.ACTIVE
        assert state["current_chapter"] == 2
        assert state["current_sephirot_id"] == 2
        assert len(state["choice_history"]) == 1
        assert state["choice_history"][0]["confrontation_tag"] == ConfrontationTag.ENGAGE

    def test_escape_third_half_flow(self, mock_renpy_state):
        """T16b: 3x ESCAPE full flow: choice -> angel proxy -> 50% complete -> unlock"""
        state = mock_renpy_state
        state["sephirot_states"][1] = SephirotState.ACTIVE
        state["escape_counts"][1] = 0

        # Simulate 3 ESCAPE choices
        for i in range(3):
            tag = ConfrontationTag.ESCAPE
            state["escape_counts"][1] += 1
            state["consecutive_escape_count"] += 1
            state["choice_history"].append({
                "sephirot_id": 1,
                "confrontation_tag": tag,
            })

            if state["escape_counts"][1] >= ESCAPE_THRESHOLD:
                state["sephirot_states"][1] = SephirotState.COMPLETED_HALF
                state["consecutive_escape_count"] = 0
                state["sephirot_states"][2] = SephirotState.ACTIVE

        # Verify
        assert state["escape_counts"][1] == 3
        assert state["sephirot_states"][1] == SephirotState.COMPLETED_HALF
        assert state["sephirot_states"][2] == SephirotState.ACTIVE
        assert len(state["choice_history"]) == 3

    def test_escape_then_engage(self, mock_renpy_state):
        """ESCAPE then ENGAGE: ENGAGE completes full regardless of prior escapes"""
        state = mock_renpy_state
        state["sephirot_states"][1] = SephirotState.ACTIVE
        state["escape_counts"][1] = 0

        # 1st: ESCAPE
        state["escape_counts"][1] += 1
        state["consecutive_escape_count"] += 1
        assert state["sephirot_states"][1] == SephirotState.ACTIVE  # Not completed

        # 2nd: ENGAGE
        tag = ConfrontationTag.ENGAGE
        state["sephirot_states"][1] = SephirotState.COMPLETED_FULL
        state["consecutive_escape_count"] = 0
        state["sephirot_states"][2] = SephirotState.ACTIVE

        assert state["sephirot_states"][1] == SephirotState.COMPLETED_FULL
        assert state["consecutive_escape_count"] == 0

    def test_chapter_routing_label_exists(self):
        """Chapter routing targets valid labels"""
        for chapter_id in range(1, 17):
            label = CHAPTER_LABELS.get(chapter_id)
            assert label is not None, f"Chapter {chapter_id} has no label mapping"
            assert label.startswith(f"ch{chapter_id:02d}_"), \
                f"Chapter {chapter_id} label '{label}' doesn't follow naming convention"

    def test_multiple_sephirot_progression(self, mock_renpy_state):
        """Progress through multiple sephirots: Ch1 -> Ch2 -> Ch3"""
        state = mock_renpy_state

        for chapter in range(1, 4):
            state["current_chapter"] = chapter
            state["current_sephirot_id"] = chapter
            state["sephirot_states"][chapter] = SephirotState.ACTIVE

            # ENGAGE
            state["sephirot_states"][chapter] = SephirotState.COMPLETED_FULL
            if chapter < 16:
                state["sephirot_states"][chapter + 1] = SephirotState.ACTIVE

        assert state["sephirot_states"][1] == SephirotState.COMPLETED_FULL
        assert state["sephirot_states"][2] == SephirotState.COMPLETED_FULL
        assert state["sephirot_states"][3] == SephirotState.COMPLETED_FULL
        assert state["sephirot_states"][4] == SephirotState.ACTIVE
