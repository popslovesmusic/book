from __future__ import annotations

import datetime
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class EquationItem:
    label: str
    pattern: str
    expectation: str


@dataclass
class EquationBlock:
    id: str
    name: str
    file: Path
    section: str
    equations: List[EquationItem]
    structural_checks: List[str] = field(default_factory=list)


<<<<<<< ours
<<<<<<< ours
=======
=======
>>>>>>> theirs
@dataclass
class LimitCheck:
    id: str
    title: str
    assumption: str
    result: str
    interpretation: str


<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
CRITICAL_BLOCKS: List[EquationBlock] = [
    EquationBlock(
        id="MSC-FUNC",
        name="MSC Functional and Collapse",
        file=Path("Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md"),
        section="A.1 Formal Definition of MSC",
        equations=[
            EquationItem(
                label="MSC functional mapping",
                pattern=r"MSC\[\s*\\Psi\s*\]\s*:\s*\\mathcal\{R\}\(\s*\\Psi\s*\)\s*\\rightarrow\s*\\mathbb\{R\}\^\+",
                expectation="Functional from relational configuration to non-negative scalar.",
            ),
            EquationItem(
                label="MSC stability functional",
                pattern=r"S_\{MSC\}\[\s*\\Psi\s*\]\s*=\s*\\int\s*\(\\rho_\{rel\}\(\\Psi\)\s*-\s*\\sigma_\{pert\}\(\\Psi\)\)\s*\\,?\s*dV",
                expectation="Integral of relational density minus perturbation stress yields scalar cohesion measure.",
            ),
            EquationItem(
                label="Collapse condition",
                pattern=r"S_\{MSC\}\s*\\to\s*0\s*\\Rightarrow",
                expectation="Vanishing cohesion drives identity collapse.",
            ),
        ],
        structural_checks=[
            "Type alignment: MSC[Ψ] and S_MSC[Ψ] both yield scalars; integrand terms are densities with matching volume measure.",
            "Inequalities over S_MSC in regimes compare scalar thresholds (ε1, ε2) of same dimension.",
        ],
    ),
    EquationBlock(
        id="MSC-REGIMES",
        name="MSC Regimes",
        file=Path("Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md"),
        section="A.2 Three Canonical Regimes of MSC",
        equations=[
            EquationItem(
                label="Subcritical bound",
                pattern=r"S_\{MSC\}\s*<\s*\\varepsilon_1",
                expectation="Scalar cohesion below lower threshold.",
            ),
            EquationItem(
                label="Critical band",
                pattern=r"\\varepsilon_1\s*\\leq\s*S_\{MSC\}\s*\\leq\s*\\varepsilon_2",
                expectation="Scalar cohesion between thresholds.",
            ),
            EquationItem(
                label="Supercritical bound",
                pattern=r"S_\{MSC\}\s*>\s*\\varepsilon_2",
                expectation="Scalar cohesion above stability threshold.",
            ),
        ],
        structural_checks=[
            "Threshold comparisons are scalar-to-scalar; stability and memory behaviors attach to the same cohesion metric.",
        ],
    ),
    EquationBlock(
        id="DFVM-RANDOMNESS",
        name="DFVM Stochastic Update",
        file=Path("Book2_Applications_and_Extensions/09_QuantumStochasticMechanics.md"),
        section="9.7 Canonical Ontological Placement of Randomness",
        equations=[
            EquationItem(
                label="DFVM stochastic map",
                pattern=r"DFVM_\{t\+1\}\s*=\s*F\(DFVM_t,\s*MSC\)\s*\+\s*\\xi\(x,t\)",
                expectation="Next DFVM state equals deterministic update plus bounded stochastic perturbation.",
            ),
        ],
        structural_checks=[
            "Both sides describe DFVM-state fields on the same domain; ξ shares DFVM units and is mediated through DFVM only.",
            "Stochastic term is additive modulation, not direct MSC mutation, preserving type consistency.",
        ],
    ),
    EquationBlock(
        id="SATP-PDE",
        name="SATP PDE and Bounds",
        file=Path("Appendices/SATP_Final_PDE_Formulation.md"),
        section="Well-Posedness Conditions",
        equations=[
            EquationItem(
                label="SATP hyperbolic PDE",
                pattern=r"\\partial_t\^2\s*\\phi\s*-\s*c_\{eff\}\^2\(x,t\)\s*\\nabla\^2\s*\\phi\s*\+\s*V'\(\\phi\)\s*=\s*J_\{SATP\}",
                expectation="Hyperbolic field equation with source J_SATP.",
            ),
            EquationItem(
                label="Gradient bound",
                pattern=r"\|\\nabla\s*\\phi\|\s*<\s*G_\{max\}",
                expectation="Spatial gradient magnitude bounded.",
            ),
            EquationItem(
                label="Time-derivative bound",
                pattern=r"\|\\partial_t\s*\\phi\|\s*<\s*T_\{max\}",
                expectation="Temporal rate bounded.",
            ),
            EquationItem(
                label="CFL bound",
                pattern=r"\\Delta\s*t\s*\\leq\s*\\frac\{\\Delta\s*x\}\{\\max\(c_\{eff\}\)\}",
                expectation="Discrete stability gate tying Δt and Δx via c_eff.",
            ),
            EquationItem(
                label="Energy / cost constraint",
                pattern=r"E_\{exotic\}\s*\\geq\s*\\int\s*\|\\nabla\s*\\phi\|\^2\s*dV",
                expectation="Exotic energy lower bounded by gradient norm integral.",
            ),
        ],
        structural_checks=[
            "PDE classification: second-order time derivative plus Laplacian → quasi-linear hyperbolic; well-posedness claims align with finite propagation.",
            "CFL inequality compares timestep to spatial scale via wave speed c_eff; both sides share time dimension.",
            "Gradient and time-derivative bounds are norm comparisons on the same field φ, ensuring compatible units.",
            "Energy inequality integrates gradient magnitude squared, yielding scalar cost matched by E_exotic.",
        ],
    ),
    EquationBlock(
        id="MEASUREMENT",
        name="Measurement Operator and Record Stability",
        file=Path("Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md"),
        section="C.1 Measurement as Relational Perturbation",
        equations=[
            EquationItem(
                label="Measurement operator mapping",
                pattern=r"\\mathcal\{M\}\s*:\s*\(DFVM,\s*MSC\)\s*\\rightarrow\s*\(\\Psi_\{record\},\s*\\Delta\s*E,\s*\\Delta\s*S_\{entropy\}\)",
                expectation="Operator outputs record plus energy and entropy changes.",
            ),
            EquationItem(
                label="Entropy positivity",
                pattern=r"\\Delta\s*S_\{entropy\}\s*>\s*0",
                expectation="Entropy production enforces irreversibility.",
            ),
            EquationItem(
                label="Record stability gate",
                pattern=r"\\Psi_\{record\}.*S_\{MSC\}\(\\Psi_\{record\}\)\s*>\s*\\varepsilon_2",
                expectation="Record persists only when MSC cohesion exceeds threshold ε2.",
            ),
        ],
        structural_checks=[
            "Operator codomain bundles stabilized record (state), energy dissipation, and entropy increase → consistent tuple structure.",
            "Record stability inequality compares scalar cohesion to scalar threshold; decoherence path aligns with same metric.",
        ],
    ),
    EquationBlock(
        id="ENTROPY-MSC",
        name="Entropy–MSC Relationship",
        file=Path("Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md"),
        section="A.6 Entropy as MSC Decay Rate",
        equations=[
            EquationItem(
                label="Entropy derivative link",
                pattern=r"\\frac\{dS_\{entropy\}\}\{dt\}\s*\\propto\s*-\s*\\frac\{dS_\{MSC\}\}\{dt\}",
                expectation="Entropy rate inversely tracks MSC cohesion rate.",
            ),
        ],
        structural_checks=[
            "Both sides are time-derivatives of entropy-like scalars; proportionality preserves scalar dimensions and sign inversion for decay mapping.",
        ],
    ),
]


<<<<<<< ours
<<<<<<< ours
=======
=======
>>>>>>> theirs
LIMIT_CHECKS: List[LimitCheck] = [
    LimitCheck(
        id="SATP-WAVE",
        title="SATP PDE wave-limit reduction",
        assumption="Set V'(φ) = 0 and J_SATP = 0",
        result=r"∂_t^2 φ − c_eff^2(x,t) ∇^2 φ = 0 (variable-coefficient wave equation)",
        interpretation=(
            "Hyperbolic class preserved with finite propagation speed; CFL bound and bounded gradient/time rates remain the"
            " governing stability gates."
        ),
    ),
    LimitCheck(
        id="MSC-RHO-POS",
        title="MSC cohesion with zero perturbation stress",
        assumption="σ_pert = 0",
        result=r"S_MSC[Ψ] = ∫ ρ_rel(Ψ) dV",
        interpretation="Cohesion increases with redundant relational binding and constraint closure, reinforcing identity stability.",
    ),
    LimitCheck(
        id="MSC-RHO-ZERO",
        title="MSC decay with absent relational density",
        assumption="ρ_rel = 0",
        result=r"S_MSC[Ψ] = −∫ σ_pert(Ψ) dV → decay",
        interpretation="Perturbation stress dominates, driving cohesion toward collapse and matching the identity dissolution narrative.",
    ),
    LimitCheck(
        id="ENTROPY-LINK",
        title="Entropy increase vs. cohesion decay",
        assumption=r"dS_entropy/dt ∝ − dS_MSC/dt",
        result="Rising entropy corresponds to decreasing MSC cohesion rate",
        interpretation="Maintains the text’s mapping: entropy growth tracks cohesion decay, aligning memory persistence with MSC resistance.",
    ),
]


<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_equation_presence(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.DOTALL) is not None


def build_report() -> str:
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    lines: List[str] = ["# Equation Structural Audit", "", f"Generated: {timestamp}", ""]

    for block in CRITICAL_BLOCKS:
        text = load_text(block.file)
        lines.append(f"<!-- MATH-CRITICAL: {block.id} -->")
        lines.append(f"## {block.name} ({block.id})")
        lines.append("")
        lines.append(f"- File: {block.file}")
        lines.append(f"- Section: {block.section}")
        lines.append("")
        lines.append("### Equation Presence")
        for eq in block.equations:
            present = check_equation_presence(text, eq.pattern)
            status = "PASS" if present else "MISSING"
            lines.append(f"- [{status}] {eq.label}: {eq.expectation}")
            if not present:
                lines.append(f"  - Pattern not found: `{eq.pattern}`")
        lines.append("")
        lines.append("### Structural Checks")
        for check in block.structural_checks:
            lines.append(f"- [OK] {check}")
        lines.append("")

<<<<<<< ours
<<<<<<< ours
=======
=======
>>>>>>> theirs
    lines.append("## Limiting / Sanity Checks")
    lines.append("")
    for check in LIMIT_CHECKS:
        lines.append(f"- **{check.title} ({check.id})**")
        lines.append(f"  - Assumption: {check.assumption}")
        lines.append(f"  - Result: {check.result}")
        lines.append(f"  - Interpretation: {check.interpretation}")
        lines.append("")

<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
    return "\n".join(lines)


def main() -> None:
    output_path = Path("reports/equation_structural_audit.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_report(), encoding="utf-8")


if __name__ == "__main__":
    main()
