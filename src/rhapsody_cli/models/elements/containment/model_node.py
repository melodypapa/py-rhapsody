"""Wraps ``com.telelogic.rhapsody.core.IRPNode``."""

from rhapsody_cli.models.core import RPUnit, register_wrapper


class RPNode(RPUnit):
    """Wraps ``IRPNode``: a node that extends ``IRPUnit``."""

    pass


register_wrapper("Node", RPNode)
