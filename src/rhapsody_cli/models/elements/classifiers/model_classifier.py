"""Wraps ``com.telelogic.rhapsody.core.IRPClassifier``."""

from typing import Any

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement, RPUnit

# IRPClassifier method parity checklist:
# [x] addActivityDiagram              [x] impl  [x] docstring  [x] test
# [x] addAttribute                    [x] impl  [x] docstring  [x] test   (already implemented)
# [x] addFlowItems                    [x] impl  [x] docstring  [x] test
# [x] addFlows                        [x] impl  [x] docstring  [x] test
# [x] addGeneralization               [x] impl  [x] docstring  [x] test   (already implemented)
# [x] addOperation                    [x] impl  [x] docstring  [x] test   (already implemented)
# [x] addRelation                     [x] impl  [x] docstring  [x] test
# [x] addRelationTo                   [x] impl  [x] docstring  [x] test
# [x] addStatechart                   [x] impl  [x] docstring  [x] test   (already implemented)
# [x] addUnidirectionalRelation       [x] impl  [x] docstring  [x] test
# [x] addUnidirectionalRelationTo     [x] impl  [x] docstring  [x] test
# [x] deleteAttribute                 [x] impl  [x] docstring  [x] test
# [x] deleteFlowItems                 [x] impl  [x] docstring  [x] test
# [x] deleteFlows                     [x] impl  [x] docstring  [x] test
# [x] deleteGeneralization            [x] impl  [x] docstring  [x] test
# [x] deleteOperation                 [x] impl  [x] docstring  [x] test
# [x] deleteRelation                  [x] impl  [x] docstring  [x] test
# [x] findAttribute                   [x] impl  [x] docstring  [x] test
# [x] findBaseClassifier              [x] impl  [x] docstring  [x] test
# [x] findDerivedClassifier           [x] impl  [x] docstring  [x] test
# [x] findGeneralization              [x] impl  [x] docstring  [x] test
# [x] findInterfaceItem               [x] impl  [x] docstring  [x] test
# [x] findNestedClassifier            [x] impl  [x] docstring  [x] test
# [x] findNestedClassifierRecursive   [x] impl  [x] docstring  [x] test
# [x] findRelation                    [x] impl  [x] docstring  [x] test
# [x] findTrigger                     [x] impl  [x] docstring  [x] test
# [x] getActivityDiagram              [x] impl  [x] docstring  [x] test   (doc recommends getBehavioralDiagrams)
# [x] getAttributes                   [x] impl  [x] docstring  [x] test   (already implemented)
# [x] getAttributesIncludingBases     [x] impl  [x] docstring  [x] test
# [x] getBaseClassifiers              [x] impl  [x] docstring  [x] test
# [x] getBehavioralDiagrams           [x] impl  [x] docstring  [x] test
# [x] getDerivedClassifiers           [x] impl  [x] docstring  [x] test
# [x] getFlowItems                    [x] impl  [x] docstring  [x] test
# [x] getFlows                        [x] impl  [x] docstring  [x] test
# [x] getGeneralizations              [x] impl  [x] docstring  [x] test
# [x] getInterfaceItems               [x] impl  [x] docstring  [x] test
# [x] getInterfaceItemsIncludingBases [x] impl  [x] docstring  [x] test
# [x] getLinks                        [x] impl  [x] docstring  [x] test
# [x] getNestedClassifiers            [x] impl  [x] docstring  [x] test
# [x] getOperations                   [x] impl  [x] docstring  [x] test   (already implemented)
# [x] getPorts                        [x] impl  [x] docstring  [x] test
# [x] getRelations                    [x] impl  [x] docstring  [x] test
# [x] getRelationsIncludingBases      [x] impl  [x] docstring  [x] test
# [x] getSequenceDiagrams             [x] impl  [x] docstring  [x] test
# [x] getSourceArtifacts              [x] impl  [x] docstring  [x] test
# [x] getStatechart                   [x] impl  [x] docstring  [x] test   (doc recommends getBehavioralDiagrams)
# [inherited] IRPUnit / IRPModelElement methods (getName, setName, getOwner, getGUID,
#              addDependency, addStereotype, getStereotypes, getNestedElements, save, load, etc.)
# No deprecated IRPClassifier methods in deprecated-list.html.
# [x] addPort (convenience method, not part of IRPClassifier's Java API -
#     ports are created generically via addNewAggr("Port", name); this
#     wraps that call for ergonomics)  [x] impl  [x] docstring  [x] test


class RPClassifier(RPUnit):
    """Wraps ``IRPClassifier``: the base class for all classifiable elements."""

    def addAttribute(self, name: str) -> Any:
        """Adds a new attribute to the classifier.

        Args:
            name: The name of the new attribute.

        Returns:
            The wrapped ``IRPAttribute`` created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addAttribute(name)))

    def addOperation(self, name: str) -> Any:
        """Adds a new operation to the classifier.

        Args:
            name: The name of the new operation.

        Returns:
            The wrapped ``IRPOperation`` created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addOperation(name)))

    def getAttributes(self) -> RPCollection:
        """Returns all attributes defined on the classifier.

        Returns:
            An ``RPCollection`` of ``IRPAttribute`` objects.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAttributes", "attributes"))

    def getOperations(self) -> RPCollection:
        """Returns all operations defined on the classifier.

        Returns:
            An ``RPCollection`` of ``IRPOperation`` objects.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getOperations", "operations"))

    def addGeneralization(self, base_classifier: "RPClassifier") -> None:
        """Adds a generalization relationship from this classifier to another.

        Args:
            base_classifier: The base classifier to generalize from.
        """
        AbstractRPModelElement.call_com(lambda: self._com.addGeneralization(base_classifier._com))

    def addStatechart(self) -> Any:
        """Adds a statechart behavior to this classifier.

        Returns:
            The wrapped ``IRPStatechart`` created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addStatechart()))

    def addActivityDiagram(self) -> Any:
        """Creates a new activity diagram.

        Returns:
            The wrapped ``IRPFlowchart`` activity diagram that was created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addActivityDiagram()))

    def addFlowItems(self, name: str) -> Any:
        """Adds a new item flow to the classifier.

        Args:
            name: The name to use for the new item flow.

        Returns:
            The wrapped ``IRPFlowItem`` item flow that was created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addFlowItems(name)))

    def addFlows(self, name: str) -> Any:
        """Adds a new flow to the classifier.

        Args:
            name: The name to use for the new flow.

        Returns:
            The wrapped ``IRPFlow`` flow that was created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addFlows(name)))

    def addRelation(
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
    ) -> Any:
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
        """
        return AbstractRPModelElement.wrap(
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
        )

    def addRelationTo(
        self,
        other_classifier: "RPClassifier",
        role_name1: str,
        link_type1: str,
        multiplicity1: str,
        role_name2: str,
        link_type2: str,
        multiplicity2: str,
        link_name: str,
    ) -> Any:
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
        """
        return AbstractRPModelElement.wrap(
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
        )

    def addUnidirectionalRelation(
        self,
        other_class_name: str,
        other_class_package_name: str,
        role_name: str,
        link_type: str,
        multiplicity: str,
        link_name: str,
    ) -> Any:
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
        """
        return AbstractRPModelElement.wrap(
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
        )

    def addUnidirectionalRelationTo(
        self,
        other_classifier: "RPClassifier",
        role_name: str,
        link_type: str,
        multiplicity: str,
        link_name: str,
    ) -> Any:
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
        """
        return AbstractRPModelElement.wrap(
            AbstractRPModelElement.call_com(
                lambda: self._com.addUnidirectionalRelationTo(
                    other_classifier._com,
                    role_name,
                    link_type,
                    multiplicity,
                    link_name,
                )
            )
        )

    def deleteAttribute(self, attribute: "RPModelElement") -> None:
        """Deletes the specified attribute.

        Args:
            attribute: The wrapped attribute that should be deleted.
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteAttribute(attribute._com))

    def deleteFlowItems(self, p_item: "RPModelElement") -> None:
        """Deletes the specified item flow.

        Args:
            p_item: The wrapped item flow that should be deleted.
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteFlowItems(p_item._com))

    def deleteFlows(self, p_flow: "RPModelElement") -> None:
        """Deletes the specified flow.

        Args:
            p_flow: The wrapped flow that should be deleted.
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteFlows(p_flow._com))

    def deleteGeneralization(self, super_class: "RPClassifier") -> None:
        """Deletes the generalization relationship between this classifier and the specified base classifier.

        Args:
            super_class: The classifier whose generalization relationship with
                this classifier should be deleted.
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteGeneralization(super_class._com))

    def deleteOperation(self, operation: "RPModelElement") -> None:
        """Deletes the specified operation.

        Args:
            operation: The wrapped operation that should be deleted.
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteOperation(operation._com))

    def deleteRelation(self, relation: "RPModelElement") -> None:
        """Deletes the specified relation.

        Args:
            relation: The wrapped relation that should be deleted.
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteRelation(relation._com))

    def findAttribute(self, new_val: str) -> Any:
        """Returns the attribute with the name specified.

        Args:
            new_val: The name of the attribute that should be returned.

        Returns:
            The wrapped ``IRPAttribute`` with the name specified.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findAttribute(new_val)))

    def findBaseClassifier(self, new_val: str) -> Any:
        """Returns the base classifier with the specified name.

        Args:
            new_val: The name of the base classifier that should be returned.

        Returns:
            The wrapped ``IRPClassifier`` base classifier with the specified name.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findBaseClassifier(new_val)))

    def findDerivedClassifier(self, new_val: str) -> Any:
        """Returns the derived classifier with the specified name.

        Args:
            new_val: The name of the derived classifier that should be returned.

        Returns:
            The wrapped ``IRPClassifier`` derived classifier with the specified name.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findDerivedClassifier(new_val)))

    def findGeneralization(self, new_val: str) -> Any:
        """Returns the generalization relationship between this classifier and the named classifier.

        Args:
            new_val: The name of the classifier whose generalization
                relationship should be returned.

        Returns:
            The wrapped ``IRPGeneralization`` representing the generalization
            relationship between this classifier and the classifier whose name
            was specified.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findGeneralization(new_val)))

    def findInterfaceItem(self, signature: str) -> Any:
        """Gets the operation or event reception that matches the signature provided.

        Args:
            signature: The signature of the operation or event reception. The
                string should consist of the operation name followed by
                parentheses containing a comma-delimited list of the types of
                the parameters, for example, ``"runEngine(int,int)"``.

        Returns:
            The wrapped ``IRPInterfaceItem`` operation or event reception.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findInterfaceItem(signature)))

    def findNestedClassifier(self, new_val: str) -> Any:
        """Searches for the nested classifier with the name specified.

        This method only searches the first level of elements below the current
        classifier. To search all of the levels below the current classifier,
        use :meth:`findNestedClassifierRecursive`.

        Args:
            new_val: The name of the classifier to search for.

        Returns:
            The wrapped ``IRPClassifier`` with the name that was specified.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findNestedClassifier(new_val)))

    def findNestedClassifierRecursive(self, new_val: str) -> Any:
        """Searches recursively for the classifier with the name specified.

        This method searches all of the levels below the current classifier. To
        search only the first level of elements below the current classifier,
        use :meth:`findNestedClassifier`.

        Args:
            new_val: The name of the classifier to search for.

        Returns:
            The wrapped classifier that was specified (returned as an
            ``IRPModelElement``).
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findNestedClassifierRecursive(new_val)))

    def findRelation(self, new_val: str) -> Any:
        """Returns the association whose name was specified as a parameter.

        Args:
            new_val: The name of the association that should be returned.

        Returns:
            The wrapped ``IRPRelation`` association whose name was specified.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findRelation(new_val)))

    def findTrigger(self, name: str) -> Any:
        """Returns the trigger with the specified name in the classifier's statechart.

        Args:
            name: The name of the trigger to find.

        Returns:
            The wrapped ``IRPInterfaceItem`` trigger with the specified name.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findTrigger(name)))

    def getActivityDiagram(self) -> Any:
        """Returns the activity diagram defined for the classifier.

        Note: the Java API recommends using :meth:`getBehavioralDiagrams`
        instead, because Rhapsody now allows more than one statechart and
        activity diagram to be defined for a class.

        Returns:
            The wrapped ``IRPFlowchart`` activity diagram.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getActivityDiagram", "activityDiagram"))

    def getAttributesIncludingBases(self) -> RPCollection:
        """Returns all the classifier's attributes, including inherited ones.

        Returns:
            An ``RPCollection`` of ``IRPAttribute`` objects, including those
            inherited from the classifier's base classifiers.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAttributesIncludingBases", "attributesIncludingBases"))

    def getBaseClassifiers(self) -> RPCollection:
        """Returns the classifiers that serve as base classifiers for this classifier.

        Returns:
            An ``RPCollection`` of ``IRPClassifier`` base classifiers.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getBaseClassifiers", "baseClassifiers"))

    def getBehavioralDiagrams(self) -> RPCollection:
        """Returns all the statecharts and activities defined for the classifier.

        The returned collection consists of elements of type ``IRPStatechart``.

        Returns:
            An ``RPCollection`` of ``IRPStatechart`` statecharts and activities.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getBehavioralDiagrams", "behavioralDiagrams"))

    def getDerivedClassifiers(self) -> RPCollection:
        """Returns all the classifiers derived from this classifier.

        Returns:
            An ``RPCollection`` of ``IRPClassifier`` derived classifiers.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getDerivedClassifiers", "derivedClassifiers"))

    def getFlowItems(self) -> RPCollection:
        """Returns all the classifier's item flows.

        Returns:
            An ``RPCollection`` of ``IRPFlowItem`` item flows.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getFlowItems", "flowItems"))

    def getFlows(self) -> RPCollection:
        """Returns all the classifier's flows.

        Returns:
            An ``RPCollection`` of ``IRPFlow`` flows.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getFlows", "flows"))

    def getGeneralizations(self) -> RPCollection:
        """Returns all the classifier's generalization relationships.

        Returns:
            An ``RPCollection`` of ``IRPGeneralization`` generalization relationships.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getGeneralizations", "generalizations"))

    def getInterfaceItems(self) -> RPCollection:
        """Returns the classifier's elements of type IRPInterfaceItem.

        This includes operations, triggered operations, and event receptions.

        Returns:
            An ``RPCollection`` of ``IRPInterfaceItem`` elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getInterfaceItems", "interfaceItems"))

    def getInterfaceItemsIncludingBases(self) -> RPCollection:
        """Returns the classifier's IRPInterfaceItem elements, including inherited ones.

        This includes operations, triggered operations, and event receptions,
        including those inherited from the classifier's base classifier.

        Returns:
            An ``RPCollection`` of ``IRPInterfaceItem`` elements, including
            those inherited from the base classifier.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getInterfaceItemsIncludingBases", "interfaceItemsIncludingBases"))

    def getLinks(self) -> RPCollection:
        """Returns all the classifier's link relationships.

        Returns:
            An ``RPCollection`` of link relationships.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getLinks", "links"))

    def getNestedClassifiers(self) -> RPCollection:
        """Returns the classifiers nested below the current classifier.

        This method is not recursive - it only returns the classifiers at the
        level directly below the current classifier.

        Returns:
            An ``RPCollection`` of ``IRPClassifier`` nested classifiers.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNestedClassifiers", "nestedClassifiers"))

    def getPorts(self) -> RPCollection:
        """Returns all the classifier's ports.

        Returns:
            An ``RPCollection`` of ``IRPPort`` ports.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getPorts", "ports"))

    def addPort(self, name: str) -> Any:
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

    def getRelations(self) -> RPCollection:
        """Returns all the classifier's associations.

        Returns:
            An ``RPCollection`` of ``IRPRelation`` associations.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRelations", "relations"))

    def getRelationsIncludingBases(self) -> RPCollection:
        """Returns all the classifier's associations, including inherited ones.

        Returns:
            An ``RPCollection`` of ``IRPRelation`` associations, including those
            inherited from the classifier's base classifier.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRelationsIncludingBases", "relationsIncludingBases"))

    def getSequenceDiagrams(self) -> RPCollection:
        """Returns the classifier's sequence diagrams.

        Returns:
            An ``RPCollection`` of sequence diagrams.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getSequenceDiagrams", "sequenceDiagrams"))

    def getSourceArtifacts(self) -> RPCollection:
        """Gets the source artifacts for the classifier.

        Returns:
            An ``RPCollection`` of ``IRPFile`` source artifacts.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getSourceArtifacts", "sourceArtifacts"))

    def getStatechart(self) -> Any:
        """Returns the statechart defined for the classifier.

        Note: the Java API recommends using :meth:`getBehavioralDiagrams`
        instead, because Rhapsody now allows more than one statechart and
        activity diagram to be defined for a class.

        Returns:
            The wrapped ``IRPStatechart`` statechart.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getStatechart", "statechart"))
