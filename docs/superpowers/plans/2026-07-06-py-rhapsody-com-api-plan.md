# py_rhapsody COM API Wrapper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `py_rhapsody`, a Python package that wraps the IBM Rhapsody COM API (`com.telelogic.rhapsody.core` interfaces, same as the Rhapsody Java API) with method names and signatures mirroring the Java API exactly, supporting both read and write operations.

**Architecture:** A generic `wrap()` factory in `py_rhapsody/_core.py` dispatches any Rhapsody COM object to the correct typed wrapper class based on the object's `getMetaClass()` value, using a registry dict populated by each element module at import time. `RPModelElement`/`RPUnit` base classes and `RPCollection` provide shared behavior; `RhapsodyApplication` is the standalone entry point for connecting to Rhapsody. All COM errors are translated to `RhapsodyRuntimeException`.

**Tech Stack:** Python 3.9+, `pywin32` (`win32com.client`, `pywintypes`) for COM, `pytest` for testing (mocked COM objects, no real Rhapsody required), `ruff` + `black` + `mypy` for lint/format/type-check gates on every task.

**Spec:** `docs/superpowers/specs/2026-07-06-py-rhapsody-com-api-design.md`

---

## Verification Gate (every task)

Every task's final steps before commit are the same three commands. They are written out in full in each task so no step is a placeholder:

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```

All three must exit 0 before the commit step. If `black --check` fails, run `black py_rhapsody tests` to auto-format, then re-run `black --check`. If `ruff check` reports fixable issues, run `ruff check --fix py_rhapsody tests` then re-check.

---

### Task 0: Project scaffolding and tooling configuration

**Files:**
- Create: `pyproject.toml`
- Create: `py_rhapsody/__init__.py`
- Create: `py_rhapsody/py.typed`
- Create: `tests/__init__.py`
- Create: `tests/fakes.py`

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "py-rhapsody"
version = "0.1.0"
description = "Pythonic wrapper around the IBM Rhapsody COM API, mirroring the Rhapsody Java API"
readme = "README.md"
requires-python = ">=3.9"
license = { text = "MIT" }
dependencies = [
    "pywin32>=306",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "ruff>=0.4",
    "black>=24.1",
    "mypy>=1.8",
]

[tool.setuptools.packages.find]
include = ["py_rhapsody*"]

[tool.setuptools.package-data]
py_rhapsody = ["py.typed"]

[tool.black]
line-length = 100
target-version = ["py39"]

[tool.ruff]
line-length = 100
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.9"
strict = true
warn_unused_ignores = true

[[tool.mypy.overrides]]
module = "win32com.*"
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "pywintypes"
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Create the package init**

```python
"""py_rhapsody: Pythonic wrapper around the IBM Rhapsody COM API."""

from __future__ import annotations

__all__: list[str] = []
```

Path: `py_rhapsody/__init__.py`

- [ ] **Step 3: Add the `py.typed` marker**

Create an empty file at `py_rhapsody/py.typed` (marks the package as typed for mypy/PEP 561 consumers). Content: empty file (zero bytes).

- [ ] **Step 4: Create `tests/__init__.py`**

Empty file, content: empty (zero bytes). This makes `tests` a package so `tests.fakes` can be imported from test modules.

- [ ] **Step 5: Create the fake-COM-object test helper**

```python
"""Helpers for building fake Rhapsody COM objects for unit tests.

These fakes stand in for real win32com dispatch objects so tests can run
without a licensed Rhapsody installation.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pywintypes


def make_fake_element(meta_class: str, **method_returns: Any) -> MagicMock:
    """Build a fake COM object representing an IRPModelElement subtype.

    ``meta_class`` is the string returned by ``getMetaClass()`` (e.g.
    ``"Class"``, ``"Package"``, ``"Attribute"``), used by ``wrap()`` to pick
    the correct wrapper class.

    ``method_returns`` maps method names to the value that mock method
    should return when called, e.g. ``getName="Foo"`` configures
    ``fake.getName()`` to return ``"Foo"``.
    """
    fake = MagicMock(name=f"FakeCom[{meta_class}]")
    fake.getMetaClass.return_value = meta_class
    for method_name, return_value in method_returns.items():
        getattr(fake, method_name).return_value = return_value
    return fake


def make_fake_collection(items: list[Any]) -> MagicMock:
    """Build a fake COM object representing an IRPCollection."""
    fake = MagicMock(name="FakeCollection")
    fake.getCount.return_value = len(items)
    fake.getItem.side_effect = lambda index: items[index]
    return fake


def make_com_error(message: str = "Rhapsody COM failure") -> pywintypes.com_error:
    """Build a ``pywintypes.com_error`` matching what a failed COM call raises."""
    return pywintypes.com_error(-2147352567, message, None, None)
```

Path: `tests/fakes.py`

- [ ] **Step 6: Install dev dependencies**

Run: `pip install -e .[dev]`
Expected: pywin32, pytest, ruff, black, mypy install successfully with no errors.

- [ ] **Step 7: Verify tooling runs clean on the scaffolding**

Run: `ruff check py_rhapsody tests`
Expected: `All checks passed!`

Run: `black --check py_rhapsody tests`
Expected: `All done!` (no files would be reformatted)

Run: `mypy py_rhapsody`
Expected: `Success: no issues found in 1 source file`

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml py_rhapsody/__init__.py py_rhapsody/py.typed tests/__init__.py tests/fakes.py
git commit -m "chore: scaffold py_rhapsody package with ruff/black/mypy tooling

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 1: Exceptions module

**Files:**
- Create: `py_rhapsody/exceptions.py`
- Test: `tests/test_exceptions.py`

- [ ] **Step 1: Write the failing test**

```python
"""Tests for py_rhapsody.exceptions."""

from __future__ import annotations

import pytest

from py_rhapsody.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException


def test_rhapsody_runtime_exception_preserves_message() -> None:
    exc = RhapsodyRuntimeException("boom")

    assert str(exc) == "boom"
    assert isinstance(exc, Exception)


def test_rhapsody_connection_error_preserves_message() -> None:
    exc = RhapsodyConnectionError("no running instance found")

    assert str(exc) == "no running instance found"
    assert isinstance(exc, Exception)


def test_rhapsody_runtime_exception_is_not_a_connection_error() -> None:
    # These are two distinct failure modes and must not be conflated by callers.
    assert not issubclass(RhapsodyRuntimeException, RhapsodyConnectionError)
    assert not issubclass(RhapsodyConnectionError, RhapsodyRuntimeException)
```

Path: `tests/test_exceptions.py`

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_exceptions.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.exceptions'`

- [ ] **Step 3: Write minimal implementation**

```python
"""Exception types raised by py_rhapsody.

These mirror the failure modes of the Rhapsody Java API: a
``RhapsodyRuntimeException`` is raised by the Java API when a COM/JNI call
into Rhapsody fails; ``RhapsodyConnectionError`` is specific to py_rhapsody
and covers failures to attach to or launch a Rhapsody instance.
"""

from __future__ import annotations


class RhapsodyRuntimeException(Exception):
    """Raised when a call into the Rhapsody COM API fails.

    Mirrors ``com.telelogic.rhapsody.core.RhapsodyRuntimeException`` from the
    Java API. The original COM error message/HRESULT text is preserved as
    the exception message.
    """


class RhapsodyConnectionError(Exception):
    """Raised when py_rhapsody cannot attach to or launch a Rhapsody instance."""
```

Path: `py_rhapsody/exceptions.py`

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_exceptions.py -v`
Expected: 3 passed

- [ ] **Step 5: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 6: Commit**

```bash
git add py_rhapsody/exceptions.py tests/test_exceptions.py
git commit -m "feat: add RhapsodyRuntimeException and RhapsodyConnectionError

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 2: COM-error translation helper and `RPModelElement` base class

**Files:**
- Create: `py_rhapsody/_core.py`
- Test: `tests/test_core.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody._core: call_com, RPModelElement, wrap()."""

from __future__ import annotations

import pytest

from py_rhapsody._core import RPModelElement, call_com
from py_rhapsody.exceptions import RhapsodyRuntimeException
from tests.fakes import make_com_error, make_fake_element


def test_call_com_returns_value_on_success() -> None:
    result = call_com(lambda: 42)

    assert result == 42


def test_call_com_translates_com_error() -> None:
    def failing() -> int:
        raise make_com_error("getName failed")

    with pytest.raises(RhapsodyRuntimeException, match="getName failed"):
        call_com(failing)


def test_call_com_does_not_translate_other_exceptions() -> None:
    def failing() -> int:
        raise ValueError("not a COM error")

    with pytest.raises(ValueError, match="not a COM error"):
        call_com(failing)


def test_model_element_get_name_delegates_to_com() -> None:
    fake = make_fake_element("Class", getName="Widget")
    element = RPModelElement(fake)

    assert element.getName() == "Widget"
    fake.getName.assert_called_once_with()


def test_model_element_set_name_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.setName("NewName")

    fake.setName.assert_called_once_with("NewName")


def test_model_element_get_meta_class_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    element = RPModelElement(fake)

    assert element.getMetaClass() == "Package"


def test_model_element_get_guid_delegates_to_com() -> None:
    fake = make_fake_element("Class", getGUID="guid-123")
    element = RPModelElement(fake)

    assert element.getGUID() == "guid-123"


def test_model_element_com_error_becomes_rhapsody_runtime_exception() -> None:
    fake = make_fake_element("Class")
    fake.getName.side_effect = make_com_error("boom")
    element = RPModelElement(fake)

    with pytest.raises(RhapsodyRuntimeException, match="boom"):
        element.getName()


def test_model_element_equality_by_underlying_com_object() -> None:
    fake = make_fake_element("Class")

    assert RPModelElement(fake) == RPModelElement(fake)
    assert RPModelElement(fake) != RPModelElement(make_fake_element("Class"))
```

Path: `tests/test_core.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody._core'`

- [ ] **Step 3: Write minimal implementation**

```python
"""Core wrapping machinery shared by all py_rhapsody element wrappers.

``call_com`` translates COM failures into ``RhapsodyRuntimeException``.
``RPModelElement`` is the base class for every wrapped Rhapsody model
element, mirroring ``com.telelogic.rhapsody.core.IRPModelElement``.
``wrap()`` (added in Task 5) dispatches a raw COM object to its matching
wrapper class using a registry populated by each element module.
"""

from __future__ import annotations

from typing import Any, Callable, TypeVar

import pywintypes

from py_rhapsody.exceptions import RhapsodyRuntimeException

T = TypeVar("T")

#: Maps a Rhapsody ``getMetaClass()`` string (e.g. "Class", "Package") to the
#: wrapper class that should represent it. Populated by each element module
#: at import time via ``register_wrapper``. Unmapped meta classes fall back
#: to ``RPModelElement`` in ``wrap()`` (Task 5).
_WRAPPER_REGISTRY: dict[str, type["RPModelElement"]] = {}


def register_wrapper(meta_class: str, wrapper_cls: type["RPModelElement"]) -> None:
    """Register ``wrapper_cls`` as the wrapper for COM objects of ``meta_class``."""
    _WRAPPER_REGISTRY[meta_class] = wrapper_cls


def call_com(func: Callable[[], T]) -> T:
    """Invoke a COM call, translating COM errors into RhapsodyRuntimeException."""
    try:
        return func()
    except pywintypes.com_error as exc:
        raise RhapsodyRuntimeException(str(exc)) from exc


class RPModelElement:
    """Wraps ``IRPModelElement``: the base interface for all model elements.

    Method names mirror the Rhapsody Java API exactly (``getName``,
    ``setName``, ``getMetaClass``, ``getGUID``, ...).
    """

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    def getName(self) -> str:
        return call_com(lambda: str(self._com.getName()))

    def setName(self, name: str) -> None:
        call_com(lambda: self._com.setName(name))

    def getMetaClass(self) -> str:
        return call_com(lambda: str(self._com.getMetaClass()))

    def getGUID(self) -> str:
        return call_com(lambda: str(self._com.getGUID()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RPModelElement):
            return NotImplemented
        return bool(self._com == other._com)

    def __hash__(self) -> int:
        return hash(id(self._com))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.getName()!r})"
```

Path: `py_rhapsody/_core.py`

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core.py -v`
Expected: 9 passed

- [ ] **Step 5: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 6: Commit**

```bash
git add py_rhapsody/_core.py tests/test_core.py
git commit -m "feat: add call_com error translation and RPModelElement base class

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 3: `RPUnit` base class

**Files:**
- Modify: `py_rhapsody/_core.py`
- Test: `tests/test_core.py`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_core.py`:

```python
from py_rhapsody._core import RPUnit


def test_unit_save_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.save()

    fake.save.assert_called_once_with()


def test_unit_get_filename_delegates_to_com() -> None:
    fake = make_fake_element("Package", getFilename="Model/Foo.sbs")
    unit = RPUnit(fake)

    assert unit.getFilename() == "Model/Foo.sbs"


def test_unit_set_filename_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.setFilename("Model/Bar.sbs")

    fake.setFilename.assert_called_once_with("Model/Bar.sbs")


def test_unit_is_read_only_delegates_to_com() -> None:
    fake = make_fake_element("Package", isReadOnly=1)
    unit = RPUnit(fake)

    assert unit.isReadOnly() is True


def test_unit_set_read_only_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    unit = RPUnit(fake)

    unit.setReadOnly(True)

    fake.setReadOnly.assert_called_once_with(1)


def test_unit_is_a_model_element() -> None:
    fake = make_fake_element("Package", getName="MyPkg")
    unit = RPUnit(fake)

    assert isinstance(unit, RPModelElement)
    assert unit.getName() == "MyPkg"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core.py -v -k RPUnit or test_unit`
Expected: FAIL with `ImportError: cannot import name 'RPUnit' from 'py_rhapsody._core'`

- [ ] **Step 3: Write minimal implementation**

Append to `py_rhapsody/_core.py`:

```python
class RPUnit(RPModelElement):
    """Wraps ``IRPUnit``: model elements that can be saved as separate files."""

    def save(self) -> None:
        call_com(lambda: self._com.save())

    def getFilename(self) -> str:
        return call_com(lambda: str(self._com.getFilename()))

    def setFilename(self, filename: str) -> None:
        call_com(lambda: self._com.setFilename(filename))

    def isReadOnly(self) -> bool:
        return call_com(lambda: bool(self._com.isReadOnly()))

    def setReadOnly(self, read_only: bool) -> None:
        call_com(lambda: self._com.setReadOnly(1 if read_only else 0))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core.py -v`
Expected: 15 passed

- [ ] **Step 5: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 6: Commit**

```bash
git add py_rhapsody/_core.py tests/test_core.py
git commit -m "feat: add RPUnit base class

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 4: `RPCollection`

**Files:**
- Modify: `py_rhapsody/_core.py`
- Test: `tests/test_core.py`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_core.py`:

```python
from py_rhapsody._core import RPCollection
from tests.fakes import make_fake_collection


def test_collection_len_delegates_to_get_count() -> None:
    fake = make_fake_collection([make_fake_element("Class")])
    collection = RPCollection(fake)

    assert len(collection) == 1


def test_collection_getitem_wraps_model_elements() -> None:
    inner = make_fake_element("Class", getName="Widget")
    fake = make_fake_collection([inner])
    collection = RPCollection(fake)

    item = collection[0]

    assert isinstance(item, RPModelElement)
    assert item.getName() == "Widget"


def test_collection_getitem_passes_through_non_element_values() -> None:
    fake = make_fake_collection(["a plain string", 42])
    collection = RPCollection(fake)

    assert collection[0] == "a plain string"
    assert collection[1] == 42


def test_collection_iter_yields_all_items() -> None:
    inner_a = make_fake_element("Class", getName="A")
    inner_b = make_fake_element("Class", getName="B")
    fake = make_fake_collection([inner_a, inner_b])
    collection = RPCollection(fake)

    names = [item.getName() for item in collection]

    assert names == ["A", "B"]


def test_collection_add_item_delegates_to_com() -> None:
    fake = make_fake_collection([])
    collection = RPCollection(fake)
    new_element = make_fake_element("Class")

    collection.addItem(RPModelElement(new_element))

    fake.addItem.assert_called_once_with(new_element)


def test_collection_get_count_delegates_to_com() -> None:
    fake = make_fake_collection([make_fake_element("Class"), make_fake_element("Class")])
    collection = RPCollection(fake)

    assert collection.getCount() == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core.py -v -k collection`
Expected: FAIL with `ImportError: cannot import name 'RPCollection' from 'py_rhapsody._core'`

- [ ] **Step 3: Write minimal implementation**

Add near the top of `py_rhapsody/_core.py` (after the existing imports) an `Iterator` import, then append the class:

Update the imports line:

```python
from typing import Any, Callable, Iterator, TypeVar
```

Append:

```python
def _wrap_if_element(value: Any) -> Any:
    """Wrap ``value`` with the registered wrapper if it looks like a model element.

    A raw COM item from an ``IRPCollection`` may be a model element (which
    exposes ``getMetaClass``) or a plain value (``str``/``int``) placed there
    via ``setInteger``/``setModelElement``. Only the former is wrapped.
    """
    if hasattr(value, "getMetaClass"):
        return wrap(value)
    return value


def wrap(com_obj: Any) -> "RPModelElement":
    """Wrap a raw Rhapsody COM model element in its matching wrapper class.

    Dispatches on ``com_obj.getMetaClass()``. Meta classes with no
    registered wrapper fall back to the generic ``RPModelElement``, so
    navigation never fails just because a specific element type hasn't been
    given a dedicated wrapper class yet.
    """
    meta_class = call_com(lambda: str(com_obj.getMetaClass()))
    wrapper_cls = _WRAPPER_REGISTRY.get(meta_class, RPModelElement)
    return wrapper_cls(com_obj)


class RPCollection:
    """Wraps ``IRPCollection``: an iterable/indexable container of elements."""

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    def getCount(self) -> int:
        return call_com(lambda: int(self._com.getCount()))

    def getItem(self, index: int) -> Any:
        return _wrap_if_element(call_com(lambda: self._com.getItem(index)))

    def addItem(self, element: RPModelElement) -> None:
        call_com(lambda: self._com.addItem(element._com))

    def __len__(self) -> int:
        return self.getCount()

    def __getitem__(self, index: int) -> Any:
        return self.getItem(index)

    def __iter__(self) -> Iterator[Any]:
        for i in range(len(self)):
            yield self[i]
```

Note: `wrap()` is defined here (ahead of schedule relative to the spec's Task 5 in the plan header) because `RPCollection.getItem` depends on it. Task 5 below only adds the registration wiring for concrete element types — the `wrap()` function itself and `_WRAPPER_REGISTRY` are implemented in this step.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core.py -v`
Expected: 21 passed

- [ ] **Step 5: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 6: Commit**

```bash
git add py_rhapsody/_core.py tests/test_core.py
git commit -m "feat: add RPCollection and the wrap() dispatch factory

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 5: `wrap()` fallback behavior and registry contract

**Files:**
- Modify: `tests/test_core.py`

This task adds the tests that lock down `wrap()`'s dispatch and fallback
contract (the implementation already exists from Task 4). It exists as a
separate task so the registry/fallback behavior — which every later element
task depends on — has its own explicit, reviewable test coverage.

- [ ] **Step 1: Write the tests**

Append to `tests/test_core.py`:

```python
from py_rhapsody._core import register_wrapper


class _FakeClassWrapper(RPModelElement):
    pass


def test_wrap_dispatches_to_registered_wrapper() -> None:
    register_wrapper("FakeMetaType", _FakeClassWrapper)
    fake = make_fake_element("FakeMetaType", getName="Thing")

    from py_rhapsody._core import wrap

    wrapped = wrap(fake)

    assert isinstance(wrapped, _FakeClassWrapper)
    assert wrapped.getName() == "Thing"


def test_wrap_falls_back_to_model_element_for_unregistered_type() -> None:
    fake = make_fake_element("SomeUnmappedType", getName="Mystery")

    from py_rhapsody._core import wrap

    wrapped = wrap(fake)

    assert type(wrapped) is RPModelElement
    assert wrapped.getName() == "Mystery"
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `pytest tests/test_core.py -v`
Expected: 23 passed (implementation already exists from Task 4, so these pass immediately — this step confirms the contract, not new production code)

- [ ] **Step 3: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 4: Commit**

```bash
git add tests/test_core.py
git commit -m "test: lock down wrap() registry dispatch and fallback contract

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 6: `RPProject` (wraps `IRPProject`)

**Files:**
- Create: `py_rhapsody/elements/__init__.py`
- Create: `py_rhapsody/elements/project.py`
- Test: `tests/elements/__init__.py`
- Test: `tests/elements/test_project.py`

- [ ] **Step 1: Create the `elements` package init (empty for now)**

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations
```

Path: `py_rhapsody/elements/__init__.py`

- [ ] **Step 2: Create the test package init**

Empty file, content: empty (zero bytes).
Path: `tests/elements/__init__.py`

- [ ] **Step 3: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.project.RPProject."""

from __future__ import annotations

from py_rhapsody._core import RPUnit
from py_rhapsody.elements.project import RPProject
from tests.fakes import make_fake_collection, make_fake_element


def test_project_is_a_unit() -> None:
    fake = make_fake_element("Project", getName="MyProject")
    project = RPProject(fake)

    assert isinstance(project, RPUnit)
    assert project.getName() == "MyProject"


def test_project_add_package_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    new_pkg = make_fake_element("Package", getName="NewPkg")
    fake.addPackage.return_value = new_pkg
    project = RPProject(fake)

    result = project.addPackage("NewPkg")

    fake.addPackage.assert_called_once_with("NewPkg")
    assert result.getName() == "NewPkg"


def test_project_close_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.close()

    fake.close.assert_called_once_with()


def test_project_become_active_project_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.becomeActiveProject()

    fake.becomeActiveProject.assert_called_once_with()


def test_project_find_component_wraps_result() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Component", getName="Comp1")
    fake.findComponent.return_value = found
    project = RPProject(fake)

    result = project.findComponent("Comp1")

    fake.findComponent.assert_called_once_with("Comp1")
    assert result.getName() == "Comp1"


def test_project_get_packages_returns_collection() -> None:
    from py_rhapsody._core import RPCollection

    fake = make_fake_element("Project")
    fake.getPackages.return_value = make_fake_collection(
        [make_fake_element("Package", getName="P1")]
    )
    project = RPProject(fake)

    packages = project.getPackages()

    assert isinstance(packages, RPCollection)
    assert len(packages) == 1
    assert packages[0].getName() == "P1"


def test_project_is_registered_for_meta_class_project() -> None:
    from py_rhapsody._core import wrap

    fake = make_fake_element("Project", getName="MyProject")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPProject)
```

Path: `tests/elements/test_project.py`

- [ ] **Step 4: Run tests to verify they fail**

Run: `pytest tests/elements/test_project.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.project'`

- [ ] **Step 5: Write minimal implementation**

```python
"""RPProject: wraps IRPProject, the top-level container for a Rhapsody model."""

from __future__ import annotations

from typing import Any

from py_rhapsody._core import RPCollection, RPUnit, call_com, register_wrapper, wrap


class RPProject(RPUnit):
    """Wraps ``IRPProject``."""

    def addPackage(self, name: str) -> "Any":
        return wrap(call_com(lambda: self._com.addPackage(name)))

    def close(self) -> None:
        call_com(lambda: self._com.close())

    def becomeActiveProject(self) -> None:
        call_com(lambda: self._com.becomeActiveProject())

    def findComponent(self, name: str) -> "Any":
        return wrap(call_com(lambda: self._com.findComponent(name)))

    def getPackages(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getPackages()))


register_wrapper("Project", RPProject)
```

Path: `py_rhapsody/elements/project.py`

Note: `getPackages` is not documented on `IRPProject` directly in every
Rhapsody version's Java doc excerpt reviewed for this plan, but `IRPProject`
exposes a `getPackages()` collection getter for the project's top-level
packages consistently across Rhapsody releases; it is included here as a
core navigation entry point.

- [ ] **Step 6: Register the `elements.project` module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import project as project  # noqa: F401
```

- [ ] **Step 7: Run tests to verify they pass**

Run: `pytest tests/elements/test_project.py -v`
Expected: 7 passed

- [ ] **Step 8: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 9: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/project.py tests/elements/__init__.py tests/elements/test_project.py
git commit -m "feat: add RPProject wrapper for IRPProject

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 7: `RPPackage` (wraps `IRPPackage`)

**Files:**
- Create: `py_rhapsody/elements/package.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_package.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.package.RPPackage."""

from __future__ import annotations

from py_rhapsody._core import RPUnit, wrap
from py_rhapsody.elements.package import RPPackage
from tests.fakes import make_fake_element


def test_package_is_a_unit() -> None:
    fake = make_fake_element("Package", getName="MyPkg")
    package = RPPackage(fake)

    assert isinstance(package, RPUnit)
    assert package.getName() == "MyPkg"


def test_package_add_class_delegates_to_com_and_wraps_result() -> None:
    fake = make_fake_element("Package")
    new_class = make_fake_element("Class", getName="Widget")
    fake.addClass.return_value = new_class
    package = RPPackage(fake)

    result = package.addClass("Widget")

    fake.addClass.assert_called_once_with("Widget")
    assert result.getName() == "Widget"


def test_package_add_nested_package_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    nested = make_fake_element("Package", getName="Nested")
    fake.addNestedPackage.return_value = nested
    package = RPPackage(fake)

    result = package.addNestedPackage("Nested")

    fake.addNestedPackage.assert_called_once_with("Nested")
    assert result.getName() == "Nested"


def test_package_add_actor_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    actor = make_fake_element("Actor", getName="Driver")
    fake.addActor.return_value = actor
    package = RPPackage(fake)

    result = package.addActor("Driver")

    fake.addActor.assert_called_once_with("Driver")
    assert result.getName() == "Driver"


def test_package_add_global_function_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    func = make_fake_element("Operation", getName="doThing")
    fake.addGlobalFunction.return_value = func
    package = RPPackage(fake)

    result = package.addGlobalFunction("doThing")

    fake.addGlobalFunction.assert_called_once_with("doThing")
    assert result.getName() == "doThing"


def test_package_is_registered_for_meta_class_package() -> None:
    fake = make_fake_element("Package", getName="MyPkg")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPPackage)
```

Path: `tests/elements/test_package.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_package.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.package'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPPackage: wraps IRPPackage, a container for classes, actors, and other elements."""

from __future__ import annotations

from typing import Any

from py_rhapsody._core import RPUnit, call_com, register_wrapper, wrap


class RPPackage(RPUnit):
    """Wraps ``IRPPackage``."""

    def addClass(self, name: str) -> "Any":
        return wrap(call_com(lambda: self._com.addClass(name)))

    def addNestedPackage(self, name: str) -> "Any":
        return wrap(call_com(lambda: self._com.addNestedPackage(name)))

    def addActor(self, name: str) -> "Any":
        return wrap(call_com(lambda: self._com.addActor(name)))

    def addGlobalFunction(self, name: str) -> "Any":
        return wrap(call_com(lambda: self._com.addGlobalFunction(name)))


register_wrapper("Package", RPPackage)
```

Path: `py_rhapsody/elements/package.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_package.py -v`
Expected: 6 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/package.py tests/elements/test_package.py
git commit -m "feat: add RPPackage wrapper for IRPPackage

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 8: `RPClassifier` (wraps `IRPClassifier`)

**Files:**
- Create: `py_rhapsody/elements/classifier.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_classifier.py`

Note: `IRPClassifier` has no dedicated `getMetaClass()` value of its own in
Rhapsody (only its concrete subtypes like `Class`/`Actor`/`UseCase` do), so
`RPClassifier` is not registered in `_WRAPPER_REGISTRY` — it exists purely as
a shared base class for `RPClass`, `RPActor`, and `RPUseCase` (Tasks 9, 12, 13).

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.classifier.RPClassifier."""

from __future__ import annotations

from py_rhapsody._core import RPUnit
from py_rhapsody.elements.classifier import RPClassifier
from tests.fakes import make_fake_collection, make_fake_element


def test_classifier_is_a_unit() -> None:
    fake = make_fake_element("Class", getName="Widget")
    classifier = RPClassifier(fake)

    assert isinstance(classifier, RPUnit)
    assert classifier.getName() == "Widget"


def test_classifier_add_attribute_wraps_result() -> None:
    fake = make_fake_element("Class")
    attr = make_fake_element("Attribute", getName="count")
    fake.addAttribute.return_value = attr
    classifier = RPClassifier(fake)

    result = classifier.addAttribute("count")

    fake.addAttribute.assert_called_once_with("count")
    assert result.getName() == "count"


def test_classifier_add_operation_wraps_result() -> None:
    fake = make_fake_element("Class")
    op = make_fake_element("Operation", getName="doIt")
    fake.addOperation.return_value = op
    classifier = RPClassifier(fake)

    result = classifier.addOperation("doIt")

    fake.addOperation.assert_called_once_with("doIt")
    assert result.getName() == "doIt"


def test_classifier_get_attributes_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getAttributes.return_value = make_fake_collection(
        [make_fake_element("Attribute", getName="count")]
    )
    classifier = RPClassifier(fake)

    attributes = classifier.getAttributes()

    assert len(attributes) == 1
    assert attributes[0].getName() == "count"


def test_classifier_get_operations_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getOperations.return_value = make_fake_collection(
        [make_fake_element("Operation", getName="doIt")]
    )
    classifier = RPClassifier(fake)

    operations = classifier.getOperations()

    assert len(operations) == 1
    assert operations[0].getName() == "doIt"


def test_classifier_add_generalization_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    classifier = RPClassifier(fake)

    classifier.addGeneralization(RPClassifier(base))

    fake.addGeneralization.assert_called_once_with(base)


def test_classifier_add_statechart_wraps_result() -> None:
    fake = make_fake_element("Class")
    statechart = make_fake_element("Statechart", getName="Behavior")
    fake.addStatechart.return_value = statechart
    classifier = RPClassifier(fake)

    result = classifier.addStatechart()

    fake.addStatechart.assert_called_once_with()
    assert result.getName() == "Behavior"
```

Path: `tests/elements/test_classifier.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_classifier.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.classifier'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPClassifier: wraps IRPClassifier, the shared base of IRPClass/IRPActor/IRPUseCase."""

from __future__ import annotations

from typing import Any

from py_rhapsody._core import RPCollection, RPUnit, call_com, wrap


class RPClassifier(RPUnit):
    """Wraps ``IRPClassifier``. Base class for ``RPClass``, ``RPActor``, ``RPUseCase``."""

    def addAttribute(self, name: str) -> "Any":
        return wrap(call_com(lambda: self._com.addAttribute(name)))

    def addOperation(self, name: str) -> "Any":
        return wrap(call_com(lambda: self._com.addOperation(name)))

    def getAttributes(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getAttributes()))

    def getOperations(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getOperations()))

    def addGeneralization(self, base_classifier: "RPClassifier") -> None:
        call_com(lambda: self._com.addGeneralization(base_classifier._com))

    def addStatechart(self) -> "Any":
        return wrap(call_com(lambda: self._com.addStatechart()))
```

Path: `py_rhapsody/elements/classifier.py`

(No `register_wrapper` call here — see the note above the tests.)

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_classifier.py -v`
Expected: 7 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/classifier.py tests/elements/test_classifier.py
git commit -m "feat: add RPClassifier base wrapper for IRPClassifier

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 9: `RPClass` (wraps `IRPClass`)

**Files:**
- Create: `py_rhapsody/elements/class_.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_class.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.class_.RPClass."""

from __future__ import annotations

from py_rhapsody._core import wrap
from py_rhapsody.elements.classifier import RPClassifier
from py_rhapsody.elements.class_ import RPClass
from tests.fakes import make_fake_element


def test_class_is_a_classifier() -> None:
    fake = make_fake_element("Class", getName="Widget")
    klass = RPClass(fake)

    assert isinstance(klass, RPClassifier)
    assert klass.getName() == "Widget"


def test_class_add_superclass_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    klass = RPClass(fake)

    klass.addSuperclass(RPClass(base))

    fake.addSuperclass.assert_called_once_with(base)


def test_class_add_constructor_wraps_result() -> None:
    fake = make_fake_element("Class")
    ctor = make_fake_element("Operation", getName="Widget")
    fake.addConstructor.return_value = ctor
    klass = RPClass(fake)

    result = klass.addConstructor("int x")

    fake.addConstructor.assert_called_once_with("int x")
    assert result.getName() == "Widget"


def test_class_add_destructor_wraps_result() -> None:
    fake = make_fake_element("Class")
    dtor = make_fake_element("Operation", getName="~Widget")
    fake.addDestructor.return_value = dtor
    klass = RPClass(fake)

    result = klass.addDestructor()

    fake.addDestructor.assert_called_once_with()
    assert result.getName() == "~Widget"


def test_class_get_is_abstract_delegates_to_com() -> None:
    fake = make_fake_element("Class", getIsAbstract=1)
    klass = RPClass(fake)

    assert klass.getIsAbstract() is True


def test_class_add_class_nested_wraps_result() -> None:
    fake = make_fake_element("Class")
    nested = make_fake_element("Class", getName="Inner")
    fake.addClass.return_value = nested
    klass = RPClass(fake)

    result = klass.addClass("Inner")

    fake.addClass.assert_called_once_with("Inner")
    assert result.getName() == "Inner"


def test_class_is_registered_for_meta_class_class() -> None:
    fake = make_fake_element("Class", getName="Widget")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPClass)
```

Path: `tests/elements/test_class.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_class.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.class_'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPClass: wraps IRPClass, a UML/SysML class in the Rhapsody model."""

from __future__ import annotations

from typing import Any

from py_rhapsody._core import call_com, register_wrapper, wrap
from py_rhapsody.elements.classifier import RPClassifier


class RPClass(RPClassifier):
    """Wraps ``IRPClass``."""

    def addSuperclass(self, super_class: "RPClass") -> None:
        call_com(lambda: self._com.addSuperclass(super_class._com))

    def addConstructor(self, arguments_data: str) -> "Any":
        return wrap(call_com(lambda: self._com.addConstructor(arguments_data)))

    def addDestructor(self) -> "Any":
        return wrap(call_com(lambda: self._com.addDestructor()))

    def getIsAbstract(self) -> bool:
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def addClass(self, name: str) -> "Any":
        return wrap(call_com(lambda: self._com.addClass(name)))


register_wrapper("Class", RPClass)
```

Path: `py_rhapsody/elements/class_.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import class_ as class_  # noqa: F401
from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_class.py -v`
Expected: 7 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/class_.py tests/elements/test_class.py
git commit -m "feat: add RPClass wrapper for IRPClass

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 10: `RPAttribute` (wraps `IRPAttribute`)

**Files:**
- Create: `py_rhapsody/elements/attribute.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_attribute.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.attribute.RPAttribute."""

from __future__ import annotations

from py_rhapsody._core import RPUnit, wrap
from py_rhapsody.elements.attribute import RPAttribute
from tests.fakes import make_fake_element


def test_attribute_is_a_unit() -> None:
    fake = make_fake_element("Attribute", getName="count")
    attribute = RPAttribute(fake)

    assert isinstance(attribute, RPUnit)
    assert attribute.getName() == "count"


def test_attribute_get_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getMultiplicity="1")
    attribute = RPAttribute(fake)

    assert attribute.getMultiplicity() == "1"


def test_attribute_set_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.setMultiplicity("0..*")

    fake.setMultiplicity.assert_called_once_with("0..*")


def test_attribute_get_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getIsStatic=0)
    attribute = RPAttribute(fake)

    assert attribute.getIsStatic() is False


def test_attribute_set_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.setIsStatic(True)

    fake.setIsStatic.assert_called_once_with(1)


def test_attribute_get_visibility_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getVisibility="private")
    attribute = RPAttribute(fake)

    assert attribute.getVisibility() == "private"


def test_attribute_set_visibility_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.setVisibility("public")

    fake.setVisibility.assert_called_once_with("public")


def test_attribute_get_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getDefaultValue="0")
    attribute = RPAttribute(fake)

    assert attribute.getDefaultValue() == "0"


def test_attribute_set_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.setDefaultValue("42")

    fake.setDefaultValue.assert_called_once_with("42")


def test_attribute_is_registered_for_meta_class_attribute() -> None:
    fake = make_fake_element("Attribute", getName="count")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPAttribute)
```

Path: `tests/elements/test_attribute.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_attribute.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.attribute'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPAttribute: wraps IRPAttribute, a class/package-level attribute or variable."""

from __future__ import annotations

from py_rhapsody._core import RPUnit, call_com, register_wrapper


class RPAttribute(RPUnit):
    """Wraps ``IRPAttribute``."""

    def getMultiplicity(self) -> str:
        return call_com(lambda: str(self._com.getMultiplicity()))

    def setMultiplicity(self, multiplicity: str) -> None:
        call_com(lambda: self._com.setMultiplicity(multiplicity))

    def getIsStatic(self) -> bool:
        return call_com(lambda: bool(self._com.getIsStatic()))

    def setIsStatic(self, is_static: bool) -> None:
        call_com(lambda: self._com.setIsStatic(1 if is_static else 0))

    def getVisibility(self) -> str:
        return call_com(lambda: str(self._com.getVisibility()))

    def setVisibility(self, visibility: str) -> None:
        call_com(lambda: self._com.setVisibility(visibility))

    def getDefaultValue(self) -> str:
        return call_com(lambda: str(self._com.getDefaultValue()))

    def setDefaultValue(self, default_value: str) -> None:
        call_com(lambda: self._com.setDefaultValue(default_value))


register_wrapper("Attribute", RPAttribute)
```

Path: `py_rhapsody/elements/attribute.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import attribute as attribute  # noqa: F401
from py_rhapsody.elements import class_ as class_  # noqa: F401
from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_attribute.py -v`
Expected: 10 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/attribute.py tests/elements/test_attribute.py
git commit -m "feat: add RPAttribute wrapper for IRPAttribute

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 11: `RPOperation` (wraps `IRPOperation`)

**Files:**
- Create: `py_rhapsody/elements/operation.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_operation.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.operation.RPOperation."""

from __future__ import annotations

from py_rhapsody._core import RPUnit, wrap
from py_rhapsody.elements.operation import RPOperation
from tests.fakes import make_fake_element


def test_operation_is_a_unit() -> None:
    fake = make_fake_element("Operation", getName="doIt")
    operation = RPOperation(fake)

    assert isinstance(operation, RPUnit)
    assert operation.getName() == "doIt"


def test_operation_get_body_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getBody="return 0;")
    operation = RPOperation(fake)

    assert operation.getBody() == "return 0;"


def test_operation_get_is_abstract_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getIsAbstract=1)
    operation = RPOperation(fake)

    assert operation.getIsAbstract() is True


def test_operation_get_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getIsStatic=0)
    operation = RPOperation(fake)

    assert operation.getIsStatic() is False


def test_operation_get_is_virtual_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getIsVirtual=1)
    operation = RPOperation(fake)

    assert operation.getIsVirtual() is True


def test_operation_get_returns_wraps_result() -> None:
    fake = make_fake_element("Operation")
    return_type = make_fake_element("Class", getName="int")
    fake.getReturns.return_value = return_type
    operation = RPOperation(fake)

    result = operation.getReturns()

    fake.getReturns.assert_called_once_with()
    assert result.getName() == "int"


def test_operation_create_auto_flow_chart_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)

    operation.createAutoFlowChart()

    fake.createAutoFlowChart.assert_called_once_with()


def test_operation_is_registered_for_meta_class_operation() -> None:
    fake = make_fake_element("Operation", getName="doIt")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPOperation)
```

Path: `tests/elements/test_operation.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_operation.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.operation'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPOperation: wraps IRPOperation, a class/package-level operation or function."""

from __future__ import annotations

from typing import Any

from py_rhapsody._core import RPUnit, call_com, register_wrapper, wrap


class RPOperation(RPUnit):
    """Wraps ``IRPOperation``."""

    def getBody(self) -> str:
        return call_com(lambda: str(self._com.getBody()))

    def getIsAbstract(self) -> bool:
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def getIsStatic(self) -> bool:
        return call_com(lambda: bool(self._com.getIsStatic()))

    def getIsVirtual(self) -> bool:
        return call_com(lambda: bool(self._com.getIsVirtual()))

    def getReturns(self) -> "Any":
        return wrap(call_com(lambda: self._com.getReturns()))

    def createAutoFlowChart(self) -> None:
        call_com(lambda: self._com.createAutoFlowChart())


register_wrapper("Operation", RPOperation)
```

Path: `py_rhapsody/elements/operation.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import attribute as attribute  # noqa: F401
from py_rhapsody.elements import class_ as class_  # noqa: F401
from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import operation as operation  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_operation.py -v`
Expected: 8 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/operation.py tests/elements/test_operation.py
git commit -m "feat: add RPOperation wrapper for IRPOperation

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 12: `RPActor` (wraps `IRPActor`)

**Files:**
- Create: `py_rhapsody/elements/actor.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_actor.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.actor.RPActor."""

from __future__ import annotations

from py_rhapsody._core import wrap
from py_rhapsody.elements.actor import RPActor
from py_rhapsody.elements.classifier import RPClassifier
from tests.fakes import make_fake_element


def test_actor_is_a_classifier() -> None:
    fake = make_fake_element("Actor", getName="Driver")
    actor = RPActor(fake)

    assert isinstance(actor, RPClassifier)
    assert actor.getName() == "Driver"


def test_actor_add_event_reception_with_event_wraps_result() -> None:
    fake = make_fake_element("Actor")
    event = make_fake_element("Event", getName="Start")
    reception = make_fake_element("EventReception", getName="onStart")
    fake.addEventReceptionWithEvent.return_value = reception
    actor = RPActor(fake)

    from py_rhapsody._core import RPModelElement

    result = actor.addEventReceptionWithEvent("onStart", RPModelElement(event))

    fake.addEventReceptionWithEvent.assert_called_once_with("onStart", event)
    assert result.getName() == "onStart"


def test_actor_get_is_behavior_overridden_delegates_to_com() -> None:
    fake = make_fake_element("Actor", getIsBehaviorOverriden=1)
    actor = RPActor(fake)

    assert actor.getIsBehaviorOverriden() is True


def test_actor_set_is_behavior_overridden_delegates_to_com() -> None:
    fake = make_fake_element("Actor")
    actor = RPActor(fake)

    actor.setIsBehaviorOverriden(False)

    fake.setIsBehaviorOverriden.assert_called_once_with(0)


def test_actor_is_registered_for_meta_class_actor() -> None:
    fake = make_fake_element("Actor", getName="Driver")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPActor)
```

Path: `tests/elements/test_actor.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_actor.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.actor'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPActor: wraps IRPActor, a UML actor (external role that interacts with the system)."""

from __future__ import annotations

from typing import Any

from py_rhapsody._core import RPModelElement, call_com, register_wrapper, wrap
from py_rhapsody.elements.classifier import RPClassifier


class RPActor(RPClassifier):
    """Wraps ``IRPActor``."""

    def addEventReceptionWithEvent(self, name: str, event: RPModelElement) -> "Any":
        return wrap(
            call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com))
        )

    def getIsBehaviorOverriden(self) -> bool:
        return call_com(lambda: bool(self._com.getIsBehaviorOverriden()))

    def setIsBehaviorOverriden(self, is_overridden: bool) -> None:
        call_com(
            lambda: self._com.setIsBehaviorOverriden(1 if is_overridden else 0)
        )


register_wrapper("Actor", RPActor)
```

Path: `py_rhapsody/elements/actor.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import actor as actor  # noqa: F401
from py_rhapsody.elements import attribute as attribute  # noqa: F401
from py_rhapsody.elements import class_ as class_  # noqa: F401
from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import operation as operation  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_actor.py -v`
Expected: 5 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/actor.py tests/elements/test_actor.py
git commit -m "feat: add RPActor wrapper for IRPActor

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 13: `RPUseCase` (wraps `IRPUseCase`)

**Files:**
- Create: `py_rhapsody/elements/usecase.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_usecase.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.usecase.RPUseCase."""

from __future__ import annotations

from py_rhapsody._core import wrap
from py_rhapsody.elements.classifier import RPClassifier
from py_rhapsody.elements.usecase import RPUseCase
from tests.fakes import make_fake_collection, make_fake_element


def test_usecase_is_a_classifier() -> None:
    fake = make_fake_element("UseCase", getName="Login")
    usecase = RPUseCase(fake)

    assert isinstance(usecase, RPClassifier)
    assert usecase.getName() == "Login"


def test_usecase_add_extension_point_delegates_to_com() -> None:
    fake = make_fake_element("UseCase")
    usecase = RPUseCase(fake)

    usecase.addExtensionPoint("failure")

    fake.addExtensionPoint.assert_called_once_with("failure")


def test_usecase_get_extension_points_returns_collection() -> None:
    fake = make_fake_element("UseCase")
    fake.getExtensionPoints.return_value = make_fake_collection(["failure"])
    usecase = RPUseCase(fake)

    points = usecase.getExtensionPoints()

    assert len(points) == 1
    assert points[0] == "failure"


def test_usecase_get_entry_points_returns_collection() -> None:
    fake = make_fake_element("UseCase")
    fake.getEntryPoints.return_value = make_fake_collection(["start"])
    usecase = RPUseCase(fake)

    points = usecase.getEntryPoints()

    assert len(points) == 1
    assert points[0] == "start"


def test_usecase_get_describing_diagrams_returns_collection() -> None:
    fake = make_fake_element("UseCase")
    diagram = make_fake_element("StatechartDiagram", getName="Flow")
    fake.getDescribingDiagrams.return_value = make_fake_collection([diagram])
    usecase = RPUseCase(fake)

    diagrams = usecase.getDescribingDiagrams()

    assert len(diagrams) == 1
    assert diagrams[0].getName() == "Flow"


def test_usecase_is_registered_for_meta_class_usecase() -> None:
    fake = make_fake_element("UseCase", getName="Login")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPUseCase)
```

Path: `tests/elements/test_usecase.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_usecase.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.usecase'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPUseCase: wraps IRPUseCase, a UML use case."""

from __future__ import annotations

from py_rhapsody._core import RPCollection, call_com, register_wrapper
from py_rhapsody.elements.classifier import RPClassifier


class RPUseCase(RPClassifier):
    """Wraps ``IRPUseCase``."""

    def addExtensionPoint(self, entry_point: str) -> None:
        call_com(lambda: self._com.addExtensionPoint(entry_point))

    def getExtensionPoints(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getExtensionPoints()))

    def getEntryPoints(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getEntryPoints()))

    def getDescribingDiagrams(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getDescribingDiagrams()))


register_wrapper("UseCase", RPUseCase)
```

Path: `py_rhapsody/elements/usecase.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import actor as actor  # noqa: F401
from py_rhapsody.elements import attribute as attribute  # noqa: F401
from py_rhapsody.elements import class_ as class_  # noqa: F401
from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import operation as operation  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
from py_rhapsody.elements import usecase as usecase  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_usecase.py -v`
Expected: 6 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/usecase.py tests/elements/test_usecase.py
git commit -m "feat: add RPUseCase wrapper for IRPUseCase

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 14: `RPInstance` (wraps `IRPInstance`)

**Files:**
- Create: `py_rhapsody/elements/instance.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_instance.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.instance.RPInstance."""

from __future__ import annotations

from py_rhapsody._core import RPUnit, wrap
from py_rhapsody.elements.instance import RPInstance
from tests.fakes import make_fake_collection, make_fake_element


def test_instance_is_a_unit() -> None:
    fake = make_fake_element("Instance", getName="driver1")
    instance = RPInstance(fake)

    assert isinstance(instance, RPUnit)
    assert instance.getName() == "driver1"


def test_instance_get_all_nested_elements_returns_collection() -> None:
    fake = make_fake_element("Instance")
    nested = make_fake_element("Attribute", getName="speed")
    fake.getAllNestedElements.return_value = make_fake_collection([nested])
    instance = RPInstance(fake)

    nested_elements = instance.getAllNestedElements()

    assert len(nested_elements) == 1
    assert nested_elements[0].getName() == "speed"


def test_instance_get_attribute_value_delegates_to_com() -> None:
    fake = make_fake_element("Instance", getAttributeValue="42")
    instance = RPInstance(fake)

    assert instance.getAttributeValue("speed") == "42"

    fake.getAttributeValue.assert_called_once_with("speed")


def test_instance_set_attribute_value_delegates_to_com() -> None:
    fake = make_fake_element("Instance")
    instance = RPInstance(fake)

    instance.setAttributeValue("speed", "88")

    fake.setAttributeValue.assert_called_once_with("speed", "88")


def test_instance_get_in_links_returns_collection() -> None:
    fake = make_fake_element("Instance")
    link = make_fake_element("Link", getName="conn1")
    fake.getInLinks.return_value = make_fake_collection([link])
    instance = RPInstance(fake)

    links = instance.getInLinks()

    assert len(links) == 1
    assert links[0].getName() == "conn1"


def test_instance_get_out_links_returns_collection() -> None:
    fake = make_fake_element("Instance")
    link = make_fake_element("Link", getName="conn2")
    fake.getOutLinks.return_value = make_fake_collection([link])
    instance = RPInstance(fake)

    links = instance.getOutLinks()

    assert len(links) == 1
    assert links[0].getName() == "conn2"


def test_instance_is_registered_for_meta_class_instance() -> None:
    fake = make_fake_element("Instance", getName="driver1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPInstance)
```

Path: `tests/elements/test_instance.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_instance.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.instance'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPInstance: wraps IRPInstance, an instance/object in the Rhapsody model."""

from __future__ import annotations

from py_rhapsody._core import RPCollection, RPUnit, call_com, register_wrapper


class RPInstance(RPUnit):
    """Wraps ``IRPInstance``."""

    def getAllNestedElements(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getAllNestedElements()))

    def getAttributeValue(self, attribute_name: str) -> str:
        return call_com(lambda: str(self._com.getAttributeValue(attribute_name)))

    def setAttributeValue(self, attribute_name: str, attribute_value: str) -> None:
        call_com(
            lambda: self._com.setAttributeValue(attribute_name, attribute_value)
        )

    def getInLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getInLinks()))

    def getOutLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getOutLinks()))


register_wrapper("Instance", RPInstance)
```

Path: `py_rhapsody/elements/instance.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import actor as actor  # noqa: F401
from py_rhapsody.elements import attribute as attribute  # noqa: F401
from py_rhapsody.elements import class_ as class_  # noqa: F401
from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import instance as instance  # noqa: F401
from py_rhapsody.elements import operation as operation  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
from py_rhapsody.elements import usecase as usecase  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_instance.py -v`
Expected: 7 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/instance.py tests/elements/test_instance.py
git commit -m "feat: add RPInstance wrapper for IRPInstance

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 15: `RPStatechart` (wraps `IRPStatechart`)

**Files:**
- Create: `py_rhapsody/elements/statechart.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_statechart.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.statechart.RPStatechart."""

from __future__ import annotations

from py_rhapsody._core import RPModelElement, RPUnit, wrap
from py_rhapsody.elements.statechart import RPStatechart
from tests.fakes import make_fake_element


def test_statechart_is_a_unit() -> None:
    fake = make_fake_element("Statechart", getName="Behavior")
    statechart = RPStatechart(fake)

    assert isinstance(statechart, RPUnit)
    assert statechart.getName() == "Behavior"


def test_statechart_add_new_node_by_type_wraps_result() -> None:
    fake = make_fake_element("Statechart")
    node = make_fake_element("State", getName="Idle")
    fake.addNewNodeByType.return_value = node
    statechart = RPStatechart(fake)

    result = statechart.addNewNodeByType("State", 10, 20, 100, 50)

    fake.addNewNodeByType.assert_called_once_with("State", 10, 20, 100, 50)
    assert result.getName() == "Idle"


def test_statechart_create_graphics_delegates_to_com() -> None:
    fake = make_fake_element("Statechart")
    statechart = RPStatechart(fake)

    statechart.createGraphics()

    fake.createGraphics.assert_called_once_with()


def test_statechart_close_diagram_delegates_to_com() -> None:
    fake = make_fake_element("Statechart")
    statechart = RPStatechart(fake)

    statechart.closeDiagram()

    fake.closeDiagram.assert_called_once_with()


def test_statechart_delete_state_delegates_to_com() -> None:
    fake = make_fake_element("Statechart")
    state = make_fake_element("State", getName="Idle")
    statechart = RPStatechart(fake)

    statechart.deleteState(RPModelElement(state))

    fake.deleteState.assert_called_once_with(state)


def test_statechart_is_registered_for_meta_class_statechart() -> None:
    fake = make_fake_element("Statechart", getName="Behavior")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPStatechart)
```

Path: `tests/elements/test_statechart.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_statechart.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.statechart'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPStatechart: wraps IRPStatechart, a class's behavioral state machine."""

from __future__ import annotations

from typing import Any

from py_rhapsody._core import RPModelElement, RPUnit, call_com, register_wrapper, wrap


class RPStatechart(RPUnit):
    """Wraps ``IRPStatechart``."""

    def addNewNodeByType(
        self, meta_type: str, x_position: int, y_position: int, width: int, height: int
    ) -> "Any":
        return wrap(
            call_com(
                lambda: self._com.addNewNodeByType(
                    meta_type, x_position, y_position, width, height
                )
            )
        )

    def createGraphics(self) -> None:
        call_com(lambda: self._com.createGraphics())

    def closeDiagram(self) -> None:
        call_com(lambda: self._com.closeDiagram())

    def deleteState(self, state: RPModelElement) -> None:
        call_com(lambda: self._com.deleteState(state._com))


register_wrapper("Statechart", RPStatechart)
```

Path: `py_rhapsody/elements/statechart.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import actor as actor  # noqa: F401
from py_rhapsody.elements import attribute as attribute  # noqa: F401
from py_rhapsody.elements import class_ as class_  # noqa: F401
from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import instance as instance  # noqa: F401
from py_rhapsody.elements import operation as operation  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
from py_rhapsody.elements import statechart as statechart  # noqa: F401
from py_rhapsody.elements import usecase as usecase  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_statechart.py -v`
Expected: 6 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/statechart.py tests/elements/test_statechart.py
git commit -m "feat: add RPStatechart wrapper for IRPStatechart

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 16: `RPRequirement` (wraps `IRPRequirement`)

**Files:**
- Create: `py_rhapsody/elements/requirement.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_requirement.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.requirement.RPRequirement."""

from __future__ import annotations

from py_rhapsody._core import RPUnit, wrap
from py_rhapsody.elements.requirement import RPRequirement
from tests.fakes import make_fake_element


def test_requirement_is_a_unit() -> None:
    fake = make_fake_element("Requirement", getName="REQ-1")
    requirement = RPRequirement(fake)

    assert isinstance(requirement, RPUnit)
    assert requirement.getName() == "REQ-1"


def test_requirement_get_requirement_id_delegates_to_com() -> None:
    fake = make_fake_element("Requirement", getRequirementID="REQ-001")
    requirement = RPRequirement(fake)

    assert requirement.getRequirementID() == "REQ-001"


def test_requirement_set_requirement_id_delegates_to_com() -> None:
    fake = make_fake_element("Requirement")
    requirement = RPRequirement(fake)

    requirement.setRequirementID("REQ-002")

    fake.setRequirementID.assert_called_once_with("REQ-002")


def test_requirement_is_registered_for_meta_class_requirement() -> None:
    fake = make_fake_element("Requirement", getName="REQ-1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPRequirement)
```

Path: `tests/elements/test_requirement.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_requirement.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.requirement'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPRequirement: wraps IRPRequirement, a traceable requirement in the model."""

from __future__ import annotations

from py_rhapsody._core import RPUnit, call_com, register_wrapper


class RPRequirement(RPUnit):
    """Wraps ``IRPRequirement``."""

    def getRequirementID(self) -> str:
        return call_com(lambda: str(self._com.getRequirementID()))

    def setRequirementID(self, requirement_id: str) -> None:
        call_com(lambda: self._com.setRequirementID(requirement_id))


register_wrapper("Requirement", RPRequirement)
```

Path: `py_rhapsody/elements/requirement.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import actor as actor  # noqa: F401
from py_rhapsody.elements import attribute as attribute  # noqa: F401
from py_rhapsody.elements import class_ as class_  # noqa: F401
from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import instance as instance  # noqa: F401
from py_rhapsody.elements import operation as operation  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
from py_rhapsody.elements import requirement as requirement  # noqa: F401
from py_rhapsody.elements import statechart as statechart  # noqa: F401
from py_rhapsody.elements import usecase as usecase  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_requirement.py -v`
Expected: 4 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/requirement.py tests/elements/test_requirement.py
git commit -m "feat: add RPRequirement wrapper for IRPRequirement

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 17: `RPDiagram` (wraps `IRPDiagram`)

**Files:**
- Create: `py_rhapsody/elements/diagram.py`
- Modify: `py_rhapsody/elements/__init__.py`
- Test: `tests/elements/test_diagram.py`

Note: concrete diagram meta classes in Rhapsody (e.g. `"StatechartDiagram"`,
`"ObjectModelDiagram"`, `"SequenceDiagram"`) are the values actually returned
by `getMetaClass()` on a real diagram COM object — there is no bare
`"Diagram"` meta class. `RPDiagram` is registered under `"ActivityDiagram"`
here as the first concrete diagram type; the remaining diagram meta classes
follow the same mechanical `register_wrapper(...)` pattern and are tracked
as future work per the spec's "Open Items" section, not blocking this task.

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.elements.diagram.RPDiagram."""

from __future__ import annotations

from py_rhapsody._core import RPModelElement, RPUnit, wrap
from py_rhapsody.elements.diagram import RPDiagram
from tests.fakes import make_fake_collection, make_fake_element


def test_diagram_is_a_unit() -> None:
    fake = make_fake_element("ActivityDiagram", getName="MainFlow")
    diagram = RPDiagram(fake)

    assert isinstance(diagram, RPUnit)
    assert diagram.getName() == "MainFlow"


def test_diagram_close_diagram_delegates_to_com() -> None:
    fake = make_fake_element("ActivityDiagram")
    diagram = RPDiagram(fake)

    diagram.closeDiagram()

    fake.closeDiagram.assert_called_once_with()


def test_diagram_add_text_box_delegates_to_com_and_wraps_result() -> None:
    fake = make_fake_element("ActivityDiagram")
    text_box = make_fake_element("GraphElement", getName="Note1")
    fake.addTextBox.return_value = text_box
    diagram = RPDiagram(fake)

    result = diagram.addTextBox("hello", 0, 0, 50, 20)

    fake.addTextBox.assert_called_once_with("hello", 0, 0, 50, 20)
    assert result.getName() == "Note1"


def test_diagram_get_custom_views_returns_collection() -> None:
    fake = make_fake_element("ActivityDiagram")
    view = make_fake_element("Package", getName="CustomView1")
    fake.getCustomViews.return_value = make_fake_collection([view])
    diagram = RPDiagram(fake)

    views = diagram.getCustomViews()

    assert len(views) == 1
    assert views[0].getName() == "CustomView1"


def test_diagram_get_corresponding_graphic_elements_returns_collection() -> None:
    fake = make_fake_element("ActivityDiagram")
    graphic = make_fake_element("GraphElement", getName="Shape1")
    fake.getCorrespondingGraphicElements.return_value = make_fake_collection(
        [graphic]
    )
    diagram = RPDiagram(fake)
    model_element = make_fake_element("Class", getName="Widget")

    elements = diagram.getCorrespondingGraphicElements(RPModelElement(model_element))

    fake.getCorrespondingGraphicElements.assert_called_once_with(model_element)
    assert len(elements) == 1
    assert elements[0].getName() == "Shape1"


def test_diagram_is_registered_for_meta_class_activity_diagram() -> None:
    fake = make_fake_element("ActivityDiagram", getName="MainFlow")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPDiagram)
```

Path: `tests/elements/test_diagram.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/elements/test_diagram.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.elements.diagram'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RPDiagram: wraps IRPDiagram, the base interface for all Rhapsody diagram types."""

from __future__ import annotations

from typing import Any

from py_rhapsody._core import RPCollection, RPModelElement, RPUnit, call_com, register_wrapper, wrap


class RPDiagram(RPUnit):
    """Wraps ``IRPDiagram``."""

    def closeDiagram(self) -> None:
        call_com(lambda: self._com.closeDiagram())

    def addTextBox(
        self, text: str, x_position: int, y_position: int, width: int, height: int
    ) -> "Any":
        return wrap(
            call_com(
                lambda: self._com.addTextBox(
                    text, x_position, y_position, width, height
                )
            )
        )

    def getCustomViews(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getCustomViews()))

    def getCorrespondingGraphicElements(
        self, model_element: RPModelElement
    ) -> RPCollection:
        return RPCollection(
            call_com(
                lambda: self._com.getCorrespondingGraphicElements(model_element._com)
            )
        )


register_wrapper("ActivityDiagram", RPDiagram)
```

Path: `py_rhapsody/elements/diagram.py`

- [ ] **Step 4: Register the module for import side effects**

Update `py_rhapsody/elements/__init__.py`:

```python
"""Concrete Rhapsody element wrappers, registered with py_rhapsody._core.wrap()."""

from __future__ import annotations

from py_rhapsody.elements import actor as actor  # noqa: F401
from py_rhapsody.elements import attribute as attribute  # noqa: F401
from py_rhapsody.elements import class_ as class_  # noqa: F401
from py_rhapsody.elements import classifier as classifier  # noqa: F401
from py_rhapsody.elements import diagram as diagram  # noqa: F401
from py_rhapsody.elements import instance as instance  # noqa: F401
from py_rhapsody.elements import operation as operation  # noqa: F401
from py_rhapsody.elements import package as package  # noqa: F401
from py_rhapsody.elements import project as project  # noqa: F401
from py_rhapsody.elements import requirement as requirement  # noqa: F401
from py_rhapsody.elements import statechart as statechart  # noqa: F401
from py_rhapsody.elements import usecase as usecase  # noqa: F401
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/elements/test_diagram.py -v`
Expected: 6 passed

- [ ] **Step 6: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 7: Commit**

```bash
git add py_rhapsody/elements/__init__.py py_rhapsody/elements/diagram.py tests/elements/test_diagram.py
git commit -m "feat: add RPDiagram wrapper for IRPDiagram

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 18: `RhapsodyApplication` (wraps `IRPApplication`, connection entry point)

**Files:**
- Create: `py_rhapsody/application.py`
- Test: `tests/test_application.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for py_rhapsody.application.RhapsodyApplication."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from py_rhapsody.application import RhapsodyApplication
from py_rhapsody.elements.project import RPProject
from py_rhapsody.exceptions import RhapsodyConnectionError
from tests.fakes import make_com_error, make_fake_collection, make_fake_element


@patch("py_rhapsody.application.win32com.client.GetActiveObject")
def test_attach_wraps_active_com_object(mock_get_active_object: MagicMock) -> None:
    fake_app = MagicMock(name="FakeApplication")
    mock_get_active_object.return_value = fake_app

    app = RhapsodyApplication.attach()

    mock_get_active_object.assert_called_once_with("Rhapsody.Application")
    assert app._com is fake_app


@patch("py_rhapsody.application.win32com.client.GetActiveObject")
def test_attach_raises_connection_error_when_none_running(
    mock_get_active_object: MagicMock,
) -> None:
    mock_get_active_object.side_effect = make_com_error("no running instance")

    with pytest.raises(RhapsodyConnectionError):
        RhapsodyApplication.attach()


@patch("py_rhapsody.application.win32com.client.Dispatch")
def test_launch_wraps_new_com_object(mock_dispatch: MagicMock) -> None:
    fake_app = MagicMock(name="FakeApplication")
    mock_dispatch.return_value = fake_app

    app = RhapsodyApplication.launch()

    mock_dispatch.assert_called_once_with("Rhapsody.Application")
    assert app._com is fake_app


@patch("py_rhapsody.application.win32com.client.Dispatch")
@patch("py_rhapsody.application.win32com.client.GetActiveObject")
def test_connect_prefers_attach_when_available(
    mock_get_active_object: MagicMock, mock_dispatch: MagicMock
) -> None:
    fake_app = MagicMock(name="FakeApplication")
    mock_get_active_object.return_value = fake_app

    app = RhapsodyApplication.connect()

    mock_get_active_object.assert_called_once_with("Rhapsody.Application")
    mock_dispatch.assert_not_called()
    assert app._com is fake_app


@patch("py_rhapsody.application.win32com.client.Dispatch")
@patch("py_rhapsody.application.win32com.client.GetActiveObject")
def test_connect_falls_back_to_launch_when_attach_fails(
    mock_get_active_object: MagicMock, mock_dispatch: MagicMock
) -> None:
    mock_get_active_object.side_effect = make_com_error("no running instance")
    fake_app = MagicMock(name="FakeApplication")
    mock_dispatch.return_value = fake_app

    app = RhapsodyApplication.connect()

    mock_dispatch.assert_called_once_with("Rhapsody.Application")
    assert app._com is fake_app


def test_open_project_wraps_result_as_rpproject() -> None:
    fake_app = MagicMock(name="FakeApplication")
    fake_project = make_fake_element("Project", getName="MyProject")
    fake_app.openProject.return_value = fake_project
    app = RhapsodyApplication(fake_app)

    project = app.openProject("C:/models/MyProject.rpy")

    fake_app.openProject.assert_called_once_with("C:/models/MyProject.rpy")
    assert isinstance(project, RPProject)
    assert project.getName() == "MyProject"


def test_active_project_wraps_result_as_rpproject() -> None:
    fake_app = MagicMock(name="FakeApplication")
    fake_project = make_fake_element("Project", getName="ActiveOne")
    fake_app.activeProject.return_value = fake_project
    app = RhapsodyApplication(fake_app)

    project = app.activeProject()

    assert isinstance(project, RPProject)
    assert project.getName() == "ActiveOne"


def test_get_projects_returns_collection_of_rpproject() -> None:
    fake_app = MagicMock(name="FakeApplication")
    fake_project = make_fake_element("Project", getName="P1")
    fake_app.getProjects.return_value = make_fake_collection([fake_project])
    app = RhapsodyApplication(fake_app)

    projects = app.getProjects()

    assert len(projects) == 1
    assert isinstance(projects[0], RPProject)
    assert projects[0].getName() == "P1"


def test_quit_delegates_to_com() -> None:
    fake_app = MagicMock(name="FakeApplication")
    app = RhapsodyApplication(fake_app)

    app.quit()

    fake_app.quit.assert_called_once_with()
```

Path: `tests/test_application.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_application.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'py_rhapsody.application'`

- [ ] **Step 3: Write minimal implementation**

```python
"""RhapsodyApplication: the entry point for connecting to IBM Rhapsody.

Wraps ``IRPApplication``. Unlike model elements, ``IRPApplication`` is not
an ``IRPModelElement`` subtype, so this class does not derive from
``RPModelElement`` and is not registered with ``wrap()``.
"""

from __future__ import annotations

from typing import Any

import pywintypes
import win32com.client

from py_rhapsody._core import RPCollection, call_com
from py_rhapsody.elements.project import RPProject
from py_rhapsody.exceptions import RhapsodyConnectionError

_PROG_ID = "Rhapsody.Application"


class RhapsodyApplication:
    """Wraps ``IRPApplication``, the top-level Rhapsody automation object."""

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    @classmethod
    def attach(cls) -> "RhapsodyApplication":
        """Attach to an already-running Rhapsody instance.

        Raises ``RhapsodyConnectionError`` if no instance is running.
        """
        try:
            com_obj = win32com.client.GetActiveObject(_PROG_ID)
        except pywintypes.com_error as exc:
            raise RhapsodyConnectionError(
                f"No running Rhapsody instance found: {exc}"
            ) from exc
        return cls(com_obj)

    @classmethod
    def launch(cls) -> "RhapsodyApplication":
        """Start a new Rhapsody instance."""
        com_obj = win32com.client.Dispatch(_PROG_ID)
        return cls(com_obj)

    @classmethod
    def connect(cls, prefer_attach: bool = True) -> "RhapsodyApplication":
        """Attach to a running instance if possible, otherwise launch a new one."""
        if prefer_attach:
            try:
                return cls.attach()
            except RhapsodyConnectionError:
                pass
        return cls.launch()

    def openProject(self, filename: str) -> RPProject:
        return RPProject(call_com(lambda: self._com.openProject(filename)))

    def activeProject(self) -> RPProject:
        return RPProject(call_com(lambda: self._com.activeProject()))

    def getProjects(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getProjects()))

    def quit(self) -> None:
        call_com(lambda: self._com.quit())
```

Path: `py_rhapsody/application.py`

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_application.py -v`
Expected: 9 passed

- [ ] **Step 5: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 6: Commit**

```bash
git add py_rhapsody/application.py tests/test_application.py
git commit -m "feat: add RhapsodyApplication connection entry point

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 19: Public package API surface (`py_rhapsody/__init__.py`)

**Files:**
- Modify: `py_rhapsody/__init__.py`
- Test: `tests/test_public_api.py`

- [ ] **Step 1: Write the failing tests**

```python
"""Tests for the public py_rhapsody package API surface."""

from __future__ import annotations

import py_rhapsody
from py_rhapsody._core import wrap
from tests.fakes import make_fake_element


def test_rhapsody_application_is_exported() -> None:
    assert py_rhapsody.RhapsodyApplication is not None


def test_exceptions_are_exported() -> None:
    assert py_rhapsody.RhapsodyConnectionError is not None
    assert py_rhapsody.RhapsodyRuntimeException is not None


def test_importing_package_registers_all_core_element_wrappers() -> None:
    for meta_class, expected_name in [
        ("Project", "RPProject"),
        ("Package", "RPPackage"),
        ("Class", "RPClass"),
        ("Attribute", "RPAttribute"),
        ("Operation", "RPOperation"),
        ("Actor", "RPActor"),
        ("UseCase", "RPUseCase"),
        ("Instance", "RPInstance"),
        ("Statechart", "RPStatechart"),
        ("Requirement", "RPRequirement"),
        ("ActivityDiagram", "RPDiagram"),
    ]:
        fake = make_fake_element(meta_class, getName="X")
        wrapped = wrap(fake)
        assert type(wrapped).__name__ == expected_name, meta_class
```

Path: `tests/test_public_api.py`

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_public_api.py -v`
Expected: FAIL with `AttributeError: module 'py_rhapsody' has no attribute 'RhapsodyApplication'`

- [ ] **Step 3: Write minimal implementation**

```python
"""py_rhapsody: Pythonic wrapper around the IBM Rhapsody COM API.

Method names on wrapped elements mirror the Rhapsody Java API
(com.telelogic.rhapsody.core) exactly, so existing Rhapsody Java API
knowledge transfers directly. Importing this package registers all core
element wrappers with the internal ``wrap()`` dispatch factory.
"""

from __future__ import annotations

from py_rhapsody import elements as elements  # noqa: F401  (populates the wrap() registry)
from py_rhapsody._core import RPCollection, RPModelElement, RPUnit
from py_rhapsody.application import RhapsodyApplication
from py_rhapsody.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException

__all__ = [
    "RPCollection",
    "RPModelElement",
    "RPUnit",
    "RhapsodyApplication",
    "RhapsodyConnectionError",
    "RhapsodyRuntimeException",
]
```

Path: `py_rhapsody/__init__.py`

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_public_api.py -v`
Expected: 3 passed

- [ ] **Step 5: Verification gate**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues.

- [ ] **Step 6: Commit**

```bash
git add py_rhapsody/__init__.py tests/test_public_api.py
git commit -m "feat: expose public py_rhapsody API and wire up wrapper registration

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 20: Full-suite verification and README update

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Run the entire test suite**

Run: `pytest -v`
Expected: all tests across `tests/test_exceptions.py`, `tests/test_core.py`,
`tests/test_application.py`, `tests/test_public_api.py`, and
`tests/elements/test_*.py` pass (approximately 115+ tests, 0 failures).

- [ ] **Step 2: Run the full verification gate across the whole repository**

```bash
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```
Expected: all three report no issues (e.g. `All checks passed!`, `All done!`,
`Success: no issues found in N source files`).

- [ ] **Step 3: Update the README with usage instructions**

Replace the content of `README.md`:

```markdown
# py_rhapsody

A Pythonic, object-oriented wrapper around the IBM Rhapsody COM API for
Windows. Method names and class hierarchy mirror the Rhapsody Java API
(`com.telelogic.rhapsody.core`) exactly, so existing Rhapsody Java API
knowledge and documentation transfer directly.

## Requirements

- Windows with a licensed IBM Rhapsody installation (COM automation is
  Windows-only).
- Python 3.9+
- `pywin32`

## Installation

```bash
pip install -e .[dev]
```

## Usage

```python
from py_rhapsody import RhapsodyApplication

# Attaches to a running Rhapsody instance, or launches a new one if none
# is running.
app = RhapsodyApplication.connect()

project = app.openProject(r"C:\Models\MyProject.rpy")
package = project.addPackage("Sensors")
sensor_class = package.addClass("TemperatureSensor")
sensor_class.addAttribute("currentTemperature")
sensor_class.addOperation("readTemperature")

project.save()
```

## Development

```bash
pip install -e .[dev]
pytest
ruff check py_rhapsody tests
black --check py_rhapsody tests
mypy py_rhapsody
```

Tests run entirely against mocked COM objects (see `tests/fakes.py`) — no
Rhapsody installation or license is required to run the test suite.

## Design

See `docs/superpowers/specs/2026-07-06-py-rhapsody-com-api-design.md` for
the full architecture and design rationale.
```

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add usage instructions and development workflow to README

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Summary of what this plan builds

- `py_rhapsody/exceptions.py` — `RhapsodyRuntimeException`, `RhapsodyConnectionError`
- `py_rhapsody/_core.py` — `call_com`, `RPModelElement`, `RPUnit`, `RPCollection`, `wrap()`, `register_wrapper()`
- `py_rhapsody/application.py` — `RhapsodyApplication` (attach/launch/connect, project navigation)
- `py_rhapsody/elements/` — `RPProject`, `RPPackage`, `RPClassifier`, `RPClass`, `RPAttribute`, `RPOperation`, `RPActor`, `RPUseCase`, `RPInstance`, `RPStatechart`, `RPRequirement`, `RPDiagram`
- `py_rhapsody/__init__.py` — public API surface
- Full mock-based test suite under `tests/`, no Rhapsody installation required
- `ruff`, `black`, `mypy` all passing at every commit

## Future work (not in this plan, tracked from the spec's Open Items)

- Expand wrapper coverage to the remaining ~140+ `IRPxxx` interfaces using
  the same `register_wrapper()` pattern established here.
- Package/publish to PyPI.
- Higher-level convenience helpers built on top of the core wrappers.

