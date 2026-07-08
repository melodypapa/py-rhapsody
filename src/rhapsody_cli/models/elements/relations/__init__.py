"""Relations package — wrappers for IRPRelation and its subtypes."""

from rhapsody_cli.models.elements.relations.model_instance import RPInstance  # noqa: F401
from rhapsody_cli.models.elements.relations.model_relation import RPRelation  # noqa: F401

__all__ = ["RPInstance", "RPRelation"]
