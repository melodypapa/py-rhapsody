"""Tests for rhapsody_cli.elements.statechart.RPStatechart."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPClass, RPStatechart
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_statechart_is_a_class() -> None:
    fake = make_fake_element("Statechart", getName="Behavior")
    statechart = RPStatechart(fake)

    assert isinstance(statechart, RPClass)
    assert statechart.get_name() == "Behavior"


def test_statechart_add_new_node_by_type_wraps_result() -> None:
    fake = make_fake_element("Statechart")
    node = make_fake_element("State", getName="Idle")
    fake.addNewNodeByType.return_value = node
    statechart = RPStatechart(fake)

    result = statechart.add_new_node_by_type("State", 10, 20, 100, 50)

    fake.addNewNodeByType.assert_called_once_with("State", 10, 20, 100, 50)
    assert result.get_name() == "Idle"


def test_statechart_create_graphics_delegates_to_com() -> None:
    fake = make_fake_element("Statechart")
    statechart = RPStatechart(fake)

    statechart.create_graphics()

    fake.createGraphics.assert_called_once_with()


def test_statechart_close_diagram_delegates_to_com() -> None:
    fake = make_fake_element("Statechart")
    statechart = RPStatechart(fake)

    statechart.close_diagram()

    fake.closeDiagram.assert_called_once_with()


def test_statechart_delete_state_delegates_to_com() -> None:
    fake = make_fake_element("Statechart")
    state = make_fake_element("State", getName="Idle")
    statechart = RPStatechart(fake)

    statechart.delete_state(RPModelElement(state))

    fake.deleteState.assert_called_once_with(state)


def test_statechart_is_registered_for_meta_class_statechart() -> None:
    fake = make_fake_element("Statechart", getName="Behavior")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPStatechart)


def test_statechart_get_pictures_with_image_map_delegates_to_com_with_two_args() -> None:
    fake = make_fake_element("Statechart")
    file_names = make_fake_collection([])
    fake.getPicturesWithImageMap.return_value = file_names
    statechart = RPStatechart(fake)
    diagram_map = RPCollection(make_fake_collection([]))

    result = statechart.get_pictures_with_image_map("output.emf", diagram_map)

    fake.getPicturesWithImageMap.assert_called_once_with("output.emf", diagram_map._com)
    assert isinstance(result, RPCollection)
