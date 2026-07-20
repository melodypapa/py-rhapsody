"""Tests for project actions.

UTS_XCH_00086: project export action writes YAML file
UTS_XCH_00087: project import action reads YAML and imports into project
"""

from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.project_action import ProjectExportAction, ProjectImportAction
from rhapsody_cli.exceptions import CliExecutionError


class TestProjectExportAction:
    """UTS_XCH_00086: project export action writes YAML file."""

    @patch("rhapsody_cli.actions.project_action.RhapsodyYaml")
    @patch("rhapsody_cli.actions.project_action.RhapsodyExporter")
    def test_export_writes_yaml_file(self, mock_exporter_cls: MagicMock, mock_yaml_cls: MagicMock) -> None:
        action = ProjectExportAction()
        fake_app = MagicMock(name="FakeApplication")
        fake_project = MagicMock(name="FakeProject")
        fake_app.active_project.return_value = fake_project

        mock_exporter = MagicMock()
        mock_exporter_cls.return_value = mock_exporter
        mock_exporter.export.return_value = {"version": 1, "project": "P", "rhapsody-model": []}

        args = MagicMock()
        args.file = "output.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app):
            action.execute(args)

        mock_exporter_cls.assert_called_once_with(app=fake_app)
        mock_exporter.export.assert_called_once_with(fake_project)
        mock_yaml_cls.assert_called_once()
        mock_yaml_cls.return_value.write.assert_called_once_with("output.yaml", {"version": 1, "project": "P", "rhapsody-model": []})

    @patch("rhapsody_cli.actions.project_action.RhapsodyYaml")
    @patch("rhapsody_cli.actions.project_action.RhapsodyExporter")
    def test_export_raises_on_connection_failure(self, mock_exporter_cls: MagicMock, mock_yaml_cls: MagicMock) -> None:
        action = ProjectExportAction()

        args = MagicMock()
        args.file = "output.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", side_effect=Exception("connection failed")):
            with pytest.raises(CliExecutionError):
                action.execute(args)


class TestProjectImportAction:
    """UTS_XCH_00087: project import action reads YAML and imports into project."""

    @patch("rhapsody_cli.actions.project_action.RhapsodyImporter")
    @patch("rhapsody_cli.actions.project_action.RhapsodyYaml")
    def test_import_reads_yaml_and_calls_import_template(self, mock_yaml_cls: MagicMock, mock_importer_cls: MagicMock) -> None:
        action = ProjectImportAction()
        fake_app = MagicMock(name="FakeApplication")
        fake_project = MagicMock(name="FakeProject")
        fake_app.active_project.return_value = fake_project

        mock_yaml = MagicMock()
        mock_yaml_cls.return_value = mock_yaml
        mock_yaml.read.return_value = {"version": 1, "project": "P", "rhapsody-model": []}

        mock_importer = MagicMock()
        mock_importer_cls.return_value = mock_importer

        args = MagicMock()
        args.file = "input.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app):
            action.execute(args)

        mock_yaml.read.assert_called_once_with("input.yaml")
        mock_importer_cls.assert_called_once_with(app=fake_app)
        mock_importer.import_template.assert_called_once_with({"version": 1, "project": "P", "rhapsody-model": []}, fake_project)
        fake_app.save_all.assert_called_once()

    @patch("rhapsody_cli.actions.project_action.RhapsodyImporter")
    @patch("rhapsody_cli.actions.project_action.RhapsodyYaml")
    def test_import_raises_on_yaml_read_failure(self, mock_yaml_cls: MagicMock, mock_importer_cls: MagicMock) -> None:
        action = ProjectImportAction()
        fake_app = MagicMock(name="FakeApplication")
        fake_app.active_project.return_value = MagicMock()

        mock_yaml = MagicMock()
        mock_yaml_cls.return_value = mock_yaml
        mock_yaml.read.side_effect = CliExecutionError("file not found")

        args = MagicMock()
        args.file = "missing.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app):
            with pytest.raises(CliExecutionError, match="file not found"):
                action.execute(args)
