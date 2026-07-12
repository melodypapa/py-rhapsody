"""Templates package — wrappers for IRPTemplateInstantiation and related types."""

from rhapsody_cli.models.elements.templates.model_templates import (  # noqa: F401
    RPTemplateInstantiation,
    RPTemplateInstantiationParameter,
    RPTemplateParameter,
)

__all__ = [
    "RPTemplateInstantiation",
    "RPTemplateInstantiationParameter",
    "RPTemplateParameter",
]
