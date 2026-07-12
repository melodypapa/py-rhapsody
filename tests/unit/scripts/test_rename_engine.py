import sys

sys.path.insert(0, "scripts")

from pathlib import Path

from rename_engine import apply_rename

MODEL_INPUT = """class RPModelElement:
    def getName(self):
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getName", "name"))

    def getMetaClass(self):
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMetaClass", "metaClass"))

    def addAssociation(self, end1, end2, name):
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addAssociation(end1._com, end2._com, name)))

    def errorMessage(self):
        return str(AbstractRPModelElement.call_com(lambda: self._com.errorMessage()))
"""

MODEL_EXPECTED = """class RPModelElement:
    def get_name(self):
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getName", "name"))

    def get_meta_class(self):
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMetaClass", "metaClass"))

    def add_association(self, end1, end2, name):
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addAssociation(end1._com, end2._com, name)))

    def error_message(self):
        return str(AbstractRPModelElement.call_com(lambda: self._com.errorMessage()))
"""

MAPPING = {
    "getName": "get_name",
    "getMetaClass": "get_meta_class",
    "addAssociation": "add_association",
    "errorMessage": "error_message",
}


def test_model_file_rename(tmp_path: Path):
    source = tmp_path / "model.py"
    source.write_text(MODEL_INPUT)
    changes = apply_rename(source, MAPPING, category="model")
    assert source.read_text() == MODEL_EXPECTED
    assert len(changes) == 4


def test_action_file_rename(tmp_path: Path):
    action_input = """class ClassListAction:
    def _collect_class_names(self, package):
        classes = package.getClasses()
        return [cls.getName() for cls in classes]

    def _resolve_and_validate_package(self, path):
        root = self._get_active_root()
        container = self._resolve_container_or_element(root, path, resolve_element=False)
        meta_class = container.getMetaClass()
        return container
"""
    action_expected = """class ClassListAction:
    def _collect_class_names(self, package):
        classes = package.get_classes()
        return [cls.get_name() for cls in classes]

    def _resolve_and_validate_package(self, path):
        root = self._get_active_root()
        container = self._resolve_container_or_element(root, path, resolve_element=False)
        meta_class = container.get_meta_class()
        return container
"""
    source = tmp_path / "action.py"
    source.write_text(action_input)
    action_mapping = {**MAPPING, "getClasses": "get_classes"}
    changes = apply_rename(source, action_mapping, category="action")
    assert source.read_text() == action_expected
    assert len(changes) == 3


def test_test_file_rename_preserves_fake_calls(tmp_path: Path):
    test_input = """def test_class_get_name():
    fake = make_fake_element("Class", getName="Widget")
    klass = RPClass(fake)
    assert klass.getName() == "Widget"

def test_class_add_superclass():
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    klass = RPClass(fake)
    klass.addSuperclass(RPClass(base))
    fake.addSuperclass.assert_called_once_with(base)

def test_class_get_is_abstract():
    fake = make_fake_element("Class", getIsAbstract=1)
    klass = RPClass(fake)
    assert klass.getIsAbstract() is True
"""
    test_expected = """def test_class_get_name():
    fake = make_fake_element("Class", getName="Widget")
    klass = RPClass(fake)
    assert klass.get_name() == "Widget"

def test_class_add_superclass():
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    klass = RPClass(fake)
    klass.add_superclass(RPClass(base))
    fake.addSuperclass.assert_called_once_with(base)

def test_class_get_is_abstract():
    fake = make_fake_element("Class", getIsAbstract=1)
    klass = RPClass(fake)
    assert klass.get_is_abstract() is True
"""
    source = tmp_path / "test_class.py"
    source.write_text(test_input)
    test_mapping = {**MAPPING, "addSuperclass": "add_superclass", "getIsAbstract": "get_is_abstract"}
    changes = apply_rename(source, test_mapping, category="test")
    assert source.read_text() == test_expected
    assert len(changes) == 3


def test_dry_run_does_not_modify(tmp_path: Path):
    source = tmp_path / "model.py"
    source.write_text(MODEL_INPUT)
    original = source.read_text()
    changes = apply_rename(source, MAPPING, category="model", dry_run=True)
    assert source.read_text() == original
    assert len(changes) == 4
