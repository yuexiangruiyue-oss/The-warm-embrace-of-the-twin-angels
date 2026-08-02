"""tests/constants.py -- Test constants mirroring game/scripts/systems/constants.rpy

The Embrace of the Twin Angels
Story: Task #5 (Test Framework)

These constants are replicated from constants.rpy for testing outside Ren'Py runtime.
When constants.rpy changes, this file MUST be updated to match.
"""

# ── Phase ──
class Phase:
    FORGETTING = "forgetting"
    TRIAL_EARLY = "trial_early"
    TRIAL_LATE = "trial_late"
    TRUTH = "truth"


# ── Sephirot State ──
class SephirotState:
    LOCKED = "LOCKED"
    ACTIVE = "ACTIVE"
    COMPLETED_FULL = "COMPLETED_FULL"
    COMPLETED_HALF = "COMPLETED_HALF"


# ── Confrontation Tag ──
class ConfrontationTag:
    ENGAGE = "ENGAGE"
    ESCAPE = "ESCAPE"
    NEUTRAL = "NEUTRAL"


# ── Undertow Code ──
class UndertowCode:
    SHAME_LOOP = "SHAME_LOOP"
    POSS_DENY = "POSS_DENY"
    PAIN_AMP = "PAIN_AMP"
    HOPE_ERASE = "HOPE_ERASE"
    EXIST_DENY = "EXIST_DENY"
    NIHILISM = "NIHILISM"
    RAGE_INC = "RAGE_INC"
    HARM_GUIDE = "HARM_GUIDE"


# ── Narrative Beat ──
class NarrativeBeat:
    ENCOUNTER = "ENCOUNTER"
    STRUGGLE = "STRUGGLE"
    COMFORT = "COMFORT"
    CHOICE = "CHOICE"
    TRANSFORM = "TRANSFORM"


# ── Numeric Constants ──
WING_BRIGHTNESS_MIN = 0.05
WING_BRIGHTNESS_MAX = 1.0
NIHILISM_THRESHOLD = 0.7
BASE_COST = 0.02
ESCAPE_THRESHOLD = 3

# ── Phase Multiplier ──
PHASE_MULTIPLIER = {
    Phase.FORGETTING: 0.0,
    Phase.TRIAL_EARLY: 1.0,
    Phase.TRIAL_LATE: 1.5,
    Phase.TRUTH: 2.5,
}

# ── Intensity Multiplier ──
INTENSITY_MULTIPLIER = {
    "low": 0.5,
    "mid": 1.0,
    "high": 1.5,
}

# ── Wing Stage Baseline ──
WING_STAGE_BASELINE = {
    1: 1.0,
    2: 0.85,
    3: 0.65,
    4: 0.35,
    5: 0.15,
}

# ── Undertow Multiplier ──
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

# ── Chapter → Phase mapping ──
CHAPTER_PHASE_MAP = {
    1: Phase.FORGETTING,
    2: Phase.FORGETTING,
    3: Phase.FORGETTING,
    4: Phase.TRIAL_EARLY,
    5: Phase.TRIAL_EARLY,
    6: Phase.TRIAL_EARLY,
    7: Phase.TRIAL_EARLY,
    8: Phase.TRIAL_EARLY,
    9: Phase.TRIAL_LATE,
    10: Phase.TRIAL_LATE,
    11: Phase.TRIAL_LATE,
    12: Phase.TRIAL_LATE,
    13: Phase.TRIAL_LATE,
    14: Phase.TRUTH,
    15: Phase.TRUTH,
    16: Phase.TRUTH,
}

# ── Chapter → Wing Stage mapping ──
CHAPTER_WING_STAGE_MAP = {
    1: 1, 2: 1, 3: 1,
    4: 2, 5: 2, 6: 2, 7: 2, 8: 2,
    9: 3, 10: 3, 11: 3, 12: 3, 13: 3,
    14: 4, 15: 4,
    16: 5,
}

# ── Chapter Labels ──
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

# ── Beat Order ──
BEAT_ORDER = [
    NarrativeBeat.ENCOUNTER,
    NarrativeBeat.STRUGGLE,
    NarrativeBeat.COMFORT,
    NarrativeBeat.CHOICE,
    NarrativeBeat.TRANSFORM,
]
