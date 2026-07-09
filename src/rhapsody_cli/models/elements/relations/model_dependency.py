"""Wraps ``com.telelogic.rhapsody.core.IRPDependency``."""

from rhapsody_cli.models._core import RPModelElement, register_wrapper


class RPDependency(RPModelElement):
    """Wraps ``IRPDependency``: a dependency relationship."""

    pass


register_wrapper("Dependency", RPDependency)
