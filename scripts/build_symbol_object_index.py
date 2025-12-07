import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
TARGET_EXTENSIONS = {".md", ".json5"}
SECTION_TYPES: Dict[str, str] = {
    "definition": "DEF",
    "theorem": "THM",
    "lemma": "LEM",
    "proposition": "PROP",
    "corollary": "COR",
    "assumption": "ASSUMP",
    "axiom": "AXIOM",
}

# Basic set of latex/control tokens to ignore when parsing symbols
STOPWORDS = {
    "frac",
    "left",
    "right",
    "begin",
    "end",
    "mathrm",
    "text",
    "cdot",
    "mathbf",
    "mathbb",
    "mathcal",
    "partial",
    "nabla",
    "int",
    "sum",
    "prod",
    "infty",
    "forall",
    "exists",
    "neq",
    "leq",
    "geq",
    "approx",
    "equiv",
}

MATH_DISPLAY_PATTERNS = [
    re.compile(r"\$\$(.+?)\$\$", re.DOTALL),
    re.compile(r"\\\[(.+?)\\\]", re.DOTALL),
]
MATH_INLINE_PATTERN = re.compile(r"(?<!\\)\$(.+?)(?<!\\)\$")

HEADING_PATTERN = re.compile(r"^(#+)\s+(.*)")


def extract_math(text: str) -> List[str]:
    expressions: List[str] = []
    for pattern in MATH_DISPLAY_PATTERNS:
        expressions.extend(match.strip() for match in pattern.findall(text))
    expressions.extend(match.strip() for match in MATH_INLINE_PATTERN.findall(text))
    return expressions


def extract_symbols_from_math(expressions: List[str]) -> List[str]:
    symbols: List[str] = []
    token_pattern = re.compile(r"\\?[A-Za-z][A-Za-z0-9_]*")
    for expr in expressions:
        for token in token_pattern.findall(expr):
            if token.startswith("\\"):
                token_name = token[1:]
            else:
                token_name = token
            if token_name in STOPWORDS:
                continue
            symbols.append(token if token.startswith("\\") else token_name)
    return sorted(set(symbols))


def parse_sections(lines: List[str]) -> List[Tuple[str, str, int, int]]:
    sections: List[Tuple[str, str, int, int]] = []
    for idx, line in enumerate(lines):
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip()
        lowered = title.lower()
        for section_type in SECTION_TYPES:
            if lowered.startswith(section_type):
                sections.append((section_type, title, level, idx))
                break
    return sections


def build_items_for_file(path: Path) -> List[Dict]:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    sections = parse_sections(lines)
    items: List[Dict] = []

    # File-wide math capture
    file_math = extract_math(content)
    if file_math:
        items.append(
            {
                "type": "math",
                "title": f"Math expressions in {path.name}",
                "name": path.stem,
                "file": str(path.relative_to(ROOT)),
                "start_line": 1,
                "end_line": len(lines),
                "equations": file_math,
                "symbols_introduced": extract_symbols_from_math(file_math),
            }
        )

    if not sections:
        return items

    for i, (section_type, title, level, start_line) in enumerate(sections):
        end_line = len(lines)
        for next_section in sections[i + 1:]:
            next_level = next_section[2]
            next_start = next_section[3]
            if next_level <= level:
                end_line = next_start
                break
        section_text = "\n".join(lines[start_line:end_line])
        math_exprs = extract_math(section_text)
        symbols = extract_symbols_from_math(math_exprs)
        name = title.split(None, 1)[1] if " " in title else title
        items.append(
            {
                "type": section_type,
                "title": title,
                "name": name,
                "file": str(path.relative_to(ROOT)),
                "start_line": start_line + 1,
                "end_line": end_line,
                "equations": math_exprs,
                "symbols_introduced": symbols,
            }
        )
    return items


def build_symbol_table(items: List[Dict]) -> Tuple[Dict[str, List[Dict]], Dict[str, List[str]]]:
    table: Dict[str, List[Dict]] = {}
    conflicts: Dict[str, List[str]] = {}
    for entry in items:
        meaning = None if entry.get("type") == "math" else entry.get("name", entry.get("title"))
        for symbol in entry.get("symbols_introduced", []):
            table.setdefault(symbol, []).append(
                {
                    "file": entry["file"],
                    "section": entry["title"],
                    "type": entry["type"],
                    "meaning": meaning,
                }
            )
    for symbol, uses in table.items():
        meanings = {use.get("meaning") for use in uses if use.get("meaning")}
        if len(meanings) > 1:
            conflicts[symbol] = sorted(meanings)
    return table, conflicts


def main() -> None:
    items: List[Dict] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TARGET_EXTENSIONS:
            continue
        # Skip hidden directories or files inside build artifacts
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        items.extend(build_items_for_file(path))

    # Assign stable IDs
    counters: Dict[str, int] = defaultdict(int)
    for entry in items:
        t = entry["type"]
        counters[t] += 1
        prefix = SECTION_TYPES.get(t, t.upper())
        entry["id"] = f"{prefix}-{counters[t]:03d}"

    symbol_table, conflicts = build_symbol_table(items)

    output = {
        "items": items,
        "symbol_table": symbol_table,
        "conflicts": conflicts,
    }

    output_path = ROOT / "reports" / "symbol_object_index.json5"
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} entries to {output_path}")
    print(f"Tracked {len(symbol_table)} unique symbols; conflicts: {len(conflicts)}")


if __name__ == "__main__":
    main()
