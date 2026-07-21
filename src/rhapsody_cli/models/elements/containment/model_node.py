"""Wraps ``com.telelogic.rhapsody.core.IRPNode``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.containment.model_component_instance import RPComponentInstance


class RPNode(RPUnit):
    """Wraps ``IRPNode``: a node that extends ``IRPUnit``."""

    # IRPNode method parity checklist:
    # [x] add_component_instance  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] delete_component_instance  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_component_instance  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_cp_utype  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_component_instances  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_cp_utype  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_unit / irp_model_element methods (covered by rp_unit / rp_model_element checklists)
    # No deprecated IRPNode methods.

    def add_component_instance(self, name: str) -> "RPComponentInstance":
        """Adds a component instance to the node.

        Args:
            name: The name of the new component instance.

        Returns:
            The wrapped ``IRPComponentInstance`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPNode::addComponentInstance(java.lang.String name)
        """
        return cast("RPComponentInstance", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addComponentInstance(name))))

    def delete_component_instance(self, instance: "RPComponentInstance") -> None:
        """Deletes a component instance from the node.

        Args:
            instance: The component instance to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPNode::deleteComponentInstance(IRPComponentInstance instance)
        """
        self.call_com(lambda: self._com.deleteComponentInstance(instance._com))

    def find_component_instance(self, name: str) -> "RPComponentInstance | None":
        """Finds a component instance by name.

        Args:
            name: The name of the component instance to find.

        Returns:
            The wrapped ``IRPComponentInstance`` if found, ``None`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPNode::findComponentInstance(java.lang.String name)
        """
        result = self.call_com(lambda: self._com.findComponentInstance(name))
        if result is None:
            return None
        return cast("RPComponentInstance", AbstractRPModelElement.wrap(result))

    def get_cpu_type(self) -> str:
        """Returns the CPU type of the node.

        Returns:
            The CPU type string.

        Reference:
            com.telelogic.rhapsody.core.IRPNode::getCPUtype()
        """
        return str(self._get_method_or_property(self._com, "getCPUtype", "CPUtype"))

    def get_component_instances(self) -> "RPCollection":
        """Returns all component instances in the node.

        Returns:
            An ``RPCollection`` of ``IRPComponentInstance`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPNode::getComponentInstances()
        """
        return RPCollection(self.call_com(lambda: self._com.getComponentInstances()))

    def set_cpu_type(self, value: str) -> None:
        """Sets the CPU type of the node.

        Args:
            value: The CPU type string.

        Reference:
            com.telelogic.rhapsody.core.IRPNode::setCPUtype(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setCPUtype", "CPUtype", value)


AbstractRPModelElement.register_wrapper("Node", RPNode)
