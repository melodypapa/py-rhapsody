"""Wraps ``com.telelogic.rhapsody.core.IRPPort``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.relations.model_instance import RPInstance

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_class import RPClass


class RPPort(RPInstance):
    """Wraps ``IRPPort``: represents a port on a classifier in the model."""

    # IRPPort method parity checklist:
    # [x] add_provided_interface      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_required_interface      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_is_behavioral           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_is_reversed             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_port_contract           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_provided_interfaces     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_required_interfaces     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] remove_provided_interface   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] remove_required_interface   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_is_behavioral           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_is_reversed             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_port_contract           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_contract (deprecated, use get_port_contract) [x] impl [x] docstring [x] unit test  [ ] integration test
    # [x] set_contract (deprecated, use set_port_contract) [x] impl [x] docstring [x] unit test  [ ] integration test

    def get_is_behavioral(self) -> int:
        """Checks whether the port is a behavioral port.

        Returns:
            ``1`` if the port is behavioral, ``0`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getIsBehavioral()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsBehavioral", "isBehavioral"))

    def set_is_behavioral(self, is_behavioral: int) -> None:
        """Specifies whether the port should be a behavioral port.

        Args:
            is_behavioral: ``1`` to make the port behavioral, ``0`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::setIsBehavioral(int isBehavioral)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsBehavioral", "isBehavioral", is_behavioral)

    def get_is_reversed(self) -> int:
        """Checks whether the port's direction is reversed.

        Returns:
            ``1`` if the port is reversed, ``0`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getIsReversed()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsReversed", "isReversed"))

    def set_is_reversed(self, is_reversed: int) -> None:
        """Specifies whether the port's direction should be reversed.

        Args:
            is_reversed: ``1`` to reverse the port, ``0`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::setIsReversed(int isReversed)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsReversed", "isReversed", is_reversed)

    def get_port_contract(self) -> "RPClass":
        """Returns the contract defined for the port.

        Returns:
            The wrapped ``IRPClass`` used as the port's contract.

        Raises:
            RhapsodyRuntimeException: if the contract cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getPortContract()
        """
        return cast("RPClass", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getPortContract", "portContract")))

    def set_port_contract(self, port_contract: RPModelElement) -> None:
        """Specifies the contract to use for the port.

        Args:
            port_contract: The class (``IRPClass``) to use as the port's contract.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::setPortContract(com.telelogic.rhapsody.core.IRPClass portContract)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setPortContract", "portContract", port_contract._com)

    def get_provided_interfaces(self) -> RPCollection:
        """Returns the interfaces provided by the port.

        Returns:
            An ``RPCollection`` of provided interface classes.

        Raises:
            RhapsodyRuntimeException: if the provided interfaces cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getProvidedInterfaces()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getProvidedInterfaces", "providedInterfaces"))

    def add_provided_interface(self, new_val: RPModelElement) -> None:
        """Adds a provided interface to the port.

        Args:
            new_val: The class (``IRPClass``) to add as a provided interface.

        Raises:
            RhapsodyRuntimeException: if the provided interface cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::addProvidedInterface(com.telelogic.rhapsody.core.IRPClass newVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addProvidedInterface(new_val._com))

    def remove_provided_interface(self, new_val: RPModelElement) -> None:
        """Removes a provided interface from the port.

        Args:
            new_val: The class (``IRPClass``) to remove from the provided interfaces.

        Raises:
            RhapsodyRuntimeException: if the provided interface cannot be removed.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::removeProvidedInterface(com.telelogic.rhapsody.core.IRPClass newVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeProvidedInterface(new_val._com))

    def get_required_interfaces(self) -> RPCollection:
        """Returns the interfaces required by the port.

        Returns:
            An ``RPCollection`` of required interface classes.

        Raises:
            RhapsodyRuntimeException: if the required interfaces cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getRequiredInterfaces()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRequiredInterfaces", "requiredInterfaces"))

    def add_required_interface(self, new_val: RPModelElement) -> None:
        """Adds a required interface to the port.

        Args:
            new_val: The class (``IRPClass``) to add as a required interface.

        Raises:
            RhapsodyRuntimeException: if the required interface cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::addRequiredInterface(com.telelogic.rhapsody.core.IRPClass newVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addRequiredInterface(new_val._com))

    def remove_required_interface(self, new_val: RPModelElement) -> None:
        """Removes a required interface from the port.

        Args:
            new_val: The class (``IRPClass``) to remove from the required interfaces.

        Raises:
            RhapsodyRuntimeException: if the required interface cannot be removed.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::removeRequiredInterface(com.telelogic.rhapsody.core.IRPClass newVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeRequiredInterface(new_val._com))

    def get_contract(self) -> "RPClass":
        """Returns the contract defined for the port.

        Deprecated:
            This method exists for backward compatibility. Use
            :meth:`get_port_contract` instead.

        Returns:
            The wrapped ``IRPClass`` used as the port's contract.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getContract()
        """
        return cast("RPClass", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getContract", "contract")))

    def set_contract(self, contract: RPModelElement) -> None:
        """Specifies the contract to use for the port.

        Deprecated:
            This method exists for backward compatibility. Use
            :meth:`set_port_contract` instead.

        Args:
            contract: The class (``IRPClass``) to use as the port's contract.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::setContract(com.telelogic.rhapsody.core.IRPClass contract)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setContract", "contract", contract._com)


AbstractRPModelElement.register_wrapper("Port", RPPort)
