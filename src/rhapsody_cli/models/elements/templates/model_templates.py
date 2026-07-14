"""Templates model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.variables.model_variables import RPVariable

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPTemplateInstantiation(RPModelElement):
    """Wraps ``IRPTemplateInstantiation``."""

    # IRPTemplateInstantiation method parity checklist:
    # [ ] getTemplateInstantiationParameters [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
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
    # [ ] getArgValue                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getType                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setArgValue                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setType                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
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
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getType", "type"))

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
    # [ ] getParameterKind             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getRepresentative            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setClassType                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setParameterKind             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setRepresentative            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # [inherited] IRPVariable methods (covered by RPVariable checklist)
    # No deprecated IRPTemplateParameter methods.

    def get_parameter_kind(self) -> str:
        """Returns the type of the template parameter.

        Returns:
            The type of the template parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::getParameterKind()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getParameterKind", "parameterKind"))

    def get_representative(self) -> "RPModelElement":
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
