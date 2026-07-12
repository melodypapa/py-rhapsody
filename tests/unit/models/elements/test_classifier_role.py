"""Tests for rhapsody_cli.models.elements.common.model_other_model.RPClassifierRole."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.common import RPClassifierRole
from rhapsody_cli.models.elements.relations import RPInstance
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPClassifierRole:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("ClassifierRole", getName="Lifeline1")
        role = RPClassifierRole(fake)
        assert isinstance(role, RPModelElement)
        assert role.get_name() == "Lifeline1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("ClassifierRole", getName="L1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPClassifierRole)

    def test_get_formal_classifier_wraps_result(self) -> None:
        # Pattern B — no-arg getter returning wrapped element
        fake = make_fake_element("ClassifierRole")
        clf = make_fake_element("Class", getName="Foo")
        fake.getFormalClassifier.return_value = clf
        role = RPClassifierRole(fake)
        wrapped = role.get_formal_classifier()
        assert wrapped.get_name() == "Foo"
        fake.getFormalClassifier.assert_called_once_with()

    def test_get_formal_instance_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("ClassifierRole")
        inst = make_fake_element("Instance", getName="Inst1")
        fake.getFormalInstance.return_value = inst
        role = RPClassifierRole(fake)
        wrapped = role.get_formal_instance()
        assert wrapped.get_name() == "Inst1"
        fake.getFormalInstance.assert_called_once_with()

    def test_get_referenced_sequence_diagram_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("ClassifierRole")
        sd = make_fake_element("SequenceDiagram", getName="SD1")
        fake.getReferencedSequenceDiagram.return_value = sd
        role = RPClassifierRole(fake)
        wrapped = role.get_referenced_sequence_diagram()
        assert wrapped.get_name() == "SD1"
        fake.getReferencedSequenceDiagram.assert_called_once_with()

    def test_get_referencing_classifier_roles_recursively_returns_collection(self) -> None:
        # Pattern C — no-arg getter returning RPCollection
        fake = make_fake_element("ClassifierRole")
        sub = make_fake_element("ClassifierRole", getName="Sub")
        fake.getReferencingClassifierRolesRecursively.return_value = make_fake_collection([sub])
        role = RPClassifierRole(fake)
        result = role.get_referencing_classifier_roles_recursively()
        assert isinstance(result, RPCollection)
        fake.getReferencingClassifierRolesRecursively.assert_called_once_with()

    def test_get_role_type_returns_string(self) -> None:
        # Pattern A — no-arg getter returning primitive
        fake = make_fake_element("ClassifierRole", getRoleType="CLASS")
        role = RPClassifierRole(fake)
        assert role.get_role_type() == "CLASS"
        fake.getRoleType.assert_called_once_with()

    def test_set_formal_classifier_delegates(self) -> None:
        # Pattern F — multi-arg void method (single RPClassifier arg)
        fake = make_fake_element("ClassifierRole")
        clf = make_fake_element("Class", getName="Foo")
        fake.setFormalClassifier.return_value = None
        role = RPClassifierRole(fake)
        role.set_formal_classifier(RPClassifier(clf))
        fake.setFormalClassifier.assert_called_once_with(clf)

    def test_set_formal_instance_delegates(self) -> None:
        # Pattern F
        fake = make_fake_element("ClassifierRole")
        inst = make_fake_element("Instance", getName="Inst1")
        fake.setFormalInstance.return_value = None
        role = RPClassifierRole(fake)
        role.set_formal_instance(RPInstance(inst))
        fake.setFormalInstance.assert_called_once_with(inst)

    def test_set_referenced_sequence_diagram_delegates(self) -> None:
        # Pattern F
        from rhapsody_cli.models.elements.diagrams import RPSequenceDiagram

        fake = make_fake_element("ClassifierRole")
        sd = make_fake_element("SequenceDiagram", getName="SD1")
        fake.setReferencedSequenceDiagram.return_value = None
        role = RPClassifierRole(fake)
        role.set_referenced_sequence_diagram(RPSequenceDiagram(sd))
        fake.setReferencedSequenceDiagram.assert_called_once_with(sd)
