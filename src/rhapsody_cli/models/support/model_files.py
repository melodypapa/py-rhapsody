"""Files model-element wrappers (auto-generated stubs)."""

from typing import Any

from rhapsody_cli.models.core import RPModelElement, RPUnit


class RPASCIIFile(RPModelElement):
    """Wraps ``IRPASCIIFile``."""

    # IRPASCIIFile method parity checklist:
    # [ ] close                        [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] open                         [ ] impl  [ ] docstring  [ ] test
    # [ ] write                        [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPASCIIFile methods.

    def close(self) -> None:
        """Closes the file.

        Raises:
            RhapsodyRuntimeException: If an error occurs while closing the file.

        Reference:
            com.telelogic.rhapsody.core.IRPASCIIFile::close()
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Gets the interfaceName property.

        Returns:
            The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPASCIIFile::getInterfaceName()
        """
        raise NotImplementedError

    def open(self, filename: str) -> None:
        """Opens the file.

        Args:
            filename: The name of the file to open.

        Raises:
            RhapsodyRuntimeException: If an error occurs while opening the file.

        Reference:
            com.telelogic.rhapsody.core.IRPASCIIFile::open(java.lang.String filename)
        """
        raise NotImplementedError

    def write(self, data: str) -> None:
        """Writes data to the file.

        Args:
            data: The data to write to the file.

        Raises:
            RhapsodyRuntimeException: If an error occurs while writing to the file.

        Reference:
            com.telelogic.rhapsody.core.IRPASCIIFile::write(java.lang.String data)
        """
        raise NotImplementedError


class RPControlledFile(RPUnit):
    """Wraps ``IRPControlledFile``: represents a controlled file in a Rhapsody model.

    To access an element's controlled files, use the method
    IRPModelElement.getControlledFiles().
    """

    # IRPControlledFile method parity checklist:
    # [ ] getFullPathFileName          [ ] impl  [ ] docstring  [ ] test
    # [ ] open                         [ ] impl  [ ] docstring  [ ] test
    # [ ] setTarget                    [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPControlledFile methods.

    def get_full_path_file_name(self) -> str:
        """Returns the full path of the controlled file.

        Returns:
            The full path of the controlled file.

        Reference:
            com.telelogic.rhapsody.core.IRPControlledFile::getFullPathFileName()
        """
        raise NotImplementedError

    def open(self) -> None:
        """Opens the controlled file, using the associated program.

        Reference:
            com.telelogic.rhapsody.core.IRPControlledFile::open()
        """
        raise NotImplementedError

    def set_target(self, filename: str) -> None:
        """Specifies a different file to associate with the Controlled File element.

        Note that this must be a file that already exists in the project directory.

        Args:
            filename: The file to associate with the Controlled File element.
                Must be a file that already exists in the project directory.

        Reference:
            com.telelogic.rhapsody.core.IRPControlledFile::setTarget(java.lang.String filename)
        """
        raise NotImplementedError


class RPFile(RPUnit):
    """Wraps ``IRPFile``: represents a file or folder to be generated during code generation."""

    # IRPFile method parity checklist:
    # [ ] addElement                   [ ] impl  [ ] docstring  [ ] test
    # [ ] addModelElement              [ ] impl  [ ] docstring  [ ] test
    # [ ] addPackageToScope            [ ] impl  [ ] docstring  [ ] test
    # [ ] addTextElement               [ ] impl  [ ] docstring  [ ] test
    # [ ] addToScope                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getElements                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFileFragments             [ ] impl  [ ] docstring  [ ] test
    # [ ] getFileType                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFiles                     [ ] impl  [ ] docstring  [ ] test
    # [ ] getImpName                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getPath                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getSpecName                  [ ] impl  [ ] docstring  [ ] test
    # [ ] isEmpty                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setFileType                  [ ] impl  [ ] docstring  [ ] test
    # [ ] setPath                      [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
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
        raise NotImplementedError

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
        raise NotImplementedError

    def add_package_to_scope(self, p: "RPPackage") -> None:
        """Adds a package to the scope of the file.

        Args:
            p: The package to add to the scope.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::addPackageToScope(com.telelogic.rhapsody.core.IRPPackage p)
        """
        raise NotImplementedError

    def add_text_element(self, text: str) -> None:
        """Adds a text element to the file.

        Args:
            text: The text to add.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::addTextElement(java.lang.String text)
        """
        raise NotImplementedError

    def add_to_scope(self, element: "RPClassifier") -> None:
        """Adds an element to the scope of the file.

        Args:
            element: The classifier element to add to the scope.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::addToScope(com.telelogic.rhapsody.core.IRPClassifier element)
        """
        raise NotImplementedError

    def get_elements(self) -> "RPCollection":
        """Gets the elements property.

        Returns:
            A collection of the file's elements.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getElements()
        """
        raise NotImplementedError

    def get_file_fragments(self) -> "RPCollection":
        """Gets the fileFragments property.

        Returns:
            A collection of the file's file fragments.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getFileFragments()
        """
        raise NotImplementedError

    def get_file_type(self) -> str:
        """Gets the fileType property.

        Returns:
            The file type.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getFileType()
        """
        raise NotImplementedError

    def get_files(self) -> "RPCollection":
        """Gets the files property.

        Returns:
            A collection of the file's files.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::getFiles()
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def is_empty(self) -> int:
        """Checks whether the file is empty.

        Returns:
            1 if the file is empty, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::isEmpty()
        """
        raise NotImplementedError

    def set_file_type(self, file_type: str) -> None:
        """Sets the fileType property.

        Args:
            file_type: The file type to set.

        Raises:
            RhapsodyRuntimeException: If an error occurs while setting the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::setFileType(java.lang.String fileType)
        """
        raise NotImplementedError

    def set_path(self, path: str) -> None:
        """Sets the path property.

        Args:
            path: The path to set.

        Raises:
            RhapsodyRuntimeException: If an error occurs while setting the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFile::setPath(java.lang.String path)
        """
        raise NotImplementedError


class RPFileFragment(RPModelElement):
    """Wraps ``IRPFileFragment``."""

    # IRPFileFragment method parity checklist:
    # [ ] getFragmentElement           [ ] impl  [ ] docstring  [ ] test
    # [ ] getFragmentText              [ ] impl  [ ] docstring  [ ] test
    # [ ] getFragmentType              [ ] impl  [ ] docstring  [ ] test
    # [ ] moveFragmentInOwner          [ ] impl  [ ] docstring  [ ] test
    # [ ] setFragmentText              [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPFileFragment methods.

    def get_fragment_element(self) -> Any:
        """Gets the fragmentElement property.

        Returns:
            The model element associated with this fragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::getFragmentElement()
        """
        raise NotImplementedError

    def get_fragment_text(self) -> str:
        """Gets the fragmentText property.

        Returns:
            The text of the fragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::getFragmentText()
        """
        raise NotImplementedError

    def get_fragment_type(self) -> str:
        """Gets the fragmentType property.

        Returns:
            The type of the fragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs while retrieving the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::getFragmentType()
        """
        raise NotImplementedError

    def move_fragment_in_owner(self, up: int) -> None:
        """Moves the fragment within its owner.

        Args:
            up: Pass 1 to move the fragment up, 0 to move it down.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::moveFragmentInOwner(int up)
        """
        raise NotImplementedError

    def set_fragment_text(self, fragment_text: str) -> None:
        """Sets the fragmentText property.

        Args:
            fragment_text: The text to set for the fragment.

        Raises:
            RhapsodyRuntimeException: If an error occurs while setting the property.

        Reference:
            com.telelogic.rhapsody.core.IRPFileFragment::setFragmentText(java.lang.String fragmentText)
        """
        raise NotImplementedError
