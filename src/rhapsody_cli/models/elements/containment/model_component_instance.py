"""Wraps ``com.telelogic.rhapsody.core.IRPComponentInstance``."""

from rhapsody_cli.models._core import register_wrapper
from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPComponentInstance(RPInstance):
    """Wraps ``IRPComponentInstance``: a component instance that extends ``IRPInstance``."""

    pass


register_wrapper("ComponentInstance", RPComponentInstance)
