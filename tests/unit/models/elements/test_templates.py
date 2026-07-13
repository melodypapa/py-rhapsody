"""Tests for rhapsody_cli.models.elements.templates.model_templates classes."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.templates import (
    RPTemplateInstantiation,
    RPTemplateInstantiationParameter,
    RPTemplateParameter,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPTemplateInstantiation:
    def test_is_registered(self) -> None:
        fake = make_fake_element("TemplateInstantiation", getName="TI1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTemplateInstantiation)

    def test_get_template_instantiation_parameters_returns_collection(self) -> None:
        fake = make_fake_element("TemplateInstantiation")
        p = make_fake_element("TemplateInstantiationParameter", getName="p1")
        fake.getTemplateInstantiationParameters.return_value = make_fake_collection([p])
        ti = RPTemplateInstantiation(fake)
        result = ti.get_template_instantiation_parameters()
        assert isinstance(result, RPCollection)
        fake.getTemplateInstantiationParameters.assert_called_once_with()


class TestRPTemplateInstantiationParameter:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("TemplateInstantiationParameter", getName="p1")
        param = RPTemplateInstantiationParameter(fake)
        assert isinstance(param, RPModelElement)
        assert param.get_name() == "p1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("TemplateInstantiationParameter", getName="p1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTemplateInstantiationParameter)

    def test_get_arg_value_returns_string(self) -> None:
        fake = make_fake_element("TemplateInstantiationParameter", getArgValue="int")
        param = RPTemplateInstantiationParameter(fake)
        assert param.get_arg_value() == "int"
        fake.getArgValue.assert_called_once_with()

    def test_get_type_wraps_result(self) -> None:
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("TemplateInstantiationParameter")
        clf = make_fake_element("Class", getName="C1")
        fake.getType.return_value = clf
        param = RPTemplateInstantiationParameter(fake)
        wrapped = param.get_type()
        assert wrapped.get_name() == "C1"
        fake.getType.assert_called_once_with()

    def test_set_arg_value_delegates(self) -> None:
        fake = make_fake_element("TemplateInstantiationParameter")
        param = RPTemplateInstantiationParameter(fake)
        param.set_arg_value("int")
        fake.setArgValue.assert_called_once_with("int")

    def test_set_type_delegates(self) -> None:
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("TemplateInstantiationParameter")
        clf = make_fake_element("Class", getName="C1")
        param = RPTemplateInstantiationParameter(fake)
        param.set_type(RPClassifier(clf))
        fake.setType.assert_called_once_with(clf)


class TestRPTemplateParameter:
    def test_is_registered(self) -> None:
        fake = make_fake_element("TemplateParameter", getName="tp1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTemplateParameter)

    def test_get_parameter_kind_returns_string(self) -> None:
        fake = make_fake_element("TemplateParameter", getParameterKind="class")
        tp = RPTemplateParameter(fake)
        assert tp.get_parameter_kind() == "class"
        fake.getParameterKind.assert_called_once_with()

    def test_get_representative_wraps_result(self) -> None:
        fake = make_fake_element("TemplateParameter")
        rep = make_fake_element("Class", getName="C1")
        fake.getRepresentative.return_value = rep
        tp = RPTemplateParameter(fake)
        wrapped = tp.get_representative()
        assert wrapped.get_name() == "C1"
        fake.getRepresentative.assert_called_once_with()

    def test_set_parameter_kind_delegates(self) -> None:
        fake = make_fake_element("TemplateParameter")
        tp = RPTemplateParameter(fake)
        tp.set_parameter_kind("class")
        fake.setParameterKind.assert_called_once_with("class")

    def test_set_representative_delegates(self) -> None:
        fake = make_fake_element("TemplateParameter")
        rep = make_fake_element("Class", getName="C1")
        tp = RPTemplateParameter(fake)
        tp.set_representative(RPModelElement(rep))
        fake.setRepresentative.assert_called_once_with(rep)

    def test_set_class_type_delegates(self) -> None:
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("TemplateParameter")
        clf = make_fake_element("Class", getName="C1")
        tp = RPTemplateParameter(fake)
        tp.set_class_type(RPClassifier(clf))
        fake.setClassType.assert_called_once_with(clf)
