"""tests/unit/test_json_validation.py -- Unit tests for JSON data validation

The Embrace of the Twin Angels
Story: E0.3

Tests that all JSON data files are valid and consistent.
Also tests the validation scripts (validate_data.py, validate_consistency.py).
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "game" / "data"
TOOLS_DIR = PROJECT_ROOT / "tools"


class TestSephirotData:
    """Tests for sephirot JSON data."""

    def test_template_exists(self):
        """Test that sephirot template exists."""
        assert (DATA_DIR / "sephirot" / "_template.json").exists()

    def test_sephirot_01_exists(self):
        """Test that sephirot_01.json exists."""
        assert (DATA_DIR / "sephirot" / "sephirot_01.json").exists()

    def test_sephirot_01_fields(self):
        """Test sephirot_01.json has all required fields."""
        with open(DATA_DIR / "sephirot" / "sephirot_01.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        required = [
            "sephirot_id", "name", "pinyin", "chapter", "phase",
            "primary_undertow", "composite_undertows", "base_intensity",
            "intervention_type", "wing_cost", "special_rules"
        ]
        for field in required:
            assert field in data, f"Missing field: {field}"

    def test_sephirot_01_values(self):
        """Test sephirot_01.json has correct values."""
        with open(DATA_DIR / "sephirot" / "sephirot_01.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["sephirot_id"] == 1
        assert data["name"] == "王国"
        assert data["chapter"] == 1
        assert data["phase"] == "FORGETTING"
        assert data["primary_undertow"] == "EXIST_DENY"
        assert data["base_intensity"] == 2
        assert data["wing_cost"] == 0.0


class TestProtectionData:
    """Tests for protection JSON data."""

    def test_template_exists(self):
        """Test that protection template exists."""
        assert (DATA_DIR / "protection" / "_template.json").exists()

    def test_undertow_definitions_exist(self):
        """Test that undertow_definitions.json exists."""
        assert (DATA_DIR / "protection" / "undertow_definitions.json").exists()

    def test_8_undertows_defined(self):
        """Test that all 8 undertow types are defined."""
        with open(DATA_DIR / "protection" / "undertow_definitions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        undertows = data.get("undertows", data)
        assert isinstance(undertows, list)
        assert len(undertows) == 8

    def test_undertow_codes(self):
        """Test that undertow codes match expected values."""
        with open(DATA_DIR / "protection" / "undertow_definitions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        undertows = data.get("undertows", data)
        codes = {uw["code"] for uw in undertows}
        expected = {
            "SHAME_LOOP", "POSS_DENY", "PAIN_AMP", "HOPE_ERASE",
            "EXIST_DENY", "NIHILISM", "RAGE_INC", "HARM_GUIDE"
        }
        assert codes == expected

    def test_each_undertow_has_3_levels(self):
        """Test that each undertow has low, mid, high levels."""
        with open(DATA_DIR / "protection" / "undertow_definitions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        undertows = data.get("undertows", data)
        for uw in undertows:
            levels = uw.get("intensity_levels", {})
            assert "low" in levels, f"{uw['code']} missing 'low'"
            assert "mid" in levels, f"{uw['code']} missing 'mid'"
            assert "high" in levels, f"{uw['code']} missing 'high'"

    def test_harm_guide_special_rules(self):
        """Test HARM_GUIDE has urgent intervention at all levels."""
        with open(DATA_DIR / "protection" / "undertow_definitions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        undertows = data.get("undertows", data)
        harm = next(uw for uw in undertows if uw["code"] == "HARM_GUIDE")
        for level in ["low", "mid", "high"]:
            assert harm["intensity_levels"][level]["angel_intervention_type"] == "urgent"


class TestChoiceData:
    """Tests for choice JSON data."""

    def test_template_exists(self):
        """Test that choice template exists."""
        assert (DATA_DIR / "choices" / "ch01" / "_template.json").exists()

    def test_ch01_choice_exists(self):
        """Test that ch01 choice data exists."""
        assert (DATA_DIR / "choices" / "ch01" / "ch01_s1_c1.json").exists()

    def test_ch01_choice_fields(self):
        """Test ch01 choice data has required fields."""
        with open(DATA_DIR / "choices" / "ch01" / "ch01_s1_c1.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "choice_id" in data
        assert "sephirot_id" in data
        assert "prompt_text" in data
        assert "options" in data
        assert len(data["options"]) >= 2

    def test_ch01_choice_engage_escape(self):
        """Test ch01 choice has ENGAGE and ESCAPE options."""
        with open(DATA_DIR / "choices" / "ch01" / "ch01_s1_c1.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        tags = {opt["confrontation_tag"] for opt in data["options"]}
        assert "ENGAGE" in tags
        assert "ESCAPE" in tags


class TestAngelData:
    """Tests for angel JSON data."""

    def test_template_exists(self):
        """Test that angel template exists."""
        assert (DATA_DIR / "angel" / "_template.json").exists()

    def test_dialogue_pool_exists(self):
        """Test that dialogue_pool.json exists."""
        assert (DATA_DIR / "angel" / "dialogue_pool.json").exists()

    def test_dialogue_pool_has_entries(self):
        """Test dialogue pool has entries."""
        with open(DATA_DIR / "angel" / "dialogue_pool.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "dialogue_entries" in data
        assert len(data["dialogue_entries"]) >= 3


class TestEndingsData:
    """Tests for endings JSON data."""

    def test_template_exists(self):
        """Test that endings template exists."""
        assert (DATA_DIR / "endings" / "_template.json").exists()


class TestValidationScripts:
    """Tests for the validation scripts."""

    def test_validate_data_passes(self):
        """Test that validate_data.py passes with no errors."""
        result = subprocess.run(
            [sys.executable, str(TOOLS_DIR / "validate_data.py")],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )
        assert result.returncode == 0, f"Validation failed:\n{result.stderr}\n{result.stdout}"

    def test_validate_consistency_passes(self):
        """Test that validate_consistency.py passes with no errors."""
        result = subprocess.run(
            [sys.executable, str(TOOLS_DIR / "validate_consistency.py")],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )
        assert result.returncode == 0, f"Consistency check failed:\n{result.stderr}\n{result.stdout}"
