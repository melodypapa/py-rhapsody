"""Wraps ``com.telelogic.rhapsody.core.IRPAssociationRole``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.relations.model_instance import RPInstance

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPAssociationRole(RPInstance):
    """Wraps ``IRPAssociationRole``: an association role that extends ``IRPInstance``."""

    # IRPAssociationRole method parity checklist:
    # [x] getClassifierRoles  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getFormalRelations  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getRoleType  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPInstance / IRPRelation / IRPUnit / IRPModelElement methods (covered by RPInstance / RPRelation / RPUnit / RPModelElement checklists)
    # No deprecated IRPAssociationRole methods.

    def get_classifier_roles(self) -> RPCollection:
        """Returns the classifier roles associated with this association role.

        Returns:
            An ``RPCollection`` of classifier roles.

        Reference:
            com.telelogic.rhapsody.core.IRPAssociationRole::getClassifierRoles()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getClassifierRoles", "classifierRoles"))

    def get_formal_relations(self) -> RPCollection:
        """Returns the formal relations for this association role.

        Returns:
            An ``RPCollection`` of relations.

        Reference:
            com.telelogic.rhapsody.core.IRPAssociationRole::getFormalRelations()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getFormalRelations", "formalRelations"))

    def get_role_type(self) -> "RPClassifier":
        """Returns the role type (classifier) for this association role.

        Returns:
            The wrapped classifier representing the role type.

        Reference:
            com.telelogic.rhapsody.core.IRPAssociationRole::getRoleType()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getRoleType", "roleType")))


AbstractRPModelElement.register_wrapper("AssociationRole", RPAssociationRole)
