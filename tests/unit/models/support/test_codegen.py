from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.graphics.model_graphics import RPTableLayout
from rhapsody_cli.models.support.model_codegen import (
    RPBaseExternalCodeGeneratorTool,
    RPCodeGenerator,
    RPCodeGenSimplifiersRegistry,
    RPDiagSynthAPI,
    RPExternalCheckRegistry,
    RPExternalCodeGeneratorInvoker,
    RPRhapsodyServer,
    RPRoundTrip,
    RPSearchManager,
    RPSearchQuery,
    RPSearchResult,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_RPBaseExternalCodeGeneratorTool_advance_code_gen_progress_bar_delegates_to_com():
    fake = make_fake_element("BaseExternalCodeGeneratorTool")
    obj = RPBaseExternalCodeGeneratorTool(fake)
    obj.advanceCodeGenProgressBar()
    fake.advanceCodeGenProgressBar.assert_called_once_with()


def test_RPBaseExternalCodeGeneratorTool_should_abort_code_generation_delegates_to_com():
    fake = make_fake_element("BaseExternalCodeGeneratorTool")
    fake.shouldAbortCodeGeneration.return_value = 1
    obj = RPBaseExternalCodeGeneratorTool(fake)
    result = obj.shouldAbortCodeGeneration()
    fake.shouldAbortCodeGeneration.assert_called_once_with()
    assert result == 1


def test_RPBaseExternalCodeGeneratorTool_write_code_gen_message_delegates_to_com():
    fake = make_fake_element("BaseExternalCodeGeneratorTool")
    obj = RPBaseExternalCodeGeneratorTool(fake)
    obj.writeCodeGenMessage("x")
    fake.writeCodeGenMessage.assert_called_once_with("x")


def test_RPCodeGenerator_get_code_annotations_delegates_to_com():
    fake = make_fake_element("CodeGenerator")
    target = make_fake_element("X")
    inner = make_fake_element("X", getName="y")
    fake.getCodeAnnotations.return_value = make_fake_collection([inner])
    obj = RPCodeGenerator(fake)
    result = obj.getCodeAnnotations(AbstractRPModelElement.wrap(target), 1)
    fake.getCodeAnnotations.assert_called_once_with(target, 1)
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPCodeGenerator_get_generated_file_names_delegates_to_com():
    fake = make_fake_element("CodeGenerator")
    target = make_fake_element("X")
    inner = make_fake_element("X", getName="y")
    fake.getGeneratedFileNames.return_value = make_fake_collection([inner])
    obj = RPCodeGenerator(fake)
    result = obj.getGeneratedFileNames(AbstractRPModelElement.wrap(target))
    fake.getGeneratedFileNames.assert_called_once_with(target)
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPDiagSynthAPI_add_instance_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    fake.addInstance.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.addInstance(1, "x")
    fake.addInstance.assert_called_once_with(1, "x")
    assert result == 1


def test_RPDiagSynthAPI_add_synth_s_d_to_model2_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    target = make_fake_element("X")
    fake.addSynthSDToModel2.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.addSynthSDToModel2(AbstractRPModelElement.wrap(target), 1, 1)
    fake.addSynthSDToModel2.assert_called_once_with(target, 1, 1)
    assert result == 1


def test_RPDiagSynthAPI_create_s_d2_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    target = make_fake_element("X")
    fake.createSD2.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.createSD2(AbstractRPModelElement.wrap(target), "x")
    fake.createSD2.assert_called_once_with(target, "x")
    assert result == 1


def test_RPDiagSynthAPI_receive_message_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    obj = RPDiagSynthAPI(fake)
    obj.receiveMessage(1, 1)
    fake.receiveMessage.assert_called_once_with(1, 1)


def test_RPDiagSynthAPI_remove_synth_s_d_to_model2_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    target = make_fake_element("X")
    fake.removeSynthSDToModel2.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.removeSynthSDToModel2(AbstractRPModelElement.wrap(target))
    fake.removeSynthSDToModel2.assert_called_once_with(target)
    assert result == 1


def test_RPDiagSynthAPI_s_d_add_condition_mark_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    fake.sDAddConditionMark.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.sDAddConditionMark(1, "x", "x", "x")
    fake.sDAddConditionMark.assert_called_once_with(1, "x", "x", "x")
    assert result == 1


def test_RPDiagSynthAPI_send_message_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    fake.sendMessage.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.sendMessage(1, "x", "x", "x", "x", "x")
    fake.sendMessage.assert_called_once_with(1, "x", "x", "x", "x", "x")
    assert result == 1


def test_RPExternalCheckRegistry_append_failed_elements_comments_delegates_to_com():
    fake = make_fake_element("ExternalCheckRegistry")
    obj = RPExternalCheckRegistry(fake)
    obj.appendFailedElementsComments("x")
    fake.appendFailedElementsComments.assert_called_once_with("x")


def test_RPExternalCheckRegistry_set_failed_elements_comments_delegates_to_com():
    fake = make_fake_element("ExternalCheckRegistry")
    obj = RPExternalCheckRegistry(fake)
    obj.setFailedElementsComments("file.txt")
    fake.setFailedElementsComments.assert_called_once_with("file.txt")


def test_RPRhapsodyServer_get_application_delegates_to_com():
    fake = make_fake_element("RhapsodyServer")
    app_fake = make_fake_element("Application")
    fake.getApplication.return_value = app_fake
    obj = RPRhapsodyServer(fake)
    result = obj.getApplication()
    assert isinstance(result, RhapsodyApplication)


def test_RPRhapsodyServer_get_hidden_application_delegates_to_com():
    fake = make_fake_element("RhapsodyServer")
    app_fake = make_fake_element("Application")
    fake.getHiddenApplication.return_value = app_fake
    obj = RPRhapsodyServer(fake)
    result = obj.getHiddenApplication()
    assert isinstance(result, RhapsodyApplication)


def test_RPRhapsodyServer_get_uninitialized_application_delegates_to_com():
    fake = make_fake_element("RhapsodyServer")
    app_fake = make_fake_element("Application")
    fake.getUninitializedApplication.return_value = app_fake
    obj = RPRhapsodyServer(fake)
    result = obj.getUninitializedApplication()
    assert isinstance(result, RhapsodyApplication)


def test_RPRhapsodyServer_initialize_application_delegates_to_com():
    fake = make_fake_element("RhapsodyServer")
    target = make_fake_element("X")
    obj = RPRhapsodyServer(fake)
    obj.initializeApplication(AbstractRPModelElement.wrap(target))
    fake.initializeApplication.assert_called_once_with(target)


def test_RPRoundTrip_roundtrip_file_delegates_to_com():
    fake = make_fake_element("RoundTrip")
    inner = make_fake_element("X", getName="y")
    fake.roundtripFile.return_value = make_fake_collection([inner])
    obj = RPRoundTrip(fake)
    result = obj.roundtripFile("x", 1)
    fake.roundtripFile.assert_called_once_with("x", 1)
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchManager_create_search_query_delegates_to_com():
    fake = make_fake_element("SearchManager")
    inner = make_fake_element("X", getName="y")
    fake.createSearchQuery.return_value = inner
    obj = RPSearchManager(fake)
    result = obj.createSearchQuery()
    fake.createSearchQuery.assert_called_once_with()
    assert isinstance(result, RPSearchQuery)


def test_RPSearchManager_search_delegates_to_com():
    fake = make_fake_element("SearchManager")
    target = make_fake_element("X")
    inner = make_fake_element("X", getName="y")
    fake.search.return_value = make_fake_collection([inner])
    obj = RPSearchManager(fake)
    result = obj.search(AbstractRPModelElement.wrap(target))
    fake.search.assert_called_once_with(target)
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchManager_search_and_show_results_delegates_to_com():
    fake = make_fake_element("SearchManager")
    target = make_fake_element("X")
    obj = RPSearchManager(fake)
    obj.searchAndShowResults(AbstractRPModelElement.wrap(target))
    fake.searchAndShowResults.assert_called_once_with(target)


def test_RPSearchManager_search_async_delegates_to_com():
    fake = make_fake_element("SearchManager")
    target = make_fake_element("X")
    obj = RPSearchManager(fake)
    obj.searchAsync(AbstractRPModelElement.wrap(target))
    fake.searchAsync.assert_called_once_with(target)


def test_RPSearchQuery_add_diagram_to_views_list_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.addDiagramToViewsList.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.addDiagramToViewsList(AbstractRPModelElement.wrap(target))
    fake.addDiagramToViewsList.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_add_filter_element_type_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.addFilterElementType("x")
    fake.addFilterElementType.assert_called_once_with("x")


def test_RPSearchQuery_add_filter_search_in_field_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.addFilterSearchInField("x")
    fake.addFilterSearchInField.assert_called_once_with("x")


def test_RPSearchQuery_add_filter_stereotype_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.addFilterStereotype(AbstractRPModelElement.wrap(target))
    fake.addFilterStereotype.assert_called_once_with(target)


def test_RPSearchQuery_add_filter_sub_query_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.addFilterSubQuery(AbstractRPModelElement.wrap(target), 1)
    fake.addFilterSubQuery.assert_called_once_with(target, 1)


def test_RPSearchQuery_add_matrix_to_views_list_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.addMatrixToViewsList.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.addMatrixToViewsList(AbstractRPModelElement.wrap(target))
    fake.addMatrixToViewsList.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_add_search_scope_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.addSearchScope(AbstractRPModelElement.wrap(target))
    fake.addSearchScope.assert_called_once_with(target)


def test_RPSearchQuery_add_table_to_views_list_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.addTableToViewsList.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.addTableToViewsList(AbstractRPModelElement.wrap(target))
    fake.addTableToViewsList.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_get_filter_element_types_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getFilterElementTypes.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.getFilterElementTypes()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_filter_reference_include_referenced_elements_in_search_results_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceIncludeReferencedElementsInSearchResults.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getFilterReferenceIncludeReferencedElementsInSearchResults() == 1


def test_RPSearchQuery_get_filter_reference_name_of_referenced_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceNameOfReferencedElements.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterReferenceNameOfReferencedElements() == "value"


def test_RPSearchQuery_get_filter_reference_number_of_references_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceNumberOfReferences.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getFilterReferenceNumberOfReferences() == 1


def test_RPSearchQuery_get_filter_reference_quantity_operator_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceQuantityOperator.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterReferenceQuantityOperator() == "value"


def test_RPSearchQuery_get_filter_reference_relation_kind_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceRelationKind.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterReferenceRelationKind() == "value"


def test_RPSearchQuery_get_filter_reference_stereotype_of_referenced_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceStereotypeOfReferencedElements.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterReferenceStereotypeOfReferencedElements() == "value"


def test_RPSearchQuery_get_filter_reference_type_of_referenced_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceTypeOfReferencedElements.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterReferenceTypeOfReferencedElements() == "value"


def test_RPSearchQuery_get_filter_search_in_fields_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getFilterSearchInFields.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.getFilterSearchInFields()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_filter_stereotypes_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getFilterStereotypes.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.getFilterStereotypes()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_filter_sub_queries_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getFilterSubQueries.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.getFilterSubQueries()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_filter_sub_query_use_with_not_operator_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.getFilterSubQueryUseWithNotOperator.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getFilterSubQueryUseWithNotOperator(AbstractRPModelElement.wrap(target)) == 1


def test_RPSearchQuery_get_filter_tag_find_as_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagFindAs.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterTagFindAs() == "value"


def test_RPSearchQuery_get_filter_tag_match_case_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagMatchCase.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getFilterTagMatchCase() == 1


def test_RPSearchQuery_get_filter_tag_match_whole_word_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagMatchWholeWord.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getFilterTagMatchWholeWord() == 1


def test_RPSearchQuery_get_filter_tag_name_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagName.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterTagName() == "value"


def test_RPSearchQuery_get_filter_tag_value_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagValue.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterTagValue() == "value"


def test_RPSearchQuery_get_search_scope_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getSearchScopeElements.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.getSearchScopeElements()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_view_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getView.return_value = inner
    obj = RPSearchQuery(fake)
    result = obj.getView(0)
    fake.getView.assert_called_once_with(0)
    assert result.getName() == "y"


def test_RPSearchQuery_get_view_count_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getViewCount.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getViewCount() == 1


def test_RPSearchQuery_load_from_query_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.loadFromQuery(AbstractRPModelElement.wrap(target))
    fake.loadFromQuery.assert_called_once_with(target)


def test_RPSearchQuery_remove_filter_element_types_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.removeFilterElementTypes()
    fake.removeFilterElementTypes.assert_called_once_with()


def test_RPSearchQuery_remove_filter_references_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.removeFilterReferences()
    fake.removeFilterReferences.assert_called_once_with()


def test_RPSearchQuery_remove_filter_search_in_fields_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.removeFilterSearchInFields()
    fake.removeFilterSearchInFields.assert_called_once_with()


def test_RPSearchQuery_remove_filter_stereotypes_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.removeFilterStereotypes()
    fake.removeFilterStereotypes.assert_called_once_with()


def test_RPSearchQuery_remove_filter_sub_queries_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.removeFilterSubQueries()
    fake.removeFilterSubQueries.assert_called_once_with()


def test_RPSearchQuery_remove_filter_sub_query_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.removeFilterSubQuery.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.removeFilterSubQuery(AbstractRPModelElement.wrap(target))
    fake.removeFilterSubQuery.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_remove_filter_tag_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.removeFilterTag()
    fake.removeFilterTag.assert_called_once_with()


def test_RPSearchQuery_remove_search_scope_element_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.removeSearchScopeElement.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.removeSearchScopeElement(AbstractRPModelElement.wrap(target))
    fake.removeSearchScopeElement.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_remove_view_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.removeView(1)
    fake.removeView.assert_called_once_with(1)


def test_RPSearchQuery_reset_search_scope_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.resetSearchScope()
    fake.resetSearchScope.assert_called_once_with()


def test_RPSearchQuery_save_as_query_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    inner = make_fake_element("X", getName="y")
    fake.saveAsQuery.return_value = inner
    obj = RPSearchQuery(fake)
    result = obj.saveAsQuery(AbstractRPModelElement.wrap(target))
    fake.saveAsQuery.assert_called_once_with(target)
    assert isinstance(result, RPTableLayout)


def test_RPSearchQuery_set_filter_tag_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setFilterTag("name", "value", 1, 1, "findAs")
    fake.setFilterTag.assert_called_once_with("name", "value", 1, 1, "findAs")


def test_RPSearchQuery_get_filter_sub_queries_operator_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterSubQueriesOperator.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterSubQueriesOperator() == "value"


def test_RPSearchQuery_get_filter_tag_local_only_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagLocalOnly.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getFilterTagLocalOnly() == 1


def test_RPSearchQuery_get_filter_units_only_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterUnitsOnly.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getFilterUnitsOnly() == 1


def test_RPSearchQuery_get_filter_unresolved_kind_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterUnresolvedKind.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getFilterUnresolvedKind() == "value"


def test_RPSearchQuery_get_include_descendants_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getIncludeDescendants.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getIncludeDescendants() == 1


def test_RPSearchQuery_get_match_case_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getMatchCase.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getMatchCase() == 1


def test_RPSearchQuery_get_match_specified_criteria_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getMatchSpecifiedCriteria.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getMatchSpecifiedCriteria() == 1


def test_RPSearchQuery_get_match_whole_word_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getMatchWholeWord.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getMatchWholeWord() == 1


def test_RPSearchQuery_get_search_find_as_option_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getSearchFindAsOption.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getSearchFindAsOption() == "value"


def test_RPSearchQuery_get_search_scope_object_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getSearchScopeObject.return_value = inner
    obj = RPSearchQuery(fake)
    result = obj.getSearchScopeObject()
    assert result.getName() == "y"


def test_RPSearchQuery_get_search_text_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getSearchText.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getSearchText() == "value"


def test_RPSearchQuery_get_view_include_model_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getViewIncludeModelElements.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.getViewIncludeModelElements() == 1


def test_RPSearchQuery_get_views_to_search_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getViewsToSearch.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.getViewsToSearch() == "value"


def test_RPSearchQuery_set_filter_sub_queries_operator_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setFilterSubQueriesOperator("file.txt")
    fake.setFilterSubQueriesOperator.assert_called_once_with("file.txt")


def test_RPSearchQuery_set_filter_tag_local_only_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setFilterTagLocalOnly(1)
    fake.setFilterTagLocalOnly.assert_called_once_with(1)


def test_RPSearchQuery_set_filter_units_only_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setFilterUnitsOnly(1)
    fake.setFilterUnitsOnly.assert_called_once_with(1)


def test_RPSearchQuery_set_filter_unresolved_kind_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setFilterUnresolvedKind("file.txt")
    fake.setFilterUnresolvedKind.assert_called_once_with("file.txt")


def test_RPSearchQuery_set_include_descendants_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setIncludeDescendants(1)
    fake.setIncludeDescendants.assert_called_once_with(1)


def test_RPSearchQuery_set_match_case_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setMatchCase(1)
    fake.setMatchCase.assert_called_once_with(1)


def test_RPSearchQuery_set_match_specified_criteria_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setMatchSpecifiedCriteria(1)
    fake.setMatchSpecifiedCriteria.assert_called_once_with(1)


def test_RPSearchQuery_set_match_whole_word_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setMatchWholeWord(1)
    fake.setMatchWholeWord.assert_called_once_with(1)


def test_RPSearchQuery_set_search_find_as_option_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setSearchFindAsOption("file.txt")
    fake.setSearchFindAsOption.assert_called_once_with("file.txt")


def test_RPSearchQuery_set_search_scope_object_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.setSearchScopeObject(AbstractRPModelElement.wrap(target))
    fake.setSearchScopeObject.assert_called_once_with(target)


def test_RPSearchQuery_set_search_text_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setSearchText("file.txt")
    fake.setSearchText.assert_called_once_with("file.txt")


def test_RPSearchQuery_set_view_include_model_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setViewIncludeModelElements(1)
    fake.setViewIncludeModelElements.assert_called_once_with(1)


def test_RPSearchQuery_set_views_to_search_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.setViewsToSearch("file.txt")
    fake.setViewsToSearch.assert_called_once_with("file.txt")


def test_RPSearchResult_get_matched_field_delegates_to_com():
    fake = make_fake_element("SearchResult")
    fake.getMatchedField.return_value = "value"
    obj = RPSearchResult(fake)
    assert obj.getMatchedField() == "value"


def test_RPSearchResult_get_matched_fields_delegates_to_com():
    fake = make_fake_element("SearchResult")
    inner = make_fake_element("X", getName="y")
    fake.getMatchedFields.return_value = make_fake_collection([inner])
    obj = RPSearchResult(fake)
    result = obj.getMatchedFields()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchResult_get_matched_object_delegates_to_com():
    fake = make_fake_element("SearchResult")
    inner = make_fake_element("X", getName="y")
    fake.getMatchedObject.return_value = inner
    obj = RPSearchResult(fake)
    result = obj.getMatchedObject()
    assert result.getName() == "y"


def test_RPSearchResult_get_name_delegates_to_com():
    fake = make_fake_element("SearchResult")
    fake.getName.return_value = "value"
    obj = RPSearchResult(fake)
    assert obj.getName() == "value"


def test_RPCodeGenSimplifiersRegistry_notify_simplification_done_delegates_to_com():
    fake = make_fake_element("CodeGenSimplifiersRegistry")
    obj = RPCodeGenSimplifiersRegistry(fake)
    obj.notifySimplificationDone()
    fake.notifySimplificationDone.assert_called_once_with()


def test_RPExternalCodeGeneratorInvoker_notify_generation_done_delegates_to_com():
    fake = make_fake_element("ExternalCodeGeneratorInvoker")
    obj = RPExternalCodeGeneratorInvoker(fake)
    obj.notifyGenerationDone()
    fake.notifyGenerationDone.assert_called_once_with()
