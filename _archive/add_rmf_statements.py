import os

rmf_statement = """
═══════════════════════════════════════════════════════════
RMF Compliance Statement

This paper affirms:
• Relational primacy (relations ontologically prior to objects)
• Monistic substrate (single undivided ground)
• Emergent identity as a relational attractor
• Strict distinction between identity law-space (IK) and identity instance
• Agency as emergent from closed relational feedback loops

This paper rejects:
• Substance dualism
• Object primacy
• Survival of personal identity as conscious entity
• Intrinsic agency in substrate or components

Classification: [RMF-COMPLIANT]
═══════════════════════════════════════════════════════════
"""

files_to_stamp = [
    "Book0_Ontological_Foundations/01_Relational_Dynamics_of_a_Monistic_Substrate.md",
    "Book0_Ontological_Foundations/02_The_NOT_Axiom.md",
    "Book0_Ontological_Foundations/03_The_Necessity_of_the_First_Action.md",
    "Book0_Ontological_Foundations/04_The_Tri-Unity_Law.md",
    "Book0_Ontological_Foundations/05_Emergence_of_Causal_Structure.md",
    "Book_1_Core_Concepts/01_Foundations_of_IGSOA.md",
    "Book_1_Core_Concepts/02_Fundamental_Dynamics_of_the_Causal_Field.md",
    "Book_1_Core_Concepts/03_Primes_RH_and_Symmetry_Breaking.md",
    "Book2_Applications_and_Extensions/04_BlackHole_HorizonImprinting.md",
    "Book2_Applications_and_Extensions/05_GravitationalWave_Echoes.md",
    "Book2_Applications_and_Extensions/06_CMB_Asymmetry.md",
    "Book2_Applications_and_Extensions/07_Fractal_Fractional_Spacetime.md",
    "Book2_Applications_and_Extensions/08_SpiralGeometry_Causality.md",
    "Book2_Applications_and_Extensions/09_QuantumStochasticMechanics.md",
    "Book2_Applications_and_Extensions/10_LotkaVolterra_Oscillators.md",
    "Book2_Applications_and_Extensions/11_LieAlgebra_BridgingFrameworks.md",
    "Book2_Applications_and_Extensions/12_Holography_and_Information.md",
    "Book2_Applications_and_Extensions/13_Entropy_and_Memory.md",
    "Book2_Applications_and_Extensions/14_CausalPolarization_LorentzForce.md",
    "Book2_Applications_and_Extensions/15_SATP_Field_Equation.md",
    "Book2_Applications_and_Extensions/16_Experimental_Predictions.md",
    "Book2_Applications_and_Extensions/17_Ethical_Frameworks.md",
    "Book2_Applications_and_Extensions/18_QMM_IGSOA_Comparison.md",
    "Book2_Applications_and_Extensions/19_Unification_and_Synthesis.md",
    "Book2_Applications_and_Extensions/20_Open_Problems.md",
    "Book2_Applications_and_Extensions/21_Future_Roadmap.md",
    "Book3_DFVM/01_Foundations.md",
    "Book3_DFVM/02_RH_as_DFVM_Regulator.md",
    "Book3_DFVM/02_RH_as_DFVM_Regulator_Outline.md",
    "Book3_DFVM/draft.md"
]

for file_path in files_to_stamp:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if rmf_statement not in content:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write("\n" + rmf_statement)
            print(f"Appended RMF statement to {file_path}")
        else:
            print(f"RMF statement already present in {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("RMF compliance stamping complete.")