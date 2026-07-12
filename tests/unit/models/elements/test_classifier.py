"""Tests for rhapsody_cli.elements.classifier.RPClassifier."""

from rhapsody_cli.models.core import RPModelElement, RPUnit
from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.relations import RPPort
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_classifier_is_a_unit() -> None:
    fake = make_fake_element("Class", getName="Widget")
    classifier = RPClassifier(fake)

    assert isinstance(classifier, RPUnit)
    assert classifier.get_name() == "Widget"


def test_classifier_add_attribute_wraps_result() -> None:
    fake = make_fake_element("Class")
    attr = make_fake_element("Attribute", getName="count")
    fake.addAttribute.return_value = attr
    classifier = RPClassifier(fake)

    result = classifier.add_attribute("count")

    fake.addAttribute.assert_called_once_with("count")
    assert result.get_name() == "count"


def test_classifier_add_operation_wraps_result() -> None:
    fake = make_fake_element("Class")
    op = make_fake_element("Operation", getName="doIt")
    fake.addOperation.return_value = op
    classifier = RPClassifier(fake)

    result = classifier.add_operation("doIt")

    fake.addOperation.assert_called_once_with("doIt")
    assert result.get_name() == "doIt"


def test_classifier_get_attributes_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getAttributes.return_value = make_fake_collection([make_fake_element("Attribute", getName="count")])
    classifier = RPClassifier(fake)

    attributes = classifier.get_attributes()

    assert len(attributes) == 1
    assert attributes[0].get_name() == "count"


def test_classifier_get_operations_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getOperations.return_value = make_fake_collection([make_fake_element("Operation", getName="doIt")])
    classifier = RPClassifier(fake)

    operations = classifier.get_operations()

    assert len(operations) == 1
    assert operations[0].get_name() == "doIt"


def test_classifier_add_generalization_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    classifier = RPClassifier(fake)

    classifier.add_generalization(RPClassifier(base))

    fake.addGeneralization.assert_called_once_with(base)


def test_classifier_add_statechart_wraps_result() -> None:
    fake = make_fake_element("Class")
    statechart = make_fake_element("Statechart", getName="Behavior")
    fake.addStatechart.return_value = statechart
    classifier = RPClassifier(fake)

    result = classifier.add_statechart()

    fake.addStatechart.assert_called_once_with()
    assert result.get_name() == "Behavior"


def test_classifier_add_activity_diagram_wraps_result() -> None:
    fake = make_fake_element("Class")
    diagram = make_fake_element("ActivityDiagram", getName="Act")
    fake.addActivityDiagram.return_value = diagram
    classifier = RPClassifier(fake)

    result = classifier.add_activity_diagram()

    fake.addActivityDiagram.assert_called_once_with()
    assert result.get_name() == "Act"


def test_classifier_add_flow_items_wraps_result() -> None:
    fake = make_fake_element("Class")
    item = make_fake_element("FlowItem", getName="flowItem")
    fake.addFlowItems.return_value = item
    classifier = RPClassifier(fake)

    result = classifier.add_flow_items("flowItem")

    fake.addFlowItems.assert_called_once_with("flowItem")
    assert result.get_name() == "flowItem"


def test_classifier_add_flows_wraps_result() -> None:
    fake = make_fake_element("Class")
    flow = make_fake_element("Flow", getName="flow")
    fake.addFlows.return_value = flow
    classifier = RPClassifier(fake)

    result = classifier.add_flows("flow")

    fake.addFlows.assert_called_once_with("flow")
    assert result.get_name() == "flow"


def test_classifier_add_relation_wraps_result() -> None:
    fake = make_fake_element("Class")
    relation = make_fake_element("Relation", getName="assoc")
    fake.addRelation.return_value = relation
    classifier = RPClassifier(fake)

    result = classifier.add_relation("Other", "Pkg", "r1", "Association", "1", "r2", "Association", "*", "Link")

    fake.addRelation.assert_called_once_with("Other", "Pkg", "r1", "Association", "1", "r2", "Association", "*", "Link")
    assert result.get_name() == "assoc"


def test_classifier_add_relation_to_unwraps_classifier_and_wraps_result() -> None:
    fake = make_fake_element("Class")
    other_fake = make_fake_element("Class", getName="Other")
    relation = make_fake_element("Relation", getName="assoc")
    fake.addRelationTo.return_value = relation
    classifier = RPClassifier(fake)

    result = classifier.add_relation_to(RPClassifier(other_fake), "r1", "Association", "1", "r2", "Association", "*", "Link")

    fake.addRelationTo.assert_called_once_with(other_fake, "r1", "Association", "1", "r2", "Association", "*", "Link")
    assert result.get_name() == "assoc"


def test_classifier_add_unidirectional_relation_wraps_result() -> None:
    fake = make_fake_element("Class")
    relation = make_fake_element("Relation", getName="assoc")
    fake.addUnidirectionalRelation.return_value = relation
    classifier = RPClassifier(fake)

    result = classifier.add_unidirectional_relation("Other", "Pkg", "r1", "Association", "1", "Link")

    fake.addUnidirectionalRelation.assert_called_once_with("Other", "Pkg", "r1", "Association", "1", "Link")
    assert result.get_name() == "assoc"


def test_classifier_add_unidirectional_relation_to_unwraps_classifier_and_wraps_result() -> None:
    fake = make_fake_element("Class")
    other_fake = make_fake_element("Class", getName="Other")
    relation = make_fake_element("Relation", getName="assoc")
    fake.addUnidirectionalRelationTo.return_value = relation
    classifier = RPClassifier(fake)

    result = classifier.add_unidirectional_relation_to(RPClassifier(other_fake), "r1", "Association", "1", "Link")

    fake.addUnidirectionalRelationTo.assert_called_once_with(other_fake, "r1", "Association", "1", "Link")
    assert result.get_name() == "assoc"


def test_classifier_delete_attribute_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    attr_fake = make_fake_element("Attribute", getName="count")
    classifier = RPClassifier(fake)

    classifier.delete_attribute(RPModelElement(attr_fake))

    fake.deleteAttribute.assert_called_once_with(attr_fake)


def test_classifier_delete_flow_items_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    item_fake = make_fake_element("FlowItem", getName="flowItem")
    classifier = RPClassifier(fake)

    classifier.delete_flow_items(RPModelElement(item_fake))

    fake.deleteFlowItems.assert_called_once_with(item_fake)


def test_classifier_delete_flows_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    flow_fake = make_fake_element("Flow", getName="flow")
    classifier = RPClassifier(fake)

    classifier.delete_flows(RPModelElement(flow_fake))

    fake.deleteFlows.assert_called_once_with(flow_fake)


def test_classifier_delete_generalization_unwraps_classifier() -> None:
    fake = make_fake_element("Class")
    base_fake = make_fake_element("Class", getName="Base")
    classifier = RPClassifier(fake)

    classifier.delete_generalization(RPClassifier(base_fake))

    fake.deleteGeneralization.assert_called_once_with(base_fake)


def test_classifier_delete_operation_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    op_fake = make_fake_element("Operation", getName="doIt")
    classifier = RPClassifier(fake)

    classifier.delete_operation(RPModelElement(op_fake))

    fake.deleteOperation.assert_called_once_with(op_fake)


def test_classifier_delete_relation_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    rel_fake = make_fake_element("Relation", getName="assoc")
    classifier = RPClassifier(fake)

    classifier.delete_relation(RPModelElement(rel_fake))

    fake.deleteRelation.assert_called_once_with(rel_fake)


def test_classifier_find_attribute_wraps_result() -> None:
    fake = make_fake_element("Class")
    attr = make_fake_element("Attribute", getName="count")
    fake.findAttribute.return_value = attr
    classifier = RPClassifier(fake)

    result = classifier.find_attribute("count")

    fake.findAttribute.assert_called_once_with("count")
    assert result.get_name() == "count"


def test_classifier_find_base_classifier_wraps_result() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    fake.findBaseClassifier.return_value = base
    classifier = RPClassifier(fake)

    result = classifier.find_base_classifier("Base")

    fake.findBaseClassifier.assert_called_once_with("Base")
    assert result.get_name() == "Base"


def test_classifier_find_derived_classifier_wraps_result() -> None:
    fake = make_fake_element("Class")
    derived = make_fake_element("Class", getName="Derived")
    fake.findDerivedClassifier.return_value = derived
    classifier = RPClassifier(fake)

    result = classifier.find_derived_classifier("Derived")

    fake.findDerivedClassifier.assert_called_once_with("Derived")
    assert result.get_name() == "Derived"


def test_classifier_find_generalization_wraps_result() -> None:
    fake = make_fake_element("Class")
    gen = make_fake_element("Generalization", getName="gen")
    fake.findGeneralization.return_value = gen
    classifier = RPClassifier(fake)

    result = classifier.find_generalization("Base")

    fake.findGeneralization.assert_called_once_with("Base")
    assert result.get_name() == "gen"


def test_classifier_find_interface_item_wraps_result() -> None:
    fake = make_fake_element("Class")
    item = make_fake_element("Operation", getName="doIt")
    fake.findInterfaceItem.return_value = item
    classifier = RPClassifier(fake)

    result = classifier.find_interface_item("doIt()")

    fake.findInterfaceItem.assert_called_once_with("doIt()")
    assert result.get_name() == "doIt"


def test_classifier_find_nested_classifier_wraps_result() -> None:
    fake = make_fake_element("Class")
    nested = make_fake_element("Class", getName="Nested")
    fake.findNestedClassifier.return_value = nested
    classifier = RPClassifier(fake)

    result = classifier.find_nested_classifier("Nested")

    fake.findNestedClassifier.assert_called_once_with("Nested")
    assert result.get_name() == "Nested"


def test_classifier_find_nested_classifier_recursive_wraps_result() -> None:
    fake = make_fake_element("Class")
    nested = make_fake_element("Class", getName="Nested")
    fake.findNestedClassifierRecursive.return_value = nested
    classifier = RPClassifier(fake)

    result = classifier.find_nested_classifier_recursive("Nested")

    fake.findNestedClassifierRecursive.assert_called_once_with("Nested")
    assert result.get_name() == "Nested"


def test_classifier_find_relation_wraps_result() -> None:
    fake = make_fake_element("Class")
    rel = make_fake_element("Relation", getName="assoc")
    fake.findRelation.return_value = rel
    classifier = RPClassifier(fake)

    result = classifier.find_relation("assoc")

    fake.findRelation.assert_called_once_with("assoc")
    assert result.get_name() == "assoc"


def test_classifier_find_trigger_wraps_result() -> None:
    fake = make_fake_element("Class")
    trigger = make_fake_element("Trigger", getName="trig")
    fake.findTrigger.return_value = trigger
    classifier = RPClassifier(fake)

    result = classifier.find_trigger("trig")

    fake.findTrigger.assert_called_once_with("trig")
    assert result.get_name() == "trig"


def test_classifier_get_activity_diagram_wraps_result() -> None:
    fake = make_fake_element("Class")
    diagram = make_fake_element("ActivityDiagram", getName="Act")
    fake.getActivityDiagram.return_value = diagram
    classifier = RPClassifier(fake)

    result = classifier.get_activity_diagram()

    fake.getActivityDiagram.assert_called_once_with()
    assert result.get_name() == "Act"


def test_classifier_get_statechart_wraps_result() -> None:
    fake = make_fake_element("Class")
    statechart = make_fake_element("Statechart", getName="Behavior")
    fake.getStatechart.return_value = statechart
    classifier = RPClassifier(fake)

    result = classifier.get_statechart()

    fake.getStatechart.assert_called_once_with()
    assert result.get_name() == "Behavior"


def test_classifier_get_attributes_including_bases_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getAttributesIncludingBases.return_value = make_fake_collection([make_fake_element("Attribute", getName="count")])
    classifier = RPClassifier(fake)

    result = classifier.get_attributes_including_bases()

    assert len(result) == 1
    assert result[0].get_name() == "count"


def test_classifier_get_base_classifiers_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getBaseClassifiers.return_value = make_fake_collection([make_fake_element("Class", getName="Base")])
    classifier = RPClassifier(fake)

    result = classifier.get_base_classifiers()

    assert len(result) == 1
    assert result[0].get_name() == "Base"


def test_classifier_get_behavioral_diagrams_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getBehavioralDiagrams.return_value = make_fake_collection([make_fake_element("Statechart", getName="Behavior")])
    classifier = RPClassifier(fake)

    result = classifier.get_behavioral_diagrams()

    assert len(result) == 1
    assert result[0].get_name() == "Behavior"


def test_classifier_get_derived_classifiers_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getDerivedClassifiers.return_value = make_fake_collection([make_fake_element("Class", getName="Derived")])
    classifier = RPClassifier(fake)

    result = classifier.get_derived_classifiers()

    assert len(result) == 1
    assert result[0].get_name() == "Derived"


def test_classifier_get_flow_items_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getFlowItems.return_value = make_fake_collection([make_fake_element("FlowItem", getName="flowItem")])
    classifier = RPClassifier(fake)

    result = classifier.get_flow_items()

    assert len(result) == 1
    assert result[0].get_name() == "flowItem"


def test_classifier_get_flows_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getFlows.return_value = make_fake_collection([make_fake_element("Flow", getName="flow")])
    classifier = RPClassifier(fake)

    result = classifier.get_flows()

    assert len(result) == 1
    assert result[0].get_name() == "flow"


def test_classifier_get_generalizations_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getGeneralizations.return_value = make_fake_collection([make_fake_element("Generalization", getName="gen")])
    classifier = RPClassifier(fake)

    result = classifier.get_generalizations()

    assert len(result) == 1
    assert result[0].get_name() == "gen"


def test_classifier_get_interface_items_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getInterfaceItems.return_value = make_fake_collection([make_fake_element("Operation", getName="doIt")])
    classifier = RPClassifier(fake)

    result = classifier.get_interface_items()

    assert len(result) == 1
    assert result[0].get_name() == "doIt"


def test_classifier_get_interface_items_including_bases_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getInterfaceItemsIncludingBases.return_value = make_fake_collection([make_fake_element("Operation", getName="doIt")])
    classifier = RPClassifier(fake)

    result = classifier.get_interface_items_including_bases()

    assert len(result) == 1
    assert result[0].get_name() == "doIt"


def test_classifier_get_links_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getLinks.return_value = make_fake_collection([make_fake_element("Link", getName="link")])
    classifier = RPClassifier(fake)

    result = classifier.get_links()

    assert len(result) == 1
    assert result[0].get_name() == "link"


def test_classifier_get_nested_classifiers_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getNestedClassifiers.return_value = make_fake_collection([make_fake_element("Class", getName="Nested")])
    classifier = RPClassifier(fake)

    result = classifier.get_nested_classifiers()

    assert len(result) == 1
    assert result[0].get_name() == "Nested"


def test_classifier_get_ports_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getPorts.return_value = make_fake_collection([make_fake_element("Port", getName="port")])
    classifier = RPClassifier(fake)

    result = classifier.get_ports()

    assert len(result) == 1
    assert result[0].get_name() == "port"


def test_classifier_add_port_delegates_to_add_new_aggr() -> None:
    fake = make_fake_element("Class")
    port_fake = make_fake_element("Port", getName="clientPort")
    fake.addNewAggr.return_value = port_fake
    classifier = RPClassifier(fake)

    result = classifier.add_port("clientPort")

    fake.addNewAggr.assert_called_once_with("Port", "clientPort")
    assert isinstance(result, RPPort)
    assert result.get_name() == "clientPort"


def test_classifier_get_relations_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getRelations.return_value = make_fake_collection([make_fake_element("Relation", getName="assoc")])
    classifier = RPClassifier(fake)

    result = classifier.get_relations()

    assert len(result) == 1
    assert result[0].get_name() == "assoc"


def test_classifier_get_relations_including_bases_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getRelationsIncludingBases.return_value = make_fake_collection([make_fake_element("Relation", getName="assoc")])
    classifier = RPClassifier(fake)

    result = classifier.get_relations_including_bases()

    assert len(result) == 1
    assert result[0].get_name() == "assoc"


def test_classifier_get_sequence_diagrams_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getSequenceDiagrams.return_value = make_fake_collection([make_fake_element("SequenceDiagram", getName="seq")])
    classifier = RPClassifier(fake)

    result = classifier.get_sequence_diagrams()

    assert len(result) == 1
    assert result[0].get_name() == "seq"


def test_classifier_get_source_artifacts_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getSourceArtifacts.return_value = make_fake_collection([make_fake_element("File", getName="file")])
    classifier = RPClassifier(fake)

    result = classifier.get_source_artifacts()

    assert len(result) == 1
    assert result[0].get_name() == "file"
