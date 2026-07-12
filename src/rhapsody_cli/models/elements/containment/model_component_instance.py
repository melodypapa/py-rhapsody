"""Wraps ``com.telelogic.rhapsody.core.IRPComponentInstance``."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPComponentInstance(RPInstance):
    """Wraps ``IRPComponentInstance``: a component instance that extends ``IRPInstance``."""

    # IRPComponentInstance method parity checklist:
    # [ ] getComponentType  [ ] impl  [ ] docstring  [ ] test
    # [ ] getNode  [ ] impl  [ ] docstring  [ ] test
    # [ ] setComponentType  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPInstance / IRPRelation / IRPUnit / IRPModelElement methods (covered by RPInstance / RPRelation / RPUnit / RPModelElement checklists)
    # No deprecated IRPComponentInstance methods.

    pass


AbstractRPModelElement.register_wrapper("ComponentInstance", RPComponentInstance)
