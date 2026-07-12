"""Abstract base class for CLI actions (subcommands)."""

import argparse
import logging
from typing import Any, List, NoReturn, Optional

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.cli.path_resolver import PathResolver, PathResolverError
from rhapsody_cli.exceptions import CliExecutionError, RhapsodyConnectionError
from rhapsody_cli.models.elements.containment import RPProject


class AbstractAction:
    """Base class for a single subcommand action.

    Each action owns:
      - command_id: The subcommand identifier (e.g., "add", "open", "import")
      - logger: Instance-specific logger for this action
      - its own argument registration (init_arguments)
      - its own execution logic (execute)

    Instance Attributes:
      command_id (str): Subcommand identifier used for CLI dispatch (e.g., "add" for "element add")
      logger (logging.Logger): Instance-specific logger using the class name
    """

    def __init__(self, command_id: str = "") -> None:
        """Initialize the action with a command identifier.

        Args:
            command_id: The subcommand identifier (e.g., "add", "open", "import")
        """
        self.command_id = command_id
        self.logger = logging.getLogger(self.__class__.__name__)

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register this action's subparser and arguments.

        Args:
            sub_parser: The subparsers object returned by
                ArgumentParser.add_subparsers(), used to add this action's
                own subparser via sub_parser.add_parser(...).
        """
        raise NotImplementedError("Subclasses must implement the init_arguments method.")

    def execute(self, args: argparse.Namespace) -> None:
        """Execute the action using the parsed arguments.

        Args:
            args: The parsed argparse.Namespace for the command group.
        """
        raise NotImplementedError("Subclasses must implement the execute method.")

    @staticmethod
    def add_verbose_argument(parser: argparse.ArgumentParser) -> None:
        """Add the shared --verbose/-v flag to a subcommand parser.

        Args:
            parser: The argument parser to add the verbose flag to.
        """
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Enable DEBUG-level logging",
        )


class RhapsodyContextAction(AbstractAction):
    """Base class for actions that require a live Rhapsody connection.

    Provides shared error handling and lazily-cached application/project
    state, plus multi-format output rendering.
    """

    _NO_ACTIVE_INSTANCE_MESSAGE = "No running Rhapsody instance found. Please open Rhapsody and a project first."

    def __init__(self, command_id: str = "") -> None:
        """Initialize the action with a command identifier and empty connection state.

        Args:
            command_id: The subcommand identifier (e.g., "add", "open", "import")
        """
        super().__init__(command_id)
        self._app: Optional[RhapsodyApplication] = None
        self._project: Optional[RPProject] = None
        self.output_format: str = "table"

    def _connect_app(self) -> RhapsodyApplication:
        """Lazily connect to Rhapsody and cache the connection for this action.

        Returns:
            The cached RhapsodyApplication, connecting on first access.
        """
        if self._app is None:
            self._app = RhapsodyApplication.connect()
        return self._app

    def _print_formatted_output(
        self,
        data: Any,
        headers: List[str],
        table_rows: List[List[Any]],
        *,
        force_table: bool = False,
    ) -> None:
        """Format `data` per this action's output_format and print to stdout.

        Result data goes to stdout (not the logger) so it stays safe for
        piping/redirection (e.g. `> out.json`).

        Args:
            data: Payload to emit when the output format is JSON.
            headers: Column headers for the table form.
            table_rows: Rows (each a list of cells) for the table form.
            force_table: When True, always render the table form even if
                output_format is JSON. Use this to preserve an existing
                table-only contract while sharing the helper.
        """
        if self.output_format == "json" and not force_table:
            output = OutputFormatter.json_format(data)
        else:
            output = OutputFormatter.table(headers, table_rows)
        print(output)

    def _handle_connection_error(self, error: RhapsodyConnectionError, context_msg: str = "") -> NoReturn:
        """Log a connection error and raise CliExecutionError for the user.

        Args:
            error: The RhapsodyConnectionError to handle.
            context_msg: Optional context message to log.

        Raises:
            CliExecutionError: Always, with the user-facing "no active
                instance" message.
        """
        msg = f"Failed to attach to Rhapsody: {error}"
        if context_msg:
            msg = f"{context_msg}: {msg}"
        self.logger.error(msg)
        raise CliExecutionError(self._NO_ACTIVE_INSTANCE_MESSAGE) from error

    def _handle_execution_error(self, error: Exception, operation: str = "Operation") -> NoReturn:
        """Log an execution error and raise CliExecutionError for the user.

        Args:
            error: The exception to handle.
            operation: Description of what operation failed.

        Raises:
            CliExecutionError: Always, wrapping `error`'s message.
        """
        self.logger.error("%s failed: %s", operation, error)
        raise CliExecutionError(f"Error: {error}") from error


class ElementManagementAction(RhapsodyContextAction):
    """Base class for element management actions (add, delete, query, view).

    Provides shared element-specific utilities.
    """

    _PATH_ARGUMENT_HELP = "Container path using '/' or '\\' separators (default: project root)"

    _RECURSIVE_QUERY_HELP = "Include elements nested at any depth below the container"
    _RECURSIVE_DELETE_HELP = "Delete the element and all elements nested within it"

    @staticmethod
    def add_path_argument(
        parser: argparse.ArgumentParser,
        *,
        required: bool = False,
        help_text: str = _PATH_ARGUMENT_HELP,
    ) -> None:
        """Add the shared --path argument to a subcommand parser.

        Args:
            parser: The argument parser to add the path argument to.
            required: Whether the argument is required (defaults to False).
            help_text: Help text shown in --help (defaults to the standard
                container-path description).
        """
        parser.add_argument("--path", default=None, required=required, help=help_text)

    @staticmethod
    def add_recursive_argument(parser: argparse.ArgumentParser, *, help_text: str) -> None:
        """Add the shared --recursive flag to a subcommand parser.

        Args:
            parser: The argument parser to add the recursive flag to.
            help_text: Help text shown in --help (caller-supplied because
                query vs. delete have different descriptions).
        """
        parser.add_argument("--recursive", action="store_true", help=help_text)

    def _get_active_project(self) -> RPProject:
        """Get the active project, handling errors appropriately.

        Returns:
            The active project object.

        Raises:
            CliExecutionError: If no active project or connection error occurs.
        """
        try:
            app = self._connect_app()
            self._project = app.active_project()
            return self._project
        except RhapsodyConnectionError as e:
            self._handle_connection_error(e)

    def _get_active_root(self) -> Any:
        """Return the root element of the active project.

        Returns:
            The root model element of the active project.
        """
        return self._get_active_project().get_root()

    def _resolve_container_or_element(
        self,
        root: Any,
        path: Optional[str],
        *,
        resolve_element: bool,
        operation: str = "resolve path",
    ) -> Any:
        """Resolve `path` to a container or element, mapping errors to CliExecutionError.

        Args:
            root: The root element to navigate from (typically the active
                project's root).
            path: A "/" or "\\"-separated path, or None/"" to mean the root
                itself (only valid when `resolve_element` is False).
            resolve_element: True to use PathResolver.resolve_element (strict,
                path required); False to use PathResolver.resolve_container
                (lenient, empty path returns root).
            operation: Short description of the calling operation, used in
                the error message if an unexpected exception occurs.

        Returns:
            The element/container resolved at the end of the path.

        Raises:
            CliExecutionError: If the path cannot be parsed or navigated, or
                if PathResolver raises any other exception.
        """
        try:
            if resolve_element:
                if path is None:
                    raise CliExecutionError(f"A path is required to {operation}")
                return PathResolver.resolve_element(root, path)
            return PathResolver.resolve_container(root, path)
        except PathResolverError as e:
            self.logger.error("%s", e)
            raise CliExecutionError(str(e)) from e
        except Exception as e:
            self._handle_execution_error(e, f"Failed to {operation}")
