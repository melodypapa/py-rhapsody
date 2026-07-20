"""RhapsodyModelHelper: reusable model manipulation for exchange and beyond.

SWR_XCH_006: Element Find-or-Create (RhapsodyModelHelper)
SWR_XCH_007: Stereotype and Tag Round-Trip
SWR_XCH_010: Reusable Model Manipulation API
"""

import logging
from typing import TYPE_CHECKING, Dict, List, Optional, Set

from rhapsody_cli.models.core import RPModelElement

if TYPE_CHECKING:
    from rhapsody_cli.application import RhapsodyApplication
    from rhapsody_cli.models.elements.containment import RPProject

logger = logging.getLogger(__name__)


class RhapsodyModelHelper:
    """Reusable model manipulation utilities.

    Provides idempotent find-or-create methods for the 14 supported element
    types, plus stereotype/tag application, classifier resolution, and
    child lookup. Used by both RhapsodyImporter and RhapsodyExporter.

    Attributes:
        app: RhapsodyApplication instance (lazily connected if not provided).
        project: Active RPProject, or None until set by caller.
    """

    def __init__(self, app: Optional["RhapsodyApplication"] = None) -> None:
        """Initialize with optional app; connect lazily if not provided.

        Args:
            app: Existing RhapsodyApplication, or None to trigger lazy connect.
        """
        if app is None:
            from rhapsody_cli.application import RhapsodyApplication

            app = RhapsodyApplication.connect(attach_only=True)
        self.app = app
        self.project: Optional["RPProject"] = None  # noqa: UP037

    # ------------------------------------------------------------------
    # Element find/create (idempotent)
    # ------------------------------------------------------------------

    def find_or_create_package(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Package under parent. Sanitizes name (spaces -> underscores)."""
        sanitized = name.replace(" ", "_")
        existing = self.find_child_by_name(parent, "Package", sanitized)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Package", sanitized)

    def find_or_create_class(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Class under parent."""
        existing = self.find_child_by_name(parent, "Class", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Class", name)

    def find_or_create_operation(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Operation under parent.

        Uses add_global_function when parent is a Package (Rhapsody stores
        global functions in a hidden TopLevel class); otherwise add_new_aggr.
        """
        existing = self.find_child_by_name(parent, "Operation", name)
        if existing is not None:
            return existing
        if parent.get_meta_class() == "Package":
            return parent.add_global_function(name)  # type: ignore[attr-defined, no-any-return]
        return parent.add_new_aggr("Operation", name)

    def find_or_create_argument(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Argument under an Operation."""
        existing = self.find_child_by_name(parent, "Argument", name)
        if existing is not None:
            return existing
        return parent.add_argument(name)  # type: ignore[attr-defined, no-any-return]

    def find_or_create_attribute(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Attribute under parent."""
        existing = self.find_child_by_name(parent, "Attribute", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Attribute", name)

    def find_or_create_type(self, parent: RPModelElement, name: str, kind: Optional[str] = None) -> RPModelElement:
        """Find or create a Type under parent, optionally setting its kind."""
        existing = self.find_child_by_name(parent, "Type", name)
        if existing is not None:
            return existing
        element = parent.add_new_aggr("Type", name)
        if kind is not None:
            self._set_type_kind(element, kind)
        return element

    def find_or_create_object(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Object (instance) under parent."""
        existing = self.find_child_by_name(parent, "Object", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Object", name)

    def find_or_create_enumeration_literal(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an EnumerationLiteral under a Type (kind=Enumeration)."""
        existing = self.find_child_by_name(parent, "EnumerationLiteral", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("EnumerationLiteral", name)

    def find_or_create_dependency(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Dependency under parent. Source/target wiring handled by importer."""
        existing = self.find_child_by_name(parent, "Dependency", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Dependency", name)

    def find_or_create_generalization(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Generalization under parent. Base class wiring handled by importer."""
        existing = self.find_child_by_name(parent, "Generalization", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Generalization", name)

    def find_or_create_relation(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Relation (Association/Aggregation/Composition) under parent."""
        existing = self.find_child_by_name(parent, "Relation", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Relation", name)

    def find_or_create_port(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Port under parent. Contract/interface wiring handled by importer."""
        existing = self.find_child_by_name(parent, "Port", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Port", name)

    def find_or_create_event(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Event under parent. Base/super event wiring handled by importer."""
        existing = self.find_child_by_name(parent, "Event", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Event", name)

    def find_or_create_event_reception(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an EventReception under parent. Event reference wiring handled by importer."""
        existing = self.find_child_by_name(parent, "EventReception", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("EventReception", name)

    # ------------------------------------------------------------------
    # Property application
    # ------------------------------------------------------------------

    def apply_stereotypes(self, element: RPModelElement, stereotypes: List[str]) -> None:
        """Apply stereotypes to element, inferring meta_type from element's metaclass.

        Skips stereotypes already applied (idempotent).
        """
        if not stereotypes:
            return
        meta_type = element.get_meta_class()
        already_applied = set()
        try:
            existing = element.get_stereotypes()
            for st in existing:
                try:
                    already_applied.add(st.get_name())
                except Exception:
                    continue
        except Exception:
            # If we can't read existing stereotypes, apply all (defensive)
            pass
        for name in stereotypes:
            if name in already_applied:
                continue
            element.add_stereotype(name, meta_type)

    def apply_tags(self, element: RPModelElement, tags: Dict[str, str]) -> None:
        """Apply tags to element via set_property_value (idempotent).

        Uses set_property_value (existing convention from package_action.py)
        which creates the property if missing and updates if present.
        """
        for name, value in tags.items():
            element.set_property_value(name, str(value))

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def resolve_classifier(self, name: str) -> Optional[RPModelElement]:
        """Find a classifier by name anywhere in the project. Returns None if not found."""
        if self.project is None:
            return None
        return self._find_element_by_name(self.project, name)

    def get_classifier_name(self, classifier: Optional[RPModelElement]) -> Optional[str]:
        """Return classifier's name, or None if classifier is None or unreadable."""
        if classifier is None:
            return None
        try:
            return classifier.get_name()
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Public lookup
    # ------------------------------------------------------------------

    def find_child_by_name(self, parent: RPModelElement, meta_class: str, name: str) -> Optional[RPModelElement]:
        """Find a direct child of parent by metaclass + name. Returns None if not found."""
        try:
            children = parent.get_nested_elements()
        except Exception:
            return None
        for child in children:
            try:
                if child.get_meta_class() == meta_class and child.get_name() == name:
                    return child  # type: ignore[no-any-return]
            except Exception:
                continue
        return None

    # ------------------------------------------------------------------
    # Private (exchange-specific internals)
    # ------------------------------------------------------------------

    def _set_type_kind(self, type_element: RPModelElement, kind: str) -> None:
        """Set a Type's kind (Enumeration, Structure, Language, Typedef, Union)."""
        type_element.set_kind(kind)  # type: ignore[attr-defined]

    def _collect_children(self, container: RPModelElement) -> List[RPModelElement]:
        """Collect all children of a container.

        For Package containers, merges get_nested_elements() with package-level
        globals (get_global_functions, get_global_variables, get_global_objects)
        since getNestedElements() excludes them.

        For other containers, returns list(get_nested_elements()).
        """
        try:
            children = list(container.get_nested_elements())
        except Exception:
            children = []
        if container.get_meta_class() == "Package":
            for getter_name in ("get_global_functions", "get_global_variables", "get_global_objects"):
                getter = getattr(container, getter_name, None)
                if getter is None:
                    continue
                try:
                    children.extend(getter())
                except Exception:
                    continue
        return children

    def _get_project_name(self, container: RPModelElement) -> str:
        """Walk owner chain to find the Project; return its name, or '' if not found."""
        current: Optional[RPModelElement] = container
        visited: Set[int] = set()
        max_depth = 1000
        depth = 0
        while current is not None:
            depth += 1
            if depth > max_depth:
                break
            try:
                meta = current.get_meta_class()
            except Exception:
                break
            if meta == "Project":
                try:
                    return current.get_name()
                except Exception:
                    return ""
            try:
                key = id(current._com) if hasattr(current, "_com") else id(current)
            except Exception:
                break
            if key in visited:
                break  # cycle guard
            visited.add(key)
            try:
                current = current.get_owner()
            except Exception:
                break
        return ""

    def _find_element_by_name(self, container: RPModelElement, name: str) -> Optional[RPModelElement]:
        """Recursively search container's nested elements for one with matching name."""
        try:
            children = container.get_nested_elements()
        except Exception:
            return None
        for child in children:
            try:
                if child.get_name() == name:
                    return child  # type: ignore[no-any-return]
            except Exception:
                continue
            result = self._find_element_by_name(child, name)
            if result is not None:
                return result
        return None
