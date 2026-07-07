# Traceability Matrix - rhapsody_cli

**Last Validated:** 2026-07-07
**Source:** Requirements (SWR) ↔ Test Specifications (UTS/ITS/SYTS/ATS) ↔ Code

---

## Overview

Three-layer traceability for the rhapsody-cli project:

- **Requirements ↔ Code:** What the system should do and where it's implemented
- **Requirements ↔ Test Specifications:** How to verify requirements are met
- **Test Specifications ↔ Code:** Which tests verify which code

**Totals:**

| Artifact | Count |
|----------|-------|
| Requirements | 52 |
| Unit Test Specs (UTS) | 116 |
| Integration Test Specs (ITS) | 38 |
| System Test Specs (SYTS) | 27 |
| Acceptance Test Specs (ATS) | 28 |
| **Total Test Specs** | **209** |

**Overall Coverage:** 52/52 requirements covered = **100%**

---

## Coverage Matrix by Category

### APP (Application Connection Layer) — 9 requirements

| Requirement ID | Title | UTS | ITS | SYTS | ATS |
|----------------|-------|-----|-----|------|-----|
| SWR_APP_00001 | Attach to running instance | UTS_APP_00001-00002 | ITS_APP_00001 | SYTS_APP_00001 | ATS_APP_00001 |
| SWR_APP_00002 | Launch new instance | UTS_APP_00003-00004 | ITS_APP_00002 | SYTS_APP_00001 | ATS_APP_00002 |
| SWR_APP_00003 | Connect with fallback | UTS_APP_00005-00006 | ITS_APP_00003 | SYTS_APP_00001 | ATS_APP_00003 |
| SWR_APP_00004 | Open project file | UTS_APP_00007-00008 | ITS_APP_00004 | SYTS_APP_00002 | ATS_APP_00004 |
| SWR_APP_00005 | Get active project | UTS_APP_00009 | ITS_APP_00004 | SYTS_APP_00002 | ATS_APP_00004 |
| SWR_APP_00006 | Get all open projects | UTS_APP_00010 | ITS_APP_00005 | SYTS_APP_00003 | ATS_APP_00004 |
| SWR_APP_00007 | Quit application | UTS_APP_00011 | ITS_APP_00005 | SYTS_APP_00003 | ATS_APP_00005 |
| SWR_APP_00008 | No global singleton | UTS_APP_00012-00013 | ITS_APP_00006 | SYTS_APP_00004 | ATS_APP_00006 |
| SWR_APP_00009 | Prog ID constant | UTS_APP_00014-00015 | ITS_APP_00007 | SYTS_APP_00004 | ATS_APP_00006 |

**APP Coverage:** 9/9 = **100%**

---

### CORE (Wrapping Machinery) — 10 requirements

| Requirement ID | Title | UTS | ITS | SYTS | ATS |
|----------------|-------|-----|-----|------|-----|
| SWR_CORE_00001 | RPModelElement base class | UTS_CORE_00001-00003 | ITS_CORE_00001 | SYTS_CORE_00001 | ATS_CORE_00001 |
| SWR_CORE_00002 | RPUnit save/file ops | UTS_CORE_00004-00005 | ITS_CORE_00002 | SYTS_CORE_00002 | ATS_CORE_00002 |
| SWR_CORE_00003 | RPCollection iterable | UTS_CORE_00006-00008 | ITS_CORE_00003 | SYTS_CORE_00002 | ATS_CORE_00003 |
| SWR_CORE_00004 | call_com error translation | UTS_CORE_00009-00010 | ITS_CORE_00004 | SYTS_CORE_00003 | ATS_CORE_00004 |
| SWR_CORE_00005 | wrap factory function | UTS_CORE_00011-00012 | ITS_CORE_00005 | SYTS_CORE_00004 | ATS_CORE_00005 |
| SWR_CORE_00006 | register_wrapper registry | UTS_CORE_00013-00014 | ITS_CORE_00005 | SYTS_CORE_00004 | ATS_CORE_00005 |
| SWR_CORE_00007 | _wrap_if_element helper | UTS_CORE_00015 | ITS_CORE_00003 | SYTS_CORE_00002 | ATS_CORE_00003 |
| SWR_CORE_00008 | Registry fallback | UTS_CORE_00016 | ITS_CORE_00006 | SYTS_CORE_00004 | ATS_CORE_00005 |
| SWR_CORE_00009 | Negative index rejection | UTS_CORE_00017 | ITS_CORE_00007 | SYTS_CORE_00006 | ATS_CORE_00006 |
| SWR_CORE_00010 | pywintypes optional import | UTS_CORE_00018 | ITS_CORE_00008 | SYTS_CORE_00003 | ATS_CORE_00004 |

**CORE Coverage:** 10/10 = **100%**

---

### ELEM (Model Element Wrappers) — 13 requirements

| Requirement ID | Title | UTS | ITS | SYTS | ATS |
|----------------|-------|-----|-----|------|-----|
| SWR_ELEM_00001 | RPProject wrapper | UTS_ELEM_00001-00002 | ITS_ELEM_00001 | SYTS_ELEM_00001 | ATS_ELEM_00001 |
| SWR_ELEM_00002 | RPPackage wrapper | UTS_ELEM_00003-00004 | ITS_ELEM_00001 | SYTS_ELEM_00001 | ATS_ELEM_00001 |
| SWR_ELEM_00003 | RPClassifier shared base | UTS_ELEM_00005-00006 | ITS_ELEM_00002 | SYTS_ELEM_00001 | ATS_ELEM_00002 |
| SWR_ELEM_00004 | RPClass wrapper | UTS_ELEM_00007-00009 | ITS_ELEM_00003 | SYTS_ELEM_00001 | ATS_ELEM_00002 |
| SWR_ELEM_00005 | RPActor wrapper | UTS_ELEM_00010-00011 | ITS_ELEM_00004 | SYTS_ELEM_00003 | ATS_ELEM_00006 |
| SWR_ELEM_00006 | RPOperation wrapper | UTS_ELEM_00012-00014 | ITS_ELEM_00005 | SYTS_ELEM_00002 | ATS_ELEM_00003 |
| SWR_ELEM_00007 | RPAttribute wrapper | UTS_ELEM_00015-00017 | ITS_ELEM_00005 | SYTS_ELEM_00002 | ATS_ELEM_00003 |
| SWR_ELEM_00008 | RPDiagram wrapper | UTS_ELEM_00018-00019 | ITS_ELEM_00006 | SYTS_ELEM_00004 | ATS_ELEM_00004 |
| SWR_ELEM_00009 | RPInstance wrapper | UTS_ELEM_00020-00021 | ITS_ELEM_00006 | SYTS_ELEM_00004 | ATS_ELEM_00004 |
| SWR_ELEM_00010 | RPRequirement wrapper | UTS_ELEM_00022-00023 | ITS_ELEM_00006 | SYTS_ELEM_00005 | ATS_ELEM_00006 |
| SWR_ELEM_00011 | RPStatechart wrapper | UTS_ELEM_00024-00025 | ITS_ELEM_00007 | SYTS_ELEM_00005 | ATS_ELEM_00005 |
| SWR_ELEM_00012 | RPUseCase wrapper | UTS_ELEM_00026 | ITS_ELEM_00007 | SYTS_ELEM_00003 | ATS_ELEM_00006 |
| SWR_ELEM_00013 | Element module registration | UTS_ELEM_00027-00028 | ITS_ELEM_00008 | SYTS_ELEM_00006 | ATS_ELEM_00001 |

**ELEM Coverage:** 13/13 = **100%**

---

### CLI (Command-Line Interface) — 16 requirements

| Requirement ID | Title | UTS | ITS | SYTS | ATS |
|----------------|-------|-----|-----|------|-----|
| SWR_CLI_00001 | CLI entry point | UTS_CLI_00001-00003 | ITS_CLI_00001 | SYTS_CLI_00001 | ATS_CLI_00001 |
| SWR_CLI_00002 | Output format option | UTS_CLI_00004-00005 | ITS_CLI_00001 | SYTS_CLI_00005 | ATS_CLI_00006 |
| SWR_CLI_00003 | RhapsodyContext session | UTS_CLI_00006-00009 | ITS_CLI_00002 | SYTS_CLI_00001 | ATS_CLI_00001 |
| SWR_CLI_00004 | Project open command | UTS_CLI_00010-00012 | ITS_CLI_00003 | SYTS_CLI_00002 | ATS_CLI_00002 |
| SWR_CLI_00005 | Project list command | UTS_CLI_00013-00015 | ITS_CLI_00004 | SYTS_CLI_00002 | ATS_CLI_00003 |
| SWR_CLI_00006 | Project close command | UTS_CLI_00016-00018 | ITS_CLI_00004 | SYTS_CLI_00002 | ATS_CLI_00003 |
| SWR_CLI_00007 | Element add command | UTS_CLI_00019-00024 | ITS_CLI_00005 | SYTS_CLI_00003 | ATS_CLI_00004 |
| SWR_CLI_00008 | Element view command | UTS_CLI_00025-00027 | ITS_CLI_00006 | SYTS_CLI_00003 | ATS_CLI_00004 |
| SWR_CLI_00009 | Element query command | UTS_CLI_00028-00030 | ITS_CLI_00006 | SYTS_CLI_00003 | ATS_CLI_00004 |
| SWR_CLI_00010 | IO import command | UTS_CLI_00031-00035 | ITS_CLI_00007 | SYTS_CLI_00004 | ATS_CLI_00005 |
| SWR_CLI_00011 | IO export command | UTS_CLI_00036-00040 | ITS_CLI_00007 | SYTS_CLI_00004 | ATS_CLI_00005 |
| SWR_CLI_00012 | OutputFormatter table | UTS_CLI_00041-00042 | ITS_CLI_00008 | SYTS_CLI_00005 | ATS_CLI_00006 |
| SWR_CLI_00013 | OutputFormatter json | UTS_CLI_00043-00044 | ITS_CLI_00008 | SYTS_CLI_00005 | ATS_CLI_00006 |
| SWR_CLI_00014 | OutputFormatter csv | UTS_CLI_00045 | ITS_CLI_00008 | SYTS_CLI_00005 | ATS_CLI_00006 |
| SWR_CLI_00015 | OutputFormatter router | UTS_CLI_00046 | ITS_CLI_00008 | SYTS_CLI_00005 | ATS_CLI_00006 |
| SWR_CLI_00016 | Class-based command arch | UTS_CLI_00047 | ITS_CLI_00009 | SYTS_CLI_00006 | ATS_CLI_00001 |

**CLI Coverage:** 16/16 = **100%**

---

### EXC (Exceptions) — 4 requirements

| Requirement ID | Title | UTS | ITS | SYTS | ATS |
|----------------|-------|-----|-----|------|-----|
| SWR_EXC_00001 | RhapsodyRuntimeException | UTS_EXC_00001-00002 | ITS_EXC_00001 | SYTS_EXC_00001 | ATS_EXC_00001 |
| SWR_EXC_00002 | RhapsodyConnectionError | UTS_EXC_00003-00004 | ITS_EXC_00002 | SYTS_EXC_00002 | ATS_EXC_00002 |
| SWR_EXC_00003 | Exceptions public API | UTS_EXC_00005-00006 | ITS_EXC_00003 | SYTS_EXC_00003 | ATS_EXC_00003 |
| SWR_EXC_00004 | COM error funneling | UTS_EXC_00007-00008 | ITS_EXC_00004 | SYTS_EXC_00004 | ATS_EXC_00004 |

**EXC Coverage:** 4/4 = **100%**

---

## Requirements ↔ Code Traceability

### APP (Application Connection Layer)

| Requirement ID | Implementation |
|----------------|----------------|
| SWR_APP_00001 | src/rhapsody_cli/application.py:RhapsodyApplication.attach |
| SWR_APP_00002 | src/rhapsody_cli/application.py:RhapsodyApplication.launch |
| SWR_APP_00003 | src/rhapsody_cli/application.py:RhapsodyApplication.connect |
| SWR_APP_00004 | src/rhapsody_cli/application.py:RhapsodyApplication.openProject |
| SWR_APP_00005 | src/rhapsody_cli/application.py:RhapsodyApplication.activeProject |
| SWR_APP_00006 | src/rhapsody_cli/application.py:RhapsodyApplication.getProjects |
| SWR_APP_00007 | src/rhapsody_cli/application.py:RhapsodyApplication.quit |
| SWR_APP_00008 | src/rhapsody_cli/application.py:RhapsodyApplication.__init__ |
| SWR_APP_00009 | src/rhapsody_cli/application.py:_PROG_ID |

### CORE (Wrapping Machinery)

| Requirement ID | Implementation |
|----------------|----------------|
| SWR_CORE_00001 | src/rhapsody_cli/models/_core.py:RPModelElement |
| SWR_CORE_00002 | src/rhapsody_cli/models/_core.py:RPUnit |
| SWR_CORE_00003 | src/rhapsody_cli/models/_core.py:RPCollection |
| SWR_CORE_00004 | src/rhapsody_cli/models/_core.py:call_com |
| SWR_CORE_00005 | src/rhapsody_cli/models/_core.py:wrap |
| SWR_CORE_00006 | src/rhapsody_cli/models/_core.py:register_wrapper |
| SWR_CORE_00007 | src/rhapsody_cli/models/_core.py:_wrap_if_element |
| SWR_CORE_00008 | src/rhapsody_cli/models/_core.py:wrap |
| SWR_CORE_00009 | src/rhapsody_cli/models/_core.py:RPCollection.__getitem__ |
| SWR_CORE_00010 | src/rhapsody_cli/models/_core.py |

### ELEM (Model Element Wrappers)

| Requirement ID | Implementation |
|----------------|----------------|
| SWR_ELEM_00001 | src/rhapsody_cli/models/elements/containment.py:RPProject |
| SWR_ELEM_00002 | src/rhapsody_cli/models/elements/containment.py:RPPackage |
| SWR_ELEM_00003 | src/rhapsody_cli/models/elements/classifiers.py:RPClassifier |
| SWR_ELEM_00004 | src/rhapsody_cli/models/elements/classifiers.py:RPClass |
| SWR_ELEM_00005 | src/rhapsody_cli/models/elements/classifiers.py:RPActor |
| SWR_ELEM_00006 | src/rhapsody_cli/models/elements/classifiers.py:RPOperation |
| SWR_ELEM_00007 | src/rhapsody_cli/models/elements/variables.py:RPAttribute |
| SWR_ELEM_00008 | src/rhapsody_cli/models/elements/diagrams.py:RPDiagram |
| SWR_ELEM_00009 | src/rhapsody_cli/models/elements/relations.py:RPInstance |
| SWR_ELEM_00010 | src/rhapsody_cli/models/elements/requirements.py:RPRequirement |
| SWR_ELEM_00011 | src/rhapsody_cli/models/elements/classifiers.py:RPStatechart |
| SWR_ELEM_00012 | src/rhapsody_cli/models/elements/classifiers.py:RPUseCase |
| SWR_ELEM_00013 | src/rhapsody_cli/models/elements/__init__.py |

### CLI (Command-Line Interface)

| Requirement ID | Implementation |
|----------------|----------------|
| SWR_CLI_00001 | src/rhapsody_cli/cli/main.py:cli |
| SWR_CLI_00002 | src/rhapsody_cli/cli/main.py:cli |
| SWR_CLI_00003 | src/rhapsody_cli/cli/context.py:RhapsodyContext |
| SWR_CLI_00004 | src/rhapsody_cli/cli/commands/project.py:OpenProjectCommand |
| SWR_CLI_00005 | src/rhapsody_cli/cli/commands/project.py:ListProjectsCommand |
| SWR_CLI_00006 | src/rhapsody_cli/cli/commands/project.py:CloseProjectCommand |
| SWR_CLI_00007 | src/rhapsody_cli/cli/commands/element.py:AddElementCommand |
| SWR_CLI_00008 | src/rhapsody_cli/cli/commands/element.py:ViewElementCommand |
| SWR_CLI_00009 | src/rhapsody_cli/cli/commands/element.py:QueryElementCommand |
| SWR_CLI_00010 | src/rhapsody_cli/cli/commands/io.py:ImportCommand |
| SWR_CLI_00011 | src/rhapsody_cli/cli/commands/io.py:ExportCommand |
| SWR_CLI_00012 | src/rhapsody_cli/cli/formatters.py:OutputFormatter.table |
| SWR_CLI_00013 | src/rhapsody_cli/cli/formatters.py:OutputFormatter.json_format |
| SWR_CLI_00014 | src/rhapsody_cli/cli/formatters.py:OutputFormatter.csv_format |
| SWR_CLI_00015 | src/rhapsody_cli/cli/formatters.py:OutputFormatter.format |
| SWR_CLI_00016 | src/rhapsody_cli/cli/commands/project.py:BaseProjectCommand |

### EXC (Exceptions)

| Requirement ID | Implementation |
|----------------|----------------|
| SWR_EXC_00001 | src/rhapsody_cli/exceptions/core.py:RhapsodyRuntimeException |
| SWR_EXC_00002 | src/rhapsody_cli/exceptions/core.py:RhapsodyConnectionError |
| SWR_EXC_00003 | src/rhapsody_cli/exceptions/__init__.py |
| SWR_EXC_00004 | src/rhapsody_cli/models/_core.py:call_com |

---

## Deviation Summary

| Deviation Type | Count | Details |
|----------------|-------|---------|
| DRIFT | 0 | No code changed without requirement update |
| ORPHAN_CODE | 0 | No code without corresponding requirement |
| ORPHAN_REQ | 0 | No requirements reference non-existent code |
| CONFLICT | 0 | No conflicting changes |
| TEST_DRIFT | 0 | No requirement changed without test update |
| UNCOVERED_REQ | 0 | All requirements have test coverage |
| STALE_TEST | 0 | No tests reference deleted requirements |
| ORPHAN_TEST | 0 | No test code without test specification |

**Status: All requirements in sync with code and test specifications.**

---

## File Inventory

### Requirements (5 files)

| File | Category | Reqs |
|------|----------|------|
| docs/requirements/swr_app_requirements.md | APP | 9 |
| docs/requirements/swr_core_requirements.md | CORE | 10 |
| docs/requirements/swr_elem_requirements.md | ELEM | 13 |
| docs/requirements/swr_cli_requirements.md | CLI | 16 |
| docs/requirements/swr_exc_requirements.md | EXC | 4 |

### Test Specifications (20 files)

| Path | Category | Tests |
|------|----------|-------|
| docs/tests/unit/uts_app_test-specs.md | APP | 15 |
| docs/tests/unit/uts_core_test-specs.md | CORE | 18 |
| docs/tests/unit/uts_elem_test-specs.md | ELEM | 28 |
| docs/tests/unit/uts_cli_test-specs.md | CLI | 47 |
| docs/tests/unit/uts_exc_test-specs.md | EXC | 8 |
| docs/tests/integration/its_app_test-specs.md | APP | 7 |
| docs/tests/integration/its_core_test-specs.md | CORE | 8 |
| docs/tests/integration/its_elem_test-specs.md | ELEM | 8 |
| docs/tests/integration/its_cli_test-specs.md | CLI | 10 |
| docs/tests/integration/its_exc_test-specs.md | EXC | 5 |
| docs/tests/system/syts_app_test-specs.md | APP | 5 |
| docs/tests/system/syts_core_test-specs.md | CORE | 6 |
| docs/tests/system/syts_elem_test-specs.md | ELEM | 6 |
| docs/tests/system/syts_cli_test-specs.md | CLI | 6 |
| docs/tests/system/syts_exc_test-specs.md | EXC | 4 |
| docs/tests/acceptance/ats_app_test-specs.md | APP | 6 |
| docs/tests/acceptance/ats_core_test-specs.md | CORE | 6 |
| docs/tests/acceptance/ats_elem_test-specs.md | ELEM | 6 |
| docs/tests/acceptance/ats_cli_test-specs.md | CLI | 6 |
| docs/tests/acceptance/ats_exc_test-specs.md | EXC | 4 |
