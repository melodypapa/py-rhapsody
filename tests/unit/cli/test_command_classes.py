"""Tests for CLI command classes."""

from __future__ import annotations

from unittest.mock import MagicMock, patch
import pytest

from rhapsody_cli.cli.commands.project import (
    OpenProjectCommand,
    ListProjectsCommand,
    CloseProjectCommand,
    NewProjectCommand,
)
from rhapsody_cli.cli.context import RhapsodyContext


class TestOpenProjectCommand:
    """Tests for OpenProjectCommand."""

    def test_open_command_execute_signature(self) -> None:
        """Test: OpenProjectCommand has execute method."""
        cmd = OpenProjectCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)


class TestListProjectsCommand:
    """Tests for ListProjectsCommand."""

    def test_list_command_execute_signature(self) -> None:
        """Test: ListProjectsCommand has execute method."""
        cmd = ListProjectsCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)

    def test_list_command_prints_name_and_filename_for_each_project(self) -> None:
        """Regression test: the list command must call getFilename() (not the
        non-existent getPath()) on each project to render its table row."""
        cmd = ListProjectsCommand(args=[])

        fake_project = MagicMock(name="FakeProject")
        fake_project.getName.return_value = "MyProject"
        fake_project.getFilename.return_value = "C:/models/MyProject.rpyx"
        fake_app = MagicMock(name="FakeApplication")
        fake_app.getProjects.return_value = [fake_project]

        def fake_connect(self: RhapsodyContext, method: str = "attach") -> MagicMock:
            self.app = fake_app
            return fake_app

        with patch.object(RhapsodyContext, "connect", fake_connect):
            # Should not raise
            cmd.execute()

        fake_project.getFilename.assert_called_once_with()


class TestCloseProjectCommand:
    """Tests for CloseProjectCommand."""

    def test_close_command_execute_signature(self) -> None:
        """Test: CloseProjectCommand has execute method."""
        cmd = CloseProjectCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)


class TestNewProjectCommand:
    """Tests for NewProjectCommand."""

    def test_new_command_execute_signature(self) -> None:
        """Test: NewProjectCommand has execute method."""
        cmd = NewProjectCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)

    def test_new_command_calls_create_project_with_arguments(self) -> None:
        """Test: new command delegates to context.create_project with given args."""
        cmd = NewProjectCommand(args=[])

        with patch("rhapsody_cli.cli.context.RhapsodyContext.connect"):
            with patch(
                "rhapsody_cli.cli.context.RhapsodyContext.create_project"
            ) as mock_create:
                cmd.execute(project_location=".", project_name="MyNewProject")
                mock_create.assert_called_once_with(".", "MyNewProject")
