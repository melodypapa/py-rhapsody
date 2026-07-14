"""Tests for rhapsody_cli.elements.package.RPPackage."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPUnit
from rhapsody_cli.models.elements.containment import RPPackage
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_package_is_a_unit() -> None:
    fake = make_fake_element("Package", getName="MyPkg")
    package = RPPackage(fake)

    assert isinstance(package, RPUnit)
    assert package.get_name() == "MyPkg"


def test_package_add_class_delegates_to_com_and_wraps_result() -> None:
    fake = make_fake_element("Package")
    new_class = make_fake_element("Class", getName="Widget")
    fake.addClass.return_value = new_class
    package = RPPackage(fake)

    result = package.add_class("Widget")

    fake.addClass.assert_called_once_with("Widget")
    assert result.get_name() == "Widget"


def test_package_add_nested_package_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    nested = make_fake_element("Package", getName="Nested")
    fake.addNestedPackage.return_value = nested
    package = RPPackage(fake)

    result = package.add_nested_package("Nested")

    fake.addNestedPackage.assert_called_once_with("Nested")
    assert result.get_name() == "Nested"


def test_package_add_actor_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    actor = make_fake_element("Actor", getName="Driver")
    fake.addActor.return_value = actor
    package = RPPackage(fake)

    result = package.add_actor("Driver")

    fake.addActor.assert_called_once_with("Driver")
    assert result.get_name() == "Driver"


def test_package_add_global_function_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    func = make_fake_element("Operation", getName="doThing")
    fake.addGlobalFunction.return_value = func
    package = RPPackage(fake)

    result = package.add_global_function("doThing")

    fake.addGlobalFunction.assert_called_once_with("doThing")
    assert result.get_name() == "doThing"


def test_package_is_registered_for_meta_class_package() -> None:
    fake = make_fake_element("Package", getName="MyPkg")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPPackage)


def test_package_get_nested_packages_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    nested1 = make_fake_element("Package", getName="Nested1")
    nested2 = make_fake_element("Package", getName="Nested2")
    fake.getPackages.return_value = make_fake_collection([nested1, nested2])
    package = RPPackage(fake)

    result = package.get_nested_packages()

    fake.getPackages.assert_called_once_with()
    assert isinstance(result, RPCollection)
    assert len(result) == 2
    assert result[0].get_name() == "Nested1"
    assert result[1].get_name() == "Nested2"


def test_package_get_classes_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    class1 = make_fake_element("Class", getName="Class1")
    class2 = make_fake_element("Class", getName="Class2")
    fake.getClasses.return_value = make_fake_collection([class1, class2])
    package = RPPackage(fake)

    result = package.get_classes()

    fake.getClasses.assert_called_once_with()
    assert isinstance(result, RPCollection)
    assert len(result) == 2


def test_package_get_actors_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    actor1 = make_fake_element("Actor", getName="Actor1")
    fake.getActors.return_value = make_fake_collection([actor1])
    package = RPPackage(fake)

    result = package.get_actors()

    fake.getActors.assert_called_once_with()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_package_get_use_cases_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    uc1 = make_fake_element("UseCase", getName="UC1")
    fake.getUseCases.return_value = make_fake_collection([uc1])
    package = RPPackage(fake)

    result = package.get_use_cases()

    fake.getUseCases.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_package_add_use_case_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    uc = make_fake_element("UseCase", getName="UC1")
    fake.addUseCase.return_value = uc
    package = RPPackage(fake)

    result = package.add_use_case("UC1")

    fake.addUseCase.assert_called_once_with("UC1")
    assert result.get_name() == "UC1"


def test_package_add_interface_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    iface = make_fake_element("Classifier", getName="IFoo")
    fake.addInterface.return_value = iface
    package = RPPackage(fake)

    result = package.add_interface("IFoo")

    fake.addInterface.assert_called_once_with("IFoo")
    assert result.get_name() == "IFoo"


def test_package_add_interface_returns_registered_wrapper() -> None:
    from rhapsody_cli.models.elements.classifiers import RPInterface

    fake = make_fake_element("Package")
    iface = make_fake_element("Interface", getName="IFoo")
    fake.addInterface.return_value = iface
    package = RPPackage(fake)

    result = package.add_interface("IFoo")

    assert isinstance(result, RPInterface)


def test_package_add_signal_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    sig = make_fake_element("Classifier", getName="Signal1")
    fake.addSignal.return_value = sig
    package = RPPackage(fake)

    package.add_signal("Signal1")

    fake.addSignal.assert_called_once_with("Signal1")


def test_package_add_signal_returns_registered_wrapper() -> None:
    from rhapsody_cli.models.elements.classifiers import RPSignal

    fake = make_fake_element("Package")
    sig = make_fake_element("Signal", getName="Signal1")
    fake.addSignal.return_value = sig
    package = RPPackage(fake)

    result = package.add_signal("Signal1")

    assert isinstance(result, RPSignal)


def test_package_add_exception_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    exc = make_fake_element("Classifier", getName="Exception1")
    fake.addException.return_value = exc
    package = RPPackage(fake)

    package.add_exception("Exception1")

    fake.addException.assert_called_once_with("Exception1")


def test_package_add_exception_returns_registered_wrapper() -> None:
    from rhapsody_cli.models.elements.classifiers import RPException

    fake = make_fake_element("Package")
    exc = make_fake_element("Exception", getName="Exception1")
    fake.addException.return_value = exc
    package = RPPackage(fake)

    result = package.add_exception("Exception1")

    assert isinstance(result, RPException)


def test_package_add_enumeration_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    enum = make_fake_element("Classifier", getName="Enum1")
    fake.addEnumeration.return_value = enum
    package = RPPackage(fake)

    package.add_enumeration("Enum1")

    fake.addEnumeration.assert_called_once_with("Enum1")


def test_package_add_enumeration_returns_registered_wrapper() -> None:
    from rhapsody_cli.models.elements.classifiers import RPEnumeration

    fake = make_fake_element("Package")
    enum = make_fake_element("Enumeration", getName="Enum1")
    fake.addEnumeration.return_value = enum
    package = RPPackage(fake)

    result = package.add_enumeration("Enum1")

    assert isinstance(result, RPEnumeration)


def test_package_get_enumerations_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    enum1 = make_fake_element("Classifier", getName="Enum1")
    fake.getEnumerations.return_value = make_fake_collection([enum1])
    package = RPPackage(fake)

    result = package.get_enumerations()

    assert isinstance(result, RPCollection)


# --- New diagram tests ---
def test_package_add_activity_diagram_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    diagram = make_fake_element("ActivityDiagram", getName="Activity1")
    fake.addActivityDiagram.return_value = diagram
    package = RPPackage(fake)

    result = package.add_activity_diagram("Activity1")

    fake.addActivityDiagram.assert_called_once_with("Activity1")
    assert result.get_name() == "Activity1"


def test_package_add_sequence_diagram_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    diagram = make_fake_element("SequenceDiagram", getName="Seq1")
    fake.addSequenceDiagram.return_value = diagram
    package = RPPackage(fake)

    result = package.add_sequence_diagram("Seq1")

    fake.addSequenceDiagram.assert_called_once_with("Seq1")
    assert result.get_name() == "Seq1"


def test_package_get_sequence_diagrams_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    diagram = make_fake_element("SequenceDiagram", getName="Seq1")
    fake.getSequenceDiagrams.return_value = make_fake_collection([diagram])
    package = RPPackage(fake)

    result = package.get_sequence_diagrams()

    fake.getSequenceDiagrams.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_package_delete_class_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)
    cls_fake = make_fake_element("Class", getName="ToDelete")

    package.delete_class(RPUnit(cls_fake))

    fake.deleteClass.assert_called_once_with(cls_fake)


def test_package_delete_package_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)
    nested_fake = make_fake_element("Package", getName="Nested")

    package.delete_package(RPUnit(nested_fake))

    fake.deletePackage.assert_called_once_with(nested_fake)


def test_package_find_class_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    found = make_fake_element("Class", getName="MyClass")
    fake.findClass.return_value = found
    package = RPPackage(fake)

    result = package.find_class("MyClass")

    fake.findClass.assert_called_once_with("MyClass")
    assert result.get_name() == "MyClass"


def test_package_find_nested_package_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    nested = make_fake_element("Package", getName="NestedPkg")
    fake.findNestedPackage.return_value = nested
    package = RPPackage(fake)

    result = package.find_nested_package("NestedPkg")

    fake.findNestedPackage.assert_called_once_with("NestedPkg")
    assert result.get_name() == "NestedPkg"


def test_package_add_association_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    assoc = make_fake_element("Relation", getName="assoc1")
    fake.addAssociation.return_value = assoc
    package = RPPackage(fake)

    result = package.add_association("assoc1")

    fake.addAssociation.assert_called_once_with("assoc1")
    assert result.get_name() == "assoc1"


def test_package_get_associations_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    assoc = make_fake_element("Relation", getName="assoc1")
    fake.getAssociations.return_value = make_fake_collection([assoc])
    package = RPPackage(fake)

    result = package.get_associations()

    assert isinstance(result, RPCollection)


def test_package_get_events_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    event = make_fake_element("Event", getName="Event1")
    fake.getEvents.return_value = make_fake_collection([event])
    package = RPPackage(fake)

    result = package.get_events()

    assert isinstance(result, RPCollection)


def test_package_get_nodes_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    node = make_fake_element("Node", getName="Node1")
    fake.getNodes.return_value = make_fake_collection([node])
    package = RPPackage(fake)

    result = package.get_nodes()

    assert isinstance(result, RPCollection)


def test_package_add_flow_items_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    flow_item = make_fake_element("FlowItem", getName="MyFlowItem")
    fake.addFlowItems.return_value = flow_item
    package = RPPackage(fake)

    result = package.add_flow_items("MyFlowItem")

    fake.addFlowItems.assert_called_once_with("MyFlowItem")
    assert result.get_name() == "MyFlowItem"


def test_package_add_flows_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    flow = make_fake_element("Flow", getName="MyFlow")
    fake.addFlows.return_value = flow
    package = RPPackage(fake)

    result = package.add_flows("MyFlow")

    fake.addFlows.assert_called_once_with("MyFlow")
    assert result.get_name() == "MyFlow"


def test_package_delete_flow_items_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPModelElement

    fake = make_fake_element("Package")
    package = RPPackage(fake)
    flow_item_fake = make_fake_element("FlowItem", getName="ToDelete")

    package.delete_flow_items(RPModelElement(flow_item_fake))

    fake.deleteFlowItems.assert_called_once_with(flow_item_fake)


def test_package_delete_flows_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPModelElement

    fake = make_fake_element("Package")
    package = RPPackage(fake)
    flow_fake = make_fake_element("Flow", getName="ToDelete")

    package.delete_flows(RPModelElement(flow_fake))

    fake.deleteFlows.assert_called_once_with(flow_fake)


def test_package_get_flow_items_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    flow_item = make_fake_element("FlowItem", getName="FlowItem1")
    fake.getFlowItems.return_value = make_fake_collection([flow_item])
    package = RPPackage(fake)

    result = package.get_flow_items()

    fake.getFlowItems.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_package_get_flows_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    flow = make_fake_element("Flow", getName="Flow1")
    fake.getFlows.return_value = make_fake_collection([flow])
    package = RPPackage(fake)

    result = package.get_flows()

    fake.getFlows.assert_called_once_with()
    assert isinstance(result, RPCollection)


# --- Remote Requirements Methods (Task 3) Tests ---
def test_package_get_remote_requirements_populate_mode_returns_int() -> None:
    fake = make_fake_element("Package")
    fake.getRemoteRequirementsPopulateMode.return_value = 1
    package = RPPackage(fake)

    result = package.get_remote_requirements_populate_mode()

    fake.getRemoteRequirementsPopulateMode.assert_called_once_with()
    assert result == 1


def test_package_get_root_instance_specifications_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    instance_spec = make_fake_element("InstanceSpecification", getName="IS1")
    fake.getRootInstanceSpecifications.return_value = make_fake_collection([instance_spec])
    package = RPPackage(fake)

    result = package.get_root_instance_specifications()

    fake.getRootInstanceSpecifications.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_package_login_to_remote_artifact_server_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)

    package.login_to_remote_artifact_server("http://server.com", "user", "pass")

    fake.loginToRemoteArtifactServer.assert_called_once_with("http://server.com", "user", "pass")


def test_package_populate_remote_requirements_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)

    package.populate_remote_requirements()

    fake.populateRemoteRequirements.assert_called_once_with()


def test_package_recalculate_events_base_id_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)

    package.recalculate_events_base_id()

    fake.reCalculateEventsBaseId.assert_called_once_with()


def test_package_set_remote_requirements_populate_mode_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)

    package.set_remote_requirements_populate_mode(2)

    fake.setRemoteRequirementsPopulateMode.assert_called_once_with(2)


def test_package_update_contained_diagrams_on_server_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)

    package.update_contained_diagrams_on_server()

    fake.updateContainedDiagramsOnServer.assert_called_once_with()


# --- SysML Methods (Task 4) Tests ---
def test_package_add_implicit_object_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    instance = make_fake_element("Instance", getName="ImplicitObj")
    fake.addImplicitObject.return_value = instance
    package = RPPackage(fake)

    result = package.add_implicit_object("ImplicitObj")

    fake.addImplicitObject.assert_called_once_with("ImplicitObj")
    assert result.get_name() == "ImplicitObj"


def test_package_add_link_between_sysml_ports_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPModelElement

    fake = make_fake_element("Package")
    port1_fake = make_fake_element("SysMLPort", getName="Port1")
    port2_fake = make_fake_element("SysMLPort", getName="Port2")
    link_fake = make_fake_element("Link", getName="Link1")
    fake.addLinkBetweenSYSMLPorts.return_value = link_fake
    package = RPPackage(fake)

    result = package.add_link_between_sysml_ports(RPModelElement(port1_fake), RPModelElement(port2_fake))

    fake.addLinkBetweenSYSMLPorts.assert_called_once_with(port1_fake, port2_fake)
    assert result.get_name() == "Link1"


# --- Misc Methods (Task 5) Tests ---
def test_package_get_all_nested_elements_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    elem1 = make_fake_element("Class", getName="Class1")
    elem2 = make_fake_element("Package", getName="NestedPkg")
    fake.getAllNestedElements.return_value = make_fake_collection([elem1, elem2])
    package = RPPackage(fake)

    result = package.get_all_nested_elements()

    fake.getAllNestedElements.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_package_get_events_base_id_returns_string() -> None:
    fake = make_fake_element("Package")
    fake.getEventsBaseId.return_value = "EventsBase_123"
    package = RPPackage(fake)

    result = package.get_events_base_id()

    fake.getEventsBaseId.assert_called_once_with()
    assert result == "EventsBase_123"


def test_package_get_namespace_returns_string() -> None:
    fake = make_fake_element("Package")
    fake.getNamespace.return_value = "com.example.mypackage"
    package = RPPackage(fake)

    result = package.get_namespace()

    fake.getNamespace.assert_called_once_with()
    assert result == "com.example.mypackage"


def test_package_get_saved_in_separate_directory_returns_int() -> None:
    fake = make_fake_element("Package")
    fake.getSavedInSeperateDirectory.return_value = 1
    package = RPPackage(fake)

    result = package.get_saved_in_separate_directory()

    fake.getSavedInSeperateDirectory.assert_called_once_with()
    assert result == 1


def test_package_get_user_defined_stereotypes_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    stereotype = make_fake_element("Stereotype", getName="MyStereotype")
    fake.getUserDefinedStereotypes.return_value = make_fake_collection([stereotype])
    package = RPPackage(fake)

    result = package.get_user_defined_stereotypes()

    fake.getUserDefinedStereotypes.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_package_set_saved_in_separate_directory_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)

    package.set_saved_in_separate_directory(1)

    fake.setSavedInSeperateDirectory.assert_called_once_with(1)


def test_package_update_contained_matrices_on_server_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)

    package.update_contained_matrices_on_server()

    fake.updateContainedMatricesOnServer.assert_called_once_with()


def test_package_update_contained_tables_on_server_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    package = RPPackage(fake)

    package.update_contained_tables_on_server()

    fake.updateContainedTablesOnServer.assert_called_once_with()
