# Snake-Case Unification Design

## Summary

Unify the dual-convention codebase to use snake_case everywhere, replacing all
camelCase methods on COM wrapper classes and caller sites while preserving COM
API method names in internal implementation calls.

## Motivation

The codebase currently uses a deliberate dual convention: camelCase on COM
wrapper public methods (to mirror `com.telelogic.rhapsody.core` Java API),
snake_case everywhere else. This design describes a clean break transition to
unified snake_case, eliminating the mental context switch for contributors.

## Scope

### Files renamed

| Layer | Files | What changes |
|-------|-------|-------------|
| Models | `src/rhapsody_cli/models/**/*.py` (~20 files) | Method definitions and internal cross-calls |
| Application | `src/rhapsody_cli/application.py` | Method definitions and internal cross-calls |
| Actions | `src/rhapsody_cli/actions/*.py` (8 files) | All call sites on wrapper objects |
| CLI utilities | `src/rhapsody_cli/cli/*.py` | All call sites on wrapper objects |
| Tests | `tests/unit/**/test_*.py` (~40 files) | Call sites on wrapper objects (not COM mocks) |
| Config/docs | `AGENTS.md`, docstrings, comments | References to renamed methods |

### NOT renamed (preserved as-is)

- `self._com.methodName(...)` — COM API calls, stays camelCase
- `make_fake_element(keyword=...)` — keyword args simulate COM properties
- `fake.methodName(...)` in tests — COM mock calls
- String args to `_get_method_or_property(self._com, "methodName", "propName")` — COM identifiers
- String args to `_set_method_or_property(self._com, "setMethod", "prop", value)` — COM identifiers
- `_method_or_property(com_obj, "methodName", "propName")` — same
- Private helpers (`call_com`, `_get_method_or_property`, `_set_method_or_property`, `wrap`, `register_wrapper`, `_wrap_if_element`) — already snake_case
- `RPCollection`, `RPModelElement`, class names — PascalCase, not affected

## Method: AST-Based Rename Script

A single-purpose Python script (`scripts/rename_to_snake_case.py`) that performs
the rename in phases.

### Phase 1: Extract Method Mapping

Scan `src/rhapsody_cli/models/` and `src/rhapsody_cli/application.py` with the
`ast` module. For every `FunctionDef` at class level whose name contains
uppercase letters (i.e., is camelCase), convert to snake_case and record in a
JSON mapping: `{"getName": "get_name", "setName": "set_name", ...}`.

#### CamelCase-to-snake_case algorithm

Insert underscore before each uppercase letter that:
- Follows a lowercase letter or digit (`getName` → `get_name`)
- Precedes a lowercase letter and isn't first (`getGUID` → `get_guid`)

Then lowercase the entire string. This correctly handles:
- `getOSLCLinks` → `get_oslc_links`
- `getIsAbstract` → `get_is_abstract`
- `getPropertyValueConditionalExplicit` → `get_property_value_conditional_explicit`
- `getNestedElementsByMetaClass` → `get_nested_elements_by_meta_class`

### Phase 2: Apply Renames using Token-Based Replacement

AST is used only for **detection** (Phase 1). All source modification is
done with the `tokenize` module, which preserves whitespace, comments,
docstrings, and formatting exactly.

For each file in scope:

1. Read the source lines
2. Tokenize the file with `tokenize.generate_tokens()`
3. For each `NAME` token:
   - If it matches a method name in the mapping:
     - **Model/application files**: check context — is this a `def` keyword
       followed by the name? Is the receiver `self._com`/`_com`?
     - **Action/CLI files**: check context — is this an attribute access
       (`.methodName(`)?
     - **Test files**: check context — is the receiver `fake` or a
       `make_fake_element` keyword?
4. Replace only the token text when the context matches; skip otherwise
5. Write the modified tokens back to source

Token-based replacement keeps every comment, docstring, blank line, and
formatting choice intact. Only the identifier tokens that match the mapping
are changed.

### Phase 3: Non-Code Updates

- **AGENTS.md**: Replace references to camelCase convention with snake_case
  convention text. Update method name examples.
- **Docstrings**: Update `:meth:` cross-references. Keep `Reference:` lines
  (Java API references) unchanged.
- **Checklist comments**: Update method names in the `# [x] ...` checklists at
  the top of each wrapper class.
- **Line 84-87 in `core.py`**: Update the docstring that explicitly documents
  the camelCase convention.

### Phase 4: Verification

```bash
ruff check src/ tests/         # catch any missed renames or syntax errors
black --check src/ tests/       # formatting
mypy src/ tests/               # type-checking
pytest tests/unit              # all unit tests pass
```

Any test failures indicate missed call sites or incorrectly renamed COM calls.
Fix and re-run.

## Edge Cases

### Method names that aren't getX/setX

Some wrapper methods don't follow the get/set prefix:
- `errorMessage()` → `error_message()`
- `addClass()`, `addSuperclass()`, `deleteFromProject()` etc. → `add_class()`, `add_superclass()`, `delete_from_project()`

These are handled identically by the same camelCase→snake_case algorithm.

### `_get_method_or_property` string arguments remain camelCase

```python
# Before:
def getName(self):
    return str(AbstractRPModelElement._get_method_or_property(self._com, "getName", "name"))

# After:
def get_name(self):
    return str(AbstractRPModelElement._get_method_or_property(self._com, "getName", "name"))
```

The strings `"getName"` and `"name"` are COM property names — NOT renamed.

### `make_fake_element` keyword arguments

```python
# Before (stays unchanged):
fake = make_fake_element("Class", getName="Widget")
```

These simulate COM properties on the fake object. The fake's `getName` attribute
is a COM-mock method name, not a Python wrapper method. NOT renamed.

### Mock assertions on fake objects

```python
# Before (stays unchanged):
fake.addClass.assert_called_once_with("Inner")
```

`fake.addClass` is a COM mock attribute — stays camelCase. The `assert_*` call
is on a mock object, not a wrapper.

### Consecutive uppercase (acronyms)

- `getGUID` → `get_guid`
- `getOSLCLinks` → `get_oslc_links`
- `getRmmUrl` → `get_rmm_url`
- `getTi` → `get_ti`
- `setTi` → `set_ti`
- `getBinaryID` → `get_binary_id`

### Cross-wrapper calls within models

When a model method calls another wrapper's method (e.g., via a return value):

```python
# Before:
def addConstructor(self, ...):
    return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addConstructor(...)))
#          ^^ COM call, stays camelCase        ^^ COM call, stays camelCase
```

No cross-wrapper calls exist in the current codebase — all model methods
delegate directly to COM via `self._com.methodName(...)` and return wrapped
results. The `wrap()` call is already snake_case.

## Naming Convention: Before vs After

| Context | Before | After |
|---------|--------|-------|
| Wrapper methods | `getName()`, `setIsAbstract()` | `get_name()`, `set_is_abstract()` |
| COM calls | `self._com.getName()` | `self._com.getName()` (unchanged) |
| Action calls | `cls.getName()`, `container.getMetaClass()` | `cls.get_name()`, `container.get_meta_class()` |
| Test wrapper calls | `klass.getName()`, `result.getIsAbstract()` | `klass.get_name()`, `result.get_is_abstract()` |
| Test COM mock calls | `fake.getName()`, `fake.setIsAbstract()` | unchanged |
| AGENTS.md convention | "camelCase to mirror Java API" | "snake_case, unified" |
| `core.py` docstring | "Method names mirror Java API exactly" | "Method names use snake_case" |

## Risk Mitigation

1. **Dry-run mode**: The script supports `--dry-run` to preview all changes
   without modifying files.
2. **Per-file backup**: The script creates `.bak` copies before modifying each
   file (unless `--no-backup` is specified).
3. **Incremental verification**: After the script runs, `pytest` serves as the
   regression gate. Any missed rename causes a test failure (method not found).
4. **Manual review gate**: The script outputs a diff report. All changes are
   reviewed file-by-file before committing.

## Out of Scope

- Renaming COM API calls (`self._com.*`) — impossible, COM interface is camelCase
- Renaming class names (`RPClass`, `RPPackage`) — PascalCase is Python convention
- Renaming private helpers (`call_com`, `wrap`) — already snake_case
- Renaming CLI argument names (`--path`, `--guid`) — kebab-case is argparse convention
- Renaming test fixture functions — already snake_case

## Timeline Estimate

| Step | Effort |
|------|--------|
| Write rename script | ~1 session |
| Dry-run + review | ~15 min |
| Apply renames | script runs in <1s |
| Fix any issues | ~1 session max |
| Run quality gates | automated |
| **Total** | **2-3 sessions** |
