"""Wraps ``com.telelogic.rhapsody.core.IRPClassifier``."""

from typing import TYPE_CHECKING, Any, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement, RPUnit

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.activity.model_activity import RPFlow, RPFlowchart, RPFlowItem
    from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem
    from rhapsody_cli.models.elements.classifiers.model_operation import RPOperation
    from rhapsody_cli.models.elements.classifiers.model_statechart import RPStatechart
    from rhapsody_cli.models.elements.relations.model_generalization import RPGeneralization
    from rhapsody_cli.models.elements.relations.model_relation import RPRelation
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute


class RPClassifier(RPUnit):
    """Wraps ``IRPClassifier``: the base class for all classifiable elements."""

    # IRPClassifier method parity checklist:
    # [x] add_activity_diagram              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_attribute                    [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] add_flow_items                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_flows                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_generalization               [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] add_operation                    [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] add_relation                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_relation_to                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_statechart                   [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] add_unidirectional_relation       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_unidirectional_relation_to     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] delete_attribute                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] delete_flow_items                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] delete_flows                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] delete_generalization            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] delete_operation                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] delete_relation                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_attribute                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_base_classifier              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_derived_classifier           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_generalization              [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] find_interface_item               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_nested_classifier            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_nested_classifier_recursive   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_relation                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_trigger                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_activity_diagram              [x] impl  [x] docstring  [x] unit test  [ ] integration test   (doc recommends get_behavioral_diagrams)
    # [x] get_attributes                   [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] get_attributes_including_bases     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_base_classifiers              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_behavioral_diagrams           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_derived_classifiers           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_flow_items                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_flows                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_generalizations              [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_interface_items               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_items_including_bases [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_links                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_nested_classifiers            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_operations                   [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] get_ports                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_relations                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_relations_including_bases      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_sequence_diagrams             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_source_artifacts              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_statechart                   [x] impl  [x] docstring  [x] unit test  [ ] integration test   (doc recommends get_behavioral_diagrams)
    # [inherited] irp_unit / irp_model_element methods (get_name, set_name, get_owner, get_guid,
    #              addDependency, addStereotype, getStereotypes, getNestedElements, save, load, etc.)
    # No deprecated IRPClassifier methods in deprecated-list.html.
    # [x] add_port (convenience method, not part of irp_classifier's Java API -
    #     ports are created generically via addNewAggr("Port", name); this
    #     wraps that call for ergonomics)  [x] impl  [x] docstring  [x] unit test  [ ] integration test

    def add_attribute(self, name: str) -> "RPAttribute":
        """Adds a new attribute to the classifier.

        Args:
            name: The name of the new attribute.

        Returns:
            The wrapped ``IRPAttribute`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addAttribute(java.lang.String name)
        """
        return cast("RPAttribute", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addAttribute(name))))

    def add_operation(self, name: str) -> "RPOperation":
        """Adds a new operation to the classifier.

        Args:
            name: The name of the new operation.

        Returns:
            The wrapped ``IRPOperation`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addOperation(java.lang.String name)
        """
        return cast("RPOperation", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addOperation(name))))

    def get_attributes(self) -> RPCollection:
        """Returns all attributes defined on the classifier.

        Returns:
            An ``RPCollection`` of ``IRPAttribute`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getAttributes()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAttributes", "attributes"))

    def get_operations(self) -> RPCollection:
        """Returns all operations defined on the classifier.

        Returns:
            An ``RPCollection`` of ``IRPOperation`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getOperations()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getOperations", "operations"))

    def add_generalization(self, base_classifier: "RPClassifier") -> None:
        """Adds a generalization relationship from this classifier to another.

        Args:
            base_classifier: The base classifier to generalize from.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addGeneralization(com.telelogic.rhapsody.core.IRPClassifier pVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addGeneralization(base_classifier._com))

    def add_statechart(self) -> "RPStatechart":
        """Adds a statechart behavior to this classifier.

        Returns:
            The wrapped ``IRPStatechart`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addStatechart()
        """
        return cast("RPStatechart", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addStatechart())))

    def add_activity_diagram(self) -> "RPFlowchart":
        """Creates a new activity diagram.

        Returns:
            The wrapped ``IRPFlowchart`` activity diagram that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addActivityDiagram()
        """
        return cast("RPFlowchart", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addActivityDiagram())))

    def add_flow_items(self, name: str) -> "RPFlowItem":
        """Adds a new item flow to the classifier.

        Args:
            name: The name to use for the new item flow.

        Returns:
            The wrapped ``IRPFlowItem`` item flow that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addFlowItems(java.lang.String name)
        """
        return cast("RPFlowItem", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addFlowItems(name))))

    def add_flows(self, name: str) -> "RPFlow":
        """Adds a new flow to the classifier.

        Args:
            name: The name to use for the new flow.

        Returns:
            The wrapped ``IRPFlow`` flow that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addFlows(java.lang.String name)
        """
        return cast("RPFlow", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addFlows(name))))

    def add_relation(
        self,
        other_class_name: str,
        other_class_package_name: str,
        role_name1: str,
        link_type1: str,
        multiplicity1: str,
        role_name2: str,
        link_type2: str,
        multiplicity2: str,
        link_name: str,
    ) -> "RPRelation":
        """Adds a new association to the classifier.

        Args:
            other_class_name: The name of the classifier that the current
                classifier should be associated with.
            other_class_package_name: The name of the package that contains the
                classifier that the current classifier should be associated with.
            role_name1: The role name to use for the association end near the
                other classifier.
            link_type1: Used with ``link_type2`` to determine the type of
                association to create. Allowed values are ``"Association"``,
                ``"Aggregation"``, and ``"Composition"`` (case-sensitive). To
                create a simple association, use ``"Association"`` for both
                ``link_type`` parameters. To create an aggregation, use
                ``"Association"`` for one and ``"Aggregation"`` for the other.
                To create a composition, use ``"Association"`` for one and
                ``"Composition"`` for the other.
            multiplicity1: The multiplicity to use for the association end near
                the other classifier (e.g. ``"1"``, ``"0,1"``, ``"*"``, ``"1..*"``).
            role_name2: The role name to use for the association end near the
                current classifier.
            link_type2: Used with ``link_type1`` to determine the type of
                association to create (see ``link_type1``).
            multiplicity2: The multiplicity to use for the association end near
                the current classifier (e.g. ``"1"``, ``"0,1"``, ``"*"``, ``"1..*"``).
            link_name: To create an association class, specify the name of the
                class. Otherwise, use an empty string.

        Returns:
            The wrapped ``IRPRelation`` association that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addRelation(
                java.lang.String otherClassName,
                java.lang.String otherClassPackageName,
                java.lang.String roleName1,
                java.lang.String linkType1,
                java.lang.String multiplicity1,
                java.lang.String roleName2,
                java.lang.String linkType2,
                java.lang.String multiplicity2,
                java.lang.String linkName)
        """
        return cast(
            "RPRelation",
            AbstractRPModelElement.wrap(
                AbstractRPModelElement.call_com(
                    lambda: self._com.addRelation(
                        other_class_name,
                        other_class_package_name,
                        role_name1,
                        link_type1,
                        multiplicity1,
                        role_name2,
                        link_type2,
                        multiplicity2,
                        link_name,
                    )
                )
            ),
        )

    def add_relation_to(
        self,
        other_classifier: "RPClassifier",
        role_name1: str,
        link_type1: str,
        multiplicity1: str,
        role_name2: str,
        link_type2: str,
        multiplicity2: str,
        link_name: str,
    ) -> "RPRelation":
        """Adds a new association to the classifier.

        Args:
            other_classifier: The classifier that the current classifier should
                be associated with.
            role_name1: The role name to use for the association end near the
                other classifier.
            link_type1: Used with ``link_type2`` to determine the type of
                association to create. Allowed values are ``"Association"``,
                ``"Aggregation"``, and ``"Composition"`` (case-sensitive). To
                create a simple association, use ``"Association"`` for both
                ``link_type`` parameters. To create an aggregation, use
                ``"Association"`` for one and ``"Aggregation"`` for the other.
                To create a composition, use ``"Association"`` for one and
                ``"Composition"`` for the other.
            multiplicity1: The multiplicity to use for the association end near
                the other classifier (e.g. ``"1"``, ``"0,1"``, ``"*"``, ``"1..*"``).
            role_name2: The role name to use for the association end near the
                current classifier.
            link_type2: Used with ``link_type1`` to determine the type of
                association to create (see ``link_type1``).
            multiplicity2: The multiplicity to use for the association end near
                the current classifier (e.g. ``"1"``, ``"0,1"``, ``"*"``, ``"1..*"``).
            link_name: To create an association class, specify the name of the
                class. Otherwise, use an empty string.

        Returns:
            The wrapped ``IRPRelation`` association that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addRelationTo(
                com.telelogic.rhapsody.core.IRPClassifier otherClassifier,
                java.lang.String roleName1,
                java.lang.String linkType1,
                java.lang.String multiplicity1,
                java.lang.String roleName2,
                java.lang.String linkType2,
                java.lang.String multiplicity2,
                java.lang.String linkName)
        """
        return cast(
            "RPRelation",
            AbstractRPModelElement.wrap(
                AbstractRPModelElement.call_com(
                    lambda: self._com.addRelationTo(
                        other_classifier._com,
                        role_name1,
                        link_type1,
                        multiplicity1,
                        role_name2,
                        link_type2,
                        multiplicity2,
                        link_name,
                    )
                )
            ),
        )

    def add_unidirectional_relation(
        self,
        other_class_name: str,
        other_class_package_name: str,
        role_name: str,
        link_type: str,
        multiplicity: str,
        link_name: str,
    ) -> "RPRelation":
        """Adds a new directed association to the classifier.

        Args:
            other_class_name: The name of the classifier that the current
                classifier should be associated with.
            other_class_package_name: The name of the package that contains the
                classifier that the current classifier should be associated with.
            role_name: The role name to use for the association end.
            link_type: Used to determine the type of association to create.
                Allowed values are ``"Association"``, ``"Aggregation"``, and
                ``"Composition"`` (case-sensitive).
            multiplicity: The multiplicity to use for the association end (e.g.
                ``"1"``, ``"0,1"``, ``"*"``, ``"1..*"``).
            link_name: To create an association class, specify the name of the
                class. Otherwise, use an empty string.

        Returns:
            The wrapped ``IRPRelation`` association that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addUnidirectionalRelation(
                java.lang.String otherClassName,
                java.lang.String otherClassPackageName,
                java.lang.String roleName,
                java.lang.String linkType,
                java.lang.String multiplicity,
                java.lang.String linkName)
        """
        return cast(
            "RPRelation",
            AbstractRPModelElement.wrap(
                AbstractRPModelElement.call_com(
                    lambda: self._com.addUnidirectionalRelation(
                        other_class_name,
                        other_class_package_name,
                        role_name,
                        link_type,
                        multiplicity,
                        link_name,
                    )
                )
            ),
        )

    def add_unidirectional_relation_to(
        self,
        other_classifier: "RPClassifier",
        role_name: str,
        link_type: str,
        multiplicity: str,
        link_name: str,
    ) -> "RPRelation":
        """Adds a new directed association to the classifier.

        Args:
            other_classifier: The classifier that the current classifier should
                be associated with.
            role_name: The role name to use for the association end.
            link_type: Used to determine the type of association to create.
                Allowed values are ``"Association"``, ``"Aggregation"``, and
                ``"Composition"`` (case-sensitive).
            multiplicity: The multiplicity to use for the association end (e.g.
                ``"1"``, ``"0,1"``, ``"*"``, ``"1..*"``).
            link_name: To create an association class, specify the name of the
                class. Otherwise, use an empty string.

        Returns:
            The wrapped ``IRPRelation`` association that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::addUnidirectionalRelationTo(
                com.telelogic.rhapsody.core.IRPClassifier otherClassifier,
                java.lang.String roleName,
                java.lang.String linkType,
                java.lang.String multiplicity,
                java.lang.String linkName)
        """
        return cast(
            "RPRelation",
            AbstractRPModelElement.wrap(
                AbstractRPModelElement.call_com(
                    lambda: self._com.addUnidirectionalRelationTo(
                        other_classifier._com,
                        role_name,
                        link_type,
                        multiplicity,
                        link_name,
                    )
                )
            ),
        )

    def delete_attribute(self, attribute: "RPModelElement") -> None:
        """Deletes the specified attribute.

        Args:
            attribute: The wrapped attribute that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::deleteAttribute(com.telelogic.rhapsody.core.IRPAttribute attribute)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteAttribute(attribute._com))

    def delete_flow_items(self, p_item: "RPModelElement") -> None:
        """Deletes the specified item flow.

        Args:
            p_item: The wrapped item flow that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::deleteFlowItems(com.telelogic.rhapsody.core.IRPFlowItem pItem)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteFlowItems(p_item._com))

    def delete_flows(self, p_flow: "RPModelElement") -> None:
        """Deletes the specified flow.

        Args:
            p_flow: The wrapped flow that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::deleteFlows(com.telelogic.rhapsody.core.IRPFlow pFlow)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteFlows(p_flow._com))

    def delete_generalization(self, super_class: "RPClassifier") -> None:
        """Deletes the generalization relationship between this classifier and the specified base classifier.

        Args:
            super_class: The classifier whose generalization relationship with
                this classifier should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::deleteGeneralization(com.telelogic.rhapsody.core.IRPClassifier superClass)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteGeneralization(super_class._com))

    def delete_operation(self, operation: "RPModelElement") -> None:
        """Deletes the specified operation.

        Args:
            operation: The wrapped operation that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::deleteOperation(com.telelogic.rhapsody.core.IRPOperation operation)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteOperation(operation._com))

    def delete_relation(self, relation: "RPModelElement") -> None:
        """Deletes the specified relation.

        Args:
            relation: The wrapped relation that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::deleteRelation(com.telelogic.rhapsody.core.IRPRelation relation)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteRelation(relation._com))

    def find_attribute(self, new_val: str) -> "RPAttribute":
        """Returns the attribute with the name specified.

        Args:
            new_val: The name of the attribute that should be returned.

        Returns:
            The wrapped ``IRPAttribute`` with the name specified.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::findAttribute(java.lang.String newVal)
        """
        return cast("RPAttribute", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findAttribute(new_val))))

    def find_base_classifier(self, new_val: str) -> "RPClassifier":
        """Returns the base classifier with the specified name.

        Args:
            new_val: The name of the base classifier that should be returned.

        Returns:
            The wrapped ``IRPClassifier`` base classifier with the specified name.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::findBaseClassifier(java.lang.String newVal)
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findBaseClassifier(new_val))))

    def find_derived_classifier(self, new_val: str) -> "RPClassifier":
        """Returns the derived classifier with the specified name.

        Args:
            new_val: The name of the derived classifier that should be returned.

        Returns:
            The wrapped ``IRPClassifier`` derived classifier with the specified name.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::findDerivedClassifier(java.lang.String newVal)
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findDerivedClassifier(new_val))))

    def find_generalization(self, new_val: str) -> "RPGeneralization":
        """Returns the generalization relationship between this classifier and the named classifier.

        Args:
            new_val: The name of the classifier whose generalization
                relationship should be returned.

        Returns:
            The wrapped ``IRPGeneralization`` representing the generalization
            relationship between this classifier and the classifier whose name
            was specified.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::findGeneralization(java.lang.String newVal)
        """
        return cast("RPGeneralization", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findGeneralization(new_val))))

    def find_interface_item(self, signature: str) -> "RPInterfaceItem":
        """Gets the operation or event reception that matches the signature provided.

        Args:
            signature: The signature of the operation or event reception. The
                string should consist of the operation name followed by
                parentheses containing a comma-delimited list of the types of
                the parameters, for example, ``"runEngine(int,int)"``.

        Returns:
            The wrapped ``IRPInterfaceItem`` operation or event reception.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::findInterfaceItem(java.lang.String signature)
        """
        return cast("RPInterfaceItem", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findInterfaceItem(signature))))

    def find_nested_classifier(self, new_val: str) -> "RPClassifier":
        """Searches for the nested classifier with the name specified.

        This method only searches the first level of elements below the current
        classifier. To search all of the levels below the current classifier,
        use :meth:`find_nested_classifier_recursive`.

        Args:
            new_val: The name of the classifier to search for.

        Returns:
            The wrapped ``IRPClassifier`` with the name that was specified.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::findNestedClassifier(java.lang.String newVal)
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findNestedClassifier(new_val))))

    def find_nested_classifier_recursive(self, new_val: str) -> "RPModelElement":
        """Searches recursively for the classifier with the name specified.

        This method searches all of the levels below the current classifier. To
        search only the first level of elements below the current classifier,
        use :meth:`find_nested_classifier`.

        Args:
            new_val: The name of the classifier to search for.

        Returns:
            The wrapped classifier that was specified (returned as an
            ``IRPModelElement``).

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::findNestedClassifierRecursive(java.lang.String newVal)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findNestedClassifierRecursive(new_val)))

    def find_relation(self, new_val: str) -> "RPRelation":
        """Returns the association whose name was specified as a parameter.

        Args:
            new_val: The name of the association that should be returned.

        Returns:
            The wrapped ``IRPRelation`` association whose name was specified.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::findRelation(java.lang.String newVal)
        """
        return cast("RPRelation", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findRelation(new_val))))

    def find_trigger(self, name: str) -> "RPInterfaceItem":
        """Returns the trigger with the specified name in the classifier's statechart.

        Args:
            name: The name of the trigger to find.

        Returns:
            The wrapped ``IRPInterfaceItem`` trigger with the specified name.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::findTrigger(java.lang.String name)
        """
        return cast("RPInterfaceItem", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findTrigger(name))))

    def get_activity_diagram(self) -> "RPFlowchart":
        """Returns the activity diagram defined for the classifier.

        Note: the Java API recommends using :meth:`get_behavioral_diagrams`
        instead, because Rhapsody now allows more than one statechart and
        activity diagram to be defined for a class.

        Returns:
            The wrapped ``IRPFlowchart`` activity diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getActivityDiagram()
        """
        return cast("RPFlowchart", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getActivityDiagram", "activityDiagram")))

    def get_attributes_including_bases(self) -> RPCollection:
        """Returns all the classifier's attributes, including inherited ones.

        Returns:
            An ``RPCollection`` of ``IRPAttribute`` objects, including those
            inherited from the classifier's base classifiers.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getAttributesIncludingBases()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAttributesIncludingBases", "attributesIncludingBases"))

    def get_base_classifiers(self) -> RPCollection:
        """Returns the classifiers that serve as base classifiers for this classifier.

        Returns:
            An ``RPCollection`` of ``IRPClassifier`` base classifiers.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getBaseClassifiers()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getBaseClassifiers", "baseClassifiers"))

    def get_behavioral_diagrams(self) -> RPCollection:
        """Returns all the statecharts and activities defined for the classifier.

        The returned collection consists of elements of type ``IRPStatechart``.

        Returns:
            An ``RPCollection`` of ``IRPStatechart`` statecharts and activities.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getBehavioralDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getBehavioralDiagrams", "behavioralDiagrams"))

    def get_derived_classifiers(self) -> RPCollection:
        """Returns all the classifiers derived from this classifier.

        Returns:
            An ``RPCollection`` of ``IRPClassifier`` derived classifiers.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getDerivedClassifiers()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getDerivedClassifiers", "derivedClassifiers"))

    def get_flow_items(self) -> RPCollection:
        """Returns all the classifier's item flows.

        Returns:
            An ``RPCollection`` of ``IRPFlowItem`` item flows.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getFlowItems()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getFlowItems", "flowItems"))

    def get_flows(self) -> RPCollection:
        """Returns all the classifier's flows.

        Returns:
            An ``RPCollection`` of ``IRPFlow`` flows.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getFlows()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getFlows", "flows"))

    def get_generalizations(self) -> RPCollection:
        """Returns all the classifier's generalization relationships.

        Returns:
            An ``RPCollection`` of ``IRPGeneralization`` generalization relationships.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getGeneralizations()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getGeneralizations", "generalizations"))

    def get_interface_items(self) -> RPCollection:
        """Returns the classifier's elements of type IRPInterfaceItem.

        This includes operations, triggered operations, and event receptions.

        Returns:
            An ``RPCollection`` of ``IRPInterfaceItem`` elements.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getInterfaceItems()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getInterfaceItems", "interfaceItems"))

    def get_interface_items_including_bases(self) -> RPCollection:
        """Returns the classifier's IRPInterfaceItem elements, including inherited ones.

        This includes operations, triggered operations, and event receptions,
        including those inherited from the classifier's base classifier.

        Returns:
            An ``RPCollection`` of ``IRPInterfaceItem`` elements, including
            those inherited from the base classifier.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getInterfaceItemsIncludingBases()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getInterfaceItemsIncludingBases", "interfaceItemsIncludingBases"))

    def get_links(self) -> RPCollection:
        """Returns all the classifier's link relationships.

        Returns:
            An ``RPCollection`` of link relationships.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getLinks()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getLinks", "links"))

    def get_nested_classifiers(self) -> RPCollection:
        """Returns the classifiers nested below the current classifier.

        This method is not recursive - it only returns the classifiers at the
        level directly below the current classifier.

        Returns:
            An ``RPCollection`` of ``IRPClassifier`` nested classifiers.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getNestedClassifiers()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNestedClassifiers", "nestedClassifiers"))

    def get_ports(self) -> RPCollection:
        """Returns all the classifier's ports.

        Returns:
            An ``RPCollection`` of ``IRPPort`` ports.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getPorts()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getPorts", "ports"))

    def add_port(self, name: str) -> Any:
        """Adds a new port to this classifier.

        Convenience method: the Rhapsody Java API has no dedicated
        ``addPort`` factory method — ports are created generically via
        ``addNewAggr("Port", name)``. This method encapsulates that call so
        callers don't need to know the metaclass-string incantation.

        Args:
            name: The name to use for the new port.

        Returns:
            The wrapped ``IRPPort`` created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNewAggr("Port", name)))

    def get_relations(self) -> RPCollection:
        """Returns all the classifier's associations.

        Returns:
            An ``RPCollection`` of ``IRPRelation`` associations.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getRelations()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRelations", "relations"))

    def get_relations_including_bases(self) -> RPCollection:
        """Returns all the classifier's associations, including inherited ones.

        Returns:
            An ``RPCollection`` of ``IRPRelation`` associations, including those
            inherited from the classifier's base classifier.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getRelationsIncludingBases()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRelationsIncludingBases", "relationsIncludingBases"))

    def get_sequence_diagrams(self) -> RPCollection:
        """Returns the classifier's sequence diagrams.

        Returns:
            An ``RPCollection`` of sequence diagrams.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getSequenceDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getSequenceDiagrams", "sequenceDiagrams"))

    def get_source_artifacts(self) -> RPCollection:
        """Gets the source artifacts for the classifier.

        Returns:
            An ``RPCollection`` of ``IRPFile`` source artifacts.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getSourceArtifacts()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getSourceArtifacts", "sourceArtifacts"))

    def get_statechart(self) -> "RPStatechart":
        """Returns the statechart defined for the classifier.

        Note: the Java API recommends using :meth:`get_behavioral_diagrams`
        instead, because Rhapsody now allows more than one statechart and
        activity diagram to be defined for a class.

        Returns:
            The wrapped ``IRPStatechart`` statechart.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifier::getStatechart()
        """
        return cast("RPStatechart", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getStatechart", "statechart")))
