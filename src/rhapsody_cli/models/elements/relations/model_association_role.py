"""Wraps ``com.telelogic.rhapsody.core.IRPAssociationRole``."""

from rhapsody_cli.models._core import register_wrapper
from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPAssociationRole(RPInstance):
    """Wraps ``IRPAssociationRole``: an association role that extends ``IRPInstance``."""

    pass


register_wrapper("AssociationRole", RPAssociationRole)
