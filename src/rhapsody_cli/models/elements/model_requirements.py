"""Requirement-family wrappers: mirrors IRPAnnotation and IRPRequirement
from com.telelogic.rhapsody.core.
"""

from rhapsody_cli.models.core import (
    RPCollection,
    RPModelElement,
    RPUnit,
    call_com,
    register_wrapper,
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
        call_com(lambda: self._com.addAnchor(target._com))

    def getAnchoredByMe(self) -> RPCollection:
        """Gets the list of model elements that are anchored to the annotation.

        Returns:
            An ``RPCollection`` of the anchored model elements.
        """
        return RPCollection(call_com(lambda: self._com.getAnchoredByMe()))

    def getBody(self) -> str:
        """Gets the text of the specification for the annotation.

        Returns:
            The annotation's body text.
        """
        return call_com(lambda: str(self._com.getBody()))

    def getSpecification(self) -> str:
        """Gets the text of the specification for the annotation.

        Returns:
            The annotation's specification text.
        """
        return call_com(lambda: str(self._com.getSpecification()))

    def getSpecificationRTF(self) -> str:
        """Returns the specification of the annotation in RTF format.

        Returns:
            The RTF-formatted specification string.
        """
        return call_com(lambda: str(self._com.getSpecificationRTF()))

    def isSpecificationRTF(self) -> bool:
        """Checks whether the specification is in RTF format.

        Returns:
            ``True`` if the specification is RTF-formatted, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.isSpecificationRTF()))

    def removeAnchor(self, target: RPModelElement) -> None:
        """Removes the anchor to the specified model element.

        Args:
            target: The model element to remove the anchor from.
        """
        call_com(lambda: self._com.removeAnchor(target._com))

    def setBody(self, body: str) -> None:
        """Adds a specification to the annotation.

        Args:
            body: The body text to set for the annotation.
        """
        call_com(lambda: self._com.setBody(body))

    def setSpecification(self, specification: str) -> None:
        """Adds a specification to the annotation.

        Args:
            specification: The specification text to set for the annotation.
        """
        call_com(lambda: self._com.setSpecification(specification))

    def setSpecificationRTF(self, specification_rtf: str) -> None:
        """Specifies the RTF string to use for the annotation's specification.

        Args:
            specification_rtf: The RTF-formatted specification string.
        """
        call_com(lambda: self._com.setSpecificationRTF(specification_rtf))


class RPRequirement(RPAnnotation):
    """Wraps ``IRPRequirement``: represents a requirement in the model."""

    def getRequirementID(self) -> str:
        """Gets the unique identifier for the requirement.

        Returns:
            The requirement ID string.
        """
        return call_com(lambda: str(self._com.getRequirementID()))

    def setRequirementID(self, requirement_id: str) -> None:
        """Sets the unique identifier for the requirement.

        Args:
            requirement_id: The new requirement ID to set.
        """
        call_com(lambda: self._com.setRequirementID(requirement_id))


register_wrapper("Requirement", RPRequirement)
