"""Wraps ``com.telelogic.rhapsody.core.IRPAssociationClass``."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers.model_class import RPClass


class RPAssociationClass(RPClass):
    """Wraps ``IRPAssociationClass``: an association class that extends ``IRPClass``."""

    # IRPAssociationClass method parity checklist:
    # [ ] getEnd1  [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd2  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsClass  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPClass / IRPClassifier / IRPUnit / IRPModelElement methods (covered by RPClass / RPClassifier / RPUnit / RPModelElement checklists)
    # No deprecated IRPAssociationClass methods.

    pass


AbstractRPModelElement.register_wrapper("AssociationClass", RPAssociationClass)
