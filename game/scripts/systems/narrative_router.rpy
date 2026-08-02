# game/scripts/systems/narrative_router.rpy -- C1 Chapter Routing
# The Embrace of the Twin Angels
# Story: E2.1, E2.4
# Routes between chapter labels, handles phase switching, title cards.

init python:

    class NarrativeRouter:
        """C1 Chapter Router: routes to chapter labels, detects phase transitions.

        Label naming: ch{NN}_sephirot_{NN}
        Phase transitions:
          Ch3->Ch4: FORGETTING -> TRIAL_EARLY
          Ch8->Ch9: TRIAL_EARLY -> TRIAL_LATE
          Ch13->Ch14: TRIAL_LATE -> TRUTH
        """

        @staticmethod
        def get_label_for_chapter(chapter_id):
            """Return the label name for a chapter number."""
            if not (1 <= chapter_id <= 16):
                raise InvalidChapterError(
                    f"Invalid chapter number: {chapter_id}. Must be 1-16."
                )
            return CHAPTER_LABELS.get(chapter_id, f"ch{chapter_id:02d}_sephirot_{chapter_id:02d}")

        @staticmethod
        def route_to_chapter(chapter_id):
            """Route to a chapter by updating state and jumping to its label.

            Args:
                chapter_id: Chapter number (1-16).

            Raises:
                InvalidChapterError: If chapter_id is out of range.
            """
            if not (1 <= chapter_id <= 16):
                raise InvalidChapterError(
                    f"Invalid chapter number: {chapter_id}. Must be 1-16."
                )

            global current_chapter, current_sephirot_id

            # Detect phase transition
            old_phase = current_phase
            new_phase = CHAPTER_PHASE_MAP.get(chapter_id, Phase.FORGETTING)

            # Update chapter and sephirot
            current_chapter = chapter_id
            current_sephirot_id = chapter_id

            # Handle phase transition
            if old_phase != new_phase:
                NarrativeRouter.on_phase_transition(old_phase, new_phase, chapter_id)

            # Update wing stage baseline for new chapter
            WingBrightnessModel.on_sephirot_enter(chapter_id)

            # Clear narrative tags for new chapter
            clear_tags()

            # Clear afterimages for new chapter (C5 integration, Batch 1+)
            # existential_protection.clear_afterimages_for_new_chapter()

            # Trigger autosave at chapter start
            try:
                SaveSystem.autosave_chapter_start()
            except Exception:
                pass  # Autosave is best-effort

        @staticmethod
        def on_phase_transition(old_phase, new_phase, chapter_id):
            """Handle phase transition side effects.

            Notifies C5 to update cost multiplier and C2 to update angel behavior.
            """
            global current_phase
            current_phase = new_phase

            # Log the transition
            # C5 integration (Batch 1+): update cost multiplier
            # C2 integration (Batch 1+): update angel behavior mode

            # Special handling for Ch16: disable existential protection
            if chapter_id == 16:
                global final_choice_unlocked, undertow_state
                final_choice_unlocked = True
                undertow_state["active_undertows"] = []
                undertow_state["afterimage_undertows"] = []
                WingBrightnessModel.reset_for_ch16()

        @staticmethod
        def get_current_narrative_context():
            """Return current narrative context as a dict.

            Returns:
                Dict with chapter, sephirot_id, phase, beat, tags.
            """
            return {
                "chapter": current_chapter,
                "sephirot_id": current_sephirot_id,
                "phase": current_phase,
                "beat": narrative_beat,
                "tags": set(active_narrative_tags) if active_narrative_tags else set(),
            }

        @staticmethod
        def show_chapter_title_card(chapter_num, chapter_name):
            """Show a chapter title card for 3 seconds then fade out.

            This is called from chapter scripts, not directly.
            """
            # This is handled in the .rpy label, not here
            # But we provide the text for convenience
            return f"第{chapter_num}章 · {chapter_name}"


# Convenience function for use in narrative scripts
# Usage: $ route_to_chapter(2)
python early:
    def route_to_chapter(chapter_id):
        """Global convenience function for chapter routing."""
        NarrativeRouter.route_to_chapter(chapter_id)
