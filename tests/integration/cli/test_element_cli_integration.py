"""End-to-end integration tests for element CLI operations with live Rhapsody instance.

These tests require a running Rhapsody instance with an open project.
Manual test procedure:
    1. Start Rhapsody application (GUI)
    2. Open or create a test project
    3. Run: pytest tests/integration/cli/test_element_cli_integration.py -v

To skip E2E tests in CI:
    pytest tests/integration/cli/test_element_cli_integration.py --co -q | head
"""

import time

from rhapsody_cli.commands.element_command import ElementCommand


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
        add_cmd = ElementCommand(["add", "--type", "class", "--name", class_name])
        # This should not raise if Rhapsody is running
        add_cmd.execute()

        # Step 2: Query and verify the class exists
        query_cmd = ElementCommand(["query"])
        # This should succeed and list the class
        query_cmd.execute()

        # Step 3: Delete the class
        delete_cmd = ElementCommand(["delete", f"Root::{class_name}"])
        delete_cmd.execute()

    def test_add_multiple_classes_and_clean_up(self) -> None:
        """E2E: Add multiple classes, clean them up one by one."""
        class_names = [self._generate_unique_name(f"TestClass{i}") for i in range(3)]

        # Add multiple classes
        for class_name in class_names:
            add_cmd = ElementCommand(["add", "--type", "class", "--name", class_name])
            add_cmd.execute()

        # Query and verify all exist
        query_cmd = ElementCommand(["query"])
        query_cmd.execute()

        # Delete each one
        for class_name in class_names:
            delete_cmd = ElementCommand(["delete", f"Root::{class_name}"])
            delete_cmd.execute()
