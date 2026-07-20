# YAML Import/Export for Rhapsody Models

**Status:** Design (awaiting review)
**Date:** 2026-07-19
**Author:** brainstorming session
**Reference:** `../py-zcu-mate` (rhapsody_generator/rhapsody/ — rough implementation)

## 1. Goal

Add YAML-based import/export to `rhapsody-cli` for round-tripping Rhapsody model structure (packages, classes, operations, attributes, types, etc.) without requiring Rhapsody's native `.sbs`/`.rpy` binary format.

**Round-trip only.** Template features (ARXML import, `for_each` loops, variable substitution) from `py-zcu-mate` are explicitly out of scope.

## 2. YAML Schema

### 2.1 Top-level structure

```yaml
version: 1
project: "MyProject"
rhapsody-model:
  - <element spec>
  - <element spec>
```

| Field | Type | Description |
|---|---|---|
| `version` | int | Schema format version. v1 importer rejects other values. |
| `project` | str | Source project name (metadata, recorded on export). |
| `rhapsody-model` | list[dict] | Top-level elements (children of the project root or import target package). |

### 2.2 Element spec (common fields)

Every element spec supports these common fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | str | yes | Element name |
| `type` | str | yes | Rhapsody metaclass name (`Package`, `Class`, `Operation`, `Attribute`, `Argument`, `Type`, `Object`, `EnumerationLiteral`, `Dependency`, `Generalization`, `Relation`, `Port`, `Event`, `EventReception`) |
| `stereotypes` | list[str] | no | Stereotype names; `meta_type` inferred from element's `type` |
| `tags` | dict[str, str] | no | Tag name → value; tags created locally if missing |
| `children` | list[dict] | no | Generic child elements (for `Package`, `Class`, `Type` with `kind: Structure`; also holds `Port`, `EventReception`, `Dependency`, `Generalization`, `Relation` under their owner) |

### 2.3 Type-specific fields

| Element type | Field | Type | Notes |
|---|---|---|---|
| `Type` | `kind` | str | `Enumeration` / `Structure` / `Language` (discriminator; required to hold typed children) |
| `Type` (Enumeration) | `literals` | list[dict] | EnumerationLiteral specs (no `type` field needed; implied) |
| `Operation` | `return_type` | str | Name of return classifier |
| `Operation` | `is_static` | bool | Static operation flag |
| `Operation` | `arguments` | list[dict] | Argument specs (no `type` field needed; implied) |
| `Attribute` | `data_type` | str | Name of attribute's type |
| `Attribute` | `visibility` | str | `public`/`protected`/`private` |
| `Attribute` | `multiplicity` | str | e.g. `1`, `0..*` |
| `Attribute` | `is_static` | bool | Static attribute flag |
| `Argument` | `data_type` | str | Name of argument's type |
| `Argument` | `direction` | str | `in`/`out`/`inout` (renamed from `argument_direction` for brevity) |
| `Object` | `classifier` | str | Name of the class this object instantiates |
| `Dependency` | `depends_on` | str | Name of target classifier (source is implied by parent) |
| `Generalization` | `base_class` | str | Name of superclass (derived class is implied by parent) |
| `Generalization` | `visibility` | str | `public`/`protected`/`private` |
| `Generalization` | `is_virtual` | bool | Virtual inheritance flag |
| `Relation` | `relation_type` | str | `Association` / `Aggregation` / `Composition` (required discriminator) |
| `Relation` | `from` | str | Name of source classifier (optional; defaults to parent) |
| `Relation` | `to` | str | Name of target classifier (required) |
| `Relation` | `multiplicity` | str | e.g. `1`, `0..*` |
| `Relation` | `is_navigable` | bool | Navigability flag |
| `Relation` | `role` | str | Role name on the source side (`relation_role_name` in Java API) |
| `Relation` | `visibility` | str | `public`/`protected`/`private` |
| `Port` | `is_behavioral` | bool | Behavioral port flag |
| `Port` | `is_reversed` | bool | Reversed port flag |
| `Port` | `contract` | str | Name of port's contract classifier (the interface/classifier the port exposes — Rhapsody's `IRPPort.setContract`/`getContract`) |
| `Port` | `provided_interfaces` | list[str] | Names of provided interfaces |
| `Port` | `required_interfaces` | list[str] | Names of required interfaces |
| `Event` | `base_event` | str | Optional name of base event |
| `Event` | `super_event` | str | Optional name of super event |
| `EventReception` | `event` | str | Name of referenced event |

### 2.4 Example

```yaml
version: 1
project: "MyProject"
rhapsody-model:
  - name: "Pkg1"
    type: "Package"
    stereotypes: ["SwComponent"]
    tags:
      TableLayoutForRecovery: "TableLayout_X"
    children:
      - name: "MyClass"
        type: "Class"
        stereotypes: ["Interface"]
        children:
          - name: "count"
            type: "Attribute"
            data_type: "int"
            visibility: "public"
            multiplicity: "1"
          - name: "reset"
            type: "Operation"
            return_type: "void"
            is_static: true
            arguments:
              - name: "newValue"
                data_type: "int"
                direction: "in"
          - name: "Color"
            type: "Type"
            kind: "Enumeration"
            literals:
              - name: "RED"
              - name: "GREEN"
              - name: "BLUE"
          - name: "Point"
            type: "Type"
            kind: "Structure"
            children:
              - name: "x"
                type: "Attribute"
                data_type: "int"
          # Port on MyClass
          - name: "p1"
            type: "Port"
            contract: "IFoo"
            is_behavioral: true
            provided_interfaces: ["IFoo"]
            required_interfaces: ["IBar"]
          # MyClass depends on OtherClass
          - name: "dep1"
            type: "Dependency"
            depends_on: "OtherClass"
          # MyClass inherits from BaseClass
          - name: "gen1"
            type: "Generalization"
            base_class: "BaseClass"
            visibility: "public"
          # Association from MyClass to OtherClass
          - name: "assoc1"
            type: "Relation"
            relation_type: "Association"
            to: "OtherClass"
            multiplicity: "0..*"
            is_navigable: true
          # Reception for an event
          - name: "onTick"
            type: "EventReception"
            event: "TickEvent"
      - name: "myObj"
        type: "Object"
        classifier: "MyClass"
      # Event at package level (referenced by receptions)
      - name: "TickEvent"
        type: "Event"
```

### 2.5 Improvements over `py-zcu-mate` schema

| Change | Rationale |
|---|---|
| `structure` → `rhapsody-model` | Clearer intent |
| Added `version: 1` | Future schema evolution signal |
| Added `project: "..."` | Records source project as metadata |
| `stereotypes[].meta_type` dropped | Redundant — inferred from element's `type` |
| `argument_direction` → `direction` | Shorter; unambiguous inside `arguments:` |
| `Operation.arguments` (not generic `children: [{type: Argument}]`) | Matches `IRPOperation.getArguments()` containment; Argument "belongs to" its Operation |
| `Type.kind` discriminator | Required — `AddNewAggr("Type", name)` defaults to Language (can't hold Attributes/EnumerationLiterals) |
| `Type.literals` for Enumeration | Matches `IRPType` (kind=Enumeration) containment of `IRPEnumerationLiteral` |
| Root wrapping + `--skip-root-package` dropped | Export writes children of target container directly; import target supplies the container |
| Added `visibility`, `multiplicity`, `is_static` | Reflects `IRPAttribute`/`IRPOperation` Java API properties for faithful round-trip |

## 3. Architecture

### 3.1 Module layout

```
src/rhapsody_cli/
├── exchange/                       # NEW — YAML import/export logic
│   ├── __init__.py                 # exports RhapsodyImporter, RhapsodyExporter, RhapsodyYaml, SCHEMA_VERSION
│   ├── core.py                     # RhapsodyModelHelper (base class)
│   ├── importer.py                 # RhapsodyImporter(RhapsodyModelHelper)
│   ├── exporter.py                 # RhapsodyExporter(RhapsodyModelHelper)
│   ├── schema.py                   # SCHEMA_VERSION, key constants
│   └── yaml_utils.py               # RhapsodyYaml class with read/write methods
├── actions/
│   ├── project_action.py           # MODIFIED — add ProjectImportAction, ProjectExportAction
│   └── package_action.py           # MODIFIED — add PackageImportAction, PackageExportAction
└── commands/
    ├── project_command.py          # MODIFIED — add Import/Export to get_actions()
    └── package_command.py          # MODIFIED — add Import/Export to get_actions()
```

No modification to `AbstractCommand`, `main()`, or any model class.

### 3.2 Layering

| Layer | Responsibility |
|---|---|
| `RhapsodyModelHelper` | Reusable model manipulation: `find_or_create_<type>`, `apply_stereotypes`/`apply_tags`, `resolve_classifier`, `find_child_by_name` (public); `_set_type_kind`, `_collect_children`, `_get_project_name` (private) |
| `RhapsodyImporter` / `RhapsodyExporter` | YAML-specific orchestration: dispatch to helper methods, apply type-specific extras, recurse children, build/parse YAML dict |
| `*Action` classes | CLI arg parsing, file I/O, path resolution (reuses existing `AbstractPackageAction._resolve_and_validate_package`), connection handling, call exchange module |

## 4. Components

### 4.1 `RhapsodyModelHelper` (base class)

Location: `src/rhapsody_cli/exchange/core.py`

Reusable model manipulation utilities. Takes `app` in constructor for lazy connection. Methods are reusable across the whole project (not just import/export).

```python
class RhapsodyModelHelper:
    def __init__(self, app: Optional[RhapsodyApplication] = None):
        self.app = app or RhapsodyApplication.connect(attach_only=True)
        self.project: Optional[RPProject] = None

    # --- Element find/create (idempotent) ---
    def find_or_create_package(self, parent: RPModelElement, name: str) -> RPPackage: ...
    def find_or_create_class(self, parent: RPModelElement, name: str) -> RPClass: ...
    def find_or_create_operation(self, parent: RPModelElement, name: str) -> RPOperation: ...
    def find_or_create_argument(self, parent: RPModelElement, name: str) -> RPArgument: ...
    def find_or_create_attribute(self, parent: RPModelElement, name: str) -> RPAttribute: ...
    def find_or_create_type(self, parent: RPModelElement, name: str, kind: Optional[str] = None) -> RPType: ...
    def find_or_create_object(self, parent: RPModelElement, name: str) -> RPInstance: ...
    def find_or_create_enumeration_literal(self, parent: RPModelElement, name: str) -> RPEnumerationLiteral: ...
    def find_or_create_dependency(self, parent: RPModelElement, name: str) -> RPDependency: ...
    def find_or_create_generalization(self, parent: RPModelElement, name: str) -> RPGeneralization: ...
    def find_or_create_relation(self, parent: RPModelElement, name: str) -> RPRelation: ...
    def find_or_create_port(self, parent: RPModelElement, name: str) -> RPPort: ...
    def find_or_create_event(self, parent: RPModelElement, name: str) -> RPEvent: ...
    def find_or_create_event_reception(self, parent: RPModelElement, name: str) -> RPEventReception: ...

    # --- Property application ---
    def apply_stereotypes(self, element: RPModelElement, stereotypes: List[str]) -> None: ...
    def apply_tags(self, element: RPModelElement, tags: Dict[str, str]) -> None: ...

    # --- Resolution ---
    def resolve_classifier(self, name: str) -> Optional[RPModelElement]: ...
    def get_classifier_name(self, classifier: RPModelElement) -> Optional[str]: ...

    # --- Public lookup ---
    def find_child_by_name(self, parent: RPModelElement, meta_class: str, name: str) -> Optional[RPModelElement]: ...

    # --- Private (exchange-specific internals) ---
    def _set_type_kind(self, type_element: RPType, kind: str) -> None: ...
    def _collect_children(self, container: RPModelElement) -> List[RPModelElement]: ...
    def _get_project_name(self, container: RPModelElement) -> str: ...
```

**Method behavior:**

- `find_or_create_<type>(parent, name)`:
  1. Call `find_child_by_name(parent, "<MetaClass>", name)`
  2. If found, return it; else create via `parent.add_new_aggr("<MetaClass>", name)` (or type-specific method)
  3. Special cases:
    - `find_or_create_package`: sanitize name (spaces → underscores) before creation
    - `find_or_create_operation`: if `parent.get_meta_class() == "Package"`, use `parent.add_global_function(name)` (Rhapsody stores global functions in a hidden TopLevel class)
    - `find_or_create_argument`: use `parent.add_argument(name)` (parent must be Operation)
    - `find_or_create_type`: if `kind` provided, call `self._set_type_kind(element, kind)` after creation
    - `find_or_create_dependency` / `find_or_create_generalization` / `find_or_create_relation` / `find_or_create_port` / `find_or_create_event` / `find_or_create_event_reception`: standard `add_new_aggr("<MetaClass>", name)`; no special creation logic. Source/target wiring happens in `_apply_<type>_extras` (importer side)

- `apply_stereotypes(element, stereotypes)`:
  - For each name: infer `meta_type` from `element.get_meta_class()`, call `element.add_stereotype(name, meta_type)` if not already applied
  - Reuses `py-zcu-mate`'s pattern but drops the redundant `meta_type` from the YAML

- `apply_tags(element, tags)`:
  - For each (name, value): find existing tag via `element.get_tag(name)`; if missing, create via `element.add_tag(name)`; then set value via `tag.set_value(value)`

- `find_child_by_name(parent, meta_class, name)`:
  - Iterate `parent.get_nested_elements()`; return the first child whose `get_meta_class() == meta_class` and `get_name() == name`
  - Returns `None` if not found

- `_set_type_kind(type_element, kind)`:
  - Calls `type_element.set_kind(kind)` (Java API: `IRPType.setKind(String)` — verified in `docs/java_api/.../IRPType.html`)
  - Required because `add_new_aggr("Type", name)` defaults to `Language`, which cannot hold `EnumerationLiteral` children or struct `Attribute` fields
  - Valid kinds: `Enumeration`, `Structure`, `Language`, `Typedef`, `Union`

- `_collect_children(container)`:
  - For `Package` containers: merge `get_nested_elements()` with package-level globals (`get_global_functions()`, `get_global_variables()`, `get_global_objects()`) since `getNestedElements()` excludes them
  - For other containers: return `list(container.get_nested_elements())`

- `_get_project_name(container)`:
  - Walk up the containment hierarchy via `get_owner()` until reaching an element with `get_meta_class() == "Project"`; return its name
  - Used to populate the YAML `project` field on export

### 4.2 `RhapsodyImporter`

Location: `src/rhapsody_cli/exchange/importer.py`

```python
class RhapsodyImporter(RhapsodyModelHelper):
    def import_template(self, data: dict, root_element: RPModelElement) -> None:
        """Import elements from `data["rhapsody-model"]` as children of `root_element`."""
        version = data.get("version")
        if version != SCHEMA_VERSION:
            raise CliExecutionError(f"Unsupported schema version: {version} (expected {SCHEMA_VERSION})")
        for spec in data.get("rhapsody-model", []):
            self._process_element(root_element, spec)

    def _process_element(self, parent: RPModelElement, spec: dict) -> Optional[RPModelElement]:
        element_type = spec["type"]
        name = spec["name"]

        # Dispatch to find_or_create_<type>
        if element_type == "Package":
            element = self.find_or_create_package(parent, name)
        elif element_type == "Class":
            element = self.find_or_create_class(parent, name)
        elif element_type == "Operation":
            element = self.find_or_create_operation(parent, name)
        elif element_type == "Attribute":
            element = self.find_or_create_attribute(parent, name)
        elif element_type == "Argument":
            element = self.find_or_create_argument(parent, name)
        elif element_type == "Type":
            element = self.find_or_create_type(parent, name, spec.get("kind"))
        elif element_type == "Object":
            element = self.find_or_create_object(parent, name)
        elif element_type == "EnumerationLiteral":
            element = self.find_or_create_enumeration_literal(parent, name)
        elif element_type == "Dependency":
            element = self.find_or_create_dependency(parent, name)
        elif element_type == "Generalization":
            element = self.find_or_create_generalization(parent, name)
        elif element_type == "Relation":
            element = self.find_or_create_relation(parent, name)
        elif element_type == "Port":
            element = self.find_or_create_port(parent, name)
        elif element_type == "Event":
            element = self.find_or_create_event(parent, name)
        elif element_type == "EventReception":
            element = self.find_or_create_event_reception(parent, name)
        else:
            logger.warning("Unsupported element type '%s'; skipping", element_type)
            return None

        # Common properties
        self.apply_stereotypes(element, spec.get("stereotypes", []))
        self.apply_tags(element, spec.get("tags", {}))

        # Type-specific extras
        if element_type == "Operation":
            self._apply_operation_extras(element, spec)
        elif element_type == "Attribute":
            self._apply_attribute_extras(element, spec)
        elif element_type == "Argument":
            self._apply_argument_extras(element, spec)
        elif element_type == "Type":
            self._apply_type_extras(element, spec)
        elif element_type == "Object":
            self._apply_object_extras(element, spec)
        elif element_type == "Dependency":
            self._apply_dependency_extras(element, spec, parent)
        elif element_type == "Generalization":
            self._apply_generalization_extras(element, spec, parent)
        elif element_type == "Relation":
            self._apply_relation_extras(element, spec, parent)
        elif element_type == "Port":
            self._apply_port_extras(element, spec)
        elif element_type == "Event":
            self._apply_event_extras(element, spec)
        elif element_type == "EventReception":
            self._apply_event_reception_extras(element, spec)

        # Generic children (Package, Class, Type with kind=Structure)
        if element_type in ("Package", "Class", "Type"):
            for child_spec in spec.get("children", []):
                self._process_element(element, child_spec)
        return element

    # Type-specific extras (YAML spec fields -> element property setters)
    def _apply_operation_extras(self, operation: RPOperation, spec: dict) -> None:
        if "return_type" in spec:
            classifier = self.resolve_classifier(spec["return_type"])
            if classifier is not None:
                operation.set_returns(classifier)
            else:
                logger.warning("Cannot resolve return_type '%s' for operation '%s'",
                               spec["return_type"], operation.get_name())
        if "is_static" in spec and hasattr(operation, "set_is_static"):
            operation.set_is_static(spec["is_static"])
        # Arguments (Operation-specific child field)
        for arg_spec in spec.get("arguments", []):
            arg = self.find_or_create_argument(operation, arg_spec["name"])
            self._apply_argument_extras(arg, arg_spec)

    def _apply_argument_extras(self, arg: RPArgument, spec: dict) -> None:
        if "data_type" in spec:
            classifier = self.resolve_classifier(spec["data_type"])
            if classifier is not None:
                arg.set_type(classifier)
            else:
                logger.warning("Cannot resolve data_type '%s' for argument '%s'",
                               spec["data_type"], arg.get_name())
        if "direction" in spec and hasattr(arg, "set_argument_direction"):
            arg.set_argument_direction(spec["direction"])
        # Common properties (parity with _process_element path)
        self.apply_stereotypes(arg, spec.get("stereotypes", []))
        self.apply_tags(arg, spec.get("tags", {}))

    def _apply_attribute_extras(self, attr: RPAttribute, spec: dict) -> None:
        if "data_type" in spec:
            classifier = self.resolve_classifier(spec["data_type"])
            if classifier is not None:
                attr.set_type(classifier)
        if "visibility" in spec and hasattr(attr, "set_visibility"):
            attr.set_visibility(spec["visibility"])
        if "multiplicity" in spec and hasattr(attr, "set_multiplicity"):
            attr.set_multiplicity(spec["multiplicity"])
        if "is_static" in spec and hasattr(attr, "set_is_static"):
            attr.set_is_static(spec["is_static"])

    def _apply_type_extras(self, type_element: RPType, spec: dict) -> None:
        # kind already applied in find_or_create_type via self._set_type_kind
        if spec.get("kind") == "Enumeration":
            for literal_spec in spec.get("literals", []):
                literal = self.find_or_create_enumeration_literal(type_element, literal_spec["name"])
                # Common properties on each literal (parity with _process_element path)
                self.apply_stereotypes(literal, literal_spec.get("stereotypes", []))
                self.apply_tags(literal, literal_spec.get("tags", {}))

    def _apply_object_extras(self, obj: RPInstance, spec: dict) -> None:
        if "classifier" in spec:
            classifier = self.resolve_classifier(spec["classifier"])
            if classifier is not None and hasattr(obj, "set_classifier"):
                obj.set_classifier(classifier)
            else:
                logger.warning("Cannot resolve classifier '%s' for object '%s'",
                               spec["classifier"], obj.get_name())

    def _apply_dependency_extras(self, dependency: RPDependency, spec: dict, parent: RPModelElement) -> None:
        # Source (dependent) is the parent that owns this dependency
        if hasattr(dependency, "set_dependent"):
            dependency.set_dependent(parent)
        if "depends_on" in spec:
            target = self.resolve_classifier(spec["depends_on"])
            if target is not None and hasattr(dependency, "set_depends_on"):
                dependency.set_depends_on(target)
            else:
                logger.warning("Cannot resolve depends_on '%s' for dependency '%s'",
                               spec["depends_on"], dependency.get_name())

    def _apply_generalization_extras(self, generalization: RPGeneralization, spec: dict, parent: RPModelElement) -> None:
        # Source (derived_class) is the parent that owns this generalization
        if hasattr(generalization, "set_derived_class"):
            generalization.set_derived_class(parent)
        if "base_class" in spec:
            target = self.resolve_classifier(spec["base_class"])
            if target is not None and hasattr(generalization, "set_base_class"):
                generalization.set_base_class(target)
            else:
                logger.warning("Cannot resolve base_class '%s' for generalization '%s'",
                               spec["base_class"], generalization.get_name())
        if "visibility" in spec and hasattr(generalization, "set_visibility"):
            generalization.set_visibility(spec["visibility"])
        if "is_virtual" in spec and hasattr(generalization, "set_is_virtual"):
            generalization.set_is_virtual(spec["is_virtual"])

    def _apply_relation_extras(self, relation: RPRelation, spec: dict, parent: RPModelElement) -> None:
        # Source (of_class) defaults to parent; spec["from"] overrides
        if "from" in spec:
            source = self.resolve_classifier(spec["from"])
            if source is None:
                logger.warning("Cannot resolve from '%s' for relation '%s'; using parent",
                               spec["from"], relation.get_name())
                source = parent
        else:
            source = parent
        if hasattr(relation, "set_of_class"):
            relation.set_of_class(source)
        if "to" in spec:
            target = self.resolve_classifier(spec["to"])
            if target is not None and hasattr(relation, "set_other_class"):
                relation.set_other_class(target)
            else:
                logger.warning("Cannot resolve to '%s' for relation '%s'",
                               spec["to"], relation.get_name())
        if "relation_type" in spec and hasattr(relation, "set_relation_type"):
            relation.set_relation_type(spec["relation_type"])
        if "multiplicity" in spec and hasattr(relation, "set_multiplicity"):
            relation.set_multiplicity(spec["multiplicity"])
        if "is_navigable" in spec and hasattr(relation, "set_is_navigable"):
            relation.set_is_navigable(spec["is_navigable"])
        if "role" in spec and hasattr(relation, "set_relation_role_name"):
            relation.set_relation_role_name(spec["role"])
        if "visibility" in spec and hasattr(relation, "set_visibility"):
            relation.set_visibility(spec["visibility"])

    def _apply_port_extras(self, port: RPPort, spec: dict) -> None:
        if "is_behavioral" in spec and hasattr(port, "set_is_behavioral"):
            port.set_is_behavioral(spec["is_behavioral"])
        if "is_reversed" in spec and hasattr(port, "set_is_reversed"):
            port.set_is_reversed(spec["is_reversed"])
        if "contract" in spec:
            classifier = self.resolve_classifier(spec["contract"])
            if classifier is not None and hasattr(port, "set_contract"):
                port.set_contract(classifier)
            else:
                logger.warning("Cannot resolve contract '%s' for port '%s'",
                               spec["contract"], port.get_name())
        for iface_name in spec.get("provided_interfaces", []):
            iface = self.resolve_classifier(iface_name)
            if iface is not None and hasattr(port, "add_provided_interface"):
                port.add_provided_interface(iface)
            else:
                logger.warning("Cannot resolve provided_interface '%s' for port '%s'",
                               iface_name, port.get_name())
        for iface_name in spec.get("required_interfaces", []):
            iface = self.resolve_classifier(iface_name)
            if iface is not None and hasattr(port, "add_required_interface"):
                port.add_required_interface(iface)
            else:
                logger.warning("Cannot resolve required_interface '%s' for port '%s'",
                               iface_name, port.get_name())

    def _apply_event_extras(self, event: RPEvent, spec: dict) -> None:
        if "base_event" in spec:
            target = self.resolve_classifier(spec["base_event"])
            if target is not None and hasattr(event, "set_base_event"):
                event.set_base_event(target)
            else:
                logger.warning("Cannot resolve base_event '%s' for event '%s'",
                               spec["base_event"], event.get_name())
        if "super_event" in spec:
            target = self.resolve_classifier(spec["super_event"])
            if target is not None and hasattr(event, "set_super_event"):
                event.set_super_event(target)
            else:
                logger.warning("Cannot resolve super_event '%s' for event '%s'",
                               spec["super_event"], event.get_name())

    def _apply_event_reception_extras(self, reception: RPEventReception, spec: dict) -> None:
        if "event" in spec:
            target = self.resolve_classifier(spec["event"])
            if target is not None and hasattr(reception, "set_event"):
                reception.set_event(target)
            else:
                logger.warning("Cannot resolve event '%s' for reception '%s'",
                               spec["event"], reception.get_name())
```

### 4.3 `RhapsodyExporter`

Location: `src/rhapsody_cli/exchange/exporter.py`

```python
class RhapsodyExporter(RhapsodyModelHelper):
    def export(self, container: RPModelElement) -> dict:
        """Export children of `container` (project root or package) as a YAML dict."""
        children = self._collect_children(container)
        return {
            "version": SCHEMA_VERSION,
            "project": self._get_project_name(container),
            "rhapsody-model": [
                result for result in (self._export_element(c) for c in children)
                if result is not None
            ],
        }

    def _export_element(self, element: RPModelElement) -> Optional[dict]:
        element_type = element.get_meta_class()
        if element_type == "Package":
            result = self._export_package(element)
        elif element_type == "Class":
            result = self._export_class(element)
        elif element_type == "Operation":
            result = self._export_operation(element)
        elif element_type == "Attribute":
            result = self._export_attribute(element)
        elif element_type == "Argument":
            result = self._export_argument(element)
        elif element_type == "Type":
            result = self._export_type(element)
        elif element_type == "Object":
            result = self._export_object(element)
        elif element_type == "EnumerationLiteral":
            result = self._export_enumeration_literal(element)
        elif element_type == "Dependency":
            result = self._export_dependency(element)
        elif element_type == "Generalization":
            result = self._export_generalization(element)
        elif element_type == "Relation":
            result = self._export_relation(element)
        elif element_type == "Port":
            result = self._export_port(element)
        elif element_type == "Event":
            result = self._export_event(element)
        elif element_type == "EventReception":
            result = self._export_event_reception(element)
        else:
            logger.warning("Unsupported metaclass '%s' on '%s'; skipping",
                           element_type, element.get_name())
            return None

        # Common: stereotypes, tags
        stereotypes = self._export_stereotypes(element)
        if stereotypes:
            result["stereotypes"] = stereotypes
        tags = self._export_tags(element)
        if tags:
            result["tags"] = tags
        return result

    # --- Type-specific exporters ---
    def _export_package(self, pkg: RPPackage) -> dict:
        result = {"name": pkg.get_name(), "type": "Package"}
        children = self._collect_children(pkg)
        if children:
            result["children"] = [
                r for r in (self._export_element(c) for c in children) if r is not None
            ]
        return result

    def _export_class(self, cls: RPClass) -> dict:
        result = {"name": cls.get_name(), "type": "Class"}
        children = self._collect_children(cls)
        if children:
            result["children"] = [
                r for r in (self._export_element(c) for c in children) if r is not None
            ]
        return result

    def _export_operation(self, op: RPOperation) -> dict:
        result = {"name": op.get_name(), "type": "Operation"}
        return_type = self.get_classifier_name(op.get_returns()) if hasattr(op, "get_returns") else None
        if return_type:
            result["return_type"] = return_type
        if hasattr(op, "get_is_static"):
            result["is_static"] = op.get_is_static()
        arguments = list(op.get_arguments()) if hasattr(op, "get_arguments") else []
        if arguments:
            # Route through _export_element so arguments also pick up stereotypes/tags
            result["arguments"] = [
                r for r in (self._export_element(a) for a in arguments) if r is not None
            ]
        return result

    def _export_argument(self, arg: RPArgument) -> dict:
        result = {"name": arg.get_name(), "type": "Argument"}
        data_type = self.get_classifier_name(arg.get_type()) if hasattr(arg, "get_type") else None
        if data_type:
            result["data_type"] = data_type
        if hasattr(arg, "get_argument_direction"):
            direction = arg.get_argument_direction()
            if direction:
                result["direction"] = direction
        return result

    def _export_attribute(self, attr: RPAttribute) -> dict:
        result = {"name": attr.get_name(), "type": "Attribute"}
        data_type = self.get_classifier_name(attr.get_type()) if hasattr(attr, "get_type") else None
        if data_type:
            result["data_type"] = data_type
        if hasattr(attr, "get_visibility"):
            result["visibility"] = attr.get_visibility()
        if hasattr(attr, "get_multiplicity"):
            multiplicity = attr.get_multiplicity()
            if multiplicity:
                result["multiplicity"] = multiplicity
        if hasattr(attr, "get_is_static"):
            result["is_static"] = attr.get_is_static()
        return result

    def _export_type(self, type_element: RPType) -> dict:
        result = {"name": type_element.get_name(), "type": "Type"}
        kind = type_element.get_kind() if hasattr(type_element, "get_kind") else None
        if kind:
            result["kind"] = kind
        if kind == "Enumeration":
            literals = list(type_element.get_enumeration_literals()) if hasattr(type_element, "get_enumeration_literals") else []
            if literals:
                # Route through _export_element so literals also pick up stereotypes/tags
                result["literals"] = [
                    r for r in (self._export_element(l) for l in literals) if r is not None
                ]
        else:
            # Structure or Language: use generic children
            children = self._collect_children(type_element)
            if children:
                result["children"] = [
                    r for r in (self._export_element(c) for c in children) if r is not None
                ]
        return result

    def _export_object(self, obj: RPInstance) -> dict:
        result = {"name": obj.get_name(), "type": "Object"}
        classifier = obj.get_classifier() if hasattr(obj, "get_classifier") else None
        if classifier is not None:
            classifier_name = self.get_classifier_name(classifier)
            if classifier_name:
                result["classifier"] = classifier_name
        return result

    def _export_enumeration_literal(self, literal: RPEnumerationLiteral) -> dict:
        return {"name": literal.get_name(), "type": "EnumerationLiteral"}

    def _export_dependency(self, dependency: RPDependency) -> dict:
        result = {"name": dependency.get_name(), "type": "Dependency"}
        # Source (dependent) is the owning parent — not emitted.
        # Only the target (depends_on) is serialized.
        target = dependency.get_depends_on() if hasattr(dependency, "get_depends_on") else None
        if target is not None:
            target_name = self.get_classifier_name(target)
            if target_name:
                result["depends_on"] = target_name
        return result

    def _export_generalization(self, generalization: RPGeneralization) -> dict:
        result = {"name": generalization.get_name(), "type": "Generalization"}
        # Source (derived_class) is the owning parent — not emitted.
        # Only the target (base_class) is serialized.
        base = generalization.get_base_class() if hasattr(generalization, "get_base_class") else None
        if base is not None:
            base_name = self.get_classifier_name(base)
            if base_name:
                result["base_class"] = base_name
        if hasattr(generalization, "get_visibility"):
            visibility = generalization.get_visibility()
            if visibility:
                result["visibility"] = visibility
        if hasattr(generalization, "get_is_virtual"):
            result["is_virtual"] = generalization.get_is_virtual()
        return result

    def _export_relation(self, relation: RPRelation) -> dict:
        result = {"name": relation.get_name(), "type": "Relation"}
        if hasattr(relation, "get_relation_type"):
            relation_type = relation.get_relation_type()
            if relation_type:
                result["relation_type"] = relation_type
        # Source (of_class). Defaults to parent on import; emit `from` only when
        # the stored source name is resolvable (covers cross-classifier overrides).
        source = relation.get_of_class() if hasattr(relation, "get_of_class") else None
        if source is not None:
            source_name = self.get_classifier_name(source)
            if source_name:
                result["from"] = source_name
        # Target (other_class) — required.
        target = relation.get_other_class() if hasattr(relation, "get_other_class") else None
        if target is not None:
            target_name = self.get_classifier_name(target)
            if target_name:
                result["to"] = target_name
        if hasattr(relation, "get_multiplicity"):
            multiplicity = relation.get_multiplicity()
            if multiplicity:
                result["multiplicity"] = multiplicity
        if hasattr(relation, "get_is_navigable"):
            result["is_navigable"] = relation.get_is_navigable()
        if hasattr(relation, "get_relation_role_name"):
            role = relation.get_relation_role_name()
            if role:
                result["role"] = role
        if hasattr(relation, "get_visibility"):
            visibility = relation.get_visibility()
            if visibility:
                result["visibility"] = visibility
        return result

    def _export_port(self, port: RPPort) -> dict:
        result = {"name": port.get_name(), "type": "Port"}
        if hasattr(port, "get_is_behavioral"):
            result["is_behavioral"] = port.get_is_behavioral()
        if hasattr(port, "get_is_reversed"):
            result["is_reversed"] = port.get_is_reversed()
        contract = port.get_contract() if hasattr(port, "get_contract") else None
        if contract is not None:
            contract_name = self.get_classifier_name(contract)
            if contract_name:
                result["contract"] = contract_name
        if hasattr(port, "get_provided_interfaces"):
            provided = [
                n for n in (self.get_classifier_name(i) for i in port.get_provided_interfaces() if i is not None)
                if n
            ]
            if provided:
                result["provided_interfaces"] = provided
        if hasattr(port, "get_required_interfaces"):
            required = [
                n for n in (self.get_classifier_name(i) for i in port.get_required_interfaces() if i is not None)
                if n
            ]
            if required:
                result["required_interfaces"] = required
        return result

    def _export_event(self, event: RPEvent) -> dict:
        result = {"name": event.get_name(), "type": "Event"}
        base = event.get_base_event() if hasattr(event, "get_base_event") else None
        if base is not None:
            base_name = self.get_classifier_name(base)
            if base_name:
                result["base_event"] = base_name
        sup = event.get_super_event() if hasattr(event, "get_super_event") else None
        if sup is not None:
            sup_name = self.get_classifier_name(sup)
            if sup_name:
                result["super_event"] = sup_name
        return result

    def _export_event_reception(self, reception: RPEventReception) -> dict:
        result = {"name": reception.get_name(), "type": "EventReception"}
        evt = reception.get_event() if hasattr(reception, "get_event") else None
        if evt is not None:
            evt_name = self.get_classifier_name(evt)
            if evt_name:
                result["event"] = evt_name
        return result

    # --- Common property exporters ---
    def _export_stereotypes(self, element: RPModelElement) -> List[str]:
        stereotypes = element.get_stereotypes() if hasattr(element, "get_stereotypes") else None
        if not stereotypes:
            return []
        return [s.get_name() for s in stereotypes if s is not None]

    def _export_tags(self, element: RPModelElement) -> Dict[str, str]:
        tags = element.get_tags() if hasattr(element, "get_tags") else None
        if not tags:
            return {}
        result: Dict[str, str] = {}
        for tag in tags:
            try:
                name = tag.get_name()
                value = tag.get_value()
                if name and value is not None:
                    result[name] = str(value)
            except Exception:
                continue
        return result
```

### 4.4 CLI Actions

Four new actions added to existing action modules. No new command files.

#### `ProjectExportAction` / `ProjectImportAction`

Added to `src/rhapsody_cli/actions/project_action.py`. Inherit from `RhapsodyContextAction` (existing pattern for project actions).

```python
class ProjectExportAction(RhapsodyContextAction):
    """Export the active project's top-level elements to YAML.

    SWR_XCH_001: Project Export
    """
    command_id = "export"

    def init_arguments(self, sub_parser: argparse.ArgumentParser) -> None:
        sub_parser.add_argument("--output", required=True, help="Output YAML file path")

    def execute(self, args: argparse.Namespace) -> None:
        app = self._connect_app()
        project = app.get_active_project()
        exporter = RhapsodyExporter(app=app)
        data = exporter.export(project)
        RhapsodyYaml().write(args.output, data)
        self._print_success(f"Exported project '{project.get_name()}' to {args.output}")


class ProjectImportAction(RhapsodyContextAction):
    """Import YAML elements as top-level elements of the active project.

    SWR_XCH_002: Project Import
    """
    command_id = "import"

    def init_arguments(self, sub_parser: argparse.ArgumentParser) -> None:
        sub_parser.add_argument("--input", required=True, help="Input YAML file path")
        sub_parser.add_argument("--no-save", action="store_true", help="Skip saving after import")

    def execute(self, args: argparse.Namespace) -> None:
        app = self._connect_app()
        project = app.get_active_project()
        data = RhapsodyYaml().read(args.input)
        importer = RhapsodyImporter(app=app)
        importer.import_template(data, root_element=project)
        if not args.no_save:
            app.save_all()
        self._print_success(f"Imported {args.input} into project '{project.get_name()}'")
```

#### `PackageExportAction` / `PackageImportAction`

Added to `src/rhapsody_cli/actions/package_action.py`. Inherit from `AbstractPackageAction` (reuses `_resolve_and_validate_package`).

```python
class PackageExportAction(AbstractPackageAction):
    """Export a package's contents to YAML.

    SWR_XCH_003: Package Export
    """
    command_id = "export"

    def init_arguments(self, sub_parser: argparse.ArgumentParser) -> None:
        sub_parser.add_argument("--package", required=True, help="Package path (e.g. Root/Sub)")
        sub_parser.add_argument("--output", required=True, help="Output YAML file path")

    def execute(self, args: argparse.Namespace) -> None:
        app = self._connect_app()
        target = self._resolve_and_validate_package(args.package)
        exporter = RhapsodyExporter(app=app)
        data = exporter.export(target)
        RhapsodyYaml().write(args.output, data)
        self._print_success(f"Exported package '{args.package}' to {args.output}")


class PackageImportAction(AbstractPackageAction):
    """Import YAML elements as children of a specific package.

    SWR_XCH_004: Package Import
    """
    command_id = "import"

    def init_arguments(self, sub_parser: argparse.ArgumentParser) -> None:
        sub_parser.add_argument("--input", required=True, help="Input YAML file path")
        sub_parser.add_argument("--package", required=True, help="Target package path")
        sub_parser.add_argument("--no-save", action="store_true", help="Skip saving after import")

    def execute(self, args: argparse.Namespace) -> None:
        app = self._connect_app()
        target = self._resolve_and_validate_package(args.package)
        data = RhapsodyYaml().read(args.input)
        importer = RhapsodyImporter(app=app)
        importer.import_template(data, root_element=target)
        if not args.no_save:
            app.save_all()
        self._print_success(f"Imported {args.input} into package '{args.package}'")
```

#### `RhapsodyYaml` I/O class

A single class in `exchange/yaml_utils.py` exposing only `read` and `write` methods. Stateless (no `__init__` arguments); instances are cheap to create. Wraps PyYAML's `safe_load` / `safe_dump` and translates errors to `CliExecutionError`.

```python
class RhapsodyYaml:
    """YAML file I/O helper. Translates PyYAML errors to CliExecutionError."""

    def read(self, path: str) -> dict:
        """Read and parse a YAML file.

        Args:
            path: Path to the YAML file.

        Returns:
            Parsed YAML mapping as a dict.

        Raises:
            CliExecutionError: If file is missing, YAML is invalid, or top-level
                value is not a mapping.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            raise CliExecutionError(f"Input file not found: {path}")
        except yaml.YAMLError as e:
            raise CliExecutionError(f"Invalid YAML in {path}: {e}")
        if not isinstance(data, dict):
            raise CliExecutionError(f"Expected YAML mapping at top level of {path}")
        return data

    def write(self, path: str, data: dict) -> None:
        """Write a dict to a YAML file.

        Args:
            path: Output file path.
            data: Dict to serialize.

        Raises:
            CliExecutionError: If the file cannot be written.
        """
        try:
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        except OSError as e:
            raise CliExecutionError(f"Failed to write {path}: {e}")
```

**Usage in actions:**

```python
yaml_io = RhapsodyYaml()
data = yaml_io.read(args.input)        # import side
yaml_io.write(args.output, data)       # export side
```

#### Command registration

`ProjectCommand.get_actions()` (in `commands/project_command.py`) — append:

```python
return [
    ProjectOpenAction(),
    ProjectListAction(),
    ProjectCloseAction(),
    ProjectNewAction(),
    ProjectExportAction(),   # NEW
    ProjectImportAction(),   # NEW
]
```

`PackageCommand.get_actions()` (in `commands/package_command.py`) — append:

```python
return [
    PackageCreateAction(),
    PackageDeleteAction(),
    PackageViewAction(),
    PackageListAction(),
    PackageUpdateAction(),
    PackageExportAction(),   # NEW
    PackageImportAction(),   # NEW
]
```

## 5. CLI Commands

| Command | Args | Behavior |
|---|---|---|
| `rhapsody-cli project export` | `--output <file>` | Export active project's top-level elements to YAML |
| `rhapsody-cli project import` | `--input <file>` `[--no-save]` | Import YAML elements as top-level elements of active project |
| `rhapsody-cli package export` | `--package <path>` `--output <file>` | Export a specific package's contents to YAML |
| `rhapsody-cli package import` | `--input <file>` `--package <path>` `[--no-save]` | Import YAML elements as children of a specific package |

Global flags `-v`/`--verbose` and `--format` work as usual (no format-specific output — these commands print success/error messages only).

**Project vs. Package distinction**: Since `RPProject extends RPPackage`, the project IS the root package. `project import/export` operates on the project root (no `--package` arg); `package import/export` operates on a specific package path (requires `--package`). Both call the same `RhapsodyExporter.export(container)` / `RhapsodyImporter.import_template(data, root_element)` API; only the container resolution differs.

## 6. Data Flow

### 6.1 Export

```
rhapsody-cli package export --package Root/Sub --output model.yaml
  |
  v
PackageExportAction.execute(args)
  |- app = self._connect_app()
  |- target = self._resolve_and_validate_package("Root/Sub")  # reuses existing helper
  |- exporter = RhapsodyExporter(app=app)
  |- data = exporter.export(target)
  |     |- children = self._collect_children(target)  # includes package globals
  |     |- for each child: self._export_element(child)
  |     |     |- dispatch on child.get_meta_class() -> _export_<type>
  |     |     |- _export_<type> serializes type-specific fields
  |     |     |   (e.g. _export_operation emits return_type + arguments)
  |     |     '- _export_stereotypes / _export_tags (common)
  |     '- return {"version": 1, "project": ..., "rhapsody-model": [...]}
  '- RhapsodyYaml().write("model.yaml", data)
```

### 6.2 Import

```
rhapsody-cli package import --input model.yaml --package Root/Target
  |
  v
PackageImportAction.execute(args)
  |- app = self._connect_app()
  |- target = self._resolve_and_validate_package("Root/Target")
  |- data = RhapsodyYaml().read("model.yaml")
  |- importer = RhapsodyImporter(app=app)
  |- importer.import_template(data, root_element=target)
  |     |- validate version == SCHEMA_VERSION
  |     '- for each spec in data["rhapsody-model"]:
  |           self._process_element(target, spec)
  |             |- dispatch on spec["type"] -> find_or_create_<type>(target, spec["name"])
  |             |- self.apply_stereotypes(element, spec.get("stereotypes"))
  |             |- self.apply_tags(element, spec.get("tags"))
  |             |- dispatch on type -> _apply_<type>_extras(element, spec)
  |             |   (e.g. _apply_operation_extras sets return_type, is_static, creates arguments)
  |             '- for child_spec in spec.get("children"):
  |                   self._process_element(element, child_spec)  # recurse
  '- if not args.no_save: app.save_all()
```

## 7. Error Handling

| Condition | Behavior |
|---|---|
| Unsupported element type (e.g. `Activity`, `State`, `Transition`) | Exporter: emit WARNING, skip element (returns `None`, filtered out). Importer: emit WARNING, skip spec (returns `None`, siblings still processed). |
| Missing type reference (`data_type: "UnknownType"`) | Importer: emit WARNING, skip setting the type (element still created). |
| Missing relation target (`to`, `base_class`, `depends_on`) | Importer: emit WARNING, skip wiring the source/target (relation/dependency/generalization element still created without the link). |
| Missing port contract / interface name | Importer: emit WARNING, skip setting that contract/interface (port still created). |
| Missing event reference (`event`, `base_event`, `super_event`) | Importer: emit WARNING, skip setting the event link (reception/event still created). |
| Schema version mismatch | Importer: raise `CliExecutionError` with expected vs. actual version. |
| Invalid YAML syntax | `RhapsodyYaml.read`: raise `CliExecutionError` with file path and parser error. |
| Input file not found | `RhapsodyYaml.read`: raise `CliExecutionError("Input file not found: <path>")`. |
| Output file not writable | `RhapsodyYaml.write`: raise `CliExecutionError("Failed to write <path>: <error>")`. |
| No active project / Rhapsody | Reuses existing `_connect_app()` / `_resolve_and_validate_package()` error handling. |
| Package path not found | `_resolve_and_validate_package` raises `CliExecutionError` (existing behavior). |
| Type kind mismatch | Best-effort: if Type has `kind: Enumeration` but `children` contains Attributes, importer processes both `literals` and `children` (WARNING logged). |

All `CliExecutionError` instances propagate to `main()` which logs and exits with the error's `exit_code`. No `sys.exit()` calls in the exchange module or actions (per project convention).

## 8. Testing

### 8.1 Unit tests (CI-runnable, no real COM)

Location: `tests/unit/exchange/` and `tests/unit/actions/`

| File | Scope |
|---|---|
| `tests/unit/exchange/test_core.py` | `RhapsodyModelHelper` — `find_or_create_<type>` dispatch (all 14 types incl. `find_or_create_dependency`/`_generalization`/`_relation`/`_port`/`_event`/`_event_reception`), `find_child_by_name`, `_set_type_kind`, `apply_stereotypes`, `apply_tags`, `resolve_classifier`, `_collect_children` (with/without package globals), `_get_project_name` |
| `tests/unit/exchange/test_importer.py` | `RhapsodyImporter` — `import_template` (version check, dispatch), `_process_element` for each of the 14 element types, `_apply_<type>_extras` for each type (incl. source/target wiring for Dependency/Generalization/Relation, port contract/interface loops, event links), recursion, skip-on-unsupported |
| `tests/unit/exchange/test_exporter.py` | `RhapsodyExporter` — `export` (dict shape, `version`/`project`/`rhapsody-model` keys), `_export_element` for each of the 14 metaclasses, `_export_<type>` field coverage (incl. relation `from`/`to`/`relation_type`/`multiplicity`/`role`/`visibility`/`is_navigable`, port `is_behavioral`/`is_reversed`/`contract`/`provided_interfaces`/`required_interfaces`, event `base_event`/`super_event`, reception `event`), skip-on-unsupported |
| `tests/unit/exchange/test_schema.py` | `SCHEMA_VERSION` value, key constant sanity |
| `tests/unit/exchange/test_yaml_utils.py` | `RhapsodyYaml.read` / `RhapsodyYaml.write` — happy path, missing file, invalid YAML, round-trip |
| `tests/unit/actions/test_project_action.py` | `ProjectExportAction` / `ProjectImportAction` — arg parsing, file I/O, success message (extend existing file) |
| `tests/unit/actions/test_package_action.py` | `PackageExportAction` / `PackageImportAction` — arg parsing, package resolution, file I/O (extend existing file) |

All tests use `make_fake_element` / `make_fake_collection` from `tests/unit/models/fakes.py` (existing convention). **Never real COM in unit tests.**

### 8.2 Integration tests (Windows + Rhapsody only, auto-skipped in CI)

Location: `tests/integration/exchange/`

| File | Scope |
|---|---|
| `test_export_round_trip.py` | Create a project with packages/classes/operations/types, export to YAML, verify dict shape |
| `test_import_round_trip.py` | Import a YAML file into an empty package, verify elements created with correct properties |
| `test_export_import_round_trip.py` | Export -> clear -> import -> compare structure (true round-trip) |

### 8.3 TDD requirement

Per project convention: write failing test first, then implementation. Coverage target 80% min, 90%+ preferred.

### 8.4 Requirement IDs

Following project convention, allocate SWR IDs in `docs/requirements/`:

| ID | Title |
|---|---|
| SWR_XCH_001 | Project Export Command |
| SWR_XCH_002 | Project Import Command |
| SWR_XCH_003 | Package Export Command |
| SWR_XCH_004 | Package Import Command |
| SWR_XCH_005 | YAML Schema (version 1) |
| SWR_XCH_006 | Element Find-or-Create (RhapsodyModelHelper) |
| SWR_XCH_007 | Stereotype and Tag Round-Trip |
| SWR_XCH_008 | Core Type-Specific Fields (arguments, literals, kind, data_type, return_type, direction, classifier, visibility, multiplicity, is_static) |
| SWR_XCH_009 | Error Handling and Skip-on-Unsupported |
| SWR_XCH_010 | Reusable Model Manipulation API |
| SWR_XCH_011 | Relations Round-Trip (Dependency, Generalization, Relation — source/target wiring, relation_type, multiplicity, role, visibility, is_navigable, is_virtual) |
| SWR_XCH_012 | Ports Round-Trip (is_behavioral, is_reversed, contract, provided_interfaces, required_interfaces) |
| SWR_XCH_013 | Events and EventReceptions Round-Trip (base_event, super_event, event reference) |

Test case IDs in `docs/tests/unit/`: `UTS_XCH_00001`+ with `Traces-To` linking to SWR IDs.

## 9. Dependencies

Add `PyYAML>=6.0` to `pyproject.toml`:

```toml
[project]
dependencies = [
    "pywin32>=306; sys_platform == 'win32'",
    "PyYAML>=6.0",
]
```

Import/export is core functionality (not optional under `[cli]` extras). PyYAML is a pure-Python wheel, works on all platforms for test/parse purposes (COM calls only happen at runtime on Windows).

## 10. Out of Scope (v1 Limitations)

Documented limitations; not silently dropped. The importer/exporter emits WARNING logs when encountering these.

| Feature | Status | Rationale |
|---|---|---|
| Multi-valued tags | Flattened to single value | Rhapsody tags can hold multiple values; v1 captures only the first |
| Diagram graphical elements (nodes, edges, coordinates) | Not supported | Graphical info is layout-specific, not structural |
| Operation bodies (source code) | Not supported | Body text is language-specific and ties to codegen settings |
| Class-level flags `is_abstract`, `is_active` | Not supported | Generalization relations ARE supported (SWR_XCH_011); classifier-level flags deferred to v2 |
| Bidirectional relation inverses (`set_inverse`, `get_inverse`) | Not supported | v1 emits one direction per Relation spec; bidirectional relations export as two specs |
| Relation qualifiers (`add_qualifier`, `get_qualifiers`) | Not supported | Qualifier typing adds complexity; deferred to v2 |
| Association classes (`get_association_class`) | Not supported | Niche construct; deferred to v2 |
| Template features (`for_each`, variable substitution, ARXML import) | Not supported | Out of scope — this is round-trip YAML only |
| `--dry-run` flag | Not in v1 | YAGNI; can add later |
| `--skip-root-package` flag | Removed | Root wrapping dropped; export writes children directly |

## 11. References

- **`../py-zcu-mate/rhapsody_generator/rhapsody/`** — rough implementation ported from. Key files: `core.py` (`AbstractRhapsodyCore`), `importer.py` (`RhapsodyImporter`), `exporter.py` (`RhapsodyExporter`). Template/ARXML code dropped.
- **`docs/java_api/com/telelogic/rhapsody/core/IRP*.html`** — authoritative Java API reference for method names and containment relationships (e.g. `IRPOperation.getArguments()`, `IRPType.getEnumerationLiterals()`, `IRPProject` extends `IRPPackage`).
- **Existing project conventions** — `AGENTS.md` (COM wrapping rules, testing, quality gate), `docs/requirements/` (SWR IDs), `docs/tests/unit/` (UTS IDs).

## 12. Open Questions

None — all design questions resolved during brainstorming.
