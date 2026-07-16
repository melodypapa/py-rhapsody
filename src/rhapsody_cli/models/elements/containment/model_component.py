"""Wraps ``com.telelogic.rhapsody.core.IRPComponent``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.containment.model_configuration import RPConfiguration


class RPComponent(RPUnit):
    """Wraps ``IRPComponent``: a component that extends ``IRPUnit``."""

    # IRPComponent method parity checklist:
    # [x] add_configuration  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_file  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] add_folder  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_nested_component  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_scope_element  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_scope_element_without_aggregates  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_to_scope  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] all_elements_in_scope  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] delete_configuration  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] delete_file  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] find_configuration  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_additional_sources  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_build_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_config_by_dependency  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_configurations  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_file  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_file_name  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_files  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_include_path  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_libraries  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_model_element_file_name  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_nested_components  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_package_file  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_panel_diagrams  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_path  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_possible_variants  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_scope_by_selected_elements  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_scope_elements  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_scope_elements_by_category  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_standard_headers  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_variant  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_variation_points  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] is_directory_per_model_component  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] remove_scope_element  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_additional_sources  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_build_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_include_path  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_libraries  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] set_path  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] set_scope_by_selected_elements  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_standard_headers  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_variant  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] update_contained_diagrams_on_server  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] irp_unit / irp_model_element methods (covered by rp_unit / rp_model_element checklists)
    # No deprecated IRPComponent methods.

    def add_configuration(self, name: str) -> "RPConfiguration":
        """Adds a new configuration to the component.

        Args:
            name: The name of the new configuration.

        Returns:
            The wrapped ``IRPConfiguration`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::addConfiguration(java.lang.String name)
        """
        return cast("RPConfiguration", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addConfiguration(name))))

    def add_file(self, name: str) -> "RPUnit":
        """Adds a new file to the component.

        Args:
            name: The name of the new file.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::addFile(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addFile(name))))

    def add_folder(self, name: str) -> "RPUnit":
        """Adds a new folder to the component.

        Args:
            name: The name of the new folder.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::addFolder(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addFolder(name))))

    def add_nested_component(self, name: str) -> "RPComponent":
        """Adds a nested component to this component.

        Args:
            name: The name of the new nested component.

        Returns:
            The wrapped ``IRPComponent`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::addNestedComponent(java.lang.String name)
        """
        return cast("RPComponent", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addNestedComponent(name))))

    def add_scope_element(self, element: RPUnit) -> None:
        """Adds a scope element to the component.

        Args:
            element: The element to add to scope.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::addScopeElement(IRPUnit element)
        """
        self.call_com(lambda: self._com.addScopeElement(element._com))

    def add_scope_element_without_aggregates(self, element: RPUnit) -> None:
        """Adds a scope element without aggregates to the component.

        Args:
            element: The element to add to scope without aggregates.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::addScopeElementWithoutAggregates(IRPUnit element)
        """
        self.call_com(lambda: self._com.addScopeElementWithoutAggregates(element._com))

    def add_to_scope(self, element: RPUnit) -> None:
        """Adds an element to the component's scope.

        Args:
            element: The element to add to scope.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::addToScope(IRPUnit element)
        """
        self.call_com(lambda: self._com.addToScope(element._com))

    def all_elements_in_scope(self) -> "RPCollection":
        """Returns all elements in the component's scope.

        Returns:
            An ``RPCollection`` of all elements in scope.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::allElementsInScope()
        """
        return RPCollection(self.call_com(lambda: self._com.allElementsInScope()))

    def delete_configuration(self, configuration: "RPConfiguration") -> None:
        """Deletes a configuration from the component.

        Args:
            configuration: The configuration to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::deleteConfiguration(IRPConfiguration configuration)
        """
        self.call_com(lambda: self._com.deleteConfiguration(configuration._com))

    def delete_file(self, file: RPUnit) -> None:
        """Deletes a file from the component.

        Args:
            file: The file to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::deleteFile(IRPUnit file)
        """
        self.call_com(lambda: self._com.deleteFile(file._com))

    def find_configuration(self, name: str) -> "RPConfiguration | None":
        """Finds a configuration by name.

        Args:
            name: The name of the configuration to find.

        Returns:
            The wrapped ``IRPConfiguration`` if found, ``None`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::findConfiguration(java.lang.String name)
        """
        result = self.call_com(lambda: self._com.findConfiguration(name))
        if result is None:
            return None
        return cast("RPConfiguration", AbstractRPModelElement.wrap(result))

    def get_additional_sources(self) -> str:
        """Returns the additional sources for the component.

        Returns:
            The additional sources string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getAdditionalSources()
        """
        return self._get_method_or_property(self._com, "getAdditionalSources", "additionalSources")

    def get_build_type(self) -> str:
        """Returns the build type for the component.

        Returns:
            The build type string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getBuildType()
        """
        return self._get_method_or_property(self._com, "getBuildType", "buildType")

    def get_config_by_dependency(self) -> "RPConfiguration":
        """Returns the configuration by dependency.

        Returns:
            The wrapped ``IRPConfiguration``.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getConfigByDependency()
        """
        return cast("RPConfiguration", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getConfigByDependency())))

    def get_configurations(self) -> "RPCollection":
        """Returns all configurations in the component.

        Returns:
            An ``RPCollection`` of ``IRPConfiguration`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getConfigurations()
        """
        return RPCollection(self.call_com(lambda: self._com.getConfigurations()))

    def get_file(self, name: str) -> "RPUnit":
        """Gets a file by name.

        Args:
            name: The name of the file to get.

        Returns:
            The wrapped ``IRPUnit`` file.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getFile(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getFile(name))))

    def get_file_name(self) -> str:
        """Returns the file name for the component.

        Returns:
            The file name string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getFileName()
        """
        return self._get_method_or_property(self._com, "getFileName", "fileName")

    def get_files(self) -> "RPCollection":
        """Returns all files in the component.

        Returns:
            An ``RPCollection`` of ``IRPUnit`` file objects.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getFiles()
        """
        return RPCollection(self.call_com(lambda: self._com.getFiles()))

    def get_include_path(self) -> str:
        """Returns the include path for the component.

        Returns:
            The include path string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getIncludePath()
        """
        return self._get_method_or_property(self._com, "getIncludePath", "includePath")

    def get_libraries(self) -> str:
        """Returns the libraries for the component.

        Returns:
            The libraries string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getLibraries()
        """
        return self._get_method_or_property(self._com, "getLibraries", "libraries")

    def get_model_element_file_name(self) -> str:
        """Returns the model element file name for the component.

        Returns:
            The model element file name string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getModelElementFileName()
        """
        return self._get_method_or_property(self._com, "getModelElementFileName", "modelElementFileName")

    def get_nested_components(self) -> "RPCollection":
        """Returns all nested components in this component.

        Returns:
            An ``RPCollection`` of ``IRPComponent`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getNestedComponents()
        """
        return RPCollection(self.call_com(lambda: self._com.getNestedComponents()))

    def get_package_file(self) -> str:
        """Returns the package file for the component.

        Returns:
            The package file string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getPackageFile()
        """
        return self._get_method_or_property(self._com, "getPackageFile", "packageFile")

    def get_panel_diagrams(self) -> "RPCollection":
        """Returns all panel diagrams in the component.

        Returns:
            An ``RPCollection`` of ``IRPPanelDiagram`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getPanelDiagrams()
        """
        return RPCollection(self.call_com(lambda: self._com.getPanelDiagrams()))

    def get_path(self) -> str:
        """Returns the path for the component.

        Returns:
            The path string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getPath()
        """
        return self._get_method_or_property(self._com, "getPath", "path")

    def get_possible_variants(self) -> "RPCollection":
        """Returns all possible variants for the component.

        Returns:
            An ``RPCollection`` of variant objects.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getPossibleVariants()
        """
        return RPCollection(self.call_com(lambda: self._com.getPossibleVariants()))

    def get_scope_by_selected_elements(self) -> "RPCollection":
        """Returns scope elements by selected elements.

        Returns:
            An ``RPCollection`` of scope elements.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getScopeBySelectedElements()
        """
        return RPCollection(self.call_com(lambda: self._com.getScopeBySelectedElements()))

    def get_scope_elements(self) -> "RPCollection":
        """Returns all scope elements in the component.

        Returns:
            An ``RPCollection`` of ``IRPUnit`` scope elements.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getScopeElements()
        """
        return RPCollection(self.call_com(lambda: self._com.getScopeElements()))

    def get_scope_elements_by_category(self, category: str) -> "RPCollection":
        """Returns scope elements by category.

        Args:
            category: The category to filter by.

        Returns:
            An ``RPCollection`` of scope elements.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getScopeElementsByCategory(java.lang.String category)
        """
        return RPCollection(self.call_com(lambda: self._com.getScopeElementsByCategory(category)))

    def get_standard_headers(self) -> str:
        """Returns the standard headers for the component.

        Returns:
            The standard headers string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getStandardHeaders()
        """
        return self._get_method_or_property(self._com, "getStandardHeaders", "standardHeaders")

    def get_variant(self) -> str:
        """Returns the variant for the component.

        Returns:
            The variant string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getVariant()
        """
        return self._get_method_or_property(self._com, "getVariant", "variant")

    def get_variation_points(self) -> "RPCollection":
        """Returns all variation points for the component.

        Returns:
            An ``RPCollection`` of variation point objects.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::getVariationPoints()
        """
        return RPCollection(self.call_com(lambda: self._com.getVariationPoints()))

    def is_directory_per_model_component(self) -> int:
        """Returns whether directory is per model component.

        Returns:
            1 if true, 0 if false.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::isDirectoryPerModelComponent()
        """
        return int(self.call_com(lambda: self._com.isDirectoryPerModelComponent()))

    def remove_scope_element(self, element: RPUnit) -> None:
        """Removes a scope element from the component.

        Args:
            element: The element to remove from scope.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::removeScopeElement(IRPUnit element)
        """
        self.call_com(lambda: self._com.removeScopeElement(element._com))

    def set_additional_sources(self, value: str) -> None:
        """Sets the additional sources for the component.

        Args:
            value: The additional sources string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::setAdditionalSources(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setAdditionalSources", "additionalSources", value)

    def set_build_type(self, value: str) -> None:
        """Sets the build type for the component.

        Args:
            value: The build type string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::setBuildType(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setBuildType", "buildType", value)

    def set_include_path(self, value: str) -> None:
        """Sets the include path for the component.

        Args:
            value: The include path string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::setIncludePath(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setIncludePath", "includePath", value)

    def set_libraries(self, value: str) -> None:
        """Sets the libraries for the component.

        Args:
            value: The libraries string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::setLibraries(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setLibraries", "libraries", value)

    def set_path(self, value: str) -> None:
        """Sets the path for the component.

        Args:
            value: The path string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::setPath(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setPath", "path", value)

    def set_scope_by_selected_elements(self, elements: "RPCollection") -> None:
        """Sets the scope by selected elements.

        Args:
            elements: The collection of elements to set scope.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::setScopeBySelectedElements(IRPCollection elements)
        """
        self.call_com(lambda: self._com.setScopeBySelectedElements(elements._com))

    def set_standard_headers(self, value: str) -> None:
        """Sets the standard headers for the component.

        Args:
            value: The standard headers string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::setStandardHeaders(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setStandardHeaders", "standardHeaders", value)

    def set_variant(self, value: str) -> None:
        """Sets the variant for the component.

        Args:
            value: The variant string.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::setVariant(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setVariant", "variant", value)

    def update_contained_diagrams_on_server(self) -> None:
        """Updates contained diagrams on server.

        Reference:
            com.telelogic.rhapsody.core.IRPComponent::updateContainedDiagramsOnServer()
        """
        self.call_com(lambda: self._com.updateContainedDiagramsOnServer())


AbstractRPModelElement.register_wrapper("Component", RPComponent)
