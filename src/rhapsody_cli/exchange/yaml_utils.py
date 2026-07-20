"""YAML file I/O helper for the exchange package.

SWR_XCH_005: YAML Schema (version 1) — file I/O layer
"""

from typing import Any, Dict

import yaml

from rhapsody_cli.exceptions import CliExecutionError


class RhapsodyYaml:
    """YAML file I/O helper. Translates PyYAML errors to CliExecutionError.

    Stateless: instances are cheap to create. Wraps PyYAML's safe_load /
    safe_dump so callers never see raw YAMLError or OSError.
    """

    def read(self, path: str) -> Dict[str, Any]:
        """Read and parse a YAML file.

        Args:
            path: Path to the YAML file.

        Returns:
            Parsed YAML mapping as a dict.

        Raises:
            CliExecutionError: If file is missing, YAML is invalid, or top-level
                value is not a mapping.
        """
        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError as e:
            raise CliExecutionError(f"Input file not found: {path}") from e
        except yaml.YAMLError as e:
            raise CliExecutionError(f"Invalid YAML in {path}: {e}") from e
        if not isinstance(data, dict):
            raise CliExecutionError(f"Expected YAML mapping at top level of {path}, got {type(data).__name__}")
        return data

    def write(self, path: str, data: Dict[str, Any]) -> None:
        """Write a dict to a YAML file.

        Args:
            path: Output file path.
            data: Dict to serialize.

        Raises:
            CliExecutionError: If the file cannot be written.
        """
        try:
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        except OSError as e:
            raise CliExecutionError(f"Failed to write {path}: {e}") from e
