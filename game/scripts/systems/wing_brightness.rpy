# game/scripts/systems/wing_brightness.rpy -- Wing Brightness Dual-Layer Model
# The Embrace of the Twin Angels
# Story: E1.2
# ADR-004: Dual-layer model (permanent + temporary -> displayed)

init python:

    class WingBrightnessModel:
        """[ADR-004] Wing Brightness Dual-Layer Model

        permanent: stage baseline init -> C5 cost permanent deduction -> stage switch reset
        temporary: high-intensity undertow instant effect -> scene end recovery
        displayed: max(dynamic_floor, permanent - temporary)
        """

        @staticmethod
        def get_displayed():
            """Return current displayed brightness."""
            dynamic_floor = max(
                WING_BRIGHTNESS_MIN,
                WING_STAGE_BASELINE.get(WingBrightnessModel.get_stage(), 0.05) * 0.15
            )
            return max(dynamic_floor, wing_brightness_permanent - wing_brightness_temporary)

        @staticmethod
        def get_stage():
            """Return wing visual stage (1-5) based on permanent brightness."""
            b = wing_brightness_permanent
            if b >= 0.8:
                return 1
            elif b >= 0.6:
                return 2
            elif b >= 0.4:
                return 3
            elif b >= 0.2:
                return 4
            else:
                return 5

        @staticmethod
        def apply_permanent_dim(amount):
            """Permanent deduction (called by C5).

            Clamps to dynamic floor: max(WING_BRIGHTNESS_MIN, stage_baseline * 0.15).
            """
            global wing_brightness_permanent
            stage = WingBrightnessModel.get_stage()
            floor = max(
                WING_BRIGHTNESS_MIN,
                WING_STAGE_BASELINE.get(stage, 0.05) * 0.15
            )
            wing_brightness_permanent = max(
                floor,
                wing_brightness_permanent - amount
            )

        @staticmethod
        def apply_temporary_dim(amount):
            """Temporary dimming (high-intensity undertow instant effect).

            Temporary dimming cannot make displayed brightness go below WING_BRIGHTNESS_MIN.
            """
            global wing_brightness_temporary
            wing_brightness_temporary += amount
            # Clamp: temporary cannot exceed (permanent - MIN)
            wing_brightness_temporary = min(
                wing_brightness_permanent - WING_BRIGHTNESS_MIN,
                wing_brightness_temporary
            )
            wing_brightness_temporary = max(0.0, wing_brightness_temporary)

        @staticmethod
        def clear_temporary_dim():
            """Clear temporary dimming (scene end)."""
            global wing_brightness_temporary
            wing_brightness_temporary = 0.0

        @staticmethod
        def set_stage_baseline(stage):
            """Set stage baseline (called on chapter/phase switch)."""
            global wing_brightness_permanent, wing_brightness_temporary
            wing_brightness_permanent = WING_STAGE_BASELINE.get(stage, 1.0)
            wing_brightness_temporary = 0.0

        @staticmethod
        def reset_for_ch16():
            """Ch16 reset: restore to 1.0 (narrative reset point)."""
            global wing_brightness_permanent, wing_brightness_temporary
            wing_brightness_permanent = 1.0
            wing_brightness_temporary = 0.0

        @staticmethod
        def get_wing_stage_for_chapter(chapter):
            """Return wing stage for a given chapter number."""
            return CHAPTER_WING_STAGE_MAP.get(chapter, 1)

        @staticmethod
        def on_sephirot_enter(chapter):
            """Called when entering a new chapter/sephirot.

            Sets the permanent brightness to the stage baseline for the chapter.
            """
            stage = WingBrightnessModel.get_wing_stage_for_chapter(chapter)
            WingBrightnessModel.set_stage_baseline(stage)
