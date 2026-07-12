"""Exception model-element wrapper."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPException(RPModelElement):
    """Wraps ``IRPException``."""


AbstractRPModelElement.register_wrapper("Exception", RPException)
