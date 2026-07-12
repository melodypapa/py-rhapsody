"""Signal model-element wrapper."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPSignal(RPModelElement):
    """Wraps ``IRPSignal``."""


AbstractRPModelElement.register_wrapper("Signal", RPSignal)
