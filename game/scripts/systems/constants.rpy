# game/scripts/systems/constants.rpy -- Constants and Enums
# The Embrace of the Twin Angels
# Story: E0.4

init python:

    # -- Phase enum --
    class Phase:
        FORGETTING = "forgetting"       # Ch 1-3
        TRIAL_EARLY = "trial_early"     # Ch 4-8
        TRIAL_LATE = "trial_late"       # Ch 9-13
        TRUTH = "truth"                 # Ch 14-16

    # -- SephirotState enum --
    class SephirotState:
        LOCKED = "LOCKED"
        ACTIVE = "ACTIVE"
        COMPLETED_FULL = "COMPLETED_FULL"
        COMPLETED_HALF = "COMPLETED_HALF"

    # -- ConfrontationTag enum --
    class ConfrontationTag:
        ENGAGE = "ENGAGE"
        ESCAPE = "ESCAPE"
        NEUTRAL = "NEUTRAL"

    # -- UndertowCode enum (8 undertow types) --
    class UndertowCode:
        SHAME_LOOP = "SHAME_LOOP"
        POSS_DENY = "POSS_DENY"
        PAIN_AMP = "PAIN_AMP"
        HOPE_ERASE = "HOPE_ERASE"
        EXIST_DENY = "EXIST_DENY"
        NIHILISM = "NIHILISM"
        RAGE_INC = "RAGE_INC"
        HARM_GUIDE = "HARM_GUIDE"

    # -- AngelEmotionalState enum --
    class AngelEmotionalState:
        CALM = "calm"
        ACHING = "aching"
        RESOLUTE = "resolute"
        SORROWFUL = "sorrowful"
        TENDER = "tender"

    # -- AngelPresenceState enum --
    class AngelPresenceState:
        PRESENT = "PRESENT"
        CONCEALED = "CONCEALED"
        INTERVENING = "INTERVENING"
        ABSENT = "ABSENT"
        ETERNAL = "ETERNAL"

    # -- InterventionType enum --
    class InterventionType:
        GENTLE = "gentle"
        ACTIVE = "active"
        FORCEFUL = "forceful"
        URGENT = "urgent"

    # -- NarrativeBeat enum (five-beat) --
    class NarrativeBeat:
        ENCOUNTER = "ENCOUNTER"
        STRUGGLE = "STRUGGLE"
        COMFORT = "COMFORT"
        CHOICE = "CHOICE"
        TRANSFORM = "TRANSFORM"

    # -- Numeric constants --
    WING_BRIGHTNESS_MIN = 0.05
    NIHILISM_THRESHOLD = 0.7
    BASE_COST = 0.02

    # -- Phase cost multiplier table --
    PHASE_MULTIPLIER = {
        Phase.FORGETTING: 0.0,
        Phase.TRIAL_EARLY: 1.0,
        Phase.TRIAL_LATE: 1.5,
        Phase.TRUTH: 2.5,
    }

    # -- Intensity multiplier table --
    INTENSITY_MULTIPLIER = {
        "low": 0.5,
        "mid": 1.0,
        "high": 1.5,
    }

    # -- Wing stage baseline table --
    WING_STAGE_BASELINE = {
        1: 1.0,
        2: 0.85,
        3: 0.65,
        4: 0.35,
        5: 0.15,
    }

    # -- Intervention delay table (seconds) --
    INTERVENTION_DELAY = {
        "low": 3,
        "mid": 5,
        "high": 8,
    }

    # -- Recovery time table (seconds) --
    RECOVERY_TIME = {
        "low": 3,
        "mid": 5,
        "high": 8,
    }

    # -- Escape count threshold --
    ESCAPE_THRESHOLD = 3  # 3rd ESCAPE triggers angel proxy confrontation

    # -- Hug limits --
    HUG_LIMIT_PHASE_1_2 = 3
    HUG_COOLDOWN = 30  # Click angel cooldown (seconds)

    # -- Undertow multiplier table (per-undertow cost modifier) --
    UNDERTOW_MULTIPLIER = {
        UndertowCode.SHAME_LOOP: 1.0,
        UndertowCode.POSS_DENY: 1.0,
        UndertowCode.PAIN_AMP: 1.0,
        UndertowCode.HOPE_ERASE: 1.0,
        UndertowCode.EXIST_DENY: 1.2,
        UndertowCode.NIHILISM: 1.5,
        UndertowCode.RAGE_INC: 1.0,
        UndertowCode.HARM_GUIDE: 2.0,
    }

    # -- Chapter to phase mapping --
    CHAPTER_PHASE_MAP = {
        1: Phase.FORGETTING, 2: Phase.FORGETTING, 3: Phase.FORGETTING,
        4: Phase.TRIAL_EARLY, 5: Phase.TRIAL_EARLY, 6: Phase.TRIAL_EARLY,
        7: Phase.TRIAL_EARLY, 8: Phase.TRIAL_EARLY,
        9: Phase.TRIAL_LATE, 10: Phase.TRIAL_LATE, 11: Phase.TRIAL_LATE,
        12: Phase.TRIAL_LATE, 13: Phase.TRIAL_LATE,
        14: Phase.TRUTH, 15: Phase.TRUTH, 16: Phase.TRUTH,
    }

    # -- Chapter to wing stage mapping --
    CHAPTER_WING_STAGE_MAP = {
        1: 1, 2: 1, 3: 1,
        4: 2, 5: 2, 6: 2,
        7: 3, 8: 3, 9: 3,
        10: 4, 11: 4, 12: 4, 13: 4, 14: 4,
        15: 5, 16: 5,
    }

    # -- Chapter label naming: ch{NN}_sephirot_{NN} --
    CHAPTER_LABELS = {
        1: "ch01_sephirot_01",
        2: "ch02_sephirot_02",
        3: "ch03_sephirot_03",
        4: "ch04_sephirot_04",
        5: "ch05_sephirot_05",
        6: "ch06_sephirot_06",
        7: "ch07_sephirot_07",
        8: "ch08_sephirot_08",
        9: "ch09_sephirot_09",
        10: "ch10_sephirot_10",
        11: "ch11_sephirot_11",
        12: "ch12_sephirot_12",
        13: "ch13_sephirot_13",
        14: "ch14_sephirot_14",
        15: "ch15_sephirot_15",
        16: "ch16_sephirot_16",
    }
