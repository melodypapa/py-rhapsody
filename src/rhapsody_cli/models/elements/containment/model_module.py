"""Wraps ``com.telelogic.rhapsody.core.IRPModule``."""

from rhapsody_cli.models.core import register_wrapper
from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPModule(RPInstance):
    """Wraps ``IRPModule``: a module that extends ``IRPInstance``."""

    pass


register_wrapper("Module", RPModule)
