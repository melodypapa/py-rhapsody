"""Wraps ``com.telelogic.rhapsody.core.IRPPackage``."""

from typing import TYPE_CHECKING, Any, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.activity.model_activity import RPFlow, RPFlowItem
    from rhapsody_cli.models.elements.classifiers.model_actor import RPActor
    from rhapsody_cli.models.elements.classifiers.model_class import RPClass
    from rhapsody_cli.models.elements.classifiers.model_operation import RPOperation
    from rhapsody_cli.models.elements.classifiers.model_usecase import RPUseCase
    from rhapsody_cli.models.elements.common.model_other_model import RPSysMLPort
    from rhapsody_cli.models.elements.diagrams import (
        RPActivityDiagram,
        RPCollaborationDiagram,
        RPComponentDiagram,
        RPDeploymentDiagram,
        RPObjectModelDiagram,
        RPSequenceDiagram,
        RPStatechartDiagram,
        RPTimingDiagram,
        RPUseCaseDiagram,
    )
    from rhapsody_cli.models.elements.graphics.model_graphics import RPLink
    from rhapsody_cli.models.elements.relations.model_instance import RPInstance
    from rhapsody_cli.models.elements.relations.model_relation import RPRelation


class RPPackage(RPUnit):
    """Wraps ``IRPPackage``: represents a package that contains model elements."""

    # IRPPackage method parity checklist:
    # [x] add_activity_diagram  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_actor  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_class  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] add_collaboration_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_component_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_deployment_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_event  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] add_flow_items  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_flows  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_global_function  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] add_global_object  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_global_variable  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] add_implicit_object  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] add_instance_specification  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_link  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] add_link_between_sysml_ports  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] add_module  [x] impl  [x] docstring  [ ] unit test  [x] integration test
    # [x] add_nested_package  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [ ] add_node  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_object_model_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_panel_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] add_sequence_diagram  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] add_statechart  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_timing_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] add_use_case  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [ ] add_use_case_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_actor  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] delete_class  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] delete_collaboration_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_component_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_deployment_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_event  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] delete_flow_items  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] delete_flows  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] delete_global_function  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_global_object  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_global_variable  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_node  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_object_model_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] delete_package  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] delete_panel_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_sequence_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_timing_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_use_case  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_use_case_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_actor  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_all_by_name  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] find_class  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] find_event  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_global_function  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_global_object  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_global_variable  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_node  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_usage  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_use_case  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_actors  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_all_nested_elements  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_behavioral_diagrams  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_classes  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [ ] get_collaboration_diagrams  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_component_diagrams  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_deployment_diagrams  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_events  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_events_base_id  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_flow_items  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_flows  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_global_functions  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_global_objects  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_global_variables  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_instance_specifications  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_links  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_modules  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_namespace  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_nested_classifiers  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_nested_components  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_nodes  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_object_model_diagrams  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_packages  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [ ] get_panel_diagrams  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_remote_requirements_populate_mode  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_root_instance_specifications  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_saved_in_seperate_directory  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_sequence_diagrams  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_source_artifacts  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_timing_diagrams  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_types  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_use_case_diagrams  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_use_cases  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_user_defined_stereotypes  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] login_to_remote_artifact_server  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] populate_remote_requirements  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] re_calculate_events_base_id  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_remote_requirements_populate_mode  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_saved_in_seperate_directory  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] update_contained_diagrams_on_server  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] update_contained_matrices_on_server  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] update_contained_tables_on_server  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_unit / irp_model_element methods (covered by rp_unit / rp_model_element checklists)
    # No deprecated IRPPackage methods.

    def add_class(self, name: str) -> "RPClass":
        """Adds a new class to the package.

        Args:
            name: The name of the new class.

        Returns:
            The wrapped ``IRPClass`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addClass(java.lang.String name)
        """
        return cast("RPClass", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addClass(name))))

    def add_nested_package(self, name: str) -> "RPPackage":
        """Adds a nested package to this package.

        Args:
            name: The name of the new nested package.

        Returns:
            The wrapped ``IRPPackage`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addNestedPackage(java.lang.String name)
        """
        return cast("RPPackage", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNestedPackage(name))))

    def add_actor(self, name: str) -> "RPActor":
        """Adds a new actor to the package.

        Args:
            name: The name of the new actor.

        Returns:
            The wrapped ``IRPActor`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addActor(java.lang.String name)
        """
        return cast("RPActor", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addActor(name))))

    def add_global_function(self, name: str) -> "RPOperation":
        """Adds a new global function to the package.

        Args:
            name: The name of the new global function.

        Returns:
            The wrapped function element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addGlobalFunction(java.lang.String name)
        """
        return cast("RPOperation", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addGlobalFunction(name))))

    def add_flow_items(self, name: str) -> "RPFlowItem":
        """Adds a new flow item to the package.

        Args:
            name: The name of the new flow item.

        Returns:
            The wrapped flow item element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addFlowItems(java.lang.String name)
        """
        return cast("RPFlowItem", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addFlowItems(name))))

    def add_flows(self, name: str) -> "RPFlow":
        """Adds a new flow to the package.

        Args:
            name: The name of the new flow.

        Returns:
            The wrapped flow element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addFlows(java.lang.String name)
        """
        return cast("RPFlow", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addFlows(name))))

    def get_nested_packages(self) -> "RPCollection":
        """Returns all nested packages in this package.

        Returns:
            An ``RPCollection`` of ``IRPPackage`` objects.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getPackages", "packages"))

    def get_classes(self) -> "RPCollection":
        """Returns all classes contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPClass`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getClasses()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getClasses", "classes"))

    def get_actors(self) -> "RPCollection":
        """Returns all actors contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPActor`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getActors()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getActors", "actors"))

    def get_use_cases(self) -> "RPCollection":
        """Returns all use cases contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPUseCase`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getUseCases()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getUseCases", "useCases"))

    def add_use_case(self, name: str) -> "RPUseCase":
        """Adds a new use case to the package.

        Args:
            name: The name of the new use case.

        Returns:
            The wrapped ``IRPUseCase`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addUseCase(java.lang.String name)
        """
        return cast("RPUseCase", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addUseCase(name))))

    def add_exception(self, name: str) -> Any:
        """Adds a new exception to the package.

        Args:
            name: The name of the new exception.

        Returns:
            The wrapped exception element created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addException(name)))

    # --- Diagram adders (Pattern E) ---
    def add_activity_diagram(self, name: str) -> "RPActivityDiagram":
        """Adds a new activity diagram to the package.

        Args:
            name: The name of the new activity diagram.

        Returns:
            The wrapped ``IRPActivityDiagram`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addActivityDiagram(java.lang.String name)
        """
        return cast("RPActivityDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addActivityDiagram(name))))

    def add_sequence_diagram(self, name: str) -> "RPSequenceDiagram":
        """Adds a new sequence diagram to the package.

        Args:
            name: The name of the new sequence diagram.

        Returns:
            The wrapped ``IRPSequenceDiagram`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addSequenceDiagram(java.lang.String name)
        """
        return cast("RPSequenceDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addSequenceDiagram(name))))

    def add_use_case_diagram(self, name: str) -> "RPUseCaseDiagram":
        """Adds a new use case diagram to the package.

        Args:
            name: The name of the new use case diagram.

        Returns:
            The wrapped ``IRPUseCaseDiagram`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addUseCaseDiagram(java.lang.String name)
        """
        return cast("RPUseCaseDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addUseCaseDiagram(name))))

    def add_collaboration_diagram(self, name: str) -> "RPCollaborationDiagram":
        """Adds a new collaboration diagram to the package.

        Args:
            name: The name of the new collaboration diagram.

        Returns:
            The wrapped ``IRPCollaborationDiagram`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addCollaborationDiagram(java.lang.String name)
        """
        return cast("RPCollaborationDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addCollaborationDiagram(name))))

    def add_component_diagram(self, name: str) -> "RPComponentDiagram":
        """Adds a new component diagram to the package.

        Args:
            name: The name of the new component diagram.

        Returns:
            The wrapped ``IRPComponentDiagram`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addComponentDiagram(java.lang.String name)
        """
        return cast("RPComponentDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addComponentDiagram(name))))

    def add_deployment_diagram(self, name: str) -> "RPDeploymentDiagram":
        """Adds a new deployment diagram to the package.

        Args:
            name: The name of the new deployment diagram.

        Returns:
            The wrapped ``IRPDeploymentDiagram`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addDeploymentDiagram(java.lang.String name)
        """
        return cast("RPDeploymentDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addDeploymentDiagram(name))))

    def add_object_model_diagram(self, name: str) -> "RPObjectModelDiagram":
        """Adds a new object model diagram to the package.

        Args:
            name: The name of the new object model diagram.

        Returns:
            The wrapped ``IRPObjectModelDiagram`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addObjectModelDiagram(java.lang.String name)
        """
        return cast("RPObjectModelDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addObjectModelDiagram(name))))

    def add_statechart_diagram(self, name: str) -> "RPStatechartDiagram":
        """Adds a new statechart diagram to the package.

        Args:
            name: The name of the new statechart diagram.

        Returns:
            The wrapped ``IRPStatechartDiagram`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addStatechart(java.lang.String name)
        """
        return cast("RPStatechartDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addStatechart(name))))

    def add_timing_diagram(self, name: str) -> "RPTimingDiagram":
        """Adds a new timing diagram to the package.

        Args:
            name: The name of the new timing diagram.

        Returns:
            The wrapped ``IRPTimingDiagram`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addTimingDiagram(java.lang.String name)
        """
        return cast("RPTimingDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addTimingDiagram(name))))

    def add_panel_diagram(self, name: str) -> Any:
        """Adds a new panel diagram to the package.

        Args:
            name: The name of the new panel diagram.

        Returns:
            The wrapped panel diagram element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addPanelDiagram(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addPanelDiagram(name)))

    # --- Diagram getters (Pattern C) ---
    def get_activity_diagrams(self) -> "RPCollection":
        """Returns all activity diagrams contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPActivityDiagram`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getActivityDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getActivityDiagrams", "activityDiagrams"))

    def get_sequence_diagrams(self) -> "RPCollection":
        """Returns all sequence diagrams contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPSequenceDiagram`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getSequenceDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getSequenceDiagrams", "sequenceDiagrams"))

    def get_use_case_diagrams(self) -> "RPCollection":
        """Returns all use case diagrams contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPUseCaseDiagram`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getUseCaseDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getUseCaseDiagrams", "useCaseDiagrams"))

    def get_collaboration_diagrams(self) -> "RPCollection":
        """Returns all collaboration diagrams contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPCollaborationDiagram`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getCollaborationDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getCollaborationDiagrams", "collaborationDiagrams"))

    def get_component_diagrams(self) -> "RPCollection":
        """Returns all component diagrams contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPComponentDiagram`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getComponentDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getComponentDiagrams", "componentDiagrams"))

    def get_deployment_diagrams(self) -> "RPCollection":
        """Returns all deployment diagrams contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPDeploymentDiagram`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getDeploymentDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getDeploymentDiagrams", "deploymentDiagrams"))

    def get_object_model_diagrams(self) -> "RPCollection":
        """Returns all object model diagrams contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPObjectModelDiagram`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getObjectModelDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getObjectModelDiagrams", "objectModelDiagrams"))

    def get_timing_diagrams(self) -> "RPCollection":
        """Returns all timing diagrams contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPTimingDiagram`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getTimingDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getTimingDiagrams", "timingDiagrams"))

    def get_panel_diagrams(self) -> "RPCollection":
        """Returns all panel diagrams contained in this package.

        Returns:
            An ``RPCollection`` of panel diagram elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getPanelDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getPanelDiagrams", "panelDiagrams"))

    # --- Diagram deleters (Pattern F) ---
    def delete_activity_diagram(self, diagram: Any) -> None:
        """Deletes an activity diagram from the package.

        Args:
            diagram: The activity diagram to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteActivityDiagram(com.telelogic.rhapsody.core.IRPActivityDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteActivityDiagram(diagram._com))

    def delete_sequence_diagram(self, diagram: Any) -> None:
        """Deletes a sequence diagram from the package.

        Args:
            diagram: The sequence diagram to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteSequenceDiagram(com.telelogic.rhapsody.core.IRPSequenceDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteSequenceDiagram(diagram._com))

    def delete_use_case_diagram(self, diagram: Any) -> None:
        """Deletes a use case diagram from the package.

        Args:
            diagram: The use case diagram to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteUseCaseDiagram(com.telelogic.rhapsody.core.IRPUseCaseDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteUseCaseDiagram(diagram._com))

    def delete_collaboration_diagram(self, diagram: Any) -> None:
        """Deletes a collaboration diagram from the package.

        Args:
            diagram: The collaboration diagram to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteCollaborationDiagram(com.telelogic.rhapsody.core.IRPCollaborationDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteCollaborationDiagram(diagram._com))

    def delete_component_diagram(self, diagram: Any) -> None:
        """Deletes a component diagram from the package.

        Args:
            diagram: The component diagram to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteComponentDiagram(com.telelogic.rhapsody.core.IRPComponentDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteComponentDiagram(diagram._com))

    def delete_deployment_diagram(self, diagram: Any) -> None:
        """Deletes a deployment diagram from the package.

        Args:
            diagram: The deployment diagram to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteDeploymentDiagram(com.telelogic.rhapsody.core.IRPDeploymentDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteDeploymentDiagram(diagram._com))

    def delete_object_model_diagram(self, diagram: Any) -> None:
        """Deletes an object model diagram from the package.

        Args:
            diagram: The object model diagram to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteObjectModelDiagram(com.telelogic.rhapsody.core.IRPObjectModelDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteObjectModelDiagram(diagram._com))

    def delete_timing_diagram(self, diagram: Any) -> None:
        """Deletes a timing diagram from the package.

        Args:
            diagram: The timing diagram to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteTimingDiagram(com.telelogic.rhapsody.core.IRPTimingDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteTimingDiagram(diagram._com))

    def delete_panel_diagram(self, diagram: Any) -> None:
        """Deletes a panel diagram from the package.

        Args:
            diagram: The panel diagram to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deletePanelDiagram(com.telelogic.rhapsody.core.IRPPanelDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deletePanelDiagram(diagram._com))

    # --- Classifier deleters (Pattern F) ---
    def delete_class(self, cls: Any) -> None:
        """Deletes a class from the package.

        Args:
            cls: The class to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteClass(com.telelogic.rhapsody.core.IRPClass cls)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteClass(cls._com))

    def delete_actor(self, actor: Any) -> None:
        """Deletes an actor from the package.

        Args:
            actor: The actor to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteActor(com.telelogic.rhapsody.core.IRPActor actor)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteActor(actor._com))

    def delete_use_case(self, use_case: Any) -> None:
        """Deletes a use case from the package.

        Args:
            use_case: The use case to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteUseCase(com.telelogic.rhapsody.core.IRPUseCase useCase)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteUseCase(use_case._com))

    def delete_flow_items(self, flow_item: "RPFlowItem") -> None:
        """Deletes a flow item from the package.

        Args:
            flow_item: The flow item to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteFlowItems(com.telelogic.rhapsody.core.IRPFlowItem flowItem)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteFlowItems(flow_item._com))

    def delete_flows(self, flow: "RPFlow") -> None:
        """Deletes a flow from the package.

        Args:
            flow: The flow to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteFlows(com.telelogic.rhapsody.core.IRPFlow flow)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteFlows(flow._com))

    def delete_package(self, package: Any) -> None:
        """Deletes a nested package from this package.

        Args:
            package: The package to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deletePackage(com.telelogic.rhapsody.core.IRPPackage package)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deletePackage(package._com))

    # --- Finders (Pattern B) ---
    def find_class(self, name: str) -> "RPClass":
        """Finds a class in the package by name.

        Args:
            name: The name of the class to find.

        Returns:
            The wrapped ``IRPClass`` if found, otherwise empty wrapper.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findClass(java.lang.String name)
        """
        return cast("RPClass", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findClass(name))))

    def find_actor(self, name: str) -> "RPActor":
        """Finds an actor in the package by name.

        Args:
            name: The name of the actor to find.

        Returns:
            The wrapped ``IRPActor`` if found, otherwise empty wrapper.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findActor(java.lang.String name)
        """
        return cast("RPActor", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findActor(name))))

    def find_use_case(self, name: str) -> "RPUseCase":
        """Finds a use case in the package by name.

        Args:
            name: The name of the use case to find.

        Returns:
            The wrapped ``IRPUseCase`` if found, otherwise empty wrapper.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findUseCase(java.lang.String name)
        """
        return cast("RPUseCase", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findUseCase(name))))

    def find_nested_package(self, name: str) -> "RPPackage":
        """Finds a nested package by name.

        Args:
            name: The name of the nested package to find.

        Returns:
            The wrapped ``IRPPackage`` if found, otherwise empty wrapper.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findNestedPackage(java.lang.String name)
        """
        return cast("RPPackage", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findNestedPackage(name))))

    # --- Association methods ---
    def add_association(self, name: str) -> "RPRelation":
        """Adds a new association to the package.

        Args:
            name: The name of the new association.

        Returns:
            The wrapped ``IRPRelation`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addAssociation(java.lang.String name)
        """
        return cast("RPRelation", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addAssociation(name))))

    def get_associations(self) -> "RPCollection":
        """Returns all associations contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPRelation`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getAssociations()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAssociations", "associations"))

    def delete_association(self, association: Any) -> None:
        """Deletes an association from the package.

        Args:
            association: The association to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteAssociation(com.telelogic.rhapsody.core.IRPRelation association)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteAssociation(association._com))

    # --- Event methods ---
    def add_event(self, name: str) -> Any:
        """Adds a new event to the package.

        Args:
            name: The name of the new event.

        Returns:
            The wrapped event element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addEvent(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addEvent(name)))

    def get_events(self) -> "RPCollection":
        """Returns all events contained in this package.

        Returns:
            An ``RPCollection`` of event elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getEvents()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getEvents", "events"))

    def get_flow_items(self) -> "RPCollection":
        """Returns all flow items contained in this package.

        Returns:
            An ``RPCollection`` of flow item elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getFlowItems()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getFlowItems", "flowItems"))

    def get_flows(self) -> "RPCollection":
        """Returns all flows contained in this package.

        Returns:
            An ``RPCollection`` of flow elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getFlows()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getFlows", "flows"))

    def find_event(self, name: str) -> Any:
        """Finds an event in the package by name.

        Args:
            name: The name of the event to find.

        Returns:
            The wrapped event element if found.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findEvent(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findEvent(name)))

    def delete_event(self, event: Any) -> None:
        """Deletes an event from the package.

        Args:
            event: The event to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteEvent(com.telelogic.rhapsody.core.IRPEvent event)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteEvent(event._com))

    # --- Node methods ---
    def add_node(self, name: str) -> Any:
        """Adds a new node to the package.

        Args:
            name: The name of the new node.

        Returns:
            The wrapped node element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addNode(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNode(name)))

    def get_nodes(self) -> "RPCollection":
        """Returns all nodes contained in this package.

        Returns:
            An ``RPCollection`` of node elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getNodes()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNodes", "nodes"))

    def find_node(self, name: str) -> Any:
        """Finds a node in the package by name.

        Args:
            name: The name of the node to find.

        Returns:
            The wrapped node element if found.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findNode(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findNode(name)))

    def delete_node(self, node: Any) -> None:
        """Deletes a node from the package.

        Args:
            node: The node to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteNode(com.telelogic.rhapsody.core.IRPNode node)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteNode(node._com))

    # --- Module methods ---
    def add_module(self, name: str) -> Any:
        """Adds a new module to the package.

        Args:
            name: The name of the new module.

        Returns:
            The wrapped module element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addModule(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addModule(name)))

    def get_modules(self) -> "RPCollection":
        """Returns all modules contained in this package.

        Returns:
            An ``RPCollection`` of module elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getModules()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getModules", "modules"))

    # --- Type methods ---
    def add_type(self, name: str) -> Any:
        """Adds a new type to the package.

        Args:
            name: The name of the new type.

        Returns:
            The wrapped type element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addType(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addType(name)))

    def get_types(self) -> "RPCollection":
        """Returns all types contained in this package.

        Returns:
            An ``RPCollection`` of type elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getTypes()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getTypes", "types"))

    def find_type(self, name: str) -> Any:
        """Finds a type in the package by name.

        Args:
            name: The name of the type to find.

        Returns:
            The wrapped type element if found.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findType(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findType(name)))

    def delete_type(self, type_elem: Any) -> None:
        """Deletes a type from the package.

        Args:
            type_elem: The type to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteType(com.telelogic.rhapsody.core.IRPType type)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteType(type_elem._com))

    # --- Global function methods ---
    def find_global_function(self, name: str) -> "RPOperation":
        """Finds a global function in the package by name.

        Args:
            name: The name of the global function to find.

        Returns:
            The wrapped operation element if found.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findGlobalFunction(java.lang.String name)
        """
        return cast("RPOperation", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findGlobalFunction(name))))

    def get_global_functions(self) -> "RPCollection":
        """Returns all global functions contained in this package.

        Returns:
            An ``RPCollection`` of operation elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getGlobalFunctions()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getGlobalFunctions", "globalFunctions"))

    def delete_global_function(self, func: Any) -> None:
        """Deletes a global function from the package.

        Args:
            func: The global function to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteGlobalFunction(com.telelogic.rhapsody.core.IRPOperation func)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteGlobalFunction(func._com))

    # --- Global object methods ---
    def add_global_object(self, name: str) -> Any:
        """Adds a new global object to the package.

        Args:
            name: The name of the new global object.

        Returns:
            The wrapped global object element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addGlobalObject(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addGlobalObject(name)))

    def get_global_objects(self) -> "RPCollection":
        """Returns all global objects contained in this package.

        Returns:
            An ``RPCollection`` of global object elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getGlobalObjects()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getGlobalObjects", "globalObjects"))

    def find_global_object(self, name: str) -> Any:
        """Finds a global object in the package by name.

        Args:
            name: The name of the global object to find.

        Returns:
            The wrapped global object element if found.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findGlobalObject(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findGlobalObject(name)))

    def delete_global_object(self, obj: Any) -> None:
        """Deletes a global object from the package.

        Args:
            obj: The global object to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteGlobalObject(com.telelogic.rhapsody.core.IRPGlobalObject obj)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteGlobalObject(obj._com))

    # --- Global variable methods ---
    def add_global_variable(self, name: str) -> Any:
        """Adds a new global variable to the package.

        Args:
            name: The name of the new global variable.

        Returns:
            The wrapped global variable element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addGlobalVariable(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addGlobalVariable(name)))

    def get_global_variables(self) -> "RPCollection":
        """Returns all global variables contained in this package.

        Returns:
            An ``RPCollection`` of global variable elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getGlobalVariables()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getGlobalVariables", "globalVariables"))

    def find_global_variable(self, name: str) -> Any:
        """Finds a global variable in the package by name.

        Args:
            name: The name of the global variable to find.

        Returns:
            The wrapped global variable element if found.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findGlobalVariable(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findGlobalVariable(name)))

    def delete_global_variable(self, var: Any) -> None:
        """Deletes a global variable from the package.

        Args:
            var: The global variable to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::deleteGlobalVariable(com.telelogic.rhapsody.core.IRPVariable var)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteGlobalVariable(var._com))

    # --- Nested classifier methods ---
    def get_nested_classifiers(self) -> "RPCollection":
        """Returns all nested classifiers in this package.

        Returns:
            An ``RPCollection`` of classifier elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getNestedClassifiers()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNestedClassifiers", "nestedClassifiers"))

    def get_nested_components(self) -> "RPCollection":
        """Returns all nested components in this package.

        Returns:
            An ``RPCollection`` of component elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getNestedComponents()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNestedComponents", "nestedComponents"))

    # --- Instance specification methods ---
    def add_instance_specification(self, name: str) -> Any:
        """Adds a new instance specification to the package.

        Args:
            name: The name of the new instance specification.

        Returns:
            The wrapped instance specification element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addInstanceSpecification(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addInstanceSpecification(name)))

    def get_instance_specifications(self) -> "RPCollection":
        """Returns all instance specifications contained in this package.

        Returns:
            An ``RPCollection`` of instance specification elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getInstanceSpecifications()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getInstanceSpecifications", "instanceSpecifications"))

    # --- Link methods ---
    def add_link(self, name: str) -> Any:
        """Adds a new link to the package.

        Args:
            name: The name of the new link.

        Returns:
            The wrapped link element created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addLink(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addLink(name)))

    def get_links(self) -> "RPCollection":
        """Returns all links contained in this package.

        Returns:
            An ``RPCollection`` of link elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getLinks()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getLinks", "links"))

    # --- Find all by name ---
    def find_all_by_name(self, name: str) -> "RPCollection":
        """Finds all elements with the given name in this package.

        Args:
            name: The name to search for.

        Returns:
            An ``RPCollection`` of matching elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findAllByName(java.lang.String name)
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.findAllByName(name)))

    # --- Behavioral diagrams ---
    def get_behavioral_diagrams(self) -> "RPCollection":
        """Returns all behavioral diagrams contained in this package.

        Returns:
            An ``RPCollection`` of behavioral diagram elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getBehavioralDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getBehavioralDiagrams", "behavioralDiagrams"))

    # --- Source artifacts ---
    def get_source_artifacts(self) -> "RPCollection":
        """Returns all source artifacts contained in this package.

        Returns:
            An ``RPCollection`` of source artifact elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getSourceArtifacts()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getSourceArtifacts", "sourceArtifacts"))

    # --- Find usage ---
    def find_usage(self, element: Any) -> "RPCollection":
        """Finds all usages of an element in this package.

        Args:
            element: The element to find usages for.

        Returns:
            An ``RPCollection`` of elements that use the given element.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::findUsage(com.telelogic.rhapsody.core.IRPModelElement element)
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.findUsage(element._com)))

    # --- Remote Requirements Methods (Task 3) ---
    def get_remote_requirements_populate_mode(self) -> int:
        """Returns the remote requirements populate mode for this package.

        Returns:
            The populate mode as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getRemoteRequirementsPopulateMode()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getRemoteRequirementsPopulateMode", "remoteRequirementsPopulateMode"))

    def get_root_instance_specifications(self) -> "RPCollection":
        """Returns all root instance specifications in this package.

        Returns:
            An ``RPCollection`` of instance specification elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getRootInstanceSpecifications()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRootInstanceSpecifications", "rootInstanceSpecifications"))

    def login_to_remote_artifact_server(self, server_url: str, username: str, password: str) -> None:
        """Logs in to the remote artifact server.

        Args:
            server_url: The URL of the remote artifact server.
            username: The username for authentication.
            password: The password for authentication.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::loginToRemoteArtifactServer(
                java.lang.String serverUrl, java.lang.String username, java.lang.String password)
        """
        AbstractRPModelElement.call_com(lambda: self._com.loginToRemoteArtifactServer(server_url, username, password))

    def populate_remote_requirements(self) -> None:
        """Populates remote requirements for this package.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::populateRemoteRequirements()
        """
        AbstractRPModelElement.call_com(lambda: self._com.populateRemoteRequirements())

    def recalculate_events_base_id(self) -> None:
        """Recalculates the events base ID for this package.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::reCalculateEventsBaseId()
        """
        AbstractRPModelElement.call_com(lambda: self._com.reCalculateEventsBaseId())

    def set_remote_requirements_populate_mode(self, mode: int) -> None:
        """Sets the remote requirements populate mode for this package.

        Args:
            mode: The populate mode to set.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::setRemoteRequirementsPopulateMode(int mode)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRemoteRequirementsPopulateMode", "remoteRequirementsPopulateMode", mode)

    def update_contained_diagrams_on_server(self) -> None:
        """Updates the contained diagrams on the server.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::updateContainedDiagramsOnServer()
        """
        AbstractRPModelElement.call_com(lambda: self._com.updateContainedDiagramsOnServer())

    # --- SysML Methods (Task 4) ---
    def add_implicit_object(self, name: str) -> "RPInstance":
        """Adds a new implicit object to the package.

        Args:
            name: The name of the new implicit object.

        Returns:
            The wrapped ``IRPInstance`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addImplicitObject(java.lang.String name)
        """
        return cast("RPInstance", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addImplicitObject(name))))

    def add_link_between_sysml_ports(self, port1: "RPSysMLPort", port2: "RPSysMLPort") -> "RPLink":
        """Adds a link between two SysML ports.

        Args:
            port1: The first SysML port.
            port2: The second SysML port.

        Returns:
            The wrapped ``IRPLink`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addLinkBetweenSYSMLPorts(
                com.telelogic.rhapsody.core.IRPSysMLPort port1, com.telelogic.rhapsody.core.IRPSysMLPort port2)
        """
        return cast("RPLink", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addLinkBetweenSYSMLPorts(port1._com, port2._com))))

    # --- Misc Methods (Task 5) ---
    def get_all_nested_elements(self) -> "RPCollection":
        """Returns all nested elements in this package.

        Returns:
            An ``RPCollection`` of nested elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getAllNestedElements()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAllNestedElements", "allNestedElements"))

    def get_events_base_id(self) -> str:
        """Returns the events base ID for this package.

        Returns:
            The events base ID as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getEventsBaseId()
        """
        return AbstractRPModelElement._get_method_or_property(self._com, "getEventsBaseId", "eventsBaseId")

    def get_namespace(self) -> str:
        """Returns the namespace for this package.

        Returns:
            The namespace as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getNamespace()
        """
        return AbstractRPModelElement._get_method_or_property(self._com, "getNamespace", "namespace")

    def get_saved_in_separate_directory(self) -> int:
        """Returns whether the package is saved in a separate directory.

        Returns:
            ``1`` if saved in separate directory, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getSavedInSeperateDirectory()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getSavedInSeperateDirectory", "savedInSeperateDirectory"))

    def get_user_defined_stereotypes(self) -> "RPCollection":
        """Returns all user-defined stereotypes in this package.

        Returns:
            An ``RPCollection`` of stereotype elements.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getUserDefinedStereotypes()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getUserDefinedStereotypes", "userDefinedStereotypes"))

    def set_saved_in_separate_directory(self, value: int) -> None:
        """Sets whether the package is saved in a separate directory.

        Args:
            value: ``1`` to save in separate directory, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::setSavedInSeperateDirectory(int value)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setSavedInSeperateDirectory", "savedInSeperateDirectory", value)

    def update_contained_matrices_on_server(self) -> None:
        """Updates the contained matrices on the server.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::updateContainedMatricesOnServer()
        """
        AbstractRPModelElement.call_com(lambda: self._com.updateContainedMatricesOnServer())

    def update_contained_tables_on_server(self) -> None:
        """Updates the contained tables on the server.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::updateContainedTablesOnServer()
        """
        AbstractRPModelElement.call_com(lambda: self._com.updateContainedTablesOnServer())


AbstractRPModelElement.register_wrapper("Package", RPPackage)
