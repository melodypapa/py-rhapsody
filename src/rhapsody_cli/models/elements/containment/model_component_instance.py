"""Wraps ``com.telelogic.rhapsody.core.IRPComponentInstance``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.relations.model_instance import RPInstance

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.containment.model_component import RPComponent
    from rhapsody_cli.models.elements.containment.model_node import RPNode


class RPComponentInstance(RPInstance):
    """Wraps ``IRPComponentInstance``: a component instance that extends ``IRPInstance``."""

    # IRPComponentInstance method parity checklist:
    # [x] getComponentType  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getNode  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setComponentType  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPInstance / IRPRelation / IRPUnit / IRPModelElement methods (covered by RPInstance / RPRelation / RPUnit / RPModelElement checklists)
    # No deprecated IRPComponentInstance methods.

    def get_component_type(self) -> "RPComponent":
        """Returns the component type of this instance.

        Returns:
            The wrapped ``IRPComponent`` type.

        Reference:
            com.telelogic.rhapsody.core.IRPComponentInstance::getComponentType()
        """
        return cast("RPComponent", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getComponentType())))

    def get_node(self) -> "RPNode":
        """Returns the node containing this component instance.

        Returns:
            The wrapped ``IRPNode``.

        Reference:
            com.telelogic.rhapsody.core.IRPComponentInstance::getNode()
        """
        return cast("RPNode", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getNode())))

    def set_component_type(self, component: "RPComponent") -> None:
        """Sets the component type for this instance.

        Args:
            component: The component to set as type.

        Reference:
            com.telelogic.rhapsody.core.IRPComponentInstance::setComponentType(IRPComponent component)
        """
        self.call_com(lambda: self._com.setComponentType(component._com))


AbstractRPModelElement.register_wrapper("ComponentInstance", RPComponentInstance)
