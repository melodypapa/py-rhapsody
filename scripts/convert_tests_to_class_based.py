"""Convert test_RP* functions to class-based pytest tests."""

import re
import sys
from pathlib import Path


def parse_blocks(lines):
    """Parse file lines into blocks: ('code', lines) or ('function', lines)."""
    blocks = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("def "):
            func_lines = [lines[i]]
            i += 1
            while i < len(lines) and (
                lines[i].startswith(" ") or lines[i].strip() == ""
            ):
                func_lines.append(lines[i])
                i += 1
            blocks.append(("function", func_lines))
        else:
            code_lines = []
            while i < len(lines) and not lines[i].startswith("def "):
                code_lines.append(lines[i])
                i += 1
            blocks.append(("code", code_lines))
    return blocks


def classname_from_funcname(func_name):
    """Extract class name from test_RPClassName_method."""
    m = re.match(r"test_(RP\w+?)_", func_name)
    return m.group(1) if m else None


def method_name_from_funcname(func_name):
    """Extract method name from test_RPClassName_method -> test_method."""
    m = re.match(r"test_RP\w+?_(.+)", func_name)
    return f"test_{m.group(1)}" if m else func_name


def convert_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    blocks = parse_blocks(lines)

    # Group consecutive function blocks by class name
    new_blocks = []
    i = 0
    while i < len(blocks):
        btype, blines = blocks[i]
        if btype != "function":
            new_blocks.append((btype, blines))
            i += 1
            continue

        func_name_match = re.match(r"def (\w+)", blines[0])
        if not func_name_match:
            new_blocks.append((btype, blines))
            i += 1
            continue

        func_name = func_name_match.group(1)
        class_name = classname_from_funcname(func_name)
        if not class_name:
            new_blocks.append((btype, blines))
            i += 1
            continue

        # Collect all consecutive functions with the same class name
        class_funcs = []
        while i < len(blocks):
            btype2, blines2 = blocks[i]
            if btype2 != "function":
                break
            fn_match = re.match(r"def (\w+)", blines2[0])
            if not fn_match or classname_from_funcname(fn_match.group(1)) != class_name:
                break
            class_funcs.append(blines2)
            i += 1

        # Generate class block
        class_lines = [f"class Test{class_name}:"]
        for idx, fn_lines in enumerate(class_funcs):
            # Convert def line: remove RPClassName_ prefix, add self
            orig_def = fn_lines[0]
            fn_name_match = re.match(r"def (\w+)", orig_def)
            meth_name = method_name_from_funcname(fn_name_match.group(1))
            new_def = re.sub(
                r"def \w+",
                f"def {meth_name}",
                orig_def.replace("():", "(self):"),
            )
            fn_lines[0] = f"    {new_def}"

            # Indent body
            for j in range(1, len(fn_lines)):
                line = fn_lines[j]
                if line.strip() == "":
                    fn_lines[j] = ""
                else:
                    fn_lines[j] = f"    {line}"

            # Remove trailing blanks
            while fn_lines and fn_lines[-1].strip() == "":
                fn_lines.pop()

            if idx > 0:
                class_lines.append("")
            class_lines.extend(fn_lines)

        new_blocks.append(("class", class_lines))

    # Reconstruct file
    out_lines = []
    for btype, blines in new_blocks:
        if btype == "function":
            out_lines.extend(blines)
        elif btype == "code":
            out_lines.extend(blines)
        elif btype == "class":
            if blines:
                if out_lines and out_lines[-1].strip() != "":
                    out_lines.append("")
                out_lines.extend(blines)
                out_lines.append("")

    # Remove trailing whitespace
    while out_lines and out_lines[-1].strip() == "":
        out_lines.pop()

    with open(filepath, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(out_lines))
        f.write("\n")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"Converting {path}...")
        convert_file(path)
        print(f"  Done.")
