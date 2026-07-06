"""Tests for py_rhapsody.elements.statechart.RPStatechart."""

from __future__ import annotations

from py_rhapsody._core import RPModelElement, RPUnit, wrap
from py_rhapsody.elements.statechart import RPStatechart
from tests.fakes import make_fake_element


def test_statechart_is_a_unit() -> None:
    fake = make_fake_element("Statechart", getName="Behavior")
    statechart = RPStatechart(fake)

    assert isinstance(statechart, RPUnit)
    assert statechart.getName() == "Behavior"


def test_statechart_add_new_node_by_type_wraps_result() -> None:
    fake = make_fake_element("Statechart")
    node = make_fake_element("State", getName="Idle")
    fake.addNewNodeByType.return_value = node
    statechart = RPStatechart(fake)

    result = statechart.addNewNodeByType("State", 10, 20, 100, 50)

    fake.addNewNodeByType.assert_called_once_with("State", 10, 20, 100, 50)
    assert result.getName() == "Idle"


def test_statechart_create_graphics_delegates_to_com() -> None:
    fake = make_fake_element("Statechart")
    statechart = RPStatechart(fake)

    statechart.createGraphics()

    fake.createGraphics.assert_called_once_with()


def test_statechart_close_diagram_delegates_to_com() -> None:
    fake = make_fake_element("Statechart")
    statechart = RPStatechart(fake)

    statechart.closeDiagram()

    fake.closeDiagram.assert_called_once_with()


def test_statechart_delete_state_delegates_to_com() -> None:
    fake = make_fake_element("Statechart")
    state = make_fake_element("State", getName="Idle")
    statechart = RPStatechart(fake)

    statechart.deleteState(RPModelElement(state))

    fake.deleteState.assert_called_once_with(state)


def test_statechart_is_registered_for_meta_class_statechart() -> None:
    fake = make_fake_element("Statechart", getName="Behavior")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPStatechart)
