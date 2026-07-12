"""Wraps ``com.telelogic.rhapsody.core.IRPPort``."""

from typing import Any

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPPort(RPInstance):
    """Wraps ``IRPPort``: represents a port on a classifier in the model."""

    # IRPPort method parity checklist:
    # [x] addProvidedInterface      [x] impl  [x] docstring  [x] test
    # [x] addRequiredInterface      [x] impl  [x] docstring  [x] test
    # [x] getIsBehavioral           [x] impl  [x] docstring  [x] test
    # [x] getIsReversed             [x] impl  [x] docstring  [x] test
    # [x] getPortContract           [x] impl  [x] docstring  [x] test
    # [x] getProvidedInterfaces     [x] impl  [x] docstring  [x] test
    # [x] getRequiredInterfaces     [x] impl  [x] docstring  [x] test
    # [x] removeProvidedInterface   [x] impl  [x] docstring  [x] test
    # [x] removeRequiredInterface   [x] impl  [x] docstring  [x] test
    # [x] setIsBehavioral           [x] impl  [x] docstring  [x] test
    # [x] setIsReversed             [x] impl  [x] docstring  [x] test
    # [x] setPortContract           [x] impl  [x] docstring  [x] test
    # [x] getContract (deprecated, use getPortContract) [x] impl [x] docstring [x] test
    # [x] setContract (deprecated, use setPortContract) [x] impl [x] docstring [x] test

    def getIsBehavioral(self) -> int:
        """Checks whether the port is a behavioral port.

        Returns:
            ``1`` if the port is behavioral, ``0`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getIsBehavioral()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsBehavioral", "isBehavioral"))

    def setIsBehavioral(self, is_behavioral: int) -> None:
        """Specifies whether the port should be a behavioral port.

        Args:
            is_behavioral: ``1`` to make the port behavioral, ``0`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::setIsBehavioral(int isBehavioral)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsBehavioral", "isBehavioral", is_behavioral)

    def getIsReversed(self) -> int:
        """Checks whether the port's direction is reversed.

        Returns:
            ``1`` if the port is reversed, ``0`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getIsReversed()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsReversed", "isReversed"))

    def setIsReversed(self, is_reversed: int) -> None:
        """Specifies whether the port's direction should be reversed.

        Args:
            is_reversed: ``1`` to reverse the port, ``0`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::setIsReversed(int isReversed)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsReversed", "isReversed", is_reversed)

    def getPortContract(self) -> Any:
        """Returns the contract defined for the port.

        Returns:
            The wrapped ``IRPClass`` used as the port's contract.

        Raises:
            RhapsodyRuntimeException: if the contract cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getPortContract()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getPortContract", "portContract"))

    def setPortContract(self, port_contract: RPModelElement) -> None:
        """Specifies the contract to use for the port.

        Args:
            port_contract: The class (``IRPClass``) to use as the port's contract.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::setPortContract(com.telelogic.rhapsody.core.IRPClass portContract)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setPortContract", "portContract", port_contract._com)

    def getProvidedInterfaces(self) -> RPCollection:
        """Returns the interfaces provided by the port.

        Returns:
            An ``RPCollection`` of provided interface classes.

        Raises:
            RhapsodyRuntimeException: if the provided interfaces cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getProvidedInterfaces()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getProvidedInterfaces", "providedInterfaces"))

    def addProvidedInterface(self, new_val: RPModelElement) -> None:
        """Adds a provided interface to the port.

        Args:
            new_val: The class (``IRPClass``) to add as a provided interface.

        Raises:
            RhapsodyRuntimeException: if the provided interface cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::addProvidedInterface(com.telelogic.rhapsody.core.IRPClass newVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addProvidedInterface(new_val._com))

    def removeProvidedInterface(self, new_val: RPModelElement) -> None:
        """Removes a provided interface from the port.

        Args:
            new_val: The class (``IRPClass``) to remove from the provided interfaces.

        Raises:
            RhapsodyRuntimeException: if the provided interface cannot be removed.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::removeProvidedInterface(com.telelogic.rhapsody.core.IRPClass newVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeProvidedInterface(new_val._com))

    def getRequiredInterfaces(self) -> RPCollection:
        """Returns the interfaces required by the port.

        Returns:
            An ``RPCollection`` of required interface classes.

        Raises:
            RhapsodyRuntimeException: if the required interfaces cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getRequiredInterfaces()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRequiredInterfaces", "requiredInterfaces"))

    def addRequiredInterface(self, new_val: RPModelElement) -> None:
        """Adds a required interface to the port.

        Args:
            new_val: The class (``IRPClass``) to add as a required interface.

        Raises:
            RhapsodyRuntimeException: if the required interface cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::addRequiredInterface(com.telelogic.rhapsody.core.IRPClass newVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addRequiredInterface(new_val._com))

    def removeRequiredInterface(self, new_val: RPModelElement) -> None:
        """Removes a required interface from the port.

        Args:
            new_val: The class (``IRPClass``) to remove from the required interfaces.

        Raises:
            RhapsodyRuntimeException: if the required interface cannot be removed.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::removeRequiredInterface(com.telelogic.rhapsody.core.IRPClass newVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeRequiredInterface(new_val._com))

    def getContract(self) -> Any:
        """Returns the contract defined for the port.

        Deprecated:
            This method exists for backward compatibility. Use
            :meth:`getPortContract` instead.

        Returns:
            The wrapped ``IRPClass`` used as the port's contract.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::getContract()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getContract", "contract"))

    def setContract(self, contract: RPModelElement) -> None:
        """Specifies the contract to use for the port.

        Deprecated:
            This method exists for backward compatibility. Use
            :meth:`setPortContract` instead.

        Args:
            contract: The class (``IRPClass``) to use as the port's contract.

        Reference:
            com.telelogic.rhapsody.core.IRPPort::setContract(com.telelogic.rhapsody.core.IRPClass contract)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setContract", "contract", contract._com)


AbstractRPModelElement.register_wrapper("Port", RPPort)
