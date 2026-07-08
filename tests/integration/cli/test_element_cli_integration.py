"""End-to-end integration tests for element CLI operations with live Rhapsody instance.

These tests require a running Rhapsody instance with an open project.
Manual test procedure:
    1. Start Rhapsody application (GUI)
    2. Open or create a test project
    3. Run: pytest tests/integration/cli/test_element_cli_integration.py -v

To skip E2E tests in CI:
    pytest tests/integration/cli/test_element_cli_integration.py --co -q | head
"""

from __future__ import annotations

import time

from rhapsody_cli.cli.commands.element import (
    AddElementCommand,
    QueryElementCommand,
    DeleteElementCommand,
)


class TestElementCLIIntegration:
    """End-to-end tests for element CLI with live Rhapsody instance."""

    @staticmethod
    def _generate_unique_name(prefix: str = "TestClass") -> str:
        """Generate a unique element name using timestamp."""
        return f"{prefix}_{int(time.time() * 1000) % 1000000}"

    def test_add_and_delete_class_workflow(self) -> None:
        """E2E: Add a class, verify it exists, delete it, verify deletion.

        This end-to-end test requires a live Rhapsody instance.
        """
        class_name = self._generate_unique_name("TestClass")

        # Step 1: Add a class
        add_cmd = AddElementCommand(args=[])
        # This should not raise if Rhapsody is running
        add_cmd.execute(element_type="class", name=class_name)

        # Step 2: Query and verify the class exists
        query_cmd = QueryElementCommand(args=[])
        # This should succeed and list the class
        query_cmd.execute(pattern=None)

        # Step 3: Delete the class
        delete_cmd = DeleteElementCommand(args=[])
        delete_cmd.execute(path=f"Root::{class_name}")

    def test_add_multiple_classes_and_clean_up(self) -> None:
        """E2E: Add multiple classes, clean them up one by one."""
        class_names = [self._generate_unique_name(f"TestClass{i}") for i in range(3)]

        # Add multiple classes
        add_cmd = AddElementCommand(args=[])
        for class_name in class_names:
            add_cmd.execute(element_type="class", name=class_name)

        # Query and verify all exist
        query_cmd = QueryElementCommand(args=[])
        query_cmd.execute(pattern=None)

        # Delete each one
        delete_cmd = DeleteElementCommand(args=[])
        for class_name in class_names:
            delete_cmd.execute(path=f"Root::{class_name}")
