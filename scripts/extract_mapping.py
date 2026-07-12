import ast
import json
from pathlib import Path
from typing import Dict, List, Optional

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


def extract_mapping(
    source_paths: List[Path], output_json: Optional[Path] = None
) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for path in _collect_files(source_paths):
        try:
            _scan_file(path, mapping)
        except SyntaxError:
            continue
    if output_json:
        output_json.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    return mapping
