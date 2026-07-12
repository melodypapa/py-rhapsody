"""Wraps ``com.telelogic.rhapsody.core.IRPGeneralization``."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPGeneralization(RPModelElement):
    """Wraps ``IRPGeneralization``: a generalization (inheritance) relationship."""

    # IRPGeneralization method parity checklist:
    # [ ] getBaseClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] getDerivedClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] getExtensionPoint  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsVirtual  [ ] impl  [ ] docstring  [ ] test
    # [ ] getVisibility  [ ] impl  [ ] docstring  [ ] test
    # [ ] setBaseClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] setDerivedClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] setExtensionPoint  [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsVirtual  [ ] impl  [ ] docstring  [ ] test
    # [ ] setVisibility  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklists)
    # No deprecated IRPGeneralization methods.

    pass


AbstractRPModelElement.register_wrapper("Generalization", RPGeneralization)
