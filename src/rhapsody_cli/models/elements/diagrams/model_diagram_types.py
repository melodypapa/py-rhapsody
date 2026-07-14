"""Diagram Types model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram

if TYPE_CHECKING:
    from rhapsody_cli.models.core import RPCollection
    from rhapsody_cli.models.elements.activity.model_activity import RPFlowchart
    from rhapsody_cli.models.elements.classifiers.model_statechart import RPStatechart
    from rhapsody_cli.models.elements.containment.model_collaboration import RPCollaboration
    from rhapsody_cli.models.elements.graphics.model_graphics import RPGraphElement, RPGraphNode


class RPCollaborationDiagram(RPDiagram):
    """Wraps ``IRPCollaborationDiagram``: represents collaboration diagrams in a Rhapsody model."""

    # IRPCollaborationDiagram method parity checklist:
    # [x] getLogicalCollaboration      [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPCollaborationDiagram methods.

    def get_logical_collaboration(self) -> "RPCollaboration":
        """Returns the collaboration object underlying the collaboration diagram.

        Returns:
            The IRPCollaboration object underlying the collaboration diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaborationDiagram::getLogicalCollaboration()
        """
        result = AbstractRPModelElement.call_com(lambda: self._com.getLogicalCollaboration())
        return cast("RPCollaboration", AbstractRPModelElement.wrap(result))


class RPComponentDiagram(RPDiagram):
    """Wraps ``IRPComponentDiagram``: represents component diagrams in Rhapsody models."""

    # IRPComponentDiagram method parity checklist:
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPComponentDiagram methods.

    pass


class RPDeploymentDiagram(RPDiagram):
    """Wraps ``IRPDeploymentDiagram``: represents deployment diagrams in Rhapsody models."""

    # IRPDeploymentDiagram method parity checklist:
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPDeploymentDiagram methods.

    pass


class RPObjectModelDiagram(RPDiagram):
    """Wraps ``IRPObjectModelDiagram``: represents object model diagrams in Rhapsody models."""

    # IRPObjectModelDiagram method parity checklist:
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPObjectModelDiagram methods.

    pass


class RPPanelDiagram(RPDiagram):
    """Wraps ``IRPPanelDiagram``: represents panel diagrams in Rhapsody models."""

    # IRPPanelDiagram method parity checklist:
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPPanelDiagram methods.

    pass


class RPSequenceDiagram(RPDiagram):
    """Wraps ``IRPSequenceDiagram``: represents sequence diagrams in a Rhapsody model."""

    # IRPSequenceDiagram method parity checklist:
    # [x] getLogicalCollaboration      [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getRelatedUseCases           [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPSequenceDiagram methods.

    def get_logical_collaboration(self) -> "RPCollaboration":
        """Returns the collaboration object underlying the sequence diagram.

        Returns:
            The IRPCollaboration object underlying the sequence diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPSequenceDiagram::getLogicalCollaboration()
        """
        result = AbstractRPModelElement.call_com(lambda: self._com.getLogicalCollaboration())
        return cast("RPCollaboration", AbstractRPModelElement.wrap(result))

    def get_related_use_cases(self) -> "RPCollection":
        """Returns use cases related to this sequence diagram.

        For internal use only.

        Returns:
            A collection of use cases related to the sequence diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPSequenceDiagram::getRelatedUseCases()
        """
        from rhapsody_cli.models.core import RPCollection

        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getRelatedUseCases()))


class RPStatechartDiagram(RPDiagram):
    """Wraps ``IRPStatechartDiagram``: represents statecharts in a Rhapsody model."""

    # IRPStatechartDiagram method parity checklist:
    # [x] addAndLine                   [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] createGraphics               [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getStatechart                [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPStatechartDiagram methods.

    def add_and_line(self, source_state: "RPGraphNode", x_start_position: int, y_start_position: int, x_end_position: int, y_end_position: int) -> "RPCollection":
        """Adds an And Line to the specified state.

        Args:
            source_state: The graphical element representing the state to which
                the And Line should be added.
            x_start_position: The x position at which the And Line should begin.
            y_start_position: The y position at which the And Line should begin.
            x_end_position: The x position at which the And Line should end.
            y_end_position: The y position at which the And Line should end.

        Returns:
            A collection of the new orthogonal states created.

        Reference:
            com.telelogic.rhapsody.core.IRPStatechartDiagram::addAndLine(
                com.telelogic.rhapsody.core.IRPGraphNode sourceState,
                int xStartPosition, int yStartPosition,
                int xEndPosition, int yEndPosition)
        """
        from rhapsody_cli.models.core import RPCollection

        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.addAndLine(source_state._com, x_start_position, y_start_position, x_end_position, y_end_position)))

    def create_graphics(self) -> None:
        """Creates the graphical representation of the elements in the statechart.

        When you create a statechart with the API, the graphical representation
        is not created by default. This means that the first time you open the
        statechart in Rhapsody, you will be asked if the graphics should be
        created. You can create the graphical representation directly by calling
        createGraphics().

        Reference:
            com.telelogic.rhapsody.core.IRPStatechartDiagram::createGraphics()
        """
        AbstractRPModelElement.call_com(lambda: self._com.createGraphics())

    def get_statechart(self) -> "RPStatechart":
        """Returns the statechart object underlying the statechart diagram.

        Returns:
            The IRPStatechart object underlying the statechart.

        Reference:
            com.telelogic.rhapsody.core.IRPStatechartDiagram::getStatechart()
        """
        result = AbstractRPModelElement.call_com(lambda: self._com.getStatechart())
        return cast("RPStatechart", AbstractRPModelElement.wrap(result))


class RPStructureDiagram(RPDiagram):
    """Wraps ``IRPStructureDiagram``: represents structure diagrams in a Rhapsody model."""

    # IRPStructureDiagram method parity checklist:
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPStructureDiagram methods.

    pass


class RPUseCaseDiagram(RPDiagram):
    """Wraps ``IRPUseCaseDiagram``: represents use case diagrams in a Rhapsody model."""

    # IRPUseCaseDiagram method parity checklist:
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPUseCaseDiagram methods.

    pass


class RPTimingDiagram(RPSequenceDiagram):
    """Wraps ``IRPTimingDiagram``."""

    # IRPTimingDiagram method parity checklist:
    # [x] getIsElaborated              [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] setIsElaborated              [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPSequenceDiagram methods (covered by RPSequenceDiagram checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPTimingDiagram methods.

    def get_is_elaborated(self) -> int:
        """Checks whether the timing diagram is an elaborated timing diagram.

        Returns:
            Indication of whether the diagram is an elaborated timing diagram.
            1 means that the diagram is an elaborated timing diagram, 0 means
            that the diagram is a compact timing diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPTimingDiagram::getIsElaborated()
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.getIsElaborated()))

    def set_is_elaborated(self, is_elaborated: int) -> None:
        """Specifies whether the diagram should be an elaborated or compact timing diagram.

        Args:
            is_elaborated: Use 1 to indicate that the diagram should be an
                elaborated timing diagram, 0 to indicate that the diagram should
                be a compact timing diagram. Note that the type of the timing
                diagram should not be changed after you have already added
                elements to the diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPTimingDiagram::setIsElaborated(int isElaborated)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setIsElaborated(is_elaborated))


class RPActivityDiagram(RPStatechartDiagram):
    """Wraps ``IRPActivityDiagram``: represents activity diagrams in Rhapsody models."""

    # IRPActivityDiagram method parity checklist:
    # [x] decomposeSwimlane            [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getFlowchart                 [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPDiagram methods (covered by RPDiagram checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPStatechartDiagram methods (covered by RPStatechartDiagram checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPActivityDiagram methods.

    def decompose_swimlane(self, graph_swimlane: "RPGraphElement") -> "RPCollection":
        """Decomposes the specified swimlane into two swimlanes.

        Args:
            graph_swimlane: The graphic element representing the swimlane to
                decompose.

        Returns:
            The graphic elements representing the two new swimlanes.

        Raises:
            RhapsodyRuntimeException: If the decomposition fails.

        Reference:
            com.telelogic.rhapsody.core.IRPActivityDiagram::decomposeSwimlane(com.telelogic.rhapsody.core.IRPGraphElement graphSwimlane)
        """
        from rhapsody_cli.models.core import RPCollection

        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.decomposeSwimlane(graph_swimlane._com)))

    def get_flowchart(self) -> "RPFlowchart":
        """Returns the flowchart object underlying the activity diagram.

        Returns:
            The IRPFlowchart object underlying the activity diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPActivityDiagram::getFlowchart()
        """
        result = AbstractRPModelElement.call_com(lambda: self._com.getFlowchart())
        return cast("RPFlowchart", AbstractRPModelElement.wrap(result))


# Registration — ActivityDiagram intentionally not re-registered here
# (existing "ActivityDiagram" -> RPDiagram mapping preserved in model_diagrams.py)
AbstractRPModelElement.register_wrapper("CollaborationDiagram", RPCollaborationDiagram)
AbstractRPModelElement.register_wrapper("ComponentDiagram", RPComponentDiagram)
AbstractRPModelElement.register_wrapper("DeploymentDiagram", RPDeploymentDiagram)
AbstractRPModelElement.register_wrapper("ObjectModelDiagram", RPObjectModelDiagram)
AbstractRPModelElement.register_wrapper("PanelDiagram", RPPanelDiagram)
AbstractRPModelElement.register_wrapper("SequenceDiagram", RPSequenceDiagram)
AbstractRPModelElement.register_wrapper("StatechartDiagram", RPStatechartDiagram)
AbstractRPModelElement.register_wrapper("StructureDiagram", RPStructureDiagram)
AbstractRPModelElement.register_wrapper("UseCaseDiagram", RPUseCaseDiagram)
AbstractRPModelElement.register_wrapper("TimingDiagram", RPTimingDiagram)
