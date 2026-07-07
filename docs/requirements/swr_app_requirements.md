# Software Requirements - APP (Application Connection Layer)

**Category:** APP
**Prefix:** SWR
**Source:** Extracted from code
**Last Validated:** 2026-07-07

---

## SWR_APP_00001: Attach to Running Rhapsody Instance

**ID:** SWR_APP_00001
**Title:** Attach to an already-running Rhapsody instance via COM
**Status:** Implemented
**Priority:** High
**Description:**
The `RhapsodyApplication.attach()` class method shall attach to an already-running
IBM Rhapsody instance by calling `win32com.client.GetActiveObject("Rhapsody2.Application.1")`.
If no running instance is found, a `RhapsodyConnectionError` shall be raised.
**Implementation:** src/rhapsody_cli/application.py:RhapsodyApplication.attach
**Last Changed:** 2026-07-07

---

## SWR_APP_00002: Launch New Rhapsody Instance

**ID:** SWR_APP_00002
**Title:** Launch a new Rhapsody instance via COM Dispatch
**Status:** Implemented
**Priority:** High
**Description:**
The `RhapsodyApplication.launch()` class method shall start a new Rhapsody instance
by calling `win32com.client.Dispatch("Rhapsody2.Application.1")`. If launch fails, a
`RhapsodyConnectionError` shall be raised.
**Implementation:** src/rhapsody_cli/application.py:RhapsodyApplication.launch
**Last Changed:** 2026-07-07

---

## SWR_APP_00003: Connect with Fallback

**ID:** SWR_APP_00003
**Title:** Connect to Rhapsody with attach-first fallback to launch
**Status:** Implemented
**Priority:** High
**Description:**
The `RhapsodyApplication.connect(prefer_attach: bool = True)` class method shall be the
primary entry point for connecting to Rhapsody. When `prefer_attach` is True (default),
it shall first attempt `attach()`; if that fails with `RhapsodyConnectionError`, it shall
fall back to `launch()`. When `prefer_attach` is False, it shall call `launch()` directly.
**Implementation:** src/rhapsody_cli/application.py:RhapsodyApplication.connect
**Last Changed:** 2026-07-07

---

## SWR_APP_00004: Open Project File

**ID:** SWR_APP_00004
**Title:** Open a Rhapsody project file from a path
**Status:** Implemented
**Priority:** High
**Description:**
The `openProject(filename: str)` method shall open the Rhapsody project at the given
file path and return a wrapped `RPProject` instance. COM errors during the call shall
be translated to `RhapsodyRuntimeException`.
**Implementation:** src/rhapsody_cli/application.py:RhapsodyApplication.openProject
**Last Changed:** 2026-07-07

---

## SWR_APP_00005: Get Active Project

**ID:** SWR_APP_00005
**Title:** Retrieve the currently active project
**Status:** Implemented
**Priority:** Medium
**Description:**
The `activeProject()` method shall return the currently active Rhapsody project as a
wrapped `RPProject` instance.
**Implementation:** src/rhapsody_cli/application.py:RhapsodyApplication.activeProject
**Last Changed:** 2026-07-07

---

## SWR_APP_00006: Get All Open Projects

**ID:** SWR_APP_00006
**Title:** Retrieve all currently open projects
**Status:** Implemented
**Priority:** Medium
**Description:**
The `getProjects()` method shall return an `RPCollection` containing all currently open
Rhapsody projects.
**Implementation:** src/rhapsody_cli/application.py:RhapsodyApplication.getProjects
**Last Changed:** 2026-07-07

---

## SWR_APP_00007: Quit Application

**ID:** SWR_APP_00007
**Title:** Terminate the wrapped Rhapsody instance
**Status:** Implemented
**Priority:** Medium
**Description:**
The `quit()` method shall terminate the Rhapsody instance by calling `quit()` on the
underlying COM object.
**Implementation:** src/rhapsody_cli/application.py:RhapsodyApplication.quit
**Last Changed:** 2026-07-07

---

## SWR_APP_00008: No Global Singleton

**ID:** SWR_APP_00008
**Title:** Each RhapsodyApplication instance wraps one COM object independently
**Status:** Implemented
**Priority:** Medium
**Description:**
`RhapsodyApplication` shall not be a global singleton. Each instance shall wrap exactly
one COM object, allowing multiple simultaneous Rhapsody instances/models to be managed
side by side in the same process.
**Implementation:** src/rhapsody_cli/application.py:RhapsodyApplication.__init__
**Last Changed:** 2026-07-07

---

## SWR_APP_00009: Prog ID Constant

**ID:** SWR_APP_00009
**Title:** Use canonical Rhapsody COM Prog ID
**Status:** Implemented
**Priority:** Low
**Description:**
The COM Prog ID used for attach/launch shall be `"Rhapsody2.Application.1"` (the
canonical Rhapsody automation Prog ID for the "new" COM API version, as documented
in IBM Rhapsody's automation samples; the legacy `"Rhapsody.Application"` Prog ID
is not registered by all Rhapsody installations, e.g. Rhapsody 9.0.2).
**Implementation:** src/rhapsody_cli/application.py:_PROG_ID
**Last Changed:** 2026-07-07
