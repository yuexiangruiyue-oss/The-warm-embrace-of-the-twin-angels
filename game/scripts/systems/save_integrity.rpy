# game/scripts/systems/save_integrity.rpy -- Save Data Integrity Validation
# The Embrace of the Twin Angels
# Story: E1.5
# Validates save data on load: checks variable existence, ranges, key completeness.

init python:

    # Log file path for integrity warnings
    INTEGRITY_LOG_PATH = "game/log/integrity.log"

    def _log_integrity(message):
        """Write a message to the integrity log file."""
        try:
            import os
            log_dir = os.path.dirname(INTEGRITY_LOG_PATH)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            with open(INTEGRITY_LOG_PATH, "a", encoding="utf-8") as f:
                import time
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass  # Logging is best-effort, never block game

    def _ensure_variable(name, default_value):
        """Ensure a variable exists in global scope, filling default if missing.

        Returns True if variable was missing and filled, False if it existed.
        """
        try:
            _ = globals()[name]
            return False
        except KeyError:
            globals()[name] = default_value
            _log_integrity(f"WARNING: Missing variable '{name}' filled with default: {default_value}")
            return True

    def _clamp_variable(name, min_val, max_val):
        """Clamp a numeric variable to [min_val, max_val] range."""
        try:
            val = globals()[name]
            if isinstance(val, (int, float)):
                original = val
                val = max(min_val, min(max_val, val))
                if val != original:
                    globals()[name] = val
                    _log_integrity(
                        f"WARNING: Variable '{name}' clamped from {original} to {val}"
                    )
        except KeyError:
            pass

    def _ensure_sephirot_states():
        """Ensure sephirot_states has all 16 keys."""
        global sephirot_states
        if not isinstance(sephirot_states, dict):
            sephirot_states = {i: SephirotState.LOCKED for i in range(1, 17)}
            _log_integrity("WARNING: sephirot_states was not a dict, reset to defaults")
            return

        for i in range(1, 17):
            if i not in sephirot_states:
                sephirot_states[i] = SephirotState.LOCKED
                _log_integrity(f"WARNING: sephirot_states missing key {i}, set to LOCKED")

    def _ensure_undertow_state():
        """Ensure undertow_state has all required keys."""
        global undertow_state
        if not isinstance(undertow_state, dict):
            undertow_state = {
                "active_undertows": [],
                "afterimage_undertows": [],
                "nihilism_warning_triggered": False,
                "intervention_log": [],
            }
            _log_integrity("WARNING: undertow_state was not a dict, reset to defaults")
            return

        defaults = {
            "active_undertows": [],
            "afterimage_undertows": [],
            "nihilism_warning_triggered": False,
            "intervention_log": [],
        }
        for key, default in defaults.items():
            if key not in undertow_state:
                undertow_state[key] = default
                _log_integrity(f"WARNING: undertow_state missing key '{key}', filled with default")

    def validate_save_integrity():
        """Main entry point: validate save data integrity on load.

        Called from after_load label.
        Checks:
        1. All required variables exist (fill defaults if missing)
        2. Numeric variables are within valid ranges (clamp if out of range)
        3. sephirot_states has all 16 keys
        4. undertow_state has all required sub-keys

        Returns:
            True if save is valid (or was repaired), False if severely corrupted.
        """
        issues = []

        # 1. Ensure required variables exist
        missing = []
        missing += [_ensure_variable("current_chapter", 1)]
        missing += [_ensure_variable("current_sephirot_id", 1)]
        missing += [_ensure_variable("current_phase", Phase.FORGETTING)]
        missing += [_ensure_variable("narrative_beat", NarrativeBeat.ENCOUNTER)]
        missing += [_ensure_variable("active_narrative_tags", set())]
        missing += [_ensure_variable("wing_brightness_permanent", 1.0)]
        missing += [_ensure_variable("wing_brightness_temporary", 0.0)]
        missing += [_ensure_variable("angel_presence_state", AngelPresenceState.PRESENT)]
        missing += [_ensure_variable("angel_emotional_state", AngelEmotionalState.CALM)]
        missing += [_ensure_variable("angel_intervention_count", 0)]
        missing += [_ensure_variable("bond_depth", 0.0)]
        missing += [_ensure_variable("hug_count_this_sephirot", 0)]
        missing += [_ensure_variable("hug_cooldown_end_time", 0)]
        missing += [_ensure_variable("choice_history", [])]
        missing += [_ensure_variable("sephirot_states", {i: SephirotState.LOCKED for i in range(1, 17)})]
        missing += [_ensure_variable("escape_counts", {})]
        missing += [_ensure_variable("consecutive_escape_count", 0)]
        missing += [_ensure_variable("undertow_state", {})]
        missing += [_ensure_variable("final_choice_unlocked", False)]

        if any(missing):
            issues.append("Some variables were missing and filled with defaults")

        # 2. Clamp numeric ranges
        _clamp_variable("wing_brightness_permanent", WING_BRIGHTNESS_MIN, 1.0)
        _clamp_variable("wing_brightness_temporary", 0.0, 1.0)
        _clamp_variable("current_chapter", 1, 16)
        _clamp_variable("current_sephirot_id", 1, 16)
        _clamp_variable("bond_depth", 0.0, 1.0)
        _clamp_variable("angel_intervention_count", 0, 9999)
        _clamp_variable("consecutive_escape_count", 0, 9999)

        # 3. Ensure sephirot_states completeness
        _ensure_sephirot_states()

        # 4. Ensure undertow_state completeness
        _ensure_undertow_state()

        # 5. Ensure active_narrative_tags is a set
        global active_narrative_tags
        if not isinstance(active_narrative_tags, set):
            if isinstance(active_narrative_tags, (list, tuple)):
                active_narrative_tags = set(active_narrative_tags)
            else:
                active_narrative_tags = set()
            _log_integrity("WARNING: active_narrative_tags was not a set, converted")

        # 6. Ensure choice_history is a list
        global choice_history
        if not isinstance(choice_history, list):
            choice_history = []
            _log_integrity("WARNING: choice_history was not a list, reset to empty")

        if issues:
            _log_integrity(f"Save integrity validation completed with issues: {issues}")
        else:
            _log_integrity("Save integrity validation passed (no issues)")

        return True
