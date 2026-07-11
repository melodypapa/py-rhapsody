"""
Rhapsody CLI Demo Scripts

This package contains standalone demo scripts that demonstrate how to work with
the Rhapsody COM API using rhapsody-cli.

Each demo script can be run independently and demonstrates a specific aspect of
Rhapsody automation:

- demo_01_basic_connection.py: Connection methods and basic setup
- demo_02_project_operations.py: Project management operations
- demo_03_element_navigation.py: Element navigation and querying
- demo_04_basic_element_creation.py: Creating model elements
- demo_05_error_handling.py: Error handling patterns

Requirements:
    - Windows OS (Rhapsody COM API is Windows-only)
    - IBM Rhapsody installation
    - Valid Rhapsody license

Usage:
    python -m rhapsody_cli.demos.demo_01_basic_connection
    python -m rhapsody_cli.demos.demo_02_project_operations
    # etc.

Or run directly:
    python src/rhapsody_cli/demos/demo_01_basic_connection.py
"""

__version__ = "0.1.0"

# Export main demo functions for programmatic use
from .demo_01_basic_connection import main as demo_connection
from .demo_02_project_operations import main as demo_projects
from .demo_03_element_navigation import main as demo_navigation
from .demo_04_basic_element_creation import main as demo_creation
from .demo_05_error_handling import main as demo_error_handling

__all__ = [
    "demo_connection",
    "demo_projects",
    "demo_navigation",
    "demo_creation",
    "demo_error_handling",
]
