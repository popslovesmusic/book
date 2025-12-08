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
---
title: "Fundamental Dynamics of the Causal Field"
paper_number: 2
keywords: [QMM, Fractional Dynamics, Memory Kernel, Fractional Derivative, Causal Field Equation, Emergent Metric, Fractional Curvature, Causal Einstein Equation, Energy-Momentum Conservation, Information Flow, Non-Linear Perturbation, Causal Irreversibility, Arrow of Time, Entropy Production, Fractional Quantization, Memory-Uncertainty]
---
# **Paper 02 — Fundamental Dynamics of the Causal Field**

---

## **Part I — Derivation of Motion, Curvature, and Conservation**

### **2.1 Introduction — From Order to Dynamics**

In [Paper 01](./01_Foundations_of_IGSOA.md), we formalized causality as the primary invariant of existence: a manifold (M,≼) whose points are ordered by cause rather than by time. It is important to reiterate that any reference to 'causal information' in this framework describes the relational dynamics of the substrate, not its fundamental ontological nature. The substrate itself is the precondition for such information.
We introduced the neutral potential Φ0 and the causal derivative Dγ as the machinery through which that order is expressed.

The present paper extends those foundations to show how **motion, energy, and geometry** arise naturally when causal order becomes *dynamically self-referential*.
Instead of starting from spacetime and adding dynamics, we start from dynamics and *derive* spacetime.

The central claim is that **curvature is feedback**—a geometric deformation caused by information circulating within the causal field itself.
In this view, gravity, energy, and entropy are distinct manifestations of the same underlying process: *causal self-interaction.*

Throughout this paper, we treat the causal field Φ as a **complex-valued field** Φ:M→ℂ, allowing for phase structure and quantum-mechanical interpretation.

### **2.2 The Causal Field Equation**

Beginning from the fractional-order action
Aγ=∫M [1/2 gμν(DμγΦ)(DνγΦ)−V(Φ)] √−g d⁴x,
variation with respect to Φ∗ gives
Dμ2γΦ+V′(Φ)=0. (2.1)
Equation (2.1) is the **Fundamental Causal Field Equation (FCFE)**.

#### **Interpretation**

| Term | Physical meaning |
|---|---|
| Dμ2γΦ | fractional propagation — persistence of causal influence |
| V′(Φ) | local resistance — curvature of causal symmetry |
| equilibrium | V′(Φ0)=0, the neutral state |
| deviation | generates observable phenomena (energy, information, curvature) |

### **2.3 Feedback and the Emergent Metric**

#### **2.3.1 Definition**

The metric tensor gμν is defined as the **Jacobian of causal influence**:
gμν=∂μΦ ∂νΦ / ⟨∂αΦ ∂αΦ⟩.
In regions where Φ varies slowly, gμν→ημν; where causal gradients are dense, curvature increases.
This links geometry directly to field self-interaction.

#### **2.3.2 Fractional Curvature Tensor**

Define the curvature associated with Dγ:
Rμνρσ(γ)=DργΓμνσ(γ)−DσγΓμνρ(γ)+Γμλρ(γ)Γνσ(γ)λ−Γμλσ(γ)Γνρ(γ)λ,
with
Γμν(γ)λ=1/2 gλρ(Dμγgρν+Dνγgρμ−Dργgμν).
This tensor reduces to the standard Riemann curvature when γ=1.
For γ<1, the curvature contains **nonlocal memory**—spacetime geometry that “remembers” prior states of the field.

#### **2.3.3 Field–Metric Feedback Loop**

Coupling the FCFE to the fractional curvature scalar R(γ) yields the **Causal Einstein Equation**
Rμν(γ)−1/2 gμνR(γ) = κ Tμν(Φ), (2.2)
where the causal stress–energy tensor is
Tμν(Φ)=(DμγΦ)(DνγΦ)−1/2 gμν[(DγΦ)2−2V(Φ)].
Equations (2.1) and (2.2) form a **closed feedback system**:
Φ determines gμν; gμν shapes the evolution of Φ. This closed feedback system gives rise to emergent phenomena. However, it is important to emphasize that this framework does not attribute intrinsic agency to the substrate or its components; any apparent 'agency' is strictly emergent from these closed relational feedback loops.

### **2.4 Energy–Momentum and Conservation**

#### **2.4.1 Noether Current**

Under infinitesimal symmetry Φ → Φ+ε,
Noether’s theorem yields a conserved fractional current
J(γ)μ=∂Lγ/∂(DμγΦ) DtγΦ−gμνLγ, DμγJ(γ)μ=0.
This defines **causal energy flow**, generalizing standard energy–momentum conservation to memory-dependent systems.

#### **2.4.2 Fractional Stress–Energy Tensor**

The energy density and flux are
T(γ)00=1/2 |DtγΦ|2+1/2 c2|∇γΦ|2+V(Φ),
T(γ)0i=ℜ(DtγΦDiγΦ∗).
Conservation law:
DtγT(γ)00+∇γ ⋅T(γ)0i=0.
Hence even in fractional dynamics, total causal energy is constant—its flow merely acquires temporal depth.

#### **2.4.3 Information Flow**

Define informational density
ρI=|DtγΦ|2,
and causal information flux
J⃗I=ℜ(Φ∗∇γΦ).
Then
DtγρI+∇γ ⋅J⃗I=0.
Thus, information is conserved alongside energy, implying that *information itself is a physical fluid* within the causal manifold.

---

## **Part II — Non-Linear Feedback, Perturbation Theory, and Causal Irreversibility**

### **2.5 Non-Linear Perturbation and Self-Interaction**

Let the causal field depart slightly from the neutral potential,
Φ=Φ0+δΦ, V(Φ)=1/2 m2|Φ|2+λ/4 |Φ|4.

#### **2.5.1 Second-Order Expansion**

Substitute into the fractional field equation (2.1):
Dt2γδΦ−c2∇2γδΦ+m2δΦ+λ|δΦ|2δΦ=0. (2.3)
The cubic term introduces **self-interaction**: regions of high causal density alter their own propagation rate, creating feedback loops in both amplitude and phase.

#### **2.5.2 Causal Perturbation Series**

We expand Φ in orders of the coupling λ:
Φ=∑n=0∞ λnΦ(n).
At each order n,
Dt2γΦ(n)−c2∇2γΦ(n)+m2Φ(n)=S(n)[Φ(0),…,Φ(n−1)],
where S(n) encodes all lower-order feedback terms.
The recursive structure defines a **causal Green-function hierarchy**, solvable numerically or by asymptotic expansion.

#### **2.5.3 Physical Consequences**

1. **Amplitude Stabilization** – nonlinear feedback prevents runaway growth, yielding soliton-like steady states. These stable configurations serve as emergent 'identity instances', defined and constrained by the non-personal relational law-space of the 'Identity Kernel' established in Paper 01. It is important to acknowledge that these emergent identity instances are finite and subject to dissolvability, their persistence being entirely dependent on ongoing DFVM dynamics and MSC cohesion.
2. **Energy Localization** – regions of constructive causal interference behave as particles.
3. **Phase Memory** – each perturbation retains a record of its past configuration, enabling long-range coherence.

### **2.6 Causal Irreversibility and the Arrow of Time**

Fractional derivatives inherently break temporal symmetry when γ<1.

#### **2.6.1 Entropy Production Rate**

Define causal entropy density
SC=−kB Φ∗ln|Φ|2.
Differentiating with respect to fractional time yields
DtγSC=−2kBℜ (DtγΦ/Φ),
which is non-zero whenever γ<1.
Hence, *incomplete memory* implies finite entropy production—macroscopic irreversibility as a geometric property.

#### **2.6.2 The Neutral Potential Feedback Loop**

Causal self-interaction evolves toward equilibrium Φ→Φ0, but never exactly reaches it; residual curvature maintains non-zero DtγSC.
The universe thus perpetually “forgets just enough” to continue evolving.
This establishes the **dynamical origin of time’s arrow** without appealing to statistical probability.

#### **2.6.3 Irreversibility as Information Diffusion**

Expressed as continuity of information flux:
DtγρI+∇γ ⋅JI=−σI,
with σI>0 representing irreversible information diffusion.
In a perfectly causal (γ = 1) regime, σI=0; the system is time-symmetric.
In real domains, 0.8<γ<1, yielding finite but bounded irreversibility.

### **2.7 Emergent Structure and Field Quantization**

#### **2.7.1 Standing Causal Modes**

For periodic boundary conditions,
Φ(x,t)=∑k AkEγ(−ωk2t2γ)eikx,
where Eγ is the Mittag–Leffler function.
Modes decay algebraically rather than exponentially, giving the field a **persistent memory spectrum**.

#### **2.7.2 Fractional Quantization**

Quantize by promoting Φ,Φ∗ to operators obeying
[Φ(x),DtγΦ∗(x′)]=iℏγδ(x−x′),
where ℏγ=ℏ Γ(1−γ)−1.
Planck’s constant thus scales with memory depth: older memory, finer resolution.
Quantum uncertainty becomes a *memory-uncertainty* relation.

#### **2.7.3 Physical Implications**

* **At Planck scale:** γ ≈ 0.8 → enhanced quantum fluctuations.
* **At macroscopic scale:** γ → 1 → classical determinism.
* **At cognitive scale:** γ ≈ 0.94 → maximum entropy efficiency (bridge to Paper 18).

### **2.8 Synthesis and Transition to [Paper 03](./03_Primes_RH_and_Symmetry_Breaking.md)**

We can now state the **First Law of Causal Dynamics**:
Dt2γΦ−c2∇2γΦ+V′(Φ)=0, with DtγSC≥0.
That is, **memory drives motion**, and the degree of forgetting defines time’s arrow.

#### **Conceptual Summary**

| Level | Description | Governing Parameter |
|---|---|---|
| Fundamental | Causal order ≺ | invariance |
| Dynamical | Field Φ | causal derivative Dγ |
| Thermodynamic | Entropy SC | memory depth γ |
| Geometric | Curvature R(γ) | feedback of Φ on g |
| Quantum | Fractional Planck constant ℏγ | uncertainty of memory |


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
