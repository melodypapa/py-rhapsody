import tokenize
import io
from pathlib import Path
from typing import Dict, List, Tuple


Change = Tuple[int, str, str]


def _is_def_name(tokens, idx):
    for i in range(idx - 1, -1, -1):
        t = tokens[i]
        if t.type == tokenize.NAME and t.string == "def":
            return True
        if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT):
            return False
    return False


def _first_receiver_name(tokens, idx):
    dot_idx = None
    for i in range(idx - 1, -1, -1):
        t = tokens[i]
        if t.type == tokenize.OP and t.string == ".":
            dot_idx = i
            break
        if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT):
            return None
    if dot_idx is None:
        return None
    for i in range(dot_idx - 1, -1, -1):
        t = tokens[i]
        if t.type == tokenize.NAME:
            return t.string
        if t.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT):
            continue
        if t.type == tokenize.OP and t.string == ".":
            continue
        return None
    return None


def _receiver_contains_com(tokens, idx):
    for i in range(idx - 1, -1, -1):
        t = tokens[i]
        if t.type == tokenize.NAME and t.string == "_com":
            return True
        if t.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT):
            continue
        if t.type == tokenize.OP and t.string == ".":
            continue
        if t.type == tokenize.NAME:
            continue
        return False
    return False


def _is_fake_receiver(tokens, idx):
    first = _first_receiver_name(tokens, idx)
    if first is None:
        return False
    return first == "fake" or first.startswith("fake_")


def _is_keyword_arg(tokens, idx):
    for i in range(idx + 1, len(tokens)):
        t = tokens[i]
        if t.type in (tokenize.NL, tokenize.ENDMARKER):
            continue
        return t.type == tokenize.OP and t.string == "="
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

    for idx, tok in enumerate(tokens):
        tok_text = tok.string
        if tok.type == tokenize.NAME and tok_text in mapping:
            should_rename = False

            if category == "model":
                if _is_def_name(tokens, idx):
                    should_rename = True
                elif _first_receiver_name(tokens, idx) is not None:
                    if not _receiver_contains_com(tokens, idx):
                        should_rename = True

            elif category == "action":
                if _first_receiver_name(tokens, idx) is not None:
                    should_rename = True

            elif category == "test":
                if _first_receiver_name(tokens, idx) is not None:
                    if not _is_fake_receiver(tokens, idx):
                        should_rename = True
                elif _is_keyword_arg(tokens, idx):
                    should_rename = False

            if should_rename:
                old_name = tok_text
                new_name = mapping[old_name]
                changes.append((tok.start[0], old_name, new_name))
                new_tokens.append(tok._replace(string=new_name))
                continue

        new_tokens.append(tok)

    if not dry_run and changes:
        new_source = tokenize.untokenize(new_tokens)
        file_path.write_text(new_source, encoding="utf-8")

    return changes
