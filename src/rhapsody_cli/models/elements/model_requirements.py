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

    def addAnchor(self, target: RPModelElement) -> None:
        """Adds an anchor from the annotation to the specified model element.

        Args:
            target: The model element to anchor this annotation to.
        """
        AbstractRPModelElement.call_com(lambda: self._com.addAnchor(target._com))

    def getAnchoredByMe(self) -> RPCollection:
        """Gets the list of model elements that are anchored to the annotation.

        Returns:
            An ``RPCollection`` of the anchored model elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAnchoredByMe", "anchoredByMe"))

    def getBody(self) -> str:
        """Gets the text of the specification for the annotation.

        Returns:
            The annotation's body text.
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getBody", "body"))

    def getSpecification(self) -> str:
        """Gets the text of the specification for the annotation.

        Returns:
            The annotation's specification text.
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getSpecification", "specification"))

    def getSpecificationRTF(self) -> str:
        """Returns the specification of the annotation in RTF format.

        Returns:
            The RTF-formatted specification string.
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getSpecificationRTF", "specificationRTF"))

    def isSpecificationRTF(self) -> bool:
        """Checks whether the specification is in RTF format.

        Returns:
            ``True`` if the specification is RTF-formatted, ``False`` otherwise.
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "isSpecificationRTF", "specificationRTF"))

    def removeAnchor(self, target: RPModelElement) -> None:
        """Removes the anchor to the specified model element.

        Args:
            target: The model element to remove the anchor from.
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeAnchor(target._com))

    def setBody(self, body: str) -> None:
        """Adds a specification to the annotation.

        Args:
            body: The body text to set for the annotation.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setBody", "body", body)

    def setSpecification(self, specification: str) -> None:
        """Adds a specification to the annotation.

        Args:
            specification: The specification text to set for the annotation.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setSpecification", "specification", specification)

    def setSpecificationRTF(self, specification_rtf: str) -> None:
        """Specifies the RTF string to use for the annotation's specification.

        Args:
            specification_rtf: The RTF-formatted specification string.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setSpecificationRTF", "specificationRTF", specification_rtf)


class RPRequirement(RPAnnotation):
    """Wraps ``IRPRequirement``: represents a requirement in the model."""

    def getRequirementID(self) -> str:
        """Gets the unique identifier for the requirement.

        Returns:
            The requirement ID string.
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRequirementID", "requirementID"))

    def setRequirementID(self, requirement_id: str) -> None:
        """Sets the unique identifier for the requirement.

        Args:
            requirement_id: The new requirement ID to set.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRequirementID", "requirementID", requirement_id)


AbstractRPModelElement.register_wrapper("Requirement", RPRequirement)
