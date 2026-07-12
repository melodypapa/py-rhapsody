"""Exception types raised by rhapsody_cli.

These mirror the failure modes of the Rhapsody Java API: a
``RhapsodyRuntimeException`` is raised by the Java API when a COM/JNI call
into Rhapsody fails; ``RhapsodyConnectionError`` is specific to rhapsody_cli
and covers failures to attach to or launch a Rhapsody instance.
"""


class RhapsodyRuntimeException(Exception):  # noqa: N818 - mirrors Java API naming
    """Raised when a call into the Rhapsody COM API fails.

    Mirrors ``com.telelogic.rhapsody.core.RhapsodyRuntimeException`` from the
    Java API. The original COM error message/HRESULT text is preserved as
    the exception message.
    """


class RhapsodyConnectionError(Exception):
    """Raised when rhapsody_cli cannot attach to or launch a Rhapsody instance."""


class CliExecutionError(Exception):
    """Raised by CLI actions/commands to signal a user-facing failure.

    Actions and command groups must raise this instead of calling
    ``sys.exit()`` directly or printing errors to stderr. The top-level CLI
    entry point (``rhapsody_cli.cli.cli.main``) is the only place that
    catches ``CliExecutionError`` and translates it into a process exit via
    ``sys.exit(exit_code)``.
    """

    def __init__(self, message: str, exit_code: int = 1) -> None:
        """Store the user-facing message and the desired process exit code.

        Args:
            message: The user-facing error message (no "Error:" prefix needed;
                the top-level handler formats and logs it).
            exit_code: The process exit code ``main()`` should use.
        """
        super().__init__(message)
        self.exit_code = exit_code
