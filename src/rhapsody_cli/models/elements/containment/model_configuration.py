"""Wraps ``com.telelogic.rhapsody.core.IRPConfiguration``."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPUnit


class RPConfiguration(RPUnit):
    """Wraps ``IRPConfiguration``: a configuration that extends ``IRPUnit``."""

    # IRPConfiguration method parity checklist:
    # [ ] addInitialInstance  [ ] impl  [ ] docstring  [ ] test
    # [ ] addPackageToInstrumentationScope  [ ] impl  [ ] docstring  [ ] test
    # [ ] addToInstrumentationScope  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteInitialInstance  [ ] impl  [ ] docstring  [ ] test
    # [ ] getAdditionalSources  [ ] impl  [ ] docstring  [ ] test
    # [ ] getAllElementsInInstrumentationScope  [ ] impl  [ ] docstring  [ ] test
    # [ ] getBuildSet  [ ] impl  [ ] docstring  [ ] test
    # [ ] getCompilerSwitches  [ ] impl  [ ] docstring  [ ] test
    # [ ] getDirectory  [ ] impl  [ ] docstring  [ ] test
    # [ ] getExecutableName  [ ] impl  [ ] docstring  [ ] test
    # [ ] getGenerateCodeForActors  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIncludePath  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInitialInstances  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInitializationCode  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInstrumentationScope  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInstrumentationType  [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsComponent  [ ] impl  [ ] docstring  [ ] test
    # [ ] getLibraries  [ ] impl  [ ] docstring  [ ] test
    # [ ] getLinkSwitches  [ ] impl  [ ] docstring  [ ] test
    # [ ] getMainName  [ ] impl  [ ] docstring  [ ] test
    # [ ] getMakefileName  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPath  [ ] impl  [ ] docstring  [ ] test
    # [ ] getScopeType  [ ] impl  [ ] docstring  [ ] test
    # [ ] getStandardHeaders  [ ] impl  [ ] docstring  [ ] test
    # [ ] getStatechartImplementation  [ ] impl  [ ] docstring  [ ] test
    # [ ] getTargetName  [ ] impl  [ ] docstring  [ ] test
    # [ ] getTimeModel  [ ] impl  [ ] docstring  [ ] test
    # [ ] needsCodeGeneration  [ ] impl  [ ] docstring  [ ] test
    # [ ] removeFromInstrumentationScope  [ ] impl  [ ] docstring  [ ] test
    # [ ] removePackageFromInstrumentationScope  [ ] impl  [ ] docstring  [ ] test
    # [ ] setAdditionalSources  [ ] impl  [ ] docstring  [ ] test
    # [ ] setAllElementsInInstrumentationScope  [ ] impl  [ ] docstring  [ ] test
    # [ ] setBuildSet  [ ] impl  [ ] docstring  [ ] test
    # [ ] setCompilerSwitches  [ ] impl  [ ] docstring  [ ] test
    # [ ] setDirectory  [ ] impl  [ ] docstring  [ ] test
    # [ ] setGenerateCodeForActors  [ ] impl  [ ] docstring  [ ] test
    # [ ] setIncludePath  [ ] impl  [ ] docstring  [ ] test
    # [ ] setInitializationCode  [ ] impl  [ ] docstring  [ ] test
    # [ ] setInstrumentationType  [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsComponent  [ ] impl  [ ] docstring  [ ] test
    # [ ] setLibraries  [ ] impl  [ ] docstring  [ ] test
    # [ ] setLinkSwitches  [ ] impl  [ ] docstring  [ ] test
    # [ ] setScopeType  [ ] impl  [ ] docstring  [ ] test
    # [ ] setStandardHeaders  [ ] impl  [ ] docstring  [ ] test
    # [ ] setStatechartImplementation  [ ] impl  [ ] docstring  [ ] test
    # [ ] setTimeModel  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPUnit / IRPModelElement methods (covered by RPUnit / RPModelElement checklists)
    # No deprecated IRPConfiguration methods.

    pass


AbstractRPModelElement.register_wrapper("Configuration", RPConfiguration)
