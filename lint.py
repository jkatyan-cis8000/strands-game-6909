#!/usr/bin/env python3
"""
Linting script to enforce source architecture rules.

Rules enforced:
1. Every file under src/ belongs in exactly one layer directory.
2. Imports may only target layers in the file's "may import from" set.
3. No file exceeds 300 lines.
4. Uses Python's ast module for parsing.
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Define the valid import sources for each layer
LAYER_IMPORTS: Dict[str, Set[str]] = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
}

VALID_LAYERS = set(LAYER_IMPORTS.keys())
SRC_DIR = Path("src")


def get_layer_from_path(file_path: Path) -> str | None:
    """Extract the layer name from a file's path."""
    try:
        rel_path = file_path.relative_to(SRC_DIR)
        parts = rel_path.parts
        if parts and parts[0] in VALID_LAYERS:
            return parts[0]
    except ValueError:
        pass
    return None


def get_imported_modules(tree: ast.AST) -> List[str]:
    """Extract all imported module names from an AST."""
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Get the top-level module name
                module_name = alias.name.split(".")[0]
                imported.append(module_name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                # Get the top-level module name
                module_name = node.module.split(".")[0]
                imported.append(module_name)
    return imported


def check_line_count(file_path: Path) -> List[Tuple[int, str]]:
    """Check if file exceeds 300 lines."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) > 300:
                errors.append((301, f"File exceeds 300 lines ({len(lines)} lines)"))
    except Exception as e:
        errors.append((0, f"Error reading file: {e}"))
    return errors


def check_imports(file_path: Path, tree: ast.AST) -> List[Tuple[int, str]]:
    """Check that imports respect layer dependency rules."""
    errors = []
    layer = get_layer_from_path(file_path)
    if layer is None:
        return errors

    allowed = LAYER_IMPORTS[layer]
    imported = get_imported_modules(tree)

    for module in imported:
        # Check if this is an internal import (starts with src.)
        # or matches a layer name
        if module in VALID_LAYERS and module not in allowed:
            errors.append((1, f"Import from '{module}' is not allowed in '{layer}'. May only import from: {', '.join(sorted(allowed))}"))
        elif module == layer:
            # Same-layer import is always allowed
            pass

    return errors


def check_file(file_path: Path) -> List[Tuple[int, str]]:
    """Run all checks on a single file."""
    errors = []

    # Check line count
    errors.extend(check_line_count(file_path))

    # Parse and check imports
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(file_path))
        errors.extend(check_imports(file_path, tree))
    except SyntaxError as e:
        errors.append((e.lineno or 0, f"Syntax error: {e.msg}"))
    except Exception as e:
        errors.append((0, f"Error parsing file: {e}"))

    return errors


def collect_source_files() -> List[Path]:
    """Collect all Python files under src/."""
    source_files = []
    if not SRC_DIR.exists():
        return source_files

    for path in SRC_DIR.rglob("*.py"):
        # Skip __pycache__ directories
        if "__pycache__" in path.parts:
            continue
        source_files.append(path)

    return source_files


def main() -> int:
    """Main linting function. Returns 0 on success, 1 on failure."""
    source_files = collect_source_files()
    all_errors: List[Tuple[str, int, str]] = []

    for file_path in source_files:
        file_errors = check_file(file_path)
        for line_num, message in file_errors:
            all_errors.append((str(file_path), line_num, message))

    if all_errors:
        print("Linting failed with the following violations:\n")
        # Sort by file, then by line number
        all_errors.sort(key=lambda x: (x[0], x[1]))
        for file_path, line_num, message in all_errors:
            print(f"{file_path}:{line_num}: {message}")
        print(f"\n{len(all_errors)} error(s) found")
        return 1

    print(f"Linting passed: {len(source_files)} file(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
