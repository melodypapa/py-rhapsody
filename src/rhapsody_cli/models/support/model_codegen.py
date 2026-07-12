"""Codegen model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.graphics.model_graphics import RPTableLayout

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_stereotype import RPStereotype
    from rhapsody_cli.models.elements.containment.model_package import RPPackage
    from rhapsody_cli.models.elements.diagrams.model_diagram_types import RPSequenceDiagram
    from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram
    from rhapsody_cli.models.elements.graphics.model_graphics import RPMatrixView, RPTableView


class RPBaseExternalCodeGeneratorTool(RPModelElement):
    """Wraps ``IRPBaseExternalCodeGeneratorTool``."""

    # IRPBaseExternalCodeGeneratorTool method parity checklist:
    # [ ] advanceCodeGenProgressBar    [ ] impl  [ ] docstring  [ ] test
    # [ ] shouldAbortCodeGeneration    [ ] impl  [ ] docstring  [ ] test
    # [ ] writeCodeGenMessage          [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPBaseExternalCodeGeneratorTool methods.

    def advanceCodeGenProgressBar(self) -> None:
        """Advances the code generation progress bar.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPBaseExternalCodeGeneratorTool::advanceCodeGenProgressBar()
        """
        self.call_com(lambda: self._com.advanceCodeGenProgressBar())

    def shouldAbortCodeGeneration(self) -> int:
        """Returns whether code generation should be aborted.

        Returns:
            int: Non-zero if code generation should be aborted, zero otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPBaseExternalCodeGeneratorTool::shouldAbortCodeGeneration()
        """
        return self.call_com(lambda: self._com.shouldAbortCodeGeneration())

    def writeCodeGenMessage(self, msg: str) -> None:
        """Writes a code generation message.

        Args:
            msg: The message to write.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPBaseExternalCodeGeneratorTool::writeCodeGenMessage(java.lang.String msg)
        """
        self.call_com(lambda: self._com.writeCodeGenMessage(msg))


class RPCodeGenerator(RPModelElement):
    """Wraps ``IRPCodeGenerator``."""

    # IRPCodeGenerator method parity checklist:
    # [x] getCodeAnnotations           [x] impl  [x] docstring  [x] test
    # [x] getGeneratedFileNames        [x] impl  [x] docstring  [x] test
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # No deprecated IRPCodeGenerator methods.

    def getCodeAnnotations(self, element: "RPModelElement", b_spec_file: int) -> "RPCollection":
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
        return RPCollection(self.call_com(lambda: self._com.getCodeAnnotations(element._com, b_spec_file)))

    def getGeneratedFileNames(self, element: "RPModelElement") -> "RPCollection":
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
        return RPCollection(self.call_com(lambda: self._com.getGeneratedFileNames(element._com)))


class RPDiagSynthAPI(RPModelElement):
    """Wraps ``IRPDiagSynthAPI``."""

    # IRPDiagSynthAPI method parity checklist:
    # [x] addInstance                  [x] impl  [x] docstring  [x] test
    # [x] addSynthSDToModel2           [x] impl  [x] docstring  [x] test
    # [x] createSD2                    [x] impl  [x] docstring  [x] test
    # [x] receiveMessage               [x] impl  [x] docstring  [x] test
    # [x] removeSynthSDToModel2        [x] impl  [x] docstring  [x] test
    # [x] sDAddConditionMark           [x] impl  [x] docstring  [x] test
    # [x] sendMessage                  [x] impl  [x] docstring  [x] test
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # No deprecated IRPDiagSynthAPI methods.

    def addInstance(self, added_to_s_d: int, instance_nav_exp: str) -> int:
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
        return self.call_com(lambda: self._com.addInstance(added_to_s_d, instance_nav_exp))

    def addSynthSDToModel2(self, p_msc_orig: "RPSequenceDiagram", synth_s_d: int, open_s_d: int) -> int:
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
        return self.call_com(lambda: self._com.addSynthSDToModel2(p_msc_orig._com, synth_s_d, open_s_d))

    def createSD2(self, p_msc_orig: "RPSequenceDiagram", testedmscname: str) -> int:
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
        return self.call_com(lambda: self._com.createSD2(p_msc_orig._com, testedmscname))

    def receiveMessage(self, p_tested_s_d: int, p_event_sent: int) -> None:
        """Receives a sequence diagram message.

        Args:
            p_tested_s_d: The handle of the tested sequence diagram.
            p_event_sent: The handle of the sent event.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagSynthAPI::receiveMessage(long pTestedSD, long pEventSent)
        """
        self.call_com(lambda: self._com.receiveMessage(p_tested_s_d, p_event_sent))

    def removeSynthSDToModel2(self, p_msc_orig: "RPSequenceDiagram") -> int:
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
        return self.call_com(lambda: self._com.removeSynthSDToModel2(p_msc_orig._com))

    def sDAddConditionMark(self, p_tested_s_d: int, instance: str, text: str, type_: str) -> int:
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
        return self.call_com(lambda: self._com.sDAddConditionMark(p_tested_s_d, instance, text, type_))

    def sendMessage(self, p_tested_s_d: int, source: str, target: str, event: str, operation: str, type_: str) -> int:
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
        return self.call_com(lambda: self._com.sendMessage(p_tested_s_d, source, target, event, operation, type_))


class RPExternalCheckRegistry(RPModelElement):
    """Wraps ``IRPExternalCheckRegistry``."""

    # IRPExternalCheckRegistry method parity checklist:
    # [x] appendFailedElementsComments [x] impl  [x] docstring  [x] test
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # [x] setFailedElementsComments    [x] impl  [x] docstring  [x] test
    # No deprecated IRPExternalCheckRegistry methods.

    def appendFailedElementsComments(self, str_val: str) -> None:
        """Appends comments for failed elements.

        Args:
            str_val: The comments string to append.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalCheckRegistry::appendFailedElementsComments(java.lang.String strVal)
        """
        self.call_com(lambda: self._com.appendFailedElementsComments(str_val))

    def setFailedElementsComments(self, str_val: str) -> None:
        """Sets the comments for failed elements.

        Args:
            str_val: The comments string to set.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalCheckRegistry::setFailedElementsComments(java.lang.String strVal)
        """
        self.call_com(lambda: self._com.setFailedElementsComments(str_val))


class RPExternalRoundtripInvoker(RPModelElement):
    """Wraps ``IRPExternalRoundtripInvoker``."""

    # IRPExternalRoundtripInvoker method parity checklist:
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # No deprecated IRPExternalRoundtripInvoker methods.


class RPIntegrator(RPModelElement):
    """Wraps ``IRPIntegrator``."""

    # IRPIntegrator method parity checklist:
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # No deprecated IRPIntegrator methods.


class RPRhapsodyServer(RPModelElement):
    """Wraps ``IRPRhapsodyServer``."""

    # IRPRhapsodyServer method parity checklist:
    # [x] getApplication               [x] impl  [x] docstring  [x] test
    # [x] getHiddenApplication         [x] impl  [x] docstring  [x] test
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # [x] getUninitializedApplication  [x] impl  [x] docstring  [x] test
    # [x] initializeApplication        [x] impl  [x] docstring  [x] test
    # No deprecated IRPRhapsodyServer methods.

    def getApplication(self) -> "RhapsodyApplication":
        """Returns the Rhapsody application.

        Returns:
            Any: The IRPApplication instance.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRhapsodyServer::getApplication()
        """
        return RhapsodyApplication(self.call_com(lambda: self._com.getApplication()))

    def getHiddenApplication(self) -> "RhapsodyApplication":
        """Returns a hidden Rhapsody application instance.

        Returns:
            Any: The hidden IRPApplication instance.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRhapsodyServer::getHiddenApplication()
        """
        return RhapsodyApplication(self.call_com(lambda: self._com.getHiddenApplication()))

    def getUninitializedApplication(self) -> "RhapsodyApplication":
        """Returns an uninitialized Rhapsody application instance.

        Returns:
            Any: The uninitialized IRPApplication instance.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRhapsodyServer::getUninitializedApplication()
        """
        return RhapsodyApplication(self.call_com(lambda: self._com.getUninitializedApplication()))

    def initializeApplication(self, p_val: "RhapsodyApplication") -> None:
        """Initializes the Rhapsody application.

        Args:
            p_val: The IRPApplication instance to initialize.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPRhapsodyServer::initializeApplication(com.telelogic.rhapsody.core.IRPApplication pVal)
        """
        self.call_com(lambda: self._com.initializeApplication(p_val._com))


class RPRoundTrip(RPModelElement):
    """Wraps ``IRPRoundTrip``."""

    # IRPRoundTrip method parity checklist:
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # [x] roundtripFile                [x] impl  [x] docstring  [x] test
    # No deprecated IRPRoundTrip methods.

    def roundtripFile(self, filename: str, re_generate_file: int) -> "RPCollection":
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
        return RPCollection(self.call_com(lambda: self._com.roundtripFile(filename, re_generate_file)))


class RPSearchManager(RPModelElement):
    """Wraps ``IRPSearchManager``: used to carry out a search in a Rhapsody model."""

    # IRPSearchManager method parity checklist:
    # [x] createSearchQuery            [x] impl  [x] docstring  [x] test
    # [x] search                       [x] impl  [x] docstring  [x] test
    # [x] searchAndShowResults         [x] impl  [x] docstring  [x] test
    # [x] searchAsync                  [x] impl  [x] docstring  [x] test
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # No deprecated IRPSearchManager methods.

    def createSearchQuery(self) -> "RPSearchQuery":
        """Creates a search query object.

        Returns:
            Any: The search query object that was created.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchManager::createSearchQuery()
        """
        return RPSearchQuery(self.call_com(lambda: self._com.createSearchQuery()))

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
        return RPCollection(self.call_com(lambda: self._com.search(p_search_query._com)))

    def searchAndShowResults(self, p_search_query: "RPSearchQuery") -> None:
        """Searches the model using the specified search query, and shows the
        results in the Search tab of the Output window.

        Args:
            p_search_query: The search query to use to search the model.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchManager::searchAndShowResults(com.telelogic.rhapsody.core.IRPSearchQuery pSearchQuery)
        """
        self.call_com(lambda: self._com.searchAndShowResults(p_search_query._com))

    def searchAsync(self, p_search_query: "RPSearchQuery") -> None:
        """Searches the model asynchronously, allowing you to continue working
        in Rhapsody.

        Args:
            p_search_query: The search query to use to search the model.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchManager::searchAsync(com.telelogic.rhapsody.core.IRPSearchQuery pSearchQuery)
        """
        self.call_com(lambda: self._com.searchAsync(p_search_query._com))


class RPSearchQuery(RPModelElement):
    """Wraps ``IRPSearchQuery``: represents the search criteria objects that are used by IRPSearchManager to carry out searches."""

    # IRPSearchQuery method parity checklist:
    # [x] addDiagramToViewsList        [x] impl  [x] docstring  [x] test
    # [x] addFilterElementType         [x] impl  [x] docstring  [x] test
    # [x] addFilterSearchInField       [x] impl  [x] docstring  [x] test
    # [x] addFilterStereotype          [x] impl  [x] docstring  [x] test
    # [x] addFilterSubQuery            [x] impl  [x] docstring  [x] test
    # [x] addMatrixToViewsList         [x] impl  [x] docstring  [x] test
    # [x] addSearchScope               [x] impl  [x] docstring  [x] test
    # [x] addTableToViewsList          [x] impl  [x] docstring  [x] test
    # [x] getFilterElementTypes        [x] impl  [x] docstring  [x] test
    # [x] getFilterReferenceIncludeReferencedElementsInSearchResults [x] impl  [x] docstring  [x] test
    # [x] getFilterReferenceNameOfReferencedElements [x] impl  [x] docstring  [x] test
    # [x] getFilterReferenceNumberOfReferences [x] impl  [x] docstring  [x] test
    # [x] getFilterReferenceQuantityOperator [x] impl  [x] docstring  [x] test
    # [x] getFilterReferenceRelationKind [x] impl  [x] docstring  [x] test
    # [x] getFilterReferenceStereotypeOfReferencedElements [x] impl  [x] docstring  [x] test
    # [x] getFilterReferenceTypeOfReferencedElements [x] impl  [x] docstring  [x] test
    # [x] getFilterSearchInFields      [x] impl  [x] docstring  [x] test
    # [x] getFilterStereotypes         [x] impl  [x] docstring  [x] test
    # [x] getFilterSubQueries          [x] impl  [x] docstring  [x] test
    # [x] getFilterSubQueryUseWithNotOperator [x] impl  [x] docstring  [x] test
    # [x] getFilterTagFindAs           [x] impl  [x] docstring  [x] test
    # [x] getFilterTagMatchCase        [x] impl  [x] docstring  [x] test
    # [x] getFilterTagMatchWholeWord   [x] impl  [x] docstring  [x] test
    # [x] getFilterTagName             [x] impl  [x] docstring  [x] test
    # [x] getFilterTagValue            [x] impl  [x] docstring  [x] test
    # [x] getSearchScopeElements       [x] impl  [x] docstring  [x] test
    # [x] getView                      [x] impl  [x] docstring  [x] test
    # [x] getViewCount                 [x] impl  [x] docstring  [x] test
    # [x] loadFromQuery                [x] impl  [x] docstring  [x] test
    # [x] removeFilterElementTypes     [x] impl  [x] docstring  [x] test
    # [x] removeFilterReferences       [x] impl  [x] docstring  [x] test
    # [x] removeFilterSearchInFields   [x] impl  [x] docstring  [x] test
    # [x] removeFilterStereotypes      [x] impl  [x] docstring  [x] test
    # [x] removeFilterSubQueries       [x] impl  [x] docstring  [x] test
    # [x] removeFilterSubQuery         [x] impl  [x] docstring  [x] test
    # [x] removeFilterTag              [x] impl  [x] docstring  [x] test
    # [x] removeSearchScopeElement     [x] impl  [x] docstring  [x] test
    # [x] removeView                   [x] impl  [x] docstring  [x] test
    # [x] resetSearchScope             [x] impl  [x] docstring  [x] test
    # [x] saveAsQuery                  [x] impl  [x] docstring  [x] test
    # [x] setFilterReference           [x] impl  [x] docstring  [x] test
    # [x] setFilterTag                 [x] impl  [x] docstring  [x] test
    # [x] getFilterSubQueriesOperator  [x] impl  [x] docstring  [x] test
    # [x] getFilterTagLocalOnly        [x] impl  [x] docstring  [x] test
    # [x] getFilterUnitsOnly           [x] impl  [x] docstring  [x] test
    # [x] getFilterUnresolvedKind      [x] impl  [x] docstring  [x] test
    # [x] getIncludeDescendants        [x] impl  [x] docstring  [x] test
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # [x] getMatchCase                 [x] impl  [x] docstring  [x] test
    # [x] getMatchSpecifiedCriteria    [x] impl  [x] docstring  [x] test
    # [x] getMatchWholeWord            [x] impl  [x] docstring  [x] test
    # [x] getSearchFindAsOption        [x] impl  [x] docstring  [x] test
    # [x] getSearchScopeObject         [x] impl  [x] docstring  [x] test
    # [x] getSearchText                [x] impl  [x] docstring  [x] test
    # [x] getViewIncludeModelElements  [x] impl  [x] docstring  [x] test
    # [x] getViewsToSearch             [x] impl  [x] docstring  [x] test
    # [x] setFilterSubQueriesOperator  [x] impl  [x] docstring  [x] test
    # [x] setFilterTagLocalOnly        [x] impl  [x] docstring  [x] test
    # [x] setFilterUnitsOnly           [x] impl  [x] docstring  [x] test
    # [x] setFilterUnresolvedKind      [x] impl  [x] docstring  [x] test
    # [x] setIncludeDescendants        [x] impl  [x] docstring  [x] test
    # [x] setMatchCase                 [x] impl  [x] docstring  [x] test
    # [x] setMatchSpecifiedCriteria    [x] impl  [x] docstring  [x] test
    # [x] setMatchWholeWord            [x] impl  [x] docstring  [x] test
    # [x] setSearchFindAsOption        [x] impl  [x] docstring  [x] test
    # [x] setSearchScopeObject         [x] impl  [x] docstring  [x] test
    # [x] setSearchText                [x] impl  [x] docstring  [x] test
    # [x] setViewIncludeModelElements  [x] impl  [x] docstring  [x] test
    # [x] setViewsToSearch             [x] impl  [x] docstring  [x] test
    # [deprecated] addSearchScope  - skipped (deprecated in Rhapsody Java API)
    # [deprecated] getSearchScopeElements  - skipped (deprecated in Rhapsody Java API)
    # [deprecated] getSearchScopeObject  - skipped (deprecated in Rhapsody Java API)
    # [deprecated] setSearchScopeObject  - skipped (deprecated in Rhapsody Java API)
    # No non-deprecated IRPSearchQuery methods.

    def addDiagramToViewsList(self, view: "RPDiagram") -> int:
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
        return self.call_com(lambda: self._com.addDiagramToViewsList(view._com))

    def addFilterElementType(self, element_type: str) -> None:
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
        self.call_com(lambda: self._com.addFilterElementType(element_type))

    def addFilterSearchInField(self, search_in_field: str) -> None:
        """Adds an element field to the list of element fields that the search
        should be applied to, for example, element name or element description.

        Args:
            search_in_field: The element field to add to the list of element
                fields to search.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addFilterSearchInField(java.lang.String searchInField)
        """
        self.call_com(lambda: self._com.addFilterSearchInField(search_in_field))

    def addFilterStereotype(self, stereotype: "RPStereotype") -> None:
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
        self.call_com(lambda: self._com.addFilterStereotype(stereotype._com))

    def addFilterSubQuery(self, sub_query: "RPTableLayout", use_with_not_operator: int) -> None:
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
        self.call_com(lambda: self._com.addFilterSubQuery(sub_query._com, use_with_not_operator))

    def addMatrixToViewsList(self, view: "RPMatrixView") -> int:
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
        return self.call_com(lambda: self._com.addMatrixToViewsList(view._com))

    def addSearchScope(self, scope_element: "RPModelElement") -> None:
        """Adds an element to the scope for the search.

        Args:
            scope_element: Model element that represents a part of the model
                that should be searched, for example, a specific package.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::addSearchScope(com.telelogic.rhapsody.core.IRPModelElement scopeElement)
        """
        self.call_com(lambda: self._com.addSearchScope(scope_element._com))

    def addTableToViewsList(self, view: "RPTableView") -> int:
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
        return self.call_com(lambda: self._com.addTableToViewsList(view._com))

    def getFilterElementTypes(self) -> "RPCollection":
        """Returns the element types that are to be searched for the search text.

        Returns:
            RPCollection: The element types that are to be searched.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterElementTypes()
        """
        return RPCollection(self._get_method_or_property(self._com, "getFilterElementTypes", "filterElementTypes"))

    def getFilterReferenceIncludeReferencedElementsInSearchResults(self) -> int:
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
        return int(self._get_method_or_property(self._com, "getFilterReferenceIncludeReferencedElementsInSearchResults", "filterReferenceIncludeReferencedElementsInSearchResults"))

    def getFilterReferenceNameOfReferencedElements(self) -> str:
        """Returns the model element name that was specified for the reference
        criterion that was defined.

        Returns:
            str: The model element name specified for the reference criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceNameOfReferencedElements()
        """
        return str(self._get_method_or_property(self._com, "getFilterReferenceNameOfReferencedElements", "filterReferenceNameOfReferencedElements"))

    def getFilterReferenceNumberOfReferences(self) -> int:
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
        return int(self._get_method_or_property(self._com, "getFilterReferenceNumberOfReferences", "filterReferenceNumberOfReferences"))

    def getFilterReferenceQuantityOperator(self) -> str:
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
        return str(self._get_method_or_property(self._com, "getFilterReferenceQuantityOperator", "filterReferenceQuantityOperator"))

    def getFilterReferenceRelationKind(self) -> str:
        """Returns the type of reference used in the search criterion, for
        example, aggregates or incoming relations.

        Returns:
            str: The type of reference used in the search criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceRelationKind()
        """
        return str(self._get_method_or_property(self._com, "getFilterReferenceRelationKind", "filterReferenceRelationKind"))

    def getFilterReferenceStereotypeOfReferencedElements(self) -> str:
        """Returns the stereotype that was specified for the reference criterion
        that was defined.

        Returns:
            str: The stereotype specified for the reference criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceStereotypeOfReferencedElements()
        """
        return str(self._get_method_or_property(self._com, "getFilterReferenceStereotypeOfReferencedElements", "filterReferenceStereotypeOfReferencedElements"))

    def getFilterReferenceTypeOfReferencedElements(self) -> str:
        """Returns the model element type that was specified for the reference
        criterion that was defined.

        Returns:
            str: The model element type specified for the reference criterion.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterReferenceTypeOfReferencedElements()
        """
        return str(self._get_method_or_property(self._com, "getFilterReferenceTypeOfReferencedElements", "filterReferenceTypeOfReferencedElements"))

    def getFilterSearchInFields(self) -> "RPCollection":
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
        return RPCollection(self._get_method_or_property(self._com, "getFilterSearchInFields", "filterSearchInFields"))

    def getFilterStereotypes(self) -> "RPCollection":
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
        return RPCollection(self._get_method_or_property(self._com, "getFilterStereotypes", "filterStereotypes"))

    def getFilterSubQueries(self) -> "RPCollection":
        """Returns the subqueries that were specified for the search.

        Returns:
            RPCollection: The subqueries that were specified for the search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterSubQueries()
        """
        return RPCollection(self._get_method_or_property(self._com, "getFilterSubQueries", "filterSubQueries"))

    def getFilterSubQueryUseWithNotOperator(self, sub_query: "RPTableLayout") -> int:
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
        return self.call_com(lambda: self._com.getFilterSubQueryUseWithNotOperator(sub_query._com))

    def getFilterTagFindAs(self) -> str:
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
        return str(self._get_method_or_property(self._com, "getFilterTagFindAs", "filterTagFindAs"))

    def getFilterTagMatchCase(self) -> int:
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
        return int(self._get_method_or_property(self._com, "getFilterTagMatchCase", "filterTagMatchCase"))

    def getFilterTagMatchWholeWord(self) -> int:
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
        return int(self._get_method_or_property(self._com, "getFilterTagMatchWholeWord", "filterTagMatchWholeWord"))

    def getFilterTagName(self) -> str:
        """Returns the tag name specified as a criterion for the search.

        Returns:
            str: The tag name specified as a criterion for the search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterTagName()
        """
        return str(self._get_method_or_property(self._com, "getFilterTagName", "filterTagName"))

    def getFilterTagValue(self) -> str:
        """Returns the tag value specified as a criterion for the search.

        Returns:
            str: The tag value specified as a criterion for the search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterTagValue()
        """
        return str(self._get_method_or_property(self._com, "getFilterTagValue", "filterTagValue"))

    def getSearchScopeElements(self) -> "RPCollection":
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
        return RPCollection(self._get_method_or_property(self._com, "getSearchScopeElements", "searchScopeElements"))

    def getView(self, index: int) -> "RPModelElement":
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
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getView(index)))

    def getViewCount(self) -> int:
        """Returns the number of views in the list of views that are to be
        searched.

        Returns:
            int: The number of views in the list of views to be searched.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getViewCount()
        """
        return int(self._get_method_or_property(self._com, "getViewCount", "viewCount"))

    def loadFromQuery(self, query: "RPTableLayout") -> None:
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
        self.call_com(lambda: self._com.loadFromQuery(query._com))

    def removeFilterElementTypes(self) -> None:
        """Removes any element type filters that you defined to limit the search
        to certain element types.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterElementTypes()
        """
        self.call_com(lambda: self._com.removeFilterElementTypes())

    def removeFilterReferences(self) -> None:
        """Removes reference search criterion that was defined for the search
        query.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterReferences()
        """
        self.call_com(lambda: self._com.removeFilterReferences())

    def removeFilterSearchInFields(self) -> None:
        """Removes any element field filters that you defined to limit the
        search to certain element fields.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterSearchInFields()
        """
        self.call_com(lambda: self._com.removeFilterSearchInFields())

    def removeFilterStereotypes(self) -> None:
        """Removes any stereotype filter that was defined to limit the search to
        model elements that have certain stereotypes applied to them.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterStereotypes()
        """
        self.call_com(lambda: self._com.removeFilterStereotypes())

    def removeFilterSubQueries(self) -> None:
        """Removes the subquery criteria that were specified for the search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterSubQueries()
        """
        self.call_com(lambda: self._com.removeFilterSubQueries())

    def removeFilterSubQuery(self, sub_query: "RPTableLayout") -> int:
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
        return self.call_com(lambda: self._com.removeFilterSubQuery(sub_query._com))

    def removeFilterTag(self) -> None:
        """Removes the tag name and tag value criteria that were defined for
        the search query.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeFilterTag()
        """
        self.call_com(lambda: self._com.removeFilterTag())

    def removeSearchScopeElement(self, scope_element: "RPModelElement") -> int:
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
        return self.call_com(lambda: self._com.removeSearchScopeElement(scope_element._com))

    def removeView(self, index: int) -> None:
        """Removes the specified view from the list of views to be searched for
        the search text.

        Args:
            index: The index of the view in the list of views to search.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::removeView(int Index)
        """
        self.call_com(lambda: self._com.removeView(index))

    def resetSearchScope(self) -> None:
        """Resets the search scope to include the entire project, or all
        projects if multiple projects are open.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::resetSearchScope()
        """
        self.call_com(lambda: self._com.resetSearchScope())

    def saveAsQuery(self, query_owner: "RPPackage") -> "RPTableLayout":
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
        return RPTableLayout(self.call_com(lambda: self._com.saveAsQuery(query_owner._com)))

    def setFilterReference(
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
        self.call_com(
            lambda: self._com.setFilterReference(
                quantity_operator,
                number_of_references,
                relation_kind,
                type_of_referenced_elements,
                stereotype_of_referenced_elements,
                name_of_referenced_elements,
                include_referenced_elements_in_search_results,
            )
        )

    def setFilterTag(self, tag_name: str, tag_value: str, match_case: int, match_whole_word: int, find_as: str) -> None:
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
        self.call_com(lambda: self._com.setFilterTag(tag_name, tag_value, match_case, match_whole_word, find_as))

    def getFilterSubQueriesOperator(self) -> str:
        """Returns indication of how the specified subqueries are to be combined
        in the search.

        Returns:
            str: Indication of how the subqueries are to be combined - one of
            the constants defined in IRPSearchQuery.SubQueriesOperator.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterSubQueriesOperator()
        """
        return str(self._get_method_or_property(self._com, "getFilterSubQueriesOperator", "filterSubQueriesOperator"))

    def getFilterTagLocalOnly(self) -> int:
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
        return int(self._get_method_or_property(self._com, "getFilterTagLocalOnly", "filterTagLocalOnly"))

    def getFilterUnitsOnly(self) -> int:
        """Checks whether the search is limited to model elements that are
        saved units.

        Returns:
            int: 1 if the search is limited to saved units, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterUnitsOnly()
        """
        return int(self._get_method_or_property(self._com, "getFilterUnitsOnly", "filterUnitsOnly"))

    def getFilterUnresolvedKind(self) -> str:
        """Returns the method that was specified for handling unresolved
        elements in the search.

        Returns:
            str: The method specified for handling unresolved elements - one of
            the constants from IRPSearchQuery.UnresolvedKind.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getFilterUnresolvedKind()
        """
        return str(self._get_method_or_property(self._com, "getFilterUnresolvedKind", "filterUnresolvedKind"))

    def getIncludeDescendants(self) -> int:
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
        return int(self._get_method_or_property(self._com, "getIncludeDescendants", "includeDescendants"))

    def getMatchCase(self) -> int:
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
        return int(self._get_method_or_property(self._com, "getMatchCase", "matchCase"))

    def getMatchSpecifiedCriteria(self) -> int:
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
        return int(self._get_method_or_property(self._com, "getMatchSpecifiedCriteria", "matchSpecifiedCriteria"))

    def getMatchWholeWord(self) -> int:
        """Checks whether a whole word match was specified for the search.

        Returns:
            int: 1 if a whole word match was specified, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getMatchWholeWord()
        """
        return int(self._get_method_or_property(self._com, "getMatchWholeWord", "matchWholeWord"))

    def getSearchFindAsOption(self) -> str:
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
        return str(self._get_method_or_property(self._com, "getSearchFindAsOption", "searchFindAsOption"))

    def getSearchScopeObject(self) -> "RPModelElement":
        """Returns the scope specified for the search.

        Deprecated. Use getSearchScopeElements instead, as Rhapsody now
        allows specifying a list of elements as the scope.

        Returns:
            Any: The model element that constitutes the scope for the search.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getSearchScopeObject()
        """
        return AbstractRPModelElement.wrap(self._get_method_or_property(self._com, "getSearchScopeObject", "searchScopeObject"))

    def getSearchText(self) -> str:
        """Returns the text that was specified as the text to search for.

        Returns:
            str: The text to search for.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getSearchText()
        """
        return str(self._get_method_or_property(self._com, "getSearchText", "searchText"))

    def getViewIncludeModelElements(self) -> int:
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
        return int(self._get_method_or_property(self._com, "getViewIncludeModelElements", "viewIncludeModelElements"))

    def getViewsToSearch(self) -> str:
        """Returns indication of which views (diagrams, tables, and matrices)
        are supposed to be searched.

        Returns:
            str: Indication of which views are supposed to be searched - one of
            the constants defined in IRPSearchQuery.ViewsToSearch.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::getViewsToSearch()
        """
        return str(self._get_method_or_property(self._com, "getViewsToSearch", "viewsToSearch"))

    def setFilterSubQueriesOperator(self, filter_sub_queries_operator: str) -> None:
        """Specifies how the various subqueries specified should be combined -
        as an AND operation or an OR operation.

        Args:
            filter_sub_queries_operator: Use one of the constants defined in
                IRPSearchQuery.SubQueriesOperator to indicate how the specified
                subqueries should be combined.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setFilterSubQueriesOperator(java.lang.String filterSubQueriesOperator)
        """
        self.call_com(lambda: self._com.setFilterSubQueriesOperator(filter_sub_queries_operator))

    def setFilterTagLocalOnly(self, filter_tag_local_only: int) -> None:
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
        self.call_com(lambda: self._com.setFilterTagLocalOnly(filter_tag_local_only))

    def setFilterUnitsOnly(self, filter_units_only: int) -> None:
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
        self.call_com(lambda: self._com.setFilterUnitsOnly(filter_units_only))

    def setFilterUnresolvedKind(self, filter_unresolved_kind: str) -> None:
        """Specifies how unresolved elements should be handled in the search.

        Args:
            filter_unresolved_kind: How unresolved elements should be handled in
                the search. One of the constants from
                IRPSearchQuery.UnresolvedKind.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setFilterUnresolvedKind(java.lang.String filterUnresolvedKind)
        """
        self.call_com(lambda: self._com.setFilterUnresolvedKind(filter_unresolved_kind))

    def setIncludeDescendants(self, include_descendants: int) -> None:
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
        self.call_com(lambda: self._com.setIncludeDescendants(include_descendants))

    def setMatchCase(self, match_case: int) -> None:
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
        self.call_com(lambda: self._com.setMatchCase(match_case))

    def setMatchSpecifiedCriteria(self, match_specified_criteria: int) -> None:
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
        self.call_com(lambda: self._com.setMatchSpecifiedCriteria(match_specified_criteria))

    def setMatchWholeWord(self, match_whole_word: int) -> None:
        """Specifies whether the search should require whole word matches.

        Args:
            match_whole_word: Use 1 to specify that a whole word match is
                required, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setMatchWholeWord(int matchWholeWord)
        """
        self.call_com(lambda: self._com.setMatchWholeWord(match_whole_word))

    def setSearchFindAsOption(self, search_find_as_option: str) -> None:
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
        self.call_com(lambda: self._com.setSearchFindAsOption(search_find_as_option))

    def setSearchScopeObject(self, search_scope_object: "RPModelElement") -> None:
        """Sets the scope for the search.

        Deprecated. Use addSearchScope instead, as Rhapsody now allows
        specifying a list of elements as the scope.

        Args:
            search_scope_object: The model element to set as the scope for the
                search.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setSearchScopeObject(com.telelogic.rhapsody.core.IRPModelElement searchScopeObject)
        """
        self.call_com(lambda: self._com.setSearchScopeObject(search_scope_object._com))

    def setSearchText(self, search_text: str) -> None:
        """Specifies the text that should be searched for.

        Args:
            search_text: The text that should be searched for.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchQuery::setSearchText(java.lang.String searchText)
        """
        self.call_com(lambda: self._com.setSearchText(search_text))

    def setViewIncludeModelElements(self, view_include_model_elements: int) -> None:
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
        self.call_com(lambda: self._com.setViewIncludeModelElements(view_include_model_elements))

    def setViewsToSearch(self, views_to_search: str) -> None:
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
        self.call_com(lambda: self._com.setViewsToSearch(views_to_search))


class RPSearchResult(RPModelElement):
    """Wraps ``IRPSearchResult``."""

    # IRPSearchResult method parity checklist:
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # [x] getMatchedField              [x] impl  [x] docstring  [x] test
    # [x] getMatchedFields             [x] impl  [x] docstring  [x] test
    # [x] getMatchedObject             [x] impl  [x] docstring  [x] test
    # [x] getName                      [x] impl  [x] docstring  [x] test
    # No deprecated IRPSearchResult methods.

    def getMatchedField(self) -> str:
        """Returns the property matchedField.

        Returns:
            str: The matched field.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchResult::getMatchedField()
        """
        return str(self._get_method_or_property(self._com, "getMatchedField", "matchedField"))

    def getMatchedFields(self) -> "RPCollection":
        """Returns the property matchedFields.

        Returns:
            RPCollection: The matched fields.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchResult::getMatchedFields()
        """
        return RPCollection(self._get_method_or_property(self._com, "getMatchedFields", "matchedFields"))

    def getMatchedObject(self) -> "RPModelElement":
        """Returns the property matchedObject.

        Returns:
            Any: The matched model element.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchResult::getMatchedObject()
        """
        return AbstractRPModelElement.wrap(self._get_method_or_property(self._com, "getMatchedObject", "matchedObject"))

    def getName(self) -> str:
        """Returns the property name.

        Returns:
            str: The name.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPSearchResult::getName()
        """
        return str(self._get_method_or_property(self._com, "getName", "name"))


class RPCodeGenSimplifiersRegistry(RPBaseExternalCodeGeneratorTool):
    """Wraps ``IRPCodeGenSimplifiersRegistry``."""

    # IRPCodeGenSimplifiersRegistry method parity checklist:
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # [x] notifySimplificationDone     [x] impl  [x] docstring  [x] test
    # [inherited] IRPBaseExternalCodeGeneratorTool methods (covered by RPBaseExternalCodeGeneratorTool checklist)
    # No deprecated IRPCodeGenSimplifiersRegistry methods.

    def notifySimplificationDone(self) -> None:
        """Notifies that simplification is done.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPCodeGenSimplifiersRegistry::notifySimplificationDone()
        """
        self.call_com(lambda: self._com.notifySimplificationDone())


class RPExternalCodeGeneratorInvoker(RPBaseExternalCodeGeneratorTool):
    """Wraps ``IRPExternalCodeGeneratorInvoker``."""

    # IRPExternalCodeGeneratorInvoker method parity checklist:
    # [x] getInterfaceName             [x] impl (inherited from RPModelElement)
    # [x] notifyGenerationDone         [x] impl  [x] docstring  [x] test
    # [inherited] IRPBaseExternalCodeGeneratorTool methods (covered by RPBaseExternalCodeGeneratorTool checklist)
    # No deprecated IRPExternalCodeGeneratorInvoker methods.

    def notifyGenerationDone(self) -> None:
        """Notifies that code generation is done.

        Raises:
            RhapsodyRuntimeException: If an error occurs in the Rhapsody API.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalCodeGeneratorInvoker::notifyGenerationDone()
        """
        self.call_com(lambda: self._com.notifyGenerationDone())
