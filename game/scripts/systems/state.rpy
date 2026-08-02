# game/scripts/systems/state.rpy -- default/persistent Variable Declarations
# The Embrace of the Twin Angels
# Story: E0.5
# Variable ownership per main-architecture.md Section 6

# ===========================================================================
# Save-level variables (default) -- saved/restored with Ren'Py saves
# ===========================================================================

# -- C1 Narrative Engine --
default current_chapter = 1                    # Current chapter number (1-16) | Owner: C1
default current_sephirot_id = 1                 # Current sephirot ID (1-16) | Owner: C1
default current_phase = Phase.FORGETTING         # Current Phase | Owner: C1
default narrative_beat = NarrativeBeat.ENCOUNTER # Current narrative beat | Owner: C1
default active_narrative_tags = set()            # Active narrative tag set | Owner: C1

# -- C2 Angel Companionship --
default wing_brightness_permanent = 1.0         # Wing permanent brightness (0.05-1.0) | Owner: C2
default wing_brightness_temporary = 0.0         # Wing temporary dimming | Owner: C2
default angel_presence_state = AngelPresenceState.PRESENT  # Angel presence state | Owner: C2
default angel_emotional_state = AngelEmotionalState.CALM   # Angel emotional state | Owner: C2
default angel_intervention_count = 0            # Angel intervention total count | Owner: C5->C2 read
default bond_depth = 0.0                        # Emotional bond depth (0.0-1.0) | Owner: C2
default hug_count_this_sephirot = 0             # Hugs in current sephirot | Owner: C2
default hug_cooldown_end_time = 0               # Click angel cooldown end time | Owner: C2

# -- C3 Choice System --
default choice_history = []                     # Choice history records | Owner: C3

# -- C4 Sephirot Progression --
default sephirot_states = {i: SephirotState.LOCKED for i in range(1, 17)}  # 16 sephirot states | Owner: C4
default escape_counts = {}                      # Per-sephirot escape counts {sephirot_id: count} | Owner: C4
default consecutive_escape_count = 0            # Consecutive escape count | Owner: C4

# -- C5 Existential Protection --
default undertow_state = {                      # Undertow runtime state | Owner: C5
    "active_undertows": [],
    "afterimage_undertows": [],
    "nihilism_warning_triggered": False,
    "intervention_log": [],
}
default final_choice_unlocked = False           # Final choice unlock flag | Owner: C5

# -- C6 Save System --
# (Save slots managed by Ren'Py natively, no default variables needed)


# ===========================================================================
# Cross-playthrough variables (persistent) -- not reset on new game
# ===========================================================================

default persistent.endings_seen = []             # Endings achieved list
default persistent.cg_unlocked = []              # Unlocked CG list
default persistent.total_playthroughs = 0        # Total playthrough count
default persistent.first_playthrough = True      # Is first playthrough
default persistent.sephirot_completion_records = {}  # Historical sephirot completion types

# -- Accessibility flags (persistent) --
default persistent.low_stim_mode = False         # Low stimulation mode
default persistent.visual_undertow_off = False   # Undertow visuals off
default persistent.screen_shake_off = False      # Screen shake off
default persistent.audio_stable_mode = False     # Audio stable mode


# ===========================================================================
# after_load hook: restore/validate after loading a save
# ===========================================================================

label after_load:
    python:
        # Save integrity validation
        validate_save_integrity()

        # Wing brightness range clamp
        wing_brightness_permanent = max(WING_BRIGHTNESS_MIN, min(1.0, wing_brightness_permanent))
        wing_brightness_temporary = max(0.0, wing_brightness_temporary)

        # Chapter number range clamp
        current_chapter = max(1, min(16, current_chapter))

        # Notify system updates (Batch 1+ implementation)
        # angel_system.update_visual()
        # narrative_router.sync_state()
    return
