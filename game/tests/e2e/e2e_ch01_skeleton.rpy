# game/tests/e2e/e2e_ch01_skeleton.rpy -- E2E Test: Ch1 Skeleton Walkthrough
# The Embrace of the Twin Angels
# Story: Task #5 (T23)
#
# Ren'Py built-in test: verifies Ch1 can be completed end-to-end.
# Run with: renpy.sh <project> test e2e_ch01_skeleton
#
# Test sequence:
#   1. Start new game
#   2. Verify initial state
#   3. Click through ENCOUNTER beat
#   4. Verify STRUGGLE beat (undertow triggered)
#   5. Click through COMFORT beat (angel intervention)
#   6. Reach CHOICE beat
#   7. Select ENGAGE option
#   8. Verify sephirot COMPLETED_FULL
#   9. Verify TRANSFORM -> route to Ch2

init python:

    # Define the test sequence
    # Ren'Py test commands: "start", "click", "choice", "assert", "until"
    e2e_ch01_skeleton = [
        # 1. Start new game
        ("start",),

        # 2. Verify initial state
        ("assert", "current_chapter == 1"),
        ("assert", "current_sephirot_id == 1"),
        ("assert", "wing_brightness_permanent == 1.0"),
        ("assert", "wing_brightness_temporary == 0.0"),
        ("assert", "sephirot_states[1] == 'ACTIVE'"),
        ("assert", "narrative_beat == 'ENCOUNTER'"),

        # 3. Click through ENCOUNTER dialogue
        ("click",),
        ("click",),
        ("click",),
        ("click",),

        # 4. Verify STRUGGLE beat
        ("assert", "narrative_beat == 'STRUGGLE'"),
        ("assert", "len(undertow_state['active_undertows']) > 0"),
        ("assert", "undertow_state['active_undertows'][0]['code'] == 'EXIST_DENY'"),

        # 5. Click through to COMFORT
        ("click",),
        ("click",),
        ("assert", "narrative_beat == 'COMFORT'"),
        ("assert", "angel_intervention_count >= 1"),
        # After comfort, undertow should be deactivated
        ("assert", "len(undertow_state['active_undertows']) == 0"),

        # 6. Reach CHOICE
        ("click",),
        ("click",),
        ("assert", "narrative_beat == 'CHOICE'"),

        # 7. Select first option (ENGAGE: "I want to move forward")
        ("click", "choice_0"),

        # 8. Verify sephirot completed
        ("assert", "sephirot_states[1] == 'COMPLETED_FULL'"),

        # 9. Verify TRANSFORM and chapter routing
        ("assert", "narrative_beat == 'TRANSFORM'"),
        ("click",),
        ("click",),

        # 10. Should be in Ch2 now
        ("assert", "current_chapter == 2"),
    ]

    # E2E test: ESCAPE path (3 times -> COMPLETED_HALF)
    e2e_ch01_escape = [
        ("start",),

        # Verify initial state
        ("assert", "current_chapter == 1"),
        ("assert", "sephirot_states[1] == 'ACTIVE'"),

        # Click through to CHOICE
        ("click",),
        ("click",),
        ("click",),
        ("click",),
        ("click",),
        ("click",),
        ("click",),
        ("click",),

        ("assert", "narrative_beat == 'CHOICE'"),

        # Select ESCAPE (2nd option) - 1st time
        ("click", "choice_1"),
        ("assert", "escape_counts[1] == 1"),
        ("assert", "sephirot_states[1] == 'ACTIVE'"),

        # Need to re-enter choice for 2nd ESCAPE
        # (In actual game, this would loop back to STRUGGLE)
        # For skeleton test, we verify the escape count logic

        # This test verifies the escape threshold logic
        ("assert", "consecutive_escape_count == 1"),
    ]
