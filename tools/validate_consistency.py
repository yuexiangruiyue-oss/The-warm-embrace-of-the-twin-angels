"""tools/validate_consistency.py -- Cross-file Consistency Validation

The Embrace of the Twin Angels
Story: E0.3

Validates cross-file consistency:
- Sephirot data chapters match expected phase mapping
- Undertow codes in sephirot data exist in undertow_definitions.json
- Choice data sephirot_ids match sephirot data
- All 8 undertow types defined in undertow_definitions.json

Exit code 0 = all consistent, 1 = inconsistencies found.
"""

import json
import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "game" / "data"

# Expected phase mapping
CHAPTER_PHASE = {
    1: "FORGETTING", 2: "FORGETTING", 3: "FORGETTING",
    4: "TRIAL_EARLY", 5: "TRIAL_EARLY", 6: "TRIAL_EARLY",
    7: "TRIAL_EARLY", 8: "TRIAL_EARLY",
    9: "TRIAL_LATE", 10: "TRIAL_LATE", 11: "TRIAL_LATE",
    12: "TRIAL_LATE", 13: "TRIAL_LATE",
    14: "TRUTH", 15: "TRUTH", 16: "TRUTH",
}

EXPECTED_UNDERTOWS = {
    "SHAME_LOOP", "POSS_DENY", "PAIN_AMP", "HOPE_ERASE",
    "EXIST_DENY", "NIHILISM", "RAGE_INC", "HARM_GUIDE"
}

errors = []


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_undertow_completeness():
    """Check that all 8 undertow types are defined."""
    filepath = DATA_DIR / "protection" / "undertow_definitions.json"
    if not filepath.exists():
        errors.append(f"Missing undertow_definitions.json: {filepath}")
        return

    data = load_json(filepath)
    undertows = data.get("undertows", data) if isinstance(data, dict) else data
    if not isinstance(undertows, list):
        errors.append("undertow_definitions.json: 'undertows' should be a list")
        return

    defined_codes = set()
    for uw in undertows:
        code = uw.get("code")
        if code:
            defined_codes.add(code)

    missing = EXPECTED_UNDERTOWS - defined_codes
    if missing:
        errors.append(f"undertow_definitions.json: Missing undertow types: {missing}")

    extra = defined_codes - EXPECTED_UNDERTOWS
    if extra:
        errors.append(f"undertow_definitions.json: Unexpected undertow types: {extra}")

    # Validate each undertow has 3 intensity levels
    for uw in undertows:
        code = uw.get("code", "UNKNOWN")
        levels = uw.get("intensity_levels", {})
        for level in ["low", "mid", "high"]:
            if level not in levels:
                errors.append(f"undertow_definitions.json: {code} missing intensity level '{level}'")
            else:
                level_data = levels[level]
                for field in ["range", "visual", "angel_intervention_type", "angel_lines"]:
                    if field not in level_data:
                        errors.append(
                            f"undertow_definitions.json: {code}.{level} missing field '{field}'"
                        )


def validate_sephirot_phases():
    """Check that sephirot data phases match expected chapter-phase mapping."""
    sephirot_dir = DATA_DIR / "sephirot"
    if not sephirot_dir.exists():
        errors.append(f"Sephirot directory not found: {sephirot_dir}")
        return

    for filepath in sorted(sephirot_dir.iterdir()):
        if filepath.suffix != ".json" or filepath.name.startswith("_"):
            continue
        data = load_json(filepath)
        chapter = data.get("chapter")
        phase = data.get("phase")
        if chapter is not None and phase is not None:
            expected_phase = CHAPTER_PHASE.get(chapter)
            if expected_phase and phase != expected_phase:
                errors.append(
                    f"{filepath.name}: chapter {chapter} should have phase "
                    f"'{expected_phase}', got '{phase}'"
                )


def validate_sephirot_undertow_references():
    """Check that undertow codes in sephirot data are valid."""
    sephirot_dir = DATA_DIR / "sephirot"
    if not sephirot_dir.exists():
        return

    for filepath in sorted(sephirot_dir.iterdir()):
        if filepath.suffix != ".json" or filepath.name.startswith("_"):
            continue
        data = load_json(filepath)
        primary = data.get("primary_undertow")
        if primary and primary not in EXPECTED_UNDERTOWS:
            errors.append(f"{filepath.name}: Invalid primary_undertow '{primary}'")

        composites = data.get("composite_undertows", [])
        for comp in composites:
            if comp not in EXPECTED_UNDERTOWS:
                errors.append(f"{filepath.name}: Invalid composite_undertow '{comp}'")


def validate_choice_sephirot_refs():
    """Check that choice data sephirot_ids reference valid sephirot data."""
    choices_dir = DATA_DIR / "choices"
    if not choices_dir.exists():
        return

    # Collect valid sephirot IDs from sephirot data
    sephirot_ids = set()
    sephirot_dir = DATA_DIR / "sephirot"
    if sephirot_dir.exists():
        for filepath in sephirot_dir.iterdir():
            if filepath.suffix == ".json" and not filepath.name.startswith("_"):
                data = load_json(filepath)
                sid = data.get("sephirot_id")
                if sid is not None:
                    sephirot_ids.add(sid)

    for chapter_dir in sorted(choices_dir.iterdir()):
        if not chapter_dir.is_dir():
            continue
        for filepath in sorted(chapter_dir.iterdir()):
            if filepath.suffix != ".json" or filepath.name.startswith("_"):
                continue
            data = load_json(filepath)
            sid = data.get("sephirot_id")
            if sid is not None and sephirot_ids and sid not in sephirot_ids:
                errors.append(
                    f"{filepath.name}: sephirot_id {sid} not found in sephirot data"
                )


def main():
    print("=" * 60)
    print("Cross-file Consistency Validation")
    print("=" * 60)

    validate_undertow_completeness()
    validate_sephirot_phases()
    validate_sephirot_undertow_references()
    validate_choice_sephirot_refs()

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  ERROR: {e}")
        print("\nConsistency validation FAILED.")
        sys.exit(1)
    else:
        print("\nAll cross-file consistency checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
