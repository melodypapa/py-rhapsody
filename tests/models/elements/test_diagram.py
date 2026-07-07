"""Tests for rhapsody_cli.elements.diagram.RPDiagram."""

from __future__ import annotations

from rhapsody_cli.models._core import RPModelElement, RPUnit, wrap
from rhapsody_cli.models.elements.diagram import RPDiagram
from tests.models.fakes import make_fake_collection, make_fake_element


def test_diagram_is_a_unit() -> None:
    fake = make_fake_element("ActivityDiagram", getName="MainFlow")
    diagram = RPDiagram(fake)

    assert isinstance(diagram, RPUnit)
    assert diagram.getName() == "MainFlow"


def test_diagram_close_diagram_delegates_to_com() -> None:
    fake = make_fake_element("ActivityDiagram")
    diagram = RPDiagram(fake)

    diagram.closeDiagram()

    fake.closeDiagram.assert_called_once_with()


def test_diagram_add_text_box_delegates_to_com_and_wraps_result() -> None:
    fake = make_fake_element("ActivityDiagram")
    text_box = make_fake_element("GraphElement", getName="Note1")
    fake.addTextBox.return_value = text_box
    diagram = RPDiagram(fake)

    result = diagram.addTextBox("hello", 0, 0, 50, 20)

    fake.addTextBox.assert_called_once_with("hello", 0, 0, 50, 20)
    assert result.getName() == "Note1"


def test_diagram_get_custom_views_returns_collection() -> None:
    fake = make_fake_element("ActivityDiagram")
    view = make_fake_element("Package", getName="CustomView1")
    fake.getCustomViews.return_value = make_fake_collection([view])
    diagram = RPDiagram(fake)

    views = diagram.getCustomViews()

    assert len(views) == 1
    assert views[0].getName() == "CustomView1"


def test_diagram_get_corresponding_graphic_elements_returns_collection() -> None:
    fake = make_fake_element("ActivityDiagram")
    graphic = make_fake_element("GraphElement", getName="Shape1")
    fake.getCorrespondingGraphicElements.return_value = make_fake_collection([graphic])
    diagram = RPDiagram(fake)
    model_element = make_fake_element("Class", getName="Widget")

    elements = diagram.getCorrespondingGraphicElements(RPModelElement(model_element))

    fake.getCorrespondingGraphicElements.assert_called_once_with(model_element)
    assert len(elements) == 1
    assert elements[0].getName() == "Shape1"


def test_diagram_is_registered_for_meta_class_activity_diagram() -> None:
    fake = make_fake_element("ActivityDiagram", getName="MainFlow")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPDiagram)
