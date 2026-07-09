"""Project actions - each subcommand of `project` as its own Action class."""

import argparse

from rhapsody_cli.actions.abstract_action import RhapsodyContextAction
from rhapsody_cli.exceptions import RhapsodyConnectionError


class ProjectOpenAction(RhapsodyContextAction):
    """Open action - opens a project file."""

    def __init__(self) -> None:
        """Initialize the 'open' action."""
        super().__init__(command_id="open")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'open' subcommand and its arguments."""
        open_parser = sub_parser.add_parser("open", help="Open a project file")
        open_parser.add_argument("project_path", help="Path to the project file")
        self.add_verbose_argument(open_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Open a project file."""
        project_path = args.project_path
        try:
            ctx = self._context
            ctx.connect("attach")
            ctx.open_project(project_path)
            self.logger.info("Opened project: %s", project_path)
        except RhapsodyConnectionError as e:
            self._handle_connection_error(e, "Failed to open project")
        except Exception as e:
            self._handle_execution_error(e, f"Failed to open project '{project_path}'")


class ProjectListAction(RhapsodyContextAction):
    """List action - lists open projects."""

    def __init__(self) -> None:
        """Initialize the 'list' action."""
        super().__init__(command_id="list")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'list' subcommand and its arguments."""
        list_parser = sub_parser.add_parser("list", help="List open projects")
        self.add_verbose_argument(list_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """List open projects."""
        try:
            ctx = self._context
            ctx.connect("attach")
            assert ctx.app is not None
            projects = ctx.app.getProjects()

            if not projects or len(projects) == 0:
                self.logger.info("No open projects")
                return

            rows = [[proj.getName(), proj.getFilename()] for proj in projects]

            # NOTE: This is the command's result data (not a status/log
            # message), so it is written directly to stdout via print()
            # rather than the logger, to keep it safe for piping/redirection.
            # force_table=True preserves the table-only contract; JSON output
            # for `project list` is a separate future enhancement.
            self._print_formatted_output(data={}, headers=["Name", "Path"], table_rows=rows, force_table=True)
        except Exception as e:
            self._handle_execution_error(e, "Failed to list projects")


class ProjectCloseAction(RhapsodyContextAction):
    """Close action - closes the active project."""

    def __init__(self) -> None:
        """Initialize the 'close' action."""
        super().__init__(command_id="close")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'close' subcommand and its arguments."""
        close_parser = sub_parser.add_parser("close", help="Close active project")
        self.add_verbose_argument(close_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Close active project."""
        try:
            ctx = self._context
            if ctx.project is None:
                self.logger.info("No active project")
                return
            ctx.close_project()
            self.logger.info("Project closed")
        except Exception as e:
            self._handle_execution_error(e, "Failed to close project")


class ProjectNewAction(RhapsodyContextAction):
    """New action - creates a new project."""

    def __init__(self) -> None:
        """Initialize the 'new' action."""
        super().__init__(command_id="new")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'new' subcommand and its arguments."""
        new_parser = sub_parser.add_parser("new", help="Create a new project")
        new_parser.add_argument("project_location", help="Location for the project")
        new_parser.add_argument("project_name", help="Name of the project")
        self.add_verbose_argument(new_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Create a new project."""
        project_location = args.project_location
        project_name = args.project_name
        try:
            ctx = self._context
            ctx.connect("attach")
            ctx.create_project(project_location, project_name)
            self.logger.info("Created project: %s at %s", project_name, project_location)
        except RhapsodyConnectionError as e:
            self._handle_connection_error(e, "Failed to create project")
        except Exception as e:
            self._handle_execution_error(e, f"Failed to create project '{project_name}'")
