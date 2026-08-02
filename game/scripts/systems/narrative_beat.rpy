# game/scripts/systems/narrative_beat.rpy -- C1 Five-Beat Narrative Framework
# The Embrace of the Twin Angels
# Story: E2.3
# Five beats: ENCOUNTER -> STRUGGLE -> COMFORT -> CHOICE -> TRANSFORM

init python:

    class NarrativeBeatManager:
        """C1 Five-Beat Narrative Structure Manager.

        Beat order (strict, cannot skip):
          1. ENCOUNTER  - Pure narrative, no system calls
          2. STRUGGLE   - C5 undertow trigger: trigger_undertow(code, intensity)
          3. COMFORT    - C5 angel intervention (auto-triggered)
          4. CHOICE     - C3 choice presentation: present_choice(choice_id)
          5. TRANSFORM  - C4 progress update + chapter transition check

        After TRANSFORM, automatically checks if advancing to next sephirot.
        """

        BEAT_ORDER = [
            NarrativeBeat.ENCOUNTER,
            NarrativeBeat.STRUGGLE,
            NarrativeBeat.COMFORT,
            NarrativeBeat.CHOICE,
            NarrativeBeat.TRANSFORM,
        ]

        @staticmethod
        def get_current_beat():
            """Return the current narrative beat."""
            return narrative_beat

        @staticmethod
        def set_beat(beat):
            """Set the current narrative beat.

            Validates that the beat is in valid order (cannot go backwards).

            Args:
                beat: One of NarrativeBeat constants.

            Raises:
                ValueError: If beat order is violated.
            """
            global narrative_beat
            current_idx = NarrativeBeatManager.BEAT_ORDER.index(narrative_beat)
            new_idx = NarrativeBeatManager.BEAT_ORDER.index(beat)
            if new_idx < current_idx:
                raise ValueError(
                    f"Cannot go backwards in beat order: "
                    f"{narrative_beat} -> {beat}"
                )
            narrative_beat = beat

        @staticmethod
        def advance_beat():
            """Advance to the next beat in sequence.

            If current beat is TRANSFORM (last), checks if should advance to next sephirot.

            Returns:
                The new beat, or None if at TRANSFORM (end of cycle).
            """
            global narrative_beat
            current_idx = NarrativeBeatManager.BEAT_ORDER.index(narrative_beat)

            if current_idx < len(NarrativeBeatManager.BEAT_ORDER) - 1:
                narrative_beat = NarrativeBeatManager.BEAT_ORDER[current_idx + 1]
                return narrative_beat
            else:
                # At TRANSFORM: check if advancing to next sephirot
                NarrativeBeatManager._check_sephirot_transition()
                return None

        @staticmethod
        def _check_sephirot_transition():
            """Check if the narrative should advance to the next sephirot/chapter.

            Called after TRANSFORM beat.
            If current sephirot is completed, route to next chapter.
            """
            # Check if current sephirot is completed
            state = sephirot_states.get(current_sephirot_id, SephirotState.LOCKED)
            if state in (SephirotState.COMPLETED_FULL, SephirotState.COMPLETED_HALF):
                next_chapter = current_chapter + 1
                if next_chapter <= 16:
                    # Route to next chapter
                    route_to_chapter(next_chapter)

        @staticmethod
        def reset_beat():
            """Reset beat to ENCOUNTER (for new chapter/sephirot)."""
            global narrative_beat
            narrative_beat = NarrativeBeat.ENCOUNTER

        @staticmethod
        def is_at_choice():
            """Check if current beat is CHOICE."""
            return narrative_beat == NarrativeBeat.CHOICE

        @staticmethod
        def is_at_transform():
            """Check if current beat is TRANSFORM."""
            return narrative_beat == NarrativeBeat.TRANSFORM


# ── Stub functions for Batch 0 ──
# These are skeleton implementations that will be fully realized in Batch 1+.
# They allow Ch1 to run without the full C3/C4/C5 systems.

init python:

    def trigger_undertow(code, intensity):
        """Stub: Trigger an existential undertow.

        Full implementation in Batch 1 (E4.1).
        For Batch 0: adds to undertow_state and applies wing cost (Phase 1 = 0 cost).
        """
        global undertow_state, angel_intervention_count

        # Add to active undertows
        undertow_state["active_undertows"].append({
            "code": code,
            "intensity": intensity,
        })

        # Calculate wing cost (Phase 1 = 0, free protection)
        phase_mult = PHASE_MULTIPLIER.get(current_phase, 0.0)
        if phase_mult > 0:
            # Determine intensity level
            if intensity <= 3:
                level = "low"
            elif intensity <= 6:
                level = "mid"
            else:
                level = "high"

            int_mult = INTENSITY_MULTIPLIER.get(level, 0.5)
            undertow_mult = UNDERTOW_MULTIPLIER.get(code, 1.0)
            cost = BASE_COST * phase_mult * int_mult * undertow_mult

            if cost > 0:
                WingBrightnessModel.apply_permanent_dim(cost)

        # Log intervention
        undertow_state["intervention_log"].append({
            "chapter": current_chapter,
            "undertow": code,
            "intensity": intensity,
        })
        angel_intervention_count += 1

    def deactivate_undertow(code):
        """Stub: Deactivate an active undertow.

        Full implementation in Batch 1 (E4.5).
        For Batch 0: removes from active list and adds afterimage.
        """
        global undertow_state
        undertow_state["active_undertows"] = [
            uw for uw in undertow_state["active_undertows"]
            if uw.get("code") != code
        ]
        # Add afterimage (reduced intensity, persists until next chapter)
        undertow_state["afterimage_undertows"].append({
            "code": code,
            "intensity": 1.5,  # Afterimage intensity
        })
        # Clear temporary wing dimming
        WingBrightnessModel.clear_temporary_dim()

    def present_choice(choice_id):
        """Stub: Present a choice to the player.

        Full implementation in Batch 1 (E3.2).
        For Batch 0: uses Ren'Py menu with hardcoded Ch1 choices.
        """
        # This will be handled by the narrative script's menu statement
        # For now, this is a marker that C3 will hook into
        pass

    def complete_sephirot(sephirot_id):
        """Stub: Mark a sephirot as completed.

        Full implementation in Batch 2 (E6.1).
        For Batch 0: marks as COMPLETED_FULL and unlocks next.
        """
        global sephirot_states

        # Determine completion type from last choice
        # For Batch 0, default to COMPLETED_FULL
        sephirot_states[sephirot_id] = SephirotState.COMPLETED_FULL

        # Unlock next sephirot
        if sephirot_id < 16:
            sephirot_states[sephirot_id + 1] = SephirotState.ACTIVE

        # Record in persistent
        persistent.sephirot_completion_records[sephirot_id] = SephirotState.COMPLETED_FULL

        # Trigger autosave
        try:
            SaveSystem.autosave_sephirot_complete()
        except Exception:
            pass

    def complete_sephirot_with_tag(sephirot_id, confrontation_tag):
        """Complete a sephirot with a specific confrontation tag.

        ENGAGE -> COMPLETED_FULL
        ESCAPE (3rd time) -> COMPLETED_HALF (angel proxy)
        ESCAPE (< 3rd time) -> escape_counts[id] += 1, no completion yet
        NEUTRAL -> no progress
        """
        global sephirot_states, escape_counts, consecutive_escape_count

        if confrontation_tag == ConfrontationTag.ENGAGE:
            sephirot_states[sephirot_id] = SephirotState.COMPLETED_FULL
            consecutive_escape_count = 0
            if sephirot_id < 16:
                sephirot_states[sephirot_id + 1] = SephirotState.ACTIVE
            persistent.sephirot_completion_records[sephirot_id] = SephirotState.COMPLETED_FULL

        elif confrontation_tag == ConfrontationTag.ESCAPE:
            escape_counts[sephirot_id] = escape_counts.get(sephirot_id, 0) + 1
            consecutive_escape_count += 1

            if escape_counts[sephirot_id] >= ESCAPE_THRESHOLD:
                # Angel proxy: 50% completion
                sephirot_states[sephirot_id] = SephirotState.COMPLETED_HALF
                consecutive_escape_count = 0
                if sephirot_id < 16:
                    sephirot_states[sephirot_id + 1] = SephirotState.ACTIVE
                persistent.sephirot_completion_records[sephirot_id] = SephirotState.COMPLETED_HALF

        elif confrontation_tag == ConfrontationTag.NEUTRAL:
            pass  # No progress

        # Record choice in history
        import time
        choice_history.append({
            "sephirot_id": sephirot_id,
            "confrontation_tag": confrontation_tag,
            "timestamp": time.time(),
        })

        # Trigger autosave
        try:
            SaveSystem.autosave_sephirot_complete()
        except Exception:
            pass
