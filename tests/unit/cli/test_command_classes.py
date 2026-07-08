"""Tests for CLI command classes."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from rhapsody_cli.cli.commands.project import ProjectCommandGroup
from rhapsody_cli.cli.context import RhapsodyContext


class TestProjectCommandGroup:
    """Tests for ProjectCommandGroup."""

    def test_project_group_has_open_command(self) -> None:
        """Test: ProjectCommandGroup includes open command."""
        group = ProjectCommandGroup()
        assert "open" in group.commands
        assert group.commands["open"].name == "open"

    def test_project_group_has_list_command(self) -> None:
        """Test: ProjectCommandGroup includes list command."""
        group = ProjectCommandGroup()
        assert "list" in group.commands
        assert group.commands["list"].name == "list"

    def test_project_group_has_close_command(self) -> None:
        """Test: ProjectCommandGroup includes close command."""
        group = ProjectCommandGroup()
        assert "close" in group.commands
        assert group.commands["close"].name == "close"

    def test_project_group_has_new_command(self) -> None:
        """Test: ProjectCommandGroup includes new command."""
        group = ProjectCommandGroup()
        assert "new" in group.commands
        assert group.commands["new"].name == "new"

    def test_project_group_name_is_project(self) -> None:
        """Test: ProjectCommandGroup name is 'project'."""
        group = ProjectCommandGroup()
        assert group.name == "project"

    def test_project_group_has_help(self) -> None:
        """Test: ProjectCommandGroup has help text."""
        group = ProjectCommandGroup()
        assert group.help is not None
        assert "project" in group.help.lower()


class TestOpenProjectCommand:
    """Tests for OpenProjectCommand."""

    def test_open_command_accepts_project_path_argument(self) -> None:
        """Test: open command accepts project_path argument."""
        runner = CliRunner()
        group = ProjectCommandGroup()

        with runner.isolated_filesystem():
            # Create a dummy project file
            with open("test.rpy", "w") as f:
                f.write("mock project")

            with patch("rhapsody_cli.cli.context.RhapsodyContext.connect"):
                with patch("rhapsody_cli.cli.context.RhapsodyContext.open_project"):
                    result = runner.invoke(group, ["open", "test.rpy"])
                    # Command executes (may fail due to mocking, but should accept args)
                    assert result.exit_code in (0, 1)

    def test_open_command_name_is_open(self) -> None:
        """Test: open command name is 'open'."""
        group = ProjectCommandGroup()
        open_cmd = group.commands["open"]
        assert open_cmd.name == "open"

    def test_open_command_has_help(self) -> None:
        """Test: open command has help text."""
        group = ProjectCommandGroup()
        open_cmd = group.commands["open"]
        assert open_cmd.help is not None
        assert "open" in open_cmd.help.lower()


class TestListProjectsCommand:
    """Tests for ListProjectsCommand."""

    def test_list_command_name_is_list(self) -> None:
        """Test: list command name is 'list'."""
        group = ProjectCommandGroup()
        list_cmd = group.commands["list"]
        assert list_cmd.name == "list"

    def test_list_command_has_help(self) -> None:
        """Test: list command has help text."""
        group = ProjectCommandGroup()
        list_cmd = group.commands["list"]
        assert list_cmd.help is not None
        assert "list" in list_cmd.help.lower()

    def test_list_command_prints_name_and_filename_for_each_project(self) -> None:
        """Regression test: the list command must call getFilename() (not the
        non-existent getPath()) on each project to render its table row."""
        runner = CliRunner()
        group = ProjectCommandGroup()

        fake_project = MagicMock(name="FakeProject")
        fake_project.getName.return_value = "MyProject"
        fake_project.getFilename.return_value = "C:/models/MyProject.rpyx"
        fake_app = MagicMock(name="FakeApplication")
        fake_app.getProjects.return_value = [fake_project]

        def fake_connect(self: RhapsodyContext, method: str = "attach") -> MagicMock:
            self.app = fake_app
            return fake_app

        with patch.object(RhapsodyContext, "connect", fake_connect):
            result = runner.invoke(group, ["list"])

        assert result.exit_code == 0
        assert "MyProject" in result.output
        assert "C:/models/MyProject.rpyx" in result.output
        fake_project.getFilename.assert_called_once_with()


class TestCloseProjectCommand:
    """Tests for CloseProjectCommand."""

    def test_close_command_name_is_close(self) -> None:
        """Test: close command name is 'close'."""
        group = ProjectCommandGroup()
        close_cmd = group.commands["close"]
        assert close_cmd.name == "close"

    def test_close_command_has_help(self) -> None:
        """Test: close command has help text."""
        group = ProjectCommandGroup()
        close_cmd = group.commands["close"]
        assert close_cmd.help is not None
        assert "close" in close_cmd.help.lower()


class TestNewProjectCommand:
    """Tests for NewProjectCommand."""

    def test_new_command_accepts_location_and_name_arguments(self) -> None:
        """Test: new command accepts project_location and project_name arguments."""
        runner = CliRunner()
        group = ProjectCommandGroup()

        with runner.isolated_filesystem():
            with patch("rhapsody_cli.cli.context.RhapsodyContext.connect"):
                with patch("rhapsody_cli.cli.context.RhapsodyContext.create_project"):
                    result = runner.invoke(group, ["new", ".", "MyNewProject"])
                    # Command executes (may fail due to mocking, but should accept args)
                    assert result.exit_code in (0, 1)

    def test_new_command_calls_create_project_with_arguments(self) -> None:
        """Test: new command delegates to context.create_project with given args."""
        runner = CliRunner()
        group = ProjectCommandGroup()

        with runner.isolated_filesystem():
            with patch("rhapsody_cli.cli.context.RhapsodyContext.connect"):
                with patch(
                    "rhapsody_cli.cli.context.RhapsodyContext.create_project"
                ) as mock_create:
                    result = runner.invoke(group, ["new", ".", "MyNewProject"])
                    assert result.exit_code == 0
                    mock_create.assert_called_once_with(".", "MyNewProject")

    def test_new_command_name_is_new(self) -> None:
        """Test: new command name is 'new'."""
        group = ProjectCommandGroup()
        new_cmd = group.commands["new"]
        assert new_cmd.name == "new"

    def test_new_command_has_help(self) -> None:
        """Test: new command has help text."""
        group = ProjectCommandGroup()
        new_cmd = group.commands["new"]
        assert new_cmd.help is not None
        assert "new" in new_cmd.help.lower()
