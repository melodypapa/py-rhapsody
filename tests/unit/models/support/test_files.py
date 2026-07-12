from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.support.model_files import (
    RPASCIIFile,
    RPControlledFile,
    RPFile,
    RPFileFragment,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_RPASCIIFile_close_delegates_to_com():
    fake = make_fake_element("ASCIIFile")
    obj = RPASCIIFile(fake)
    obj.close()
    fake.close.assert_called_once_with()


def test_RPASCIIFile_open_delegates_to_com():
    fake = make_fake_element("ASCIIFile")
    obj = RPASCIIFile(fake)
    obj.open("x")
    fake.open.assert_called_once_with("x")


def test_RPASCIIFile_write_delegates_to_com():
    fake = make_fake_element("ASCIIFile")
    obj = RPASCIIFile(fake)
    obj.write("x")
    fake.write.assert_called_once_with("x")


def test_RPControlledFile_get_full_path_file_name_delegates_to_com():
    fake = make_fake_element("ControlledFile")
    fake.getFullPathFileName.return_value = "value"
    obj = RPControlledFile(fake)
    assert obj.get_full_path_file_name() == "value"


def test_RPControlledFile_open_delegates_to_com():
    fake = make_fake_element("ControlledFile")
    obj = RPControlledFile(fake)
    obj.open()
    fake.open.assert_called_once_with()


def test_RPControlledFile_set_target_delegates_to_com():
    fake = make_fake_element("ControlledFile")
    obj = RPControlledFile(fake)
    obj.set_target("file.txt")
    fake.setTarget.assert_called_once_with("file.txt")


def test_RPFile_add_element_delegates_to_com():
    fake = make_fake_element("File")
    target = make_fake_element("X")
    obj = RPFile(fake)
    obj.add_element(AbstractRPModelElement.wrap(target), "x")
    fake.addElement.assert_called_once_with(target, "x")


def test_RPFile_add_model_element_delegates_to_com():
    fake = make_fake_element("File")
    target = make_fake_element("X")
    obj = RPFile(fake)
    obj.add_model_element(AbstractRPModelElement.wrap(target), "x")
    fake.addModelElement.assert_called_once_with(target, "x")


def test_RPFile_add_package_to_scope_delegates_to_com():
    fake = make_fake_element("File")
    target = make_fake_element("X")
    obj = RPFile(fake)
    obj.add_package_to_scope(AbstractRPModelElement.wrap(target))
    fake.addPackageToScope.assert_called_once_with(target)


def test_RPFile_add_text_element_delegates_to_com():
    fake = make_fake_element("File")
    obj = RPFile(fake)
    obj.add_text_element("x")
    fake.addTextElement.assert_called_once_with("x")


def test_RPFile_add_to_scope_delegates_to_com():
    fake = make_fake_element("File")
    target = make_fake_element("X")
    obj = RPFile(fake)
    obj.add_to_scope(AbstractRPModelElement.wrap(target))
    fake.addToScope.assert_called_once_with(target)


def test_RPFile_get_elements_delegates_to_com():
    fake = make_fake_element("File")
    inner = make_fake_element("X", getName="y")
    fake.getElements.return_value = make_fake_collection([inner])
    obj = RPFile(fake)
    result = obj.get_elements()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPFile_get_file_fragments_delegates_to_com():
    fake = make_fake_element("File")
    inner = make_fake_element("X", getName="y")
    fake.getFileFragments.return_value = make_fake_collection([inner])
    obj = RPFile(fake)
    result = obj.get_file_fragments()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPFile_get_file_type_delegates_to_com():
    fake = make_fake_element("File")
    fake.getFileType.return_value = "value"
    obj = RPFile(fake)
    assert obj.get_file_type() == "value"


def test_RPFile_get_files_delegates_to_com():
    fake = make_fake_element("File")
    inner = make_fake_element("X", getName="y")
    fake.getFiles.return_value = make_fake_collection([inner])
    obj = RPFile(fake)
    result = obj.get_files()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPFile_get_imp_name_delegates_to_com():
    fake = make_fake_element("File")
    fake.getImpName.return_value = "value"
    obj = RPFile(fake)
    assert obj.get_imp_name(1) == "value"


def test_RPFile_get_path_delegates_to_com():
    fake = make_fake_element("File")
    fake.getPath.return_value = "value"
    obj = RPFile(fake)
    assert obj.get_path(1) == "value"


def test_RPFile_get_spec_name_delegates_to_com():
    fake = make_fake_element("File")
    fake.getSpecName.return_value = "value"
    obj = RPFile(fake)
    assert obj.get_spec_name(1) == "value"


def test_RPFile_is_empty_delegates_to_com():
    fake = make_fake_element("File")
    fake.isEmpty.return_value = 1
    obj = RPFile(fake)
    result = obj.is_empty()
    fake.isEmpty.assert_called_once_with()
    assert result == 1


def test_RPFile_set_file_type_delegates_to_com():
    fake = make_fake_element("File")
    obj = RPFile(fake)
    obj.set_file_type("file.txt")
    fake.setFileType.assert_called_once_with("file.txt")


def test_RPFile_set_path_delegates_to_com():
    fake = make_fake_element("File")
    obj = RPFile(fake)
    obj.set_path("file.txt")
    fake.setPath.assert_called_once_with("file.txt")


def test_RPFileFragment_get_fragment_element_delegates_to_com():
    fake = make_fake_element("FileFragment")
    inner = make_fake_element("X", getName="y")
    fake.getFragmentElement.return_value = inner
    obj = RPFileFragment(fake)
    result = obj.get_fragment_element()
    assert result.getName() == "y"


def test_RPFileFragment_get_fragment_text_delegates_to_com():
    fake = make_fake_element("FileFragment")
    fake.getFragmentText.return_value = "value"
    obj = RPFileFragment(fake)
    assert obj.get_fragment_text() == "value"


def test_RPFileFragment_get_fragment_type_delegates_to_com():
    fake = make_fake_element("FileFragment")
    fake.getFragmentType.return_value = "value"
    obj = RPFileFragment(fake)
    assert obj.get_fragment_type() == "value"


def test_RPFileFragment_move_fragment_in_owner_delegates_to_com():
    fake = make_fake_element("FileFragment")
    obj = RPFileFragment(fake)
    obj.move_fragment_in_owner(1)
    fake.moveFragmentInOwner.assert_called_once_with(1)


def test_RPFileFragment_set_fragment_text_delegates_to_com():
    fake = make_fake_element("FileFragment")
    obj = RPFileFragment(fake)
    obj.set_fragment_text("file.txt")
    fake.setFragmentText.assert_called_once_with("file.txt")
