import json
from pathlib import Path


CLAIMS = [
    {
        "id": "MSC-Functional-01",
        "claim": "S_MSC[Ψ] = ∫ (ρ_rel(Ψ) − σ_pert(Ψ)) dV defines the cohesion functional with collapse when S_MSC → 0",
        "status": "ASSERTED",
        "location": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md#A.1 Formal Definition of MSC",
    },
    {
        "id": "MSC-Regimes-01",
        "claim": "ε₁ and ε₂ bound subcritical, critical, and supercritical MSC regimes with corresponding identity stability behaviors",
        "status": "ASSERTED",
        "location": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md#A.2 Three Canonical Regimes of Modal Structural Cohesion",
    },
    {
        "id": "MSC-Entropy-Link",
        "claim": "dS_entropy/dt ∝ − dS_MSC/dt ties entropy growth to cohesion decay",
        "status": "ASSERTED",
        "location": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md#A.6 Entropy as MSC Decay Rate",
    },
    {
        "id": "Identity-Attractor-01",
        "claim": "Identity equals occupancy of a supercritical MSC basin and dissolves when S_MSC drops subcritical without transfer",
        "status": "ASSERTED",
        "location": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md#A.5 Identity as a Supercritical MSC Attractor",
    },
    {
        "id": "DFVM-Randomness-01",
        "claim": "DFVM_{t+1} = F(DFVM_t, MSC) + ξ(x,t) canonically localizes bounded, zero-mean, non-agentic randomness to DFVM",
        "status": "ASSERTED",
        "location": "Book2_Applications_and_Extensions/09_QuantumStochasticMechanics.md#Canonical Ontological Placement of Randomness",
    },
    {
        "id": "DFVM-Stochastic-Overdrive-02",
        "claim": "|ξ| ≫ MSC damping capacity forces MSC decay, identity collapse, and DFVM turbulence saturation",
        "status": "ASSERTED",
        "location": "Book2_Applications_and_Extensions/09_QuantumStochasticMechanics.md#Failure Mode: Stochastic Overdrive",
    },
    {
        "id": "Measurement-Operator-01",
        "claim": "ℳ : (DFVM, MSC) → (Ψ_record, ΔE, ΔS_entropy) with ΔS_entropy > 0 models measurement as energetic, relational, irreversible",
        "status": "SKETCHED",
        "location": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md#Formal Measurement Operator",
    },
    {
        "id": "Measurement-Record-Stability-02",
        "claim": "Ψ_record is stable iff S_MSC(Ψ_record) > ε₂; otherwise measurement decoheres",
        "status": "ASSERTED",
        "location": "Book_1_Core_Concepts/04_Modal_Structural_Cohesion.md#Record Stability Condition",
    },
    {
        "id": "SATP-PDE-01",
        "claim": "∂_t^2 φ − c_eff^2 ∇^2 φ + V′(φ) = J_SATP with bounded gradients/time-derivatives is a locally well-posed hyperbolic system",
        "status": "SKETCHED",
        "location": "Appendices/SATP_Final_PDE_Formulation.md#Well-Posedness Conditions",
    },
    {
        "id": "SATP-CFL-01",
        "claim": "Δt ≤ Δx / max(c_eff) is necessary for discrete SATP stability and prevents unphysical translation",
        "status": "SKETCHED",
        "location": "Appendices/SATP_CFL_Stability_Appendix.md#CFL-Type Stability Bound",
    },
    {
        "id": "SATP-Energy-01",
        "claim": "E_exotic ≥ ∫ |∇φ|^2 dV sets the minimum exotic energy cost, forbidding thin-wall shortcuts",
        "status": "ASSERTED",
        "location": "Appendices/SATP_Final_PDE_Formulation.md#Energy / Cost Constraint",
    },
]


def write_status_file(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(CLAIMS, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {len(CLAIMS)} rigour status entries to {output_path}")


def main() -> None:
    output_path = Path("reports/Math_Rigour_Status.json5")
    write_status_file(output_path)


if __name__ == "__main__":
    main()
