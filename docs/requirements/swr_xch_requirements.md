# Software Requirements - YAML Import/Export

**Category:** YAML Import/Export
**Prefix:** SWR_XCH
**Source:** Extracted from docs/superpowers/specs/2026-07-19-yaml-import-export-design.md
**Last Validated:** 2026-07-19

---

## SWR_XCH_001: Project Export Command

**ID:** SWR_XCH_001
**Title:** project export command exports the active project to YAML
**Status:** Planned
**Priority:** High
**Description:**
The project CLI
- SHALL provide a `project export` command that exports the active project's top-level elements to a YAML file.
- SHALL accept `--file <path>` argument (required) for the output YAML file.
- SHALL accept `-v`/`--verbose` flag (inherited from AbstractAction).
- SHALL connect to the active Rhapsody application via `_connect_app()`.
- SHALL obtain the active project via `app.active_project()`.
- SHALL delegate to `RhapsodyExporter(app=app).export(project)` to produce the YAML dict.
- SHALL write the dict via `RhapsodyYaml().write(args.file, data)`.
- SHALL wrap errors as `CliExecutionError` (no `sys.exit()` in the action).
- SHALL log a success message via `self.logger.info(...)`.
**Implementation:** src/rhapsody_cli/actions/project_action.py:ProjectExportAction
**Last Changed:** 2026-07-19

---

## SWR_XCH_002: Project Import Command

**ID:** SWR_XCH_002
**Title:** project import command imports YAML into the active project
**Status:** Planned
**Priority:** High
**Description:**
The project CLI
- SHALL provide a `project import` command that imports YAML elements as top-level elements of the active project.
- SHALL accept `--file <path>` argument (required) for the input YAML file.
- SHALL accept `-v`/`--verbose` flag.
- SHALL connect to the active Rhapsody application via `_connect_app()`.
- SHALL obtain the active project via `app.active_project()`.
- SHALL read the YAML dict via `RhapsodyYaml().read(args.file)`.
- SHALL delegate to `RhapsodyImporter(app=app).import_template(data, project)`.
- SHALL call `app.save_all()` after a successful import.
- SHALL wrap errors as `CliExecutionError`.
- SHALL log a success message via `self.logger.info(...)`.
**Implementation:** src/rhapsody_cli/actions/project_action.py:ProjectImportAction
**Last Changed:** 2026-07-19

---

## SWR_XCH_003: Package Export Command

**ID:** SWR_XCH_003
**Title:** package export command exports a package to YAML
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
- SHALL provide a `package export` command that exports a specific package's contents to a YAML file.
- SHALL accept `--path <package-path>` argument (optional; defaults to project root).
- SHALL accept `--file <path>` argument (required) for the output YAML file.
- SHALL accept `-v`/`--verbose` flag.
- SHALL resolve the target package via `_resolve_and_validate_package(args.path)` (reuses existing helper).
- SHALL delegate to `RhapsodyExporter(app=app).export(package)`.
- SHALL write the dict via `RhapsodyYaml().write(args.file, data)`.
- SHALL wrap errors as `CliExecutionError`.
- SHALL log a success message via `self.logger.info(...)`.
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageExportAction
**Last Changed:** 2026-07-19

---

## SWR_XCH_004: Package Import Command

**ID:** SWR_XCH_004
**Title:** package import command imports YAML into a package
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
- SHALL provide a `package import` command that imports YAML elements as children of a specific package.
- SHALL accept `--path <package-path>` argument (optional; defaults to project root).
- SHALL accept `--file <path>` argument (required) for the input YAML file.
- SHALL accept `-v`/`--verbose` flag.
- SHALL resolve the target package via `_resolve_and_validate_package(args.path)`.
- SHALL read the YAML dict via `RhapsodyYaml().read(args.file)`.
- SHALL delegate to `RhapsodyImporter(app=app).import_template(data, package)`.
- SHALL call `app.save_all()` after a successful import.
- SHALL wrap errors as `CliExecutionError`.
- SHALL log a success message via `self.logger.info(...)`.
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageImportAction
**Last Changed:** 2026-07-19

---

## SWR_XCH_005: YAML Schema (version 1)

**ID:** SWR_XCH_005
**Title:** YAML schema for round-tripping Rhapsody model structure
**Status:** Planned
**Priority:** High
**Description:**
The exchange module
- SHALL define `SCHEMA_VERSION = 1` as an integer constant in `exchange/schema.py`.
- SHALL define key constants `VERSION_KEY = "version"`, `PROJECT_KEY = "project"`, `RHAPSODY_MODEL_KEY = "rhapsody-model"`.
- SHALL produce YAML files whose top-level mapping contains `version`, `project`, and `rhapsody-model` keys.
- SHALL set `version: 1` in every exported file.
- SHALL set `project` to the project name obtained by walking the owner chain from the export container.
- SHALL set `rhapsody-model` to a list of element spec dicts, one per top-level child.
- SHALL validate `version == SCHEMA_VERSION` on import and raise `CliExecutionError` on mismatch.
- SHALL use `type` discriminator field on each element spec (e.g. `type: "Package"`, `type: "Class"`, `type: "Relation"`).
**Implementation:** src/rhapsody_cli/exchange/schema.py
**Last Changed:** 2026-07-19

---

## SWR_XCH_006: Element Find-or-Create (RhapsodyModelHelper)

**ID:** SWR_XCH_006
**Title:** RhapsodyModelHelper provides find_or_create dispatch for 14 element types
**Status:** Planned
**Priority:** High
**Description:**
The `RhapsodyModelHelper` base class in `exchange/core.py`
- SHALL expose `find_or_create_<type>(parent, name)` methods for 14 element types: Package, Class, Operation, Argument, Attribute, Type, Object, EnumerationLiteral, Dependency, Generalization, Relation, Port, Event, EventReception.
- SHALL use `find_child_by_name(parent, name)` to locate an existing child; return it if found (idempotent re-import).
- SHALL create the element via the appropriate COM add method when not found: `add_new_aggr("MetaClass", name)` for most types, `add_global_function(name)` for operations on packages, `add_argument(name)` for arguments, `add_new_aggr("LiteralValue", name)` for enumeration literals.
- SHALL sanitize names by stripping whitespace and replacing invalid characters with underscores.
- SHALL be idempotent: importing the same YAML twice SHALL NOT create duplicates.
- SHALL expose public `find_child_by_name` and `_set_type_kind` helpers (other internals are private).
**Implementation:** src/rhapsody_cli/exchange/core.py:RhapsodyModelHelper
**Last Changed:** 2026-07-19

---

## SWR_XCH_007: Stereotype and Tag Round-Trip

**ID:** SWR_XCH_007
**Title:** Stereotypes and tags round-trip via apply_stereotypes / apply_tags
**Status:** Planned
**Priority:** High
**Description:**
The `RhapsodyModelHelper` base class
- SHALL expose `apply_stereotypes(element, stereotypes_list)` that infers the element's meta type via `get_meta_class()` and calls `element.add_stereotype(name, meta_type)` for each entry.
- SHALL skip stereotypes that are already applied (idempotent — no duplicate add).
- SHALL expose `apply_tags(element, tags_dict)` that calls `element.set_property_value(key, val)` for each entry.
- SHALL apply stereotypes and tags to ALL element types including Argument and EnumerationLiteral (routed through `_process_element` / `_export_element`).
- SHALL export stereotypes as a list of names and tags as a dict of name→string via `RhapsodyExporter._export_stereotypes` / `_export_tags`.
- SHALL export tags by enumerating `element.get_all_tags()` and reading each tag's `get_name()` and `get_value()` (via `tag.call_com(lambda: tag._com.getValue())`).
- SHALL skip malformed tags with a warning during export (best-effort).
**Implementation:** src/rhapsody_cli/exchange/core.py:RhapsodyModelHelper (apply_stereotypes, apply_tags); src/rhapsody_cli/exchange/exporter.py:RhapsodyExporter (_export_stereotypes, _export_tags)
**Last Changed:** 2026-07-19

---

## SWR_XCH_008: Core Type-Specific Fields

**ID:** SWR_XCH_008
**Title:** Type-specific YAML fields for 8 core element types
**Status:** Planned
**Priority:** High
**Description:**
The importer and exporter SHALL round-trip the following type-specific fields:
- `Operation`: `return_type` (string, optional), `arguments` (list of Argument specs), `is_static` (bool, optional), `visibility` (string, optional).
- `Argument`: `direction` (string, optional — in/out/inout), `type` (string, optional — type name).
- `Attribute`: `type` (string, optional), `visibility` (string, optional), `multiplicity` (string, optional), `is_static` (bool, optional), `default_value` (string, optional).
- `Type`: `kind` (string — sets via `set_kind()`), `literals` (list of EnumerationLiteral specs, only when kind=Enumeration).
- `Object`: `classifier` (string, optional — class name to instantiate).
- `Class`: `is_abstract` (bool, optional), `is_active` (bool, optional), `is_final` (bool, optional), `visibility` (string, optional).
- `Package`: `children` (list of nested element specs).
- `EnumerationLiteral`: no type-specific fields (only common name/stereotypes/tags).
The importer SHALL use `_apply_<type>_extras` methods to set these fields; the exporter SHALL use `_export_<type>` methods to serialize them.
**Implementation:** src/rhapsody_cli/exchange/importer.py:RhapsodyImporter (_apply_*_extras); src/rhapsody_cli/exchange/exporter.py:RhapsodyExporter (_export_*)
**Last Changed:** 2026-07-19

---

## SWR_XCH_009: Error Handling and Skip-on-Unsupported

**ID:** SWR_XCH_009
**Title:** Skip unsupported element types and missing references with warnings
**Status:** Planned
**Priority:** High
**Description:**
The exchange module
- SHALL skip unsupported metaclasses during export (returns `None`, filtered out of `rhapsody-model` list) with a WARNING log.
- SHALL skip unsupported `type` values during import (returns `None`, siblings still processed) with a WARNING log.
- SHALL skip missing type references (e.g. `data_type: "UnknownType"`) with a WARNING; the element is still created without the type set.
- SHALL skip missing relation targets (`to`, `base_class`, `depends_on`) with a WARNING; the relation/dependency/generalization is still created without the link.
- SHALL skip missing port contract / interface names with a WARNING; the port is still created.
- SHALL skip missing event references (`event`, `base_event`, `super_event`) with a WARNING; the reception/event is still created.
- SHALL raise `CliExecutionError` on schema version mismatch (with expected vs. actual version in the message).
- SHALL raise `CliExecutionError` on invalid YAML syntax, missing input file, or unwritable output file (via `RhapsodyYaml`).
- SHALL NOT call `sys.exit()` anywhere in the exchange module or actions.
**Implementation:** src/rhapsody_cli/exchange/importer.py, src/rhapsody_cli/exchange/exporter.py, src/rhapsody_cli/exchange/yaml_utils.py
**Last Changed:** 2026-07-19

---

## SWR_XCH_010: Reusable Model Manipulation API

**ID:** SWR_XCH_010
**Title:** RhapsodyModelHelper exposes reusable find/create/apply/resolve helpers
**Status:** Planned
**Priority:** Medium
**Description:**
The `RhapsodyModelHelper` base class
- SHALL expose `find_child_by_name(parent, name) -> Optional[RPModelElement]` (PUBLIC) that iterates `parent.get_nested_elements()` and returns the first child whose `get_name()` matches, else `None`.
- SHALL expose `_set_type_kind(type_element, kind) -> None` (PRIVATE) that calls `type_element.set_kind(kind)` with try/except.
- SHALL expose `apply_stereotypes(element, stereotypes)` and `apply_tags(element, tags)` (PUBLIC).
- SHALL expose `resolve_classifier(name) -> Optional[RPModelElement]` (PUBLIC) that recursively searches the project for a classifier by name.
- SHALL expose `get_classifier_name(classifier) -> Optional[str]` (PUBLIC) — None-safe wrapper around `classifier.get_name()`.
- SHALL expose private helpers `_collect_children(container)`, `_get_project_name(element)`, `_wrap_if_needed(element)`.
- SHALL be subclassed by `RhapsodyImporter` and `RhapsodyExporter`; the base class itself SHALL NOT perform YAML I/O.
**Implementation:** src/rhapsody_cli/exchange/core.py:RhapsodyModelHelper
**Last Changed:** 2026-07-19

---

## SWR_XCH_011: Relations Round-Trip

**ID:** SWR_XCH_011
**Title:** Dependency, Generalization, and Relation round-trip with source/target wiring
**Status:** Planned
**Priority:** High
**Description:**
The exchange module SHALL round-trip relation elements:
- `Dependency`: `from` (string, source classifier name), `to` (string, target classifier name), `stereotypes`, `tags`.
- `Generalization`: `subtype` (string, derived classifier name), `superclass` (string, base classifier name), `stereotypes`, `tags`.
- `Relation`: `from` (string), `to` (string), `relation_type` (string — one of "Association", "Aggregation", "Composition"), `multiplicity` (string, optional), `role` (string, optional), `visibility` (string, optional), `is_navigable` (bool, optional), `is_virtual` (bool, optional), `stereotypes`, `tags`.
The importer SHALL create the relation via `find_or_create_<type>(parent, name)` then wire source/target via `set_from()`/`set_to()` (Dependency, Relation) or `set_from()`/`set_to()` (Generalization) using classifiers resolved via `resolve_classifier(name)`.
The exporter SHALL serialize `from`/`to` via `get_from().get_name()` / `get_to().get_name()` and `relation_type` via `get_relation_type()`.
Missing references SHALL be skipped with a WARNING (per SWR_XCH_009).
**Implementation:** src/rhapsody_cli/exchange/importer.py:_apply_dependency_extras, _apply_generalization_extras, _apply_relation_extras; src/rhapsody_cli/exchange/exporter.py:_export_dependency, _export_generalization, _export_relation
**Last Changed:** 2026-07-19

---

## SWR_XCH_012: Ports Round-Trip

**ID:** SWR_XCH_012
**Title:** Port round-trip with interfaces and contract
**Status:** Planned
**Priority:** High
**Description:**
The exchange module SHALL round-trip `Port` elements with the following fields:
- `is_behavioral` (bool, optional) — set via `set_is_behavioral(1/0)`.
- `is_reversed` (bool, optional) — set via `set_is_reversed(1/0)`.
- `contract` (string, optional) — interface name resolved via `resolve_classifier(name)` and set via `set_contract(interface)`.
- `provided_interfaces` (list of strings, optional) — each resolved via `resolve_classifier(name)` and added via `add_provided_interface(interface)`.
- `required_interfaces` (list of strings, optional) — each resolved via `resolve_classifier(name)` and added via `add_required_interface(interface)`.
- `stereotypes`, `tags` (common fields).
The exporter SHALL serialize these fields via the corresponding getters; missing references SHALL be skipped with a WARNING (per SWR_XCH_009).
**Implementation:** src/rhapsody_cli/exchange/importer.py:_apply_port_extras; src/rhapsody_cli/exchange/exporter.py:_export_port
**Last Changed:** 2026-07-19

---

## SWR_XCH_013: Events and EventReceptions Round-Trip

**ID:** SWR_XCH_013
**Title:** Event and EventReception round-trip with event references
**Status:** Planned
**Priority:** High
**Description:**
The exchange module SHALL round-trip `Event` and `EventReception` elements:
- `Event`: `base_event` (string, optional — name of parent event), `super_event` (string, optional — name of super event), `stereotypes`, `tags`.
- `EventReception`: `event` (string, optional — name of referenced event, set via `set_event(event_element)` after resolution), `stereotypes`, `tags`.
The importer SHALL resolve event references via `resolve_classifier(name)`; missing references SHALL be skipped with a WARNING (per SWR_XCH_009).
The exporter SHALL serialize these fields via the corresponding getters (None-safe).
**Implementation:** src/rhapsody_cli/exchange/importer.py:_apply_event_extras, _apply_event_reception_extras; src/rhapsody_cli/exchange/exporter.py:_export_event, _export_event_reception
**Last Changed:** 2026-07-19