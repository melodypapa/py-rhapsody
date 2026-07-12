"""Wraps ``com.telelogic.rhapsody.core.IRPComponent``."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPUnit


class RPComponent(RPUnit):
    """Wraps ``IRPComponent``: a component that extends ``IRPUnit``."""

    # IRPComponent method parity checklist:
    # [ ] addConfiguration  [ ] impl  [ ] docstring  [ ] test
    # [ ] addFile  [ ] impl  [ ] docstring  [ ] test
    # [ ] addFolder  [ ] impl  [ ] docstring  [ ] test
    # [ ] addNestedComponent  [ ] impl  [ ] docstring  [ ] test
    # [ ] addScopeElement  [ ] impl  [ ] docstring  [ ] test
    # [ ] addScopeElementWithoutAggregates  [ ] impl  [ ] docstring  [ ] test
    # [ ] addToScope  [ ] impl  [ ] docstring  [ ] test
    # [ ] allElementsInScope  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteConfiguration  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteFile  [ ] impl  [ ] docstring  [ ] test
    # [ ] findConfiguration  [ ] impl  [ ] docstring  [ ] test
    # [ ] getAdditionalSources  [ ] impl  [ ] docstring  [ ] test
    # [ ] getBuildType  [ ] impl  [ ] docstring  [ ] test
    # [ ] getConfigByDependency  [ ] impl  [ ] docstring  [ ] test
    # [ ] getConfigurations  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFile  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFileName  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFiles  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIncludePath  [ ] impl  [ ] docstring  [ ] test
    # [ ] getLibraries  [ ] impl  [ ] docstring  [ ] test
    # [ ] getModelElementFileName  [ ] impl  [ ] docstring  [ ] test
    # [ ] getNestedComponents  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPackageFile  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPanelDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPath  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPossibleVariants  [ ] impl  [ ] docstring  [ ] test
    # [ ] getScopeBySelectedElements  [ ] impl  [ ] docstring  [ ] test
    # [ ] getScopeElements  [ ] impl  [ ] docstring  [ ] test
    # [ ] getScopeElementsByCategory  [ ] impl  [ ] docstring  [ ] test
    # [ ] getStandardHeaders  [ ] impl  [ ] docstring  [ ] test
    # [ ] getVariant  [ ] impl  [ ] docstring  [ ] test
    # [ ] getVariationPoints  [ ] impl  [ ] docstring  [ ] test
    # [ ] isDirectoryPerModelComponent  [ ] impl  [ ] docstring  [ ] test
    # [ ] removeScopeElement  [ ] impl  [ ] docstring  [ ] test
    # [ ] setAdditionalSources  [ ] impl  [ ] docstring  [ ] test
    # [ ] setBuildType  [ ] impl  [ ] docstring  [ ] test
    # [ ] setIncludePath  [ ] impl  [ ] docstring  [ ] test
    # [ ] setLibraries  [ ] impl  [ ] docstring  [ ] test
    # [ ] setPath  [ ] impl  [ ] docstring  [ ] test
    # [ ] setScopeBySelectedElements  [ ] impl  [ ] docstring  [ ] test
    # [ ] setStandardHeaders  [ ] impl  [ ] docstring  [ ] test
    # [ ] setVariant  [ ] impl  [ ] docstring  [ ] test
    # [ ] updateContainedDiagramsOnServer  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPUnit / IRPModelElement methods (covered by RPUnit / RPModelElement checklists)
    # No deprecated IRPComponent methods.

    pass


AbstractRPModelElement.register_wrapper("Component", RPComponent)
