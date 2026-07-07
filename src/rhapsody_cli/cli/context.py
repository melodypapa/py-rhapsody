"""CLI session context management."""

from __future__ import annotations

from rhapsody_cli import RhapsodyApplication
from rhapsody_cli.models.elements.containment import RPProject


class RhapsodyContext:
    """Manages CLI session state: active project, output format, etc."""

    def __init__(self) -> None:
        self.app: RhapsodyApplication | None = None
        self.project: RPProject | None = None
        self.output_format: str = "table"  # table, json, csv

    def connect(self, method: str = "attach") -> RhapsodyApplication:
        """Connect to running Rhapsody or launch new instance."""
        if self.app is None:
            if method == "attach":
                self.app = RhapsodyApplication.attach()
            else:
                self.app = RhapsodyApplication.launch()
        return self.app

    def open_project(self, project_path: str) -> RPProject:
        """Open a Rhapsody project file."""
        if self.app is None:
            self.connect()
        assert self.app is not None  # For mypy type narrowing
        self.project = self.app.openProject(project_path)
        return self.project

    def create_project(self, project_location: str, project_name: str) -> RPProject:
        """Create a new empty Rhapsody project."""
        if self.app is None:
            self.connect()
        assert self.app is not None  # For mypy type narrowing
        self.project = self.app.createNewProject(project_location, project_name)
        return self.project

    def close_project(self) -> None:
        """Close active project."""
        if self.project:
            self.project.close()
            self.project = None

    def disconnect(self) -> None:
        """Disconnect from Rhapsody."""
        self.close_project()
        if self.app:
            self.app.quit()
            self.app = None
