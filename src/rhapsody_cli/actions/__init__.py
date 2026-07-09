"""Action classes for CLI subcommands (PanGu-style architecture)."""

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.element_action import (
    ElementAddAction,
    ElementDeleteAction,
    ElementQueryAction,
    ElementViewAction,
)
from rhapsody_cli.actions.project_action import (
    ProjectCloseAction,
    ProjectListAction,
    ProjectNewAction,
    ProjectOpenAction,
)

__all__ = [
    "AbstractAction",
    "ElementAddAction",
    "ElementDeleteAction",
    "ElementQueryAction",
    "ElementViewAction",
    "ProjectCloseAction",
    "ProjectListAction",
    "ProjectNewAction",
    "ProjectOpenAction",
]
