"""YAML import/export for Rhapsody models.

Public API:
    - RhapsodyImporter: YAML dict -> Rhapsody model
    - RhapsodyExporter: Rhapsody model -> YAML dict
    - RhapsodyYaml: file I/O wrapper around PyYAML
    - SCHEMA_VERSION: YAML schema format version (currently 1)
"""

from rhapsody_cli.exchange.schema import PROJECT_KEY, RHAPSODY_MODEL_KEY, SCHEMA_VERSION, VERSION_KEY

__all__ = [
    "PROJECT_KEY",
    "RHAPSODY_MODEL_KEY",
    "SCHEMA_VERSION",
    "VERSION_KEY",
]

# RhapsodyImporter, RhapsodyExporter, RhapsodyYaml are imported lazily by actions
# to avoid importing pywin32 at module load on non-Windows dev machines.
