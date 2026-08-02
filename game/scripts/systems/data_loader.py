"""game/scripts/systems/data_loader.py -- JSON Data Loader

The Embrace of the Twin Angels
Story: E0.3

Provides JSON loading utilities for both Ren'Py runtime and test environment.
Compatible with Ren'Py 8.3.x runtime and standard Python 3.11+ for tests.
"""

import json
import os
from pathlib import Path


class DataLoadError(Exception):
    """Data loading error with path context."""

    def __init__(self, path, message):
        self.path = path
        self.message = message
        super().__init__(f"DataLoadError [{path}]: {message}")


class InvalidChapterError(Exception):
    """Raised when an invalid chapter number is requested."""

    pass


def load_json(path):
    """Load a single JSON file and return as dict.

    Args:
        path: File path (string or Path) to the JSON file.

    Returns:
        Parsed JSON content as dict.

    Raises:
        DataLoadError: If file not found or JSON decode error.
    """
    path = str(path)
    if not os.path.exists(path):
        raise DataLoadError(path, "File not found")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise DataLoadError(path, f"JSON decode error: {e}")
    except Exception as e:
        raise DataLoadError(path, f"Unexpected error: {e}")


def load_all(directory):
    """Load all JSON files in a directory.

    Skips files starting with '_' (template files).

    Args:
        directory: Directory path (string or Path).

    Returns:
        Dict mapping filename (without extension) to parsed JSON dict.

    Raises:
        DataLoadError: If directory not found.
    """
    directory = str(directory)
    result = {}
    if not os.path.isdir(directory):
        raise DataLoadError(directory, "Directory not found")
    for filename in os.listdir(directory):
        if filename.endswith(".json") and not filename.startswith("_"):
            filepath = os.path.join(directory, filename)
            key = filename.replace(".json", "")
            result[key] = load_json(filepath)
    return result


def load_all_including_templates(directory):
    """Load all JSON files in a directory, including templates.

    Args:
        directory: Directory path (string or Path).

    Returns:
        Dict mapping filename (without extension) to parsed JSON dict.

    Raises:
        DataLoadError: If directory not found.
    """
    directory = str(directory)
    result = {}
    if not os.path.isdir(directory):
        raise DataLoadError(directory, "Directory not found")
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            key = filename.replace(".json", "")
            result[key] = load_json(filepath)
    return result


def get_game_data_path():
    """Get the game/data/ directory path.

    In Ren'Py runtime: uses config.gamedir.
    In test environment: derives path from this file's location.

    Returns:
        String path to the game/data/ directory.
    """
    try:
        import renpy  # noqa: F401

        return os.path.join(renpy.config.gamedir, "data")
    except ImportError:
        # Test environment: game/scripts/systems/data_loader.py -> game/data
        this_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up from systems/ -> scripts/ -> game/ -> then into data/
        return os.path.normpath(os.path.join(this_dir, "..", "..", "data"))


def get_data_subpath(subdir):
    """Get a subdirectory path under game/data/.

    Args:
        subdir: Subdirectory name (e.g. 'sephirot', 'choices', 'angel').

    Returns:
        String path to the subdirectory.
    """
    return os.path.join(get_game_data_path(), subdir)


def load_sephirot_data(sephirot_id):
    """Load a specific sephirot's JSON data.

    Args:
        sephirot_id: Sephirot ID (1-16).

    Returns:
        Parsed sephirot JSON data as dict.

    Raises:
        DataLoadError: If file not found or invalid.
        InvalidChapterError: If sephirot_id is out of range.
    """
    if not (1 <= sephirot_id <= 16):
        raise InvalidChapterError(f"Invalid sephirot_id: {sephirot_id}")
    filename = f"sephirot_{sephirot_id:02d}.json"
    filepath = os.path.join(get_data_subpath("sephirot"), filename)
    return load_json(filepath)


def load_choice_node(chapter, choice_id):
    """Load a choice node JSON by chapter and choice_id.

    Args:
        chapter: Chapter number (1-16).
        choice_id: Choice node identifier.

    Returns:
        Parsed choice node JSON data as dict.

    Raises:
        DataLoadError: If file not found.
    """
    filepath = os.path.join(
        get_data_subpath("choices"),
        f"ch{chapter:02d}",
        f"{choice_id}.json",
    )
    return load_json(filepath)


def load_undertow_definitions():
    """Load the undertow definitions JSON.

    Returns:
        List of undertow definition dicts.
    """
    filepath = os.path.join(get_data_subpath("protection"), "undertow_definitions.json")
    data = load_json(filepath)
    if isinstance(data, dict) and "undertows" in data:
        return data["undertows"]
    return data


def load_dialogue_pool():
    """Load the angel dialogue pool JSON.

    Returns:
        Parsed dialogue pool JSON data as dict.
    """
    filepath = os.path.join(get_data_subpath("angel"), "dialogue_pool.json")
    return load_json(filepath)


def load_ending_data(ending_code):
    """Load a specific ending's JSON data.

    Args:
        ending_code: Ending code string.

    Returns:
        Parsed ending JSON data as dict.
    """
    filepath = os.path.join(get_data_subpath("endings"), f"{ending_code}.json")
    return load_json(filepath)
