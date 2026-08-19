# Peer review: 2+1D NLKG energy lumps and effective metrics

**Manuscript:** Tiziano Fulceri, *From 2+1D Nonlinear Klein–Gordon Energy
Lumps to Geodesic Propagation in an Effective Metric Induced by Substrate
Inhomogeneity, Anisotropy and Flow*, version 0.1 corrected, 19 August 2026.

**Recommendation:** major revision, with concrete repair paths below. The manuscript contains useful exact
wave-analogue constructions, especially the contravariant principal-symbol
metric and the exterior Schwarzschild acoustic eigenvalue/profile model. Its
central emergence claim is not established in the present draft. Three
load-bearing steps need independent correction: the cited existence theorem does not
apply to the stated real field, the field-to-square-root reduction is asserted
rather than derived, and the displayed covariant metric is not the inverse of
the contravariant one. The minimal rotating model also does not match Kerr.

All 18 frozen claims have been reviewed: 5 are supported as written within an
explicit domain, and 13 need revision. “Needs revision” is not a gate or a
claim that the research direction is impossible. It means the current wording,
derivation, citation, or evidence does not yet support the stated conclusion;
each such finding below includes a scoping, algebraic, or evidential repair.
Novelty is not an acceptance criterion.

The scientific comparator is the manuscript itself. Each statement is tested
against its own displayed definitions, equations, assumptions, source anchors,
and cited dependencies. Substrate supplies the workflow, issue tracker, and
execution environment only; no Substrate claim or implementation determines
whether a paper claim is supported or needs revision.

## Method and reproducibility

The source was acquired from canonical issue #108 and frozen at SHA-256
`7cd35b8c397e874b581ce6da83c05b7047c256439d615d2f05cbbfb33536dd36`.
Claims were inventoried before published outputs were used as comparators.
Exact algebra and counterexamples were reconstructed with SymPy 1.14.0 and
Lean 4.28.0/mathlib; independent floating-point/domain probes used NumPy 2.5.2
and SciPy 1.18.0. The portable sources are in `../companion/` and the exact
machine-readable dispositions are in `../evidence/claim-results.yaml`.
Author-ready replacement language, formulas, and file mapping are in
`../evidence/repair-guide.md`.

Passing an oracle means that the review predicate behaved as intended. Some
predicates prove a counterexample, so a successful program run does not mean
that every manuscript claim passed.

## Claim-by-claim decision

| ID | Source | Decision | Review finding |
| --- | --- | --- | --- |
| P238-S01 | pp. 3–4, (1)–(5) | Revision | Material-derivative algebra is supported. Scope “most general” by listing the symmetry, locality, derivative-order, and excluded-coupling assumptions. |
| P238-S02 | p. 4, (6)–(9) | Revision | Euler–Lagrange and homogeneous equations are supported. Add `U''(0)u/rho0`, or say only the principal part is the quoted convective wave operator. |
| P238-S03 | pp. 4–5, (10)–(13) | Revision | Determinant normalization is supported; generic reflectionlessness is not. Scope the language or derive directional interface impedances. |
| P238-S04 | pp. 5–6, (14)–(20) | Supported | Conditional reconstruction of `rho`, `Theta`, and `N=c0 A^(-1/2)` is exact. Detach it from the reflectionless interpretation. |
| P238-S05 | p. 6, (21)–(22) | Revision | Dispersion is supported. Replace the generic directional-index quadratic form with `c0/sqrt(khat^T A khat)`. |
| P238-S06 | pp. 6–7, §4 | Revision | The cited theorem assumes a complex charged field and does not establish the real 2+1D claim. Change the model/hypotheses or add matching existence/persistence evidence. |
| P238-S07 | p. 7, (23) | Revision | The eikonal statement is acceptable as a hypothesis. Keep downstream conclusions conditional, or add a concrete family and residual/error bound. |
| P238-S08 | pp. 7–8, (24) | Revision | The displayed rigid ansatz yields velocity-quadratic dynamics, not an all-orders square root. Supply the velocity-dependent boosted-profile integral and errors. |
| P238-S09 | pp. 7–8, (25)–(28) | Supported | Independent elimination, null variation, and generic 2D Euler–Lagrange reconstruction establish the conditional einbein/geodesic identities; they do not repair S08. |
| P238-S10 | pp. 8–9, (29)–(32) | Supported | With `K=(-omega/c0,k)`, the contravariant null polynomial exactly reproduces the wave dispersion relation. |
| P238-S11 | p. 9, (33)–(38) | Revision | The proposed covariant matrix is not the inverse. Replace it with the exact block inverse supplied below and rerun downstream maps. |
| P238-S12 | p. 8, §6 bullets | Revision | Scope these conclusions to wave-ray kinematics until a concrete lump supplies clocks, rulers, and the massive free-fall bridge. |
| P238-S13 | pp. 10–11, (39), (43)–(49), (53)–(54) | Supported | The acoustic eigenvalues give the Schwarzschild exterior null cone up to factor `f`; equations (40)–(42) separately need the S11 correction. |
| P238-S14 | p. 11, (50)–(52) | Supported | Physical-basis constitutive profiles are exact for `r>rs`; explicitly state the horizon divergence/degeneracy and basis convention. |
| P238-S15 | pp. 12–13, (55)–(59) | Revision | Rederive the coefficient system from the corrected S11 inverse; the present dictionary cannot establish Kerr matching. |
| P238-S16 | p. 13, (60)–(67) | Revision | Rename this a minimal rotating acoustic model, or solve the full independent Kerr coefficient-ratio system. The current model is not conformal to Kerr. |
| P238-S17 | p. 14, (68)–(72) | Revision | Roots and selected surfaces are supported. Correct the prose: the lower/counter-rotating root changes sign. |
| P238-S18 | pp. 15–16, §9 | Revision | Scope the headline to the supported wave-analogue constructions until S06/S08/S11/S15 are repaired. |

## Required mathematical corrections

### 1. Separate the wave principal symbol from massive-lump mechanics

Equations (29)–(32) are a valid null-cone representation of the local
high-frequency dispersion relation. That establishes ray kinematics. It does
not establish that a finite nonlinear energy lump has the square-root action,
uses the same metric, or carries operational clocks and rulers. The manuscript
should state this boundary every time it moves from rays to massive lumps.

The companion supplies two pieces of the repair: a finite-time real 2+1D
localized trajectory in `scipy_replacements.py`, and the exact Legendre
derivation `E=gamma E0`, `p=gamma E0 v/c0^2` implies
`L=-E0/gamma` in `sympy_replacements.py` and
`P238ReplacementProofs.lean`. The manuscript can use that square-root result
conditionally for a boost-closed family. Its inhomogeneous extension still
needs the substituted residual, adiabatic order, radiation, and internal-mode
error; those should be explicit hypotheses until calculated.

### 2. Replace the covariant metric dictionary

Write `v=V/c0`, `B=N^(-2)`, and

```text
H = [ -1      -v^T      ]
    [ -v   B - v v^T ].
```

The inverse of `nbar H` is

```text
1/nbar [ -1 + v^T N^2 v    -v^T N^2 ]
       [     -N^2 v              N^2 ].
```

Thus equations (33)–(38) use the wrong matrix power and mixed-term sign. This
is not removable by a scalar conformal factor when the principal indices are
unequal. All clock/ruler statements and all covariant Schwarzschild/Kerr
matching must be rederived from the corrected inverse.

### 3. Narrow the existence statement to the actual theorem

The cited theorem's complex U(1)-charged field, conserved charge, dimension,
and phase ansatz are indispensable. `scipy_replacements.py` supplies a usable
narrower replacement: for `U=1-cos u` and declared Gaussian data, both
leapfrog and DOP853 reproduce a real radial 2+1D localized trajectory through
`t=30`, with spatial refinement and late core-energy fraction above 0.90.
State that finite-time computational claim rather than an all-potential
existence theorem. Long-lived oscillons, Q-balls, vortices, and static real
solitons remain distinct categories.

### 4. Correct the anisotropic index and impedance statements

Use

```text
n_phase(khat) = c0 / sqrt(khat^T A khat)
```

for phase propagation. `khat^T N khat` is generally different. Likewise,
`rho sqrt(det Theta)=constant` is a useful scalar constitutive normalization,
but it does not match the normal impedance of every anisotropic interface.
Any reflectionless claim needs boundary conditions, interface orientation,
mode/polarization, and the appropriate directional impedance.

### 5. Replace or rename the rotating construction

The model in equations (60)–(72) is a minimal rotating acoustic analogue. It
shares the Kerr radial factor and selected horizon/ergosurface locations, but
it does not reproduce the independent equatorial Kerr coefficient ratios.
The companion provides an exact replacement: with
`Delta=r^2-rs*r+a^2`, `G=r^2+a^2+a^2 rs/r`, choose
`Omega^2=Delta/G`, `h_rr=r^2 G/Delta^2`, `h_phiphi=G^2/Delta`, and
`V^phi/c0=a rs/(rG)`. Then `Omega^2 g_acoustic=g_Kerr` coefficient by
coefficient, as proved in both replacement proof files. If the original
profiles are retained instead, rename them a minimal rotating acoustic model.
The root sentence must also be corrected: the counter-rotating/lower root
changes sign; the co-rotating/upper root remains positive.

## What survives and is worth retaining

The following form a coherent paper after applying the supplied corrections:

1. the specific convective anisotropic scalar action and its exact field
   equation;
2. the conditional algebraic reconstruction of constitutive fields from SPD
   `A` under the chosen determinant normalization;
3. the contravariant wave metric/null-cone representation;
4. the exterior Schwarzschild acoustic eigenvalues, coordinate null speeds,
   and determinant-normalized constitutive profiles; and
5. the exact einbein identities, explicitly conditional on the repaired
   field-to-particle bridge;
6. the scoped finite-time real 2+1D localized trajectory; and
7. the exact conformal equatorial Kerr acoustic map from the corrected inverse.

The corrected conclusion can claim the exact wave analogue, the scoped
finite-time real lump, the conditional boosted-family worldline action, and the
exact conformal Kerr map. Operational time/ruler effects and the inhomogeneous
massive-lump error bound remain conditional research objectives rather than
grounds for rejecting the program.

## Repository boundary

Substrate is not a scientific comparator in this review. Its repository-native
workflow provides source freezing, issue traceability, executable environments,
and validation checks. The supported/revision assessments above use only the
paper's claims, definitions, assumptions, internal dependencies, and the
external theorems the paper itself invokes. The portable SymPy/SciPy/Lean
corpus is retained intact so it can be moved into a future author companion
repository without inheriting Substrate governance.
