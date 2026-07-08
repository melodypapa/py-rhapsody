"""Tests for project actions and the ProjectCommand dispatcher."""

import argparse
from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.project_action import (
    ProjectCloseAction,
    ProjectListAction,
    ProjectNewAction,
    ProjectOpenAction,
)
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.commands.project_command import ProjectCommand


class TestProjectCommandDispatch:
    """Tests for the ProjectCommand group dispatcher."""

    def test_open_subcommand_dispatches(self) -> None:
        """Test: 'open' subcommand is parsed correctly."""
        cmd = ProjectCommand(["open", "MyProject.rpy"])
        assert cmd._subcommand == "open"

    def test_missing_subcommand_exits(self) -> None:
        """Test: no subcommand causes SystemExit."""
        with pytest.raises(SystemExit):
            ProjectCommand([])


class TestProjectOpenAction:
    """Tests for ProjectOpenAction."""

    def test_open_action_execute_signature(self) -> None:
        """Test: ProjectOpenAction has execute method."""
        action = ProjectOpenAction()
        assert hasattr(action, "execute")
        assert callable(action.execute)


class TestProjectListAction:
    """Tests for ProjectListAction."""

    def test_list_action_prints_name_and_filename_for_each_project(self) -> None:
        """Regression test: the list action must call getFilename() (not the
        non-existent getPath()) on each project to render its table row."""
        action = ProjectListAction()
        args = argparse.Namespace(verbose=False)

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
            action.execute(args)

        fake_project.getFilename.assert_called_once_with()


class TestProjectCloseAction:
    """Tests for ProjectCloseAction."""

    def test_close_action_execute_signature(self) -> None:
        """Test: ProjectCloseAction has execute method."""
        action = ProjectCloseAction()
        assert hasattr(action, "execute")
        assert callable(action.execute)


class TestProjectNewAction:
    """Tests for ProjectNewAction."""

    def test_new_action_calls_create_project_with_arguments(self) -> None:
        """Test: new action delegates to context.create_project with given args."""
        action = ProjectNewAction()
        args = argparse.Namespace(project_location=".", project_name="MyNewProject", verbose=False)

        with patch("rhapsody_cli.cli.context.RhapsodyContext.connect"):
            with patch("rhapsody_cli.cli.context.RhapsodyContext.create_project") as mock_create:
                action.execute(args)
                mock_create.assert_called_once_with(".", "MyNewProject")
