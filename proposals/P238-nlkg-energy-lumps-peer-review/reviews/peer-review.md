# Peer review: 2+1D NLKG energy lumps and effective metrics

**Manuscript:** Tiziano Fulceri, *From 2+1D Nonlinear Klein–Gordon Energy
Lumps to Geodesic Propagation in an Effective Metric Induced by Substrate
Inhomogeneity, Anisotropy and Flow*, version 0.1 corrected, 19 August 2026.

**Recommendation:** major revision. The manuscript contains useful exact
wave-analogue constructions, especially the contravariant principal-symbol
metric and the exterior Schwarzschild acoustic eigenvalue/profile model. Its
central emergence claim is not established in the present draft. Three
load-bearing steps fail independently: the cited existence theorem does not
apply to the stated real field, the field-to-square-root reduction is asserted
rather than derived, and the displayed covariant metric is not the inverse of
the contravariant one. The minimal rotating model also does not match Kerr.

The review is terminal for all 18 frozen claims: 5 pass within an explicit
domain, 4 require qualification, and 9 fail their acceptance criterion. A
failed paper claim is a complete review disposition; it is not deferred review
debt.

## Method and reproducibility

The source was acquired from canonical issue #108 and frozen at SHA-256
`7cd35b8c397e874b581ce6da83c05b7047c256439d615d2f05cbbfb33536dd36`.
Claims were inventoried before published outputs were used as comparators.
Exact algebra and counterexamples were reconstructed with SymPy 1.14.0 and
Lean 4.28.0/mathlib; independent floating-point/domain probes used NumPy 2.5.2
and SciPy 1.18.0. The portable sources are in `../companion/` and the exact
machine-readable dispositions are in `../evidence/claim-results.yaml`.

Passing an oracle means that the review predicate behaved as intended. Some
predicates prove a counterexample, so a successful program run does not mean
that every manuscript claim passed.

## Claim-by-claim decision

| ID | Source | Decision | Review finding |
| --- | --- | --- | --- |
| P238-S01 | pp. 3–4, (1)–(5) | Qualified | Material-derivative algebra passes. “Most general” requires additional declared modelling restrictions. |
| P238-S02 | p. 4, (6)–(9) | Qualified | Euler–Lagrange and homogeneous equations pass. The full constant-background linearization retains `U''(0)u/rho0`; only the principal part is the quoted convective wave operator. |
| P238-S03 | pp. 4–5, (10)–(13) | Fail | Determinant matching has the right dimensions but does not eliminate generic anisotropic reflection; an exact matched-determinant interface has `R=1/3`. |
| P238-S04 | pp. 5–6, (14)–(20) | Pass | Conditional reconstruction of `rho`, `Theta`, and `N=c0 A^(-1/2)` is exact. It must be detached from the reflectionless interpretation. |
| P238-S05 | p. 6, (21)–(22) | Fail | Dispersion passes; the generic directional index is not the ordinary quadratic form of `N`. The 45-degree exact counterexample is `sqrt(10)/5 != 3/4`. |
| P238-S06 | pp. 6–7, §4 | Fail | Benci–Fortunato requires a complex charged field; its Q-ball theorem also uses `N>=3`. It does not guarantee the paper's real 2+1D lumps. |
| P238-S07 | p. 7, (23) | Qualified | A legitimate hypothesis, but no concrete family, residual order, internal-mode treatment, or error bound validates it here. |
| P238-S08 | pp. 7–8, (24) | Fail | A rigid translated profile in the stated quadratic field action yields velocity-quadratic dynamics, not an all-orders square root. The required boosted-profile integral is absent. |
| P238-S09 | pp. 7–8, (25)–(28) | Pass | Conditional einbein/geodesic identities pass and duplicate accepted `C-WLN-001`–`003`; they do not repair S08. |
| P238-S10 | pp. 8–9, (29)–(32) | Pass | With `K=(-omega/c0,k)`, the contravariant null polynomial exactly reproduces the wave dispersion relation. |
| P238-S11 | p. 9, (33)–(38) | Fail | The proposed covariant matrix is not the inverse. A diagonal exact example gives product `diag(1,2,1/2)`. |
| P238-S12 | p. 8, §6 bullets | Fail | Clock, ruler, massive free-fall, and equivalence-principle conclusions lack the required concrete observables and depend on failed S06/S08/S11. |
| P238-S13 | pp. 10–11, (39), (43)–(49), (53)–(54) | Pass | The acoustic eigenvalues give the Schwarzschild exterior null cone up to factor `f`; equations (40)–(42) do not and must be replaced. |
| P238-S14 | p. 11, (50)–(52) | Pass | Physical-basis constitutive profiles pass exactly for `r>rs`; density diverges and stiffness degenerates at the horizon. |
| P238-S15 | pp. 12–13, (55)–(59) | Fail | The coefficient dictionary inherits the false inverse and cannot establish Kerr matching. |
| P238-S16 | p. 13, (60)–(67) | Fail | The minimal model has `g_tphi=-a`, `g_phiphi=r^2`; Kerr has `-a rs/r` and `r^2+a^2+a^2 rs/r`. No generic conformal match exists. |
| P238-S17 | p. 14, (68)–(72) | Qualified | Roots and selected surfaces pass. The prose reverses which root changes sign: it is the lower/counter-rotating root. |
| P238-S18 | pp. 15–16, §9 | Fail | The surviving evidence establishes narrower wave-analogue kinematics, not the claimed explicit emergence of massive-particle SR, GR, or equivalence. |

## Required mathematical corrections

### 1. Separate the wave principal symbol from massive-lump mechanics

Equations (29)–(32) are a valid null-cone representation of the local
high-frequency dispersion relation. That establishes ray kinematics. It does
not establish that a finite nonlinear energy lump has the square-root action,
uses the same metric, or carries operational clocks and rulers. The manuscript
should state this boundary every time it moves from rays to massive lumps.

For the latter claim, provide one explicit localized solution family
`u(x-X(t); alpha(t), Xdot(t))`, perform the spatial action integral, state the
adiabatic order, and bound the residual, radiation, and internal-mode terms.
The cited 1+1D paper assumes a boosted breather and omits this decisive
integral; it cannot substitute for the 2+1D calculation.

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
and phase ansatz are indispensable. Either change the field model to match
those hypotheses or supply existence/persistence evidence for an actual real
2+1D time-dependent family. Long-lived oscillons, Q-balls, vortices, and static
real solitons are not interchangeable categories.

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

### 5. Rename the rotating construction

The model in equations (60)–(72) is a minimal rotating acoustic analogue. It
shares the Kerr radial factor and selected horizon/ergosurface locations, but
it does not reproduce the independent equatorial Kerr coefficient ratios.
Conformal freedom cannot change those ratios. The sentence about root reversal
must also be corrected: the counter-rotating/lower root changes sign in the
sampled ergoregion; the co-rotating/upper root remains positive.

## What survives and is worth retaining

The following form a coherent, defensible narrower paper after correction:

1. the specific convective anisotropic scalar action and its exact field
   equation;
2. the conditional algebraic reconstruction of constitutive fields from SPD
   `A` under the chosen determinant normalization;
3. the contravariant wave metric/null-cone representation;
4. the exterior Schwarzschild acoustic eigenvalues, coordinate null speeds,
   and determinant-normalized constitutive profiles; and
5. the exact einbein identities, explicitly identified as conditional prior
   results rather than a field-to-particle derivation.

The corrected conclusion should say that these results define a program for
wave analogue geometry. Massive energy-lump kinematics, operational
time/ruler effects, a full Kerr analogue, and an emergent equivalence principle
remain research objectives requiring new evidence.

## Framework disposition

No accepted Substrate claim is changed. The exact einbein content is already
accepted; other surviving statements are conditional constructions preserved
as P238 proposal evidence. This review requests no silent claim promotion. The
portable SymPy/SciPy/Lean corpus is retained intact so it can be moved into a
future author companion repository without depending on Substrate governance.
