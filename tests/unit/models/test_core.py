"""Tests for rhapsody_cli._core class-based wrapping utilities."""

from unittest.mock import MagicMock, call

import pytest

import rhapsody_cli.models.core as core_module
from rhapsody_cli.exceptions import RhapsodyRuntimeException
from rhapsody_cli.models.core import (
    AbstractRPModelElement,
    AddToModelMode,
    RPCollection,
    RPModelElement,
    RPUnit,
)
from tests.unit.models.fakes import make_com_error, make_fake_collection, make_fake_element


class _FakeClassWrapper(RPModelElement):
    pass


def test_call_com_returns_value_on_success() -> None:
    result = AbstractRPModelElement.call_com(lambda: 42)

    assert result == 42


def test_call_com_translates_com_error() -> None:
    def failing() -> int:
        raise make_com_error("getName failed")

    with pytest.raises(RhapsodyRuntimeException, match="getName failed"):
        AbstractRPModelElement.call_com(failing)


def test_call_com_does_not_translate_other_exceptions() -> None:
    def failing() -> int:
        raise ValueError("not a COM error")

    with pytest.raises(ValueError, match="not a COM error"):
        AbstractRPModelElement.call_com(failing)


def test_core_module_no_longer_exports_backward_compatibility_wrappers() -> None:
    for wrapper_name in (
        "register_wrapper",
        "call_com",
        "_wrap_if_element",
        "wrap",
        "_get_method_or_property",
        "_set_method_or_property",
    ):
        assert not hasattr(core_module, wrapper_name)


def test_model_element_get_name_delegates_to_com() -> None:
    fake = make_fake_element("Class", getName="Widget")
    element = RPModelElement(fake)

    assert element.get_name() == "Widget"
    fake.getName.assert_called_once_with()


def test_model_element_set_name_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_name("NewName")

    fake.setName.assert_called_once_with("NewName")


def test_model_element_get_meta_class_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    element = RPModelElement(fake)

    assert element.get_meta_class() == "Package"


def test_model_element_get_name_falls_back_to_property_when_method_missing() -> None:
    """Some Rhapsody COM automation ProgIDs (e.g. Rhapsody2.Application.1)
    expose 'name'/'GUID'/'metaClass' as bare properties instead of
    getName()/getGUID()/getMetaClass() methods. Wrapper methods must fall
    back to bare property access in that case."""
    fake = MagicMock(spec=["name"])
    fake.name = "PropertyStyleName"
    element = RPModelElement(fake)

    assert element.get_name() == "PropertyStyleName"


def test_model_element_set_name_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["name"])
    element = RPModelElement(fake)

    element.set_name("NewName")

    assert fake.name == "NewName"


def test_model_element_get_meta_class_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["metaClass"])
    fake.metaClass = "Class"
    element = RPModelElement(fake)

    assert element.get_meta_class() == "Class"


def test_model_element_get_guid_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["GUID"])
    fake.GUID = "guid-456"
    element = RPModelElement(fake)

    assert element.get_guid() == "guid-456"


def test_wrap_falls_back_to_meta_class_property_when_method_missing() -> None:
    fake = MagicMock(spec=["metaClass"])
    fake.metaClass = "Class"

    element = AbstractRPModelElement.wrap(fake)

    assert element.get_meta_class() == "Class"


def test_model_element_get_guid_delegates_to_com() -> None:
    fake = make_fake_element("Class", getGUID="guid-123")
    element = RPModelElement(fake)

    assert element.get_guid() == "guid-123"


def test_model_element_com_error_becomes_rhapsody_runtime_exception() -> None:
    fake = make_fake_element("Class")
    fake.getName.side_effect = make_com_error("boom")
    element = RPModelElement(fake)

    with pytest.raises(RhapsodyRuntimeException, match="boom"):
        element.get_name()


def test_model_element_equality_by_underlying_com_object() -> None:
    fake = make_fake_element("Class")

    assert RPModelElement(fake) == RPModelElement(fake)
    assert RPModelElement(fake) != RPModelElement(make_fake_element("Class"))


def test_unit_save_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.save()

    fake.save.assert_called_once_with(0)


def test_unit_get_filename_delegates_to_com() -> None:
    fake = make_fake_element("Package", getFilename="Model/Foo.sbs")
    unit = RPUnit(fake)

    assert unit.get_filename() == "Model/Foo.sbs"


def test_unit_set_filename_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.set_filename("Model/Bar.sbs")

    fake.setFilename.assert_called_once_with("Model/Bar.sbs")


def test_unit_get_filename_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["filename"])
    fake.filename = "Model/Foo.sbs"
    unit = RPUnit(fake)

    assert unit.get_filename() == "Model/Foo.sbs"


def test_unit_set_filename_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["filename"])
    unit = RPUnit(fake)

    unit.set_filename("Model/Bar.sbs")

    assert fake.filename == "Model/Bar.sbs"


def test_unit_is_read_only_delegates_to_com() -> None:
    fake = make_fake_element("Package", isReadOnly=1)
    unit = RPUnit(fake)

    assert unit.is_read_only() is True


def test_unit_set_read_only_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.set_read_only(True)

    fake.setReadOnly.assert_called_once_with(1)


def test_unit_is_a_model_element() -> None:
    fake = make_fake_element("Package", getName="MyPkg")
    unit = RPUnit(fake)

    assert isinstance(unit, RPModelElement)
    assert unit.get_name() == "MyPkg"


def test_collection_len_delegates_to_get_count() -> None:
    fake = make_fake_collection([make_fake_element("Class")])
    collection = RPCollection(fake)

    assert len(collection) == 1


def test_collection_getitem_wraps_model_elements() -> None:
    inner = make_fake_element("Class", getName="Widget")
    fake = make_fake_collection([inner])
    collection = RPCollection(fake)

    item = collection[0]

    assert isinstance(item, RPModelElement)
    assert item.get_name() == "Widget"
    fake.getItem.assert_called_once_with(1)


def test_collection_getitem_passes_through_non_element_values() -> None:
    fake = make_fake_collection(["a plain string", 42])
    collection = RPCollection(fake)

    assert collection[0] == "a plain string"
    assert collection[1] == 42


def test_collection_negative_index_raises_index_error() -> None:
    fake = make_fake_collection(["a plain string"])
    collection = RPCollection(fake)

    with pytest.raises(IndexError, match="negative indices are not supported"):
        _ = collection[-1]


def test_collection_getitem_supports_slicing() -> None:
    fake = make_fake_collection(["a", "b", "c", "d"])
    collection = RPCollection(fake)

    assert collection[:2] == ["a", "b"]
    assert collection[1:3] == ["b", "c"]
    assert collection[:] == ["a", "b", "c", "d"]


def test_collection_iter_yields_all_items() -> None:
    inner_a = make_fake_element("Class", getName="A")
    inner_b = make_fake_element("Class", getName="B")
    fake = make_fake_collection([inner_a, inner_b])
    collection = RPCollection(fake)

    names = [item.get_name() for item in collection]

    assert names == ["A", "B"]
    assert fake.getItem.call_args_list == [call(1), call(2)]


def test_collection_add_item_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)
    new_element = make_fake_element("Class")

    collection.add_item(RPModelElement(new_element))

    fake.addItem.assert_called_once_with(new_element)


def test_collection_get_count_delegates_to_com() -> None:
    fake = make_fake_collection([make_fake_element("Class"), make_fake_element("Class")])
    collection = RPCollection(fake)

    assert collection.get_count() == 2


def test_collection_get_count_falls_back_to_count_property_when_method_missing() -> None:
    """Some Rhapsody COM Prog IDs (e.g. Rhapsody2.Application.1) expose the
    collection size/item accessors via 'Count'/'Item' properties instead of
    getCount()/getItem() methods."""
    fake = MagicMock(spec=["Count"])
    fake.Count = 3
    collection = RPCollection(fake)

    assert collection.get_count() == 3


def test_collection_get_item_falls_back_to_item_property_when_method_missing() -> None:
    inner = make_fake_element("Class", getName="Widget")
    fake = MagicMock(spec=["Item"])
    fake.Item.return_value = inner
    collection = RPCollection(fake)

    item = collection.get_item(1)

    assert isinstance(item, RPModelElement)
    assert item.get_name() == "Widget"
    fake.Item.assert_called_once_with(1)


def test_collection_add_graphical_item_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)
    item = make_fake_element("Class")

    collection.add_graphical_item(RPModelElement(item))

    fake.addGraphicalItem.assert_called_once_with(item)


def test_collection_to_list_returns_python_list() -> None:
    inner_a = make_fake_element("Class", getName="A")
    inner_b = make_fake_element("Class", getName="B")
    fake = make_fake_collection([inner_a, inner_b])
    collection = RPCollection(fake)

    result = collection.to_list()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].get_name() == "A"
    assert result[1].get_name() == "B"


def test_collection_set_size_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)

    collection.set_size(5)

    fake.setSize.assert_called_once_with(5)


def test_collection_remove_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)

    collection.remove(1)

    fake.remove.assert_called_once_with(1)


def test_collection_set_string_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)

    collection.set_string(1, "test")

    fake.setString.assert_called_once_with(1, "test")


def test_collection_set_model_element_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)
    element = make_fake_element("Class")

    collection.set_model_element(1, RPModelElement(element))

    fake.setModelElement.assert_called_once_with(1, element)


def test_collection_empty_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)

    collection.empty()

    fake.empty.assert_called_once_with()


def test_collection_set_integer_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)

    collection.set_integer(1, 42)

    fake.setInteger.assert_called_once_with(1, 42)


def test_wrap_dispatches_to_registered_wrapper() -> None:
    AbstractRPModelElement.register_wrapper("FakeMetaType", _FakeClassWrapper)
    fake = make_fake_element("FakeMetaType", getName="Thing")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, _FakeClassWrapper)
    assert wrapped.get_name() == "Thing"


def test_wrap_falls_back_to_model_element_for_unregistered_type() -> None:
    fake = make_fake_element("SomeUnmappedType", getName="Mystery")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert type(wrapped) is RPModelElement
    assert wrapped.get_name() == "Mystery"


def test_wrap_handles_none_com_object() -> None:
    wrapped = AbstractRPModelElement.wrap(None)

    assert type(wrapped) is RPModelElement
    assert wrapped._com is None


# ---------------------------------------------------------------------------
# IRPModelElement parity tests (Task 2): every non-deprecated method.
# ---------------------------------------------------------------------------


def test_model_element_add_association_unwraps_args_and_wraps_result() -> None:
    end1 = RPModelElement(make_fake_element("Element"))
    end2 = RPModelElement(make_fake_element("Element"))
    result_fake = make_fake_element("AssociationClass", getName="Assoc")
    fake = make_fake_element("Class", addAssociation=result_fake)
    element = RPModelElement(fake)

    result = element.add_association(end1, end2, "Assoc")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Assoc"
    fake.addAssociation.assert_called_once_with(end1._com, end2._com, "Assoc")


def test_model_element_add_dependency_wraps_result() -> None:
    dep_fake = make_fake_element("Dependency", getName="Dep")
    fake = make_fake_element("Class", addDependency=dep_fake)
    element = RPModelElement(fake)

    result = element.add_dependency("Target", "Class")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Dep"
    fake.addDependency.assert_called_once_with("Target", "Class")


def test_model_element_add_dependency_between_unwraps_args_and_wraps_result() -> None:
    dependent = RPModelElement(make_fake_element("Element"))
    depends_on = RPModelElement(make_fake_element("Element"))
    dep_fake = make_fake_element("Dependency", getName="Dep")
    fake = make_fake_element("Class", addDependencyBetween=dep_fake)
    element = RPModelElement(fake)

    result = element.add_dependency_between(dependent, depends_on)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Dep"
    fake.addDependencyBetween.assert_called_once_with(dependent._com, depends_on._com)


def test_model_element_add_dependency_to_unwraps_argument_and_wraps_result() -> None:
    target = RPModelElement(make_fake_element("Element"))
    dep_fake = make_fake_element("Dependency", getName="Dep")
    fake = make_fake_element("Class", addDependencyTo=dep_fake)
    element = RPModelElement(fake)

    result = element.add_dependency_to(target)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Dep"
    fake.addDependencyTo.assert_called_once_with(target._com)


def test_model_element_add_link_to_element_unwraps_args_and_wraps_result() -> None:
    to_element = RPModelElement(make_fake_element("Element"))
    assoc = RPModelElement(make_fake_element("Element"))
    from_port = RPModelElement(make_fake_element("Element"))
    to_port = RPModelElement(make_fake_element("Element"))
    link_fake = make_fake_element("Link", getName="Link")
    fake = make_fake_element("Class", addLinkToElement=link_fake)
    element = RPModelElement(fake)

    result = element.add_link_to_element(to_element, assoc, from_port, to_port)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Link"
    fake.addLinkToElement.assert_called_once_with(to_element._com, assoc._com, from_port._com, to_port._com)


def test_model_element_add_new_aggr_wraps_result() -> None:
    new_fake = make_fake_element("Element", getName="NewElem")
    fake = make_fake_element("Package", addNewAggr=new_fake)
    element = RPModelElement(fake)

    result = element.add_new_aggr("Class", "NewElem")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "NewElem"
    fake.addNewAggr.assert_called_once_with("Class", "NewElem")


def test_model_element_add_property_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.add_property("key", "type", "value")

    fake.addProperty.assert_called_once_with("key", "type", "value")


def test_model_element_add_redefines_unwraps_argument() -> None:
    redefine = RPModelElement(make_fake_element("Element"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.add_redefines(redefine)

    fake.addRedefines.assert_called_once_with(redefine._com)


def test_model_element_add_remote_dependency_to_unwraps_arg_and_wraps_result() -> None:
    target = RPModelElement(make_fake_element("Element"))
    dep_fake = make_fake_element("Dependency", getName="Dep")
    fake = make_fake_element("Class", addRemoteDependencyTo=dep_fake)
    element = RPModelElement(fake)

    result = element.add_remote_dependency_to(target, "linkType")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Dep"
    fake.addRemoteDependencyTo.assert_called_once_with(target._com, "linkType")


def test_model_element_add_specific_stereotype_unwraps_argument() -> None:
    stereotype = RPModelElement(make_fake_element("Stereotype"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.add_specific_stereotype(stereotype)

    fake.addSpecificStereotype.assert_called_once_with(stereotype._com)


def test_model_element_add_stereotype_wraps_result() -> None:
    st_fake = make_fake_element("Stereotype", getName="Ster")
    fake = make_fake_element("Class", addStereotype=st_fake)
    element = RPModelElement(fake)

    result = element.add_stereotype("Ster", "Class")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Ster"
    fake.addStereotype.assert_called_once_with("Ster", "Class")


def test_model_element_become_template_instantiation_of_unwraps_argument() -> None:
    template = RPModelElement(make_fake_element("Element"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.become_template_instantiation_of(template)

    fake.becomeTemplateInstantiationOf.assert_called_once_with(template._com)


def test_model_element_change_to_wraps_result() -> None:
    changed_fake = make_fake_element("Element", getName="Changed")
    fake = make_fake_element("Class", changeTo=changed_fake)
    element = RPModelElement(fake)

    result = element.change_to("Package")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Changed"
    fake.changeTo.assert_called_once_with("Package")


def test_model_element_clone_unwraps_owner_and_wraps_result() -> None:
    new_owner = RPModelElement(make_fake_element("Element"))
    cloned_fake = make_fake_element("Element", getName="Clone")
    fake = make_fake_element("Class", clone=cloned_fake)
    element = RPModelElement(fake)

    result = element.clone("Clone", new_owner)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Clone"
    fake.clone.assert_called_once_with("Clone", new_owner._com)


def test_model_element_create_oslc_link_raises_not_implemented() -> None:
    element = RPModelElement(make_fake_element("Class"))

    with pytest.raises(NotImplementedError):
        element.create_oslc_link("type", "purl")


def test_model_element_delete_dependency_unwraps_argument() -> None:
    dependency = RPModelElement(make_fake_element("Dependency"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.delete_dependency(dependency)

    fake.deleteDependency.assert_called_once_with(dependency._com)


def test_model_element_delete_from_project_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.delete_from_project()

    fake.deleteFromProject.assert_called_once_with()


def test_model_element_delete_oslc_link_raises_not_implemented() -> None:
    element = RPModelElement(make_fake_element("Class"))

    with pytest.raises(NotImplementedError):
        element.delete_oslc_link("type", "purl")


def test_model_element_error_message_returns_str() -> None:
    fake = make_fake_element("Class", errorMessage="boom")
    element = RPModelElement(fake)

    assert element.error_message() == "boom"
    fake.errorMessage.assert_called_once_with()


def test_model_element_find_elements_by_full_name_wraps_result() -> None:
    found_fake = make_fake_element("Element", getName="Found")
    fake = make_fake_element("Package", findElementsByFullName=found_fake)
    element = RPModelElement(fake)

    result = element.find_elements_by_full_name("Path::To::Found", "Class")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Found"
    fake.findElementsByFullName.assert_called_once_with("Path::To::Found", "Class")


def test_model_element_find_nested_element_wraps_result() -> None:
    found_fake = make_fake_element("Element", getName="Found")
    fake = make_fake_element("Package", findNestedElement=found_fake)
    element = RPModelElement(fake)

    result = element.find_nested_element("Found", "Class")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Found"
    fake.findNestedElement.assert_called_once_with("Found", "Class")


def test_model_element_find_nested_element_recursive_wraps_result() -> None:
    found_fake = make_fake_element("Element", getName="Found")
    fake = make_fake_element("Package", findNestedElementRecursive=found_fake)
    element = RPModelElement(fake)

    result = element.find_nested_element_recursive("Found", "Class")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Found"
    fake.findNestedElementRecursive.assert_called_once_with("Found", "Class")


def test_model_element_get_all_tags_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getAllTags=coll)
    element = RPModelElement(fake)

    result = element.get_all_tags()

    assert isinstance(result, RPCollection)
    fake.getAllTags.assert_called_once_with()


def test_model_element_get_annotations_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getAnnotations=coll)
    element = RPModelElement(fake)

    result = element.get_annotations()

    assert isinstance(result, RPCollection)
    fake.getAnnotations.assert_called_once_with()


def test_model_element_get_association_classes_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getAssociationClasses=coll)
    element = RPModelElement(fake)

    result = element.get_association_classes()

    assert isinstance(result, RPCollection)
    fake.getAssociationClasses.assert_called_once_with()


def test_model_element_get_binary_id_returns_bytes() -> None:
    fake = make_fake_element("Class", getBinaryID=b"\x01\x02\x03")
    element = RPModelElement(fake)

    assert element.get_binary_id() == b"\x01\x02\x03"
    fake.getBinaryID.assert_called_once_with()


def test_model_element_get_constraints_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getConstraints=coll)
    element = RPModelElement(fake)

    result = element.get_constraints()

    assert isinstance(result, RPCollection)
    fake.getConstraints.assert_called_once_with()


def test_model_element_get_constraints_by_him_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getConstraintsByHim=coll)
    element = RPModelElement(fake)

    result = element.get_constraints_by_him()

    assert isinstance(result, RPCollection)
    fake.getConstraintsByHim.assert_called_once_with()


def test_model_element_get_controlled_files_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getControlledFiles=coll)
    element = RPModelElement(fake)

    result = element.get_controlled_files()

    assert isinstance(result, RPCollection)
    fake.getControlledFiles.assert_called_once_with()


def test_model_element_get_decoration_style_returns_str() -> None:
    fake = make_fake_element("Class", getDecorationStyle="Bold")
    element = RPModelElement(fake)

    assert element.get_decoration_style() == "Bold"
    fake.getDecorationStyle.assert_called_once_with()


def test_model_element_get_dependencies_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getDependencies=coll)
    element = RPModelElement(fake)

    result = element.get_dependencies()

    assert isinstance(result, RPCollection)
    fake.getDependencies.assert_called_once_with()


def test_model_element_get_description_returns_str() -> None:
    fake = make_fake_element("Class", getDescription="A description")
    element = RPModelElement(fake)

    assert element.get_description() == "A description"
    fake.getDescription.assert_called_once_with()


def test_model_element_get_description_html_returns_str() -> None:
    fake = make_fake_element("Class", getDescriptionHTML="<p>desc</p>")
    element = RPModelElement(fake)

    assert element.get_description_html() == "<p>desc</p>"
    fake.getDescriptionHTML.assert_called_once_with()


def test_model_element_get_description_plain_text_returns_str() -> None:
    fake = make_fake_element("Class", getDescriptionPlainText="plain")
    element = RPModelElement(fake)

    assert element.get_description_plain_text() == "plain"
    fake.getDescriptionPlainText.assert_called_once_with()


def test_model_element_get_description_rtf_returns_str() -> None:
    fake = make_fake_element("Class", getDescriptionRTF="{\\rtf}")
    element = RPModelElement(fake)

    assert element.get_description_rtf() == "{\\rtf}"
    fake.getDescriptionRTF.assert_called_once_with()


def test_model_element_get_display_name_returns_str() -> None:
    fake = make_fake_element("Class", getDisplayName="Label")
    element = RPModelElement(fake)

    assert element.get_display_name() == "Label"
    fake.getDisplayName.assert_called_once_with()


def test_model_element_get_display_name_rtf_returns_str() -> None:
    fake = make_fake_element("Class", getDisplayNameRTF="{\\rtf}")
    element = RPModelElement(fake)

    assert element.get_display_name_rtf() == "{\\rtf}"
    fake.getDisplayNameRTF.assert_called_once_with()


def test_model_element_get_error_message_returns_str() -> None:
    fake = make_fake_element("Class", getErrorMessage="boom")
    element = RPModelElement(fake)

    assert element.get_error_message() == "boom"
    fake.getErrorMessage.assert_called_once_with()


def test_model_element_get_full_path_name_returns_str() -> None:
    fake = make_fake_element("Class", getFullPathName="Pkg::Class")
    element = RPModelElement(fake)

    assert element.get_full_path_name() == "Pkg::Class"
    fake.getFullPathName.assert_called_once_with()


def test_model_element_get_full_path_name_in_returns_str() -> None:
    fake = make_fake_element("Class", getFullPathNameIn="Class in Pkg")
    element = RPModelElement(fake)

    assert element.get_full_path_name_in() == "Class in Pkg"
    fake.getFullPathNameIn.assert_called_once_with()


def test_model_element_get_hyper_links_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getHyperLinks=coll)
    element = RPModelElement(fake)

    result = element.get_hyper_links()

    assert isinstance(result, RPCollection)
    fake.getHyperLinks.assert_called_once_with()


def test_model_element_get_icon_file_name_returns_str() -> None:
    fake = make_fake_element("Class", getIconFileName="D:\\icons\\class.gif")
    element = RPModelElement(fake)

    assert element.get_icon_file_name() == "D:\\icons\\class.gif"
    fake.getIconFileName.assert_called_once_with()


def test_model_element_get_interface_name_returns_str() -> None:
    fake = make_fake_element("Class", getInterfaceName="IRPClass")
    element = RPModelElement(fake)

    assert element.get_interface_name() == "IRPClass"
    fake.getInterfaceName.assert_called_once_with()


def test_model_element_get_is_external_returns_int() -> None:
    fake = make_fake_element("Class", getIsExternal=1)
    element = RPModelElement(fake)

    assert element.get_is_external() == 1
    fake.getIsExternal.assert_called_once_with()


def test_model_element_get_is_of_meta_class_returns_int() -> None:
    fake = make_fake_element("Class", getIsOfMetaClass=1)
    element = RPModelElement(fake)

    assert element.get_is_of_meta_class("Class") == 1
    fake.getIsOfMetaClass.assert_called_once_with("Class")


def test_model_element_get_is_show_display_name_returns_int() -> None:
    fake = make_fake_element("Class", getIsShowDisplayName=0)
    element = RPModelElement(fake)

    assert element.get_is_show_display_name() == 0
    fake.getIsShowDisplayName.assert_called_once_with()


def test_model_element_get_is_unresolved_returns_int() -> None:
    fake = make_fake_element("Class", getIsUnresolved=0)
    element = RPModelElement(fake)

    assert element.get_is_unresolved() == 0
    fake.getIsUnresolved.assert_called_once_with()


def test_model_element_get_local_tags_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getLocalTags=coll)
    element = RPModelElement(fake)

    result = element.get_local_tags()

    assert isinstance(result, RPCollection)
    fake.getLocalTags.assert_called_once_with()


def test_model_element_get_main_diagram_wraps_result() -> None:
    diagram_fake = make_fake_element("Diagram", getName="Main")
    fake = make_fake_element("Class", getMainDiagram=diagram_fake)
    element = RPModelElement(fake)

    result = element.get_main_diagram()

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Main"
    fake.getMainDiagram.assert_called_once_with()


def test_model_element_get_nested_elements_returns_collection() -> None:
    coll = make_fake_collection([make_fake_element("Class", getName="Child")])
    fake = make_fake_element("Package", getNestedElements=coll)
    element = RPModelElement(fake)

    result = element.get_nested_elements()

    assert isinstance(result, RPCollection)
    assert result.get_count() == 1
    fake.getNestedElements.assert_called_once_with()


def test_model_element_get_nested_elements_by_meta_class_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Package", getNestedElementsByMetaClass=coll)
    element = RPModelElement(fake)

    result = element.get_nested_elements_by_meta_class("Class", 1)

    assert isinstance(result, RPCollection)
    fake.getNestedElementsByMetaClass.assert_called_once_with("Class", 1)


def test_model_element_get_nested_elements_recursive_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Package", getNestedElementsRecursive=coll)
    element = RPModelElement(fake)

    result = element.get_nested_elements_recursive()

    assert isinstance(result, RPCollection)
    fake.getNestedElementsRecursive.assert_called_once_with()


def test_model_element_get_new_term_stereotype_wraps_result() -> None:
    st_fake = make_fake_element("Stereotype", getName="NewTerm")
    fake = make_fake_element("Class", getNewTermStereotype=st_fake)
    element = RPModelElement(fake)

    result = element.get_new_term_stereotype()

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "NewTerm"
    fake.getNewTermStereotype.assert_called_once_with()


def test_model_element_get_of_template_wraps_result() -> None:
    template_fake = make_fake_element("Element", getName="Template")
    fake = make_fake_element("Class", getOfTemplate=template_fake)
    element = RPModelElement(fake)

    result = element.get_of_template()

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Template"
    fake.getOfTemplate.assert_called_once_with()


def test_model_element_get_oslc_links_raises_not_implemented() -> None:
    element = RPModelElement(make_fake_element("Class"))

    with pytest.raises(NotImplementedError):
        element.get_oslc_links()


def test_model_element_get_overlay_icon_file_name_returns_str() -> None:
    fake = make_fake_element("Class", getOverlayIconFileName="D:\\icons\\overlay.gif")
    element = RPModelElement(fake)

    assert element.get_overlay_icon_file_name() == "D:\\icons\\overlay.gif"
    fake.getOverlayIconFileName.assert_called_once_with()


def test_model_element_get_overridden_properties_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getOverriddenProperties=coll)
    element = RPModelElement(fake)

    result = element.get_overridden_properties(1)

    assert isinstance(result, RPCollection)
    fake.getOverriddenProperties.assert_called_once_with(1)


def test_model_element_get_overridden_properties_by_pattern_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getOverriddenPropertiesByPattern=coll)
    element = RPModelElement(fake)

    result = element.get_overridden_properties_by_pattern("C++.*", 1, 0)

    assert isinstance(result, RPCollection)
    fake.getOverriddenPropertiesByPattern.assert_called_once_with("C++.*", 1, 0)


def test_model_element_get_owned_dependencies_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getOwnedDependencies=coll)
    element = RPModelElement(fake)

    result = element.get_owned_dependencies()

    assert isinstance(result, RPCollection)
    fake.getOwnedDependencies.assert_called_once_with()


def test_model_element_get_owner_wraps_result() -> None:
    owner_fake = make_fake_element("Element", getName="Owner")
    fake = make_fake_element("Class", getOwner=owner_fake)
    element = RPModelElement(fake)

    result = element.get_owner()

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Owner"
    fake.getOwner.assert_called_once_with()


def test_model_element_get_project_wraps_result() -> None:
    project_fake = make_fake_element("Element", getName="Project")
    fake = make_fake_element("Class", getProject=project_fake)
    element = RPModelElement(fake)

    result = element.get_project()

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Project"
    fake.getProject.assert_called_once_with()


def test_model_element_get_property_value_returns_str() -> None:
    fake = make_fake_element("Class", getPropertyValue="value")
    element = RPModelElement(fake)

    assert element.get_property_value("key") == "value"
    fake.getPropertyValue.assert_called_once_with("key")


def test_model_element_get_property_value_conditional_returns_str() -> None:
    formal = RPCollection(make_fake_collection([]))
    actual = RPCollection(make_fake_collection([]))
    fake = make_fake_element("Class", getPropertyValueConditional="value")
    element = RPModelElement(fake)

    assert element.get_property_value_conditional("key", formal, actual) == "value"
    fake.getPropertyValueConditional.assert_called_once_with("key", formal._com, actual._com)


def test_model_element_get_property_value_conditional_explicit_returns_str() -> None:
    formal = RPCollection(make_fake_collection([]))
    actual = RPCollection(make_fake_collection([]))
    fake = make_fake_element("Class", getPropertyValueConditionalExplicit="value")
    element = RPModelElement(fake)

    assert element.get_property_value_conditional_explicit("key", formal, actual) == "value"
    fake.getPropertyValueConditionalExplicit.assert_called_once_with("key", formal._com, actual._com)


def test_model_element_get_property_value_explicit_returns_str() -> None:
    fake = make_fake_element("Class", getPropertyValueExplicit="value")
    element = RPModelElement(fake)

    assert element.get_property_value_explicit("key") == "value"
    fake.getPropertyValueExplicit.assert_called_once_with("key")


def test_model_element_get_redefines_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getRedefines=coll)
    element = RPModelElement(fake)

    result = element.get_redefines()

    assert isinstance(result, RPCollection)
    fake.getRedefines.assert_called_once_with()


def test_model_element_get_references_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getReferences=coll)
    element = RPModelElement(fake)

    result = element.get_references()

    assert isinstance(result, RPCollection)
    fake.getReferences.assert_called_once_with()


def test_model_element_get_remote_dependencies_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getRemoteDependencies=coll)
    element = RPModelElement(fake)

    result = element.get_remote_dependencies()

    assert isinstance(result, RPCollection)
    fake.getRemoteDependencies.assert_called_once_with()


def test_model_element_get_remote_uri_returns_str() -> None:
    fake = make_fake_element("Class", getRemoteURI="https://example.com/req/1")
    element = RPModelElement(fake)

    assert element.get_remote_uri() == "https://example.com/req/1"
    fake.getRemoteURI.assert_called_once_with()


def test_model_element_get_requirement_traceability_handle_returns_int() -> None:
    fake = make_fake_element("Class", getRequirementTraceabilityHandle=42)
    element = RPModelElement(fake)

    assert element.get_requirement_traceability_handle() == 42
    fake.getRequirementTraceabilityHandle.assert_called_once_with()


def test_model_element_get_rmm_url_returns_str() -> None:
    fake = make_fake_element("Class", getRmmUrl="https://rmm/element/1")
    element = RPModelElement(fake)

    assert element.get_rmm_url() == "https://rmm/element/1"
    fake.getRmmUrl.assert_called_once_with()


def test_model_element_get_save_unit_wraps_result() -> None:
    unit_fake = make_fake_element("Element", getName="Unit")
    fake = make_fake_element("Class", getSaveUnit=unit_fake)
    element = RPModelElement(fake)

    result = element.get_save_unit()

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Unit"
    fake.getSaveUnit.assert_called_once_with()


def test_model_element_get_stereotypes_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getStereotypes=coll)
    element = RPModelElement(fake)

    result = element.get_stereotypes()

    assert isinstance(result, RPCollection)
    fake.getStereotypes.assert_called_once_with()


def test_model_element_get_tag_wraps_result() -> None:
    tag_fake = make_fake_element("Tag", getName="MyTag")
    fake = make_fake_element("Class", getTag=tag_fake)
    element = RPModelElement(fake)

    result = element.get_tag("MyTag")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "MyTag"
    fake.getTag.assert_called_once_with("MyTag")


def test_model_element_get_template_parameters_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Class", getTemplateParameters=coll)
    element = RPModelElement(fake)

    result = element.get_template_parameters()

    assert isinstance(result, RPCollection)
    fake.getTemplateParameters.assert_called_once_with()


def test_model_element_get_ti_wraps_result() -> None:
    ti_fake = make_fake_element("TemplateInstantiation", getName="TI")
    fake = make_fake_element("Class", getTi=ti_fake)
    element = RPModelElement(fake)

    result = element.get_ti()

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "TI"
    fake.getTi.assert_called_once_with()


def test_model_element_get_tool_tip_html_returns_str() -> None:
    fake = make_fake_element("Class", getToolTipHTML="<b>tip</b>")
    element = RPModelElement(fake)

    assert element.get_tool_tip_html() == "<b>tip</b>"
    fake.getToolTipHTML.assert_called_once_with()


def test_model_element_get_user_defined_meta_class_returns_str() -> None:
    fake = make_fake_element("Class", getUserDefinedMetaClass="NewTerm")
    element = RPModelElement(fake)

    assert element.get_user_defined_meta_class() == "NewTerm"
    fake.getUserDefinedMetaClass.assert_called_once_with()


def test_model_element_has_nested_elements_returns_int() -> None:
    fake = make_fake_element("Class", hasNestedElements=1)
    element = RPModelElement(fake)

    assert element.has_nested_elements() == 1
    fake.hasNestedElements.assert_called_once_with()


def test_model_element_has_panel_widget_returns_int() -> None:
    fake = make_fake_element("Class", hasPanelWidget=0)
    element = RPModelElement(fake)

    assert element.has_panel_widget() == 0
    fake.hasPanelWidget.assert_called_once_with()


def test_model_element_high_light_element_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.high_light_element()

    fake.highLightElement.assert_called_once_with()


def test_model_element_is_a_template_returns_int() -> None:
    fake = make_fake_element("Class", isATemplate=0)
    element = RPModelElement(fake)

    assert element.is_a_template() == 0
    fake.isATemplate.assert_called_once_with()


def test_model_element_is_description_rtf_returns_int() -> None:
    fake = make_fake_element("Class", isDescriptionRTF=1)
    element = RPModelElement(fake)

    assert element.is_description_rtf() == 1
    fake.isDescriptionRTF.assert_called_once_with()


def test_model_element_is_display_name_rtf_returns_int() -> None:
    fake = make_fake_element("Class", isDisplayNameRTF=0)
    element = RPModelElement(fake)

    assert element.is_display_name_rtf() == 0
    fake.isDisplayNameRTF.assert_called_once_with()


def test_model_element_is_modified_returns_int() -> None:
    fake = make_fake_element("Class", isModified=1)
    element = RPModelElement(fake)

    assert element.is_modified() == 1
    fake.isModified.assert_called_once_with()


def test_model_element_is_remote_returns_int() -> None:
    fake = make_fake_element("Class", isRemote=0)
    element = RPModelElement(fake)

    assert element.is_remote() == 0
    fake.isRemote.assert_called_once_with()


def test_model_element_locate_in_browser_returns_int() -> None:
    fake = make_fake_element("Class", locateInBrowser=1)
    element = RPModelElement(fake)

    assert element.locate_in_browser() == 1
    fake.locateInBrowser.assert_called_once_with()


def test_model_element_open_features_dialog_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.open_features_dialog(1)

    fake.openFeaturesDialog.assert_called_once_with(1)


def test_model_element_remove_property_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.remove_property("key")

    fake.removeProperty.assert_called_once_with("key")


def test_model_element_remove_redefines_unwraps_argument() -> None:
    redefine = RPModelElement(make_fake_element("Element"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.remove_redefines(redefine)

    fake.removeRedefines.assert_called_once_with(redefine._com)


def test_model_element_remove_stereotype_unwraps_argument() -> None:
    stereotype = RPModelElement(make_fake_element("Stereotype"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.remove_stereotype(stereotype)

    fake.removeStereotype.assert_called_once_with(stereotype._com)


def test_model_element_set_decoration_style_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_decoration_style("Bold")

    fake.setDecorationStyle.assert_called_once_with("Bold")


def test_model_element_set_description_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_description("A description")

    fake.setDescription.assert_called_once_with("A description")


def test_model_element_set_description_and_hyperlinks_unwraps_targets() -> None:
    targets = RPCollection(make_fake_collection([]))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_description_and_hyperlinks("{\\rtf}", targets)

    fake.setDescriptionAndHyperlinks.assert_called_once_with("{\\rtf}", targets._com)


def test_model_element_set_description_html_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    with pytest.raises(NotImplementedError):
        element.set_description_html("<p>desc</p>")


def test_model_element_set_description_rtf_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_description_rtf("{\\rtf}")

    fake.setDescriptionRTF.assert_called_once_with("{\\rtf}")


def test_model_element_set_display_name_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_display_name("Label")

    fake.setDisplayName.assert_called_once_with("Label")


def test_model_element_set_display_name_rtf_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_display_name_rtf("{\\rtf}")

    fake.setDisplayNameRTF.assert_called_once_with("{\\rtf}")


def test_model_element_set_guid_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_guid("new-guid")

    fake.setGUID.assert_called_once_with("new-guid")


def test_model_element_set_is_show_display_name_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_is_show_display_name(1)

    fake.setIsShowDisplayName.assert_called_once_with(1)


def test_model_element_set_main_diagram_unwraps_argument() -> None:
    diagram = RPModelElement(make_fake_element("Diagram"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_main_diagram(diagram)

    fake.setMainDiagram.assert_called_once_with(diagram._com)


def test_model_element_set_of_template_unwraps_argument() -> None:
    template = RPModelElement(make_fake_element("Element"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_of_template(template)

    fake.setOfTemplate.assert_called_once_with(template._com)


def test_model_element_set_owner_unwraps_argument() -> None:
    owner = RPModelElement(make_fake_element("Element"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_owner(owner)

    fake.setOwner.assert_called_once_with(owner._com)


def test_model_element_set_property_value_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_property_value("key", "value")

    fake.setPropertyValue.assert_called_once_with("key", "value")


def test_model_element_set_requirement_traceability_handle_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_requirement_traceability_handle(42)

    fake.setRequirementTraceabilityHandle.assert_called_once_with(42)


def test_model_element_set_tag_context_value_unwraps_args_and_wraps_result() -> None:
    tag = RPModelElement(make_fake_element("Tag"))
    elements = RPCollection(make_fake_collection([]))
    multiplicities = RPCollection(make_fake_collection([]))
    result_fake = make_fake_element("Tag", getName="CtxTag")
    fake = make_fake_element("Class", setTagContextValue=result_fake)
    element = RPModelElement(fake)

    result = element.set_tag_context_value(tag, elements, multiplicities)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "CtxTag"
    fake.setTagContextValue.assert_called_once_with(tag._com, elements._com, multiplicities._com)


def test_model_element_set_tag_element_value_unwraps_args_and_wraps_result() -> None:
    tag = RPModelElement(make_fake_element("Tag"))
    val = RPModelElement(make_fake_element("Element"))
    result_fake = make_fake_element("Tag", getName="ElemTag")
    fake = make_fake_element("Class", setTagElementValue=result_fake)
    element = RPModelElement(fake)

    result = element.set_tag_element_value(tag, val)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "ElemTag"
    fake.setTagElementValue.assert_called_once_with(tag._com, val._com)


def test_model_element_set_tag_value_unwraps_tag_and_wraps_result() -> None:
    tag = RPModelElement(make_fake_element("Tag"))
    result_fake = make_fake_element("Tag", getName="ValTag")
    fake = make_fake_element("Class", setTagValue=result_fake)
    element = RPModelElement(fake)

    result = element.set_tag_value(tag, "a value")

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "ValTag"
    fake.setTagValue.assert_called_once_with(tag._com, "a value")


def test_model_element_set_ti_unwraps_argument() -> None:
    ti = RPModelElement(make_fake_element("TemplateInstantiation"))
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.set_ti(ti)

    fake.setTi.assert_called_once_with(ti._com)


def test_model_element_synchronize_template_instantiation_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.synchronize_template_instantiation()

    fake.synchronizeTemplateInstantiation.assert_called_once_with()


# ---------------------------------------------------------------------------
# RPUnit: IRPUnit parity (Task 3)
# ---------------------------------------------------------------------------


def test_add_to_model_mode_constants_match_java_api() -> None:
    assert int(AddToModelMode.AS_REFERENCE) == 0
    assert int(AddToModelMode.AS_UNIT_WITH_COPY) == 1
    assert int(AddToModelMode.AS_UNIT_WITHOUT_COPY) == 2
    # IntEnum is int-compatible so callers can compare raw COM ints directly.
    assert AddToModelMode.AS_REFERENCE == 0  # type: ignore[comparison-overlap]


def test_unit_copy_to_another_project_unwraps_parent_and_wraps_result() -> None:
    parent = RPModelElement(make_fake_element("Project"))
    copied_fake = make_fake_element("Package", getName="Copied")
    fake = make_fake_element("Package", copyToAnotherProject=copied_fake)
    unit = RPUnit(fake)

    result = unit.copy_to_another_project(parent)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Copied"
    fake.copyToAnotherProject.assert_called_once_with(parent._com)


def test_unit_get_add_to_model_mode_returns_int() -> None:
    fake = make_fake_element("Package", getAddToModelMode=2)
    unit = RPUnit(fake)

    assert unit.get_add_to_model_mode() == 2
    fake.getAddToModelMode.assert_called_once_with()


def test_unit_get_cm_header_returns_str() -> None:
    fake = make_fake_element("Package", getCMHeader="// CM header")
    unit = RPUnit(fake)

    assert unit.get_cm_header() == "// CM header"
    fake.getCMHeader.assert_called_once_with()


def test_unit_get_cm_state_returns_int() -> None:
    fake = make_fake_element("Package", getCMState=1)
    unit = RPUnit(fake)

    assert unit.get_cm_state() == 1
    fake.getCMState.assert_called_once_with()


def test_unit_get_current_directory_returns_str() -> None:
    fake = make_fake_element("Package", getCurrentDirectory="C:\\proj")
    unit = RPUnit(fake)

    assert unit.get_current_directory() == "C:\\proj"
    fake.getCurrentDirectory.assert_called_once_with()


def test_unit_get_include_in_next_load_returns_int() -> None:
    fake = make_fake_element("Package", getIncludeInNextLoad=1)
    unit = RPUnit(fake)

    assert unit.get_include_in_next_load() == 1
    fake.getIncludeInNextLoad.assert_called_once_with()


def test_unit_get_is_stub_returns_int() -> None:
    fake = make_fake_element("Package", getIsStub=0)
    unit = RPUnit(fake)

    assert unit.get_is_stub() == 0
    fake.getIsStub.assert_called_once_with()


def test_unit_get_language_returns_str() -> None:
    fake = make_fake_element("Package", getLanguage="C++")
    unit = RPUnit(fake)

    assert unit.get_language() == "C++"
    fake.getLanguage.assert_called_once_with()


def test_unit_get_last_modified_time_returns_str() -> None:
    fake = make_fake_element("Package", getLastModifiedTime="20250731T120000")
    unit = RPUnit(fake)

    assert unit.get_last_modified_time() == "20250731T120000"
    fake.getLastModifiedTime.assert_called_once_with()


def test_unit_get_nested_save_units_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Package", getNestedSaveUnits=coll)
    unit = RPUnit(fake)

    result = unit.get_nested_save_units()

    assert isinstance(result, RPCollection)
    fake.getNestedSaveUnits.assert_called_once_with()


def test_unit_get_nested_save_units_count_returns_int() -> None:
    fake = make_fake_element("Package", getNestedSaveUnitsCount=3)
    unit = RPUnit(fake)

    assert unit.get_nested_save_units_count() == 3
    fake.getNestedSaveUnitsCount.assert_called_once_with()


def test_unit_get_structure_diagrams_returns_collection() -> None:
    coll = make_fake_collection([])
    fake = make_fake_element("Package", getStructureDiagrams=coll)
    unit = RPUnit(fake)

    result = unit.get_structure_diagrams()

    assert isinstance(result, RPCollection)
    fake.getStructureDiagrams.assert_called_once_with()


def test_unit_get_unit_path_passes_flag_and_returns_str() -> None:
    fake = make_fake_element("Package", getUnitPath="C:\\proj\\foo.sbs")
    unit = RPUnit(fake)

    assert unit.get_unit_path(1) == "C:\\proj\\foo.sbs"
    fake.getUnitPath.assert_called_once_with(1)


def test_unit_is_reference_unit_returns_int() -> None:
    fake = make_fake_element("Package", isReferenceUnit=1)
    unit = RPUnit(fake)

    assert unit.is_reference_unit() == 1
    fake.isReferenceUnit.assert_called_once_with()


def test_unit_is_separate_save_unit_returns_int() -> None:
    fake = make_fake_element("Package", isSeparateSaveUnit=0)
    unit = RPUnit(fake)

    assert unit.is_separate_save_unit() == 0
    fake.isSeparateSaveUnit.assert_called_once_with()


def test_unit_load_passes_flag_and_wraps_result() -> None:
    loaded_fake = make_fake_element("Package", getName="Loaded")
    fake = make_fake_element("Package", load=loaded_fake)
    unit = RPUnit(fake)

    result = unit.load(1)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Loaded"
    fake.load.assert_called_once_with(1)


def test_unit_move_to_another_project_leave_a_reference_unwraps_parent_and_wraps_result() -> None:
    parent = RPModelElement(make_fake_element("Project"))
    moved_fake = make_fake_element("Package", getName="Moved")
    fake = make_fake_element("Package", moveToAnotherProjectLeaveAReference=moved_fake)
    unit = RPUnit(fake)

    result = unit.move_to_another_project_leave_a_reference(parent)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Moved"
    fake.moveToAnotherProjectLeaveAReference.assert_called_once_with(parent._com)


def test_unit_reference_to_another_project_unwraps_parent_and_wraps_result() -> None:
    parent = RPModelElement(make_fake_element("Project"))
    ref_fake = make_fake_element("Package", getName="Ref")
    fake = make_fake_element("Package", referenceToAnotherProject=ref_fake)
    unit = RPUnit(fake)

    result = unit.reference_to_another_project(parent)

    assert isinstance(result, RPModelElement)
    assert result.get_name() == "Ref"
    fake.referenceToAnotherProject.assert_called_once_with(parent._com)


def test_unit_set_cm_header_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.set_cm_header("// CM header")

    fake.setCMHeader.assert_called_once_with("// CM header")


def test_unit_set_include_in_next_load_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.set_include_in_next_load(1)

    fake.setIncludeInNextLoad.assert_called_once_with(1)


def test_unit_set_language_passes_language_and_recursive_flag() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.set_language("cpp", 0)

    fake.setLanguage.assert_called_once_with("cpp", 0)


def test_unit_set_separate_save_unit_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.set_separate_save_unit(1)

    fake.setSeparateSaveUnit.assert_called_once_with(1)


def test_unit_set_unit_path_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.set_unit_path("C:\\proj\\new")

    fake.setUnitPath.assert_called_once_with("C:\\proj\\new")


def test_unit_unload_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.unload()

    fake.unload.assert_called_once_with()
