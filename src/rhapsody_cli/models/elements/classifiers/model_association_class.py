"""Wraps ``com.telelogic.rhapsody.core.IRPAssociationClass``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers.model_class import RPClass

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.relations.model_relation import RPRelation


class RPAssociationClass(RPClass):
    """Wraps ``IRPAssociationClass``: an association class that extends ``IRPClass``."""

    # IRPAssociationClass method parity checklist:
    # [x] getEnd1  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getEnd2  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getIsClass  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] setIsClass  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPClass / IRPClassifier / IRPUnit / IRPModelElement methods (covered by RPClass / RPClassifier / RPUnit / RPModelElement checklists)
    # No deprecated IRPAssociationClass methods.

    def get_end1(self) -> "RPRelation":
        """Returns the first end of the association.

        Returns:
            The wrapped relation representing the first end.

        Reference:
            com.telelogic.rhapsody.core.IRPAssociationClass::getEnd1()
        """
        return cast("RPRelation", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getEnd1", "end1")))

    def get_end2(self) -> "RPRelation":
        """Returns the second end of the association.

        Returns:
            The wrapped relation representing the second end.

        Reference:
            com.telelogic.rhapsody.core.IRPAssociationClass::getEnd2()
        """
        return cast("RPRelation", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getEnd2", "end2")))

    def get_is_class(self) -> int:
        """Checks whether this association class is also a class.

        Returns:
            ``1`` if this is also a class, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAssociationClass::getIsClass()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsClass", "isClass"))

    def set_is_class(self, is_class: int) -> None:
        """Sets whether this association class is also a class.

        Args:
            is_class: ``1`` to mark as a class, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAssociationClass::setIsClass(int isClass)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setIsClass(is_class))


AbstractRPModelElement.register_wrapper("AssociationClass", RPAssociationClass)
