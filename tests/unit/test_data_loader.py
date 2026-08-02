"""tests/unit/test_data_loader.py -- Unit tests for data_loader.py

The Embrace of the Twin Angels
Story: E0.3
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add systems directory to path
SYSTEMS_DIR = Path(__file__).parent.parent.parent / "game" / "scripts" / "systems"
sys.path.insert(0, str(SYSTEMS_DIR))

from data_loader import (
    DataLoadError,
    InvalidChapterError,
    load_json,
    load_all,
    load_all_including_templates,
    get_game_data_path,
    get_data_subpath,
    load_sephirot_data,
    load_choice_node,
    load_undertow_definitions,
    load_dialogue_pool,
)


class TestLoadJson:
    """Tests for load_json function."""

    def test_load_valid_json(self, tmp_path):
        """Test loading a valid JSON file."""
        test_file = tmp_path / "test.json"
        test_file.write_text('{"key": "value"}', encoding="utf-8")
        result = load_json(str(test_file))
        assert result == {"key": "value"}

    def test_load_nonexistent_file(self):
        """Test that loading a nonexistent file raises DataLoadError."""
        with pytest.raises(DataLoadError) as exc_info:
            load_json("/nonexistent/path/file.json")
        assert "File not found" in str(exc_info.value)

    def test_load_invalid_json(self, tmp_path):
        """Test that loading invalid JSON raises DataLoadError."""
        test_file = tmp_path / "invalid.json"
        test_file.write_text("{invalid json}", encoding="utf-8")
        with pytest.raises(DataLoadError) as exc_info:
            load_json(str(test_file))
        assert "JSON decode error" in str(exc_info.value)

    def test_load_json_with_unicode(self, tmp_path):
        """Test loading JSON with Unicode content."""
        test_file = tmp_path / "unicode.json"
        test_file.write_text('{"name": "王国"}', encoding="utf-8")
        result = load_json(str(test_file))
        assert result["name"] == "王国"


class TestLoadAll:
    """Tests for load_all function."""

    def test_load_all_skips_templates(self, tmp_path):
        """Test that load_all skips files starting with underscore."""
        (tmp_path / "_template.json").write_text('{"template": true}', encoding="utf-8")
        (tmp_path / "data1.json").write_text('{"id": 1}', encoding="utf-8")
        (tmp_path / "data2.json").write_text('{"id": 2}', encoding="utf-8")
        (tmp_path / "readme.txt").write_text("not json", encoding="utf-8")

        result = load_all(str(tmp_path))
        assert "_template" not in result
        assert "data1" in result
        assert "data2" in result
        assert len(result) == 2

    def test_load_all_nonexistent_directory(self):
        """Test that loading from nonexistent directory raises DataLoadError."""
        with pytest.raises(DataLoadError):
            load_all("/nonexistent/directory")

    def test_load_all_empty_directory(self, tmp_path):
        """Test loading from an empty directory."""
        result = load_all(str(tmp_path))
        assert result == {}

    def test_load_all_including_templates(self, tmp_path):
        """Test that load_all_including_templates includes template files."""
        (tmp_path / "_template.json").write_text('{"template": true}', encoding="utf-8")
        (tmp_path / "data1.json").write_text('{"id": 1}', encoding="utf-8")

        result = load_all_including_templates(str(tmp_path))
        assert "_template" in result
        assert "data1" in result


class TestGetGamePath:
    """Tests for path resolution functions."""

    def test_get_game_data_path_returns_string(self):
        """Test that get_game_data_path returns a string."""
        path = get_game_data_path()
        assert isinstance(path, str)
        assert "data" in path

    def test_get_data_subpath(self):
        """Test that get_data_subpath returns correct subdirectory."""
        path = get_data_subpath("sephirot")
        assert "sephirot" in path


class TestLoadSephirotData:
    """Tests for load_sephirot_data function."""

    def test_load_sephirot_01(self):
        """Test loading sephirot 1 data."""
        data = load_sephirot_data(1)
        assert data["sephirot_id"] == 1
        assert data["name"] == "王国"
        assert data["phase"] == "FORGETTING"
        assert data["primary_undertow"] == "EXIST_DENY"

    def test_load_sephirot_invalid_id(self):
        """Test that invalid sephirot_id raises InvalidChapterError."""
        with pytest.raises(InvalidChapterError):
            load_sephirot_data(0)
        with pytest.raises(InvalidChapterError):
            load_sephirot_data(17)
        with pytest.raises(InvalidChapterError):
            load_sephirot_data(-1)


class TestLoadUndertowDefinitions:
    """Tests for load_undertow_definitions function."""

    def test_load_undertow_definitions(self):
        """Test loading undertow definitions."""
        undertows = load_undertow_definitions()
        assert isinstance(undertows, list)
        assert len(undertows) == 8

    def test_all_8_undertows_present(self):
        """Test that all 8 undertow types are present."""
        undertows = load_undertow_definitions()
        codes = {uw["code"] for uw in undertows}
        expected = {
            "SHAME_LOOP", "POSS_DENY", "PAIN_AMP", "HOPE_ERASE",
            "EXIST_DENY", "NIHILISM", "RAGE_INC", "HARM_GUIDE"
        }
        assert codes == expected

    def test_undertow_has_3_intensity_levels(self):
        """Test that each undertow has low, mid, high intensity levels."""
        undertows = load_undertow_definitions()
        for uw in undertows:
            levels = uw["intensity_levels"]
            assert "low" in levels
            assert "mid" in levels
            assert "high" in levels

    def test_harm_guide_uses_urgent_all_levels(self):
        """Test that HARM_GUIDE uses urgent intervention at all levels."""
        undertows = load_undertow_definitions()
        harm_guide = next(uw for uw in undertows if uw["code"] == "HARM_GUIDE")
        for level_name in ["low", "mid", "high"]:
            assert harm_guide["intensity_levels"][level_name]["angel_intervention_type"] == "urgent"


class TestLoadDialoguePool:
    """Tests for load_dialogue_pool function."""

    def test_load_dialogue_pool(self):
        """Test loading dialogue pool."""
        pool = load_dialogue_pool()
        assert "dialogue_entries" in pool
        assert isinstance(pool["dialogue_entries"], list)
        assert len(pool["dialogue_entries"]) > 0

    def test_dialogue_entries_have_required_fields(self):
        """Test that dialogue entries have required fields."""
        pool = load_dialogue_pool()
        for entry in pool["dialogue_entries"]:
            assert "id" in entry
            assert "phase" in entry
            assert "emotional_state" in entry
            assert "text" in entry
