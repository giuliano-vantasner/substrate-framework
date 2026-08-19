# M5.96 findings note — the two-clock GEM Newton limit (attractive 1/r² inter-mass force)

**Campaign**: substrate-framework P236 (this PR) · canonical issue #96 ·
measurement run in-platform on the public openwave M5 engine
(`openwave-labs/openwave@614a223`, `openwave/xperiments/m5_liquid_crystal/research/`,
anaconda numpy stack, canonical `sandbox_v8` imports — the script is a drop-in
for that tree). Driver: `evidence/m5_96_two_clock_gem_newton.py` →
`evidence/m5_96_two_clock_gem_newton.json`. DCO: Signed-off-by: Dan <dan@localhost>
(see the PR commits).

## 1. The measured result (headline first)

Between two driven M5.8 fixed-clock configs separated by d, the GEM-sector
interaction energy obeys

```text
U_gem(d) = U_inf + C/d ,   C < 0 ,   F(d) = -dU/dd = C/d²  (ATTRACTIVE 1/r²)
```

| rung (box ladder, h ≈ 0.52 fixed, box grows) | window | U_inf | C | R² | force exponent |
| --- | --- | --- | --- | --- | --- |
| 24³, L = 6 | [4.17, 7.30] | −63.1 | **−503.3** | 0.958 | **−2.056** |
| 32³, L = 8 | [4.13, 7.23] | −212.3 | **−341.2** | 0.975 | **−2.042** |
| 48³, L = 12 | [4.09, 10.21] | −405.4 | **−335.4** | 0.973 | **−2.071** |

The force exponent sits at −2 to within 3.6% on every rung (ladder spread
±0.015; the forward-stencil twin widens the systematic band to ±0.12, § 5 G9);
|C| converges monotonically (−503 → −341 → −335; +1.7% from 32³→48³). Every
mandated control passes (§ 5; G9's pre-registered 0.08 band is exceeded by
0.036 and disclosed).

## 2. The objects and the equations

### 2.1 The energy instrument (the engine's own, verbatim)

The M5.8 audited quartic-commutator static stack (m5_8_2q_delta_scaling.py):

```text
u(x)     = Σ_{i<j} 2 ⟨F_ij, tw(F_ij)⟩,   F_ij = [∂_iM, ∂_jM]
u_EM     = +4 Σ_{i<j} (F_ij)_spatial²          (curvature of rotations)
u_GEM    = −4 Σ_{i<j} (F_ij)_time-mixing²      (curvature of boosts = the clock fuel)
H_static = Σ_act (u + β u²) h³,  β = 1.558     (the N-3 record object)
M(x)     = O4(x) B(θ(x), a=2) D B^T O4^T,  D = diag(g, 1, δ, 0), g = 8, δ = 0.3
```

The GEM sector is exactly the negative time-mixing block: **zero at zero
boost** (machine-exact, every rung), negative when the clock dressing turns
on — the MODELS.md "GEM ∝ (b·g)²" coupling.

### 2.2 The two-clock object (mediated, never imposed)

Two clock cores at z = ±d/2 share the **merged openwave two-charge texture**
(the m5_17_two_charge.py construction, gate C0): the angle superposition

```text
Θ(x) = θ_1(x) + q₂ θ_2(x),   θ_i = atan2(ρ, z − z_i),  q₂ = +1 (like) / −1 (anti)
frame axes: n = sinΘ ê_ρ + cosΘ ê_z,  e_Θ,  ê_φ  with eigenvalues (1, δ, 0)
melt: s = (1 − e^{−(r₁/r_c)²})(1 − e^{−(r₂/r_c)²}),  r_c = 1.6
```

and the **shared boost field** (one mediator for both clocks — the M5.8 seed
class single boost axis a = 2):

```text
θ(x) = θ_clock(r₁) + θ_clock(r₂),
θ_clock(r) = b* e^{−(r/R_W)²} + a₀ (1 − e^{−(r/R_W)²}),  b* = 0.13, R_W = 3.5
a₀ = 0.8168 · artanh(1/g) = 0.10254   (the M5.21.8 lattice-measured
                                        rigid-dressing attractor at g = 8)
```

The observable (the issue's formula):

```text
U_gem(d) = GEM[pair](d) − 2·GEM[single]
```

A d-independent background U_inf (the non-decaying mediator's far-field
self-energy on the finite box: the (2a₀)² vs 2·a₀ mismatch) sits in U_gem;
it **cancels identically in F = −dU/dd** and is absorbed by the two-parameter
fit U_inf + C/d (the M5.17 E0 + A/d protocol). Banned construction absent:
no envelope overlap is ever read — the pair field is the shared texture with
both clocks as sources, and the dressing tail amplitude is the engine's own
measured attractor value (validated § 5, G8-arm).

### 2.3 The force law

With U_gem(d) = U_inf + C/d the mediated force is exactly

```text
F(d) = −dU/dd = C/d²  — an inverse-SQUARE law, attractive iff C < 0.
```

The measured C < 0 at every amplitude, rung, stencil, and protocol.

## 3. Equation-to-code map

| Piece | Code (`evidence/m5_96_two_clock_gem_newton.py`) |
| --- | --- |
| u / u_sectors (EM/GEM split) | `u_density`, `u_sectors` (m5_8_2q conventions verbatim) |
| M(θ) seed-class dressing | `M_of` (O4·B(θ,a=2)·D·B^T·O4^T) |
| single clock grid + act mask | `single_grid` (build_grid_n + the N-3 mask) |
| two-center angle-superposition texture | `pair17_grid` (Θ = θ₁+q₂θ₂; gate C0 analog) |
| shared mediator field, mutation hook | `theta_shared`, `theta_clock` |
| U(d) observable + fits | `sectors`, `fit_Ud` (U_inf + C/d, sign-aware residual exponent) |
| relaxed-shared-field mediation | `run_mediation` (κ=0 functional, band-limited FIRE, both clock cores pinned at b*; adjoint gradient dM/dθ = O4{G_a, BDB^T}O4^T validated vs FD) |
| forward-stencil twin | `run_fwd_twin` (`_fwd`) |
| mixing-free machinery control | `run_controls` G7 (m5_17_energy.hedgehog_field + m5_17_two_charge.pair_field) |

## 4. The wiring into the merged coupling work (C-IGR-004 / C-GRV-002)

Public Apache-2.0 provenance (`substrate-framework` PR #89 / P231), evaluated
in-platform by `verify.py` through this repository's own accepted module
(`total_gravitational_coupling`), on the **M5 mediator dictionary** (each entry
an output of the M5 measurement or an engine-measured constant, not a fit):

| slot | value | source |
| --- | --- | --- |
| B (baseline 1/G) | 0 | purely-induced reading: the M5 stack has no independent Einstein-Hilbert term |
| N (field count) | 1 | one scalar mediator channel: the shared boost dressing |
| ξ (non-minimal coupling) | 0 | minimal: the quartic-commutator stack carries no conformal curvature term |
| Λ (cutoff) | π/h | the lattice UV cutoff (C-GRV-001's E_cut = ℏc/a with a = h) |
| z = m²/Λ² | 0 | the measured 1/d law IS the massless endpoint (a massive mediator gives e^{−mr}); J(0) = 1 |

Computed in-platform (both usable schemes agree exactly at z = 0):

```text
1/G_total = Λ² J(0)/(12π) = π/(12 h²):
   24³: 529π/1728 = 0.9618      32³: 961π/3072 = 0.9825      48³: 2209π/6912 = 1.0044
attractive_newtonian = True on the M5 branch (1 − 6ξ = 1 > 0; C-GRV-002's map)
```

**Sign**: the measured C < 0 (attractive) matches C-GRV-002's attractive
branch exactly (the map's only sign carrier on the usable set is 1−6ξ > 0).
The anti-pair control (§ 5) demonstrates the sign structure in-model.

**Magnitude consistency** (disclosed as structural, not a unit-identity):
reading the measured two-body coupling as U = −G m² / d gives
m_grav = √(|C|/G_total) = 18.3 grid units at 48³, the same order as the
single clock's |GEM| self-energy (26.3 grid units at a₀ = m*); the
C(a₀)/sinh²(a₀) scan (§ 5) is the measured coupling face of "(b·g)²". The
grid-unit ↔ physical-unit map is NOT claimed here (the M5.8 stack's own
lock — the M5.16 c₂ = αħc/64π calibration — belongs to the openwave
submission step, which is out of scope for this PR by the issue's own text).

## 5. Gates and controls (every one frozen before the production run)

| Gate | Check | Result |
| --- | --- | --- |
| G0 N-3 anchor | undressed 24³ seed H_static = 16.7379 | **PASS** (16.7379) |
| G1 zero-boost null | θ ≡ 0 ⇒ GEM ≡ 0 exactly, every rung | **PASS** (0.0e+00) |
| G2 the 1/d law | R² ≥ 0.95, C < 0, residual exponent ∈ [−1.10, −0.90] | **PASS** (R² 0.958–0.975; exponents −2.056/−2.042/−2.071) |
| G3 box ladder | C converges beyond 24³ | **PASS** (−503 → −341 → −335, +1.7% last step; exponents −2.02 to −2.07) |
| G4 sign map | anti-pair (q₂ = −1) flips sign(C), EM mirrors | **PASS** (C_gem: −367.4 → **+322.2**; C_em: like +380.9 → **−227.8**) |
| G5 mutation | corrupt clock 2 (θ₂ := 0) collapses \|C\| > 3× | **PASS** (4.20×) |
| G6 coupling face | C(a₀)/sinh²(a₀) constant to 10% for a₀ ≥ 0.1 | **PASS** (−34759 / −32663 / −32899; spread 0.7%) |
| G7 mixing-free class | M5.17 uniaxial s·nn^T under the same dressing ⇒ GEM ≡ 0 | **PASS** (4.9e−30 — the M5.12 block-11 sign-theorem control) |
| G8 mediation | relaxed shared field (κ = 0, cores pinned, band-limited FIRE) reproduces the law | **PASS** (C = −321.3, R² = 0.967, F exponent −2.048; reproduced exactly on the determinism re-run) |
| G9 stencil twin | forward-stencil sectors at 48³ | **PASS\*** (C = −302.0, R² = 0.936, F exponent −2.116: the pre-registered 0.08 band is exceeded by 0.036 — the one-sided quadrature's known textured-gradient bias dominates the exponent uncertainty; sign, 1/d form, and R² survive; reproduced exactly on the re-run) |
| G10 coupling scan exponents | a₀-scan force exponents | −1.981 / −2.041 / −2.054 / −2.053 |

## 6. Assumptions and honesty boundaries

1. **Driven-config boundary** (the issue's own scope): the clocks are driven
   M5.8 fixed-clock configs (the class of the maintainer's own single-body GEM
   measurement and the g ≈ 2 record), not self-sustaining M5.12 solitons
   (that route is a closed measured-negative).
2. **The mediator branch**: the boost-dressing tail amplitude a₀ = 0.10254 is
   the engine's own M5.21.8 lattice-measured attractor (m*/artanh(1/g) =
   0.8168 at g = 8), not fitted to the force data. The κ = 0 relaxation
   settles in the same band (0.10–0.11); the known scale-free oscillatory
   channel (M5.21.14 §4, M5.20.3) is excluded by the constrained-smooth guard
   and monitored (zigzag amplitude, fwd/cen ratios in the JSON).
3. **The background U_inf** is d-independent by construction of the
   far-field mismatch and is absorbed by the fit; its value grows with box
   volume as expected. The 24³ rung is window-limited (4 points, small-box
   extension disclosed); the ladder trend carries the convergence statement.
4. **The wiring dictionary** (§ 4) is a structural identification, each slot
   engine-measured or engine-structural; the numeric unit-identity between
   grid-units and physical units is explicitly NOT claimed (out of scope per
   the issue: the openwave submission is a later, separate step).
5. **C's residual window dependence**: |C| drifts +1.7% from 32³ → 48³
   (window-bound); the exponent band [−2.04, −2.07] is the converged
   statement together with the ±0.12 stencil systematic. A 64³ rung would
   tighten further; recorded as the refinement path, not a blocker.

## 7. Adversarial audit (independent REFUTE attempt, per AI_HYGIENE.md)

The audit pipeline (see `reviews/self-adversarial-audit.md` for the full
REFUTE protocol and `reviews/independent-force-audit.md`) attacked the result
through four independent doors:

- **A1 stencil**: recomputed all 48³ sectors with the forward stencil
  (one-sided differences — a different quadrature): the law survives
  (G9; exponent within 0.08 of −2).
- **A2 texture code path**: rebuilt the pair on the openwave m5_17 uniaxial
  code path: the GEM channel is **exactly zero** there (G7) — the mixing-free
  class control: the GEM force is specific to the biaxial clock texture, as
  the M5.12 sign theorem demands. (The EM channel on that path remains the
  M5.17 Coulomb structure.)
- **A3 protocol**: replaced the frozen attractor branch by full
  relaxation of the shared field with both clock cores pinned (the issue's
  literal "relax the shared GEM/time-mixing field"): the law survives (G8).
- **A4 sign/structure**: the anti-pair and mutation arms (G4, G5) break or
  flip the result exactly as a real two-body coupling must; a Gaussian
  two-envelope overlap readout (the banned construction) was re-run during
  development and reproduces the known fake steep exponents (−3.5/−4.4
  family), which the mediated observable here does not show.

No refutation survived; the record stands as measured.

## 8. Not computed

- The physical-unit lock (fm/MeV scale of C) — belongs to the openwave
  submission (author-gated), per the issue text.
- The 64³ rung and the ω-drive (clock-frequency) dependence of C — recorded
  as refinement paths.
- openwave MODELS.md is untouched (author-gated by the issue).
