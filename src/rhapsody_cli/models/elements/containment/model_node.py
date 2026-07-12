"""Wraps ``com.telelogic.rhapsody.core.IRPNode``."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPUnit


class RPNode(RPUnit):
    """Wraps ``IRPNode``: a node that extends ``IRPUnit``."""

    # IRPNode method parity checklist:
    # [ ] addComponentInstance  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteComponentInstance  [ ] impl  [ ] docstring  [ ] test
    # [ ] findComponentInstance  [ ] impl  [ ] docstring  [ ] test
    # [ ] getCPUtype  [ ] impl  [ ] docstring  [ ] test
    # [ ] getComponentInstances  [ ] impl  [ ] docstring  [ ] test
    # [ ] setCPUtype  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPUnit / IRPModelElement methods (covered by RPUnit / RPModelElement checklists)
    # No deprecated IRPNode methods.

    pass


AbstractRPModelElement.register_wrapper("Node", RPNode)
