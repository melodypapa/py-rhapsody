"""Enumeration model-element wrapper."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPEnumeration(RPModelElement):
    """Wraps ``IRPEnumeration``."""


AbstractRPModelElement.register_wrapper("Enumeration", RPEnumeration)
