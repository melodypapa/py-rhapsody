"""Tests for RhapsodyYaml file I/O.

UTS_XCH_00002: RhapsodyYaml.read happy path
UTS_XCH_00003: RhapsodyYaml.read missing file
UTS_XCH_00004: RhapsodyYaml.read invalid YAML
UTS_XCH_00005: RhapsodyYaml.read non-mapping top level
UTS_XCH_00006: RhapsodyYaml.write happy path
UTS_XCH_00007: RhapsodyYaml.write failure
UTS_XCH_00008: RhapsodyYaml round-trip
"""

from typing import Any

import pytest

from rhapsody_cli.exceptions import CliExecutionError
from rhapsody_cli.exchange.yaml_utils import RhapsodyYaml


class TestRhapsodyYamlRead:
    """UTS_XCH_00002-00005: RhapsodyYaml.read behavior."""

    def test_read_returns_parsed_dict(self, tmp_path: Any) -> None:
        """UTS_XCH_00002: read() returns the parsed YAML mapping."""
        yaml_file = tmp_path / "model.yaml"
        yaml_file.write_text("version: 1\nproject: MyProject\n", encoding="utf-8")

        result = RhapsodyYaml().read(str(yaml_file))

        assert result == {"version": 1, "project": "MyProject"}

    def test_read_missing_file_raises_cli_execution_error(self, tmp_path: Any) -> None:
        """UTS_XCH_00003: read() raises CliExecutionError for missing file."""
        missing = tmp_path / "nonexistent.yaml"

        with pytest.raises(CliExecutionError) as exc_info:
            RhapsodyYaml().read(str(missing))

        assert "not found" in str(exc_info.value).lower()

    def test_read_invalid_yaml_raises_cli_execution_error(self, tmp_path: Any) -> None:
        """UTS_XCH_00004: read() raises CliExecutionError for malformed YAML."""
        yaml_file = tmp_path / "bad.yaml"
        yaml_file.write_text("version: 1\n  bad: : : indent\n", encoding="utf-8")

        with pytest.raises(CliExecutionError) as exc_info:
            RhapsodyYaml().read(str(yaml_file))

        assert "invalid yaml" in str(exc_info.value).lower()

    def test_read_non_mapping_top_level_raises_cli_execution_error(self, tmp_path: Any) -> None:
        """UTS_XCH_00005: read() raises CliExecutionError when top level is a list/scalar."""
        yaml_file = tmp_path / "list.yaml"
        yaml_file.write_text("- item1\n- item2\n", encoding="utf-8")

        with pytest.raises(CliExecutionError) as exc_info:
            RhapsodyYaml().read(str(yaml_file))

        assert "mapping" in str(exc_info.value).lower()


class TestRhapsodyYamlWrite:
    """UTS_XCH_00006-00007: RhapsodyYaml.write behavior."""

    def test_write_creates_file_with_yaml_content(self, tmp_path: Any) -> None:
        """UTS_XCH_00006: write() serializes dict to YAML file."""
        yaml_file = tmp_path / "out.yaml"
        data = {"version": 1, "project": "MyProject", "items": ["a", "b"]}

        RhapsodyYaml().write(str(yaml_file), data)

        assert yaml_file.exists()
        content = yaml_file.read_text(encoding="utf-8")
        assert "version: 1" in content
        assert "MyProject" in content

    def test_write_failure_raises_cli_execution_error(self, tmp_path: Any) -> None:
        """UTS_XCH_00007: write() raises CliExecutionError on OS error (e.g. directory missing)."""
        missing_dir = tmp_path / "nonexistent_dir" / "out.yaml"

        with pytest.raises(CliExecutionError) as exc_info:
            RhapsodyYaml().write(str(missing_dir), {"version": 1})

        assert "failed to write" in str(exc_info.value).lower()


class TestRhapsodyYamlRoundTrip:
    """UTS_XCH_00008: round-trip write -> read preserves data."""

    def test_round_trip_preserves_data(self, tmp_path: Any) -> None:
        """UTS_XCH_00008: data written then read back equals original."""
        yaml_file = tmp_path / "round.yaml"
        data = {
            "version": 1,
            "project": "MyProject",
            "rhapsody-model": [
                {"name": "Pkg1", "type": "Package", "children": []},
                {"name": "MyClass", "type": "Class"},
            ],
        }

        yaml_io = RhapsodyYaml()
        yaml_io.write(str(yaml_file), data)
        result = yaml_io.read(str(yaml_file))

        assert result == data
