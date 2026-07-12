"""Wraps ``com.telelogic.rhapsody.core.IRPHyperLink``."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.relations.model_dependency import RPDependency


class RPHyperLink(RPDependency):
    """Wraps ``IRPHyperLink``: a hyperlink that extends ``IRPDependency``."""

    # IRPHyperLink method parity checklist:
    # [deprecated] getTextToDisplay  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [deprecated] getTextToDisplayType  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [deprecated] getDisplayOption  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [ ] getTarget  [ ] impl  [ ] docstring  [ ] test
    # [ ] getURL  [ ] impl  [ ] docstring  [ ] test
    # [ ] setDisplayOption  [ ] impl  [ ] docstring  [ ] test
    # [ ] setTarget  [ ] impl  [ ] docstring  [ ] test
    # [ ] setURL  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPDependency / IRPModelElement methods (covered by RPDependency / RPModelElement checklists)
    # Deprecated IRPHyperLink methods listed above.

    pass


AbstractRPModelElement.register_wrapper("HyperLink", RPHyperLink)
