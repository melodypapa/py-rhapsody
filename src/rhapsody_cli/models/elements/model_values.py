"""Values model-element wrappers (auto-generated stubs)."""

from typing import Any

from rhapsody_cli.models.core import RPModelElement


class RPInstanceSlot(RPModelElement):
    """Wraps ``IRPInstanceSlot``."""

    # IRPInstanceSlot method parity checklist:
    # [ ] addElementValue              [ ] impl  [ ] docstring  [ ] test
    # [ ] addStringValue               [ ] impl  [ ] docstring  [ ] test
    # [ ] getSlotProperty              [ ] impl  [ ] docstring  [ ] test
    # [ ] getValues                    [ ] impl  [ ] docstring  [ ] test
    # [ ] setSlotProperty              [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPInstanceSlot methods.

    def add_element_value(self, val: "RPModelElement") -> Any:
        """Adds an element value to this instance slot.

        Args:
            val: The model element value to add.

        Returns:
            The ``IRPInstanceValue`` that was created for the element value.

        Raises:
            RhapsodyRuntimeException: If the value cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSlot::addElementValue(com.telelogic.rhapsody.core.IRPModelElement val)
        """
        raise NotImplementedError

    def add_string_value(self, val: str) -> Any:
        """Adds a string value to this instance slot.

        Args:
            val: The string value to add.

        Returns:
            The ``IRPLiteralSpecification`` that was created for the string value.

        Raises:
            RhapsodyRuntimeException: If the value cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSlot::addStringValue(java.lang.String val)
        """
        raise NotImplementedError

    def get_slot_property(self) -> Any:
        """Returns the slot property of this instance slot.

        Returns:
            The slot property of this instance slot.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSlot::getSlotProperty()
        """
        raise NotImplementedError

    def get_values(self) -> "RPCollection":
        """Returns the values of this instance slot.

        Returns:
            A ``RPCollection`` of the values of this instance slot.

        Raises:
            RhapsodyRuntimeException: If the values cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSlot::getValues()
        """
        raise NotImplementedError

    def set_slot_property(self, slot_property: "RPModelElement") -> None:
        """Sets the slot property of this instance slot.

        Args:
            slot_property: The slot property to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSlot::setSlotProperty(com.telelogic.rhapsody.core.IRPModelElement slotProperty)
        """
        raise NotImplementedError


class RPInstanceSpecification(RPModelElement):
    """Wraps ``IRPInstanceSpecification``."""

    # IRPInstanceSpecification method parity checklist:
    # [ ] addInstanceSlot              [ ] impl  [ ] docstring  [ ] test
    # [ ] getClassifier                [ ] impl  [ ] docstring  [ ] test
    # [ ] getInstanceSlots             [ ] impl  [ ] docstring  [ ] test
    # [ ] isRootInstanceSpecification  [ ] impl  [ ] docstring  [ ] test
    # [ ] populateSlots                [ ] impl  [ ] docstring  [ ] test
    # [ ] setClassifier                [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPInstanceSpecification methods.

    def add_instance_slot(self, name: str, slot_property: "RPModelElement") -> Any:
        """Adds a new instance slot for the specified property of the classifier.

        Args:
            name: The name to use for the new instance slot.
            slot_property: The property of the classifier that a slot should be
                created for.

        Returns:
            The instance slot that was created.

        Raises:
            RhapsodyRuntimeException: If the slot cannot be created.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::addInstanceSlot(java.lang.String name, com.telelogic.rhapsody.core.IRPModelElement slotProperty)
        """
        raise NotImplementedError

    def get_classifier(self) -> Any:
        """Returns the classifier of this instance specification.

        Returns:
            The classifier of this instance specification.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::getClassifier()
        """
        raise NotImplementedError

    def get_instance_slots(self) -> "RPCollection":
        """Returns the instance slots of this instance specification.

        Returns:
            A ``RPCollection`` of the instance slots of this instance specification.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::getInstanceSlots()
        """
        raise NotImplementedError

    def is_root_instance_specification(self) -> int:
        """Checks whether the instance specification is a root instance specification.

        A root instance specification is any instance specification that is not a
        nested instance specification.

        Returns:
            1 if the instance specification is a root instance specification,
            0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::isRootInstanceSpecification()
        """
        raise NotImplementedError

    def populate_slots(self) -> None:
        """Populates the slots of this instance specification.

        Raises:
            RhapsodyRuntimeException: If the slots cannot be populated.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::populateSlots()
        """
        raise NotImplementedError

    def set_classifier(self, classifier: "RPClassifier") -> None:
        """Sets the classifier of this instance specification.

        Args:
            classifier: The classifier to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::setClassifier(com.telelogic.rhapsody.core.IRPClassifier classifier)
        """
        raise NotImplementedError


class RPValueSpecification(RPModelElement):
    """Wraps ``IRPValueSpecification``: represents the UML concept of "value specification" and serves as the base interface for IRPContextSpecification, IRPInstanceValue, and IRPLiteralSpecification."""

    # IRPValueSpecification method parity checklist:
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPValueSpecification methods.

    pass


class RPInstanceValue(RPValueSpecification):
    """Wraps ``IRPInstanceValue``: used in contexts where a single model element must be stored."""

    # IRPInstanceValue method parity checklist:
    # [ ] getValue                     [ ] impl  [ ] docstring  [ ] test
    # [ ] setValue                     [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPValueSpecification methods (covered by RPValueSpecification checklist)
    # No deprecated IRPInstanceValue methods.

    def get_value(self) -> Any:
        """Returns the stored value.

        Returns:
            The stored model element value.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceValue::getValue()
        """
        raise NotImplementedError

    def set_value(self, value: "RPModelElement") -> None:
        """Sets the value to store.

        Args:
            value: The model element to store as the value.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceValue::setValue(com.telelogic.rhapsody.core.IRPModelElement value)
        """
        raise NotImplementedError


class RPLiteralSpecification(RPValueSpecification):
    """Wraps ``IRPLiteralSpecification``: used in contexts where a single value must be stored."""

    # IRPLiteralSpecification method parity checklist:
    # [ ] getValue                     [ ] impl  [ ] docstring  [ ] test
    # [ ] setValue                     [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPValueSpecification methods (covered by RPValueSpecification checklist)
    # No deprecated IRPLiteralSpecification methods.

    def get_value(self) -> str:
        """Returns the stored value.

        Returns:
            The stored value as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPLiteralSpecification::getValue()
        """
        raise NotImplementedError

    def set_value(self, value: str) -> None:
        """Sets the value to store.

        Args:
            value: The value to store.

        Reference:
            com.telelogic.rhapsody.core.IRPLiteralSpecification::setValue(java.lang.String value)
        """
        raise NotImplementedError
