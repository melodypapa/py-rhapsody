"""Templates model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING, Optional, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.variables.model_variables import RPVariable

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPTemplateInstantiation(RPModelElement):
    """Wraps ``IRPTemplateInstantiation``."""

    # IRPTemplateInstantiation method parity checklist:
    # [x] get_template_instantiation_parameters [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # No deprecated IRPTemplateInstantiation methods.

    def get_template_instantiation_parameters(self) -> "RPCollection":
        """Returns the template instantiation parameters of this template instantiation.

        Returns:
            A ``RPCollection`` of the template instantiation parameters.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateInstantiation::getTemplateInstantiationParameters()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getTemplateInstantiationParameters", "templateInstantiationParameters"))


class RPTemplateInstantiationParameter(RPModelElement):
    """Wraps ``IRPTemplateInstantiationParameter``."""

    # IRPTemplateInstantiationParameter method parity checklist:
    # [x] get_arg_value                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_type                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_arg_value                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_type                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # No deprecated IRPTemplateInstantiationParameter methods.

    def get_arg_value(self) -> str:
        """Returns the argument value of this template instantiation parameter.

        Returns:
            The argument value as a string.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateInstantiationParameter::getArgValue()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getArgValue", "argValue"))

    def get_type(self) -> "RPClassifier":
        """Returns the type of this template instantiation parameter.

        Returns:
            The type of this template instantiation parameter.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateInstantiationParameter::getType()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getType", "type")))

    def set_arg_value(self, arg_value: str) -> None:
        """Sets the argument value of this template instantiation parameter.

        Args:
            arg_value: The argument value to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateInstantiationParameter::setArgValue(java.lang.String argValue)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setArgValue", "argValue", arg_value)

    def set_type(self, type_: "RPClassifier") -> None:
        """Sets the type of this template instantiation parameter.

        Args:
            type_: The type to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateInstantiationParameter::setType(com.telelogic.rhapsody.core.IRPClassifier type)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setType", "type", type_._com)


class RPTemplateParameter(RPVariable):
    """Wraps ``IRPTemplateParameter``: represents parameters of a template in Rhapsody models."""

    # IRPTemplateParameter method parity checklist:
    # [x] get_parameter_kind             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_representative            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_class_type                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_parameter_kind             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_representative            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # [inherited] irp_unit methods (covered by rp_unit checklist)
    # [inherited] irp_variable methods (covered by rp_variable checklist)
    # No deprecated IRPTemplateParameter methods.

    def get_parameter_kind(self) -> str:
        """Returns the type of the template parameter.

        Returns:
            The type of the template parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::getParameterKind()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getParameterKind", "parameterKind"))

    def get_representative(self) -> Optional["RPModelElement"]:
        """Returns the representative of this template parameter.

        For internal use only.

        Returns:
            The representative model element of this template parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::getRepresentative()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getRepresentative", "representative"))

    def set_class_type(self, class_type: "RPClassifier") -> None:
        """Sets the type of the parameter to "class".

        Args:
            class_type: The classifier to set as the class type.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::setClassType(com.telelogic.rhapsody.core.IRPClassifier classType)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setClassType(class_type._com))

    def set_parameter_kind(self, parameter_kind: str) -> None:
        """Specifies the type of the template parameter.

        Args:
            parameter_kind: The type to use for the template parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::setParameterKind(java.lang.String parameterKind)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setParameterKind", "parameterKind", parameter_kind)

    def set_representative(self, representative: "RPModelElement") -> None:
        """Sets the representative of this template parameter.

        For internal use only.

        Args:
            representative: The representative model element to set.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::setRepresentative(com.telelogic.rhapsody.core.IRPModelElement representative)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRepresentative", "representative", representative._com)


AbstractRPModelElement.register_wrapper("TemplateInstantiation", RPTemplateInstantiation)
AbstractRPModelElement.register_wrapper("TemplateInstantiationParameter", RPTemplateInstantiationParameter)
AbstractRPModelElement.register_wrapper("TemplateParameter", RPTemplateParameter)
