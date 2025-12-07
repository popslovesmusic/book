# SATP – Final PDE Formulation

## Well-Posedness Conditions
The SATP conformal–scale field equations form a quasi-linear hyperbolic PDE system that is locally well-posed when gradients and curvatures remain bounded. In canonical form:

$$ \partial_t^2 \phi - c_{eff}^2(x,t) \nabla^2 \phi + V'(\phi) = J_{SATP} $$

Subject to bounds:

* $|\nabla \phi| < G_{max}$
* $|\partial_t \phi| < T_{max}$

These constraints preserve finite propagation, forbid superluminal worldlines, and avoid any symmetry restoration.

## CFL-Type Stability Bound
A Courant–Friedrichs–Lewy constraint governs stable discretizations:

$$ \Delta t \leq \frac{\Delta x}{\max(c_{eff})} $$

Violation produces numerical blow-up and unphysical “translation,” invalidating simulations and any operational mission profile.

## Energy / Cost Constraint
The exotic energy budget must satisfy

$$ E_{exotic} \geq \int |\nabla \phi|^2 dV $$

Sharper gradients raise the energetic cost, disallowing thin-wall shortcuts and favoring smooth profiles that minimize exotic load.

## Failure Modes

| Failure Mode | Trigger | Result |
| --- | --- | --- |
| CFL violation | $\Delta t$ too large | Numerical explosion |
| Gradient blowup | $\nabla \phi$ unbounded | Translation breakdown |
| Cost divergence | Thin-wall forcing | Prohibitive exotic requirement |
