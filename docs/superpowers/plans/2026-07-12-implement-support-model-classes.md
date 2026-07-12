# Implement Support Model Classes & Update Parity Checklists

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.


**Goal:** Replace every `raise NotImplementedError` body in the three auto-generated support stub modules (`model_files.py`, `model_ide.py`, `model_codegen.py`) with real COM-backed implementations that mirror the Rhapsody Java API, add unit tests for each method using fakes, and flip the per-class "method parity checklist" comment boxes from `[ ]` to `[x]`.


**Architecture:** Pure method-body completion against the existing `RPModelElement` wrapping machinery (`AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap`). No new classes or registry entries are introduced. Each stub method already carries its exact Java reference (e.g. `com.telelogic.rhapsody.core.IRPFile::addElement(...)`); the implementation follows a deterministic, category-based recipe derived from that reference. Checklists are updated in place.


**Tech Stack:** Python 3.8+, pytest, ruff, black, mypy. Tests run against fakes (`tests/unit/models/fakes.py`); no live Rhapsody needed.


## Global Constraints

- TDD is mandatory — write the failing test for a method before implementing its body; coverage target 80% min, 90%+ preferred.

- Do NOT use `from __future__ import annotations` — it is forbidden.

- All constants use `SCREAMING_SNAKE_CASE`. Method names mirror the Rhapsody Java API exactly (snake_case Python wrapper, camelCase COM target).

- `mypy` runs in strict mode; all functions need return type annotations (already present on every stub).

- All COM read/write goes through `AbstractRPModelElement._get_method_or_property` / `_set_method_or_property`; all COM mutating/action calls go through `AbstractRPModelElement.call_com(lambda: ...)` so `pywintypes.com_error` becomes `RhapsodyRuntimeException`.

- `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest` is the full quality gate.

- All changes go on a feature branch (e.g. `feat/implement-support-model-classes`); never commit directly to `main`.

- Commits are human-authored only; no AI co-author trailers.

- `get_interface_name` is ALREADY implemented on `RPModelElement` (see `src/rhapsody_cli/models/core.py:844`). Every support class inherits it, so the `get_interface_name` override in each stub is a redundant duplicate: **delete the override method** and mark that checklist line `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


## Implementation Recipe (canonical patterns)

Each stub method falls into exactly one category. Apply the matching template; `COM` = the Java method name from the method's `Reference:` docstring line (fallback: snake_case→camelCase), `PROP` = the camelCase property derived from `COM` (drop a leading `get`/`set`/`is` and lower-case the next letter).


**Getter (returns primitive / collection / element):**

```python

def get_x(self) -> str:

    return str(self._get_method_or_property(self._com, "getX", "x"))

def get_elements(self) -> "RPCollection":

    return RPCollection(self._get_method_or_property(self._com, "getElements", "elements"))

def get_owner(self) -> "RPModelElement":

    return AbstractRPModelElement.wrap(self._get_method_or_property(self._com, "getOwner", "owner"))

```


**Setter:**

```python

def set_path(self, path: str) -> None:

    self._set_method_or_property(self._com, "setPath", "path", path)

def set_contract(self, contract: "RPModelElement") -> None:

    self._set_method_or_property(self._com, "setContract", "contract", contract._com)

```


**Action / command (void or returns value, mutates COM):**

```python

def add_element(self, element: "RPClassifier", file_fragment_type: str) -> None:

    self.call_com(lambda: self._com.addElement(element._com, file_fragment_type))

def search(self, p_search_query: "RPSearchQuery") -> "RPCollection":

    return RPCollection(self.call_com(lambda: self._com.search(p_search_query._com)))

```


**Argument unwrapping rule:** if an argument's type annotation is a wrapper type (`RPClassifier`, `RPModelElement`, `RPPackage`, `RPSearchQuery`, `RPTableLayout`, `RPMatrixView`, `RPTableView`, `RPDiagram`, `RPSequenceDiagram`, `RPStereotype`, `RPowListListener`, `RPowTextListener`, `RPRhapsodyApplication`, `RPCollection`, `RhapsodyApplication`), pass `arg._com` to the COM call. Primitive `str`/`int` args are passed as-is.


**Return wrapping rule:** `-> str` ⇒ `str(...)`; `-> int` ⇒ `int(...)`; `-> "RPCollection"` ⇒ `RPCollection(...)`; `-> "RPModelElement"` ⇒ `AbstractRPModelElement.wrap(...)`; `-> "RhapsodyApplication"` ⇒ `RhapsodyApplication(...)`; any other specific wrapper (e.g. `RPTableLayout`, `RPowListListener`) ⇒ construct that wrapper directly around the COM result.


## Checklist Update Rule

Each class opens with a `# IRP<X> method parity checklist:` comment block. For every method you implement/write-a-test-for, change its line:

```
# [ ] methodName   [ ] impl  [ ] docstring  [ ] test
```
to
```
# [x] methodName   [x] impl  [x] docstring  [x] test
```
The `[x] docstring` box is already valid (docstrings ship in the stubs); flip it together with `impl` and `test` once that method's test exists. `get_interface_name` lines become `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


## Test Recipe (fakes)

One test function per method in `tests/unit/models/support/test_<module>.py`. Pattern (verified against existing `tests/unit/models/elements/test_annotation.py` / `test_actor.py`):

```python
from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.support.model_files import RPFile
from tests.unit.models.fakes import make_fake_collection, make_fake_element

def test_RPFile_get_file_type_delegates_to_com():
    fake = make_fake_element("File", getFileType="cpp")
    obj = RPFile(fake)
    assert obj.get_file_type() == "cpp"

def test_RPFile_add_element_delegates_to_com():
    fake = make_fake_element("File")
    target = make_fake_element("Class", getName="Widget")
    obj = RPFile(fake)
    obj.add_element(AbstractRPModelElement.wrap(target), "implFragment")
    fake.addElement.assert_called_once_with(target, "implFragment")
```
Error-path (`com_error` → `RhapsodyRuntimeException`) translation is already covered globally in `tests/unit/models/test_core.py`; per-method error tests are NOT required.


## Task 1: Implement `RPASCIIFile` (files)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_files.py` (class `RPASCIIFile`)

- Test: `tests/unit/models/support/test_files.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPASCIIFile` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `close` | `close` | ACTION | - | - |

| `open` | `open` | ACTION | - | filename |

| `write` | `write` | ACTION | - | data |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_files.py`)


```python

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from tests.unit.models.fakes import make_fake_collection, make_fake_element
from rhapsody_cli.models.support.model_files import (
    RPASCIIFile, RPControlledFile, RPFile, RPFileFragment,
)

def test_RPASCIIFile_close_delegates_to_com():
    fake = make_fake_element("ASCIIFile")
    obj = RPASCIIFile(fake)
    obj.close()
    fake.close.assert_called_once_with()


def test_RPASCIIFile_open_delegates_to_com():
    fake = make_fake_element("ASCIIFile")
    obj = RPASCIIFile(fake)
    obj.open("x")
    fake.open.assert_called_once_with("x")


def test_RPASCIIFile_write_delegates_to_com():
    fake = make_fake_element("ASCIIFile")
    obj = RPASCIIFile(fake)
    obj.write("x")
    fake.write.assert_called_once_with("x")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_files.py -k RPASCIIFile -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPASCIIFile`)

```python

    def close(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.close())

    def open(self, filename: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.open(filename))

    def write(self, data: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.write(data))

```



> **Imports:** ensure `src/rhapsody_cli/models/support/model_files.py` also imports what the bodies below need (add to the existing `from rhapsody_cli.models.core import ...` line / module top):
```python
from rhapsody_cli.models.core import RPCollection  # add to existing core import
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
from rhapsody_cli.models.elements.containment.model_package import RPPackage
```


- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_files.py -k RPASCIIFile -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_files.py` for class `RPASCIIFile`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_files.py tests/unit/models/support/test_files.py
git commit -m "feat(support): implement RPASCIIFile methods with tests"
```


## Task 2: Implement `RPControlledFile` (files)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_files.py` (class `RPControlledFile`)

- Test: `tests/unit/models/support/test_files.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPControlledFile` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `get_full_path_file_name` | `getFullPathFileName` | GETTER | (raw) | - |

| `open` | `open` | ACTION | - | - |

| `set_target` | `setTarget` | SETTER | - | filename |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_files.py`)


```python

def test_RPControlledFile_get_full_path_file_name_delegates_to_com():
    fake = make_fake_element("ControlledFile")
    fake.getFullPathFileName.return_value = "value"
    obj = RPControlledFile(fake)
    assert obj.get_full_path_file_name() == "value"


def test_RPControlledFile_open_delegates_to_com():
    fake = make_fake_element("ControlledFile")
    obj = RPControlledFile(fake)
    obj.open()
    fake.open.assert_called_once_with()


def test_RPControlledFile_set_target_delegates_to_com():
    fake = make_fake_element("ControlledFile")
    obj = RPControlledFile(fake)
    obj.set_target("file.txt")
    fake.setTarget.assert_called_once_with("file.txt")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_files.py -k RPControlledFile -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPControlledFile`)

```python

    def get_full_path_file_name(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFullPathFileName", "fullPathFileName"))

    def open(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.open())

    def set_target(self, filename: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setTarget", "target", filename)

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_files.py -k RPControlledFile -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_files.py` for class `RPControlledFile`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_files.py tests/unit/models/support/test_files.py
git commit -m "feat(support): implement RPControlledFile methods with tests"
```


## Task 3: Implement `RPFile` (files)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_files.py` (class `RPFile`)

- Test: `tests/unit/models/support/test_files.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPFile` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `add_element` | `addElement` | ACTION | - | element→._com, file_fragment_type |

| `add_model_element` | `addModelElement` | ACTION | - | element→._com, file_fragment_type |

| `add_package_to_scope` | `addPackageToScope` | ACTION | - | p→._com |

| `add_text_element` | `addTextElement` | ACTION | - | text |

| `add_to_scope` | `addToScope` | ACTION | - | element→._com |

| `get_elements` | `getElements` | GETTER | RPCollection | - |

| `get_file_fragments` | `getFileFragments` | GETTER | RPCollection | - |

| `get_file_type` | `getFileType` | GETTER | (raw) | - |

| `get_files` | `getFiles` | GETTER | RPCollection | - |

| `get_imp_name` | `getImpName` | GETTER | (raw) | including_path |

| `get_path` | `getPath` | GETTER | (raw) | full_path |

| `get_spec_name` | `getSpecName` | GETTER | (raw) | including_path |

| `is_empty` | `isEmpty` | ACTION | (raw) | - |

| `set_file_type` | `setFileType` | SETTER | - | file_type |

| `set_path` | `setPath` | SETTER | - | path |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_files.py`)


```python

def test_RPFile_add_element_delegates_to_com():
    fake = make_fake_element("File")
    target = make_fake_element("X")
    obj = RPFile(fake)
    obj.add_element(AbstractRPModelElement.wrap(target), "x")
    fake.addElement.assert_called_once_with(target, "x")


def test_RPFile_add_model_element_delegates_to_com():
    fake = make_fake_element("File")
    target = make_fake_element("X")
    obj = RPFile(fake)
    obj.add_model_element(AbstractRPModelElement.wrap(target), "x")
    fake.addModelElement.assert_called_once_with(target, "x")


def test_RPFile_add_package_to_scope_delegates_to_com():
    fake = make_fake_element("File")
    target = make_fake_element("X")
    obj = RPFile(fake)
    obj.add_package_to_scope(AbstractRPModelElement.wrap(target))
    fake.addPackageToScope.assert_called_once_with(target)


def test_RPFile_add_text_element_delegates_to_com():
    fake = make_fake_element("File")
    obj = RPFile(fake)
    obj.add_text_element("x")
    fake.addTextElement.assert_called_once_with("x")


def test_RPFile_add_to_scope_delegates_to_com():
    fake = make_fake_element("File")
    target = make_fake_element("X")
    obj = RPFile(fake)
    obj.add_to_scope(AbstractRPModelElement.wrap(target))
    fake.addToScope.assert_called_once_with(target)


def test_RPFile_get_elements_delegates_to_com():
    fake = make_fake_element("File")
    inner = make_fake_element("X", getName="y")
    fake.getElements.return_value = make_fake_collection([inner])
    obj = RPFile(fake)
    result = obj.get_elements()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPFile_get_file_fragments_delegates_to_com():
    fake = make_fake_element("File")
    inner = make_fake_element("X", getName="y")
    fake.getFileFragments.return_value = make_fake_collection([inner])
    obj = RPFile(fake)
    result = obj.get_file_fragments()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPFile_get_file_type_delegates_to_com():
    fake = make_fake_element("File")
    fake.getFileType.return_value = "value"
    obj = RPFile(fake)
    assert obj.get_file_type() == "value"


def test_RPFile_get_files_delegates_to_com():
    fake = make_fake_element("File")
    inner = make_fake_element("X", getName="y")
    fake.getFiles.return_value = make_fake_collection([inner])
    obj = RPFile(fake)
    result = obj.get_files()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPFile_get_imp_name_delegates_to_com():
    fake = make_fake_element("File")
    fake.getImpName.return_value = "value"
    obj = RPFile(fake)
    assert obj.get_imp_name() == "value"


def test_RPFile_get_path_delegates_to_com():
    fake = make_fake_element("File")
    fake.getPath.return_value = "value"
    obj = RPFile(fake)
    assert obj.get_path() == "value"


def test_RPFile_get_spec_name_delegates_to_com():
    fake = make_fake_element("File")
    fake.getSpecName.return_value = "value"
    obj = RPFile(fake)
    assert obj.get_spec_name() == "value"


def test_RPFile_is_empty_delegates_to_com():
    fake = make_fake_element("File")
    fake.isEmpty.return_value = 1
    obj = RPFile(fake)
    result = obj.is_empty()
    fake.isEmpty.assert_called_once_with()
    assert result == 1


def test_RPFile_set_file_type_delegates_to_com():
    fake = make_fake_element("File")
    obj = RPFile(fake)
    obj.set_file_type("file.txt")
    fake.setFileType.assert_called_once_with("file.txt")


def test_RPFile_set_path_delegates_to_com():
    fake = make_fake_element("File")
    obj = RPFile(fake)
    obj.set_path("file.txt")
    fake.setPath.assert_called_once_with("file.txt")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_files.py -k RPFile -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPFile`)

```python

    def add_element(self, element: RPClassifier, file_fragment_type: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addElement(element._com, file_fragment_type))

    def add_model_element(self, element: RPModelElement, file_fragment_type: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addModelElement(element._com, file_fragment_type))

    def add_package_to_scope(self, p: RPPackage) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addPackageToScope(p._com))

    def add_text_element(self, text: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addTextElement(text))

    def add_to_scope(self, element: RPClassifier) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addToScope(element._com))

    def get_elements(self) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getElements", "elements"))

    def get_file_fragments(self) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getFileFragments", "fileFragments"))

    def get_file_type(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFileType", "fileType"))

    def get_files(self) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getFiles", "files"))

    def get_imp_name(self, including_path: int) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getImpName", "impName"))

    def get_path(self, full_path: int) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getPath", "path"))

    def get_spec_name(self, including_path: int) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getSpecName", "specName"))

    def is_empty(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.isEmpty()))

    def set_file_type(self, file_type: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setFileType", "fileType", file_type)

    def set_path(self, path: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setPath", "path", path)

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_files.py -k RPFile -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_files.py` for class `RPFile`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_files.py tests/unit/models/support/test_files.py
git commit -m "feat(support): implement RPFile methods with tests"
```


## Task 4: Implement `RPFileFragment` (files)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_files.py` (class `RPFileFragment`)

- Test: `tests/unit/models/support/test_files.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPFileFragment` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `get_fragment_element` | `getFragmentElement` | GETTER | AbstractRPModelElement.wrap | - |

| `get_fragment_text` | `getFragmentText` | GETTER | (raw) | - |

| `get_fragment_type` | `getFragmentType` | GETTER | (raw) | - |

| `move_fragment_in_owner` | `moveFragmentInOwner` | ACTION | - | up |

| `set_fragment_text` | `setFragmentText` | SETTER | - | fragment_text |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_files.py`)


```python

def test_RPFileFragment_get_fragment_element_delegates_to_com():
    fake = make_fake_element("FileFragment")
    inner = make_fake_element("X", getName="y")
    fake.getFragmentElement.return_value = inner
    obj = RPFileFragment(fake)
    result = obj.get_fragment_element()
    assert result.getName() == "y"


def test_RPFileFragment_get_fragment_text_delegates_to_com():
    fake = make_fake_element("FileFragment")
    fake.getFragmentText.return_value = "value"
    obj = RPFileFragment(fake)
    assert obj.get_fragment_text() == "value"


def test_RPFileFragment_get_fragment_type_delegates_to_com():
    fake = make_fake_element("FileFragment")
    fake.getFragmentType.return_value = "value"
    obj = RPFileFragment(fake)
    assert obj.get_fragment_type() == "value"


def test_RPFileFragment_move_fragment_in_owner_delegates_to_com():
    fake = make_fake_element("FileFragment")
    obj = RPFileFragment(fake)
    obj.move_fragment_in_owner(1)
    fake.moveFragmentInOwner.assert_called_once_with(1)


def test_RPFileFragment_set_fragment_text_delegates_to_com():
    fake = make_fake_element("FileFragment")
    obj = RPFileFragment(fake)
    obj.set_fragment_text("file.txt")
    fake.setFragmentText.assert_called_once_with("file.txt")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_files.py -k RPFileFragment -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPFileFragment`)

```python

    def get_fragment_element(self) -> RPModelElement:

        # (keep existing docstring)

        return AbstractRPModelElement.wrap(self._get_method_or_property(self._com, "getFragmentElement", "fragmentElement"))

    def get_fragment_text(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFragmentText", "fragmentText"))

    def get_fragment_type(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFragmentType", "fragmentType"))

    def move_fragment_in_owner(self, up: int) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.moveFragmentInOwner(up))

    def set_fragment_text(self, fragment_text: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setFragmentText", "fragmentText", fragment_text)

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_files.py -k RPFileFragment -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_files.py` for class `RPFileFragment`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_files.py tests/unit/models/support/test_files.py
git commit -m "feat(support): implement RPFileFragment methods with tests"
```


## Task 5: Implement `RPAXViewCtrl` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPAXViewCtrl`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPAXViewCtrl` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `do_command` | `doCommand` | ACTION | - | command_i_d |

| `execute_command` | `executeCommand` | ACTION | - | command_type, p_command_initialization→._com, p_command_result→._com |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from tests.unit.models.fakes import make_fake_collection, make_fake_element
from rhapsody_cli.models.support.model_ide import (
    RPAXViewCtrl, RPExternalIDERegistry, RPInternalOEMPlugin, RPJavaPlugins,
    RPPlugInWindow, RPProgressBar, RPSelection, RPowListListener,
    RPowPaneMgr, RPowTextListener,
)

def test_RPAXViewCtrl_do_command_delegates_to_com():
    fake = make_fake_element("AXViewCtrl")
    obj = RPAXViewCtrl(fake)
    obj.do_command(1)
    fake.doCommand.assert_called_once_with(1)


def test_RPAXViewCtrl_execute_command_delegates_to_com():
    fake = make_fake_element("AXViewCtrl")
    coll = RPCollection(make_fake_collection([make_fake_element('X')]))
    coll = RPCollection(make_fake_collection([make_fake_element('X')]))
    obj = RPAXViewCtrl(fake)
    obj.execute_command("x", coll, coll)
    fake.executeCommand.assert_called_once_with("x", coll._com, coll._com)


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPAXViewCtrl -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPAXViewCtrl`)

```python

    def do_command(self, command_i_d: int) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.doCommand(command_i_d))

    def execute_command(self, command_type: str, p_command_initialization: RPCollection, p_command_result: RPCollection) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.executeCommand(command_type, p_command_initialization._com, p_command_result._com))

```



> **Imports:** ensure `src/rhapsody_cli/models/support/model_ide.py` also imports what the bodies below need (add to the existing `from rhapsody_cli.models.core import ...` line / module top):
```python
from rhapsody_cli.models.core import RPCollection  # add to existing core import
from rhapsody_cli.application import RhapsodyApplication
```


- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPAXViewCtrl -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPAXViewCtrl`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPAXViewCtrl methods with tests"
```


## Task 6: Implement `RPExternalIDERegistry` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPExternalIDERegistry`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPExternalIDERegistry` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `progress_task_asynch_callback` | `progressTaskAsynchCallback` | ACTION | - | n_group_number, n_task_number |

| `progress_task_asynch_eliminate` | `progressTaskAsynchEliminate` | ACTION | - | n_group_number, n_task_number |

| `send_i_d_e_text_message` | `sendIDETextMessage` | ACTION | - | message |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

def test_RPExternalIDERegistry_progress_task_asynch_callback_delegates_to_com():
    fake = make_fake_element("ExternalIDERegistry")
    obj = RPExternalIDERegistry(fake)
    obj.progress_task_asynch_callback(1, 1)
    fake.progressTaskAsynchCallback.assert_called_once_with(1, 1)


def test_RPExternalIDERegistry_progress_task_asynch_eliminate_delegates_to_com():
    fake = make_fake_element("ExternalIDERegistry")
    obj = RPExternalIDERegistry(fake)
    obj.progress_task_asynch_eliminate(1, 1)
    fake.progressTaskAsynchEliminate.assert_called_once_with(1, 1)


def test_RPExternalIDERegistry_send_i_d_e_text_message_delegates_to_com():
    fake = make_fake_element("ExternalIDERegistry")
    obj = RPExternalIDERegistry(fake)
    obj.send_i_d_e_text_message("x")
    fake.sendIDETextMessage.assert_called_once_with("x")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPExternalIDERegistry -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPExternalIDERegistry`)

```python

    def progress_task_asynch_callback(self, n_group_number: int, n_task_number: int) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.progressTaskAsynchCallback(n_group_number, n_task_number))

    def progress_task_asynch_eliminate(self, n_group_number: int, n_task_number: int) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.progressTaskAsynchEliminate(n_group_number, n_task_number))

    def send_i_d_e_text_message(self, message: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.sendIDETextMessage(message))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPExternalIDERegistry -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPExternalIDERegistry`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPExternalIDERegistry methods with tests"
```


## Task 7: Implement `RPInternalOEMPlugin` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPInternalOEMPlugin`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPInternalOEMPlugin` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `active_project_about_to_change` | `activeProjectAboutToChange` | ACTION | (raw) | - |

| `active_project_has_changed` | `activeProjectHasChanged` | ACTION | (raw) | - |

| `on_menu_item_select` | `onMenuItemSelect` | ACTION | (raw) | menu_item |

| `on_menu_item_select_with_parameters` | `onMenuItemSelectWithParameters` | ACTION | (raw) | menu_item, parameters |

| `rhap_plugin_animation_stopped` | `rhapPluginAnimationStopped` | ACTION | (raw) | - |

| `rhp_plugin_animation_started` | `rhpPluginAnimationStarted` | ACTION | (raw) | - |

| `rhp_plugin_cleanup` | `rhpPluginCleanup` | ACTION | (raw) | - |

| `rhp_plugin_do_command` | `rhpPluginDoCommand` | ACTION | - | the_command |

| `rhp_plugin_final_cleanup` | `rhpPluginFinalCleanup` | ACTION | (raw) | - |

| `rhp_plugin_init` | `rhpPluginInit` | ACTION | (raw) | - |

| `rhp_plugin_invoke_item` | `rhpPluginInvokeItem` | ACTION | (raw) | - |

| `rhp_plugin_on_i_d_e_build_done` | `rhpPluginOnIDEBuildDone` | ACTION | - | build_status |

| `rhp_plugin_set_application` | `rhpPluginSetApplication` | ACTION | (raw) | p_r_p_app→._com |

| `rhp_saving_project` | `rhpSavingProject` | ACTION | (raw) | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

def test_RPInternalOEMPlugin_active_project_about_to_change_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.activeProjectAboutToChange.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.active_project_about_to_change()
    fake.activeProjectAboutToChange.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_active_project_has_changed_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.activeProjectHasChanged.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.active_project_has_changed()
    fake.activeProjectHasChanged.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_on_menu_item_select_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.onMenuItemSelect.return_value = "value"
    obj = RPInternalOEMPlugin(fake)
    result = obj.on_menu_item_select("x")
    fake.onMenuItemSelect.assert_called_once_with("x")
    assert result == "value"


def test_RPInternalOEMPlugin_on_menu_item_select_with_parameters_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.onMenuItemSelectWithParameters.return_value = "value"
    obj = RPInternalOEMPlugin(fake)
    result = obj.on_menu_item_select_with_parameters("x", "x")
    fake.onMenuItemSelectWithParameters.assert_called_once_with("x", "x")
    assert result == "value"


def test_RPInternalOEMPlugin_rhap_plugin_animation_stopped_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhapPluginAnimationStopped.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhap_plugin_animation_stopped()
    fake.rhapPluginAnimationStopped.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_animation_started_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginAnimationStarted.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_animation_started()
    fake.rhpPluginAnimationStarted.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_cleanup_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginCleanup.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_cleanup()
    fake.rhpPluginCleanup.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_do_command_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    obj = RPInternalOEMPlugin(fake)
    obj.rhp_plugin_do_command("x")
    fake.rhpPluginDoCommand.assert_called_once_with("x")


def test_RPInternalOEMPlugin_rhp_plugin_final_cleanup_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginFinalCleanup.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_final_cleanup()
    fake.rhpPluginFinalCleanup.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_init_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginInit.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_init()
    fake.rhpPluginInit.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_invoke_item_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginInvokeItem.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_invoke_item()
    fake.rhpPluginInvokeItem.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_on_i_d_e_build_done_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    obj = RPInternalOEMPlugin(fake)
    obj.rhp_plugin_on_i_d_e_build_done("x")
    fake.rhpPluginOnIDEBuildDone.assert_called_once_with("x")


def test_RPInternalOEMPlugin_rhp_plugin_set_application_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    target = make_fake_element("X")
    fake.rhpPluginSetApplication.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_set_application(AbstractRPModelElement.wrap(target))
    fake.rhpPluginSetApplication.assert_called_once_with(target)
    assert result == 1


def test_RPInternalOEMPlugin_rhp_saving_project_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpSavingProject.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_saving_project()
    fake.rhpSavingProject.assert_called_once_with()
    assert result == 1


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPInternalOEMPlugin -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPInternalOEMPlugin`)

```python

    def active_project_about_to_change(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.activeProjectAboutToChange()))

    def active_project_has_changed(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.activeProjectHasChanged()))

    def on_menu_item_select(self, menu_item: str) -> str:

        # (keep existing docstring)

        return str(self.call_com(lambda: self._com.onMenuItemSelect(menu_item)))

    def on_menu_item_select_with_parameters(self, menu_item: str, parameters: str) -> str:

        # (keep existing docstring)

        return str(self.call_com(lambda: self._com.onMenuItemSelectWithParameters(menu_item, parameters)))

    def rhap_plugin_animation_stopped(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.rhapPluginAnimationStopped()))

    def rhp_plugin_animation_started(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.rhpPluginAnimationStarted()))

    def rhp_plugin_cleanup(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.rhpPluginCleanup()))

    def rhp_plugin_do_command(self, the_command: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.rhpPluginDoCommand(the_command))

    def rhp_plugin_final_cleanup(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.rhpPluginFinalCleanup()))

    def rhp_plugin_init(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.rhpPluginInit()))

    def rhp_plugin_invoke_item(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.rhpPluginInvokeItem()))

    def rhp_plugin_on_i_d_e_build_done(self, build_status: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.rhpPluginOnIDEBuildDone(build_status))

    def rhp_plugin_set_application(self, p_r_p_app: RhapsodyApplication) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.rhpPluginSetApplication(p_r_p_app._com)))

    def rhp_saving_project(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.rhpSavingProject()))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPInternalOEMPlugin -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPInternalOEMPlugin`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPInternalOEMPlugin methods with tests"
```


## Task 8: Implement `RPJavaPlugins` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPJavaPlugins`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPJavaPlugins` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPJavaPlugins -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPJavaPlugins`)

```python

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPJavaPlugins -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPJavaPlugins`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPJavaPlugins methods with tests"
```


## Task 9: Implement `RPPlugInWindow` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPPlugInWindow`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPPlugInWindow` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `destroy_window` | `destroyWindow` | ACTION | - | - |

| `get_docking` | `getDocking` | GETTER | (raw) | - |

| `get_pos_string` | `getPosString` | GETTER | (raw) | - |

| `get_window_handle` | `getWindowHandle` | GETTER | (raw) | - |

| `set_docking` | `setDocking` | SETTER | - | n_dock_pos |

| `set_pos_string` | `setPosString` | SETTER | - | s_pos |

| `set_title` | `setTitle` | SETTER | - | s_title |

| `show_window` | `showWindow` | ACTION | - | n_show |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

def test_RPPlugInWindow_destroy_window_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.destroy_window()
    fake.destroyWindow.assert_called_once_with()


def test_RPPlugInWindow_get_docking_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    fake.getDocking.return_value = 1
    obj = RPPlugInWindow(fake)
    assert obj.get_docking() == 1


def test_RPPlugInWindow_get_pos_string_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    fake.getPosString.return_value = "value"
    obj = RPPlugInWindow(fake)
    assert obj.get_pos_string() == "value"


def test_RPPlugInWindow_get_window_handle_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    fake.getWindowHandle.return_value = 1
    obj = RPPlugInWindow(fake)
    assert obj.get_window_handle() == 1


def test_RPPlugInWindow_set_docking_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.set_docking(1)
    fake.setDocking.assert_called_once_with(1)


def test_RPPlugInWindow_set_pos_string_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.set_pos_string("file.txt")
    fake.setPosString.assert_called_once_with("file.txt")


def test_RPPlugInWindow_set_title_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.set_title("file.txt")
    fake.setTitle.assert_called_once_with("file.txt")


def test_RPPlugInWindow_show_window_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.show_window(1)
    fake.showWindow.assert_called_once_with(1)


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPPlugInWindow -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPPlugInWindow`)

```python

    def destroy_window(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.destroyWindow())

    def get_docking(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getDocking", "docking"))

    def get_pos_string(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getPosString", "posString"))

    def get_window_handle(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getWindowHandle", "windowHandle"))

    def set_docking(self, n_dock_pos: int) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setDocking", "docking", n_dock_pos)

    def set_pos_string(self, s_pos: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setPosString", "posString", s_pos)

    def set_title(self, s_title: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setTitle", "title", s_title)

    def show_window(self, n_show: int) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.showWindow(n_show))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPPlugInWindow -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPPlugInWindow`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPPlugInWindow methods with tests"
```


## Task 10: Implement `RPProgressBar` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPProgressBar`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPProgressBar` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `reset` | `reset` | ACTION | - | - |

| `tick` | `tick` | ACTION | - | amount |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

def test_RPProgressBar_reset_delegates_to_com():
    fake = make_fake_element("ProgressBar")
    obj = RPProgressBar(fake)
    obj.reset()
    fake.reset.assert_called_once_with()


def test_RPProgressBar_tick_delegates_to_com():
    fake = make_fake_element("ProgressBar")
    obj = RPProgressBar(fake)
    obj.tick(1)
    fake.tick.assert_called_once_with(1)


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPProgressBar -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPProgressBar`)

```python

    def reset(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.reset())

    def tick(self, amount: int) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.tick(amount))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPProgressBar -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPProgressBar`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPProgressBar methods with tests"
```


## Task 11: Implement `RPSelection` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPSelection`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPSelection` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `can_copy` | `canCopy` | ACTION | (raw) | - |

| `can_cut` | `canCut` | ACTION | (raw) | - |

| `can_delete` | `canDelete` | ACTION | (raw) | - |

| `can_paste` | `canPaste` | ACTION | (raw) | - |

| `copy_selected` | `copySelected` | ACTION | (raw) | - |

| `cut_selected` | `cutSelected` | ACTION | (raw) | - |

| `delete_selected` | `deleteSelected` | ACTION | (raw) | - |

| `paste_selected` | `pasteSelected` | ACTION | (raw) | - |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

def test_RPSelection_can_copy_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.canCopy.return_value = 1
    obj = RPSelection(fake)
    result = obj.can_copy()
    fake.canCopy.assert_called_once_with()
    assert result == 1


def test_RPSelection_can_cut_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.canCut.return_value = 1
    obj = RPSelection(fake)
    result = obj.can_cut()
    fake.canCut.assert_called_once_with()
    assert result == 1


def test_RPSelection_can_delete_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.canDelete.return_value = 1
    obj = RPSelection(fake)
    result = obj.can_delete()
    fake.canDelete.assert_called_once_with()
    assert result == 1


def test_RPSelection_can_paste_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.canPaste.return_value = 1
    obj = RPSelection(fake)
    result = obj.can_paste()
    fake.canPaste.assert_called_once_with()
    assert result == 1


def test_RPSelection_copy_selected_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.copySelected.return_value = 1
    obj = RPSelection(fake)
    result = obj.copy_selected()
    fake.copySelected.assert_called_once_with()
    assert result == 1


def test_RPSelection_cut_selected_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.cutSelected.return_value = 1
    obj = RPSelection(fake)
    result = obj.cut_selected()
    fake.cutSelected.assert_called_once_with()
    assert result == 1


def test_RPSelection_delete_selected_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.deleteSelected.return_value = 1
    obj = RPSelection(fake)
    result = obj.delete_selected()
    fake.deleteSelected.assert_called_once_with()
    assert result == 1


def test_RPSelection_paste_selected_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.pasteSelected.return_value = 1
    obj = RPSelection(fake)
    result = obj.paste_selected()
    fake.pasteSelected.assert_called_once_with()
    assert result == 1


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPSelection -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPSelection`)

```python

    def can_copy(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.canCopy()))

    def can_cut(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.canCut()))

    def can_delete(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.canDelete()))

    def can_paste(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.canPaste()))

    def copy_selected(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.copySelected()))

    def cut_selected(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.cutSelected()))

    def delete_selected(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.deleteSelected()))

    def paste_selected(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.pasteSelected()))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPSelection -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPSelection`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPSelection methods with tests"
```


## Task 12: Implement `RPowListListener` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPowListListener`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPowListListener` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `dbl_click_notify` | `dblClickNotify` | ACTION | - | n_row, n_col, s_content |

| `set_obj_i_d` | `setObjID` | SETTER | - | bstr_obj_i_d |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

def test_RPowListListener_dbl_click_notify_delegates_to_com():
    fake = make_fake_element("owListListener")
    obj = RPowListListener(fake)
    obj.dbl_click_notify(1, 1, "x")
    fake.dblClickNotify.assert_called_once_with(1, 1, "x")


def test_RPowListListener_set_obj_i_d_delegates_to_com():
    fake = make_fake_element("owListListener")
    obj = RPowListListener(fake)
    obj.set_obj_i_d("file.txt")
    fake.setObjID.assert_called_once_with("file.txt")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPowListListener -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPowListListener`)

```python

    def dbl_click_notify(self, n_row: int, n_col: int, s_content: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.dblClickNotify(n_row, n_col, s_content))

    def set_obj_i_d(self, bstr_obj_i_d: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setObjID", "objID", bstr_obj_i_d)

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPowListListener -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPowListListener`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPowListListener methods with tests"
```


## Task 13: Implement `RPowPaneMgr` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPowPaneMgr`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPowPaneMgr` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `add_tab_notify` | `addTabNotify` | ACTION | - | n_type, n_sub_type, s_obj_i_d, s_title |

| `close_tab_notify` | `closeTabNotify` | ACTION | - | s_obj_i_d |

| `get_o_w_list_listener` | `getOWListListener` | GETTER | RPowListListener | s_obj_i_d |

| `get_o_w_text_listener` | `getOWTextListener` | GETTER | RPowTextListener | s_obj_i_d |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

def test_RPowPaneMgr_add_tab_notify_delegates_to_com():
    fake = make_fake_element("owPaneMgr")
    obj = RPowPaneMgr(fake)
    obj.add_tab_notify(1, 1, "x", "x")
    fake.addTabNotify.assert_called_once_with(1, 1, "x", "x")


def test_RPowPaneMgr_close_tab_notify_delegates_to_com():
    fake = make_fake_element("owPaneMgr")
    obj = RPowPaneMgr(fake)
    obj.close_tab_notify("x")
    fake.closeTabNotify.assert_called_once_with("x")


def test_RPowPaneMgr_get_o_w_list_listener_delegates_to_com():
    fake = make_fake_element("owPaneMgr")
    inner = make_fake_element("X", getName="y")
    fake.getOWListListener.return_value = inner
    obj = RPowPaneMgr(fake)
    result = obj.get_o_w_list_listener()
    assert isinstance(result, RPowListListener)


def test_RPowPaneMgr_get_o_w_text_listener_delegates_to_com():
    fake = make_fake_element("owPaneMgr")
    inner = make_fake_element("X", getName="y")
    fake.getOWTextListener.return_value = inner
    obj = RPowPaneMgr(fake)
    result = obj.get_o_w_text_listener()
    assert isinstance(result, RPowTextListener)


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPowPaneMgr -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPowPaneMgr`)

```python

    def add_tab_notify(self, n_type: int, n_sub_type: int, s_obj_i_d: str, s_title: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addTabNotify(n_type, n_sub_type, s_obj_i_d, s_title))

    def close_tab_notify(self, s_obj_i_d: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.closeTabNotify(s_obj_i_d))

    def get_o_w_list_listener(self, s_obj_i_d: str) -> RPowListListener:

        # (keep existing docstring)

        return RPowListListener(self._get_method_or_property(self._com, "getOWListListener", "oWListListener"))

    def get_o_w_text_listener(self, s_obj_i_d: str) -> RPowTextListener:

        # (keep existing docstring)

        return RPowTextListener(self._get_method_or_property(self._com, "getOWTextListener", "oWTextListener"))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPowPaneMgr -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPowPaneMgr`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPowPaneMgr methods with tests"
```


## Task 14: Implement `RPowTextListener` (ide)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_ide.py` (class `RPowTextListener`)

- Test: `tests/unit/models/support/test_ide.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPowTextListener` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `dbl_click_notify` | `dblClickNotify` | ACTION | - | n_line, sz_line |

| `set_obj_i_d` | `setObjID` | SETTER | - | bstr_obj_i_d |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_ide.py`)


```python

def test_RPowTextListener_dbl_click_notify_delegates_to_com():
    fake = make_fake_element("owTextListener")
    obj = RPowTextListener(fake)
    obj.dbl_click_notify(1, "x")
    fake.dblClickNotify.assert_called_once_with(1, "x")


def test_RPowTextListener_set_obj_i_d_delegates_to_com():
    fake = make_fake_element("owTextListener")
    obj = RPowTextListener(fake)
    obj.set_obj_i_d("file.txt")
    fake.setObjID.assert_called_once_with("file.txt")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_ide.py -k RPowTextListener -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPowTextListener`)

```python

    def dbl_click_notify(self, n_line: int, sz_line: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.dblClickNotify(n_line, sz_line))

    def set_obj_i_d(self, bstr_obj_i_d: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setObjID", "objID", bstr_obj_i_d)

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_ide.py -k RPowTextListener -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_ide.py` for class `RPowTextListener`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py tests/unit/models/support/test_ide.py
git commit -m "feat(support): implement RPowTextListener methods with tests"
```


## Task 15: Implement `RPBaseExternalCodeGeneratorTool` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPBaseExternalCodeGeneratorTool`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPBaseExternalCodeGeneratorTool` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `advance_code_gen_progress_bar` | `advanceCodeGenProgressBar` | ACTION | - | - |

| `should_abort_code_generation` | `shouldAbortCodeGeneration` | ACTION | (raw) | - |

| `write_code_gen_message` | `writeCodeGenMessage` | ACTION | - | msg |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from tests.unit.models.fakes import make_fake_collection, make_fake_element
from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.models.support.model_codegen import (
    RPBaseExternalCodeGeneratorTool, RPCodeGenerator, RPDiagSynthAPI,
    RPExternalCheckRegistry, RPExternalRoundtripInvoker, RPIntegrator,
    RPRhapsodyServer, RPRoundTrip, RPSearchManager, RPSearchQuery,
    RPSearchResult, RPCodeGenSimplifiersRegistry, RPExternalCodeGeneratorInvoker,
)
from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.models.elements.graphics.model_graphics import RPTableLayout

def test_RPBaseExternalCodeGeneratorTool_advance_code_gen_progress_bar_delegates_to_com():
    fake = make_fake_element("BaseExternalCodeGeneratorTool")
    obj = RPBaseExternalCodeGeneratorTool(fake)
    obj.advance_code_gen_progress_bar()
    fake.advanceCodeGenProgressBar.assert_called_once_with()


def test_RPBaseExternalCodeGeneratorTool_should_abort_code_generation_delegates_to_com():
    fake = make_fake_element("BaseExternalCodeGeneratorTool")
    fake.shouldAbortCodeGeneration.return_value = 1
    obj = RPBaseExternalCodeGeneratorTool(fake)
    result = obj.should_abort_code_generation()
    fake.shouldAbortCodeGeneration.assert_called_once_with()
    assert result == 1


def test_RPBaseExternalCodeGeneratorTool_write_code_gen_message_delegates_to_com():
    fake = make_fake_element("BaseExternalCodeGeneratorTool")
    obj = RPBaseExternalCodeGeneratorTool(fake)
    obj.write_code_gen_message("x")
    fake.writeCodeGenMessage.assert_called_once_with("x")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPBaseExternalCodeGeneratorTool -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPBaseExternalCodeGeneratorTool`)

```python

    def advance_code_gen_progress_bar(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.advanceCodeGenProgressBar())

    def should_abort_code_generation(self) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.shouldAbortCodeGeneration()))

    def write_code_gen_message(self, msg: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.writeCodeGenMessage(msg))

```



> **Imports:** ensure `src/rhapsody_cli/models/support/model_codegen.py` also imports what the bodies below need (add to the existing `from rhapsody_cli.models.core import ...` line / module top):
```python
from rhapsody_cli.models.core import RPCollection  # add to existing core import
from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.models.elements.classifiers.model_stereotype import RPStereotype
from rhapsody_cli.models.elements.containment.model_package import RPPackage
from rhapsody_cli.models.elements.diagrams.model_diagram_types import RPSequenceDiagram
from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram
from rhapsody_cli.models.elements.graphics.model_graphics import RPMatrixView
from rhapsody_cli.models.elements.graphics.model_graphics import RPTableLayout
from rhapsody_cli.models.elements.graphics.model_graphics import RPTableView
```


- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPBaseExternalCodeGeneratorTool -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPBaseExternalCodeGeneratorTool`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPBaseExternalCodeGeneratorTool methods with tests"
```


## Task 16: Implement `RPCodeGenerator` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPCodeGenerator`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPCodeGenerator` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `get_code_annotations` | `getCodeAnnotations` | GETTER | RPCollection | element→._com, b_spec_file |

| `get_generated_file_names` | `getGeneratedFileNames` | GETTER | RPCollection | element→._com |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPCodeGenerator_get_code_annotations_delegates_to_com():
    fake = make_fake_element("CodeGenerator")
    inner = make_fake_element("X", getName="y")
    fake.getCodeAnnotations.return_value = make_fake_collection([inner])
    obj = RPCodeGenerator(fake)
    result = obj.get_code_annotations()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPCodeGenerator_get_generated_file_names_delegates_to_com():
    fake = make_fake_element("CodeGenerator")
    inner = make_fake_element("X", getName="y")
    fake.getGeneratedFileNames.return_value = make_fake_collection([inner])
    obj = RPCodeGenerator(fake)
    result = obj.get_generated_file_names()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPCodeGenerator -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPCodeGenerator`)

```python

    def get_code_annotations(self, element: RPModelElement, b_spec_file: int) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getCodeAnnotations", "codeAnnotations"))

    def get_generated_file_names(self, element: RPModelElement) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getGeneratedFileNames", "generatedFileNames"))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPCodeGenerator -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPCodeGenerator`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPCodeGenerator methods with tests"
```


## Task 17: Implement `RPDiagSynthAPI` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPDiagSynthAPI`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPDiagSynthAPI` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `add_instance` | `addInstance` | ACTION | (raw) | added_to_s_d, instance_nav_exp |

| `add_synth_s_d_to_model2` | `addSynthSDToModel2` | ACTION | (raw) | p_msc_orig→._com, synth_s_d, open_s_d |

| `create_s_d2` | `createSD2` | ACTION | (raw) | p_msc_orig→._com, testedmscname |

| `receive_message` | `receiveMessage` | ACTION | - | p_tested_s_d, p_event_sent |

| `remove_synth_s_d_to_model2` | `removeSynthSDToModel2` | ACTION | (raw) | p_msc_orig→._com |

| `s_d_add_condition_mark` | `sDAddConditionMark` | ACTION | (raw) | p_tested_s_d, instance, text, type_ |

| `send_message` | `sendMessage` | ACTION | (raw) | p_tested_s_d, source, target, event, operation, type_ |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPDiagSynthAPI_add_instance_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    fake.addInstance.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.add_instance(1, "x")
    fake.addInstance.assert_called_once_with(1, "x")
    assert result == 1


def test_RPDiagSynthAPI_add_synth_s_d_to_model2_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    target = make_fake_element("X")
    fake.addSynthSDToModel2.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.add_synth_s_d_to_model2(AbstractRPModelElement.wrap(target), 1, 1)
    fake.addSynthSDToModel2.assert_called_once_with(target, 1, 1)
    assert result == 1


def test_RPDiagSynthAPI_create_s_d2_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    target = make_fake_element("X")
    fake.createSD2.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.create_s_d2(AbstractRPModelElement.wrap(target), "x")
    fake.createSD2.assert_called_once_with(target, "x")
    assert result == 1


def test_RPDiagSynthAPI_receive_message_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    obj = RPDiagSynthAPI(fake)
    obj.receive_message(1, 1)
    fake.receiveMessage.assert_called_once_with(1, 1)


def test_RPDiagSynthAPI_remove_synth_s_d_to_model2_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    target = make_fake_element("X")
    fake.removeSynthSDToModel2.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.remove_synth_s_d_to_model2(AbstractRPModelElement.wrap(target))
    fake.removeSynthSDToModel2.assert_called_once_with(target)
    assert result == 1


def test_RPDiagSynthAPI_s_d_add_condition_mark_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    fake.sDAddConditionMark.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.s_d_add_condition_mark(1, "x", "x", "x")
    fake.sDAddConditionMark.assert_called_once_with(1, "x", "x", "x")
    assert result == 1


def test_RPDiagSynthAPI_send_message_delegates_to_com():
    fake = make_fake_element("DiagSynthAPI")
    fake.sendMessage.return_value = 1
    obj = RPDiagSynthAPI(fake)
    result = obj.send_message(1, "x", "x", "x", "x", "x")
    fake.sendMessage.assert_called_once_with(1, "x", "x", "x", "x", "x")
    assert result == 1


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPDiagSynthAPI -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPDiagSynthAPI`)

```python

    def add_instance(self, added_to_s_d: int, instance_nav_exp: str) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.addInstance(added_to_s_d, instance_nav_exp)))

    def add_synth_s_d_to_model2(self, p_msc_orig: RPSequenceDiagram, synth_s_d: int, open_s_d: int) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.addSynthSDToModel2(p_msc_orig._com, synth_s_d, open_s_d)))

    def create_s_d2(self, p_msc_orig: RPSequenceDiagram, testedmscname: str) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.createSD2(p_msc_orig._com, testedmscname)))

    def receive_message(self, p_tested_s_d: int, p_event_sent: int) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.receiveMessage(p_tested_s_d, p_event_sent))

    def remove_synth_s_d_to_model2(self, p_msc_orig: RPSequenceDiagram) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.removeSynthSDToModel2(p_msc_orig._com)))

    def s_d_add_condition_mark(self, p_tested_s_d: int, instance: str, text: str, type_: str) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.sDAddConditionMark(p_tested_s_d, instance, text, type_)))

    def send_message(self, p_tested_s_d: int, source: str, target: str, event: str, operation: str, type_: str) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.sendMessage(p_tested_s_d, source, target, event, operation, type_)))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPDiagSynthAPI -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPDiagSynthAPI`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPDiagSynthAPI methods with tests"
```


## Task 18: Implement `RPExternalCheckRegistry` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPExternalCheckRegistry`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPExternalCheckRegistry` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `append_failed_elements_comments` | `appendFailedElementsComments` | ACTION | - | str_val |

| `set_failed_elements_comments` | `setFailedElementsComments` | SETTER | - | str_val |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPExternalCheckRegistry_append_failed_elements_comments_delegates_to_com():
    fake = make_fake_element("ExternalCheckRegistry")
    obj = RPExternalCheckRegistry(fake)
    obj.append_failed_elements_comments("x")
    fake.appendFailedElementsComments.assert_called_once_with("x")


def test_RPExternalCheckRegistry_set_failed_elements_comments_delegates_to_com():
    fake = make_fake_element("ExternalCheckRegistry")
    obj = RPExternalCheckRegistry(fake)
    obj.set_failed_elements_comments("file.txt")
    fake.setFailedElementsComments.assert_called_once_with("file.txt")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPExternalCheckRegistry -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPExternalCheckRegistry`)

```python

    def append_failed_elements_comments(self, str_val: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.appendFailedElementsComments(str_val))

    def set_failed_elements_comments(self, str_val: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setFailedElementsComments", "failedElementsComments", str_val)

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPExternalCheckRegistry -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPExternalCheckRegistry`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPExternalCheckRegistry methods with tests"
```


## Task 19: Implement `RPExternalRoundtripInvoker` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPExternalRoundtripInvoker`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPExternalRoundtripInvoker` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPExternalRoundtripInvoker -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPExternalRoundtripInvoker`)

```python

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPExternalRoundtripInvoker -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPExternalRoundtripInvoker`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPExternalRoundtripInvoker methods with tests"
```


## Task 20: Implement `RPIntegrator` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPIntegrator`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPIntegrator` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPIntegrator -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPIntegrator`)

```python

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPIntegrator -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPIntegrator`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPIntegrator methods with tests"
```


## Task 21: Implement `RPRhapsodyServer` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPRhapsodyServer`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPRhapsodyServer` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `get_application` | `getApplication` | GETTER | RhapsodyApplication | - |

| `get_hidden_application` | `getHiddenApplication` | GETTER | RhapsodyApplication | - |

| `get_uninitialized_application` | `getUninitializedApplication` | GETTER | RhapsodyApplication | - |

| `initialize_application` | `initializeApplication` | ACTION | - | p_val→._com |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPRhapsodyServer_get_application_delegates_to_com():
    fake = make_fake_element("RhapsodyServer")
    app_fake = make_fake_element("Application")
    fake.getApplication.return_value = app_fake
    obj = RPRhapsodyServer(fake)
    result = obj.get_application()
    assert isinstance(result, RhapsodyApplication)


def test_RPRhapsodyServer_get_hidden_application_delegates_to_com():
    fake = make_fake_element("RhapsodyServer")
    app_fake = make_fake_element("Application")
    fake.getHiddenApplication.return_value = app_fake
    obj = RPRhapsodyServer(fake)
    result = obj.get_hidden_application()
    assert isinstance(result, RhapsodyApplication)


def test_RPRhapsodyServer_get_uninitialized_application_delegates_to_com():
    fake = make_fake_element("RhapsodyServer")
    app_fake = make_fake_element("Application")
    fake.getUninitializedApplication.return_value = app_fake
    obj = RPRhapsodyServer(fake)
    result = obj.get_uninitialized_application()
    assert isinstance(result, RhapsodyApplication)


def test_RPRhapsodyServer_initialize_application_delegates_to_com():
    fake = make_fake_element("RhapsodyServer")
    target = make_fake_element("X")
    obj = RPRhapsodyServer(fake)
    obj.initialize_application(AbstractRPModelElement.wrap(target))
    fake.initializeApplication.assert_called_once_with(target)


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPRhapsodyServer -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPRhapsodyServer`)

```python

    def get_application(self) -> RhapsodyApplication:

        # (keep existing docstring)

        return RhapsodyApplication(self._get_method_or_property(self._com, "getApplication", "application"))

    def get_hidden_application(self) -> RhapsodyApplication:

        # (keep existing docstring)

        return RhapsodyApplication(self._get_method_or_property(self._com, "getHiddenApplication", "hiddenApplication"))

    def get_uninitialized_application(self) -> RhapsodyApplication:

        # (keep existing docstring)

        return RhapsodyApplication(self._get_method_or_property(self._com, "getUninitializedApplication", "uninitializedApplication"))

    def initialize_application(self, p_val: RhapsodyApplication) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.initializeApplication(p_val._com))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPRhapsodyServer -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPRhapsodyServer`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPRhapsodyServer methods with tests"
```


## Task 22: Implement `RPRoundTrip` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPRoundTrip`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPRoundTrip` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `roundtrip_file` | `roundtripFile` | ACTION | RPCollection | filename, re_generate_file |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPRoundTrip_roundtrip_file_delegates_to_com():
    fake = make_fake_element("RoundTrip")
    inner = make_fake_element("X", getName="y")
    fake.roundtripFile.return_value = make_fake_collection([inner])
    obj = RPRoundTrip(fake)
    result = obj.roundtrip_file("x", 1)
    fake.roundtripFile.assert_called_once_with("x", 1)
    assert isinstance(result, RPCollection)
    assert len(result) == 1


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPRoundTrip -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPRoundTrip`)

```python

    def roundtrip_file(self, filename: str, re_generate_file: int) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self.call_com(lambda: self._com.roundtripFile(filename, re_generate_file)))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPRoundTrip -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPRoundTrip`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPRoundTrip methods with tests"
```


## Task 23: Implement `RPSearchManager` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPSearchManager`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPSearchManager` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `create_search_query` | `createSearchQuery` | ACTION | RPSearchQuery | - |

| `search` | `search` | ACTION | RPCollection | p_search_query→._com |

| `search_and_show_results` | `searchAndShowResults` | ACTION | - | p_search_query→._com |

| `search_async` | `searchAsync` | ACTION | - | p_search_query→._com |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPSearchManager_create_search_query_delegates_to_com():
    fake = make_fake_element("SearchManager")
    inner = make_fake_element("X", getName="y")
    fake.createSearchQuery.return_value = inner
    obj = RPSearchManager(fake)
    result = obj.create_search_query()
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
    obj.search_and_show_results(AbstractRPModelElement.wrap(target))
    fake.searchAndShowResults.assert_called_once_with(target)


def test_RPSearchManager_search_async_delegates_to_com():
    fake = make_fake_element("SearchManager")
    target = make_fake_element("X")
    obj = RPSearchManager(fake)
    obj.search_async(AbstractRPModelElement.wrap(target))
    fake.searchAsync.assert_called_once_with(target)


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPSearchManager -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPSearchManager`)

```python

    def create_search_query(self) -> RPSearchQuery:

        # (keep existing docstring)

        return RPSearchQuery(self.call_com(lambda: self._com.createSearchQuery()))

    def search(self, p_search_query: RPSearchQuery) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self.call_com(lambda: self._com.search(p_search_query._com)))

    def search_and_show_results(self, p_search_query: RPSearchQuery) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.searchAndShowResults(p_search_query._com))

    def search_async(self, p_search_query: RPSearchQuery) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.searchAsync(p_search_query._com))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPSearchManager -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPSearchManager`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPSearchManager methods with tests"
```


## Task 24: Implement `RPSearchQuery` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPSearchQuery`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPSearchQuery` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `add_diagram_to_views_list` | `addDiagramToViewsList` | ACTION | (raw) | view→._com |

| `add_filter_element_type` | `addFilterElementType` | ACTION | - | element_type |

| `add_filter_search_in_field` | `addFilterSearchInField` | ACTION | - | search_in_field |

| `add_filter_stereotype` | `addFilterStereotype` | ACTION | - | stereotype→._com |

| `add_filter_sub_query` | `addFilterSubQuery` | ACTION | - | sub_query→._com, use_with_not_operator |

| `add_matrix_to_views_list` | `addMatrixToViewsList` | ACTION | (raw) | view→._com |

| `add_search_scope` | `addSearchScope` | ACTION | - | scope_element→._com |

| `add_table_to_views_list` | `addTableToViewsList` | ACTION | (raw) | view→._com |

| `get_filter_element_types` | `getFilterElementTypes` | GETTER | RPCollection | - |

| `get_filter_reference_include_referenced_elements_in_search_results` | `getFilterReferenceIncludeReferencedElementsInSearchResults` | GETTER | (raw) | - |

| `get_filter_reference_name_of_referenced_elements` | `getFilterReferenceNameOfReferencedElements` | GETTER | (raw) | - |

| `get_filter_reference_number_of_references` | `getFilterReferenceNumberOfReferences` | GETTER | (raw) | - |

| `get_filter_reference_quantity_operator` | `getFilterReferenceQuantityOperator` | GETTER | (raw) | - |

| `get_filter_reference_relation_kind` | `getFilterReferenceRelationKind` | GETTER | (raw) | - |

| `get_filter_reference_stereotype_of_referenced_elements` | `getFilterReferenceStereotypeOfReferencedElements` | GETTER | (raw) | - |

| `get_filter_reference_type_of_referenced_elements` | `getFilterReferenceTypeOfReferencedElements` | GETTER | (raw) | - |

| `get_filter_search_in_fields` | `getFilterSearchInFields` | GETTER | RPCollection | - |

| `get_filter_stereotypes` | `getFilterStereotypes` | GETTER | RPCollection | - |

| `get_filter_sub_queries` | `getFilterSubQueries` | GETTER | RPCollection | - |

| `get_filter_sub_query_use_with_not_operator` | `getFilterSubQueryUseWithNotOperator` | GETTER | (raw) | sub_query→._com |

| `get_filter_tag_find_as` | `getFilterTagFindAs` | GETTER | (raw) | - |

| `get_filter_tag_match_case` | `getFilterTagMatchCase` | GETTER | (raw) | - |

| `get_filter_tag_match_whole_word` | `getFilterTagMatchWholeWord` | GETTER | (raw) | - |

| `get_filter_tag_name` | `getFilterTagName` | GETTER | (raw) | - |

| `get_filter_tag_value` | `getFilterTagValue` | GETTER | (raw) | - |

| `get_search_scope_elements` | `getSearchScopeElements` | GETTER | RPCollection | - |

| `get_view` | `getView` | GETTER | AbstractRPModelElement.wrap | index |

| `get_view_count` | `getViewCount` | GETTER | (raw) | - |

| `load_from_query` | `loadFromQuery` | ACTION | - | query→._com |

| `remove_filter_element_types` | `removeFilterElementTypes` | ACTION | - | - |

| `remove_filter_references` | `removeFilterReferences` | ACTION | - | - |

| `remove_filter_search_in_fields` | `removeFilterSearchInFields` | ACTION | - | - |

| `remove_filter_stereotypes` | `removeFilterStereotypes` | ACTION | - | - |

| `remove_filter_sub_queries` | `removeFilterSubQueries` | ACTION | - | - |

| `remove_filter_sub_query` | `removeFilterSubQuery` | ACTION | (raw) | sub_query→._com |

| `remove_filter_tag` | `removeFilterTag` | ACTION | - | - |

| `remove_search_scope_element` | `removeSearchScopeElement` | ACTION | (raw) | scope_element→._com |

| `remove_view` | `removeView` | ACTION | - | index |

| `reset_search_scope` | `resetSearchScope` | ACTION | - | - |

| `save_as_query` | `saveAsQuery` | ACTION | RPTableLayout | query_owner→._com |

| `set_filter_tag` | `setFilterTag` | SETTER | - | tag_name, tag_value, match_case, match_whole_word, find_as |

| `get_filter_sub_queries_operator` | `getFilterSubQueriesOperator` | GETTER | (raw) | - |

| `get_filter_tag_local_only` | `getFilterTagLocalOnly` | GETTER | (raw) | - |

| `get_filter_units_only` | `getFilterUnitsOnly` | GETTER | (raw) | - |

| `get_filter_unresolved_kind` | `getFilterUnresolvedKind` | GETTER | (raw) | - |

| `get_include_descendants` | `getIncludeDescendants` | GETTER | (raw) | - |

| `get_match_case` | `getMatchCase` | GETTER | (raw) | - |

| `get_match_specified_criteria` | `getMatchSpecifiedCriteria` | GETTER | (raw) | - |

| `get_match_whole_word` | `getMatchWholeWord` | GETTER | (raw) | - |

| `get_search_find_as_option` | `getSearchFindAsOption` | GETTER | (raw) | - |

| `get_search_scope_object` | `getSearchScopeObject` | GETTER | AbstractRPModelElement.wrap | - |

| `get_search_text` | `getSearchText` | GETTER | (raw) | - |

| `get_view_include_model_elements` | `getViewIncludeModelElements` | GETTER | (raw) | - |

| `get_views_to_search` | `getViewsToSearch` | GETTER | (raw) | - |

| `set_filter_sub_queries_operator` | `setFilterSubQueriesOperator` | SETTER | - | filter_sub_queries_operator |

| `set_filter_tag_local_only` | `setFilterTagLocalOnly` | SETTER | - | filter_tag_local_only |

| `set_filter_units_only` | `setFilterUnitsOnly` | SETTER | - | filter_units_only |

| `set_filter_unresolved_kind` | `setFilterUnresolvedKind` | SETTER | - | filter_unresolved_kind |

| `set_include_descendants` | `setIncludeDescendants` | SETTER | - | include_descendants |

| `set_match_case` | `setMatchCase` | SETTER | - | match_case |

| `set_match_specified_criteria` | `setMatchSpecifiedCriteria` | SETTER | - | match_specified_criteria |

| `set_match_whole_word` | `setMatchWholeWord` | SETTER | - | match_whole_word |

| `set_search_find_as_option` | `setSearchFindAsOption` | SETTER | - | search_find_as_option |

| `set_search_scope_object` | `setSearchScopeObject` | SETTER | - | search_scope_object→._com |

| `set_search_text` | `setSearchText` | SETTER | - | search_text |

| `set_view_include_model_elements` | `setViewIncludeModelElements` | SETTER | - | view_include_model_elements |

| `set_views_to_search` | `setViewsToSearch` | SETTER | - | views_to_search |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPSearchQuery_add_diagram_to_views_list_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.addDiagramToViewsList.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.add_diagram_to_views_list(AbstractRPModelElement.wrap(target))
    fake.addDiagramToViewsList.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_add_filter_element_type_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.add_filter_element_type("x")
    fake.addFilterElementType.assert_called_once_with("x")


def test_RPSearchQuery_add_filter_search_in_field_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.add_filter_search_in_field("x")
    fake.addFilterSearchInField.assert_called_once_with("x")


def test_RPSearchQuery_add_filter_stereotype_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.add_filter_stereotype(AbstractRPModelElement.wrap(target))
    fake.addFilterStereotype.assert_called_once_with(target)


def test_RPSearchQuery_add_filter_sub_query_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.add_filter_sub_query(AbstractRPModelElement.wrap(target), 1)
    fake.addFilterSubQuery.assert_called_once_with(target, 1)


def test_RPSearchQuery_add_matrix_to_views_list_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.addMatrixToViewsList.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.add_matrix_to_views_list(AbstractRPModelElement.wrap(target))
    fake.addMatrixToViewsList.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_add_search_scope_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.add_search_scope(AbstractRPModelElement.wrap(target))
    fake.addSearchScope.assert_called_once_with(target)


def test_RPSearchQuery_add_table_to_views_list_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.addTableToViewsList.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.add_table_to_views_list(AbstractRPModelElement.wrap(target))
    fake.addTableToViewsList.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_get_filter_element_types_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getFilterElementTypes.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.get_filter_element_types()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_filter_reference_include_referenced_elements_in_search_results_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceIncludeReferencedElementsInSearchResults.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_filter_reference_include_referenced_elements_in_search_results() == 1


def test_RPSearchQuery_get_filter_reference_name_of_referenced_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceNameOfReferencedElements.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_reference_name_of_referenced_elements() == "value"


def test_RPSearchQuery_get_filter_reference_number_of_references_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceNumberOfReferences.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_filter_reference_number_of_references() == 1


def test_RPSearchQuery_get_filter_reference_quantity_operator_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceQuantityOperator.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_reference_quantity_operator() == "value"


def test_RPSearchQuery_get_filter_reference_relation_kind_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceRelationKind.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_reference_relation_kind() == "value"


def test_RPSearchQuery_get_filter_reference_stereotype_of_referenced_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceStereotypeOfReferencedElements.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_reference_stereotype_of_referenced_elements() == "value"


def test_RPSearchQuery_get_filter_reference_type_of_referenced_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterReferenceTypeOfReferencedElements.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_reference_type_of_referenced_elements() == "value"


def test_RPSearchQuery_get_filter_search_in_fields_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getFilterSearchInFields.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.get_filter_search_in_fields()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_filter_stereotypes_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getFilterStereotypes.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.get_filter_stereotypes()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_filter_sub_queries_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getFilterSubQueries.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.get_filter_sub_queries()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_filter_sub_query_use_with_not_operator_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterSubQueryUseWithNotOperator.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_filter_sub_query_use_with_not_operator() == 1


def test_RPSearchQuery_get_filter_tag_find_as_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagFindAs.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_tag_find_as() == "value"


def test_RPSearchQuery_get_filter_tag_match_case_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagMatchCase.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_filter_tag_match_case() == 1


def test_RPSearchQuery_get_filter_tag_match_whole_word_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagMatchWholeWord.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_filter_tag_match_whole_word() == 1


def test_RPSearchQuery_get_filter_tag_name_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagName.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_tag_name() == "value"


def test_RPSearchQuery_get_filter_tag_value_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagValue.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_tag_value() == "value"


def test_RPSearchQuery_get_search_scope_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getSearchScopeElements.return_value = make_fake_collection([inner])
    obj = RPSearchQuery(fake)
    result = obj.get_search_scope_elements()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchQuery_get_view_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getView.return_value = inner
    obj = RPSearchQuery(fake)
    result = obj.get_view()
    assert result.getName() == "y"


def test_RPSearchQuery_get_view_count_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getViewCount.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_view_count() == 1


def test_RPSearchQuery_load_from_query_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.load_from_query(AbstractRPModelElement.wrap(target))
    fake.loadFromQuery.assert_called_once_with(target)


def test_RPSearchQuery_remove_filter_element_types_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.remove_filter_element_types()
    fake.removeFilterElementTypes.assert_called_once_with()


def test_RPSearchQuery_remove_filter_references_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.remove_filter_references()
    fake.removeFilterReferences.assert_called_once_with()


def test_RPSearchQuery_remove_filter_search_in_fields_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.remove_filter_search_in_fields()
    fake.removeFilterSearchInFields.assert_called_once_with()


def test_RPSearchQuery_remove_filter_stereotypes_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.remove_filter_stereotypes()
    fake.removeFilterStereotypes.assert_called_once_with()


def test_RPSearchQuery_remove_filter_sub_queries_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.remove_filter_sub_queries()
    fake.removeFilterSubQueries.assert_called_once_with()


def test_RPSearchQuery_remove_filter_sub_query_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.removeFilterSubQuery.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.remove_filter_sub_query(AbstractRPModelElement.wrap(target))
    fake.removeFilterSubQuery.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_remove_filter_tag_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.remove_filter_tag()
    fake.removeFilterTag.assert_called_once_with()


def test_RPSearchQuery_remove_search_scope_element_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    fake.removeSearchScopeElement.return_value = 1
    obj = RPSearchQuery(fake)
    result = obj.remove_search_scope_element(AbstractRPModelElement.wrap(target))
    fake.removeSearchScopeElement.assert_called_once_with(target)
    assert result == 1


def test_RPSearchQuery_remove_view_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.remove_view(1)
    fake.removeView.assert_called_once_with(1)


def test_RPSearchQuery_reset_search_scope_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.reset_search_scope()
    fake.resetSearchScope.assert_called_once_with()


def test_RPSearchQuery_save_as_query_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    inner = make_fake_element("X", getName="y")
    fake.saveAsQuery.return_value = inner
    obj = RPSearchQuery(fake)
    result = obj.save_as_query(AbstractRPModelElement.wrap(target))
    fake.saveAsQuery.assert_called_once_with(target)
    assert isinstance(result, RPTableLayout)


def test_RPSearchQuery_set_filter_tag_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_filter_tag("file.txt")
    fake.setFilterTag.assert_called_once_with("file.txt")


def test_RPSearchQuery_get_filter_sub_queries_operator_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterSubQueriesOperator.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_sub_queries_operator() == "value"


def test_RPSearchQuery_get_filter_tag_local_only_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterTagLocalOnly.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_filter_tag_local_only() == 1


def test_RPSearchQuery_get_filter_units_only_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterUnitsOnly.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_filter_units_only() == 1


def test_RPSearchQuery_get_filter_unresolved_kind_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getFilterUnresolvedKind.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_filter_unresolved_kind() == "value"


def test_RPSearchQuery_get_include_descendants_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getIncludeDescendants.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_include_descendants() == 1


def test_RPSearchQuery_get_match_case_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getMatchCase.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_match_case() == 1


def test_RPSearchQuery_get_match_specified_criteria_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getMatchSpecifiedCriteria.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_match_specified_criteria() == 1


def test_RPSearchQuery_get_match_whole_word_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getMatchWholeWord.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_match_whole_word() == 1


def test_RPSearchQuery_get_search_find_as_option_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getSearchFindAsOption.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_search_find_as_option() == "value"


def test_RPSearchQuery_get_search_scope_object_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    inner = make_fake_element("X", getName="y")
    fake.getSearchScopeObject.return_value = inner
    obj = RPSearchQuery(fake)
    result = obj.get_search_scope_object()
    assert result.getName() == "y"


def test_RPSearchQuery_get_search_text_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getSearchText.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_search_text() == "value"


def test_RPSearchQuery_get_view_include_model_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getViewIncludeModelElements.return_value = 1
    obj = RPSearchQuery(fake)
    assert obj.get_view_include_model_elements() == 1


def test_RPSearchQuery_get_views_to_search_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    fake.getViewsToSearch.return_value = "value"
    obj = RPSearchQuery(fake)
    assert obj.get_views_to_search() == "value"


def test_RPSearchQuery_set_filter_sub_queries_operator_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_filter_sub_queries_operator("file.txt")
    fake.setFilterSubQueriesOperator.assert_called_once_with("file.txt")


def test_RPSearchQuery_set_filter_tag_local_only_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_filter_tag_local_only(1)
    fake.setFilterTagLocalOnly.assert_called_once_with(1)


def test_RPSearchQuery_set_filter_units_only_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_filter_units_only(1)
    fake.setFilterUnitsOnly.assert_called_once_with(1)


def test_RPSearchQuery_set_filter_unresolved_kind_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_filter_unresolved_kind("file.txt")
    fake.setFilterUnresolvedKind.assert_called_once_with("file.txt")


def test_RPSearchQuery_set_include_descendants_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_include_descendants(1)
    fake.setIncludeDescendants.assert_called_once_with(1)


def test_RPSearchQuery_set_match_case_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_match_case(1)
    fake.setMatchCase.assert_called_once_with(1)


def test_RPSearchQuery_set_match_specified_criteria_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_match_specified_criteria(1)
    fake.setMatchSpecifiedCriteria.assert_called_once_with(1)


def test_RPSearchQuery_set_match_whole_word_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_match_whole_word(1)
    fake.setMatchWholeWord.assert_called_once_with(1)


def test_RPSearchQuery_set_search_find_as_option_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_search_find_as_option("file.txt")
    fake.setSearchFindAsOption.assert_called_once_with("file.txt")


def test_RPSearchQuery_set_search_scope_object_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    target = make_fake_element("X")
    obj = RPSearchQuery(fake)
    obj.set_search_scope_object(AbstractRPModelElement.wrap(target))
    fake.setSearchScopeObject.assert_called_once_with(target)


def test_RPSearchQuery_set_search_text_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_search_text("file.txt")
    fake.setSearchText.assert_called_once_with("file.txt")


def test_RPSearchQuery_set_view_include_model_elements_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_view_include_model_elements(1)
    fake.setViewIncludeModelElements.assert_called_once_with(1)


def test_RPSearchQuery_set_views_to_search_delegates_to_com():
    fake = make_fake_element("SearchQuery")
    obj = RPSearchQuery(fake)
    obj.set_views_to_search("file.txt")
    fake.setViewsToSearch.assert_called_once_with("file.txt")


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPSearchQuery -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPSearchQuery`)

```python

    def add_diagram_to_views_list(self, view: RPDiagram) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.addDiagramToViewsList(view._com)))

    def add_filter_element_type(self, element_type: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addFilterElementType(element_type))

    def add_filter_search_in_field(self, search_in_field: str) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addFilterSearchInField(search_in_field))

    def add_filter_stereotype(self, stereotype: RPStereotype) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addFilterStereotype(stereotype._com))

    def add_filter_sub_query(self, sub_query: RPTableLayout, use_with_not_operator: int) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addFilterSubQuery(sub_query._com, use_with_not_operator))

    def add_matrix_to_views_list(self, view: RPMatrixView) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.addMatrixToViewsList(view._com)))

    def add_search_scope(self, scope_element: RPModelElement) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.addSearchScope(scope_element._com))

    def add_table_to_views_list(self, view: RPTableView) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.addTableToViewsList(view._com)))

    def get_filter_element_types(self) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getFilterElementTypes", "filterElementTypes"))

    def get_filter_reference_include_referenced_elements_in_search_results(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getFilterReferenceIncludeReferencedElementsInSearchResults", "filterReferenceIncludeReferencedElementsInSearchResults"))

    def get_filter_reference_name_of_referenced_elements(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterReferenceNameOfReferencedElements", "filterReferenceNameOfReferencedElements"))

    def get_filter_reference_number_of_references(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getFilterReferenceNumberOfReferences", "filterReferenceNumberOfReferences"))

    def get_filter_reference_quantity_operator(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterReferenceQuantityOperator", "filterReferenceQuantityOperator"))

    def get_filter_reference_relation_kind(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterReferenceRelationKind", "filterReferenceRelationKind"))

    def get_filter_reference_stereotype_of_referenced_elements(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterReferenceStereotypeOfReferencedElements", "filterReferenceStereotypeOfReferencedElements"))

    def get_filter_reference_type_of_referenced_elements(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterReferenceTypeOfReferencedElements", "filterReferenceTypeOfReferencedElements"))

    def get_filter_search_in_fields(self) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getFilterSearchInFields", "filterSearchInFields"))

    def get_filter_stereotypes(self) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getFilterStereotypes", "filterStereotypes"))

    def get_filter_sub_queries(self) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getFilterSubQueries", "filterSubQueries"))

    def get_filter_sub_query_use_with_not_operator(self, sub_query: RPTableLayout) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getFilterSubQueryUseWithNotOperator", "filterSubQueryUseWithNotOperator"))

    def get_filter_tag_find_as(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterTagFindAs", "filterTagFindAs"))

    def get_filter_tag_match_case(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getFilterTagMatchCase", "filterTagMatchCase"))

    def get_filter_tag_match_whole_word(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getFilterTagMatchWholeWord", "filterTagMatchWholeWord"))

    def get_filter_tag_name(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterTagName", "filterTagName"))

    def get_filter_tag_value(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterTagValue", "filterTagValue"))

    def get_search_scope_elements(self) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getSearchScopeElements", "searchScopeElements"))

    def get_view(self, index: int) -> RPModelElement:

        # (keep existing docstring)

        return AbstractRPModelElement.wrap(self._get_method_or_property(self._com, "getView", "view"))

    def get_view_count(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getViewCount", "viewCount"))

    def load_from_query(self, query: RPTableLayout) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.loadFromQuery(query._com))

    def remove_filter_element_types(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.removeFilterElementTypes())

    def remove_filter_references(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.removeFilterReferences())

    def remove_filter_search_in_fields(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.removeFilterSearchInFields())

    def remove_filter_stereotypes(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.removeFilterStereotypes())

    def remove_filter_sub_queries(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.removeFilterSubQueries())

    def remove_filter_sub_query(self, sub_query: RPTableLayout) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.removeFilterSubQuery(sub_query._com)))

    def remove_filter_tag(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.removeFilterTag())

    def remove_search_scope_element(self, scope_element: RPModelElement) -> int:

        # (keep existing docstring)

        return int(self.call_com(lambda: self._com.removeSearchScopeElement(scope_element._com)))

    def remove_view(self, index: int) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.removeView(index))

    def reset_search_scope(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.resetSearchScope())

    def save_as_query(self, query_owner: RPPackage) -> RPTableLayout:

        # (keep existing docstring)

        return RPTableLayout(self.call_com(lambda: self._com.saveAsQuery(query_owner._com)))

    def set_filter_tag(self, tag_name: str, tag_value: str, match_case: int, match_whole_word: int, find_as: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setFilterTag", "filterTag", tag_name)

    def get_filter_sub_queries_operator(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterSubQueriesOperator", "filterSubQueriesOperator"))

    def get_filter_tag_local_only(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getFilterTagLocalOnly", "filterTagLocalOnly"))

    def get_filter_units_only(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getFilterUnitsOnly", "filterUnitsOnly"))

    def get_filter_unresolved_kind(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getFilterUnresolvedKind", "filterUnresolvedKind"))

    def get_include_descendants(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getIncludeDescendants", "includeDescendants"))

    def get_match_case(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getMatchCase", "matchCase"))

    def get_match_specified_criteria(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getMatchSpecifiedCriteria", "matchSpecifiedCriteria"))

    def get_match_whole_word(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getMatchWholeWord", "matchWholeWord"))

    def get_search_find_as_option(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getSearchFindAsOption", "searchFindAsOption"))

    def get_search_scope_object(self) -> RPModelElement:

        # (keep existing docstring)

        return AbstractRPModelElement.wrap(self._get_method_or_property(self._com, "getSearchScopeObject", "searchScopeObject"))

    def get_search_text(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getSearchText", "searchText"))

    def get_view_include_model_elements(self) -> int:

        # (keep existing docstring)

        return int(self._get_method_or_property(self._com, "getViewIncludeModelElements", "viewIncludeModelElements"))

    def get_views_to_search(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getViewsToSearch", "viewsToSearch"))

    def set_filter_sub_queries_operator(self, filter_sub_queries_operator: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setFilterSubQueriesOperator", "filterSubQueriesOperator", filter_sub_queries_operator)

    def set_filter_tag_local_only(self, filter_tag_local_only: int) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setFilterTagLocalOnly", "filterTagLocalOnly", filter_tag_local_only)

    def set_filter_units_only(self, filter_units_only: int) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setFilterUnitsOnly", "filterUnitsOnly", filter_units_only)

    def set_filter_unresolved_kind(self, filter_unresolved_kind: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setFilterUnresolvedKind", "filterUnresolvedKind", filter_unresolved_kind)

    def set_include_descendants(self, include_descendants: int) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setIncludeDescendants", "includeDescendants", include_descendants)

    def set_match_case(self, match_case: int) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setMatchCase", "matchCase", match_case)

    def set_match_specified_criteria(self, match_specified_criteria: int) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setMatchSpecifiedCriteria", "matchSpecifiedCriteria", match_specified_criteria)

    def set_match_whole_word(self, match_whole_word: int) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setMatchWholeWord", "matchWholeWord", match_whole_word)

    def set_search_find_as_option(self, search_find_as_option: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setSearchFindAsOption", "searchFindAsOption", search_find_as_option)

    def set_search_scope_object(self, search_scope_object: RPModelElement) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setSearchScopeObject", "searchScopeObject", search_scope_object)

    def set_search_text(self, search_text: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setSearchText", "searchText", search_text)

    def set_view_include_model_elements(self, view_include_model_elements: int) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setViewIncludeModelElements", "viewIncludeModelElements", view_include_model_elements)

    def set_views_to_search(self, views_to_search: str) -> None:

        # (keep existing docstring)

        self._set_method_or_property(self._com, "setViewsToSearch", "viewsToSearch", views_to_search)

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPSearchQuery -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPSearchQuery`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPSearchQuery methods with tests"
```


## Task 25: Implement `RPSearchResult` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPSearchResult`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPSearchResult` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `get_matched_field` | `getMatchedField` | GETTER | (raw) | - |

| `get_matched_fields` | `getMatchedFields` | GETTER | RPCollection | - |

| `get_matched_object` | `getMatchedObject` | GETTER | AbstractRPModelElement.wrap | - |

| `get_name` | `getName` | GETTER | (raw) | - |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPSearchResult_get_matched_field_delegates_to_com():
    fake = make_fake_element("SearchResult")
    fake.getMatchedField.return_value = "value"
    obj = RPSearchResult(fake)
    assert obj.get_matched_field() == "value"


def test_RPSearchResult_get_matched_fields_delegates_to_com():
    fake = make_fake_element("SearchResult")
    inner = make_fake_element("X", getName="y")
    fake.getMatchedFields.return_value = make_fake_collection([inner])
    obj = RPSearchResult(fake)
    result = obj.get_matched_fields()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_RPSearchResult_get_matched_object_delegates_to_com():
    fake = make_fake_element("SearchResult")
    inner = make_fake_element("X", getName="y")
    fake.getMatchedObject.return_value = inner
    obj = RPSearchResult(fake)
    result = obj.get_matched_object()
    assert result.getName() == "y"


def test_RPSearchResult_get_name_delegates_to_com():
    fake = make_fake_element("SearchResult")
    fake.getName.return_value = "value"
    obj = RPSearchResult(fake)
    assert obj.get_name() == "value"


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPSearchResult -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPSearchResult`)

```python

    def get_matched_field(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getMatchedField", "matchedField"))

    def get_matched_fields(self) -> RPCollection:

        # (keep existing docstring)

        return RPCollection(self._get_method_or_property(self._com, "getMatchedFields", "matchedFields"))

    def get_matched_object(self) -> RPModelElement:

        # (keep existing docstring)

        return AbstractRPModelElement.wrap(self._get_method_or_property(self._com, "getMatchedObject", "matchedObject"))

    def get_name(self) -> str:

        # (keep existing docstring)

        return str(self._get_method_or_property(self._com, "getName", "name"))

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPSearchResult -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPSearchResult`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPSearchResult methods with tests"
```


## Task 26: Implement `RPCodeGenSimplifiersRegistry` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPCodeGenSimplifiersRegistry`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPCodeGenSimplifiersRegistry` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `notify_simplification_done` | `notifySimplificationDone` | ACTION | - | - |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPCodeGenSimplifiersRegistry_notify_simplification_done_delegates_to_com():
    fake = make_fake_element("CodeGenSimplifiersRegistry")
    obj = RPCodeGenSimplifiersRegistry(fake)
    obj.notify_simplification_done()
    fake.notifySimplificationDone.assert_called_once_with()


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPCodeGenSimplifiersRegistry -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPCodeGenSimplifiersRegistry`)

```python

    def notify_simplification_done(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.notifySimplificationDone())

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPCodeGenSimplifiersRegistry -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPCodeGenSimplifiersRegistry`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPCodeGenSimplifiersRegistry methods with tests"
```


## Task 27: Implement `RPExternalCodeGeneratorInvoker` (codegen)


**Files:**

- Modify: `src/rhapsody_cli/models/support/model_codegen.py` (class `RPExternalCodeGeneratorInvoker`)

- Test: `tests/unit/models/support/test_codegen.py`


**Interfaces:**

- Consumes: `AbstractRPModelElement.call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap` (core).

- Produces: fully-implemented `RPExternalCodeGeneratorInvoker` methods (no new public API).


**Method inventory (COM mapping):**

| Python method | COM method | Category | Return wrap | Arg unwrap |

|---|---|---|---|---|

| `notify_generation_done` | `notifyGenerationDone` | ACTION | - | - |

| `get_interface_name` | `getInterfaceName` | INHERIT (delete) | - | - |


- [ ] **Step 1: Write the failing tests** (append to `tests/unit/models/support/test_codegen.py`)


```python

def test_RPExternalCodeGeneratorInvoker_notify_generation_done_delegates_to_com():
    fake = make_fake_element("ExternalCodeGeneratorInvoker")
    obj = RPExternalCodeGeneratorInvoker(fake)
    obj.notify_generation_done()
    fake.notifyGenerationDone.assert_called_once_with()


```


- [ ] **Step 2: Run the tests to confirm they fail**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPExternalCodeGeneratorInvoker -v
```
Expected: FAIL (`NotImplementedError`).


- [ ] **Step 3: Implement the method bodies** (replace each `raise NotImplementedError` in class `RPExternalCodeGeneratorInvoker`)

```python

    def notify_generation_done(self) -> None:

        # (keep existing docstring)

        self.call_com(lambda: self._com.notifyGenerationDone())

```



- [ ] **Step 4: Run the tests to confirm they pass**

```bash

pytest tests/unit/models/support/test_codegen.py -k RPExternalCodeGeneratorInvoker -v
```
Expected: PASS.


- [ ] **Step 5: Update the parity checklist** in `src/rhapsody_cli/models/support/model_codegen.py` for class `RPExternalCodeGeneratorInvoker`: flip every method line's `[ ] impl / [ ] docstring / [ ] test` to `[x]`; for `get_interface_name` delete the method and mark `[x] impl (inherited from RPModelElement) [x] docstring [x] test`.


- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py tests/unit/models/support/test_codegen.py
git commit -m "feat(support): implement RPExternalCodeGeneratorInvoker methods with tests"
```


## Task 28: Full Quality Gate


**Files:** None new — verification only.


- [ ] **Step 1: ruff** `ruff check src/ tests/` → no errors.

- [ ] **Step 2: black** `black --check src/ tests/` → no diffs (run `black src/ tests/` if needed, re-commit).

- [ ] **Step 3: mypy** `mypy src/ tests/` → no type errors.

- [ ] **Step 4: tests + coverage** `pytest tests/unit -v --cov=rhapsody_cli` → all pass, coverage ≥ 80%.

- [ ] **Step 5: checklist audit** `grep -rn "\[ \] impl" src/rhapsody_cli/models/support/` → no remaining `[ ] impl` boxes.

- [ ] **Step 6: Commit fixes** `git add -A && git commit -m "style: lint/format fixes after support model completion" || echo nothing`


## Plan Self-Review

1. **Spec coverage:** Every `raise NotImplementedError` in the three support modules maps to exactly one method row in a Task inventory table; the full method count is 190 across 27 classes (`RPASCIIFile`, `RPControlledFile`, `RPFile`, `RPFileFragment`, `RPAXViewCtrl`, `RPExternalIDERegistry`, `RPInternalOEMPlugin`, `RPJavaPlugins`, `RPPlugInWindow`, `RPProgressBar`, `RPSelection`, `RPowListListener`, `RPowPaneMgr`, `RPowTextListener`, `RPBaseExternalCodeGeneratorTool`, `RPCodeGenerator`, `RPDiagSynthAPI`, `RPExternalCheckRegistry`, `RPExternalRoundtripInvoker`, `RPIntegrator`, `RPRhapsodyServer`, `RPRoundTrip`, `RPSearchManager`, `RPSearchQuery`, `RPSearchResult`, `RPCodeGenSimplifiersRegistry`, `RPExternalCodeGeneratorInvoker`).

2. **Placeholder scan:** Every step shows concrete code (method body or test function) generated from the stub's `Reference:` line; no `TBD`/`similar to` placeholders. The only derived-with-verification COM names are the ~8 methods lacking a `Reference:` line (`execute_command`, `add_instance`, `add_synth_s_d_to_model2`, `create_s_d2`, `remove_synth_s_d_to_model2`, `add_diagram_to_views_list`, `add_matrix_to_views_list`, `add_table_to_views_list`, `get_filter_sub_query_use_with_not_operator`, `remove_filter_sub_query`) — these use snake→camel fallback and the implementer should confirm against the live Rhapsody API.

3. **Type consistency:** Return-wrapping and argument-unwrapping rules are applied uniformly from each method's declared annotation; wrapper types (`RPTableLayout`, `RPMatrixView`, `RPTableView`, `RPDiagram`, `RPSequenceDiagram`, `RPStereotype`, `RPClassifier`, `RPPackage`, `RPSearchQuery`, `RPowListListener`, `RPowTextListener`, `RhapsodyApplication`) are imported where used (module-level import notes + test headers).

4. **Green-state rule:** Each Task is independently testable (red test → green impl → checklist flip → commit). `get_interface_name` is handled once as an inherited duplicate (deleted + checklist marked inherited), not re-implemented.

5. **Registry safety:** No `register_wrapper` calls are added or removed; the support `__init__.py` and `elements/__init__.py` are untouched, so the wrapper registry stays exactly as-is.
