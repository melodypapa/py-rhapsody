"""Wraps ``com.telelogic.rhapsody.core.IRPDependency``."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPDependency(RPModelElement):
    """Wraps ``IRPDependency``: a dependency relationship."""

    # IRPDependency method parity checklist:
    # [ ] getDependent  [ ] impl  [ ] docstring  [ ] test
    # [ ] getDependsOn  [ ] impl  [ ] docstring  [ ] test
    # [ ] isNeedToMigrate  [ ] impl  [ ] docstring  [ ] test
    # [ ] setDependent  [ ] impl  [ ] docstring  [ ] test
    # [ ] setDependsOn  [ ] impl  [ ] docstring  [ ] test
    # [ ] setLinkType  [ ] impl  [ ] docstring  [ ] test
    # [ ] setOwnerWithoutChangingDependent  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklists)
    # No deprecated IRPDependency methods.

    pass


AbstractRPModelElement.register_wrapper("Dependency", RPDependency)
