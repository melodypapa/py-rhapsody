"""Wraps ``com.telelogic.rhapsody.core.IRPModule``."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPModule(RPInstance):
    """Wraps ``IRPModule``: a module that extends ``IRPInstance``."""

    # IRPModule method parity checklist:
    # [inherited] irp_instance / irp_relation / irp_unit / irp_model_element methods (covered by rp_instance / rp_relation / rp_unit / rp_model_element checklists)
    # No deprecated IRPModule methods.

    pass


AbstractRPModelElement.register_wrapper("Module", RPModule)
