"""Wraps ``com.telelogic.rhapsody.core.IRPProfile``."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.containment.model_package import RPPackage


class RPProfile(RPPackage):
    """Wraps ``IRPProfile``: a profile that extends ``IRPPackage``."""

    # IRPProfile method parity checklist:
    # [inherited] irp_package / irp_unit / irp_model_element methods (covered by rp_package / rp_unit / rp_model_element checklists)
    # No deprecated IRPProfile methods.

    pass


AbstractRPModelElement.register_wrapper("Profile", RPProfile)
