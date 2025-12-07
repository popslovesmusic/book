---
title: "Foundations of the IGSOA–QMM Framework"
paper_number: 1
keywords: [IGSOA, Axioms, Causal Primacy, Causal Manifold, Neutral Potential, Invariant Action, Causal Field Equation, Automorphism Invariance, Fractional Extension, Causal Memory]
---
# **Paper 01 — Foundations of the IGSOA–QMM Framework**

---

## **Part I — Axioms, Neutral Potential, and the Invariant Action**

### **1.1 Introduction — Causality Before Time**

Every physical law presupposes sequence.
Before there is motion, there must be order; before there is time, there must be cause.
This principle—the primacy of *causal order*—is the cornerstone of the IGSOA–QMM synthesis.

Conventional physics treats time as a coordinate t and builds dynamics upon it.
IGSOA reverses that logic: time is *derived* from the structure of causal relations.
The manifold of the universe is therefore not (M,gμν) in the classical sense but (M,≺), a topological set M endowed with a partial order ≺ representing the direction of cause.

From this single axiom flow all others.
Metric, curvature, and what is described as 'information' and 'meaning' become emergent properties of how the manifold preserves or distorts this order. It is crucial to note that 'information' here denotes the relational dynamics and patterns, not the intrinsic nature of the monistic substrate itself, which remains the precondition for all such emergent properties.
The goal of this paper is to formalize that principle mathematically and prepare it for its later generalization under fractional dynamics (QMM).

### **1.2 Axioms of the Causal Manifold**

We postulate the existence of a manifold M equipped with a binary relation ≺ satisfying:

1. **Irreflexivity** x⊀x.
2. **Transitivity** x≺y, y≺z⇒x≺z.
3. **Local Density** For any x≺z there exists y such that x≺y≺z.
4. **Causal Connectivity** Every point admits a neighborhood whose causal links form a connected graph.
5. **Automorphism Invariance** Physical law is invariant under all automorphisms of (M,≺).

A field configuration is then a section
Φ:M→C,
assigning to each event its *causal amplitude*.
Causality itself is encoded in how Φ propagates along the order relation, not through external coordinates.

### **1.3 The Neutral Potential Φ0**

#### **Definition**

The neutral potential is the field configuration corresponding to perfect causal symmetry:
DμDμΦ0=0, Φ0=const.
It represents the state of the manifold when every causal path is balanced—no net asymmetry, no directionality beyond order itself.
In ordinary physics this would correspond to the vacuum, but here it is more fundamental: the *ground of possibility* from which curvature, energy, and information emerge when symmetry breaks.

#### **Perturbations and the Genesis of Structure**

Let
Φ=Φ0+δΦ.
Substituting into the invariant action (derived below) produces to first order
DμDμδΦ+V′(Φ0) δΦ=0.
Non-trivial V′(Φ0) defines the *asymmetry potential*—the seed of all later dynamics, including fractional memory terms once the kernel of D is extended in [Paper 02](./02_Fundamental_Dynamics_of_the_Causal_Field.md).

#### **Physical Interpretation**

| Quantity | Conceptual Meaning |
|---|---|
| Φ0 | neutral potential; pure causal equilibrium |
| δΦ | asymmetry; generator of phenomena |
| Dμ | causal derivative operator (directional, not temporal) |
| V(Φ) | curvature of causal information; determines stability |

The *universe before time* corresponds to Φ=Φ0.
Every event since is a perturbation in that field—a deviation from perfect causal symmetry. These stable patterns of perturbation, or coherent configurations within the causal field, can be understood as 'identity instances'. Their stability is maintained through MSC-level cohesion, acting as 'stable relational attractors'. It is important to note that this framework describes emergent phenomena and does not attribute intrinsic agency to the substrate or its components. Any apparent 'agency' is strictly emergent from closed relational feedback loops within the causal field. Furthermore, all such identity instances, by their emergent nature, are finite and subject to dissolvability, their persistence being entirely dependent on ongoing DFVM dynamics and MSC cohesion.

### **1.4 The Invariant Action**

We now define the **Invariant Causal-Order Spacetime Action**:
A[Φ,g]=∫M [1/2 gμν(DμΦ)(DνΦ)−V(Φ)] √−g d⁴x.

#### **Postulate of Invariance**

For any automorphism f:(M,≺)→(M,≺),
A[Φ,g]=A[Φ ∘ f,gf],
where gf is the pullback of the metric under f.
This guarantees that physics depends only on the *causal structure*, not on coordinate representation. This causal structure itself acts as a non-personal 'Identity Kernel', defining the relational law-space within which all emergent identity instances (stable configurations) are formed and constrained.

#### **Causal Derivative Operator**

Unlike the standard covariant derivative, Dμ acts along chains in the causal set:
DμΦ(x)=lim⁡ϵ→0 Φ(x+ϵvμ)−Φ(x) / ϵ, vμ∈TxM, where vμ is future-directed.
This ensures that derivatives respect the arrow of cause.
In later fractional generalization ([Paper 02](./02_Fundamental_Dynamics_of_the_Causal_Field.md)) this derivative acquires a non-integer order γ, giving rise to the *memory kernel* fundamental to QMM.

#### **Variation and Field Equation**

Variation of A with respect to Φ yields the **Causal Field Equation**:
DμDμΦ=∂V/∂Φ.
At equilibrium V′(Φ0)=0, the field is neutral.
Perturbations evolve by propagating causal curvature—precisely the mechanism that will later generate gravity, information, and semantic fields.

---

## **Part II — Automorphism Invariance, Fractional Extension, and Causal Memory**

### **1.5 Automorphism Invariance Theorem**

#### **Statement**

Let (M,≺) be a causal manifold and
A[Φ,g] the invariant action
A=∫M [1/2 gμν(DμΦ)(DνΦ)−V(Φ)] √−g d⁴x.
Then A is invariant under every automorphism
f:(M,≺) → (M,≺) satisfying
f(x)≺f(y)⟺x≺y.

#### **Proof**

1. Under f, coordinates transform as x′μ=fμ(x).
2. The causal derivative transforms covariantly:
D′μΦ′(x′)=∂xν/∂x′μ DνΦ(x).
3. Because f preserves ≺, the sign of causal separation is unchanged; hence the measure √−g d⁴x is invariant up to a Jacobian J with |J|=1.
4. Substitution yields
A′=∫M [1/2 gμν(DμΦ)(DνΦ)−V(Φ)] √−g d⁴x = A.
Thus, A depends only on the **causal structure**, not on any coordinate chart. □

#### **Corollary — Causal Equivalence Principle**

If two manifolds M1,M2 share identical causal orderings up to automorphism, all physical predictions coincide.
Geometry is therefore *secondary*; causal symmetry alone determines physics.
This principle becomes the seed of the **Causal Equivalence Hypothesis** in later cosmological applications ([Paper 03](./03_Primes_RH_and_Symmetry_Breaking.md)–20).

### **1.6 Fractional Extension of the Causal Derivative**

To model persistence and memory, we extend the integer-order causal derivative Dμ to a **fractional-order operator** Dμγ, 0<γ≤1.

#### **Definition**

DμγΦ(x)=1/Γ(1−γ) ∫_{x₀}^{x} DμΦ(ξ)/(x−ξ)γ dξ, where vμ is future-directed.
This nonlocal kernel gives weight to all prior causal events ξ≺x, so the present field value encodes its history.

#### **Modified Action**

Aγ=∫M [1/2 gμν(DμγΦ)(DνγΦ)−V(Φ)] √−g d⁴x.
Varying Aγ yields the **Fractional Causal Field Equation**
Dμ2γΦ=∂V/∂Φ.
For γ=1, this reduces to the standard IGSOA equation; for γ<1, nonlocal memory enters explicitly.
This is the mathematical bridge to the Quantum Memory Mechanism (QMM).

#### **Physical Interpretation**

| Parameter | Meaning |
|---|---|
| γ | order of causal memory (how far back influence extends) |
| Dμγ | weighted causal derivative, integrating history |
| V(Φ) | potential curvature controlling stability of memory |
| Dμ2γΦ | propagation through self-memory (fractional inertia) |

The appearance of Γ(1−γ) implies power-law memory decay—a property observed in quantum noise, biological cognition, and gravitational echo phenomena.

### **1.7 Time as Causal Memory**

#### **Definition**

Define *causal time* τ as the cumulative integral of causal weight:
τ(x)=1/Γ(γ) ∫_{x₀}^{x}(x−ξ)γ−1 dξ ⇒ Dτ1=Dμγ.
Hence, what we perceive as temporal flow is merely the *integration of causal memory*.
There is no external clock—only the manifold’s own remembrance of its previous states.

### **Implications**

1. **Arrow of Time:**
The direction of increasing memory depth defines time’s arrow.
2. **Reversibility:**
Perfect recollection (γ=1) implies reversible dynamics; incomplete memory (γ<1) produces apparent irreversibility.
3. **Entropy:**
Growth of entropy corresponds to dilution of causal memory density, not fundamental disorder.

Thus, thermodynamic time emerges naturally from causal incompleteness, linking microscopic memory with macroscopic irreversibility.

### **1.8 Synthesis and Transition to Paper 02**

The structure now established can be summarized succinctly:
Causal Order ⇒ Derivative Operator Dγ ⇒ Memory Propagation ⇒ Time.
All subsequent physics arises from this chain.
In [Paper 02](./02_Fundamental_Dynamics_of_the_Causal_Field.md) we will:
* derive the **fundamental dynamical equations** of the causal field,
* extract the **energy–momentum tensor** and conservation laws,
* and show how curvature emerges from the feedback of Φ upon gμν.
This will complete the transition from pure causal geometry to **dynamic spacetime**, paving the way for the fractional thermodynamic, semantic, and cosmological developments that follow.


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
