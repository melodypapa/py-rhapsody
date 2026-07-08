"""Containment package — wrappers for IRPPackage and IRPProject."""

from rhapsody_cli.models.elements.containment.model_package import RPPackage  # noqa: F401
from rhapsody_cli.models.elements.containment.model_project import RPProject  # noqa: F401

__all__ = ["RPPackage", "RPProject"]
