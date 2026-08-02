"""tools/validate_data.py -- JSON Data Validation Script

The Embrace of the Twin Angels
Story: E0.3

Validates all JSON data files against expected schema structures.
Exit code 0 = all valid, 1 = errors found.
"""

import json
import os
import sys
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "game" / "data"

# Expected schemas for each data type
SCHEMAS = {
    "sephirot": {
        "required_fields": [
            "sephirot_id", "name", "pinyin", "chapter", "phase",
            "primary_undertow", "composite_undertows", "base_intensity",
            "intervention_type", "wing_cost", "special_rules"
        ],
        "field_types": {
            "sephirot_id": int,
            "name": str,
            "pinyin": str,
            "chapter": int,
            "phase": str,
            "primary_undertow": str,
            "composite_undertows": list,
            "base_intensity": int,
            "intervention_type": str,
            "wing_cost": (int, float),
            "special_rules": list,
        }
    },
    "choices": {
        "required_fields": [
            "choice_id", "sephirot_id", "prompt_text", "options"
        ],
        "field_types": {
            "choice_id": str,
            "sephirot_id": int,
            "prompt_text": str,
            "options": list,
        }
    },
    "angel": {
        "required_fields": ["dialogue_entries"],
        "field_types": {
            "dialogue_entries": list,
        }
    },
    "protection": {
        "required_fields": ["code", "name", "description", "intensity_levels"],
        "field_types": {
            "code": str,
            "name": str,
            "description": str,
            "intensity_levels": dict,
        }
    },
    "endings": {
        "required_fields": ["ending_code", "name", "conditions"],
        "field_types": {
            "ending_code": str,
            "name": str,
            "conditions": dict,
        }
    },
}

# Valid enum values for cross-validation
VALID_PHASES = {"FORGETTING", "TRIAL_EARLY", "TRIAL_LATE", "TRUTH", "forgetting", "trial_early", "trial_late", "truth"}
VALID_UNDERTOWS = {
    "SHAME_LOOP", "POSS_DENY", "PAIN_AMP", "HOPE_ERASE",
    "EXIST_DENY", "NIHILISM", "RAGE_INC", "HARM_GUIDE"
}
VALID_INTERVENTIONS = {"gentle", "active", "forceful", "urgent"}
VALID_CONFRONTATION_TAGS = {"ENGAGE", "ESCAPE", "NEUTRAL"}

errors = []
warnings = []


def validate_json_file(filepath, schema_name):
    """Validate a single JSON file against its schema."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"{filepath}: JSON decode error: {e}")
        return
    except Exception as e:
        errors.append(f"{filepath}: Error reading file: {e}")
        return

    schema = SCHEMAS.get(schema_name)
    if not schema:
        return

    # Check required fields
    for field in schema["required_fields"]:
        if field not in data:
            errors.append(f"{filepath}: Missing required field '{field}'")

    # Check field types
    for field, expected_type in schema["field_types"].items():
        if field in data:
            if not isinstance(data[field], expected_type):
                errors.append(
                    f"{filepath}: Field '{field}' has wrong type. "
                    f"Expected {expected_type}, got {type(data[field]).__name__}"
                )

    # Cross-validation for sephirot data
    if schema_name == "sephirot":
        if "phase" in data and data["phase"] not in VALID_PHASES:
            errors.append(f"{filepath}: Invalid phase '{data['phase']}'")
        if "primary_undertow" in data and data["primary_undertow"] not in VALID_UNDERTOWS:
            errors.append(f"{filepath}: Invalid undertow '{data['primary_undertow']}'")
        if "intervention_type" in data and data["intervention_type"] not in VALID_INTERVENTIONS:
            errors.append(f"{filepath}: Invalid intervention type '{data['intervention_type']}'")
        if "sephirot_id" in data:
            sid = data["sephirot_id"]
            if not (0 <= sid <= 16):
                errors.append(f"{filepath}: sephirot_id {sid} out of range (0-16)")
        if "chapter" in data:
            ch = data["chapter"]
            if not (0 <= ch <= 16):
                errors.append(f"{filepath}: chapter {ch} out of range (0-16)")

    # Cross-validation for choice data
    if schema_name == "choices" and "options" in data:
        for opt in data["options"]:
            if "confrontation_tag" in opt and opt["confrontation_tag"] is not None:
                if opt["confrontation_tag"] not in VALID_CONFRONTATION_TAGS:
                    errors.append(
                        f"{filepath}: Invalid confrontation_tag '{opt['confrontation_tag']}'"
                    )
            # Check confrontation_tag / progress_value consistency
            if "confrontation_tag" in opt and "progress_value" in opt:
                tag = opt["confrontation_tag"]
                pv = opt["progress_value"]
                if tag == "ENGAGE" and pv != 1.0:
                    warnings.append(
                        f"{filepath}: ENGAGE tag with progress_value {pv} (expected 1.0)"
                    )
                elif tag == "ESCAPE" and pv != 0.3:
                    warnings.append(
                        f"{filepath}: ESCAPE tag with progress_value {pv} (expected 0.3)"
                    )
                elif tag == "NEUTRAL" and pv != 0.0:
                    warnings.append(
                        f"{filepath}: NEUTRAL tag with progress_value {pv} (expected 0.0)"
                    )

    # Cross-validation for protection data
    if schema_name == "protection":
        if "code" in data and data["code"] not in VALID_UNDERTOWS and data["code"] != "TEMPLATE":
            errors.append(f"{filepath}: Invalid undertow code '{data['code']}'")
        if "intensity_levels" in data:
            for level_name in ["low", "mid", "high"]:
                if level_name not in data["intensity_levels"]:
                    errors.append(f"{filepath}: Missing intensity level '{level_name}'")


def validate_directory(dirpath, schema_name, skip_templates=True):
    """Validate all JSON files in a directory.

    Args:
        dirpath: Directory to validate.
        schema_name: Schema name for validation.
        skip_templates: If True, skip files starting with '_'.
    """
    if not dirpath.exists():
        warnings.append(f"Directory not found: {dirpath}")
        return

    for filepath in sorted(dirpath.iterdir()):
        if filepath.suffix == ".json":
            if skip_templates and filepath.name.startswith("_"):
                continue
            validate_json_file(filepath, schema_name)


def validate_choices_directory():
    """Validate choice JSON files in chapter subdirectories."""
    choices_dir = DATA_DIR / "choices"
    if not choices_dir.exists():
        warnings.append(f"Choices directory not found: {choices_dir}")
        return

    for chapter_dir in sorted(choices_dir.iterdir()):
        if chapter_dir.is_dir():
            for filepath in sorted(chapter_dir.iterdir()):
                if filepath.suffix == ".json":
                    validate_json_file(filepath, "choices")


def validate_undertow_definitions(filepath):
    """Validate the undertow_definitions.json file specially.

    This file has a {"undertows": [...]} structure, where each undertow
    has the protection schema fields.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"{filepath}: JSON decode error: {e}")
        return
    except Exception as e:
        errors.append(f"{filepath}: Error reading file: {e}")
        return

    undertows = data.get("undertows", data) if isinstance(data, dict) else data
    if not isinstance(undertows, list):
        errors.append(f"{filepath}: 'undertows' should be a list")
        return

    for i, uw in enumerate(undertows):
        # Validate each undertow against the protection schema
        for field in ["code", "name", "description", "intensity_levels"]:
            if field not in uw:
                errors.append(f"{filepath}: undertow[{i}] missing field '{field}'")

        if "code" in uw and uw["code"] not in VALID_UNDERTOWS:
            errors.append(f"{filepath}: undertow[{i}] invalid code '{uw['code']}'")

        if "intensity_levels" in uw:
            for level_name in ["low", "mid", "high"]:
                if level_name not in uw["intensity_levels"]:
                    errors.append(
                        f"{filepath}: undertow[{i}] missing intensity level '{level_name}'"
                    )


def validate_protection_directory(dirpath):
    """Validate protection JSON files, handling undertow_definitions specially."""
    if not dirpath.exists():
        warnings.append(f"Directory not found: {dirpath}")
        return

    for filepath in sorted(dirpath.iterdir()):
        if filepath.suffix != ".json":
            continue
        if filepath.name.startswith("_"):
            continue  # Skip templates
        if filepath.name == "undertow_definitions.json":
            validate_undertow_definitions(filepath)
        else:
            validate_json_file(filepath, "protection")


def main():
    print("=" * 60)
    print("JSON Data Validation")
    print("=" * 60)

    # Validate each data type
    validate_directory(DATA_DIR / "sephirot", "sephirot")
    validate_choices_directory()
    validate_directory(DATA_DIR / "angel", "angel")
    validate_protection_directory(DATA_DIR / "protection")
    validate_directory(DATA_DIR / "endings", "endings")

    # Report
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  WARNING: {w}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  ERROR: {e}")
        print("\nValidation FAILED.")
        sys.exit(1)
    else:
        print(f"\nAll JSON data files validated successfully.")
        if warnings:
            print(f"({len(warnings)} warnings)")
        sys.exit(0)


if __name__ == "__main__":
    main()
