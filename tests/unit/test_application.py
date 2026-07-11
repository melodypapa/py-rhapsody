"""Tests for rhapsody_cli.application.RhapsodyApplication."""

from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError
from rhapsody_cli.models.elements.containment import RPProject
from tests.unit.models.fakes import make_com_error, make_fake_collection, make_fake_element


@patch("rhapsody_cli.application.win32com.client.GetActiveObject")
def test_attach_wraps_active_com_object(mock_get_active_object: MagicMock) -> None:
    fake_app = MagicMock(name="FakeApplication")
    mock_get_active_object.return_value = fake_app

    app = RhapsodyApplication.attach()

    mock_get_active_object.assert_called_once_with("Rhapsody2.Application.1")
    assert app._com is fake_app


@patch("rhapsody_cli.application.win32com.client.GetActiveObject")
def test_attach_raises_connection_error_when_none_running(
    mock_get_active_object: MagicMock,
) -> None:
    mock_get_active_object.side_effect = make_com_error("no running instance")

    with pytest.raises(RhapsodyConnectionError):
        RhapsodyApplication.attach()


@patch("rhapsody_cli.application.win32com.client.Dispatch")
def test_launch_wraps_new_com_object(mock_dispatch: MagicMock) -> None:
    fake_app = MagicMock(name="FakeApplication")
    mock_dispatch.return_value = fake_app

    app = RhapsodyApplication.launch()

    mock_dispatch.assert_called_once_with("Rhapsody2.Application.1")
    assert app._com is fake_app


@patch("rhapsody_cli.application.win32com.client.Dispatch")
def test_launch_raises_connection_error_when_dispatch_fails(
    mock_dispatch: MagicMock,
) -> None:
    mock_dispatch.side_effect = make_com_error("launch failed")

    with pytest.raises(RhapsodyConnectionError):
        RhapsodyApplication.launch()


@patch("rhapsody_cli.application.win32com.client.Dispatch")
@patch("rhapsody_cli.application.win32com.client.GetActiveObject")
def test_connect_prefers_attach_when_available(mock_get_active_object: MagicMock, mock_dispatch: MagicMock) -> None:
    fake_app = MagicMock(name="FakeApplication")
    mock_get_active_object.return_value = fake_app

    app = RhapsodyApplication.connect()

    mock_get_active_object.assert_called_once_with("Rhapsody2.Application.1")
    mock_dispatch.assert_not_called()
    assert app._com is fake_app


@patch("rhapsody_cli.application.win32com.client.Dispatch")
@patch("rhapsody_cli.application.win32com.client.GetActiveObject")
def test_connect_falls_back_to_launch_when_attach_fails(mock_get_active_object: MagicMock, mock_dispatch: MagicMock) -> None:
    mock_get_active_object.side_effect = make_com_error("no running instance")
    fake_app = MagicMock(name="FakeApplication")
    mock_dispatch.return_value = fake_app

    app = RhapsodyApplication.connect()

    mock_dispatch.assert_called_once_with("Rhapsody2.Application.1")
    assert app._com is fake_app


@patch("rhapsody_cli.application.win32com.client.Dispatch")
@patch("rhapsody_cli.application.win32com.client.GetActiveObject")
def test_connect_raises_connection_error_when_launch_fails(mock_get_active_object: MagicMock, mock_dispatch: MagicMock) -> None:
    mock_get_active_object.side_effect = make_com_error("no running instance")
    mock_dispatch.side_effect = make_com_error("launch failed")

    with pytest.raises(RhapsodyConnectionError):
        RhapsodyApplication.connect()


def test_open_project_wraps_result_as_rpproject() -> None:
    fake_app = MagicMock(name="FakeApplication")
    fake_project = make_fake_element("Project", getName="MyProject")
    fake_app.openProject.return_value = fake_project
    app = RhapsodyApplication(fake_app)

    project = app.openProject("C:/models/MyProject.rpy")

    fake_app.openProject.assert_called_once_with("C:/models/MyProject.rpy")
    assert isinstance(project, RPProject)
    assert project.getName() == "MyProject"


def test_active_project_wraps_result_as_rpproject() -> None:
    fake_app = MagicMock(name="FakeApplication")
    fake_project = make_fake_element("Project", getName="ActiveOne")
    fake_app.activeProject.return_value = fake_project
    app = RhapsodyApplication(fake_app)

    project = app.activeProject()

    assert isinstance(project, RPProject)
    assert project.getName() == "ActiveOne"


def test_get_projects_returns_collection_of_rpproject() -> None:
    fake_app = MagicMock(name="FakeApplication")
    fake_project = make_fake_element("Project", getName="P1")
    fake_app.getProjects.return_value = make_fake_collection([fake_project])
    app = RhapsodyApplication(fake_app)

    projects = app.getProjects()

    assert len(projects) == 1
    assert isinstance(projects[0], RPProject)
    assert projects[0].getName() == "P1"


def test_get_projects_falls_back_to_projects_property_when_method_missing() -> None:
    """Some Rhapsody COM Prog IDs (e.g. Rhapsody2.Application.1) expose the
    projects collection via the bare 'projects' property instead of a
    getProjects() method."""
    fake_project = make_fake_element("Project", getName="P1")
    fake_app = MagicMock(spec=["projects"])
    fake_app.projects = make_fake_collection([fake_project])
    app = RhapsodyApplication(fake_app)

    projects = app.getProjects()

    assert len(projects) == 1
    assert isinstance(projects[0], RPProject)
    assert projects[0].getName() == "P1"


def test_create_new_project_calls_com_and_returns_active_project() -> None:
    fake_app = MagicMock(name="FakeApplication")
    fake_project = make_fake_element("Project", getName="NewProject")
    fake_app.activeProject.return_value = fake_project
    app = RhapsodyApplication(fake_app)

    project = app.createNewProject("C:/models", "NewProject")

    fake_app.createNewProject.assert_called_once_with("C:/models", "NewProject")
    fake_app.activeProject.assert_called_once_with()
    assert isinstance(project, RPProject)
    assert project.getName() == "NewProject"


def test_quit_delegates_to_com() -> None:
    fake_app = MagicMock(name="FakeApplication")
    app = RhapsodyApplication(fake_app)

    app.quit()

    fake_app.quit.assert_called_once_with()


def test_get_is_hidden_ui_calls_method_when_present() -> None:
    fake_app = MagicMock(name="FakeApplication")
    fake_app.getIsHiddenUI.return_value = 1
    app = RhapsodyApplication(fake_app)

    result = app.getIsHiddenUI()

    fake_app.getIsHiddenUI.assert_called_once_with()
    assert result is True


def test_get_is_hidden_ui_falls_back_to_property_when_method_missing() -> None:
    fake_app = MagicMock(spec=["isHiddenUI"])
    fake_app.isHiddenUI = 0
    app = RhapsodyApplication(fake_app)

    result = app.getIsHiddenUI()

    assert result is False


def test_set_hidden_ui_calls_method_when_present() -> None:
    fake_app = MagicMock(name="FakeApplication")
    app = RhapsodyApplication(fake_app)

    app.setHiddenUI(False)

    fake_app.setHiddenUI.assert_called_once_with(False)


def test_set_hidden_ui_falls_back_to_property_when_method_missing() -> None:
    fake_app = MagicMock(spec=["isHiddenUI"])
    app = RhapsodyApplication(fake_app)

    app.setHiddenUI(False)

    assert fake_app.isHiddenUI is False


def test_bring_window_to_top_delegates_to_com() -> None:
    fake_app = MagicMock(name="FakeApplication")
    app = RhapsodyApplication(fake_app)

    app.bringWindowToTop()

    fake_app.bringWindowToTop.assert_called_once_with()
