"""Tests for rhapsody_cli._core: call_com, RPModelElement, wrap()."""

from __future__ import annotations

from unittest.mock import MagicMock, call

import pytest

from rhapsody_cli.exceptions import RhapsodyRuntimeException
from rhapsody_cli.models._core import (
    RPCollection,
    RPModelElement,
    RPUnit,
    call_com,
    register_wrapper,
)
from tests.models.fakes import make_com_error, make_fake_collection, make_fake_element


class _FakeClassWrapper(RPModelElement):
    pass


def test_call_com_returns_value_on_success() -> None:
    result = call_com(lambda: 42)

    assert result == 42


def test_call_com_translates_com_error() -> None:
    def failing() -> int:
        raise make_com_error("getName failed")

    with pytest.raises(RhapsodyRuntimeException, match="getName failed"):
        call_com(failing)


def test_call_com_does_not_translate_other_exceptions() -> None:
    def failing() -> int:
        raise ValueError("not a COM error")

    with pytest.raises(ValueError, match="not a COM error"):
        call_com(failing)


def test_model_element_get_name_delegates_to_com() -> None:
    fake = make_fake_element("Class", getName="Widget")
    element = RPModelElement(fake)

    assert element.getName() == "Widget"
    fake.getName.assert_called_once_with()


def test_model_element_set_name_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.setName("NewName")

    fake.setName.assert_called_once_with("NewName")


def test_model_element_get_meta_class_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    element = RPModelElement(fake)

    assert element.getMetaClass() == "Package"


def test_model_element_get_name_falls_back_to_property_when_method_missing() -> None:
    """Some Rhapsody COM automation ProgIDs (e.g. Rhapsody2.Application.1)
    expose 'name'/'GUID'/'metaClass' as bare properties instead of
    getName()/getGUID()/getMetaClass() methods. Wrapper methods must fall
    back to bare property access in that case."""
    fake = MagicMock(spec=["name"])
    fake.name = "PropertyStyleName"
    element = RPModelElement(fake)

    assert element.getName() == "PropertyStyleName"


def test_model_element_set_name_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["name"])
    element = RPModelElement(fake)

    element.setName("NewName")

    assert fake.name == "NewName"


def test_model_element_get_meta_class_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["metaClass"])
    fake.metaClass = "Class"
    element = RPModelElement(fake)

    assert element.getMetaClass() == "Class"


def test_model_element_get_guid_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["GUID"])
    fake.GUID = "guid-456"
    element = RPModelElement(fake)

    assert element.getGUID() == "guid-456"


def test_wrap_falls_back_to_meta_class_property_when_method_missing() -> None:
    fake = MagicMock(spec=["metaClass"])
    fake.metaClass = "Class"

    from rhapsody_cli.models._core import wrap

    element = wrap(fake)

    assert element.getMetaClass() == "Class"


def test_model_element_get_guid_delegates_to_com() -> None:
    fake = make_fake_element("Class", getGUID="guid-123")
    element = RPModelElement(fake)

    assert element.getGUID() == "guid-123"


def test_model_element_com_error_becomes_rhapsody_runtime_exception() -> None:
    fake = make_fake_element("Class")
    fake.getName.side_effect = make_com_error("boom")
    element = RPModelElement(fake)

    with pytest.raises(RhapsodyRuntimeException, match="boom"):
        element.getName()


def test_model_element_equality_by_underlying_com_object() -> None:
    fake = make_fake_element("Class")

    assert RPModelElement(fake) == RPModelElement(fake)
    assert RPModelElement(fake) != RPModelElement(make_fake_element("Class"))


def test_unit_save_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.save()

    fake.save.assert_called_once_with()


def test_unit_get_filename_delegates_to_com() -> None:
    fake = make_fake_element("Package", getFilename="Model/Foo.sbs")
    unit = RPUnit(fake)

    assert unit.getFilename() == "Model/Foo.sbs"


def test_unit_set_filename_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.setFilename("Model/Bar.sbs")

    fake.setFilename.assert_called_once_with("Model/Bar.sbs")


def test_unit_get_filename_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["filename"])
    fake.filename = "Model/Foo.sbs"
    unit = RPUnit(fake)

    assert unit.getFilename() == "Model/Foo.sbs"


def test_unit_set_filename_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["filename"])
    unit = RPUnit(fake)

    unit.setFilename("Model/Bar.sbs")

    assert fake.filename == "Model/Bar.sbs"


def test_unit_is_read_only_delegates_to_com() -> None:
    fake = make_fake_element("Package", isReadOnly=1)
    unit = RPUnit(fake)

    assert unit.isReadOnly() is True


def test_unit_set_read_only_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.setReadOnly(True)

    fake.setReadOnly.assert_called_once_with(1)


def test_unit_is_a_model_element() -> None:
    fake = make_fake_element("Package", getName="MyPkg")
    unit = RPUnit(fake)

    assert isinstance(unit, RPModelElement)
    assert unit.getName() == "MyPkg"


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
    assert item.getName() == "Widget"
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


def test_collection_iter_yields_all_items() -> None:
    inner_a = make_fake_element("Class", getName="A")
    inner_b = make_fake_element("Class", getName="B")
    fake = make_fake_collection([inner_a, inner_b])
    collection = RPCollection(fake)

    names = [item.getName() for item in collection]

    assert names == ["A", "B"]
    assert fake.getItem.call_args_list == [call(1), call(2)]


def test_collection_add_item_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)
    new_element = make_fake_element("Class")

    collection.addItem(RPModelElement(new_element))

    fake.addItem.assert_called_once_with(new_element)


def test_collection_get_count_delegates_to_com() -> None:
    fake = make_fake_collection([make_fake_element("Class"), make_fake_element("Class")])
    collection = RPCollection(fake)

    assert collection.getCount() == 2


def test_collection_get_count_falls_back_to_count_property_when_method_missing() -> None:
    """Some Rhapsody COM Prog IDs (e.g. Rhapsody2.Application.1) expose the
    collection size/item accessors via 'Count'/'Item' properties instead of
    getCount()/getItem() methods."""
    fake = MagicMock(spec=["Count"])
    fake.Count = 3
    collection = RPCollection(fake)

    assert collection.getCount() == 3


def test_collection_get_item_falls_back_to_item_property_when_method_missing() -> None:
    inner = make_fake_element("Class", getName="Widget")
    fake = MagicMock(spec=["Item"])
    fake.Item.return_value = inner
    collection = RPCollection(fake)

    item = collection.getItem(1)

    assert isinstance(item, RPModelElement)
    assert item.getName() == "Widget"
    fake.Item.assert_called_once_with(1)


def test_wrap_dispatches_to_registered_wrapper() -> None:
    register_wrapper("FakeMetaType", _FakeClassWrapper)
    fake = make_fake_element("FakeMetaType", getName="Thing")

    from rhapsody_cli.models._core import wrap

    wrapped = wrap(fake)

    assert isinstance(wrapped, _FakeClassWrapper)
    assert wrapped.getName() == "Thing"


def test_wrap_falls_back_to_model_element_for_unregistered_type() -> None:
    fake = make_fake_element("SomeUnmappedType", getName="Mystery")

    from rhapsody_cli.models._core import wrap

    wrapped = wrap(fake)

    assert type(wrapped) is RPModelElement
    assert wrapped.getName() == "Mystery"
