"""Tests for exchange.schema constants.

UTS_XCH_00001: Schema version constant sanity
"""

from rhapsody_cli.exchange.schema import (
    PROJECT_KEY,
    RHAPSODY_MODEL_KEY,
    SCHEMA_VERSION,
    VERSION_KEY,
)


def test_schema_version_is_one() -> None:
    """UTS_XCH_00001: SCHEMA_VERSION must be 1 for v1 of the format."""
    assert SCHEMA_VERSION == 1


def test_schema_version_is_int() -> None:
    """UTS_XCH_00001: SCHEMA_VERSION must be an int (not str) for clean comparison."""
    assert isinstance(SCHEMA_VERSION, int)


def test_rhapsody_model_key_constant() -> None:
    """UTS_XCH_00001: rhapsody-model key constant matches YAML schema."""
    assert RHAPSODY_MODEL_KEY == "rhapsody-model"


def test_version_key_constant() -> None:
    """UTS_XCH_00001: version key constant matches YAML schema."""
    assert VERSION_KEY == "version"


def test_project_key_constant() -> None:
    """UTS_XCH_00001: project key constant matches YAML schema."""
    assert PROJECT_KEY == "project"
