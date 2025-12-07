# SATP CFL Stability Appendix

## CFL-Type Stability Bound

The discrete evolution of the SATP hyperbolic system must satisfy

$$ \Delta t \leq \frac{\Delta x}{\max(c_{eff})} $$

Any violation induces numerical blow-up and unphysical translation artifacts. This bound is mandatory for simulation validity and for engineering feasibility studies tied to mission timelines.

## Operational Guidance

* Calibrate $c_{eff}$ envelopes before selecting $\Delta t$.
* Enforce adaptive meshing to maintain $\Delta x / \Delta t$ within the stability cone.
* Log any attempted bound violations as test failures rather than silently clipping parameters.

## Failure Tracking

| Failure Mode | Diagnostic Signature | Mitigation |
| --- | --- | --- |
| CFL violation | Divergent energy norm within a timestep | Reduce $\Delta t$, refine mesh |
| Gradient blowup | $\|\nabla \phi\|$ exceeds $G_{max}$ | Apply smoothing, revisit boundary conditions |
| Cost divergence | Exotic energy budget exceeds payload | Relax thin-wall forcing, adopt smoother profiles |
