"""Wraps ``com.telelogic.rhapsody.core.IRPModule``."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPModule(RPInstance):
    """Wraps ``IRPModule``: a module that extends ``IRPInstance``."""

    # IRPModule method parity checklist:
    # [inherited] IRPInstance / IRPRelation / IRPUnit / IRPModelElement methods (covered by RPInstance / RPRelation / RPUnit / RPModelElement checklists)
    # No deprecated IRPModule methods.

    pass


AbstractRPModelElement.register_wrapper("Module", RPModule)
