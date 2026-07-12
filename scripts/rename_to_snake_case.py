#!/usr/bin/env python3
import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List

_SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(_SCRIPTS_DIR))

from extract_mapping import extract_mapping
from rename_engine import apply_rename, Change


CATEGORY_DIRS: Dict[str, List[Path]] = {
    "model": [Path("src/rhapsody_cli/models"), Path("src/rhapsody_cli/application.py")],
    "action": [Path("src/rhapsody_cli/actions"), Path("src/rhapsody_cli/commands"), Path("src/rhapsody_cli/cli")],
    "test": [Path("tests")],
}


def _backup_file(file_path: Path) -> None:
    bak = file_path.with_suffix(".py.bak")
    shutil.copy2(file_path, bak)


def _print_changes(changes: List[Change], label: str):
    print(f"\n{label}:")
    changed_lines = {}
    for line, old, new in changes:
        changed_lines.setdefault(line, []).append((old, new))
    for line in sorted(changed_lines):
        pairs = ", ".join(f"{o}->{n}" for o, n in changed_lines[line])
        print(f"  L{line:>5}: {pairs}")
    print(f"  Total: {len(changes)} changes")


def main():
    parser = argparse.ArgumentParser(description="Rename camelCase methods to snake_case across rhapsody-cli")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    parser.add_argument("--no-backup", action="store_true", help="Skip .bak file creation")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent

    # Phase 1: Build mapping
    print("Phase 1: Extracting method mapping...")
    source_paths = [
        project_root / "src" / "rhapsody_cli" / "models",
        project_root / "src" / "rhapsody_cli" / "application.py",
    ]
    mapping_path = project_root / "scripts" / "_method_mapping.json"
    mapping = extract_mapping(source_paths, output_json=(None if args.dry_run else mapping_path))

    print(f"  Found {len(mapping)} methods to rename:")
    for old, new in sorted(mapping.items()):
        print(f"    {old} -> {new}")

    if not mapping:
        print("  No methods to rename. Exiting.")
        return

    # Phase 2-4: Apply renames
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

    # Summary
    total_files = len(set(c[0] for c in all_changes))
    _print_changes(all_changes, "Changes by line")
    print(f"\nFiles affected: {total_files}")

    if args.dry_run:
        print("\nDry-run complete. Run without --dry-run to apply changes.")
    else:
        print("\nRename complete. Run quality gates to verify:")
        print("  ruff check src/ tests/")
        print("  black --check src/ tests/")
        print("  pytest tests/unit")


if __name__ == "__main__":
    main()
