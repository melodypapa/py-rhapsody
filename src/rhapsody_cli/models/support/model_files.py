"""Files model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement, RPUnit

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
    from rhapsody_cli.models.elements.containment.model_package import RPPackage


class RPASCIIFile(RPModelElement):
    """Wraps ``IRPASCIIFile``."""

    # IRPASCIIFile method parity checklist:
    # [x] close                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_name             [x] impl (inherited from rp_model_element)  [x] docstring  [x] unit test  [ ] integration test
    # [x] open                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] write                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # No deprecated IRPASCIIFile methods.

    def close(self) -> None:
        """Closes the file.

        Raises:
            RhapsodyRuntimeException: If an error occurs while closing the file.

        Reference:
            com.telelogic.rhapsody.core.IRPASCIIFile::close()
        """
        self.call_com(lambda: self._com.close())

    def open(self, filename: str) -> None:
        """Opens the file.

        Args:
            filename: The name of the file to open.

        Raises:
            RhapsodyRuntimeException: If an error occurs while opening the file.

        Reference:
            com.telelogic.rhapsody.core.IRPASCIIFile::open(java.lang.String filename)
        """
        self.call_com(lambda: self._com.open(filename))

    def write(self, data: str) -> None:
        """Writes data to the file.

        Args:
            data: The data to write to the file.

        Raises:
            RhapsodyRuntimeException: If an error occurs while writing to the file.

        Reference:
            com.telelogic.rhapsody.core.IRPASCIIFile::write(java.lang.String data)
        """
        self.call_com(lambda: self._com.write(data))


class RPControlledFile(RPUnit):
    """Wraps ``IRPControlledFile``: represents a controlled file in a Rhapsody model.

    To access an element's controlled files, use the method
    IRPModelElement.getControlledFiles().
    """

    # IRPControlledFile method parity checklist:
    # [x] get_full_path_file_name          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] open                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_target                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # [inherited] irp_unit methods (covered by rp_unit checklist)
    # No deprecated IRPControlledFile methods.

    def get_full_path_file_name(self) -> str:
        """Returns the full path of the controlled file.

        Returns:
            The full path of the controlled file.

        Reference:
            com.telelogic.rhapsody.core.IRPControlledFile::getFullPathFileName()
        """
        return str(self._get_method_or_property(self._com, "getFullPathFileName", "fullPathFileName"))

    def open(self) -> None:
        """Opens the controlled file, using the associated program.

        Reference:
            com.telelogic.rhapsody.core.IRPControlledFile::open()
        """
        self.call_com(lambda: self._com.open())

    def set_target(self, filename: str) -> None:
        """Specifies a different file to associate with the Controlled File element.

        Note that this must be a file that already exists in the project directory.

        Args:
            filename: The file to associate with the Controlled File element.
                Must be a file that already exists in the project directory.

        Reference:
            com.telelogic.rhapsody.core.IRPControlledFile::setTarget(java.lang.String filename)
        """
        self._set_method_or_property(self._com, "setTarget", "target", filename)


class RPFile(RPUnit):
    """Wraps ``IRPFile``: represents a file or folder to be generated during code generation."""

    # IRPFile method parity checklist:
    # [x] add_element                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_model_element              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_package_to_scope            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_text_element               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_to_scope                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_elements                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_file_fragments             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_file_type                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_files                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_imp_name                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_path                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_spec_name                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] is_empty                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_file_type                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_path                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # [inherited] irp_unit methods (covered by rp_unit checklist)
    # No deprecated IRPFile methods.

    def add_element(self, element: "RPClassifier", file_fragment_type: str) -> None:
        """Adds an element to the file with the specified fragment type.

        Args:
            element: The classifier element to add.
            file_fragment_type: The file fragment type. Choose from: undefFragment,
                textFragment, implFragment, specFragment, moduleFragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::addElement(com.telelogic.rhapsody.core.IRPClassifier element, java.lang.String fileFragmentType)
        """
        self.call_com(lambda: self._com.addElement(element._com, file_fragment_type))

    def add_model_element(self, element: "RPModelElement", file_fragment_type: str) -> None:
        """Adds a model element to the file with the specified fragment type.

        Args:
            element: The model element to add.
            file_fragment_type: The file fragment type. Choose from: undefFragment,
                textFragment, implFragment, specFragment, moduleFragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::addModelElement(com.telelogic.rhapsody.core.IRPModelElement element, java.lang.String fileFragmentType)
        """
        self.call_com(lambda: self._com.addModelElement(element._com, file_fragment_type))

    def add_package_to_scope(self, p: "RPPackage") -> None:
        """Adds a package to the scope of the file.

        Args:
            p: The package to add to the scope.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::addPackageToScope(com.telelogic.rhapsody.core.IRPPackage p)
        """
        self.call_com(lambda: self._com.addPackageToScope(p._com))

    def add_text_element(self, text: str) -> None:
        """Adds a text element to the file.

        Args:
            text: The text to add.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::addTextElement(java.lang.String text)
        """
        self.call_com(lambda: self._com.addTextElement(text))

    def add_to_scope(self, element: "RPClassifier") -> None:
        """Adds an element to the scope of the file.

        Args:
            element: The classifier element to add to the scope.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::addToScope(com.telelogic.rhapsody.core.IRPClassifier element)
        """
        self.call_com(lambda: self._com.addToScope(element._com))

    def get_elements(self) -> "RPCollection":
        """Gets the elements property.

        Returns:
            A collection of the file's elements.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getElements()
        """
        return RPCollection(self._get_method_or_property(self._com, "getElements", "elements"))

    def get_file_fragments(self) -> "RPCollection":
        """Gets the fileFragments property.

        Returns:
            A collection of the file's file fragments.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getFileFragments()
        """
        return RPCollection(self._get_method_or_property(self._com, "getFileFragments", "fileFragments"))

    def get_file_type(self) -> str:
        """Gets the fileType property.

        Returns:
            The file type.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getFileType()
        """
        return str(self._get_method_or_property(self._com, "getFileType", "fileType"))

    def get_files(self) -> "RPCollection":
        """Gets the files property.

        Returns:
            A collection of the file's files.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getFiles()
        """
        return RPCollection(self._get_method_or_property(self._com, "getFiles", "files"))

    def get_imp_name(self, including_path: int) -> str:
        """Gets the implementation name.

        Args:
            including_path: Whether to include the path in the name.

        Returns:
            The implementation name.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getImpName(int includingPath)
        """
        return str(self.call_com(lambda: self._com.getImpName(including_path)))

    def get_path(self, full_path: int) -> str:
        """Gets the path property.

        Args:
            full_path: Whether to return the full path.

        Returns:
            The path.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getPath(int fullPath)
        """
        return str(self.call_com(lambda: self._com.getPath(full_path)))

    def get_spec_name(self, including_path: int) -> str:
        """Gets the specification name.

        Args:
            including_path: Whether to include the path in the name.

        Returns:
            The specification name.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getSpecName(int includingPath)
        """
        return str(self.call_com(lambda: self._com.getSpecName(including_path)))

    def is_empty(self) -> int:
        """Checks whether the file is empty.

        Returns:
            1 if the file is empty, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::isEmpty()
        """
        return int(self.call_com(lambda: self._com.isEmpty()))

    def set_file_type(self, file_type: str) -> None:
        """Sets the fileType property.

        Args:
            file_type: The file type to set.

        Raises:
            RhapsodyRuntimeException: If an error occurs while setting the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::setFileType(java.lang.String fileType)
        """
        self._set_method_or_property(self._com, "setFileType", "fileType", file_type)

    def set_path(self, path: str) -> None:
        """Sets the path property.

        Args:
            path: The path to set.

        Raises:
            RhapsodyRuntimeException: If an error occurs while setting the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::setPath(java.lang.String path)
        """
        self._set_method_or_property(self._com, "setPath", "path", path)


class RPFileFragment(RPModelElement):
    """Wraps ``IRPFileFragment``."""

    # IRPFileFragment method parity checklist:
    # [x] get_fragment_element           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_fragment_text              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_fragment_type              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] move_fragment_in_owner          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_fragment_text              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # No deprecated IRPFileFragment methods.

    def get_fragment_element(self) -> "RPModelElement":
        """Gets the fragmentElement property.

        Returns:
            The model element associated with this fragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::getFragmentElement()
        """
        return AbstractRPModelElement.wrap(self._get_method_or_property(self._com, "getFragmentElement", "fragmentElement"))

    def get_fragment_text(self) -> str:
        """Gets the fragmentText property.

        Returns:
            The text of the fragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::getFragmentText()
        """
        return str(self._get_method_or_property(self._com, "getFragmentText", "fragmentText"))

    def get_fragment_type(self) -> str:
        """Gets the fragmentType property.

        Returns:
            The type of the fragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::getFragmentType()
        """
        return str(self._get_method_or_property(self._com, "getFragmentType", "fragmentType"))

    def move_fragment_in_owner(self, up: int) -> None:
        """Moves the fragment within its owner.

        Args:
            up: Pass 1 to move the fragment up, 0 to move it down.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::moveFragmentInOwner(int up)
        """
        self.call_com(lambda: self._com.moveFragmentInOwner(up))

    def set_fragment_text(self, fragment_text: str) -> None:
        """Sets the fragmentText property.

        Args:
            fragment_text: The text to set for the fragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs while setting the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::setFragmentText(java.lang.String fragmentText)
        """
        self._set_method_or_property(self._com, "setFragmentText", "fragmentText", fragment_text)
