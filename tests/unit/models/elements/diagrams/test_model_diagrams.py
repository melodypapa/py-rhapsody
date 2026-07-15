"""Tests for rhapsody_cli.elements.diagram.RPDiagram."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement, RPUnit
from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_diagram_is_a_unit() -> None:
    fake = make_fake_element("ActivityDiagram", getName="MainFlow")
    diagram = RPDiagram(fake)

    assert isinstance(diagram, RPUnit)
    assert diagram.get_name() == "MainFlow"


def test_diagram_close_diagram_delegates_to_com() -> None:
    fake = make_fake_element("ActivityDiagram")
    diagram = RPDiagram(fake)

    diagram.close_diagram()

    fake.closeDiagram.assert_called_once_with()


def test_diagram_add_text_box_delegates_to_com_and_wraps_result() -> None:
    fake = make_fake_element("ActivityDiagram")
    text_box = make_fake_element("GraphElement", getName="Note1")
    fake.addTextBox.return_value = text_box
    diagram = RPDiagram(fake)

    result = diagram.add_text_box("hello", 0, 0, 50, 20)

    fake.addTextBox.assert_called_once_with("hello", 0, 0, 50, 20)
    assert result.get_name() == "Note1"


def test_diagram_get_custom_views_returns_collection() -> None:
    fake = make_fake_element("ActivityDiagram")
    view = make_fake_element("Package", getName="CustomView1")
    fake.getCustomViews.return_value = make_fake_collection([view])
    diagram = RPDiagram(fake)

    views = diagram.get_custom_views()

    assert len(views) == 1
    assert views[0].get_name() == "CustomView1"


def test_diagram_get_corresponding_graphic_elements_returns_collection() -> None:
    fake = make_fake_element("ActivityDiagram")
    graphic = make_fake_element("GraphElement", getName="Shape1")
    fake.getCorrespondingGraphicElements.return_value = make_fake_collection([graphic])
    diagram = RPDiagram(fake)
    model_element = make_fake_element("Class", getName="Widget")

    elements = diagram.get_corresponding_graphic_elements(RPModelElement(model_element))

    fake.getCorrespondingGraphicElements.assert_called_once_with(model_element)
    assert len(elements) == 1
    assert elements[0].get_name() == "Shape1"


def test_diagram_is_registered_for_meta_class_activity_diagram() -> None:
    fake = make_fake_element("ActivityDiagram", getName="MainFlow")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPDiagram)


def test_diagram_get_pictures_with_image_map_delegates_to_com_with_two_args() -> None:
    fake = make_fake_element("ObjectModelDiagram")
    file_names = make_fake_collection([])
    fake.getPicturesWithImageMap.return_value = file_names
    diagram = RPDiagram(fake)
    diagram_map = RPCollection(make_fake_collection([]))

    result = diagram.get_pictures_with_image_map("output.emf", diagram_map)

    fake.getPicturesWithImageMap.assert_called_once_with("output.emf", diagram_map._com)
    assert isinstance(result, RPCollection)
