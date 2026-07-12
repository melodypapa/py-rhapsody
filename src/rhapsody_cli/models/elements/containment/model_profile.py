"""Wraps ``com.telelogic.rhapsody.core.IRPProfile``."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.containment.model_package import RPPackage


class RPProfile(RPPackage):
    """Wraps ``IRPProfile``: a profile that extends ``IRPPackage``."""

    # IRPProfile method parity checklist:
    # [inherited] IRPPackage / IRPUnit / IRPModelElement methods (covered by RPPackage / RPUnit / RPModelElement checklists)
    # No deprecated IRPProfile methods.

    pass


AbstractRPModelElement.register_wrapper("Profile", RPProfile)
