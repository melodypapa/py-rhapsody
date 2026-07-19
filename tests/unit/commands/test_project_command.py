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
from rhapsody_cli.commands.project_command import ProjectCommand
from rhapsody_cli.exceptions import CliExecutionError


class TestProjectCommandDispatch:
    """Tests for the ProjectCommand group dispatcher."""

    def test_open_subcommand_dispatches(self) -> None:
        """Test: 'open' subcommand is parsed correctly."""
        cmd = ProjectCommand(["open", "MyProject.rpy"])
        assert cmd._subcommand == "open"

    def test_missing_subcommand_exits(self) -> None:
        """Test: no subcommand raises CliExecutionError."""
        with pytest.raises(CliExecutionError):
            ProjectCommand([])


class TestProjectOpenAction:
    """Tests for ProjectOpenAction."""

    def test_open_action_execute_signature(self) -> None:
        """Test: ProjectOpenAction has execute method."""
        action = ProjectOpenAction()
        assert hasattr(action, "execute")
        assert callable(action.execute)

    def test_open_action_calls_open_project_on_connected_app(self) -> None:
        """Test: open action connects, then calls app.open_project() with the given path."""
        action = ProjectOpenAction()
        args = argparse.Namespace(project_path="MyProject.rpy", verbose=False)
        fake_project = MagicMock(name="FakeProject")
        fake_app = MagicMock(name="FakeApplication")
        fake_app.open_project.return_value = fake_project

        with patch.object(ProjectOpenAction, "_connect_app", return_value=fake_app):
            action.execute(args)

        fake_app.open_project.assert_called_once_with("MyProject.rpy")
        assert action._project is fake_project


class TestProjectListAction:
    """Tests for ProjectListAction."""

    def test_list_action_prints_name_and_filename_for_each_project(self) -> None:
        """Regression test: the list action must call get_filename() (not the
        non-existent get_path()) on each project to render its table row."""
        action = ProjectListAction()
        args = argparse.Namespace(verbose=False)

        fake_project = MagicMock(name="FakeProject")
        fake_project.get_name.return_value = "MyProject"
        fake_project.get_filename.return_value = "C:/models/MyProject.rpyx"
        fake_app = MagicMock(name="FakeApplication")
        fake_app.get_projects.return_value = [fake_project]

        with patch.object(ProjectListAction, "_connect_app", return_value=fake_app):
            # Should not raise
            action.execute(args)

        fake_project.get_filename.assert_called_once_with()


class TestProjectCloseAction:
    """Tests for ProjectCloseAction."""

    def test_close_action_execute_signature(self) -> None:
        """Test: ProjectCloseAction has execute method."""
        action = ProjectCloseAction()
        assert hasattr(action, "execute")
        assert callable(action.execute)

    def test_close_action_does_nothing_when_no_project_cached(self) -> None:
        """Test: close is a no-op (does not raise) when no project has been opened yet."""
        action = ProjectCloseAction()
        args = argparse.Namespace(verbose=False)

        action.execute(args)  # Should not raise

        assert action._project is None

    def test_close_action_closes_and_clears_cached_project(self) -> None:
        """Test: close calls project.close() and clears the cached project."""
        action = ProjectCloseAction()
        args = argparse.Namespace(verbose=False)
        fake_project = MagicMock(name="FakeProject")
        action._project = fake_project

        action.execute(args)

        fake_project.close.assert_called_once_with()
        assert action._project is None


class TestProjectNewAction:
    """Tests for ProjectNewAction."""

    def test_new_action_calls_create_project_with_arguments(self) -> None:
        """Test: new action delegates to app.create_new_project with given args."""
        action = ProjectNewAction()
        args = argparse.Namespace(project_location=".", project_name="MyNewProject", verbose=False)
        fake_project = MagicMock(name="FakeProject")
        fake_app = MagicMock(name="FakeApplication")
        fake_app.create_new_project.return_value = fake_project

        with patch.object(ProjectNewAction, "_connect_app", return_value=fake_app):
            action.execute(args)

        fake_app.create_new_project.assert_called_once_with(".", "MyNewProject")
        assert action._project is fake_project


class TestProjectCommandExportImportRegistration:
    """Tests that ProjectCommand registers export/import subcommands.

    UTS_XCH_00090: ProjectCommand registers export/import subcommands
    """

    def test_get_actions_includes_export_action(self) -> None:
        """ProjectCommand.get_actions() must include a ProjectExportAction instance."""
        cmd = ProjectCommand(["export", "--file", "out.yaml"])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "export" in command_ids

    def test_get_actions_includes_import_action(self) -> None:
        """ProjectCommand.get_actions() must include a ProjectImportAction instance."""
        cmd = ProjectCommand(["import", "--file", "in.yaml"])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "import" in command_ids

    def test_get_actions_returns_six_actions(self) -> None:
        """ProjectCommand.get_actions() must return exactly 6 actions after adding export/import."""
        cmd = ProjectCommand(["open", "MyProject.rpy"])
        actions = cmd.get_actions()

        assert len(actions) == 6
