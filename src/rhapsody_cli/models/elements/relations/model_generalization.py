"""Wraps ``com.telelogic.rhapsody.core.IRPGeneralization``."""

from rhapsody_cli.models._core import RPModelElement, register_wrapper


class RPGeneralization(RPModelElement):
    """Wraps ``IRPGeneralization``: a generalization (inheritance) relationship."""

    pass


register_wrapper("Generalization", RPGeneralization)
