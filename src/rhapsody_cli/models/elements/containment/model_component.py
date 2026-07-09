"""Wraps ``com.telelogic.rhapsody.core.IRPComponent``."""

from rhapsody_cli.models.core import RPUnit, register_wrapper


class RPComponent(RPUnit):
    """Wraps ``IRPComponent``: a component that extends ``IRPUnit``."""

    pass


register_wrapper("Component", RPComponent)
