# game/scripts/systems/save_system.rpy -- C6 Save System
# The Embrace of the Twin Angels
# Story: E1.1, E1.3, E1.4
# Uses Ren'Py native renpy.save/renpy.load API

init python:

    class SaveSystem:
        """C6 Save System: slot management, autosave triggers, persistent variables.

        Slot naming:
          - Manual: 'page_{N}-{slot}' (6 manual slots per page)
          - Auto: 'auto-1', 'auto-2', 'auto-3'
          - Quick: 'quick-1'
        """

        MANUAL_SLOTS_PER_PAGE = 6
        AUTO_SLOTS = ["auto-1", "auto-2", "auto-3"]
        QUICK_SLOT = "quick-1"

        @staticmethod
        def save(slot):
            """Save game to specified slot.

            Args:
                slot: Slot name string (e.g. '1-1', 'auto-1', 'quick-1').
            """
            renpy.save(slot)

        @staticmethod
        def load(slot):
            """Load game from specified slot.

            Args:
                slot: Slot name string.
            """
            renpy.load(slot)

        @staticmethod
        def get_slot_info(slot):
            """Get save slot metadata.

            Returns dict with: exists, chapter, sephirot_id, wing_stage, timestamp.
            """
            info = renpy.slot_json(slot)
            if info is None:
                return {"exists": False}

            # Extract info from saved state
            return {
                "exists": True,
                "chapter": info.get("current_chapter", 1),
                "sephirot_id": info.get("current_sephirot_id", 1),
                "wing_stage": WingBrightnessModel.get_stage(),
                "timestamp": renpy.slot_time(slot),
                "screenshot": renpy.slot_screenshot(slot),
            }

        @staticmethod
        def autosave_chapter_start():
            """Trigger autosave at chapter start (auto-1 slot)."""
            renpy.save("auto-1")

        @staticmethod
        def autosave_sephirot_complete():
            """Trigger autosave at sephirot completion (auto-2 slot)."""
            renpy.save("auto-2")

        @staticmethod
        def autosave_before_choice():
            """Trigger autosave before key choice (auto-3 slot)."""
            renpy.save("auto-3")

        @staticmethod
        def quick_save():
            """Quick save to quick-1 slot."""
            renpy.save("quick-1")

        @staticmethod
        def quick_load():
            """Quick load from quick-1 slot."""
            renpy.load("quick-1")

        @staticmethod
        def delete_slot(slot):
            """Delete a save slot."""
            renpy.unlink_save(slot)

        @staticmethod
        def get_sephirot_progress_summary():
            """Return progress summary for save/load UI display.

            Returns dict with: completed_count, total, current_sephirot, current_chapter.
            """
            completed = sum(
                1 for s in sephirot_states.values()
                if s in (SephirotState.COMPLETED_FULL, SephirotState.COMPLETED_HALF)
            )
            return {
                "completed_count": completed,
                "total": 16,
                "current_sephirot": current_sephirot_id,
                "current_chapter": current_chapter,
            }

        @staticmethod
        def unlock_ending(ending_code):
            """Record an ending as seen (persistent)."""
            if ending_code not in persistent.endings_seen:
                persistent.endings_seen.append(ending_code)

        @staticmethod
        def check_first_playthrough():
            """Check if this is the first playthrough."""
            return persistent.first_playthrough

        @staticmethod
        def new_game_init():
            """Initialize persistent variables for new game.

            Called from label start: before jumping to chapter 1.
            Resets default variables but preserves persistent.
            """
            persistent.total_playthroughs += 1
            persistent.first_playthrough = False

        @staticmethod
        def reset_save_variables():
            """Reset all save-level variables to defaults (new game).

            This is called from label start: to ensure clean state.
            """
            global current_chapter, current_sephirot_id, current_phase
            global narrative_beat, active_narrative_tags
            global wing_brightness_permanent, wing_brightness_temporary
            global angel_presence_state, angel_emotional_state
            global angel_intervention_count, bond_depth
            global hug_count_this_sephirot, hug_cooldown_end_time
            global choice_history, sephirot_states, escape_counts
            global consecutive_escape_count, undertow_state, final_choice_unlocked

            current_chapter = 1
            current_sephirot_id = 1
            current_phase = Phase.FORGETTING
            narrative_beat = NarrativeBeat.ENCOUNTER
            active_narrative_tags = set()

            wing_brightness_permanent = 1.0
            wing_brightness_temporary = 0.0
            angel_presence_state = AngelPresenceState.PRESENT
            angel_emotional_state = AngelEmotionalState.CALM
            angel_intervention_count = 0
            bond_depth = 0.0
            hug_count_this_sephirot = 0
            hug_cooldown_end_time = 0

            choice_history = []

            sephirot_states = {i: SephirotState.LOCKED for i in range(1, 17)}
            sephirot_states[1] = SephirotState.ACTIVE
            escape_counts = {}
            consecutive_escape_count = 0

            undertow_state = {
                "active_undertows": [],
                "afterimage_undertows": [],
                "nihilism_warning_triggered": False,
                "intervention_log": [],
            }
            final_choice_unlocked = False
