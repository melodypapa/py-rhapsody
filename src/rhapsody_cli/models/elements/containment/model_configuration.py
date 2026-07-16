"""Wraps ``com.telelogic.rhapsody.core.IRPConfiguration``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.containment.model_component import RPComponent
    from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPConfiguration(RPUnit):
    """Wraps ``IRPConfiguration``: a configuration that extends ``IRPUnit``."""

    # IRPConfiguration method parity checklist:
    # [x] add_initial_instance  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] add_package_to_instrumentation_scope  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_to_instrumentation_scope  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] delete_initial_instance  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_additional_sources  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_all_elements_in_instrumentation_scope  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_build_set  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_compiler_switches  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_directory  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_executable_name  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_generate_code_for_actors  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_include_path  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_initial_instances  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_initialization_code  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_instrumentation_scope  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_instrumentation_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_its_component  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_libraries  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_link_switches  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_main_name  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_makefile_name  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_path  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_scope_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_standard_headers  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_statechart_implementation  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_target_name  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_time_model  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] needs_code_generation  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] remove_from_instrumentation_scope  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] remove_package_from_instrumentation_scope  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_additional_sources  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_all_elements_in_instrumentation_scope  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_build_set  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_compiler_switches  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] set_directory  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] set_generate_code_for_actors  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_include_path  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_initialization_code  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_instrumentation_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] set_its_component  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] set_libraries  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_link_switches  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_scope_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_standard_headers  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_statechart_implementation  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_time_model  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] irp_unit / irp_model_element methods (covered by rp_unit / rp_model_element checklists)
    # No deprecated IRPConfiguration methods.

    def add_initial_instance(self, instance: "RPInstance") -> None:
        """Adds an initial instance to the configuration.

        Args:
            instance: The instance to add.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::addInitialInstance(IRPInstance instance)
        """
        self.call_com(lambda: self._com.addInitialInstance(instance._com))

    def add_package_to_instrumentation_scope(self, package: RPUnit) -> None:
        """Adds a package to the instrumentation scope.

        Args:
            package: The package to add to instrumentation scope.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::addPackageToInstrumentationScope(IRPPackage package)
        """
        self.call_com(lambda: self._com.addPackageToInstrumentationScope(package._com))

    def add_to_instrumentation_scope(self, element: RPUnit) -> None:
        """Adds an element to the instrumentation scope.

        Args:
            element: The element to add to instrumentation scope.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::addToInstrumentationScope(IRPModelElement element)
        """
        self.call_com(lambda: self._com.addToInstrumentationScope(element._com))

    def delete_initial_instance(self, instance: "RPInstance") -> None:
        """Deletes an initial instance from the configuration.

        Args:
            instance: The instance to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::deleteInitialInstance(IRPInstance instance)
        """
        self.call_com(lambda: self._com.deleteInitialInstance(instance._com))

    def get_additional_sources(self) -> str:
        """Returns the additional sources for the configuration.

        Returns:
            The additional sources string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getAdditionalSources()
        """
        return self._get_method_or_property(self._com, "getAdditionalSources", "additionalSources")

    def get_all_elements_in_instrumentation_scope(self) -> "RPCollection":
        """Returns all elements in instrumentation scope.

        Returns:
            An ``RPCollection`` of all elements in instrumentation scope.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getAllElementsInInstrumentationScope()
        """
        return RPCollection(self.call_com(lambda: self._com.getAllElementsInInstrumentationScope()))

    def get_build_set(self) -> str:
        """Returns the build set for the configuration.

        Returns:
            The build set string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getBuildSet()
        """
        return self._get_method_or_property(self._com, "getBuildSet", "buildSet")

    def get_compiler_switches(self) -> str:
        """Returns the compiler switches for the configuration.

        Returns:
            The compiler switches string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getCompilerSwitches()
        """
        return self._get_method_or_property(self._com, "getCompilerSwitches", "compilerSwitches")

    def get_directory(self) -> str:
        """Returns the directory for the configuration.

        Returns:
            The directory string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getDirectory()
        """
        return self._get_method_or_property(self._com, "getDirectory", "directory")

    def get_executable_name(self) -> str:
        """Returns the executable name for the configuration.

        Returns:
            The executable name string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getExecutableName()
        """
        return self._get_method_or_property(self._com, "getExecutableName", "executableName")

    def get_generate_code_for_actors(self) -> int:
        """Returns whether to generate code for actors.

        Returns:
            1 if true, 0 if false.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getGenerateCodeForActors()
        """
        return int(self.call_com(lambda: self._com.getGenerateCodeForActors()))

    def get_include_path(self) -> str:
        """Returns the include path for the configuration.

        Returns:
            The include path string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getIncludePath()
        """
        return self._get_method_or_property(self._com, "getIncludePath", "includePath")

    def get_initial_instances(self) -> "RPCollection":
        """Returns all initial instances in the configuration.

        Returns:
            An ``RPCollection`` of ``IRPInstance`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getInitialInstances()
        """
        return RPCollection(self.call_com(lambda: self._com.getInitialInstances()))

    def get_initialization_code(self) -> str:
        """Returns the initialization code for the configuration.

        Returns:
            The initialization code string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getInitializationCode()
        """
        return self._get_method_or_property(self._com, "getInitializationCode", "initializationCode")

    def get_instrumentation_scope(self) -> "RPCollection":
        """Returns the instrumentation scope for the configuration.

        Returns:
            An ``RPCollection`` of elements in instrumentation scope.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getInstrumentationScope()
        """
        return RPCollection(self.call_com(lambda: self._com.getInstrumentationScope()))

    def get_instrumentation_type(self) -> int:
        """Returns the instrumentation type for the configuration.

        Returns:
            The instrumentation type as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getInstrumentationType()
        """
        return int(self.call_com(lambda: self._com.getInstrumentationType()))

    def get_its_component(self) -> "RPComponent":
        """Returns the component for this configuration.

        Returns:
            The wrapped ``IRPComponent``.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getItsComponent()
        """
        return cast("RPComponent", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getItsComponent())))

    def get_libraries(self) -> str:
        """Returns the libraries for the configuration.

        Returns:
            The libraries string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getLibraries()
        """
        return self._get_method_or_property(self._com, "getLibraries", "libraries")

    def get_link_switches(self) -> str:
        """Returns the link switches for the configuration.

        Returns:
            The link switches string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getLinkSwitches()
        """
        return self._get_method_or_property(self._com, "getLinkSwitches", "linkSwitches")

    def get_main_name(self) -> str:
        """Returns the main name for the configuration.

        Returns:
            The main name string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getMainName()
        """
        return self._get_method_or_property(self._com, "getMainName", "mainName")

    def get_makefile_name(self) -> str:
        """Returns the makefile name for the configuration.

        Returns:
            The makefile name string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getMakefileName()
        """
        return self._get_method_or_property(self._com, "getMakefileName", "makefileName")

    def get_path(self) -> str:
        """Returns the path for the configuration.

        Returns:
            The path string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getPath()
        """
        return self._get_method_or_property(self._com, "getPath", "path")

    def get_scope_type(self) -> int:
        """Returns the scope type for the configuration.

        Returns:
            The scope type as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getScopeType()
        """
        return int(self.call_com(lambda: self._com.getScopeType()))

    def get_standard_headers(self) -> str:
        """Returns the standard headers for the configuration.

        Returns:
            The standard headers string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getStandardHeaders()
        """
        return self._get_method_or_property(self._com, "getStandardHeaders", "standardHeaders")

    def get_statechart_implementation(self) -> int:
        """Returns the statechart implementation for the configuration.

        Returns:
            The statechart implementation as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getStatechartImplementation()
        """
        return int(self.call_com(lambda: self._com.getStatechartImplementation()))

    def get_target_name(self) -> str:
        """Returns the target name for the configuration.

        Returns:
            The target name string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getTargetName()
        """
        return self._get_method_or_property(self._com, "getTargetName", "targetName")

    def get_time_model(self) -> int:
        """Returns the time model for the configuration.

        Returns:
            The time model as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::getTimeModel()
        """
        return int(self.call_com(lambda: self._com.getTimeModel()))

    def needs_code_generation(self) -> int:
        """Returns whether code generation is needed.

        Returns:
            1 if needed, 0 if not.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::needsCodeGeneration()
        """
        return int(self.call_com(lambda: self._com.needsCodeGeneration()))

    def remove_from_instrumentation_scope(self, element: RPUnit) -> None:
        """Removes an element from instrumentation scope.

        Args:
            element: The element to remove from instrumentation scope.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::removeFromInstrumentationScope(IRPModelElement element)
        """
        self.call_com(lambda: self._com.removeFromInstrumentationScope(element._com))

    def remove_package_from_instrumentation_scope(self, package: RPUnit) -> None:
        """Removes a package from instrumentation scope.

        Args:
            package: The package to remove from instrumentation scope.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::removePackageFromInstrumentationScope(IRPPackage package)
        """
        self.call_com(lambda: self._com.removePackageFromInstrumentationScope(package._com))

    def set_additional_sources(self, value: str) -> None:
        """Sets the additional sources for the configuration.

        Args:
            value: The additional sources string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setAdditionalSources(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setAdditionalSources", "additionalSources", value)

    def set_all_elements_in_instrumentation_scope(self, elements: "RPCollection") -> None:
        """Sets all elements in instrumentation scope.

        Args:
            elements: The collection of elements to set.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setAllElementsInInstrumentationScope(IRPCollection elements)
        """
        self.call_com(lambda: self._com.setAllElementsInInstrumentationScope(elements._com))

    def set_build_set(self, value: str) -> None:
        """Sets the build set for the configuration.

        Args:
            value: The build set string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setBuildSet(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setBuildSet", "buildSet", value)

    def set_compiler_switches(self, value: str) -> None:
        """Sets the compiler switches for the configuration.

        Args:
            value: The compiler switches string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setCompilerSwitches(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setCompilerSwitches", "compilerSwitches", value)

    def set_directory(self, value: str) -> None:
        """Sets the directory for the configuration.

        Args:
            value: The directory string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setDirectory(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setDirectory", "directory", value)

    def set_generate_code_for_actors(self, value: int) -> None:
        """Sets whether to generate code for actors.

        Args:
            value: 1 to generate, 0 to not generate.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setGenerateCodeForActors(int value)
        """
        self.call_com(lambda: self._com.setGenerateCodeForActors(value))

    def set_include_path(self, value: str) -> None:
        """Sets the include path for the configuration.

        Args:
            value: The include path string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setIncludePath(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setIncludePath", "includePath", value)

    def set_initialization_code(self, value: str) -> None:
        """Sets the initialization code for the configuration.

        Args:
            value: The initialization code string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setInitializationCode(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setInitializationCode", "initializationCode", value)

    def set_instrumentation_type(self, value: int) -> None:
        """Sets the instrumentation type for the configuration.

        Args:
            value: The instrumentation type as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setInstrumentationType(int value)
        """
        self.call_com(lambda: self._com.setInstrumentationType(value))

    def set_its_component(self, component: "RPComponent") -> None:
        """Sets the component for this configuration.

        Args:
            component: The component to set.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setItsComponent(IRPComponent component)
        """
        self.call_com(lambda: self._com.setItsComponent(component._com))

    def set_libraries(self, value: str) -> None:
        """Sets the libraries for the configuration.

        Args:
            value: The libraries string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setLibraries(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setLibraries", "libraries", value)

    def set_link_switches(self, value: str) -> None:
        """Sets the link switches for the configuration.

        Args:
            value: The link switches string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setLinkSwitches(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setLinkSwitches", "linkSwitches", value)

    def set_scope_type(self, value: int) -> None:
        """Sets the scope type for the configuration.

        Args:
            value: The scope type as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setScopeType(int value)
        """
        self.call_com(lambda: self._com.setScopeType(value))

    def set_standard_headers(self, value: str) -> None:
        """Sets the standard headers for the configuration.

        Args:
            value: The standard headers string.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setStandardHeaders(java.lang.String value)
        """
        self._set_method_or_property(self._com, "setStandardHeaders", "standardHeaders", value)

    def set_statechart_implementation(self, value: int) -> None:
        """Sets the statechart implementation for the configuration.

        Args:
            value: The statechart implementation as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setStatechartImplementation(int value)
        """
        self.call_com(lambda: self._com.setStatechartImplementation(value))

    def set_time_model(self, value: int) -> None:
        """Sets the time model for the configuration.

        Args:
            value: The time model as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPConfiguration::setTimeModel(int value)
        """
        self.call_com(lambda: self._com.setTimeModel(value))


AbstractRPModelElement.register_wrapper("Configuration", RPConfiguration)
