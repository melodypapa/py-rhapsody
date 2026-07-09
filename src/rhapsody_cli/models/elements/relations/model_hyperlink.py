"""Wraps ``com.telelogic.rhapsody.core.IRPHyperLink``."""

from rhapsody_cli.models._core import register_wrapper
from rhapsody_cli.models.elements.relations.model_dependency import RPDependency


class RPHyperLink(RPDependency):
    """Wraps ``IRPHyperLink``: a hyperlink that extends ``IRPDependency``."""

    pass


register_wrapper("HyperLink", RPHyperLink)
