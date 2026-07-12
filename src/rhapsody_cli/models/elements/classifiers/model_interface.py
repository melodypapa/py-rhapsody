"""Interface model-element wrapper."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPInterface(RPModelElement):
    """Wraps ``IRPInterface``."""


AbstractRPModelElement.register_wrapper("Interface", RPInterface)
