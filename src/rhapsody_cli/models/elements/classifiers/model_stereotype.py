"""Wraps ``com.telelogic.rhapsody.core.IRPStereotype``."""

from rhapsody_cli.models._core import register_wrapper
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPStereotype(RPClassifier):
    """Wraps ``IRPStereotype``: a stereotype that extends ``IRPClassifier``."""

    pass


register_wrapper("Stereotype", RPStereotype)
