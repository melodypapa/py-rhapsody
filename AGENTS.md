# AGENTS.md

## Project

Pythonic wrapper around the IBM Rhapsody COM API. All method names use snake_case (e.g. `get_name`, `set_name`, `add_class`). Internal COM calls preserve the camelCase API (`self._com.methodName(...)`). Windows-only for runtime (COM); tests run anywhere via fakes.

## Architecture (3 layers, bottom-up)

| Layer | Path | Purpose |
|-------|------|---------|
| Models | `src/rhapsody_cli/models/` | COM wrappers for 50+ element types. `elements/` has 13 domain subpackages (`classifiers/`, `containment/`, `relations/`, etc.). `support/` wraps codegen/IDE/file APIs. |
| Application | `src/rhapsody_cli/application.py` | `RhapsodyApplication` — attach/launch/connect to Rhapsody. Prog ID: `Rhapsody2.Application.1`. |
| CLI | `src/rhapsody_cli/cli/` + `commands/` + `actions/` | argparse (stdlib), "PanGu style": `AbstractCommand` → `AbstractAction`. Dispatch: `main()` → `AbstractCommand.execute()` → `AbstractAction.execute()`. |

## COM Wrapping Rules (critical)

- All COM calls → `call_com(lambda: self._com.methodName(...))` (translates `com_error` → `RhapsodyRuntimeException`)
- No-arg getters → `_get_method_or_property(self._com, "getX", "x")` (prefers method, falls back to property; note: strings are COM identifiers, not Python names)
- Parameterized getters → MUST use `call_com` directly (`_get_method_or_property` drops extra args)
- Single-arg setters → `_set_method_or_property(self._com, "setX", "x", value)`
- Multi-arg setters → MUST use `call_com` directly
- Return wrapped element → `AbstractRPModelElement.wrap(...)` or specific wrapper constructor
- Return collection → `RPCollection(self.call_com(...))`

## Testing

```bash
pip install -e ".[dev,cli]"   # full setup (CLI tests need tabulate/rich)
pytest tests/unit/             # unit tests only — what CI runs (1505 tests collected)
pytest -k "test_foo"           # pattern match
```

- All unit tests use fakes from `tests/unit/models/fakes.py` (`make_fake_element`, `make_fake_collection`). **Never real COM in tests.**
- `tests/integration/` (live Rhapsody instance) and `tests/system/` (end-to-end subprocess) require Windows + Rhapsody — auto-skip in CI, not run by default `pytest`.

## TDD Requirement

Write failing test first, then implement. Coverage target 80% min, 90%+ preferred.

## Quality Gate

```bash
ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit
```

- ruff: E, F, I, UP, B, N rule sets. Black: line-length 200, py38 target.
- `win32com.*` / `pywintypes`: `ignore_missing_imports` in mypy config.
- CI runs `mypy` only on Python < 3.10 (pattern-matching syntax issue in pytest on 3.10+ blocks the type-checked code path).
- CI runs full gate on `windows-latest` across Python 3.8–3.13. Codecov upload.

## Forbidden

- `from __future__ import annotations` (use string-quoted forward refs or `TYPE_CHECKING` imports instead)
- `element._com.delete()` (use `element.delete_from_project()` instead)
- `Co-authored-by: Copilot` or any AI attribution
- Direct commits to `main` — always use `feature/`, `fix/`, `refactor/`, `docs/` branches

## Adding a New Element Wrapper

**Read `docs/java_api` html files first** — it documents every java model classes detail information. before you start to write the wrapper and integration tests.

1. Create `src/rhapsody_cli/models/elements/<subpackage>/model_<class>.py`
2. Subclass `RPModelElement`, add methods using snake_case names mirroring Java API
3. `AbstractRPModelElement.register_wrapper("MetaClass", RPMyClass)` at module level
4. Add import in the subpackage's `__init__.py`
5. Write tests using `make_fake_element` / `make_fake_collection` (use `docs/java_api.md` to find the exact Java method names to mock)

## Adding a CLI Subcommand

1. Create action class inheriting `AbstractAction` (or `RhapsodyContextAction`)
2. Implement `init_arguments(sub_parser)` and `execute(args)`
3. Register action in the command group's `get_actions()` method
