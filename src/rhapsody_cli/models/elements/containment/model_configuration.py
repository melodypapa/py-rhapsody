"""Wraps ``com.telelogic.rhapsody.core.IRPConfiguration``."""

from rhapsody_cli.models._core import RPUnit, register_wrapper


class RPConfiguration(RPUnit):
    """Wraps ``IRPConfiguration``: a configuration that extends ``IRPUnit``."""

    pass


register_wrapper("Configuration", RPConfiguration)
