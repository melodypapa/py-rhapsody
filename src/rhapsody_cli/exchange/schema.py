"""YAML schema constants for Rhapsody model exchange.

SWR_XCH_005: YAML Schema (version 1)
"""

# Schema format version. The importer rejects any other value.
SCHEMA_VERSION: int = 1

# Top-level YAML keys (kept as constants so importer/exporter stay in sync).
VERSION_KEY: str = "version"
PROJECT_KEY: str = "project"
RHAPSODY_MODEL_KEY: str = "rhapsody-model"
