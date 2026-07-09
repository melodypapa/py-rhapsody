"""Wraps ``com.telelogic.rhapsody.core.IRPCollaboration``."""

from rhapsody_cli.models._core import RPUnit, register_wrapper


class RPCollaboration(RPUnit):
    """Wraps ``IRPCollaboration``: a collaboration that extends ``IRPUnit``."""

    pass


register_wrapper("Collaboration", RPCollaboration)
