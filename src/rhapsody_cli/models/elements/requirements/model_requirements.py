"""Requirement-family wrappers: mirrors IRPAnnotation and IRPRequirement
from com.telelogic.rhapsody.core.
"""

from rhapsody_cli.models.core import (
    AbstractRPModelElement,
    RPCollection,
    RPModelElement,
    RPUnit,
)


class RPAnnotation(RPUnit):
    """Wraps ``IRPAnnotation``: the base interface for free-text annotation
    elements (such as requirements and notes) that can be anchored to other
    model elements.
    """

    # IRPAnnotation method parity checklist:
    # [x] add_anchor  [x] impl  [x] docstring  [x] test
    # [x] get_anchored_by_me  [x] impl  [x] docstring  [x] test
    # [x] get_body  [x] impl  [x] docstring  [x] test
    # [x] get_specification  [x] impl  [x] docstring  [x] test
    # [x] get_specification_rtf  [x] impl  [x] docstring  [x] test
    # [x] is_specification_rtf  [x] impl  [x] docstring  [x] test
    # [x] remove_anchor  [x] impl  [x] docstring  [x] test
    # [x] set_body  [x] impl  [x] docstring  [x] test
    # [x] set_specification  [x] impl  [x] docstring  [x] test
    # [x] set_specification_rtf  [x] impl  [x] docstring  [x] test
    # [inherited] IRPUnit / IRPModelElement methods (covered by RPUnit / RPModelElement checklists)
    # No deprecated IRPAnnotation methods.

    def add_anchor(self, target: RPModelElement) -> None:
        """Adds an anchor from the annotation to the specified model element.

        Args:
            target: The model element to anchor this annotation to.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::addAnchor(com.telelogic.rhapsody.core.IRPModelElement target)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addAnchor(target._com))

    def get_anchored_by_me(self) -> RPCollection:
        """Gets the list of model elements that are anchored to the annotation.

        Returns:
            An ``RPCollection`` of the anchored model elements.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::getAnchoredByMe()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAnchoredByMe", "anchoredByMe"))

    def get_body(self) -> str:
        """Gets the text of the specification for the annotation.

        Returns:
            The annotation's body text.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::getBody()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getBody", "body"))

    def get_specification(self) -> str:
        """Gets the text of the specification for the annotation.

        Returns:
            The annotation's specification text.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::getSpecification()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getSpecification", "specification"))

    def get_specification_rtf(self) -> str:
        """Returns the specification of the annotation in RTF format.

        Returns:
            The RTF-formatted specification string.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::getSpecificationRTF()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getSpecificationRTF", "specificationRTF"))

    def is_specification_rtf(self) -> bool:
        """Checks whether the specification is in RTF format.

        Returns:
            ``True`` if the specification is RTF-formatted, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::isSpecificationRTF()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "isSpecificationRTF", "specificationRTF"))

    def remove_anchor(self, target: RPModelElement) -> None:
        """Removes the anchor to the specified model element.

        Args:
            target: The model element to remove the anchor from.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::removeAnchor(com.telelogic.rhapsody.core.IRPModelElement target)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeAnchor(target._com))

    def set_body(self, body: str) -> None:
        """Adds a specification to the annotation.

        Args:
            body: The body text to set for the annotation.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::setBody(java.lang.String body)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setBody", "body", body)

    def set_specification(self, specification: str) -> None:
        """Adds a specification to the annotation.

        Args:
            specification: The specification text to set for the annotation.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::setSpecification(java.lang.String specification)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setSpecification", "specification", specification)

    def set_specification_rtf(self, specification_rtf: str) -> None:
        """Specifies the RTF string to use for the specification of the annotation.

        Args:
            specification_rtf: The RTF-formatted specification string.

        Reference:
            com.telelogic.rhapsody.core.IRPAnnotation::setSpecificationRTF(java.lang.String specificationRTF)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setSpecificationRTF", "specificationRTF", specification_rtf)


class RPRequirement(RPAnnotation):
    """Wraps ``IRPRequirement``: represents a requirement in the model."""

    # IRPRequirement method parity checklist:
    # [x] get_requirement_id  [x] impl  [x] docstring  [x] test
    # [x] set_requirement_id  [x] impl  [x] docstring  [x] test
    # [inherited] IRPAnnotation / IRPUnit / IRPModelElement methods (covered by RPAnnotation / RPUnit / RPModelElement checklists)
    # No deprecated IRPRequirement methods.

    def get_requirement_id(self) -> str:
        """Returns the ID that was set for the requirement.

        Returns:
            The requirement ID string.

        Reference:
            com.telelogic.rhapsody.core.IRPRequirement::getRequirementID()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRequirementID", "requirementID"))

    def set_requirement_id(self, requirement_id: str) -> None:
        """Sets the ID for the requirement.

        Args:
            requirement_id: The new requirement ID to set.

        Reference:
            com.telelogic.rhapsody.core.IRPRequirement::setRequirementID(java.lang.String requirementID)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRequirementID", "requirementID", requirement_id)


AbstractRPModelElement.register_wrapper("Requirement", RPRequirement)
