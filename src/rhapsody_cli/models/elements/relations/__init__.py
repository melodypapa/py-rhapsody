"""Relations package — wrappers for IRPRelation and its subtypes."""

from rhapsody_cli.models.elements.relations.model_association_role import (  # noqa: F401
    RPAssociationRole,
)
from rhapsody_cli.models.elements.relations.model_dependency import RPDependency  # noqa: F401
from rhapsody_cli.models.elements.relations.model_generalization import (  # noqa: F401
    RPGeneralization,
)
from rhapsody_cli.models.elements.relations.model_hyperlink import RPHyperLink  # noqa: F401
from rhapsody_cli.models.elements.relations.model_instance import RPInstance  # noqa: F401
from rhapsody_cli.models.elements.relations.model_relation import RPRelation  # noqa: F401

__all__ = [
    "RPAssociationRole",
    "RPDependency",
    "RPGeneralization",
    "RPHyperLink",
    "RPInstance",
    "RPRelation",
]
