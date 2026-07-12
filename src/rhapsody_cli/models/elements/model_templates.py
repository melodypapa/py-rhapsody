"""Templates model-element wrappers (auto-generated stubs)."""

from typing import Any

from rhapsody_cli.models.core import RPModelElement
from rhapsody_cli.models.elements.model_variables import RPVariable


class RPTemplateInstantiation(RPModelElement):
    """Wraps ``IRPTemplateInstantiation``."""

    # IRPTemplateInstantiation method parity checklist:
    # [ ] getTemplateInstantiationParameters [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError


class RPTemplateInstantiationParameter(RPModelElement):
    """Wraps ``IRPTemplateInstantiationParameter``."""

    # IRPTemplateInstantiationParameter method parity checklist:
    # [ ] getArgValue                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getType                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setArgValue                  [ ] impl  [ ] docstring  [ ] test
    # [ ] setType                      [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def get_type(self) -> Any:
        """Returns the type of this template instantiation parameter.

        Returns:
            The type of this template instantiation parameter.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateInstantiationParameter::getType()
        """
        raise NotImplementedError

    def set_arg_value(self, arg_value: str) -> None:
        """Sets the argument value of this template instantiation parameter.

        Args:
            arg_value: The argument value to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateInstantiationParameter::setArgValue(java.lang.String argValue)
        """
        raise NotImplementedError

    def set_type(self, type_: "RPClassifier") -> None:
        """Sets the type of this template instantiation parameter.

        Args:
            type_: The type to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateInstantiationParameter::setType(com.telelogic.rhapsody.core.IRPClassifier type)
        """
        raise NotImplementedError


class RPTemplateParameter(RPVariable):
    """Wraps ``IRPTemplateParameter``: represents parameters of a template in Rhapsody models."""

    # IRPTemplateParameter method parity checklist:
    # [ ] getParameterKind             [ ] impl  [ ] docstring  [ ] test
    # [ ] getRepresentative            [ ] impl  [ ] docstring  [ ] test
    # [ ] setClassType                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setParameterKind             [ ] impl  [ ] docstring  [ ] test
    # [ ] setRepresentative            [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def get_representative(self) -> Any:
        """Returns the representative of this template parameter.

        For internal use only.

        Returns:
            The representative model element of this template parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::getRepresentative()
        """
        raise NotImplementedError

    def set_class_type(self) -> None:
        """Sets the type of the parameter to "class".

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::setClassType()
        """
        raise NotImplementedError

    def set_parameter_kind(self, parameter_kind: str) -> None:
        """Specifies the type of the template parameter.

        Args:
            parameter_kind: The type to use for the template parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::setParameterKind(java.lang.String parameterKind)
        """
        raise NotImplementedError

    def set_representative(self, representative: "RPModelElement") -> None:
        """Sets the representative of this template parameter.

        For internal use only.

        Args:
            representative: The representative model element to set.

        Reference:
            com.telelogic.rhapsody.core.IRPTemplateParameter::setRepresentative(com.telelogic.rhapsody.core.IRPModelElement representative)
        """
        raise NotImplementedError
