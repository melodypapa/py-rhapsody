"""Values model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING, Optional, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPInstanceSlot(RPModelElement):
    """Wraps ``IRPInstanceSlot``."""

    # IRPInstanceSlot method parity checklist:
    # [x] add_element_value              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_string_value               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_slot_property              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_values                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_slot_property              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # No deprecated IRPInstanceSlot methods.

    def add_element_value(self, val: "RPModelElement") -> "RPInstanceValue":
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
        return cast("RPInstanceValue", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addElementValue(val._com))))

    def add_string_value(self, val: str) -> "RPLiteralSpecification":
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
        return cast("RPLiteralSpecification", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addStringValue(val))))

    def get_slot_property(self) -> Optional["RPModelElement"]:
        """Returns the slot property of this instance slot.

        Returns:
            The slot property of this instance slot, or None if not set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSlot::getSlotProperty()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getSlotProperty()))

    def get_values(self) -> "RPCollection":
        """Returns the values of this instance slot.

        Returns:
            A ``RPCollection`` of the values of this instance slot.

        Raises:
            RhapsodyRuntimeException: If the values cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSlot::getValues()
        """
        return RPCollection(self.call_com(lambda: self._com.getValues()))

    def set_slot_property(self, slot_property: "RPModelElement") -> None:
        """Sets the slot property of this instance slot.

        Args:
            slot_property: The slot property to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSlot::setSlotProperty(com.telelogic.rhapsody.core.IRPModelElement slotProperty)
        """
        self.call_com(lambda: self._com.setSlotProperty(slot_property._com))


class RPInstanceSpecification(RPModelElement):
    """Wraps ``IRPInstanceSpecification``."""

    # IRPInstanceSpecification method parity checklist:
    # [x] add_instance_slot              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_classifier                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_instance_slots             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] is_root_instance_specification  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] populate_slots                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_classifier                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # No deprecated IRPInstanceSpecification methods.

    def add_instance_slot(self, name: str, slot_property: "RPModelElement") -> "RPInstanceSlot":
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
        return cast("RPInstanceSlot", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addInstanceSlot(name, slot_property._com))))

    def get_classifier(self) -> "RPClassifier":
        """Returns the classifier of this instance specification.

        Returns:
            The classifier of this instance specification.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::getClassifier()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getClassifier())))

    def get_instance_slots(self) -> "RPCollection":
        """Returns the instance slots of this instance specification.

        Returns:
            A ``RPCollection`` of the instance slots of this instance specification.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::getInstanceSlots()
        """
        return RPCollection(self.call_com(lambda: self._com.getInstanceSlots()))

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
        return int(self.call_com(lambda: self._com.isRootInstanceSpecification()))

    def populate_slots(self) -> None:
        """Populates the slots of this instance specification.

        Raises:
            RhapsodyRuntimeException: If the slots cannot be populated.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::populateSlots()
        """
        self.call_com(lambda: self._com.populateSlots())

    def set_classifier(self, classifier: "RPClassifier") -> None:
        """Sets the classifier of this instance specification.

        Args:
            classifier: The classifier to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceSpecification::setClassifier(com.telelogic.rhapsody.core.IRPClassifier classifier)
        """
        self.call_com(lambda: self._com.setClassifier(classifier._com))


class RPValueSpecification(RPModelElement):
    """Wraps ``IRPValueSpecification``: represents the UML concept of "value specification".

    Serves as the base interface for IRPContextSpecification,
    IRPInstanceValue, and IRPLiteralSpecification.
    """

    # IRPValueSpecification method parity checklist:
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # No deprecated IRPValueSpecification methods.

    pass


class RPInstanceValue(RPValueSpecification):
    """Wraps ``IRPInstanceValue``: used in contexts where a single model element must be stored."""

    # IRPInstanceValue method parity checklist:
    # [x] get_value                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_value                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # [inherited] irp_value_specification methods (covered by rp_value_specification checklist)
    # No deprecated IRPInstanceValue methods.

    def get_value(self) -> Optional["RPModelElement"]:
        """Returns the stored value.

        Returns:
            The stored model element value, or None if not set.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceValue::getValue()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getValue()))

    def set_value(self, value: "RPModelElement") -> None:
        """Sets the value to store.

        Args:
            value: The model element to store as the value.

        Reference:
            com.telelogic.rhapsody.core.IRPInstanceValue::setValue(com.telelogic.rhapsody.core.IRPModelElement value)
        """
        self.call_com(lambda: self._com.setValue(value._com))


class RPLiteralSpecification(RPValueSpecification):
    """Wraps ``IRPLiteralSpecification``: used in contexts where a single value must be stored."""

    # IRPLiteralSpecification method parity checklist:
    # [x] get_value                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_value                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # [inherited] irp_value_specification methods (covered by rp_value_specification checklist)
    # No deprecated IRPLiteralSpecification methods.

    def get_value(self) -> str:
        """Returns the stored value.

        Returns:
            The stored value as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPLiteralSpecification::getValue()
        """
        return str(self._get_method_or_property(self._com, "getValue", "value"))

    def set_value(self, value: str) -> None:
        """Sets the value to store.

        Args:
            value: The value to store.

        Reference:
            com.telelogic.rhapsody.core.IRPLiteralSpecification::setValue(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setValue", "value", value)


AbstractRPModelElement.register_wrapper("InstanceSlot", RPInstanceSlot)
AbstractRPModelElement.register_wrapper("InstanceSpecification", RPInstanceSpecification)
AbstractRPModelElement.register_wrapper("ValueSpecification", RPValueSpecification)
AbstractRPModelElement.register_wrapper("InstanceValue", RPInstanceValue)
AbstractRPModelElement.register_wrapper("LiteralSpecification", RPLiteralSpecification)
