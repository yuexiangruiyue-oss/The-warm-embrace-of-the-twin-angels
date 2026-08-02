"""tests/conftest.py -- pytest fixtures

The Embrace of the Twin Angels
Story: E0.6

Provides fixtures for testing system modules outside of Ren'Py runtime.
"""

import sys
import os
import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest


# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
GAME_DIR = PROJECT_ROOT / "game"
SYSTEMS_DIR = GAME_DIR / "scripts" / "systems"


# Add game/scripts/systems to Python path for imports
sys.path.insert(0, str(SYSTEMS_DIR))


@pytest.fixture
def data_dir():
    """Return the game/data directory path."""
    return GAME_DIR / "data"


@pytest.fixture
def sephirot_data_dir(data_dir):
    """Return the sephirot data directory path."""
    return data_dir / "sephirot"


@pytest.fixture
def protection_data_dir(data_dir):
    """Return the protection data directory path."""
    return data_dir / "protection"


@pytest.fixture
def choices_data_dir(data_dir):
    """Return the choices data directory path."""
    return data_dir / "choices"


@pytest.fixture
def angel_data_dir(data_dir):
    """Return the angel data directory path."""
    return data_dir / "angel"


@pytest.fixture
def load_json_file():
    """Return a helper function to load JSON files."""
    def _load(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return _load


@pytest.fixture
def mock_renpy_state():
    """Provide a mock Ren'Py global state for testing system modules.

    Creates a dictionary that simulates the global variables available
    in Ren'Py's init python: context.
    """
    state = {
        "current_chapter": 1,
        "current_sephirot_id": 1,
        "current_phase": "forgetting",
        "narrative_beat": "ENCOUNTER",
        "active_narrative_tags": set(),
        "wing_brightness_permanent": 1.0,
        "wing_brightness_temporary": 0.0,
        "angel_presence_state": "PRESENT",
        "angel_emotional_state": "calm",
        "angel_intervention_count": 0,
        "bond_depth": 0.0,
        "hug_count_this_sephirot": 0,
        "hug_cooldown_end_time": 0,
        "choice_history": [],
        "sephirot_states": {i: "LOCKED" for i in range(1, 17)},
        "escape_counts": {},
        "consecutive_escape_count": 0,
        "undertow_state": {
            "active_undertows": [],
            "afterimage_undertows": [],
            "nihilism_warning_triggered": False,
            "intervention_log": [],
        },
        "final_choice_unlocked": False,
    }
    state["sephirot_states"][1] = "ACTIVE"
    return state


@pytest.fixture
def mock_persistent():
    """Provide a mock persistent object for testing."""
    persistent = MagicMock()
    persistent.endings_seen = []
    persistent.cg_unlocked = []
    persistent.total_playthroughs = 0
    persistent.first_playthrough = True
    persistent.sephirot_completion_records = {}
    persistent.low_stim_mode = False
    persistent.visual_undertow_off = False
    persistent.screen_shake_off = False
    persistent.audio_stable_mode = False
    return persistent


# ── Data fixtures ──

TEST_DATA_ROOT = Path(__file__).parent / "data" / "fixtures"


@pytest.fixture
def undertow_definitions():
    """Load complete 8-undertow definitions from game data."""
    with open(GAME_DIR / "data" / "protection" / "undertow_definitions.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def sephirot_01_data():
    """Load Sephirot 1 data from game data."""
    with open(GAME_DIR / "data" / "sephirot" / "sephirot_01.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def choice_engage():
    """Load ENGAGE/ESCAPE choice data from game data."""
    with open(GAME_DIR / "data" / "choices" / "ch01" / "ch01_s1_c1.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def dialogue_pool():
    """Load angel dialogue pool from game data."""
    with open(GAME_DIR / "data" / "angel" / "dialogue_pool.json", "r", encoding="utf-8") as f:
        return json.load(f)
