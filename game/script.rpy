# game/script.rpy -- Ren'Py Entry Point
# The Embrace of the Twin Angels
# Routes from label start: to Chapter 1

label start:
    python:
        # Initialize new game state
        persistent.total_playthroughs += 1
        persistent.first_playthrough = False

        # Reset save-level variables to defaults
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

    # Route to Chapter 1
    jump ch01_sephirot_01
