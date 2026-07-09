"""Wraps ``com.telelogic.rhapsody.core.IRPAssociationClass``."""

from rhapsody_cli.models._core import register_wrapper
from rhapsody_cli.models.elements.classifiers.model_class import RPClass


class RPAssociationClass(RPClass):
    """Wraps ``IRPAssociationClass``: an association class that extends ``IRPClass``."""

    pass


register_wrapper("AssociationClass", RPAssociationClass)
