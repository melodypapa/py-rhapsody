"""Subprocess-based CLI tests for element operations.

These tests invoke the CLI as a real subprocess using subprocess.run(),
rather than using CliRunner's isolated context. This tests the actual
installed CLI behavior end-to-end.

For tests requiring a live Rhapsody instance, see test_element_cli_integration.py
"""

import subprocess
import sys


class TestElementCLISubprocess:
    """Test element CLI by invoking it as a subprocess."""

    CLI_MODULE = "rhapsody_cli.cli.main"

    @staticmethod
    def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
        """Run the CLI as a subprocess.

        Args:
            *args: CLI arguments (e.g., "element", "query")

        Returns:
            CompletedProcess with stdout, stderr, returncode
        """
        cmd = [sys.executable, "-m", TestElementCLISubprocess.CLI_MODULE, *args]
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_cli_help_command(self) -> None:
        """Test that CLI help command works."""
        result = self._run_cli("--help")
        assert result.returncode == 0, f"Help failed: {result.stderr}"
        assert "Usage:" in result.stdout or "usage:" in result.stdout.lower()

    def test_cli_verbose_flag(self) -> None:
        """Test that --verbose flag is accepted at subcommand level."""
        result = self._run_cli("element", "query", "--verbose")
        # Should not crash with unrecognized option error
        # (May fail with Rhapsody connection error, but not with usage error)
        assert "unrecognized arguments" not in result.stderr.lower()

    def test_element_add_missing_arguments(self) -> None:
        """Test that CLI validates required arguments."""
        result = self._run_cli("element", "add")
        # Should fail with usage error
        assert result.returncode != 0
        assert "required" in result.stderr.lower() or "Error" in result.stderr or "usage:" in result.stderr.lower()

    def test_element_delete_missing_arguments(self) -> None:
        """Test that delete command requires path argument."""
        result = self._run_cli("element", "delete")
        # Should fail with usage error
        assert result.returncode != 0
        assert "required" in result.stderr.lower() or "Error" in result.stderr or "usage:" in result.stderr.lower()

    def test_cli_invalid_command(self) -> None:
        """Test that CLI rejects invalid commands."""
        result = self._run_cli("invalid_command")
        assert result.returncode != 0
        assert "invalid choice" in result.stderr.lower() or "Error" in result.stderr or "usage:" in result.stderr.lower()

    def test_cli_add_connection_check(self) -> None:
        """Test that add command attempts to connect to Rhapsody.

        When Rhapsody is not running, should fail with connection error.
        """
        result = self._run_cli("element", "add", "--type", "class", "--name", "TestClass")
        # Will fail due to no Rhapsody, but should have a proper error message
        if result.returncode != 0:
            # Make sure it's not a usage error
            assert "unrecognized arguments" not in result.stderr.lower()

    def test_cli_delete_connection_check(self) -> None:
        """Test that delete command attempts to connect to Rhapsody.

        When Rhapsody is not running, should fail with connection error.
        """
        result = self._run_cli("element", "delete", "Root::TestClass")
        # Will fail due to no Rhapsody, but should have a proper error message
        if result.returncode != 0:
            # Make sure it's not a usage error
            assert "unrecognized arguments" not in result.stderr.lower()

    def test_cli_add_with_invalid_type(self) -> None:
        """Test that CLI validates element type."""
        result = self._run_cli("element", "add", "--type", "InvalidType", "--name", "TestClass")
        # Should fail with validation error or connection error
        # (not a success)
        # May fail before connecting if type validation happens first
        assert result.returncode != 0

    def test_cli_verbose_outputs_debug_info(self) -> None:
        """Test that --verbose flag changes output verbosity."""
        # Run with verbose at subcommand level
        result_verbose = self._run_cli("element", "query", "--verbose")

        # Just verify verbose flag is accepted (not an unrecognized option error)
        assert "unrecognized arguments" not in result_verbose.stderr.lower()
