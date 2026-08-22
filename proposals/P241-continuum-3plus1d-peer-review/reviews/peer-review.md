# P241 Peer Review — Constructive Review of the 3+1D Continuum Paper

**Paper:** Tiziano Fulceri, *2026-08-21_continuum_dynamics_3plus1D_solitonic_matter_equivalence_principle_v1.0*
**SHA-256 (frozen):** `dc23cbd98a551cb95d2409ab6bef0b1720303d420b6fb0d2b44a9ddd2f580783`
**Campaign:** P241 · **Lineage:** substrate-framework issue #154
**Review oracle boundary:** `python3 review/verify.py` (SymPy 21/21 modules, SciPy 5/5 modules, Lean 20 theorems, 10 replacement records)

## Summary

The manuscript generalizes a 1+1D sine–Gordon synthesis and a 2+1D nonlinear
Klein–Gordon treatment to three spatial dimensions: an elastic continuum with
Lagrangian density (2) produces localized energy lumps; impedance matching
(Section 4), a collective-coordinate/eikonal reduction (Section 5), and an
induced metric construction (Sections 6–9) yield special-relativistic
kinematics and a continuum-mechanics "equivalence principle".

The mathematical core that we could verify exactly **is correct**: the
Euler–Lagrange equation, the isotropic NLKG reduction with c0² = Θ0/ρ0, the
Compton-scale identities, the square-root effective Lagrangian identification,
the einbein/geodesic/optical-metric chain, time dilation, contraction, and
principal speeds all check symbolically. The defects are concentrated where
the manuscript asserts more than its own mathematics supports: existence
language for oscillons under a convex potential, two sign/factor errors in the
Newtonian limit and massless extension, determinant-convention slips in the
Kerr dictionary, unit-table inconsistencies, and an unhypothesized rest-mass
constancy. Every defect comes with a minimum honest repair (see
`repair-guide.md`); none undermines the framework's core program.

**Disposition: request changes.** 13 of 23 audited claims are supported as
stated (one with an editorial provenance rename); 10 require bounded
revisions. The Section 10 headline ("first fundamental advancement since
Einstein 1907") should be withdrawn or restated as the scoped conditional
theorem that survives.

## Findings by claim

### Supported as stated (13)

| ID | Content | Oracle |
|----|---------|--------|
| S01 | EL equation (5) from Lagrangian (2) | SymPy exact |
| S03 | Isotropic reduction (6)-(8) to NLKG, c0²=Θ0/ρ0 | SymPy exact |
| S04 | Compton scales (11)-(12); M0 scaling-only qualifier | SymPy exact |
| S07 | Eikonal hypothesis is declared; residual O(ℓ/L) confirmed | SciPy scaling |
| S09 | Centroid follows effective particle; M0-universality demonstrated | SciPy dynamics |
| S11 | Leff radicand = −g(X,X); boosted-family Legendre derivation | SymPy exact |
| S12 | Einbein constraint (27) recovers (26) | SymPy exact |
| S13 | Einbein EL ⇒ geodesics (28)-(30) | SymPy exact |
| S14 | Optical components (31)-(34) ≡ metric components (23)-(25) | SymPy exact |
| S15 | Time dilation ω = ω0√(−g00) | SymPy + Lean |
| S16/S17 | Contraction (37)-(39) and principal speeds (40)-(42) with stated premises | SymPy exact |
| S22 | Minimal rotating model (58)-(60) reproduces published 2+1D verbatim | SymPy exact |

### Revision required (10)

* **S02 (units).** The Section 2 bullets are mutually inconsistent: u
  dimensionless with Θ in N makes c0² carry m⁴/s². Repair: declare u a length;
  then [Θ]=Pa=J/m³, [Z0]=kg·m⁻²·s⁻¹ as intended.
* **S05 (static lumps).** The cited no-go literature concerns charged or
  time-dependent classes; for this uncharged static class Derrick gives
  E(λ)=E_g/λ+E_p/λ³ with E′<0 in d=3 — no static lump. Lean:
  `derrick_derivative_negative`.
* **S06 (oscillon existence language).** The displayed potential family is
  convex (hardening): local frequency ω(A)²=1+3A²/4 sits above the linear
  cutoff, so small lumps radiate rather than bind. Numerically: core energy
  fraction falls 0.63 → 0.04 between t=20π and t=40π with core frequency
  → 1.000 (linear), while the paper's own cited sine–Gordon class exhibits an
  exact breather keeping 100% of its energy with measured ω = 0.80002 vs
  exact √(1−η²) = 0.8. The mechanism lives in nonconvex potentials only.
* **S08 (reflectionless claim).** Scalar matching ρ(detΘ)^{1/3}=Z0 is exact
  only for isotropic slices; directional impedances of anisotropic media
  differ even when scalars match (Lean `s08_directional_mismatch_despite_
  scalar_match`; numerically matched interface reflects <2e-4 while Z2=2Z1
  reflects exactly the analytic (1/3)²=0.1111).
* **S10 (M0 constancy).** Used but never hypothesized; counterexamples with
  frozen profiles give dM0/dX ≠ 0.
* **S18 (Eq. 43).** Two defects: displayed sign is opposite to the geodesic
  value +c0²n′/(2n³) (which matches the manuscript's own prose), and the exact
  law carries 1/n² beyond grad(ln n). Mass-independence IS supported.
* **S19 (massless case).** Null rays curve exactly twice as much per unit
  time (a_null/a_massive = n³/n³·2 → 2; Richardson-extrapolated angle ratio
  2.0005 ± 0.0005 numerically). The equivalence principle must be scoped to
  massive universality.
* **S20 (Schwarzschild realization).** Profiles left implicit with convention
  ambiguity; exact corrected realization supplied: Ω²=f^{−1/3},
  n_r=f^{−4/3}, n_t=n_φ=f^{−1/3} (verified componentwise; Lean probe at
  f=8/27).
* **S21 (Kerr dictionary).** Four concrete defects: printed (56) drops one
  Σ² from its own coordinate determinant and matches no convention; spatial
  exactness forces Ω²=1 so the temporal component cannot match; (57)'s second
  equality contradicts its first (c0-power slip); A^{θθ}, A^{φφ} scale as
  L⁻²/T², L⁻⁶/T² — not speed squared. Full corrected dictionary supplied and
  verified (rational core identity K(Q+R)=1; five-component match up to
  declared Ω²).
* **S23 (composition).** The Section 10 chain inherits every scope above;
  composed unconditionally it overclaims. Headline sentence should be deleted
  or restated as the scoped theorem.

## What the revision does NOT require

No result needs to be retracted to zero: each repair preserves the strongest
supported statement (per the constructive-review policy). The corrected
Newtonian law, the corrected Kerr dictionary, the directional impedance
condition, and the scoped equivalence principle are all *stronger* scientific
objects than the defective originals because they now close.

## Provenance

* Upstream canonical issue: substrate-framework #154.
* Example pattern followed: PR #2 of vantasner-T/2026-08-19_NLKG…v0.1 (P238).
* All oracle modules are standalone (no substrate-framework imports);
  pinned environment: numpy==2.x-compatible fallbacks, scipy>=1.14,
  sympy==1.14, Lean/mathlib v4.28.0.

## Validation receipt

Run `python3 review/verify.py`. Expected tail state: all checks true;
claim counts {revision_required: 10, supported: 13}; oracle counts
sympy 21, scipy 5, lean_theorems 20, replacement records 10.
