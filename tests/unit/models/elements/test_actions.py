"""Tests for rhapsody_cli.models.elements.activity.model_actions."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.activity.model_actions import (
    RPAcceptEventAction,
    RPAcceptTimeEvent,
    RPAction,
    RPActionBlock,
    RPCallOperation,
    RPContextSpecification,
    RPSendAction,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPAcceptEventAction:
    def test_is_state(self) -> None:
        fake = make_fake_element("AcceptEventAction", getName="AEA1")
        aea = RPAcceptEventAction(fake)
        assert isinstance(aea, RPModelElement)
        assert aea.get_name() == "AEA1"

    def test_get_event_wraps_result(self) -> None:
        fake = make_fake_element("AcceptEventAction")
        event = make_fake_element("Event", getName="MyEvent")
        fake.getEvent.return_value = event
        aea = RPAcceptEventAction(fake)
        result = aea.get_event()
        assert result.get_name() == "MyEvent"
        fake.getEvent.assert_called_once_with()

    def test_set_event_delegates(self) -> None:
        fake = make_fake_element("AcceptEventAction")
        event = make_fake_element("Event", getName="MyEvent")
        aea = RPAcceptEventAction(fake)
        aea.set_event(AbstractRPModelElement.wrap(event))
        fake.setEvent.assert_called_once_with(event)

    def test_is_registered(self) -> None:
        fake = make_fake_element("AcceptEventAction", getName="AEA1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPAcceptEventAction)


class TestRPAcceptTimeEvent:
    def test_is_state(self) -> None:
        fake = make_fake_element("AcceptTimeEvent", getName="ATE1")
        ate = RPAcceptTimeEvent(fake)
        assert isinstance(ate, RPModelElement)
        assert ate.get_name() == "ATE1"

    def test_get_duration_time_returns_string(self) -> None:
        fake = make_fake_element("AcceptTimeEvent", getDurationTime="5s")
        ate = RPAcceptTimeEvent(fake)
        assert ate.get_duration_time() == "5s"
        fake.getDurationTime.assert_called_once_with()

    def test_set_duration_time_delegates(self) -> None:
        fake = make_fake_element("AcceptTimeEvent")
        ate = RPAcceptTimeEvent(fake)
        ate.set_duration_time("10s")
        fake.setDurationTime.assert_called_once_with("10s")

    def test_is_registered(self) -> None:
        fake = make_fake_element("AcceptTimeEvent", getName="ATE1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPAcceptTimeEvent)


class TestRPAction:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("Action", getName="Act1")
        act = RPAction(fake)
        assert isinstance(act, RPModelElement)
        assert act.get_name() == "Act1"

    def test_get_body_returns_string(self) -> None:
        fake = make_fake_element("Action", getBody="doSomething()")
        act = RPAction(fake)
        assert act.get_body() == "doSomething()"
        fake.getBody.assert_called_once_with()

    def test_set_body_delegates(self) -> None:
        fake = make_fake_element("Action")
        act = RPAction(fake)
        act.set_body("doOther()")
        fake.setBody.assert_called_once_with("doOther()")

    def test_is_registered(self) -> None:
        fake = make_fake_element("Action", getName="Act1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPAction)


class TestRPActionBlock:
    def test_is_message(self) -> None:
        fake = make_fake_element("ActionBlock", getName="AB1")
        ab = RPActionBlock(fake)
        assert isinstance(ab, RPModelElement)
        assert ab.get_name() == "AB1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("ActionBlock", getName="AB1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPActionBlock)


class TestRPCallOperation:
    def test_is_state(self) -> None:
        fake = make_fake_element("CallOperation", getName="CO1")
        co = RPCallOperation(fake)
        assert isinstance(co, RPModelElement)
        assert co.get_name() == "CO1"

    def test_get_operation_wraps_result(self) -> None:
        fake = make_fake_element("CallOperation")
        op = make_fake_element("Operation", getName="myOp")
        fake.getOperation.return_value = op
        co = RPCallOperation(fake)
        result = co.get_operation()
        assert result.get_name() == "myOp"
        fake.getOperation.assert_called_once_with()

    def test_get_target_wraps_result(self) -> None:
        fake = make_fake_element("CallOperation")
        target = make_fake_element("Relation", getName="myTarget")
        fake.getTarget.return_value = target
        co = RPCallOperation(fake)
        result = co.get_target()
        assert result.get_name() == "myTarget"
        fake.getTarget.assert_called_once_with()

    def test_set_operation_delegates(self) -> None:
        fake = make_fake_element("CallOperation")
        op = make_fake_element("Operation", getName="myOp")
        co = RPCallOperation(fake)
        co.set_operation(AbstractRPModelElement.wrap(op))
        fake.setOperation.assert_called_once_with(op)

    def test_set_target_delegates(self) -> None:
        fake = make_fake_element("CallOperation")
        target = make_fake_element("Relation", getName="myTarget")
        co = RPCallOperation(fake)
        co.set_target(AbstractRPModelElement.wrap(target))
        fake.setTarget.assert_called_once_with(target)

    def test_is_registered(self) -> None:
        fake = make_fake_element("CallOperation", getName="CO1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPCallOperation)


class TestRPContextSpecification:
    def test_is_value_specification(self) -> None:
        fake = make_fake_element("ContextSpecification", getName="CS1")
        cs = RPContextSpecification(fake)
        assert isinstance(cs, RPModelElement)
        assert cs.get_name() == "CS1"

    def test_get_multiplicities_returns_collection(self) -> None:
        fake = make_fake_element("ContextSpecification")
        fake.getMultiplicities.return_value = make_fake_collection(["1", "2"])
        cs = RPContextSpecification(fake)
        result = cs.get_multiplicities()
        assert isinstance(result, RPCollection)
        assert len(result) == 2
        fake.getMultiplicities.assert_called_once_with()

    def test_get_value_returns_collection(self) -> None:
        fake = make_fake_element("ContextSpecification")
        fake.getValue.return_value = make_fake_collection(["pkg", "cls"])
        cs = RPContextSpecification(fake)
        result = cs.get_value()
        assert isinstance(result, RPCollection)
        assert len(result) == 2
        fake.getValue.assert_called_once_with()

    def test_set_multiplicities_delegates(self) -> None:
        fake = make_fake_element("ContextSpecification")
        coll = make_fake_collection(["1", "2"])
        cs = RPContextSpecification(fake)
        cs.set_multiplicities(RPCollection(coll))
        fake.setMultiplicities.assert_called_once_with(coll)

    def test_set_value_delegates(self) -> None:
        fake = make_fake_element("ContextSpecification")
        coll = make_fake_collection(["pkg", "cls"])
        cs = RPContextSpecification(fake)
        cs.set_value(RPCollection(coll))
        fake.setValue.assert_called_once_with(coll)

    def test_is_registered(self) -> None:
        fake = make_fake_element("ContextSpecification", getName="CS1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPContextSpecification)


class TestRPSendAction:
    def test_is_action(self) -> None:
        fake = make_fake_element("SendAction", getName="SA1")
        sa = RPSendAction(fake)
        assert isinstance(sa, RPAction)
        assert sa.get_name() == "SA1"

    def test_add_argument_value_delegates(self) -> None:
        fake = make_fake_element("SendAction")
        sa = RPSendAction(fake)
        sa.add_argument_value("value1", 1)
        fake.addArgumentValue.assert_called_once_with("value1", 1)

    def test_get_arg_vals_returns_collection(self) -> None:
        fake = make_fake_element("SendAction")
        fake.getArgVals.return_value = make_fake_collection(["arg1", "arg2"])
        sa = RPSendAction(fake)
        result = sa.get_arg_vals()
        assert isinstance(result, RPCollection)
        assert len(result) == 2
        fake.getArgVals.assert_called_once_with()

    def test_get_event_wraps_result(self) -> None:
        fake = make_fake_element("SendAction")
        event = make_fake_element("Event", getName="MyEvent")
        fake.getEvent.return_value = event
        sa = RPSendAction(fake)
        result = sa.get_event()
        assert result.get_name() == "MyEvent"
        fake.getEvent.assert_called_once_with()

    def test_get_invoked_operation_wraps_result(self) -> None:
        fake = make_fake_element("SendAction")
        op = make_fake_element("Operation", getName="myOp")
        fake.getInvokedOperation.return_value = op
        sa = RPSendAction(fake)
        result = sa.get_invoked_operation()
        assert result.get_name() == "myOp"
        fake.getInvokedOperation.assert_called_once_with()

    def test_get_target_wraps_result(self) -> None:
        fake = make_fake_element("SendAction")
        target = make_fake_element("Class", getName="MyClass")
        fake.getTarget.return_value = target
        sa = RPSendAction(fake)
        result = sa.get_target()
        assert result.get_name() == "MyClass"
        fake.getTarget.assert_called_once_with()

    def test_set_event_delegates(self) -> None:
        fake = make_fake_element("SendAction")
        event = make_fake_element("Event", getName="MyEvent")
        sa = RPSendAction(fake)
        sa.set_event(AbstractRPModelElement.wrap(event))
        fake.setEvent.assert_called_once_with(event)

    def test_set_invoked_operation_delegates(self) -> None:
        fake = make_fake_element("SendAction")
        op = make_fake_element("Operation", getName="myOp")
        sa = RPSendAction(fake)
        sa.set_invoked_operation(AbstractRPModelElement.wrap(op))
        fake.setInvokedOperation.assert_called_once_with(op)

    def test_set_target_delegates(self) -> None:
        fake = make_fake_element("SendAction")
        target = make_fake_element("Class", getName="MyClass")
        sa = RPSendAction(fake)
        sa.set_target(AbstractRPModelElement.wrap(target))
        fake.setTarget.assert_called_once_with(target)

    def test_is_registered(self) -> None:
        fake = make_fake_element("SendAction", getName="SA1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPSendAction)