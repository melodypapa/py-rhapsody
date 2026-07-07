"""End-to-end integration tests for element CLI operations with live Rhapsody instance.

These tests require a running Rhapsody instance with an open project.
Manual test procedure:
    1. Start Rhapsody application (GUI)
    2. Open or create a test project
    3. Run: pytest tests/cli/test_element_cli_integration.py -v -m "not skip"

To skip E2E tests in CI:
    pytest tests/cli/test_element_cli_integration.py -m "skip"
"""

from __future__ import annotations

import time

import pytest
from click.testing import CliRunner

from rhapsody_cli.cli.commands.element import ElementCommandGroup


class TestElementCLIIntegration:
    """End-to-end tests for element CLI with live Rhapsody instance."""

    @staticmethod
    def _generate_unique_name(prefix: str = "TestClass") -> str:
        """Generate a unique element name using timestamp."""
        return f"{prefix}_{int(time.time() * 1000) % 1000000}"

    @pytest.mark.skip(
        reason=(
            "Requires live Rhapsody instance. Run manually: "
            "pytest tests/cli/test_element_cli_integration.py -m 'not skip'"
        )
    )
    def test_add_and_delete_class_workflow(self) -> None:
        """E2E: Add a class, verify it exists, delete it, verify deletion.

        This end-to-end test requires a live Rhapsody instance.
        """
        runner = CliRunner()
        group = ElementCommandGroup()
        class_name = self._generate_unique_name("TestClass")

        # Step 1: Add a class
        add_result = runner.invoke(group, ["add", "--type", "class", "--name", class_name])
        assert add_result.exit_code == 0, f"Add failed: {add_result.output}"
        assert f"Created class: {class_name}" in add_result.output

        # Step 2: Query and verify the class exists
        query_result = runner.invoke(group, ["query"])
        assert query_result.exit_code == 0, f"Query failed: {query_result.output}"
        assert (
            class_name in query_result.output
        ), f"Class not found in query output: {query_result.output}"

        # Step 3: Delete the class
        delete_result = runner.invoke(group, ["delete", "--path", f"Root::{class_name}"])
        assert delete_result.exit_code == 0, f"Delete failed: {delete_result.output}"
        assert f"Deleted class: {class_name}" in delete_result.output

        # Step 4: Query and verify the class is gone
        query_after_delete = runner.invoke(group, ["query"])
        assert query_after_delete.exit_code == 0, f"Query failed: {query_after_delete.output}"
        assert (
            class_name not in query_after_delete.output
        ), f"Class still exists after deletion: {query_after_delete.output}"

    @pytest.mark.skip(
        reason=(
            "Requires live Rhapsody instance. Run manually: "
            "pytest tests/cli/test_element_cli_integration.py -m 'not skip'"
        )
    )
    def test_add_multiple_classes_and_clean_up(self) -> None:
        """E2E: Add multiple classes, clean them up one by one."""
        runner = CliRunner()
        group = ElementCommandGroup()

        class_names = [self._generate_unique_name(f"TestClass{i}") for i in range(3)]

        # Add multiple classes
        for class_name in class_names:
            result = runner.invoke(group, ["add", "--type", "class", "--name", class_name])
            assert result.exit_code == 0, f"Add failed: {result.output}"

        # Query and verify all exist
        query_result = runner.invoke(group, ["query"])
        assert query_result.exit_code == 0
        for class_name in class_names:
            assert class_name in query_result.output, f"Class {class_name} not found in query"

        # Delete each one and verify
        for class_name in class_names:
            delete_result = runner.invoke(group, ["delete", "--path", f"Root::{class_name}"])
            assert delete_result.exit_code == 0, f"Delete failed: {delete_result.output}"

            query_result = runner.invoke(group, ["query"])
            assert query_result.exit_code == 0
            assert (
                class_name not in query_result.output
            ), f"Class {class_name} still exists after deletion"
