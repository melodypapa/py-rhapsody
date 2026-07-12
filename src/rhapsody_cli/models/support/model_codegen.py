"""Codegen model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import RPModelElement

if TYPE_CHECKING:
    from rhapsody_cli.application import RhapsodyApplication
    from rhapsody_cli.models.core import RPCollection
    from rhapsody_cli.models.elements.classifiers.model_stereotype import RPStereotype
    from rhapsody_cli.models.elements.containment.model_package import RPPackage
    from rhapsody_cli.models.elements.diagrams.model_diagram_types import RPSequenceDiagram
    from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram
    from rhapsody_cli.models.elements.graphics.model_graphics import RPMatrixView, RPTableLayout, RPTableView


class RPBaseExternalCodeGeneratorTool(RPModelElement):
    """Wraps ``IRPBaseExternalCodeGeneratorTool``."""

    # IRPBaseExternalCodeGeneratorTool method parity checklist:
    # [ ] advanceCodeGenProgressBar    [ ] impl  [ ] docstring  [ ] test
    # [ ] shouldAbortCodeGeneration    [ ] impl  [ ] docstring  [ ] test
    # [ ] writeCodeGenMessage          [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPBaseExternalCodeGeneratorTool methods.

    def advance_code_gen_progress_bar(self) -> None:
        """Advances the code generation progress bar.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPBaseExternalCodeGeneratorTool::advanceCodeGenProgressBar()
        """
        raise NotImplementedError

    def should_abort_code_generation(self) -> int:
        """Returns whether code generation should be aborted.

        Returns:
            int: Non-zero if code generation should be aborted, zero otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPBaseExternalCodeGeneratorTool::shouldAbortCodeGeneration()
        """
        raise NotImplementedError

    def write_code_gen_message(self, msg: str) -> None:
        """Writes a code generation message.

        Args:
            msg: The message to write.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPBaseExternalCodeGeneratorTool::writeCodeGenMessage(java.lang.String msg)
        """
        raise NotImplementedError


class RPCodeGenerator(RPModelElement):
    """Wraps ``IRPCodeGenerator``."""

    # IRPCodeGenerator method parity checklist:
    # [ ] getCodeAnnotations           [ ] impl  [ ] docstring  [ ] test
    # [ ] getGeneratedFileNames        [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPCodeGenerator methods.

    def get_code_annotations(self, element: "RPModelElement", b_spec_file: int) -> "RPCollection":
        """Returns code annotations for the given model element.

        Args:
            element: The model element to get code annotations for.
            b_spec_file: Whether to include specification file annotations.

        Returns:
            RPCollection: A collection of code annotations for the element.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPCodeGenerator::getCodeAnnotations(com.telelogic.rhapsody.core.IRPModelElement element, int bSpecFile)
        """
        raise NotImplementedError

    def get_generated_file_names(self, element: "RPModelElement") -> "RPCollection":
        """Returns the generated file names for the given model element.

        Args:
            element: The model element to get generated file names for.

        Returns:
            RPCollection: A collection of generated file names for the element.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPCodeGenerator::getGeneratedFileNames(com.telelogic.rhapsody.core.IRPModelElement element)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPCodeGenerator::getInterfaceName()
        """
        raise NotImplementedError


class RPDiagSynthAPI(RPModelElement):
    """Wraps ``IRPDiagSynthAPI``."""

    # IRPDiagSynthAPI method parity checklist:
    # [ ] addInstance                  [ ] impl  [ ] docstring  [ ] test
    # [ ] addSynthSDToModel2           [ ] impl  [ ] docstring  [ ] test
    # [ ] createSD2                    [ ] impl  [ ] docstring  [ ] test
    # [ ] receiveMessage               [ ] impl  [ ] docstring  [ ] test
    # [ ] removeSynthSDToModel2        [ ] impl  [ ] docstring  [ ] test
    # [ ] sDAddConditionMark           [ ] impl  [ ] docstring  [ ] test
    # [ ] sendMessage                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPDiagSynthAPI methods.

    def add_instance(self, added_to_s_d: int, instance_nav_exp: str) -> int:
        """Adds an instance to a sequence diagram.

        Args:
            added_to_s_d: The sequence diagram handle to add the instance to.
            instance_nav_exp: The navigation expression for the instance.

        Returns:
            int: The handle of the added instance.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagSynthAPI::addInstance(long addedToSD, java.lang.String instanceNavExp)
        """
        raise NotImplementedError

    def add_synth_s_d_to_model2(self, p_msc_orig: "RPSequenceDiagram", synth_s_d: int, open_s_d: int) -> int:
        """Adds a synthesized sequence diagram to the model.

        Args:
            p_msc_orig: The original sequence diagram.
            synth_s_d: The handle of the synthesized sequence diagram.
            open_s_d: Whether to open the sequence diagram after adding.

        Returns:
            int: Result code indicating success or failure.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagSynthAPI::addSynthSDToModel2(com.telelogic.rhapsody.core.IRPSequenceDiagram pMscOrig, long synthSD, int openSD)
        """
        raise NotImplementedError

    def create_s_d2(self, p_msc_orig: "RPSequenceDiagram", testedmscname: str) -> int:
        """Creates a sequence diagram.

        Args:
            p_msc_orig: The original sequence diagram.
            testedmscname: The name of the tested MSC.

        Returns:
            int: The handle of the created sequence diagram.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagSynthAPI::createSD2(com.telelogic.rhapsody.core.IRPSequenceDiagram pMscOrig, java.lang.String testedmscname)
        """
        raise NotImplementedError

    def receive_message(self, p_tested_s_d: int, p_event_sent: int) -> None:
        """Receives a sequence diagram message.

        Args:
            p_tested_s_d: The handle of the tested sequence diagram.
            p_event_sent: The handle of the sent event.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagSynthAPI::receiveMessage(long pTestedSD, long pEventSent)
        """
        raise NotImplementedError

    def remove_synth_s_d_to_model2(self, p_msc_orig: "RPSequenceDiagram") -> int:
        """Removes a synthesized sequence diagram from the model.

        Args:
            p_msc_orig: The original sequence diagram whose synthesized diagram
                should be removed.

        Returns:
            int: Result code indicating success or failure.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagSynthAPI::removeSynthSDToModel2(com.telelogic.rhapsody.core.IRPSequenceDiagram pMscOrig)
        """
        raise NotImplementedError

    def s_d_add_condition_mark(self, p_tested_s_d: int, instance: str, text: str, type_: str) -> int:
        """Sends a condition mark to an instance in a sequence diagram.

        Args:
            p_tested_s_d: The handle of the tested sequence diagram.
            instance: The instance to add the condition mark to.
            text: The text of the condition mark.
            type_: The type of the condition mark.

        Returns:
            int: The handle of the created condition mark.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagSynthAPI::sDAddConditionMark(long pTestedSD, java.lang.String instance, java.lang.String text, java.lang.String type)
        """
        raise NotImplementedError

    def send_message(self, p_tested_s_d: int, source: str, target: str, event: str, operation: str, type_: str) -> int:
        """Sends a sequence diagram message.

        Args:
            p_tested_s_d: The handle of the tested sequence diagram.
            source: The source instance of the message.
            target: The target instance of the message.
            event: The event associated with the message.
            operation: The operation associated with the message.
            type_: The type of the message.

        Returns:
            int: The handle of the sent message.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagSynthAPI::sendMessage(
                long pTestedSD, java.lang.String source,
                java.lang.String target, java.lang.String event,
                java.lang.String operation, java.lang.String type)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagSynthAPI::getInterfaceName()
        """
        raise NotImplementedError


class RPExternalCheckRegistry(RPModelElement):
    """Wraps ``IRPExternalCheckRegistry``."""

    # IRPExternalCheckRegistry method parity checklist:
    # [ ] appendFailedElementsComments [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] setFailedElementsComments    [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPExternalCheckRegistry methods.

    def append_failed_elements_comments(self, str_val: str) -> None:
        """Appends comments for failed elements.

        Args:
            str_val: The comments string to append.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalCheckRegistry::appendFailedElementsComments(java.lang.String strVal)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalCheckRegistry::getInterfaceName()
        """
        raise NotImplementedError

    def set_failed_elements_comments(self, str_val: str) -> None:
        """Sets the comments for failed elements.

        Args:
            str_val: The comments string to set.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalCheckRegistry::setFailedElementsComments(java.lang.String strVal)
        """
        raise NotImplementedError


class RPExternalRoundtripInvoker(RPModelElement):
    """Wraps ``IRPExternalRoundtripInvoker``."""

    # IRPExternalRoundtripInvoker method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPExternalRoundtripInvoker methods.

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalRoundtripInvoker::getInterfaceName()
        """
        raise NotImplementedError


class RPIntegrator(RPModelElement):
    """Wraps ``IRPIntegrator``."""

    # IRPIntegrator method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPIntegrator methods.

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPIntegrator::getInterfaceName()
        """
        raise NotImplementedError


class RPRhapsodyServer(RPModelElement):
    """Wraps ``IRPRhapsodyServer``."""

    # IRPRhapsodyServer method parity checklist:
    # [ ] getApplication               [ ] impl  [ ] docstring  [ ] test
    # [ ] getHiddenApplication         [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] getUninitializedApplication  [ ] impl  [ ] docstring  [ ] test
    # [ ] initializeApplication        [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPRhapsodyServer methods.

    def get_application(self) -> "RhapsodyApplication":
        """Returns the Rhapsody application.

        Returns:
            Any: The IRPApplication instance.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRhapsodyServer::getApplication()
        """
        raise NotImplementedError

    def get_hidden_application(self) -> "RhapsodyApplication":
        """Returns a hidden Rhapsody application instance.

        Returns:
            Any: The hidden IRPApplication instance.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRhapsodyServer::getHiddenApplication()
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRhapsodyServer::getInterfaceName()
        """
        raise NotImplementedError

    def get_uninitialized_application(self) -> "RhapsodyApplication":
        """Returns an uninitialized Rhapsody application instance.

        Returns:
            Any: The uninitialized IRPApplication instance.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRhapsodyServer::getUninitializedApplication()
        """
        raise NotImplementedError

    def initialize_application(self, p_val: "RhapsodyApplication") -> None:
        """Initializes the Rhapsody application.

        Args:
            p_val: The IRPApplication instance to initialize.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRhapsodyServer::initializeApplication(com.telelogic.rhapsody.core.IRPApplication pVal)
        """
        raise NotImplementedError


class RPRoundTrip(RPModelElement):
    """Wraps ``IRPRoundTrip``."""

    # IRPRoundTrip method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] roundtripFile                [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPRoundTrip methods.

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRoundTrip::getInterfaceName()
        """
        raise NotImplementedError

    def roundtrip_file(self, filename: str, re_generate_file: int) -> "RPCollection":
        """Roundtrips a file, importing external changes back into the model.

        Args:
            filename: The name of the file to roundtrip.
            re_generate_file: Whether to regenerate the file.

        Returns:
            RPCollection: A collection of elements affected by the roundtrip.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRoundTrip::roundtripFile(java.lang.String filename, int reGenerateFile)
        """
        raise NotImplementedError


class RPSearchManager(RPModelElement):
    """Wraps ``IRPSearchManager``: used to carry out a search in a Rhapsody model."""

    # IRPSearchManager method parity checklist:
    # [ ] createSearchQuery            [ ] impl  [ ] docstring  [ ] test
    # [ ] search                       [ ] impl  [ ] docstring  [ ] test
    # [ ] searchAndShowResults         [ ] impl  [ ] docstring  [ ] test
    # [ ] searchAsync                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPSearchManager methods.

    def create_search_query(self) -> "RPSearchQuery":
        """Creates a search query object.

        Returns:
            Any: The search query object that was created.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchManager::createSearchQuery()
        """
        raise NotImplementedError

    def search(self, p_search_query: "RPSearchQuery") -> "RPCollection":
        """Searches the model using the specified search query.

        Args:
            p_search_query: The search query to use to search the model.

        Returns:
            RPCollection: Collection of the model elements returned by the search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchManager::search(com.telelogic.rhapsody.core.IRPSearchQuery pSearchQuery)
        """
        raise NotImplementedError

    def search_and_show_results(self, p_search_query: "RPSearchQuery") -> None:
        """Searches the model using the specified search query, and shows the
        results in the Search tab of the Output window.

        Args:
            p_search_query: The search query to use to search the model.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchManager::searchAndShowResults(com.telelogic.rhapsody.core.IRPSearchQuery pSearchQuery)
        """
        raise NotImplementedError

    def search_async(self, p_search_query: "RPSearchQuery") -> None:
        """Searches the model asynchronously, allowing you to continue working
        in Rhapsody.

        Args:
            p_search_query: The search query to use to search the model.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchManager::searchAsync(com.telelogic.rhapsody.core.IRPSearchQuery pSearchQuery)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Returns the name of the API interface corresponding to the current
        element, for example, IRPClass for a class element, IRPOperation for an
        operation element.

        Returns:
            str: The name of the API interface corresponding to the current element.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchManager::getInterfaceName()
        """
        raise NotImplementedError


class RPSearchQuery(RPModelElement):
    """Wraps ``IRPSearchQuery``: represents the search criteria objects that are used by IRPSearchManager to carry out searches."""

    # IRPSearchQuery method parity checklist:
    # [ ] addDiagramToViewsList        [ ] impl  [ ] docstring  [ ] test
    # [ ] addFilterElementType         [ ] impl  [ ] docstring  [ ] test
    # [ ] addFilterSearchInField       [ ] impl  [ ] docstring  [ ] test
    # [ ] addFilterStereotype          [ ] impl  [ ] docstring  [ ] test
    # [ ] addFilterSubQuery            [ ] impl  [ ] docstring  [ ] test
    # [ ] addMatrixToViewsList         [ ] impl  [ ] docstring  [ ] test
    # [ ] addSearchScope               [ ] impl  [ ] docstring  [ ] test
    # [ ] addTableToViewsList          [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterElementTypes        [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterReferenceIncludeReferencedElementsInSearchResults [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterReferenceNameOfReferencedElements [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterReferenceNumberOfReferences [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterReferenceQuantityOperator [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterReferenceRelationKind [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterReferenceStereotypeOfReferencedElements [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterReferenceTypeOfReferencedElements [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterSearchInFields      [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterStereotypes         [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterSubQueries          [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterSubQueryUseWithNotOperator [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterTagFindAs           [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterTagMatchCase        [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterTagMatchWholeWord   [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterTagName             [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterTagValue            [ ] impl  [ ] docstring  [ ] test
    # [ ] getSearchScopeElements       [ ] impl  [ ] docstring  [ ] test
    # [ ] getView                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getViewCount                 [ ] impl  [ ] docstring  [ ] test
    # [ ] loadFromQuery                [ ] impl  [ ] docstring  [ ] test
    # [ ] removeFilterElementTypes     [ ] impl  [ ] docstring  [ ] test
    # [ ] removeFilterReferences       [ ] impl  [ ] docstring  [ ] test
    # [ ] removeFilterSearchInFields   [ ] impl  [ ] docstring  [ ] test
    # [ ] removeFilterStereotypes      [ ] impl  [ ] docstring  [ ] test
    # [ ] removeFilterSubQueries       [ ] impl  [ ] docstring  [ ] test
    # [ ] removeFilterSubQuery         [ ] impl  [ ] docstring  [ ] test
    # [ ] removeFilterTag              [ ] impl  [ ] docstring  [ ] test
    # [ ] removeSearchScopeElement     [ ] impl  [ ] docstring  [ ] test
    # [ ] removeView                   [ ] impl  [ ] docstring  [ ] test
    # [ ] resetSearchScope             [ ] impl  [ ] docstring  [ ] test
    # [ ] saveAsQuery                  [ ] impl  [ ] docstring  [ ] test
    # [ ] setFilterReference           [ ] impl  [ ] docstring  [ ] test
    # [ ] setFilterTag                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterSubQueriesOperator  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterTagLocalOnly        [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterUnitsOnly           [ ] impl  [ ] docstring  [ ] test
    # [ ] getFilterUnresolvedKind      [ ] impl  [ ] docstring  [ ] test
    # [ ] getIncludeDescendants        [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] getMatchCase                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getMatchSpecifiedCriteria    [ ] impl  [ ] docstring  [ ] test
    # [ ] getMatchWholeWord            [ ] impl  [ ] docstring  [ ] test
    # [ ] getSearchFindAsOption        [ ] impl  [ ] docstring  [ ] test
    # [ ] getSearchScopeObject         [ ] impl  [ ] docstring  [ ] test
    # [ ] getSearchText                [ ] impl  [ ] docstring  [ ] test
    # [ ] getViewIncludeModelElements  [ ] impl  [ ] docstring  [ ] test
    # [ ] getViewsToSearch             [ ] impl  [ ] docstring  [ ] test
    # [ ] setFilterSubQueriesOperator  [ ] impl  [ ] docstring  [ ] test
    # [ ] setFilterTagLocalOnly        [ ] impl  [ ] docstring  [ ] test
    # [ ] setFilterUnitsOnly           [ ] impl  [ ] docstring  [ ] test
    # [ ] setFilterUnresolvedKind      [ ] impl  [ ] docstring  [ ] test
    # [ ] setIncludeDescendants        [ ] impl  [ ] docstring  [ ] test
    # [ ] setMatchCase                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setMatchSpecifiedCriteria    [ ] impl  [ ] docstring  [ ] test
    # [ ] setMatchWholeWord            [ ] impl  [ ] docstring  [ ] test
    # [ ] setSearchFindAsOption        [ ] impl  [ ] docstring  [ ] test
    # [ ] setSearchScopeObject         [ ] impl  [ ] docstring  [ ] test
    # [ ] setSearchText                [ ] impl  [ ] docstring  [ ] test
    # [ ] setViewIncludeModelElements  [ ] impl  [ ] docstring  [ ] test
    # [ ] setViewsToSearch             [ ] impl  [ ] docstring  [ ] test
    # [deprecated] addSearchScope  - skipped (deprecated in Rhapsody Java API)
    # [deprecated] getSearchScopeElements  - skipped (deprecated in Rhapsody Java API)
    # [deprecated] getSearchScopeObject  - skipped (deprecated in Rhapsody Java API)
    # [deprecated] setSearchScopeObject  - skipped (deprecated in Rhapsody Java API)
    # No non-deprecated IRPSearchQuery methods.

    def add_diagram_to_views_list(self, view: "RPDiagram") -> int:
        """Adds the specified diagram to the list of views to be searched for
        the search text.

        Args:
            view: The diagram to add to the list of views to search.

        Returns:
            int: The location of the new item in the list of views.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addDiagramToViewsList(com.telelogic.rhapsody.core.IRPDiagram view)
        """
        raise NotImplementedError

    def add_filter_element_type(self, element_type: str) -> None:
        """Adds an element type to the list of element types that the search
        should be applied to.

        Args:
            element_type: The element type to add to the list of element types
                to search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addFilterElementType(java.lang.String elementType)
        """
        raise NotImplementedError

    def add_filter_search_in_field(self, search_in_field: str) -> None:
        """Adds an element field to the list of element fields that the search
        should be applied to, for example, element name or element description.

        Args:
            search_in_field: The element field to add to the list of element
                fields to search.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addFilterSearchInField(java.lang.String searchInField)
        """
        raise NotImplementedError

    def add_filter_stereotype(self, stereotype: "RPStereotype") -> None:
        """Specifies that the search should be limited to model elements with a
        specific stereotype applied to them.

        Args:
            stereotype: The stereotype to use as a search criterion. Use null to
                search for model elements that do not have any stereotypes
                applied to them.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addFilterStereotype(com.telelogic.rhapsody.core.IRPStereotype stereotype)
        """
        raise NotImplementedError

    def add_filter_sub_query(self, sub_query: "RPTableLayout", use_with_not_operator: int) -> None:
        """Adds a subquery to the list of subqueries specified for the search.

        Args:
            sub_query: The subquery to add for the search.
            use_with_not_operator: Use 1 if you want the NOT operator to be used
                for the specified subquery, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addFilterSubQuery(com.telelogic.rhapsody.core.IRPTableLayout subQuery, int useWithNotOperator)
        """
        raise NotImplementedError

    def add_matrix_to_views_list(self, view: "RPMatrixView") -> int:
        """Adds the specified matrix to the list of views to be searched for
        the search text.

        Args:
            view: The matrix to add to the list of views to search.

        Returns:
            int: The location of the new item in the list of views.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addMatrixToViewsList(com.telelogic.rhapsody.core.IRPMatrixView view)
        """
        raise NotImplementedError

    def add_search_scope(self, scope_element: "RPModelElement") -> None:
        """Adds an element to the scope for the search.

        Args:
            scope_element: Model element that represents a part of the model
                that should be searched, for example, a specific package.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addSearchScope(com.telelogic.rhapsody.core.IRPModelElement scopeElement)
        """
        raise NotImplementedError

    def add_table_to_views_list(self, view: "RPTableView") -> int:
        """Adds the specified table to the list of views to be searched for
        the search text.

        Args:
            view: The table to add to the list of views to search.

        Returns:
            int: The location of the new item in the list of views.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addTableToViewsList(com.telelogic.rhapsody.core.IRPTableView view)
        """
        raise NotImplementedError

    def get_filter_element_types(self) -> "RPCollection":
        """Returns the element types that are to be searched for the search text.

        Returns:
            RPCollection: The element types that are to be searched.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterElementTypes()
        """
        raise NotImplementedError

    def get_filter_reference_include_referenced_elements_in_search_results(self) -> int:
        """Checks whether the reference search criterion specified that the
        referenced elements should also be displayed in the search results.

        Returns:
            int: 1 if the referenced elements should be displayed in the search
            results, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceIncludeReferencedElementsInSearchResults()
        """
        raise NotImplementedError

    def get_filter_reference_name_of_referenced_elements(self) -> str:
        """Returns the model element name that was specified for the reference
        criterion that was defined.

        Returns:
            str: The model element name specified for the reference criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceNameOfReferencedElements()
        """
        raise NotImplementedError

    def get_filter_reference_number_of_references(self) -> int:
        """Returns the number of references that was specified as a search
        criterion.

        Returns:
            int: The number of references that was specified as a search
            criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceNumberOfReferences()
        """
        raise NotImplementedError

    def get_filter_reference_quantity_operator(self) -> str:
        """Returns a value indicating whether the reference criterion was an
        exact number of references, less than that number, or more than that
        number.

        Returns:
            str: Value indicating the quantity operator for the reference
            criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceQuantityOperator()
        """
        raise NotImplementedError

    def get_filter_reference_relation_kind(self) -> str:
        """Returns the type of reference used in the search criterion, for
        example, aggregates or incoming relations.

        Returns:
            str: The type of reference used in the search criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceRelationKind()
        """
        raise NotImplementedError

    def get_filter_reference_stereotype_of_referenced_elements(self) -> str:
        """Returns the stereotype that was specified for the reference criterion
        that was defined.

        Returns:
            str: The stereotype specified for the reference criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceStereotypeOfReferencedElements()
        """
        raise NotImplementedError

    def get_filter_reference_type_of_referenced_elements(self) -> str:
        """Returns the model element type that was specified for the reference
        criterion that was defined.

        Returns:
            str: The model element type specified for the reference criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceTypeOfReferencedElements()
        """
        raise NotImplementedError

    def get_filter_search_in_fields(self) -> "RPCollection":
        """Returns the list of element fields that the search is to be applied
        to.

        Returns:
            RPCollection: The list of element fields that the search is to be
            applied to.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterSearchInFields()
        """
        raise NotImplementedError

    def get_filter_stereotypes(self) -> "RPCollection":
        """Returns the names of the stereotypes that were specified as search
        criteria.

        Returns:
            RPCollection: The names of the stereotypes specified as search
            criteria.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterStereotypes()
        """
        raise NotImplementedError

    def get_filter_sub_queries(self) -> "RPCollection":
        """Returns the subqueries that were specified for the search.

        Returns:
            RPCollection: The subqueries that were specified for the search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterSubQueries()
        """
        raise NotImplementedError

    def get_filter_sub_query_use_with_not_operator(self, sub_query: "RPTableLayout") -> int:
        """Checks whether the NOT operator was specified for the specified
        subquery.

        Args:
            sub_query: The subquery to be checked.

        Returns:
            int: 1 if the NOT operator was specified for the subquery, 0
            otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterSubQueryUseWithNotOperator(com.telelogic.rhapsody.core.IRPTableLayout subQuery)
        """
        raise NotImplementedError

    def get_filter_tag_find_as(self) -> str:
        """Returns the type of search that was specified for the tag name and
        tag value search criteria.

        Returns:
            str: The type of search specified for the tag criteria - regular
            text, wildcard, regular expression, or empty string.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterTagFindAs()
        """
        raise NotImplementedError

    def get_filter_tag_match_case(self) -> int:
        """Checks whether an exact match was specified for the tag name and tag
        value search criteria, in terms of upper and lower case.

        Returns:
            int: 1 if an exact match was specified in terms of upper and lower
            case, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterTagMatchCase()
        """
        raise NotImplementedError

    def get_filter_tag_match_whole_word(self) -> int:
        """Checks whether a whole word match was specified for the tag name and
        tag value search criteria.

        Returns:
            int: 1 if whole word match was specified for the tag criteria, 0
            otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterTagMatchWholeWord()
        """
        raise NotImplementedError

    def get_filter_tag_name(self) -> str:
        """Returns the tag name specified as a criterion for the search.

        Returns:
            str: The tag name specified as a criterion for the search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterTagName()
        """
        raise NotImplementedError

    def get_filter_tag_value(self) -> str:
        """Returns the tag value specified as a criterion for the search.

        Returns:
            str: The tag value specified as a criterion for the search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterTagValue()
        """
        raise NotImplementedError

    def get_search_scope_elements(self) -> "RPCollection":
        """Returns a collection of the model elements that constitute the scope
        for the search.

        Returns:
            RPCollection: The model elements that constitute the scope for the
            search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getSearchScopeElements()
        """
        raise NotImplementedError

    def get_view(self, index: int) -> "RPModelElement":
        """Retrieves the specified item from the list of tables, matrices, and
        diagrams that are to be searched.

        Args:
            index: The index of the view to retrieve. The index of the first
                view in the list is 0.

        Returns:
            Any: The specified item from the list of views to be searched.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getView(int Index)
        """
        raise NotImplementedError

    def get_view_count(self) -> int:
        """Returns the number of views in the list of views that are to be
        searched.

        Returns:
            int: The number of views in the list of views to be searched.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getViewCount()
        """
        raise NotImplementedError

    def load_from_query(self, query: "RPTableLayout") -> None:
        """Loads the settings from the specified query into the search query
        object.

        Args:
            query: The query element whose settings should be loaded into the
                search query object.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::loadFromQuery(com.telelogic.rhapsody.core.IRPTableLayout query)
        """
        raise NotImplementedError

    def remove_filter_element_types(self) -> None:
        """Removes any element type filters that you defined to limit the search
        to certain element types.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterElementTypes()
        """
        raise NotImplementedError

    def remove_filter_references(self) -> None:
        """Removes reference search criterion that was defined for the search
        query.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterReferences()
        """
        raise NotImplementedError

    def remove_filter_search_in_fields(self) -> None:
        """Removes any element field filters that you defined to limit the
        search to certain element fields.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterSearchInFields()
        """
        raise NotImplementedError

    def remove_filter_stereotypes(self) -> None:
        """Removes any stereotype filter that was defined to limit the search to
        model elements that have certain stereotypes applied to them.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterStereotypes()
        """
        raise NotImplementedError

    def remove_filter_sub_queries(self) -> None:
        """Removes the subquery criteria that were specified for the search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterSubQueries()
        """
        raise NotImplementedError

    def remove_filter_sub_query(self, sub_query: "RPTableLayout") -> int:
        """Removes the specified subquery from the search.

        Args:
            sub_query: The subquery that should be removed from the list of
                subqueries for the search.

        Returns:
            int: Result code indicating success or failure.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterSubQuery(com.telelogic.rhapsody.core.IRPTableLayout subQuery)
        """
        raise NotImplementedError

    def remove_filter_tag(self) -> None:
        """Removes the tag name and tag value criteria that were defined for
        the search query.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterTag()
        """
        raise NotImplementedError

    def remove_search_scope_element(self, scope_element: "RPModelElement") -> int:
        """Removes the specified model element from the scope for the search.

        Args:
            scope_element: The model element that should be removed from the
                scope of the search.

        Returns:
            int: Result code indicating success or failure.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeSearchScopeElement(com.telelogic.rhapsody.core.IRPModelElement scopeElement)
        """
        raise NotImplementedError

    def remove_view(self, index: int) -> None:
        """Removes the specified view from the list of views to be searched for
        the search text.

        Args:
            index: The index of the view in the list of views to search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeView(int Index)
        """
        raise NotImplementedError

    def reset_search_scope(self) -> None:
        """Resets the search scope to include the entire project, or all
        projects if multiple projects are open.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::resetSearchScope()
        """
        raise NotImplementedError

    def save_as_query(self, query_owner: "RPPackage") -> "RPTableLayout":
        """Saves the search query object that you defined as a query in your
        model.

        Args:
            query_owner: The model element under which the new query should be
                created.

        Returns:
            Any: The new query element that was created.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::saveAsQuery(com.telelogic.rhapsody.core.IRPPackage queryOwner)
        """
        raise NotImplementedError

    def set_filter_reference(
        self,
        quantity_operator: str,
        number_of_references: int,
        relation_kind: str,
        type_of_referenced_elements: str,
        stereotype_of_referenced_elements: str,
        name_of_referenced_elements: str,
        include_referenced_elements_in_search_results: int,
    ) -> None:
        """Sets criteria for the search based on an element's references.

        Args:
            quantity_operator: Specifies whether the criterion should be exactly
                that number of references, less than, or more than.
            number_of_references: The number of references that should be used as
                a search criterion.
            relation_kind: The type of references to use as a search criterion,
                for example, aggregates or incoming relations.
            type_of_referenced_elements: Model element type to further limit the
                reference criterion.
            stereotype_of_referenced_elements: Limit to references to elements with
                a specific stereotype.
            name_of_referenced_elements: Limit to references to elements with a
                specific name.
            include_referenced_elements_in_search_results: Use 1 to display
                referenced elements in search results, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setFilterReference(
                java.lang.String quantityOperator, int numberOfReferences,
                java.lang.String relationKind,
                java.lang.String typeOfReferencedElements,
                java.lang.String stereotypeOfReferencedElements,
                java.lang.String nameOfReferencedElements,
                int includeReferencedElementsInSearchResults)
        """
        raise NotImplementedError

    def set_filter_tag(self, tag_name: str, tag_value: str, match_case: int, match_whole_word: int, find_as: str) -> None:
        """Sets tag name and tag value criteria for the search query.

        Args:
            tag_name: The text to use for the tag name criterion.
            tag_value: The text to use for the tag value criterion.
            match_case: Use 1 to require an exact match in terms of upper and
                lower case, 0 otherwise.
            match_whole_word: Use 1 to require a whole word match, 0 otherwise.
            find_as: Use one of the constants defined in SearchFindAsEnum to
                indicate the type of search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setFilterTag(java.lang.String tagName, java.lang.String tagValue, int matchCase, int matchWholeWord, char findAs)
        """
        raise NotImplementedError

    def get_filter_sub_queries_operator(self) -> str:
        """Returns indication of how the specified subqueries are to be combined
        in the search.

        Returns:
            str: Indication of how the subqueries are to be combined - one of
            the constants defined in IRPSearchQuery.SubQueriesOperator.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterSubQueriesOperator()
        """
        raise NotImplementedError

    def get_filter_tag_local_only(self) -> int:
        """Checks whether the tag criterion set for a search is limited to only
        local tags.

        Returns:
            int: 1 if the tag criterion is limited to local tags only, 0
            otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterTagLocalOnly()
        """
        raise NotImplementedError

    def get_filter_units_only(self) -> int:
        """Checks whether the search is limited to model elements that are
        saved units.

        Returns:
            int: 1 if the search is limited to saved units, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterUnitsOnly()
        """
        raise NotImplementedError

    def get_filter_unresolved_kind(self) -> str:
        """Returns the method that was specified for handling unresolved
        elements in the search.

        Returns:
            str: The method specified for handling unresolved elements - one of
            the constants from IRPSearchQuery.UnresolvedKind.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterUnresolvedKind()
        """
        raise NotImplementedError

    def get_include_descendants(self) -> int:
        """Checks whether the scope of the search is to include the descendants
        of the elements specified for the scope.

        Returns:
            int: 1 if the scope of the search is to include descendants, 0
            otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getIncludeDescendants()
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Returns the name of the interface (IRPSearchQuery).

        Returns:
            str: The name of the interface (IRPSearchQuery).

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getInterfaceName()
        """
        raise NotImplementedError

    def get_match_case(self) -> int:
        """Checks whether an exact match was specified for the query in terms of
        upper and lower case.

        Returns:
            int: 1 if an exact match was specified in terms of upper and lower
            case, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getMatchCase()
        """
        raise NotImplementedError

    def get_match_specified_criteria(self) -> int:
        """Checks whether the query is to return the model elements that match
        the criteria specified, or the model elements that do not match the
        criteria specified.

        Returns:
            int: 1 if the query is to return the model elements that match the
            criteria specified, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getMatchSpecifiedCriteria()
        """
        raise NotImplementedError

    def get_match_whole_word(self) -> int:
        """Checks whether a whole word match was specified for the search.

        Returns:
            int: 1 if a whole word match was specified, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getMatchWholeWord()
        """
        raise NotImplementedError

    def get_search_find_as_option(self) -> str:
        """Returns the type of search that was specified for the search text -
        regular text, wildcard, regular expression, or empty string.

        Returns:
            str: The type of search specified for the search text - one of the
            constants defined in SearchFindAsEnum.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getSearchFindAsOption()
        """
        raise NotImplementedError

    def get_search_scope_object(self) -> "RPModelElement":
        """Returns the scope specified for the search.

        Deprecated. Use get_search_scope_elements instead, as Rhapsody now
        allows specifying a list of elements as the scope.

        Returns:
            Any: The model element that constitutes the scope for the search.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getSearchScopeObject()
        """
        raise NotImplementedError

    def get_search_text(self) -> str:
        """Returns the text that was specified as the text to search for.

        Returns:
            str: The text to search for.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getSearchText()
        """
        raise NotImplementedError

    def get_view_include_model_elements(self) -> int:
        """Checks whether the query specifies that the search results should
        also include model elements that were found by the search but are not
        referenced in any of the views specified.

        Returns:
            int: 1 if the search results should also include model elements not
            referenced in any of the views, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getViewIncludeModelElements()
        """
        raise NotImplementedError

    def get_views_to_search(self) -> str:
        """Returns indication of which views (diagrams, tables, and matrices)
        are supposed to be searched.

        Returns:
            str: Indication of which views are supposed to be searched - one of
            the constants defined in IRPSearchQuery.ViewsToSearch.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getViewsToSearch()
        """
        raise NotImplementedError

    def set_filter_sub_queries_operator(self, filter_sub_queries_operator: str) -> None:
        """Specifies how the various subqueries specified should be combined -
        as an AND operation or an OR operation.

        Args:
            filter_sub_queries_operator: Use one of the constants defined in
                IRPSearchQuery.SubQueriesOperator to indicate how the specified
                subqueries should be combined.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setFilterSubQueriesOperator(java.lang.String filterSubQueriesOperator)
        """
        raise NotImplementedError

    def set_filter_tag_local_only(self, filter_tag_local_only: int) -> None:
        """Specifies whether the tag criterion for a search should be limited to
        only local tags.

        Args:
            filter_tag_local_only: Use 1 to specify that the tag criterion should
                be limited to only local tags, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setFilterTagLocalOnly(int filterTagLocalOnly)
        """
        raise NotImplementedError

    def set_filter_units_only(self, filter_units_only: int) -> None:
        """Specifies whether the search should be limited to model elements that
        are saved units.

        Args:
            filter_units_only: Use 1 to specify that the search should be limited
                to model elements that are saved units, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setFilterUnitsOnly(int filterUnitsOnly)
        """
        raise NotImplementedError

    def set_filter_unresolved_kind(self, filter_unresolved_kind: str) -> None:
        """Specifies how unresolved elements should be handled in the search.

        Args:
            filter_unresolved_kind: How unresolved elements should be handled in
                the search. One of the constants from
                IRPSearchQuery.UnresolvedKind.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setFilterUnresolvedKind(java.lang.String filterUnresolvedKind)
        """
        raise NotImplementedError

    def set_include_descendants(self, include_descendants: int) -> None:
        """Specifies whether the scope for the search should include the
        descendants of the elements specified for the scope.

        Args:
            include_descendants: Use 1 if you want the search scope to include
                the descendants of the specified elements, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setIncludeDescendants(int includeDescendants)
        """
        raise NotImplementedError

    def set_match_case(self, match_case: int) -> None:
        """Specifies whether the search should require an exact match in terms
        of upper and lower case.

        Args:
            match_case: Use 1 to specify that an exact match is required in
                terms of upper and lower case, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setMatchCase(int matchCase)
        """
        raise NotImplementedError

    def set_match_specified_criteria(self, match_specified_criteria: int) -> None:
        """Specifies whether the query should return the model elements that
        match the criteria specified, or the model elements that do not match
        the criteria specified.

        Args:
            match_specified_criteria: Use 1 if you want the query to return the
                model elements that match the criteria specified, use 0
                otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setMatchSpecifiedCriteria(int matchSpecifiedCriteria)
        """
        raise NotImplementedError

    def set_match_whole_word(self, match_whole_word: int) -> None:
        """Specifies whether the search should require whole word matches.

        Args:
            match_whole_word: Use 1 to specify that a whole word match is
                required, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setMatchWholeWord(int matchWholeWord)
        """
        raise NotImplementedError

    def set_search_find_as_option(self, search_find_as_option: str) -> None:
        """Sets the type of search that should be used for the search text -
        regular text, wildcard, regular expression, or empty string.

        Args:
            search_find_as_option: Use one of the constants defined in
                SearchFindAsEnum to indicate the type of search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setSearchFindAsOption(char searchFindAsOption)
        """
        raise NotImplementedError

    def set_search_scope_object(self, search_scope_object: "RPModelElement") -> None:
        """Sets the scope for the search.

        Deprecated. Use add_search_scope instead, as Rhapsody now allows
        specifying a list of elements as the scope.

        Args:
            search_scope_object: The model element to set as the scope for the
                search.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setSearchScopeObject(com.telelogic.rhapsody.core.IRPModelElement searchScopeObject)
        """
        raise NotImplementedError

    def set_search_text(self, search_text: str) -> None:
        """Specifies the text that should be searched for.

        Args:
            search_text: The text that should be searched for.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setSearchText(java.lang.String searchText)
        """
        raise NotImplementedError

    def set_view_include_model_elements(self, view_include_model_elements: int) -> None:
        """Specifies whether the search results should also include model
        elements that were found by the search but are not referenced in any of
        the views specified.

        Args:
            view_include_model_elements: Use 1 to specify that the search results
                should also include model elements not referenced in any of the
                views, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setViewIncludeModelElements(int viewIncludeModelElements)
        """
        raise NotImplementedError

    def set_views_to_search(self, views_to_search: str) -> None:
        """Specifies which views (tables, matrices, and diagrams) should be
        searched - all, none, all open, or just the views that were specified.

        Args:
            views_to_search: Use one of the constants defined in
                IRPSearchQuery.ViewsToSearch to indicate which views should be
                searched.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setViewsToSearch(java.lang.String viewsToSearch)
        """
        raise NotImplementedError


class RPSearchResult(RPModelElement):
    """Wraps ``IRPSearchResult``."""

    # IRPSearchResult method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] getMatchedField              [ ] impl  [ ] docstring  [ ] test
    # [ ] getMatchedFields             [ ] impl  [ ] docstring  [ ] test
    # [ ] getMatchedObject             [ ] impl  [ ] docstring  [ ] test
    # [ ] getName                      [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPSearchResult methods.

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchResult::getInterfaceName()
        """
        raise NotImplementedError

    def get_matched_field(self) -> str:
        """Returns the property matchedField.

        Returns:
            str: The matched field.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchResult::getMatchedField()
        """
        raise NotImplementedError

    def get_matched_fields(self) -> "RPCollection":
        """Returns the property matchedFields.

        Returns:
            RPCollection: The matched fields.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchResult::getMatchedFields()
        """
        raise NotImplementedError

    def get_matched_object(self) -> "RPModelElement":
        """Returns the property matchedObject.

        Returns:
            Any: The matched model element.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchResult::getMatchedObject()
        """
        raise NotImplementedError

    def get_name(self) -> str:
        """Returns the property name.

        Returns:
            str: The name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchResult::getName()
        """
        raise NotImplementedError


class RPCodeGenSimplifiersRegistry(RPBaseExternalCodeGeneratorTool):
    """Wraps ``IRPCodeGenSimplifiersRegistry``."""

    # IRPCodeGenSimplifiersRegistry method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] notifySimplificationDone     [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPBaseExternalCodeGeneratorTool methods (covered by RPBaseExternalCodeGeneratorTool checklist)
    # No deprecated IRPCodeGenSimplifiersRegistry methods.

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPCodeGenSimplifiersRegistry::getInterfaceName()
        """
        raise NotImplementedError

    def notify_simplification_done(self) -> None:
        """Notifies that simplification is done.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPCodeGenSimplifiersRegistry::notifySimplificationDone()
        """
        raise NotImplementedError


class RPExternalCodeGeneratorInvoker(RPBaseExternalCodeGeneratorTool):
    """Wraps ``IRPExternalCodeGeneratorInvoker``."""

    # IRPExternalCodeGeneratorInvoker method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] notifyGenerationDone         [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPBaseExternalCodeGeneratorTool methods (covered by RPBaseExternalCodeGeneratorTool checklist)
    # No deprecated IRPExternalCodeGeneratorInvoker methods.

    def get_interface_name(self) -> str:
        """Returns the property interfaceName.

        Returns:
            str: The interface name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalCodeGeneratorInvoker::getInterfaceName()
        """
        raise NotImplementedError

    def notify_generation_done(self) -> None:
        """Notifies that code generation is done.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalCodeGeneratorInvoker::notifyGenerationDone()
        """
        raise NotImplementedError
