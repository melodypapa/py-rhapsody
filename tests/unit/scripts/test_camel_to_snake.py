import sys

sys.path.insert(0, "scripts")

from camel_to_snake import camel_to_snake


def test_simple_getter():
    assert camel_to_snake("getName") == "get_name"


def test_simple_setter():
    assert camel_to_snake("setName") == "set_name"


def test_get_is_prefix():
    assert camel_to_snake("getIsAbstract") == "get_is_abstract"
    assert camel_to_snake("setIsAbstract") == "set_is_abstract"


def test_consecutive_uppercase():
    assert camel_to_snake("getGUID") == "get_guid"
    assert camel_to_snake("getOSLCLinks") == "get_oslc_links"
    assert camel_to_snake("getRmmUrl") == "get_rmm_url"


def test_no_get_set_prefix():
    assert camel_to_snake("addClass") == "add_class"
    assert camel_to_snake("deleteFromProject") == "delete_from_project"
    assert camel_to_snake("errorMessage") == "error_message"


def test_long_compound_name():
    assert camel_to_snake("getPropertyValueConditionalExplicit") == "get_property_value_conditional_explicit"
    assert camel_to_snake("getNestedElementsByMetaClass") == "get_nested_elements_by_meta_class"
    assert camel_to_snake("becomeTemplateInstantiationOf") == "become_template_instantiation_of"
    assert camel_to_snake("synchronizeTemplateInstantiation") == "synchronize_template_instantiation"


def test_ti_and_id():
    assert camel_to_snake("getTi") == "get_ti"
    assert camel_to_snake("setTi") == "set_ti"
    assert camel_to_snake("getBinaryID") == "get_binary_id"


def test_already_snake_case_is_unchanged():
    assert camel_to_snake("already_snake") == "already_snake"


def test_empty_string():
    assert camel_to_snake("") == ""
