from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

LAYER_NAMES = ["MSP", "MSC", "MBC", "IGSOA", "DFVM", "SATP"]
FILE_EXTENSIONS = {".md", ".json5"}
CONTRADICTION_KEYS = {
    "xi_outside_dfvm": "xi or ξ located outside DFVM context",
    "observer_primacy": "observer primacy or observer-driven measurement references",
    "superluminal_or_time_reversal": "superluminal transport or time reversal allowance",
}

CONTEXT_WIDTH = 1  # lines of padding shown around a hit


def iter_files(root: Path) -> List[Path]:
    paths: List[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in FILE_EXTENSIONS and ".git" not in path.parts:
            paths.append(path)
    return paths


def scan_layers(files: List[Path]):
    layer_hits: Dict[str, List[Tuple[Path, int, str]]] = {k: [] for k in LAYER_NAMES}
    contradictions: Dict[str, List[Tuple[Path, int, str]]] = {k: [] for k in CONTRADICTION_KEYS}

    xi_pattern = re.compile(r"(\\xi|ξ)")
    observer_pattern = re.compile(r"observer.*(primacy|dependent|driven)", re.IGNORECASE)
    superluminal_pattern = re.compile(r"superluminal|time[- ]reversal", re.IGNORECASE)

    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        lines = text.splitlines()
        for idx, line in enumerate(lines, start=1):
            for layer in LAYER_NAMES:
                if re.search(rf"\b{layer}\b", line):
                    layer_hits[layer].append((file_path, idx, line.strip()))

            if xi_pattern.search(line) and "DFVM" not in line:
                contradictions["xi_outside_dfvm"].append((file_path, idx, line.strip()))

            if observer_pattern.search(line):
                contradictions["observer_primacy"].append((file_path, idx, line.strip()))

            if superluminal_pattern.search(line):
                contradictions["superluminal_or_time_reversal"].append(
                    (file_path, idx, line.strip())
                )

    return layer_hits, contradictions


def bucketize(entries: List[Tuple[Path, int, str]], keywords: Set[str]) -> List[str]:
    results: List[str] = []
    seen: Set[str] = set()
    for path, line_no, text in entries:
        if any(word.lower() in text.lower() for word in keywords):
            key = f"{path}:{line_no}:{text}"
            if key not in seen:
                seen.add(key)
                results.append(f"{path}:{line_no}: {text}")
    return results


def summarize_layer(entries: List[Tuple[Path, int, str]]):
    definitions = bucketize(entries, {"define", "definition", "layer", "canonical"})
    math_objs = bucketize(entries, {"field", "functional", "operator", "$", "PDE", "equation", "functional"})
    constraints = bucketize(entries, {"must", "forbidden", "no ", "only", "bounded", "ban", "without", "prohibit"})
    return definitions, math_objs, constraints


def primary_entry(entries: List[str]) -> str | None:
    if not entries:
        return None
    return entries[0]


def trim_list(entries: List[str], limit: int = 5) -> List[str]:
    return entries[:limit]


def write_report(layer_hits, contradictions, output_path: Path):
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    lines: List[str] = ["# Ontological Consistency Report", "", f"Generated: {timestamp}", ""]

    for layer in LAYER_NAMES:
        definitions, math_objs, constraints = summarize_layer(layer_hits[layer])
        canonical_def = primary_entry(definitions)
        lines.append(f"## {layer}")
        lines.append("")
        lines.append("- Canonical definition:")
        lines.append(f"  - {canonical_def}" if canonical_def else "  - None detected")

        extra_defs = trim_list(definitions[1:])
        lines.append("- Additional definition references:")
        if extra_defs:
            lines.extend([f"  - {item}" for item in extra_defs])
        else:
            lines.append("  - None detected")

        math_trimmed = trim_list(math_objs)
        lines.append("- Mathematical objects:")
        if math_trimmed:
            lines.extend([f"  - {item}" for item in math_trimmed])
        else:
            lines.append("  - None detected")

        constraint_trimmed = trim_list(constraints)
        lines.append("- Constraints:")
        if constraint_trimmed:
            lines.extend([f"  - {item}" for item in constraint_trimmed])
        else:
            lines.append("  - None detected")

        lines.append(f"- Total occurrences scanned: {len(layer_hits[layer])}")
        lines.append("")

    lines.append("## Detected Contradictions")
    lines.append("")
    for key, label in CONTRADICTION_KEYS.items():
        lines.append(f"- {label}:")
        hits = contradictions[key]
        if hits:
            for path, line_no, text in hits:
                lines.append(f"  - {path}:{line_no}: {text}")
        else:
            lines.append("  - None detected")
    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    files = iter_files(Path("."))
    layer_hits, contradictions = scan_layers(files)
    write_report(layer_hits, contradictions, Path("reports/ontological_consistency_report.md"))


if __name__ == "__main__":
    main()
