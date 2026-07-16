"""Wraps ``com.telelogic.rhapsody.core.IRPDependency``."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement

if TYPE_CHECKING:
    pass


class RPDependency(RPModelElement):
    """Wraps ``IRPDependency``: a dependency relationship."""

    # IRPDependency method parity checklist:
    # [ ] get_dependent  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_depends_on  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] is_need_to_migrate  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_dependent  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_depends_on  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_link_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_owner_without_changing_dependent  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklists)
    # No deprecated IRPDependency methods.

    def get_dependent(self) -> RPModelElement:
        """Returns the model element that is dependent.

        Returns:
            The wrapped dependent model element.

        Reference:
            com.telelogic.rhapsody.core.IRPDependency::getDependent()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getDependent", "dependent"))

    def get_depends_on(self) -> RPModelElement:
        """Returns the model element that is depended upon.

        Returns:
            The wrapped model element that is depended upon.

        Reference:
            com.telelogic.rhapsody.core.IRPDependency::getDependsOn()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getDependsOn", "dependsOn"))

    def is_need_to_migrate(self) -> int:
        """Checks whether the dependency needs to be migrated.

        Returns:
            ``1`` if the dependency needs migration, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPDependency::isNeedToMigrate()
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.isNeedToMigrate()))

    def set_dependent(self, dependent: RPModelElement) -> None:
        """Sets the model element that is dependent.

        Args:
            dependent: The wrapped model element to set as dependent.

        Reference:
            com.telelogic.rhapsody.core.IRPDependency::setDependent(com.telelogic.rhapsody.core.IRPModelElement dependent)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setDependent(dependent._com))

    def set_depends_on(self, depends_on: RPModelElement) -> None:
        """Sets the model element that is depended upon.

        Args:
            depends_on: The wrapped model element to set as the dependency target.

        Reference:
            com.telelogic.rhapsody.core.IRPDependency::setDependsOn(com.telelogic.rhapsody.core.IRPModelElement dependsOn)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setDependsOn(depends_on._com))

    def set_link_type(self, link_type: str) -> None:
        """Sets the link type of the dependency.

        Args:
            link_type: The link type string to set.

        Reference:
            com.telelogic.rhapsody.core.IRPDependency::setLinkType(java.lang.String linkType)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setLinkType(link_type))

    def set_owner_without_changing_dependent(self, owner: RPModelElement) -> None:
        """Sets the owner of the dependency without changing the dependent.

        Args:
            owner: The wrapped model element to set as the owner.

        Reference:
            com.telelogic.rhapsody.core.IRPDependency::setOwnerWithoutChangingDependent(IRPModelElement owner)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setOwnerWithoutChangingDependent(owner._com))


AbstractRPModelElement.register_wrapper("Dependency", RPDependency)
