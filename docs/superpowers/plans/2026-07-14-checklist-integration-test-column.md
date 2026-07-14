# Integration Test Checklist Column Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an "integration test status" (`integration test`) checkbox field to every per-class method-parity checklist comment in `src/rhapsody_cli/models/**/*.py`, alongside the renamed unit-test field (`unit test`), so integration test coverage can be tracked in-source per method.

**Architecture:** A one-off Python transform script walks all `model_*.py` files (plus `core.py`), applies a scoped regex substitution to each checklist row (`[.] test` → `[.] unit test  [ ] integration test`), and writes files back in place. No behavioral code changes — comments only.

**Tech Stack:** Python (stdlib `re`, `pathlib`), existing repo quality gate (`ruff`, `black`, `mypy`, `pytest`).

## Global Constraints

- Only comment lines change — zero behavioral/code changes.
- Every one of the 1,458 existing checklist rows across 40 files must gain the new field; none may be skipped or double-transformed.
- New `integration test` checkbox always starts unchecked (`[ ]`), regardless of existing integration test coverage.
- Existing trailing notes (e.g. `(already implemented)`, `(inherited from RPModelElement)`, `(NotImplementedError)`) must be preserved unchanged after the new field.
- Repo quality gate must still pass after the change: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`.
- Do not touch `docs/superpowers/plans/2026-07-13-integration-tests.md` or `2026-07-14-model-class-integration-tests.md` — out of scope for this pass.
- Follow repo branch convention (`feature/`, `fix/`, `refactor/`, `docs/`) — no direct commits to `main`.

---

### Task 1: Write and run the transform script

**Files:**
- Create (temporary, not committed): `C:\Users\uie54187\AppData\Local\Temp\opencode\add_its_checklist_field.py`
- Modifies (in place): all files matching `src/rhapsody_cli/models/**/*.py` that contain checklist rows (40 files, including `src/rhapsody_cli/models/core.py`)

**Interfaces:**
- Consumes: nothing external — pure text transform.
- Produces: every checklist row of the form
  `# [x|  ] <method_name>  [x|  ] impl  [x|  ] docstring  [x|  ] test   (optional note)`
  becomes
  `# [x|  ] <method_name>  [x|  ] impl  [x|  ] docstring  [x|  ] unit test  [ ] integration test   (optional note)`
  Regex used: `(\[[ x]\])(\s+)test\b` matched only on lines that also contain the literal substring `docstring`, replaced with `\1\2unit test  [ ] integration test`.

- [ ] **Step 1: Write the script**

```python
# add_its_checklist_field.py
import re
from pathlib import Path

ROOT = Path(r"E:\Working\rhapsody-cli\src\rhapsody_cli\models")

# Only touch lines that are checklist rows: they contain "docstring" as a
# field label. Renames the trailing "test" field to "unit test" and appends a new
# unchecked "integration test" (integration test status) field right after it.
PATTERN = re.compile(r"(\[[ x]\])(\s+)test\b")

changed_files = 0
changed_lines = 0

for path in ROOT.rglob("*.py"):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    new_lines = []
    file_changed = False
    for line in lines:
        if "docstring" in line and PATTERN.search(line):
            new_line = PATTERN.sub(r"\1\2unit test  [ ] integration test", line, count=1)
            if new_line != line:
                changed_lines += 1
                file_changed = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    if file_changed:
        path.write_text("".join(new_lines), encoding="utf-8")
        changed_files += 1

print(f"Files changed: {changed_files}")
print(f"Lines changed: {changed_lines}")
```

- [ ] **Step 2: Run the script**

Run: `python "C:\Users\uie54187\AppData\Local\Temp\opencode\add_its_checklist_field.py"`
Expected output:
```
Files changed: 40
Lines changed: 1458
```

- [ ] **Step 3: Verify no rows were missed and none double-transformed**

Run:
```bash
grep -rE '\[.\] +test\b' src/rhapsody_cli/models --include=*.py | wc -l
```
Expected: `0` (no leftover unrenamed `test` fields)

Run:
```bash
grep -rE '\[ \] integration test' src/rhapsody_cli/models --include=*.py | wc -l
```
Expected: `1458`

- [ ] **Step 4: Spot-check formatting on representative files**

Run: `git diff src/rhapsody_cli/models/core.py src/rhapsody_cli/models/elements/classifiers/model_class.py src/rhapsody_cli/models/elements/containment/model_package.py src/rhapsody_cli/models/support/model_ide.py`

Confirm:
- `core.py`: rows for `RPModelElement`, `RPUnit`, `RPCollection` all show `unit test` + `[ ] integration test`
- `model_class.py`: all-`[x]` rows now show `[x] unit test  [ ] integration test`
- `model_package.py`: mixed `[x]`/`[ ]` rows preserved correctly, only `test`→`unit test`+`integration test` changed
- `model_ide.py`: the 10 anomaly rows with `impl (inherited from RPModelElement)` still transform correctly (note text between `impl` and `docstring` untouched, `test` at end still renamed)

---

### Task 2: Run the quality gate and fix any fallout

**Files:**
- None created/modified beyond Task 1 (this task only runs checks; fix forward if something breaks).

**Interfaces:**
- Consumes: transformed files from Task 1.
- Produces: a clean quality-gate pass, ready to commit.

- [ ] **Step 1: Run the full quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

Expected: all four commands exit 0 (comment-only changes should not affect linting, formatting, typing, or test behavior).

- [ ] **Step 2: If `black --check` fails**

This should not happen since changes are inside `#` comments (black does not reformat comments), but if any line now exceeds the configured `line-length = 200`, wrap the note text or shorten spacing manually in that specific line, then re-run Step 1.

- [ ] **Step 3: If `pytest tests/unit` fails**

This would indicate the script accidentally altered code outside a comment. Use `git diff` to locate the offending line, revert just that line, and re-run the verification greps from Task 1 Step 3.

---

### Task 3: Commit the change

**Files:**
- All 40 modified files under `src/rhapsody_cli/models/`.

**Interfaces:**
- Consumes: verified, gate-passing changes from Task 2.
- Produces: a single commit on a `docs/` or `refactor/` branch (comment-only, non-behavioral).

- [ ] **Step 1: Create branch**

```bash
git checkout -b docs/checklist-integration-test-column
```

- [ ] **Step 2: Stage and commit**

```bash
git add src/rhapsody_cli/models
git commit -m "docs: add integration test status column to method parity checklists"
```

- [ ] **Step 3: Confirm commit contents**

Run: `git show --stat HEAD`
Expected: 40 files changed, only `model_*.py`/`core.py` under `src/rhapsody_cli/models/`, no test or non-comment code changes.

- [ ] **Step 4: Delete the temporary script**

```bash
rm "C:\Users\uie54187\AppData\Local\Temp\opencode\add_its_checklist_field.py"
```

(Not committed — lived only in the temp scratch directory.)
</content>
