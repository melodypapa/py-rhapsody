"""Wraps ``com.telelogic.rhapsody.core.IRPAssociationRole``."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPAssociationRole(RPInstance):
    """Wraps ``IRPAssociationRole``: an association role that extends ``IRPInstance``."""

    # IRPAssociationRole method parity checklist:
    # [ ] getClassifierRoles  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFormalRelations  [ ] impl  [ ] docstring  [ ] test
    # [ ] getRoleType  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPInstance / IRPRelation / IRPUnit / IRPModelElement methods (covered by RPInstance / RPRelation / RPUnit / RPModelElement checklists)
    # No deprecated IRPAssociationRole methods.

    pass


AbstractRPModelElement.register_wrapper("AssociationRole", RPAssociationRole)
