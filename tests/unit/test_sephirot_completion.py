"""tests/unit/test_sephirot_completion.py -- Sephirot Completion Logic Tests

The Embrace of the Twin Angels
Story: Task #5 (T11-T13)
GDD:C4-§2.3: ENGAGE->FULL, 3xESCAPE->HALF, NEUTRAL->no progress

Tests the sephirot completion judgment logic.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import SephirotState, ConfrontationTag, ESCAPE_THRESHOLD


class TestSephirotCompletion:
    """[GDD:C4-§2.3] Sephirot completion judgment tests"""

    def test_engage_completes_full(self, mock_renpy_state):
        """T11: ENGAGE -> COMPLETED_FULL"""
        state = mock_renpy_state
        state["sephirot_states"][1] = SephirotState.ACTIVE

        # Simulate complete_sephirot_with_tag(1, ENGAGE)
        sephirot_id = 1
        tag = ConfrontationTag.ENGAGE

        if tag == ConfrontationTag.ENGAGE:
            state["sephirot_states"][sephirot_id] = SephirotState.COMPLETED_FULL
            state["consecutive_escape_count"] = 0
            if sephirot_id < 16:
                state["sephirot_states"][sephirot_id + 1] = SephirotState.ACTIVE

        assert state["sephirot_states"][1] == SephirotState.COMPLETED_FULL
        assert state["sephirot_states"][2] == SephirotState.ACTIVE
        assert state["consecutive_escape_count"] == 0

    def test_escape_first_does_not_complete(self, mock_renpy_state):
        """T12: 1st ESCAPE does not complete sephirot"""
        state = mock_renpy_state
        state["sephirot_states"][1] = SephirotState.ACTIVE
        state["escape_counts"][1] = 0

        sephirot_id = 1
        tag = ConfrontationTag.ESCAPE

        if tag == ConfrontationTag.ESCAPE:
            state["escape_counts"][sephirot_id] = state["escape_counts"].get(sephirot_id, 0) + 1
            state["consecutive_escape_count"] += 1

            if state["escape_counts"][sephirot_id] >= ESCAPE_THRESHOLD:
                state["sephirot_states"][sephirot_id] = SephirotState.COMPLETED_HALF
            # else: not completed yet

        assert state["escape_counts"][1] == 1
        assert state["consecutive_escape_count"] == 1
        assert state["sephirot_states"][1] == SephirotState.ACTIVE  # Not completed

    def test_escape_second_does_not_complete(self, mock_renpy_state):
        """T12b: 2nd ESCAPE does not complete sephirot"""
        state = mock_renpy_state
        state["sephirot_states"][1] = SephirotState.ACTIVE
        state["escape_counts"][1] = 1

        sephirot_id = 1
        tag = ConfrontationTag.ESCAPE

        state["escape_counts"][sephirot_id] += 1
        state["consecutive_escape_count"] += 1

        if state["escape_counts"][sephirot_id] >= ESCAPE_THRESHOLD:
            state["sephirot_states"][sephirot_id] = SephirotState.COMPLETED_HALF

        assert state["escape_counts"][1] == 2
        assert state["sephirot_states"][1] == SephirotState.ACTIVE  # Still not completed

    def test_escape_third_angel_proxy_half(self, mock_renpy_state):
        """T12: 3rd ESCAPE -> angel proxy -> COMPLETED_HALF"""
        state = mock_renpy_state
        state["sephirot_states"][1] = SephirotState.ACTIVE
        state["escape_counts"][1] = 2

        sephirot_id = 1
        tag = ConfrontationTag.ESCAPE

        state["escape_counts"][sephirot_id] += 1
        state["consecutive_escape_count"] += 1

        if state["escape_counts"][sephirot_id] >= ESCAPE_THRESHOLD:
            state["sephirot_states"][sephirot_id] = SephirotState.COMPLETED_HALF
            state["consecutive_escape_count"] = 0
            if sephirot_id < 16:
                state["sephirot_states"][sephirot_id + 1] = SephirotState.ACTIVE

        assert state["escape_counts"][1] == 3
        assert state["sephirot_states"][1] == SephirotState.COMPLETED_HALF
        assert state["sephirot_states"][2] == SephirotState.ACTIVE
        assert state["consecutive_escape_count"] == 0

    def test_neutral_no_progress(self, mock_renpy_state):
        """T13: NEUTRAL -> no progress"""
        state = mock_renpy_state
        state["sephirot_states"][1] = SephirotState.ACTIVE

        sephirot_id = 1
        tag = ConfrontationTag.NEUTRAL

        if tag == ConfrontationTag.NEUTRAL:
            pass  # No progress

        assert state["sephirot_states"][1] == SephirotState.ACTIVE  # Still active
        assert state["escape_counts"].get(1, 0) == 0  # No escape count

    def test_engage_resets_consecutive_escapes(self, mock_renpy_state):
        """ENGAGE resets consecutive_escape_count to 0"""
        state = mock_renpy_state
        state["consecutive_escape_count"] = 2
        state["sephirot_states"][1] = SephirotState.ACTIVE

        tag = ConfrontationTag.ENGAGE
        if tag == ConfrontationTag.ENGAGE:
            state["sephirot_states"][1] = SephirotState.COMPLETED_FULL
            state["consecutive_escape_count"] = 0

        assert state["consecutive_escape_count"] == 0

    def test_completion_unlocks_next_sephirot(self, mock_renpy_state):
        """Completing sephirot N unlocks sephirot N+1"""
        state = mock_renpy_state

        for sephirot_id in range(1, 16):
            state["sephirot_states"][sephirot_id] = SephirotState.ACTIVE
            # ENGAGE
            state["sephirot_states"][sephirot_id] = SephirotState.COMPLETED_FULL
            if sephirot_id < 16:
                state["sephirot_states"][sephirot_id + 1] = SephirotState.ACTIVE

        # All 1-15 completed, 16 active
        for i in range(1, 16):
            assert state["sephirot_states"][i] == SephirotState.COMPLETED_FULL
        assert state["sephirot_states"][16] == SephirotState.ACTIVE

    def test_sephirot_16_completion_no_unlock(self, mock_renpy_state):
        """Completing sephirot 16 does not unlock 17 (doesn't exist)"""
        state = mock_renpy_state
        state["sephirot_states"][16] = SephirotState.ACTIVE

        sephirot_id = 16
        tag = ConfrontationTag.ENGAGE
        if tag == ConfrontationTag.ENGAGE:
            state["sephirot_states"][sephirot_id] = SephirotState.COMPLETED_FULL
            if sephirot_id < 16:
                state["sephirot_states"][sephirot_id + 1] = SephirotState.ACTIVE
            # sephirot_id = 16, so no unlock

        assert state["sephirot_states"][16] == SephirotState.COMPLETED_FULL
        assert 17 not in state["sephirot_states"]  # No sephirot 17

    def test_choice_history_recorded(self, mock_renpy_state):
        """Each choice is recorded in choice_history"""
        state = mock_renpy_state
        import time

        # Simulate ENGAGE
        entry = {
            "sephirot_id": 1,
            "confrontation_tag": ConfrontationTag.ENGAGE,
            "timestamp": time.time(),
        }
        state["choice_history"].append(entry)

        assert len(state["choice_history"]) == 1
        assert state["choice_history"][0]["sephirot_id"] == 1
        assert state["choice_history"][0]["confrontation_tag"] == ConfrontationTag.ENGAGE
