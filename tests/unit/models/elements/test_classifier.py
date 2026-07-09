"""Tests for rhapsody_cli.elements.classifier.RPClassifier."""

from rhapsody_cli.models.core import RPModelElement, RPUnit
from rhapsody_cli.models.elements.classifiers import RPClassifier
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_classifier_is_a_unit() -> None:
    fake = make_fake_element("Class", getName="Widget")
    classifier = RPClassifier(fake)

    assert isinstance(classifier, RPUnit)
    assert classifier.getName() == "Widget"


def test_classifier_add_attribute_wraps_result() -> None:
    fake = make_fake_element("Class")
    attr = make_fake_element("Attribute", getName="count")
    fake.addAttribute.return_value = attr
    classifier = RPClassifier(fake)

    result = classifier.addAttribute("count")

    fake.addAttribute.assert_called_once_with("count")
    assert result.getName() == "count"


def test_classifier_add_operation_wraps_result() -> None:
    fake = make_fake_element("Class")
    op = make_fake_element("Operation", getName="doIt")
    fake.addOperation.return_value = op
    classifier = RPClassifier(fake)

    result = classifier.addOperation("doIt")

    fake.addOperation.assert_called_once_with("doIt")
    assert result.getName() == "doIt"


def test_classifier_get_attributes_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getAttributes.return_value = make_fake_collection([make_fake_element("Attribute", getName="count")])
    classifier = RPClassifier(fake)

    attributes = classifier.getAttributes()

    assert len(attributes) == 1
    assert attributes[0].getName() == "count"


def test_classifier_get_operations_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getOperations.return_value = make_fake_collection([make_fake_element("Operation", getName="doIt")])
    classifier = RPClassifier(fake)

    operations = classifier.getOperations()

    assert len(operations) == 1
    assert operations[0].getName() == "doIt"


def test_classifier_add_generalization_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    classifier = RPClassifier(fake)

    classifier.addGeneralization(RPClassifier(base))

    fake.addGeneralization.assert_called_once_with(base)


def test_classifier_add_statechart_wraps_result() -> None:
    fake = make_fake_element("Class")
    statechart = make_fake_element("Statechart", getName="Behavior")
    fake.addStatechart.return_value = statechart
    classifier = RPClassifier(fake)

    result = classifier.addStatechart()

    fake.addStatechart.assert_called_once_with()
    assert result.getName() == "Behavior"


def test_classifier_add_activity_diagram_wraps_result() -> None:
    fake = make_fake_element("Class")
    diagram = make_fake_element("ActivityDiagram", getName="Act")
    fake.addActivityDiagram.return_value = diagram
    classifier = RPClassifier(fake)

    result = classifier.addActivityDiagram()

    fake.addActivityDiagram.assert_called_once_with()
    assert result.getName() == "Act"


def test_classifier_add_flow_items_wraps_result() -> None:
    fake = make_fake_element("Class")
    item = make_fake_element("FlowItem", getName="flowItem")
    fake.addFlowItems.return_value = item
    classifier = RPClassifier(fake)

    result = classifier.addFlowItems("flowItem")

    fake.addFlowItems.assert_called_once_with("flowItem")
    assert result.getName() == "flowItem"


def test_classifier_add_flows_wraps_result() -> None:
    fake = make_fake_element("Class")
    flow = make_fake_element("Flow", getName="flow")
    fake.addFlows.return_value = flow
    classifier = RPClassifier(fake)

    result = classifier.addFlows("flow")

    fake.addFlows.assert_called_once_with("flow")
    assert result.getName() == "flow"


def test_classifier_add_relation_wraps_result() -> None:
    fake = make_fake_element("Class")
    relation = make_fake_element("Relation", getName="assoc")
    fake.addRelation.return_value = relation
    classifier = RPClassifier(fake)

    result = classifier.addRelation("Other", "Pkg", "r1", "Association", "1", "r2", "Association", "*", "Link")

    fake.addRelation.assert_called_once_with("Other", "Pkg", "r1", "Association", "1", "r2", "Association", "*", "Link")
    assert result.getName() == "assoc"


def test_classifier_add_relation_to_unwraps_classifier_and_wraps_result() -> None:
    fake = make_fake_element("Class")
    other_fake = make_fake_element("Class", getName="Other")
    relation = make_fake_element("Relation", getName="assoc")
    fake.addRelationTo.return_value = relation
    classifier = RPClassifier(fake)

    result = classifier.addRelationTo(RPClassifier(other_fake), "r1", "Association", "1", "r2", "Association", "*", "Link")

    fake.addRelationTo.assert_called_once_with(other_fake, "r1", "Association", "1", "r2", "Association", "*", "Link")
    assert result.getName() == "assoc"


def test_classifier_add_unidirectional_relation_wraps_result() -> None:
    fake = make_fake_element("Class")
    relation = make_fake_element("Relation", getName="assoc")
    fake.addUnidirectionalRelation.return_value = relation
    classifier = RPClassifier(fake)

    result = classifier.addUnidirectionalRelation("Other", "Pkg", "r1", "Association", "1", "Link")

    fake.addUnidirectionalRelation.assert_called_once_with("Other", "Pkg", "r1", "Association", "1", "Link")
    assert result.getName() == "assoc"


def test_classifier_add_unidirectional_relation_to_unwraps_classifier_and_wraps_result() -> None:
    fake = make_fake_element("Class")
    other_fake = make_fake_element("Class", getName="Other")
    relation = make_fake_element("Relation", getName="assoc")
    fake.addUnidirectionalRelationTo.return_value = relation
    classifier = RPClassifier(fake)

    result = classifier.addUnidirectionalRelationTo(RPClassifier(other_fake), "r1", "Association", "1", "Link")

    fake.addUnidirectionalRelationTo.assert_called_once_with(other_fake, "r1", "Association", "1", "Link")
    assert result.getName() == "assoc"


def test_classifier_delete_attribute_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    attr_fake = make_fake_element("Attribute", getName="count")
    classifier = RPClassifier(fake)

    classifier.deleteAttribute(RPModelElement(attr_fake))

    fake.deleteAttribute.assert_called_once_with(attr_fake)


def test_classifier_delete_flow_items_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    item_fake = make_fake_element("FlowItem", getName="flowItem")
    classifier = RPClassifier(fake)

    classifier.deleteFlowItems(RPModelElement(item_fake))

    fake.deleteFlowItems.assert_called_once_with(item_fake)


def test_classifier_delete_flows_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    flow_fake = make_fake_element("Flow", getName="flow")
    classifier = RPClassifier(fake)

    classifier.deleteFlows(RPModelElement(flow_fake))

    fake.deleteFlows.assert_called_once_with(flow_fake)


def test_classifier_delete_generalization_unwraps_classifier() -> None:
    fake = make_fake_element("Class")
    base_fake = make_fake_element("Class", getName="Base")
    classifier = RPClassifier(fake)

    classifier.deleteGeneralization(RPClassifier(base_fake))

    fake.deleteGeneralization.assert_called_once_with(base_fake)


def test_classifier_delete_operation_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    op_fake = make_fake_element("Operation", getName="doIt")
    classifier = RPClassifier(fake)

    classifier.deleteOperation(RPModelElement(op_fake))

    fake.deleteOperation.assert_called_once_with(op_fake)


def test_classifier_delete_relation_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    rel_fake = make_fake_element("Relation", getName="assoc")
    classifier = RPClassifier(fake)

    classifier.deleteRelation(RPModelElement(rel_fake))

    fake.deleteRelation.assert_called_once_with(rel_fake)


def test_classifier_find_attribute_wraps_result() -> None:
    fake = make_fake_element("Class")
    attr = make_fake_element("Attribute", getName="count")
    fake.findAttribute.return_value = attr
    classifier = RPClassifier(fake)

    result = classifier.findAttribute("count")

    fake.findAttribute.assert_called_once_with("count")
    assert result.getName() == "count"


def test_classifier_find_base_classifier_wraps_result() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    fake.findBaseClassifier.return_value = base
    classifier = RPClassifier(fake)

    result = classifier.findBaseClassifier("Base")

    fake.findBaseClassifier.assert_called_once_with("Base")
    assert result.getName() == "Base"


def test_classifier_find_derived_classifier_wraps_result() -> None:
    fake = make_fake_element("Class")
    derived = make_fake_element("Class", getName="Derived")
    fake.findDerivedClassifier.return_value = derived
    classifier = RPClassifier(fake)

    result = classifier.findDerivedClassifier("Derived")

    fake.findDerivedClassifier.assert_called_once_with("Derived")
    assert result.getName() == "Derived"


def test_classifier_find_generalization_wraps_result() -> None:
    fake = make_fake_element("Class")
    gen = make_fake_element("Generalization", getName="gen")
    fake.findGeneralization.return_value = gen
    classifier = RPClassifier(fake)

    result = classifier.findGeneralization("Base")

    fake.findGeneralization.assert_called_once_with("Base")
    assert result.getName() == "gen"


def test_classifier_find_interface_item_wraps_result() -> None:
    fake = make_fake_element("Class")
    item = make_fake_element("Operation", getName="doIt")
    fake.findInterfaceItem.return_value = item
    classifier = RPClassifier(fake)

    result = classifier.findInterfaceItem("doIt()")

    fake.findInterfaceItem.assert_called_once_with("doIt()")
    assert result.getName() == "doIt"


def test_classifier_find_nested_classifier_wraps_result() -> None:
    fake = make_fake_element("Class")
    nested = make_fake_element("Class", getName="Nested")
    fake.findNestedClassifier.return_value = nested
    classifier = RPClassifier(fake)

    result = classifier.findNestedClassifier("Nested")

    fake.findNestedClassifier.assert_called_once_with("Nested")
    assert result.getName() == "Nested"


def test_classifier_find_nested_classifier_recursive_wraps_result() -> None:
    fake = make_fake_element("Class")
    nested = make_fake_element("Class", getName="Nested")
    fake.findNestedClassifierRecursive.return_value = nested
    classifier = RPClassifier(fake)

    result = classifier.findNestedClassifierRecursive("Nested")

    fake.findNestedClassifierRecursive.assert_called_once_with("Nested")
    assert result.getName() == "Nested"


def test_classifier_find_relation_wraps_result() -> None:
    fake = make_fake_element("Class")
    rel = make_fake_element("Relation", getName="assoc")
    fake.findRelation.return_value = rel
    classifier = RPClassifier(fake)

    result = classifier.findRelation("assoc")

    fake.findRelation.assert_called_once_with("assoc")
    assert result.getName() == "assoc"


def test_classifier_find_trigger_wraps_result() -> None:
    fake = make_fake_element("Class")
    trigger = make_fake_element("Trigger", getName="trig")
    fake.findTrigger.return_value = trigger
    classifier = RPClassifier(fake)

    result = classifier.findTrigger("trig")

    fake.findTrigger.assert_called_once_with("trig")
    assert result.getName() == "trig"


def test_classifier_get_activity_diagram_wraps_result() -> None:
    fake = make_fake_element("Class")
    diagram = make_fake_element("ActivityDiagram", getName="Act")
    fake.getActivityDiagram.return_value = diagram
    classifier = RPClassifier(fake)

    result = classifier.getActivityDiagram()

    fake.getActivityDiagram.assert_called_once_with()
    assert result.getName() == "Act"


def test_classifier_get_statechart_wraps_result() -> None:
    fake = make_fake_element("Class")
    statechart = make_fake_element("Statechart", getName="Behavior")
    fake.getStatechart.return_value = statechart
    classifier = RPClassifier(fake)

    result = classifier.getStatechart()

    fake.getStatechart.assert_called_once_with()
    assert result.getName() == "Behavior"


def test_classifier_get_attributes_including_bases_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getAttributesIncludingBases.return_value = make_fake_collection([make_fake_element("Attribute", getName="count")])
    classifier = RPClassifier(fake)

    result = classifier.getAttributesIncludingBases()

    assert len(result) == 1
    assert result[0].getName() == "count"


def test_classifier_get_base_classifiers_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getBaseClassifiers.return_value = make_fake_collection([make_fake_element("Class", getName="Base")])
    classifier = RPClassifier(fake)

    result = classifier.getBaseClassifiers()

    assert len(result) == 1
    assert result[0].getName() == "Base"


def test_classifier_get_behavioral_diagrams_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getBehavioralDiagrams.return_value = make_fake_collection([make_fake_element("Statechart", getName="Behavior")])
    classifier = RPClassifier(fake)

    result = classifier.getBehavioralDiagrams()

    assert len(result) == 1
    assert result[0].getName() == "Behavior"


def test_classifier_get_derived_classifiers_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getDerivedClassifiers.return_value = make_fake_collection([make_fake_element("Class", getName="Derived")])
    classifier = RPClassifier(fake)

    result = classifier.getDerivedClassifiers()

    assert len(result) == 1
    assert result[0].getName() == "Derived"


def test_classifier_get_flow_items_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getFlowItems.return_value = make_fake_collection([make_fake_element("FlowItem", getName="flowItem")])
    classifier = RPClassifier(fake)

    result = classifier.getFlowItems()

    assert len(result) == 1
    assert result[0].getName() == "flowItem"


def test_classifier_get_flows_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getFlows.return_value = make_fake_collection([make_fake_element("Flow", getName="flow")])
    classifier = RPClassifier(fake)

    result = classifier.getFlows()

    assert len(result) == 1
    assert result[0].getName() == "flow"


def test_classifier_get_generalizations_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getGeneralizations.return_value = make_fake_collection([make_fake_element("Generalization", getName="gen")])
    classifier = RPClassifier(fake)

    result = classifier.getGeneralizations()

    assert len(result) == 1
    assert result[0].getName() == "gen"


def test_classifier_get_interface_items_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getInterfaceItems.return_value = make_fake_collection([make_fake_element("Operation", getName="doIt")])
    classifier = RPClassifier(fake)

    result = classifier.getInterfaceItems()

    assert len(result) == 1
    assert result[0].getName() == "doIt"


def test_classifier_get_interface_items_including_bases_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getInterfaceItemsIncludingBases.return_value = make_fake_collection([make_fake_element("Operation", getName="doIt")])
    classifier = RPClassifier(fake)

    result = classifier.getInterfaceItemsIncludingBases()

    assert len(result) == 1
    assert result[0].getName() == "doIt"


def test_classifier_get_links_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getLinks.return_value = make_fake_collection([make_fake_element("Link", getName="link")])
    classifier = RPClassifier(fake)

    result = classifier.getLinks()

    assert len(result) == 1
    assert result[0].getName() == "link"


def test_classifier_get_nested_classifiers_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getNestedClassifiers.return_value = make_fake_collection([make_fake_element("Class", getName="Nested")])
    classifier = RPClassifier(fake)

    result = classifier.getNestedClassifiers()

    assert len(result) == 1
    assert result[0].getName() == "Nested"


def test_classifier_get_ports_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getPorts.return_value = make_fake_collection([make_fake_element("Port", getName="port")])
    classifier = RPClassifier(fake)

    result = classifier.getPorts()

    assert len(result) == 1
    assert result[0].getName() == "port"


def test_classifier_get_relations_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getRelations.return_value = make_fake_collection([make_fake_element("Relation", getName="assoc")])
    classifier = RPClassifier(fake)

    result = classifier.getRelations()

    assert len(result) == 1
    assert result[0].getName() == "assoc"


def test_classifier_get_relations_including_bases_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getRelationsIncludingBases.return_value = make_fake_collection([make_fake_element("Relation", getName="assoc")])
    classifier = RPClassifier(fake)

    result = classifier.getRelationsIncludingBases()

    assert len(result) == 1
    assert result[0].getName() == "assoc"


def test_classifier_get_sequence_diagrams_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getSequenceDiagrams.return_value = make_fake_collection([make_fake_element("SequenceDiagram", getName="seq")])
    classifier = RPClassifier(fake)

    result = classifier.getSequenceDiagrams()

    assert len(result) == 1
    assert result[0].getName() == "seq"


def test_classifier_get_source_artifacts_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getSourceArtifacts.return_value = make_fake_collection([make_fake_element("File", getName="file")])
    classifier = RPClassifier(fake)

    result = classifier.getSourceArtifacts()

    assert len(result) == 1
    assert result[0].getName() == "file"
