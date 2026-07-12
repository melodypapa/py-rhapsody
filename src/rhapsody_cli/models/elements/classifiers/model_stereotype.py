"""Wraps ``com.telelogic.rhapsody.core.IRPStereotype``."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPStereotype(RPClassifier):
    """Wraps ``IRPStereotype``: a stereotype that extends ``IRPClassifier``."""

    # IRPStereotype method parity checklist:
    # [ ] addMetaClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIcon  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsNewTerm  [ ] impl  [ ] docstring  [ ] test
    # [ ] getOfMetaClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] removeMetaClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsNewTerm  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPClassifier / IRPUnit / IRPModelElement methods (covered by RPClassifier / RPUnit / RPModelElement checklists)
    # No deprecated IRPStereotype methods.

    pass


AbstractRPModelElement.register_wrapper("Stereotype", RPStereotype)
