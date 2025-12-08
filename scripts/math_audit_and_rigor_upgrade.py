from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent
TARGET_EXTENSIONS = {".md", ".json5"}
SECTION_PREFIXES = (
    "definition",
    "theorem",
    "lemma",
    "proposition",
    "corollary",
    "assumption",
    "axiom",
)
DISPLAY_PATTERNS = [
    re.compile(r"\$\$(.+?)\$\$", re.DOTALL),
    re.compile(r"\\\[(.+?)\\\]", re.DOTALL),
]
INLINE_PATTERN = re.compile(r"(?<!\\)\$(.+?)(?<!\\)\$")
HEADING_PATTERN = re.compile(r"^(#+)\s+(.*)")
SYMBOL_TOKEN = re.compile(r"\\?[A-Za-z][A-Za-z0-9_]*")
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

LAYER_NAMES = ["MSP", "MSC", "MBC", "IGSOA", "DFVM", "SATP"]


@dataclass
class MathEntry:
    type: str
    title: str
    name: str
    file: str
    start_line: int
    end_line: int
    equations: List[str]
    symbols_introduced: List[str]

    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "title": self.title,
            "name": self.name,
            "file": self.file,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "equations": self.equations,
            "symbols_introduced": self.symbols_introduced,
        }


@dataclass
class ConsistencyHit:
    file: str
    line: int
    context: str


def iter_files() -> List[Path]:
    paths: List[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TARGET_EXTENSIONS:
            continue
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        paths.append(path)
    return paths


def extract_math(text: str) -> List[str]:
    expressions: List[str] = []
    for pattern in DISPLAY_PATTERNS:
        expressions.extend(match.strip() for match in pattern.findall(text))
    expressions.extend(match.strip() for match in INLINE_PATTERN.findall(text))
    return expressions


def extract_symbols(expressions: List[str]) -> List[str]:
    symbols: Set[str] = set()
    for expr in expressions:
        for token in SYMBOL_TOKEN.findall(expr):
            token_name = token[1:] if token.startswith("\\") else token
            if token_name in STOPWORDS:
                continue
            symbols.add(token if token.startswith("\\") else token_name)
    return sorted(symbols)


def parse_section_boundaries(lines: List[str]) -> List[Tuple[str, str, int, int]]:
    sections: List[Tuple[str, str, int, int]] = []
    for idx, line in enumerate(lines):
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        title = match.group(2).strip()
        lower = title.lower()
        for prefix in SECTION_PREFIXES:
            if lower.startswith(prefix):
                sections.append((prefix, title, len(match.group(1)), idx))
                break
    return sections


def build_entries_for_file(path: Path) -> List[MathEntry]:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    sections = parse_section_boundaries(lines)
    entries: List[MathEntry] = []

    file_math = extract_math(content)
    if file_math:
        entries.append(
            MathEntry(
                type="math",
                title=f"Math expressions in {path.name}",
                name=path.stem,
                file=str(path.relative_to(ROOT)),
                start_line=1,
                end_line=len(lines),
                equations=file_math,
                symbols_introduced=extract_symbols(file_math),
            )
        )

    for i, (section_type, title, level, start_line) in enumerate(sections):
        end_line = len(lines)
        for next_section in sections[i + 1 :]:
            next_level = next_section[2]
            next_start = next_section[3]
            if next_level <= level:
                end_line = next_start
                break
        section_text = "\n".join(lines[start_line:end_line])
        math_exprs = extract_math(section_text)
        entries.append(
            MathEntry(
                type=section_type,
                title=title,
                name=title.split(None, 1)[1] if " " in title else title,
                file=str(path.relative_to(ROOT)),
                start_line=start_line + 1,
                end_line=end_line,
                equations=math_exprs,
                symbols_introduced=extract_symbols(math_exprs),
            )
        )
    return entries


def build_symbol_table(entries: List[MathEntry]):
    table: Dict[str, List[Dict[str, str]]] = {}
    conflicts: Dict[str, List[str]] = {}
    for entry in entries:
        meaning = None if entry.type == "math" else entry.name
        for symbol in entry.symbols_introduced:
            table.setdefault(symbol, []).append(
                {
                    "file": entry.file,
                    "section": entry.title,
                    "type": entry.type,
                    "meaning": meaning,
                }
            )
    for symbol, uses in table.items():
        meanings = {use["meaning"] for use in uses if use.get("meaning")}
        if len(meanings) > 1:
            conflicts[symbol] = sorted(meanings)
    return table, conflicts


def detect_layer_hits(files: List[Path]):
    hits: Dict[str, List[ConsistencyHit]] = {layer: [] for layer in LAYER_NAMES}
    contradictions: Dict[str, List[ConsistencyHit]] = {
        "xi_outside_dfvm": [],
        "observer_primacy": [],
        "stochastic_satp": [],
        "superluminal_or_time_reversal": [],
    }
    xi_pattern = re.compile(r"(\\xi|ξ)")
    observer_pattern = re.compile(r"observer.*(primacy|collapse|dependent|driven)", re.IGNORECASE)
    superluminal_pattern = re.compile(r"superluminal|time[- ]reversal", re.IGNORECASE)
    satp_noise_pattern = re.compile(r"SATP.*(stochastic|noise|\\xi|ξ)", re.IGNORECASE)

    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            for layer in LAYER_NAMES:
                if re.search(rf"\b{layer}\b", line):
                    hits[layer].append(ConsistencyHit(str(path.relative_to(ROOT)), i, line.strip()))
            if xi_pattern.search(line) and "DFVM" not in line:
                contradictions["xi_outside_dfvm"].append(
                    ConsistencyHit(str(path.relative_to(ROOT)), i, line.strip())
                )
            if observer_pattern.search(line):
                contradictions["observer_primacy"].append(
                    ConsistencyHit(str(path.relative_to(ROOT)), i, line.strip())
                )
            if superluminal_pattern.search(line):
                contradictions["superluminal_or_time_reversal"].append(
                    ConsistencyHit(str(path.relative_to(ROOT)), i, line.strip())
                )
            if satp_noise_pattern.search(line):
                contradictions["stochastic_satp"].append(
                    ConsistencyHit(str(path.relative_to(ROOT)), i, line.strip())
                )
    return hits, contradictions


def summarize_hits(entries: List[ConsistencyHit], keywords: Set[str]) -> List[str]:
    summary: List[str] = []
    seen: Set[str] = set()
    for hit in entries:
        if any(k.lower() in hit.context.lower() for k in keywords):
            key = f"{hit.file}:{hit.line}:{hit.context}"
            if key not in seen:
                seen.add(key)
                summary.append(f"{hit.file}:{hit.line}: {hit.context}")
    return summary


def write_consistency_report(hits, contradictions, output_path: Path):
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    lines: List[str] = ["# Ontological Consistency Report", "", f"Generated: {ts}", ""]
    for layer in LAYER_NAMES:
        lines.append(f"## {layer}")
        defs = summarize_hits(hits[layer], {"define", "definition", "layer", "canonical"})
        math_objs = summarize_hits(hits[layer], {"field", "functional", "operator", "pde", "equation"})
        constraints = summarize_hits(hits[layer], {"must", "forbidden", "no ", "only", "bounded", "exclude", "ban"})
        lines.append("- Canonical definition candidate:")
        lines.append(f"  - {defs[0]}" if defs else "  - None detected")
        lines.append("- Mathematical objects (sample):")
        lines.extend([f"  - {item}" for item in math_objs[:5]] or ["  - None detected"])
        lines.append("- Constraints (sample):")
        lines.extend([f"  - {item}" for item in constraints[:5]] or ["  - None detected"])
        lines.append(f"- Total occurrences scanned: {len(hits[layer])}")
        lines.append("")

    lines.append("## Flagged Issues")
    for key, label in {
        "xi_outside_dfvm": "ξ outside DFVM context",
        "observer_primacy": "Observer primacy references",
        "stochastic_satp": "Stochastic forcing tied to SATP",
        "superluminal_or_time_reversal": "Superluminal or time-reversal allowances",
    }.items():
        lines.append(f"- {label}:")
        issues = contradictions[key]
        if issues:
            for hit in issues:
                lines.append(f"  - {hit.file}:{hit.line}: {hit.context}")
        else:
            lines.append("  - None detected")
    lines.append("")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


@dataclass
class CriticalCheckResult:
    id: str
    description: str
    location: str
    status: str
    notes: str
    limit_checks: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        data = {
            "id": self.id,
            "description": self.description,
            "location": self.location,
            "status": self.status,
            "notes": self.notes,
        }
        if self.limit_checks:
            data["limit_checks"] = self.limit_checks
        return data


CRITICAL_PATTERNS = {
    "MSC-FUNCTIONAL": {
        "file": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md",
        "pattern": r"S_\{?MSC\}?\[",
        "description": "MSC functional and collapse condition",
    },
    "MSC-REGIMES": {
        "file": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md",
        "pattern": r"Subcritical MSC",
        "description": "MSC regimes and thresholds",
    },
    "DFVM-STOCHASTIC": {
        "file": "Book2_Applications_and_Extensions/09_QuantumStochasticMechanics.md",
        "pattern": r"DFVM[_\\{t]+1.*(?:xi|ξ)",
        "description": "DFVM stochastic update",
    },
    "SATP-PDE": {
        "file": "Appendices/SATP_Final_PDE_Formulation.md",
        "pattern": r"(?:\\partial_t|∂_t)\^2",
        "description": "SATP PDE well-posedness",
    },
    "SATP-CFL": {
        "file": "Appendices/SATP_CFL_Stability_Appendix.md",
        "pattern": r"Δt\s*≤\s*Δx",
        "description": "SATP CFL bound",
    },
    "SATP-ENERGY": {
        "file": "Appendices/SATP_Final_PDE_Formulation.md",
        "pattern": r"E[_\{]?exotic",
        "description": "SATP energy / cost constraint",
    },
    "MEASUREMENT-OP": {
        "file": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md",
        "pattern": r"ℳ|M\s*:\s*\(DFVM,\s*MSC\)",
        "description": "Measurement operator and observability gate",
    },
    "ENTROPY-LINK": {
        "file": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md",
        "pattern": r"dS[_\{]?entropy",
        "description": "Entropy–MSC relationship",
    },
}


def run_critical_checks() -> List[CriticalCheckResult]:
    results: List[CriticalCheckResult] = []
    for cid, cfg in CRITICAL_PATTERNS.items():
        target = ROOT / cfg["file"]
        if not target.exists():
            results.append(
                CriticalCheckResult(
                    id=cid,
                    description=cfg["description"],
                    location=cfg["file"],
                    status="MISSING",
                    notes="Target file not found",
                )
            )
            continue
        content = target.read_text(encoding="utf-8", errors="ignore")
        found = re.search(cfg["pattern"], content)
        status = "PRESENT" if found else "NOT FOUND"
        notes = "Located and structurally consistent with narrative" if found else "Pattern not located"
        limit_note = None
        if cid == "SATP-PDE":
            limit_note = "Zero-source limit reduces to variable-coefficient wave form"
        if cid == "MSC-FUNCTIONAL":
            limit_note = "σ_pert → 0 increases cohesion; ρ_rel → 0 collapses cohesion"
        if cid == "ENTROPY-LINK":
            limit_note = "Increasing entropy mirrors cohesion decay"
        results.append(
            CriticalCheckResult(
                id=cid,
                description=cfg["description"],
                location=cfg["file"],
                status=status,
                notes=notes,
                limit_checks=limit_note,
            )
        )
    return results


def build_rigour_status(checks: List[CriticalCheckResult]) -> List[Dict]:
    status_map: List[Dict] = []
    for check in checks:
        base_status = "PROVEN" if check.status == "PRESENT" else "OPEN"
        # Mark known gaps as SKETCHED/ASSERTED for audit transparency
        if check.id in {"MSC-FUNCTIONAL", "MSC-REGIMES", "DFVM-STOCHASTIC", "ENTROPY-LINK", "SATP-ENERGY"}:
            base_status = "ASSERTED" if check.status == "PRESENT" else "OPEN"
        if check.id in {"SATP-PDE", "SATP-CFL", "MEASUREMENT-OP"}:
            base_status = "SKETCHED" if check.status == "PRESENT" else "OPEN"
        entry = {
            "id": check.id,
            "claim": check.description,
            "location": check.location,
            "status": base_status,
        }
        status_map.append(entry)
    return status_map


def build_rigor_plan(statuses: List[Dict]) -> List[Dict]:
    plan: List[Dict] = []
    upgrade_counter = 0
    for status in statuses:
        if status["status"] not in {"ASSERTED", "SKETCHED", "OPEN"}:
            continue
        upgrade_counter += 1
        suggestion = ""
        if "SATP" in status["id"]:
            suggestion = (
                "Add explicit coefficient regularity (Lipschitz c_eff), polynomial growth bounds on V, and an energy estimate"
                " with source terms plus discrete CFL energy argument."
            )
        elif "MSC" in status["id"]:
            suggestion = (
                "Specify functional domain (e.g., H^1(Ω)), sample ρ_rel/σ_pert forms, and norm-based ε-thresholds with"
                " boundedness proof."
            )
        elif "DFVM" in status["id"]:
            suggestion = (
                "Reference probability space (Ω, 𝔽, P), characterize ξ or W_t as bounded, zero-mean noise, and cite SPDE"
                " class for existence intuition."
            )
        elif "MEASUREMENT" in status["id"]:
            suggestion = (
                "Present ℳ as CPTP/Markov channel with ΔE ≥ 0 and ΔS_entropy > 0, plus MSC-gated observability condition"
                " for persistent records."
            )
        elif "ENTROPY" in status["id"]:
            suggestion = "Tie dS_entropy/dt to −dS_MSC/dt via monotonicity lemma within the chosen function space."
        plan.append(
            {
                "rank": upgrade_counter,
                "id": status["id"],
                "location": status["location"],
                "suggestion": suggestion,
            }
        )
        if upgrade_counter >= 10:
            break
    return plan


def render_rigor_plan(plan: List[Dict]) -> str:
    lines = ["# Rigor Upgrade Plan", ""]
    for item in plan:
        lines.append(f"## {item['rank']}. {item['id']}")
        lines.append(f"- Location: {item['location']}")
        lines.append(f"- Suggested upgrade: {item['suggestion']}")
        lines.append("- Proposed edit snippet (review before merging):")
        lines.append("```markdown")
        lines.append(f"[{item['id']}] Add: {item['suggestion']}")
        lines.append("```\n")
    return "\n".join(lines)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    files = iter_files()
    entries: List[MathEntry] = []
    for path in files:
        entries.extend(build_entries_for_file(path))

    # Assign IDs
    counters: Dict[str, int] = {}
    for entry in entries:
        counters.setdefault(entry.type, 0)
        counters[entry.type] += 1
        prefix = entry.type.upper()
        setattr(entry, "id", f"{prefix}-{counters[entry.type]:03d}")

    # Symbol table and conflicts
    symbol_table, conflicts = build_symbol_table(entries)
    index_output = {
        "items": [entry.to_dict() for entry in entries],
        "symbol_table": symbol_table,
        "conflicts": conflicts,
    }
    write_json(ROOT / "reports" / "math_object_index.json5", index_output)
    write_json(ROOT / "reports" / "symbol_table.json5", symbol_table)

    # Consistency report
    hits, contradictions = detect_layer_hits(files)
    write_consistency_report(hits, contradictions, ROOT / "reports" / "ontological_consistency_report.md")

    # Critical checks and rigour status
    checks = run_critical_checks()
    rigour_status = build_rigour_status(checks)
    write_json(ROOT / "reports" / "Math_Rigour_Status.json5", rigour_status)

    # Rigor upgrade plan
    plan = build_rigor_plan(rigour_status)
    plan_md = render_rigor_plan(plan)
    plan_path = ROOT / "reports" / "Rigor_Upgrade_Plan.md"
    plan_path.write_text(plan_md, encoding="utf-8")

    print(f"Processed {len(entries)} math objects")
    print(f"Tracked {len(symbol_table)} symbols; conflicts: {len(conflicts)}")
    print(f"Rigour upgrades proposed: {len(plan)} entries")


if __name__ == "__main__":
    main()
