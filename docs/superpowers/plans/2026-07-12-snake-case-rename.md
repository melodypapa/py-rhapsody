# Snake-Case Unification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename all camelCase public methods on COM wrapper classes to snake_case across the entire codebase via an automated script.

**Architecture:** A single-purpose Python script (`scripts/rename_to_snake_case.py`) using `ast` for method detection and `tokenize` for source-safe replacement. Executed once; changes reviewed and committed.

**Tech Stack:** Python 3.8+, standard library only (ast, tokenize, pathlib, json, argparse)

## Global Constraints

- Clean break — no deprecated aliases
- COM calls (`self._com.*`) and test fakes (`fake.*`) must NOT be renamed
- `_get_method_or_property` / `_set_method_or_property` string args must NOT be renamed
- `make_fake_element` keyword arguments must NOT be renamed
- All comment blocks, docstrings, and formatting must be preserved

---

## File Structure

### Created

| File | Purpose |
|------|---------|
| `scripts/camel_to_snake.py` | Pure conversion function + tests inline |
| `scripts/extract_mapping.py` | AST scanner to build old→new name mapping |
| `scripts/rename_engine.py` | Token-based source rewriter |
| `scripts/rename_to_snake_case.py` | CLI entry point (wires 1-3) |
| `tests/unit/scripts/__init__.py` | Empty test package |
| `tests/unit/scripts/test_camel_to_snake.py` | Tests for conversion |
| `tests/unit/scripts/test_extract_mapping.py` | Tests for AST scanner |
| `tests/unit/scripts/test_rename_engine.py` | Tests for rename logic |

### Modified

| File | What changes |
|------|-------------|
| `src/rhapsody_cli/**/*.py` (~70 files) | Method names renamed by script |
| `tests/unit/**/test_*.py` (~40 files) | Wrapper call sites renamed by script |
| `AGENTS.md` | Convention documentation updated manually |
| `src/rhapsody_cli/models/core.py` | Docstring on RPModelElement updated manually |

---

### Task 1: `camel_to_snake` conversion utility

**Files:**
- Create: `scripts/camel_to_snake.py`
- Test: `tests/unit/scripts/test_camel_to_snake.py`

**Interfaces:**
- Produces: `camel_to_snake(name: str) -> str`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/scripts/test_camel_to_snake.py
import sys
sys.path.insert(0, "scripts")

from camel_to_snake import camel_to_snake


def test_simple_getter():
    assert camel_to_snake("getName") == "get_name"


def test_simple_setter():
    assert camel_to_snake("setName") == "set_name"


def test_get_is_prefix():
    assert camel_to_snake("getIsAbstract") == "get_is_abstract"
    assert camel_to_snake("setIsAbstract") == "set_is_abstract"


def test_consecutive_uppercase():
    assert camel_to_snake("getGUID") == "get_guid"
    assert camel_to_snake("getOSLCLinks") == "get_oslc_links"
    assert camel_to_snake("getRmmUrl") == "get_rmm_url"


def test_no_get_set_prefix():
    assert camel_to_snake("addClass") == "add_class"
    assert camel_to_snake("deleteFromProject") == "delete_from_project"
    assert camel_to_snake("errorMessage") == "error_message"


def test_long_compound_name():
    assert camel_to_snake("getPropertyValueConditionalExplicit") == "get_property_value_conditional_explicit"
    assert camel_to_snake("getNestedElementsByMetaClass") == "get_nested_elements_by_meta_class"
    assert camel_to_snake("becomeTemplateInstantiationOf") == "become_template_instantiation_of"
    assert camel_to_snake("synchronizeTemplateInstantiation") == "synchronize_template_instantiation"


def test_ti_and_id():
    assert camel_to_snake("getTi") == "get_ti"
    assert camel_to_snake("setTi") == "set_ti"
    assert camel_to_snake("getBinaryID") == "get_binary_id"


def test_already_snake_case_is_unchanged():
    assert camel_to_snake("already_snake") == "already_snake"


def test_empty_string():
    assert camel_to_snake("") == ""
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
pytest tests/unit/scripts/test_camel_to_snake.py -v
```
Expected: FAIL — ModuleNotFoundError or similar

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/camel_to_snake.py
import re


def camel_to_snake(name: str) -> str:
    if not name:
        return name
    result = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    result = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", result)
    return result.lower()
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
pytest tests/unit/scripts/test_camel_to_snake.py -v
```
Expected: PASS

- [ ] **Step 5: Create `__init__.py` and commit**

```bash
mkdir -p tests/unit/scripts
touch tests/unit/scripts/__init__.py
git add scripts/camel_to_snake.py tests/unit/scripts/__init__.py tests/unit/scripts/test_camel_to_snake.py
git commit -m "feat: add camel_to_snake conversion utility"
```

---

### Task 2: Method mapping extraction (AST scanner)

**Files:**
- Create: `scripts/extract_mapping.py`
- Test: `tests/unit/scripts/test_extract_mapping.py`

**Interfaces:**
- Consumes: `camel_to_snake(name: str) -> str` from Task 1
- Produces: `extract_mapping(source_paths: List[Path], output_json: Optional[Path] = None) -> Dict[str, str]`
  - `source_paths`: mix of `.py` files and directories (searched recursively)

- [ ] **Step 1: Write failing test**

```python
# tests/unit/scripts/test_extract_mapping.py
import sys
sys.path.insert(0, "scripts")

from pathlib import Path
from extract_mapping import extract_mapping


SAMPLE_CLASS = """
class RPModelElement:
    def getName(self):
        return something

    def setName(self, name):
        pass

    def getGUID(self):
        return something

    def errorMessage(self):
        return ""
"""


def test_extract_mapping_from_directory(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir(parents=True)
    mod = src / "model_test.py"
    mod.write_text(SAMPLE_CLASS)

    mapping = extract_mapping([src])

    assert mapping["getName"] == "get_name"
    assert mapping["setName"] == "set_name"
    assert mapping["getGUID"] == "get_guid"
    assert mapping["errorMessage"] == "error_message"
    assert len(mapping) == 4


def test_extract_mapping_from_single_file(tmp_path: Path):
    app_file = tmp_path / "application.py"
    app_file.write_text("""
class RhapsodyApplication:
    def openProject(self):
        pass
    def closeAllProjects(self):
        pass
""")
    mapping = extract_mapping([app_file])

    assert mapping["openProject"] == "open_project"
    assert mapping["closeAllProjects"] == "close_all_projects"
    assert len(mapping) == 2


def test_private_methods_not_included(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir(parents=True)
    mod = src / "model_test.py"
    mod.write_text("""
class RPModelElement:
    def _internal(self):
        pass
""")
    mapping = extract_mapping([src])
    assert len(mapping) == 0


def test_method_without_uppercase_not_included(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir(parents=True)
    mod = src / "model_test.py"
    mod.write_text("""
class Foo:
    def already_snake(self):
        pass
""")
    mapping = extract_mapping([src])
    assert len(mapping) == 0


def test_output_to_json(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir(parents=True)
    mod = src / "model_test.py"
    mod.write_text("""
class RPModelElement:
    def getName(self):
        pass
""")
    json_path = tmp_path / "mapping.json"
    extract_mapping([src], output_json=json_path)

    import json
    data = json.loads(json_path.read_text())
    assert data["getName"] == "get_name"
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
pytest tests/unit/scripts/test_extract_mapping.py -v
```
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/extract_mapping.py
import ast
import json
from pathlib import Path
from typing import Dict, List

from camel_to_snake import camel_to_snake


def _scan_file(file_path: Path, mapping: Dict[str, str]) -> None:
    tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            name = node.name
            if name.startswith("_"):
                continue
            if name == name.lower():
                continue
            snake = camel_to_snake(name)
            mapping[name] = snake


def _collect_files(source_paths: List[Path]) -> List[Path]:
    files: List[Path] = []
    for sp in source_paths:
        if sp.is_file():
            files.append(sp)
        elif sp.is_dir():
            for py in sp.rglob("*.py"):
                if py.name.startswith("__"):
                    continue
                files.append(py)
    return files


def extract_mapping(source_paths, output_json=None) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for path in _collect_files(source_paths):
        try:
            _scan_file(path, mapping)
        except SyntaxError:
            continue
    if output_json:
        output_json.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    return mapping
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
pytest tests/unit/scripts/test_extract_mapping.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/extract_mapping.py tests/unit/scripts/test_extract_mapping.py
git commit -m "feat: add AST-based method mapping extractor"
```

---

### Task 3: Token-based rename engine

**Files:**
- Create: `scripts/rename_engine.py`
- Test: `tests/unit/scripts/test_rename_engine.py`

**Interfaces:**
- Consumes: `extract_mapping(...)` mapping from Task 2
- Produces: `apply_rename(file_path: Path, mapping: Dict[str, str], category: str = "model") -> List[Tuple[int, str, str]]`

- [ ] **Step 1: Write test for model file renaming**

```python
# tests/unit/scripts/test_rename_engine.py
import sys
sys.path.insert(0, "scripts")

from pathlib import Path
from rename_engine import apply_rename


MODEL_INPUT = """class RPModelElement:
    def getName(self):
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getName", "name"))

    def getMetaClass(self):
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMetaClass", "metaClass"))

    def addAssociation(self, end1, end2, name):
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addAssociation(end1._com, end2._com, name)))

    def errorMessage(self):
        return str(AbstractRPModelElement.call_com(lambda: self._com.errorMessage()))
"""

MODEL_EXPECTED = """class RPModelElement:
    def get_name(self):
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getName", "name"))

    def get_meta_class(self):
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMetaClass", "metaClass"))

    def add_association(self, end1, end2, name):
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addAssociation(end1._com, end2._com, name)))

    def error_message(self):
        return str(AbstractRPModelElement.call_com(lambda: self._com.errorMessage()))
"""

MAPPING = {
    "getName": "get_name",
    "getMetaClass": "get_meta_class",
    "addAssociation": "add_association",
    "errorMessage": "error_message",
}


def test_model_file_rename(tmp_path: Path):
    source = tmp_path / "model.py"
    source.write_text(MODEL_INPUT)
    changes = apply_rename(source, MAPPING, category="model")
    assert source.read_text() == MODEL_EXPECTED
    assert len(changes) == 4


def test_action_file_rename(tmp_path: Path):
    action_input = """class ClassListAction:
    def _collect_class_names(self, package):
        classes = package.getClasses()
        return [cls.getName() for cls in classes]

    def _resolve_and_validate_package(self, path):
        root = self._get_active_root()
        container = self._resolve_container_or_element(root, path, resolve_element=False)
        meta_class = container.getMetaClass()
        return container
"""
    action_expected = """class ClassListAction:
    def _collect_class_names(self, package):
        classes = package.get_classes()
        return [cls.get_name() for cls in classes]

    def _resolve_and_validate_package(self, path):
        root = self._get_active_root()
        container = self._resolve_container_or_element(root, path, resolve_element=False)
        meta_class = container.get_meta_class()
        return container
"""
    source = tmp_path / "action.py"
    source.write_text(action_input)
    changes = apply_rename(source, MAPPING, category="action")
    assert source.read_text() == action_expected
    assert len(changes) == 3


def test_test_file_rename_preserves_fake_calls(tmp_path: Path):
    test_input = """def test_class_get_name():
    fake = make_fake_element("Class", getName="Widget")
    klass = RPClass(fake)
    assert klass.getName() == "Widget"

def test_class_add_superclass():
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    klass = RPClass(fake)
    klass.addSuperclass(RPClass(base))
    fake.addSuperclass.assert_called_once_with(base)

def test_class_get_is_abstract():
    fake = make_fake_element("Class", getIsAbstract=1)
    klass = RPClass(fake)
    assert klass.getIsAbstract() is True
"""
    # klasses.getName, klass.addSuperclass, klass.getIsAbstract renamed
    # fake.addSuperclass, make_fake_element kwargs, fake.mock assertions preserved
    test_expected = """def test_class_get_name():
    fake = make_fake_element("Class", getName="Widget")
    klass = RPClass(fake)
    assert klass.get_name() == "Widget"

def test_class_add_superclass():
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    klass = RPClass(fake)
    klass.add_superclass(RPClass(base))
    fake.addSuperclass.assert_called_once_with(base)

def test_class_get_is_abstract():
    fake = make_fake_element("Class", getIsAbstract=1)
    klass = RPClass(fake)
    assert klass.get_is_abstract() is True
"""
    source = tmp_path / "test_class.py"
    source.write_text(test_input)
    test_mapping = {**MAPPING, "addSuperclass": "add_superclass", "getIsAbstract": "get_is_abstract"}
    changes = apply_rename(source, test_mapping, category="test")
    assert source.read_text() == test_expected
    assert len(changes) == 3


def test_dry_run_does_not_modify(tmp_path: Path):
    source = tmp_path / "model.py"
    source.write_text(MODEL_INPUT)
    original = source.read_text()
    changes = apply_rename(source, MAPPING, category="model", dry_run=True)
    assert source.read_text() == original
    assert len(changes) == 4
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
pytest tests/unit/scripts/test_rename_engine.py -v
```
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
# scripts/rename_engine.py
import tokenize
import io
from pathlib import Path
from typing import Dict, List, Tuple, Set


Change = Tuple[int, str, str]  # (line_number, old_name, new_name)


# Method names on mock objects — must never be renamed
_MOCK_PREFIXES: Set[str] = {
    "assert_called_once_with", "assert_called_with",
    "assert_has_calls", "assert_not_called", "assert_called_once",
    "return_value", "side_effect",
}

_KEYWORD_FUNC = "make_fake_element"
_FAKE_VAR_PREFIX = "fake"


def _find_colon_before(tokens, idx):
    """Walk backward from idx to find the nearest OP ':' token at same indent level."""
    for i in range(idx - 1, -1, -1):
        t = tokens[i]
        if t.type == tokenize.OP and t.string == ":":
            for j in range(i + 1, idx):
                inner = tokens[j]
                if inner.type == tokenize.NAME and inner.string in ("def", "class"):
                    return i
                if inner.type == tokenize.OP and inner.string in ("{", ";"):
                    return None
            return i
    return None


def _is_def_name(tokens, idx):
    """Check if the NAME token at idx is a function definition name (after 'def')."""
    for i in range(idx - 1, -1, -1):
        t = tokens[i]
        if t.type == tokenize.NAME and t.string == "def":
            return True
        if t.type not in (tokenize.NAME, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT) and not (t.type == tokenize.OP and t.string == "@"):
            break
    return False


def _is_attribute_receiver(tokens, idx):
    """Check if the NAME token at idx is an attribute access (after '.').

    Walk backwards from idx looking for '.' at start of the same logical line.
    """
    for i in range(idx - 1, -1, -1):
        t = tokens[i]
        if t.type == tokenize.OP:
            if t.string == ".":
                return True
            elif t.string in ("(", "[", "{", ":", "=", ",", "@"):
                return False
        elif t.type in (tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT):
            continue
        elif t.type == tokenize.NAME and t.string in ("import", "from", "class", "def", "return", "raise", "yield", "if", "elif", "else", "for", "while", "with", "try", "except", "finally"):
            return False
        elif t.type == tokenize.NAME and t.string == "self" and i > 0 and tokens[i-1].type == tokenize.OP and tokens[i-1].string == ".":
            return True
        else:
            return False
    return False


def _get_receiver_name(tokens, idx):
    """Get the receiver expression for an attribute access at idx.

    Walk back from the '.' just before the attribute name and collect
    the receiver tokens.
    """
    dot_idx = None
    for i in range(idx - 1, -1, -1):
        if tokens[i].type == tokenize.OP and tokens[i].string == ".":
            dot_idx = i
            break
    if dot_idx is None:
        return ""
    # Collect tokens from the start of the receiver expression
    parts = []
    for i in range(dot_idx - 1, -1, -1):
        t = tokens[i]
        if t.type in (tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT):
            break
        if t.type == tokenize.OP and t.string in (".", "(", ")", "[", "]", ",", ":", "=", "+", "-", "*", "/"):
            break
        parts.append(t.string)
    return "".join(reversed(parts)).strip()


def _is_fake_receiver(tokens, idx):
    """Check if the receiver of an attribute access is a 'fake' variable."""
    receiver = _get_receiver_name(tokens, idx)
    if not receiver:
        return False
    # Check exact match or prefix match for dotted access
    parts = receiver.split(".")
    first = parts[0]
    return first == _FAKE_VAR_PREFIX or first.startswith(_FAKE_VAR_PREFIX + "_")


def _token_is_keyword_arg(tokens, idx, func_name=_KEYWORD_FUNC):
    """Check if the NAME token at idx is a keyword argument name in make_fake_element call.

    Walk backward to find if we're inside the argument list of make_fake_element(...).
    """
    # Walk backward to find an opening paren, then check if the function before it
    # is make_fake_element
    depth = 0
    found_call = False
    fname = None
    for i in range(idx - 1, -1, -1):
        t = tokens[i]
        if t.type == tokenize.OP:
            if t.string == ")":
                depth += 1
            elif t.string == "(":
                depth -= 1
                if depth < 0:
                    # Found the opening paren of this call
                    # Look for the function name before it
                    for j in range(i - 1, -1, -1):
                        pt = tokens[j]
                        if pt.type == tokenize.NAME:
                            fname = pt.string
                            break
                        if pt.type in (tokenize.NEWLINE, tokenize.NL, tokenize.INDENT):
                            continue
                        break
                    break
    return fname == func_name


def _is_mock_method(tokens, idx):
    """Check if this name is a mock assertion method call that should NOT be renamed.

    Pattern: fake.addSuperclass.assert_called_once_with(...)
    The name after '.' when the preceding attribute chain ends with assert_called_once_with etc.
    """
    receiver = _get_receiver_name(tokens, idx)
    if not receiver:
        return False
    # Check if any part of the chain contains _MOCK_PREFIXES
    parts = receiver.split(".")
    for part in parts:
        if part in _MOCK_PREFIXES:
            return True
    return False


def apply_rename(
    file_path: Path,
    mapping: Dict[str, str],
    category: str = "model",
    dry_run: bool = False,
) -> List[Change]:
    source = file_path.read_text(encoding="utf-8")
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))

    changes: List[Change] = []
    new_tokens = []

    for tok in tokens:
        start_line = tok.start[0]
        tok_text = tok.string

        if tok.type == tokenize.NAME and tok_text in mapping:
            should_rename = False

            if category == "model":
                # Only rename def names and non-_com attribute calls
                if _is_def_name(tokens, tokens.index(tok)):
                    should_rename = True
                elif _is_attribute_receiver(tokens, tokens.index(tok)):
                    receiver = _get_receiver_name(tokens, tokens.index(tok))
                    if "_com" not in receiver:
                        should_rename = True

            elif category == "action":
                if _is_attribute_receiver(tokens, tokens.index(tok)):
                    should_rename = True

            elif category == "test":
                if _is_def_name(tokens, tokens.index(tok)):
                    should_rename = False  # shouldn't happen in tests
                elif _is_attribute_receiver(tokens, tokens.index(tok)):
                    if not _is_fake_receiver(tokens, tokens.index(tok)):
                        if not _is_mock_method(tokens, tokens.index(tok)):
                            should_rename = True
                elif _token_is_keyword_arg(tokens, tokens.index(tok)):
                    should_rename = False

            if should_rename:
                old_name = tok_text
                new_name = mapping[old_name]
                changes.append((start_line, old_name, new_name))
                new_tokens.append(tok._replace(string=new_name))
                continue

        new_tokens.append(tok)

    if not dry_run and changes:
        new_source = tokenize.untokenize(new_tokens)
        file_path.write_text(new_source, encoding="utf-8")

    return changes
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
pytest tests/unit/scripts/test_rename_engine.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/rename_engine.py tests/unit/scripts/test_rename_engine.py
git commit -m "feat: add token-based rename engine"
```

---

### Task 4: Main script CLI

**Files:**
- Create: `scripts/rename_to_snake_case.py`

**Interfaces:**
- Consumes: `extract_mapping(...)` from Task 2, `apply_rename(...)` from Task 3
- Produces: CLI script with `--dry-run`, `--no-backup`, `--source-dirs` arguments

- [ ] **Step 1: Write the script**

```python
# scripts/rename_to_snake_case.py
#!/usr/bin/env python3
"""Rename all camelCase method names to snake_case across the rhapsody-cli codebase.

Usage:
    python scripts/rename_to_snake_case.py [--dry-run] [--no-backup]

Phases:
    1. Scan model/application source to build old→new name mapping
    2. Apply renames to model/application files (rename defs + non-COM calls)
    3. Apply renames to action/CLI files (rename all wrapper call sites)
    4. Apply renames to test files (preserve COM mocks + fake variables)
    5. Print summary of changes
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List

# Add scripts dir to path for sibling imports
_SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(_SCRIPTS_DIR))

from extract_mapping import extract_mapping
from rename_engine import apply_rename, Change


# Source directories to scan for method definitions
MODEL_DIRS = [
    Path("src/rhapsody_cli/models"),
    Path("src/rhapsody_cli/application.py"),
]

# Directories to rename (call sites)
CATEGORY_DIRS: Dict[str, List[Path]] = {
    "model": [Path("src/rhapsody_cli/models"), Path("src/rhapsody_cli/application.py")],
    "action": [Path("src/rhapsody_cli/actions"), Path("src/rhapsody_cli/commands"), Path("src/rhapsody_cli/cli")],
    "test":   [Path("tests")],
}


def _backup_file(file_path: Path) -> None:
    bak = file_path.with_suffix(".py.bak")
    shutil.copy2(file_path, bak)


def _print_changes(changes: List[Change], label: str):
    print(f"\n{label}:")
    for line, old, new in sorted(changes, key=lambda c: c[0]):
        print(f"  {line:>5}: {old} -> {new}")
    print(f"  Total: {len(changes)} changes")


def main():
    parser = argparse.ArgumentParser(description="Rename camelCase methods to snake_case")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    parser.add_argument("--no-backup", action="store_true", help="Skip .bak file creation")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent

    # Phase 1: Build mapping (extract_mapping accepts both dirs and files)
    print("Phase 1: Extracting method mapping...")
    source_paths = [
        project_root / "src" / "rhapsody_cli" / "models",
        project_root / "src" / "rhapsody_cli" / "application.py",
    ]
    mapping_path = project_root / "scripts" / "_method_mapping.json"
    mapping = extract_mapping(source_paths, output_json=(None if args.dry_run else mapping_path))

    print(f"  Found {len(mapping)} methods to rename: {json.dumps(mapping, indent=2)}")

    if not mapping:
        print("  No methods to rename. Exiting.")
        return

    # Phase 2-4: Apply renames per category
    all_changes: List[Change] = []
    for category, dirs in CATEGORY_DIRS.items():
        for dir_path in dirs:
            full_path = project_root / dir_path
            if not full_path.exists():
                continue
            if full_path.is_file():
                files = [full_path]
            else:
                files = sorted(full_path.rglob("*.py"))

            for py_file in files:
                if py_file.name.startswith("__"):
                    continue
                if "_method_mapping" in py_file.name:
                    continue

                if not args.dry_run and not args.no_backup:
                    _backup_file(py_file)

                changes = apply_rename(py_file, mapping, category=category, dry_run=args.dry_run)
                if changes:
                    all_changes.extend(changes)

    # Phase 5: Summary
    total_files = len(set(c[0] for c in all_changes))
    _print_changes(all_changes, "Summary")
    print(f"\nFiles affected: {total_files}")

    if args.dry_run:
        print("\nDry-run complete. Run without --dry-run to apply changes.")
    else:
        print("\nRename complete. Run quality gates to verify.")
        print("  ruff check src/ tests/")
        print("  black --check src/ tests/")
        print("  pytest tests/unit")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify script runs**

Run:
```bash
python scripts/rename_to_snake_case.py --dry-run
```
Expected: Output shows Phase 1 extracting mapping, lists methods to rename, and shows changes in each file category.

- [ ] **Step 3: Commit**

```bash
git add scripts/rename_to_snake_case.py
git commit -m "feat: add rename CLI script wiring extractor + engine"
```

---

### Task 5: Non-code updates (Phase 3)

**Files:**
- Modify: `AGENTS.md`
- Modify: `src/rhapsody_cli/models/core.py` (lines 83-87)
- No script needed — manual edits

- [ ] **Step 1: Update AGENTS.md**

Replace line 17:
```markdown
Method names mirror `com.telelogic.rhapsody.core` Java API exactly.
```
with:
```markdown
Method names use snake_case (e.g. `get_name`, `set_name`, `add_class`).
Internal COM calls preserve the camelCase API (`self._com.methodName(...)`).
```

- [ ] **Step 2: Update `core.py` docstring**

In `src/rhapsody_cli/models/core.py`, change lines 83-87:
```python
    Method names mirror the Rhapsody Java API exactly (``getName``,
    ``setName``, ``getMetaClass``, ``getGUID``, ...). Some Rhapsody COM Prog
    IDs expose these as bare properties instead of methods; see
    :func:`_get_method_or_property`.
```
to:
```python
    Method names use snake_case (``get_name``, ``set_name``,
    ``get_meta_class``, ``get_guid``, ...). Internal COM calls preserve
    the camelCase API (``self._com.methodName(...)``). Some Rhapsody COM
    Prog IDs expose these as bare properties instead of methods; see
    :func:`_get_method_or_property`.
```

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md src/rhapsody_cli/models/core.py
git commit -m "docs: update convention docs to reflect snake_case rename"
```

---

### Task 6: Execute the rename and verify

- [ ] **Step 1: Run the script in production mode**

```bash
python scripts/rename_to_snake_case.py
```
Expected: Output lists all renamed methods with line numbers and total file count.

- [ ] **Step 2: Update checklist comments and `:meth:` references (missed by script)**

The rename script skips comments and docstrings. Stale camelCase names remain in:
1. `# [x] addSuperclass  [x] impl ...` checklists at top of each wrapper class
2. `:meth:`addSuperclass\`` cross-references in docstrings

Replace them programmatically using the mapping file:

```bash
python -c "
import json, glob
mapping = json.load(open('scripts/_method_mapping.json'))
for f in sorted(glob.glob('src/rhapsody_cli/models/**/*.py', recursive=True)):
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    changed = False
    for old, new in sorted(mapping.items(), key=lambda x: -len(x[0])):
        content = content.replace(f'# [x] {old}', f'# [x] {new}')
        content = content.replace(f':meth:\`{old}\`', f':meth:\`{new}\`')
        changed = changed or content != open(f, encoding='utf-8').read()
    if changed:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'Updated: {f}')
"
```

- [ ] **Step 3: Run quality gates**

```bash
ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit
```

- [ ] **Step 4: Fix any issues**

If ruff reports issues (`F811` redefinitions, unused imports, etc.), fix them manually.
If black reports formatting issues, run `black src/ tests/` to auto-fix.
If pytest fails, inspect failures and fix (likely a missed COM-AST rename in tests).

- [ ] **Step 5: Clean up backup files**

```bash
find src/ tests/ -name "*.bak" -delete
```

- [ ] **Step 6: Final review — inspect diff**

```bash
git diff --stat
```
Expected: Shows ~60-80 files changed.
Manually spot-check a model file, an action file, and a test file.

- [ ] **Step 7: Commit all changes**

```bash
git add -A
git commit -m "refactor: rename all camelCase wrapper methods to snake_case"
```
