"""Wraps ``com.telelogic.rhapsody.core.IRPPackage``."""

from typing import Any

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit


class RPPackage(RPUnit):
    """Wraps ``IRPPackage``: represents a package that contains model elements."""

    # IRPPackage method parity checklist:
    # [ ] addActivityDiagram  [ ] impl  [ ] docstring  [ ] test
    # [x] addActor  [x] impl  [x] docstring  [x] test
    # [x] addClass  [x] impl  [x] docstring  [x] test
    # [ ] addCollaborationDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] addComponentDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] addDeploymentDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] addEvent  [ ] impl  [ ] docstring  [ ] test
    # [ ] addFlowItems  [ ] impl  [ ] docstring  [ ] test
    # [ ] addFlows  [ ] impl  [ ] docstring  [ ] test
    # [x] addGlobalFunction  [x] impl  [x] docstring  [x] test
    # [ ] addGlobalObject  [ ] impl  [ ] docstring  [ ] test
    # [ ] addGlobalVariable  [ ] impl  [ ] docstring  [ ] test
    # [ ] addImplicitObject  [ ] impl  [ ] docstring  [ ] test
    # [ ] addInstanceSpecification  [ ] impl  [ ] docstring  [ ] test
    # [ ] addLink  [ ] impl  [ ] docstring  [ ] test
    # [ ] addLinkBetweenSYSMLPorts  [ ] impl  [ ] docstring  [ ] test
    # [ ] addModule  [ ] impl  [ ] docstring  [ ] test
    # [x] addNestedPackage  [x] impl  [x] docstring  [x] test
    # [ ] addNode  [ ] impl  [ ] docstring  [ ] test
    # [ ] addObjectModelDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] addPanelDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] addSequenceDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] addStatechart  [ ] impl  [ ] docstring  [ ] test
    # [ ] addTimingDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] addType  [ ] impl  [ ] docstring  [ ] test
    # [x] addUseCase  [x] impl  [x] docstring  [x] test
    # [ ] addUseCaseDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteActor  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteCollaborationDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteComponentDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteDeploymentDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteEvent  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteFlowItems  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteFlows  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteGlobalFunction  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteGlobalObject  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteGlobalVariable  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteNode  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteObjectModelDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] deletePackage  [ ] impl  [ ] docstring  [ ] test
    # [ ] deletePanelDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteSequenceDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteTimingDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteType  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteUseCase  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteUseCaseDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] findActor  [ ] impl  [ ] docstring  [ ] test
    # [ ] findAllByName  [ ] impl  [ ] docstring  [ ] test
    # [ ] findClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] findEvent  [ ] impl  [ ] docstring  [ ] test
    # [ ] findGlobalFunction  [ ] impl  [ ] docstring  [ ] test
    # [ ] findGlobalObject  [ ] impl  [ ] docstring  [ ] test
    # [ ] findGlobalVariable  [ ] impl  [ ] docstring  [ ] test
    # [ ] findNode  [ ] impl  [ ] docstring  [ ] test
    # [ ] findType  [ ] impl  [ ] docstring  [ ] test
    # [ ] findUsage  [ ] impl  [ ] docstring  [ ] test
    # [ ] findUseCase  [ ] impl  [ ] docstring  [ ] test
    # [x] getActors  [x] impl  [x] docstring  [x] test
    # [ ] getAllNestedElements  [ ] impl  [ ] docstring  [ ] test
    # [ ] getBehavioralDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [x] getClasses  [x] impl  [x] docstring  [x] test
    # [ ] getCollaborationDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [ ] getComponentDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [ ] getDeploymentDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [ ] getEvents  [ ] impl  [ ] docstring  [ ] test
    # [ ] getEventsBaseId  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFlowItems  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFlows  [ ] impl  [ ] docstring  [ ] test
    # [ ] getGlobalFunctions  [ ] impl  [ ] docstring  [ ] test
    # [ ] getGlobalObjects  [ ] impl  [ ] docstring  [ ] test
    # [ ] getGlobalVariables  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInstanceSpecifications  [ ] impl  [ ] docstring  [ ] test
    # [ ] getLinks  [ ] impl  [ ] docstring  [ ] test
    # [ ] getModules  [ ] impl  [ ] docstring  [ ] test
    # [ ] getNamespace  [ ] impl  [ ] docstring  [ ] test
    # [ ] getNestedClassifiers  [ ] impl  [ ] docstring  [ ] test
    # [ ] getNestedComponents  [ ] impl  [ ] docstring  [ ] test
    # [ ] getNodes  [ ] impl  [ ] docstring  [ ] test
    # [ ] getObjectModelDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPackages  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPanelDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [ ] getRemoteRequirementsPopulateMode  [ ] impl  [ ] docstring  [ ] test
    # [ ] getRootInstanceSpecifications  [ ] impl  [ ] docstring  [ ] test
    # [ ] getSavedInSeperateDirectory  [ ] impl  [ ] docstring  [ ] test
    # [ ] getSequenceDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [ ] getSourceArtifacts  [ ] impl  [ ] docstring  [ ] test
    # [ ] getTimingDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [ ] getTypes  [ ] impl  [ ] docstring  [ ] test
    # [ ] getUseCaseDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [x] getUseCases  [x] impl  [x] docstring  [x] test
    # [ ] getUserDefinedStereotypes  [ ] impl  [ ] docstring  [ ] test
    # [ ] loginToRemoteArtifactServer  [ ] impl  [ ] docstring  [ ] test
    # [ ] populateRemoteRequirements  [ ] impl  [ ] docstring  [ ] test
    # [ ] reCalculateEventsBaseId  [ ] impl  [ ] docstring  [ ] test
    # [ ] setRemoteRequirementsPopulateMode  [ ] impl  [ ] docstring  [ ] test
    # [ ] setSavedInSeperateDirectory  [ ] impl  [ ] docstring  [ ] test
    # [ ] updateContainedDiagramsOnServer  [ ] impl  [ ] docstring  [ ] test
    # [ ] updateContainedMatricesOnServer  [ ] impl  [ ] docstring  [ ] test
    # [ ] updateContainedTablesOnServer  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPUnit / IRPModelElement methods (covered by RPUnit / RPModelElement checklists)
    # No deprecated IRPPackage methods.

    def addClass(self, name: str) -> Any:
        """Adds a new class to the package.

        Args:
            name: The name of the new class.

        Returns:
            The wrapped ``IRPClass`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addClass(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addClass(name)))

    def addNestedPackage(self, name: str) -> Any:
        """Adds a nested package to this package.

        Args:
            name: The name of the new nested package.

        Returns:
            The wrapped ``IRPPackage`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addNestedPackage(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNestedPackage(name)))

    def addActor(self, name: str) -> Any:
        """Adds a new actor to the package.

        Args:
            name: The name of the new actor.

        Returns:
            The wrapped ``IRPActor`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addActor(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addActor(name)))

    def addGlobalFunction(self, name: str) -> Any:
        """Adds a new global function to the package.

        Args:
            name: The name of the new global function.

        Returns:
            The wrapped function element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addGlobalFunction(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addGlobalFunction(name)))

    def getNestedPackages(self) -> "RPCollection":
        """Returns all nested packages in this package.

        Returns:
            An ``RPCollection`` of ``IRPPackage`` objects.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNestedPackages", "nestedPackages"))

    def getClasses(self) -> "RPCollection":
        """Returns all classes contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPClass`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getClasses()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getClasses", "classes"))

    def getActors(self) -> "RPCollection":
        """Returns all actors contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPActor`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getActors()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getActors", "actors"))

    def getUseCases(self) -> "RPCollection":
        """Returns all use cases contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPUseCase`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getUseCases()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getUseCases", "useCases"))

    def addUseCase(self, name: str) -> Any:
        """Adds a new use case to the package.

        Args:
            name: The name of the new use case.

        Returns:
            The wrapped ``IRPUseCase`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addUseCase(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addUseCase(name)))

    def addInterface(self, name: str) -> Any:
        """Adds a new interface to the package.

        Args:
            name: The name of the new interface.

        Returns:
            The wrapped interface element created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addInterface(name)))

    def addSignal(self, name: str) -> Any:
        """Adds a new signal to the package.

        Args:
            name: The name of the new signal.

        Returns:
            The wrapped signal element created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addSignal(name)))

    def addException(self, name: str) -> Any:
        """Adds a new exception to the package.

        Args:
            name: The name of the new exception.

        Returns:
            The wrapped exception element created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addException(name)))

    def addEnumeration(self, name: str) -> Any:
        """Adds a new enumeration to the package.

        Args:
            name: The name of the new enumeration.

        Returns:
            The wrapped enumeration element created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addEnumeration(name)))

    def getEnumerations(self) -> "RPCollection":
        """Returns all enumerations contained in this package.

        Returns:
            An ``RPCollection`` of enumeration elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getEnumerations", "enumerations"))


AbstractRPModelElement.register_wrapper("Package", RPPackage)
