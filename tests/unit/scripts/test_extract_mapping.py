import sys

sys.path.insert(0, "scripts")

from pathlib import Path

from extract_mapping import extract_mapping

SAMPLE_CLASS = """
class RPModelElement:
    def getName(self):
        return something

    def setName(self, name):
        pass

    def getGUID(self):
        return something

    def errorMessage(self):
        return ""
"""


def test_extract_mapping_from_directory(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir(parents=True)
    mod = src / "model_test.py"
    mod.write_text(SAMPLE_CLASS)

    mapping = extract_mapping([src])

    assert mapping["getName"] == "get_name"
    assert mapping["setName"] == "set_name"
    assert mapping["getGUID"] == "get_guid"
    assert mapping["errorMessage"] == "error_message"
    assert len(mapping) == 4


def test_extract_mapping_from_single_file(tmp_path: Path):
    app_file = tmp_path / "application.py"
    app_file.write_text(
        """
class RhapsodyApplication:
    def openProject(self):
        pass
    def closeAllProjects(self):
        pass
"""
    )
    mapping = extract_mapping([app_file])

    assert mapping["openProject"] == "open_project"
    assert mapping["closeAllProjects"] == "close_all_projects"
    assert len(mapping) == 2


def test_private_methods_not_included(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir(parents=True)
    mod = src / "model_test.py"
    mod.write_text(
        """
class RPModelElement:
    def _internal(self):
        pass
"""
    )
    mapping = extract_mapping([src])
    assert len(mapping) == 0


def test_method_without_uppercase_not_included(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir(parents=True)
    mod = src / "model_test.py"
    mod.write_text(
        """
class Foo:
    def already_snake(self):
        pass
"""
    )
    mapping = extract_mapping([src])
    assert len(mapping) == 0


def test_output_to_json(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir(parents=True)
    mod = src / "model_test.py"
    mod.write_text(
        """
class RPModelElement:
    def getName(self):
        pass
"""
    )
    json_path = tmp_path / "mapping.json"
    extract_mapping([src], output_json=json_path)

    import json

    data = json.loads(json_path.read_text())
    assert data["getName"] == "get_name"
