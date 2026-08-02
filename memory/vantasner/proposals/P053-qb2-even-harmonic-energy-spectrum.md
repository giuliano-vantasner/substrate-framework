---
description: Derive and audit the even-harmonic energy spectrum behind QB2
author: vantasner
created: '2026-08-02T06:15:00Z'
updated: '2026-08-02T08:45:00Z'
tags:
- substrate-framework
- campaign-proposal
- radial-sine-gordon
- migration-QB2
category: proposals
confidence: exploratory
status: archived
---
# P053 QB2 Even-Harmonic Energy-Spectrum Audit

## Question and Positive Deliverable

P053 must produce a reusable, importable temporal-spectrum construction for
canonical energy observables of the accepted radial harmonic-balance branch
and determine the strongest honest twice-frequency statement supported by
QB2. The positive object includes an exact half-period selection theorem,
normalization-explicit Fourier coefficients, a declared local or integrated
observable, and numerical line evidence only if harmonic, temporal, radial,
domain, tolerance, and independent-transform gates pass. Merely showing that
QB2 overcalls a scalar FFT line “radiation” would be failure evidence, not the
positive deliverable.

## Base Release and Provenance

The accepted base is `v0.46.0` at framework commit `a1e9adf`; its scientific
transaction is `7659414`. Relevant authority is `C-PDE-001`, `C-MOM-003`,
`C-PDE-003` through `C-PDE-006`, and only the explicitly conditional portions
of `C-GW-005` and `C-GW-006`. QB2 is pending at `substrate@6d1f4e0`, path
`merged-framework/bridges/phase-16/bridge_QB2_clean_2omega_line.py`, SHA-256
`f7ff064a708d4b3072b247088bee532eda6b14ef4a9d9f5480ea80743a22bbff`.
Its cited FS2, P3D1, P3D3, and QB1 units are navigation evidence; their only
authority is the accepted claim mappings and qualifications. Memory search
found the P052 handoff and no accepted QB2 result. The full QB2 executable and
its numerical spectrum remain unopened until this contract is frozen.

## Invariants, Conventions, and Allowed Imports

The field is the dimensionless radial sine-Gordon scalar with canonical
energy density `T00=(u_t^2+u_r^2)/2+1-cos(u)`. The accepted finite odd-cosine
ansatz has `u(t+T/2)=-u(t)`, but its finite-box numerical branch is not an
exact periodic solution of the full PDE. Canonical energy density is even
under simultaneous sign reversal of the field and its derivatives. A radial
energy density has an exactly isotropic Cartesian second moment and zero STF
part under `C-MOM-003`, independently of any temporal line. A radiating STF
statement therefore requires a separately regular nonspherical mode,
conserved source conditions, and explicitly conditional gravity inputs.
Standard Fourier orthogonality, periodic DFT algebra, spherical integration,
and audited SciPy quadrature or BVP methods are allowed. No QB2 or P3D1 line
frequency, amplitude, peak ratio, window, or threshold is an input.

## Candidate Preregistration

The three candidates are frozen from accepted structure and queue metadata
before the source executable is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal QB2 field, energy observable, transform, and line classifier | Every source harmonic, mesh, wall, time grid, window, normalization, and threshold is explicit | Source branch point and spectral controls | May reproduce a clean finite-box scalar line but earns no authority from its tally | Hash-pinned run, equation and observable reconstruction, normalization audit, refinements, and load-bearing mutations |
| B | Exact and direct even-harmonic canonical-energy coefficients on C-PDE-006 | Odd field harmonics, canonical T00, explicit radial observable and finite box | Retained set, radial grid, temporal samples, wall, quadrature, coefficient convention | Natural positive scalar-spectrum object; exact odd-line nulls and generally nonzero even lines | Symbolic half-period proof, direct DFT/cosine-integral agreement, harmonic/radial/time/domain/tolerance refinement, residual correlation, and phase-shift tests |
| C | Regular infinitesimal l=2 moment spectrum on the harmonic background | C-PDE-003 linearized mode, formal epsilon, explicit regular data and outer condition | Mode normalization, domain, mesh, time or Floquet data, moment and derivative estimator | Only route capable of a nonzero STF source moment without violating spherical symmetry | Origin regularity, linearized residual, mode/moment convergence, zero-amplitude guard, convention-safe TT map, and an independent solver or soluble limit |

## Selection Criteria and Blinding

Selection is ordered by exact stress-energy and Fourier normalization,
half-period symmetry, spherical STF null and l=2 regularity, distinction among
local density, scalar radial moment, STF moment and conditional waveform,
assumption and parameter economy, numerical convergence, independent transform
agreement, and compatibility with every accepted epistemic ceiling. Numerical
closeness to a source or P3D1 value cannot select a candidate. The comparator
gate opens only after this contract, the manifest, line metric, structural
symmetry guards, refinement plan, mutations, and interpretation ceiling are
frozen.

## Proposed Claim Delta

Provisional `C-PDE-007` may state the exact even-harmonic selection theorem for
canonical energy density and any time-independent radial linear functional of
it, together with the spherical STF null. Provisional `C-PDE-008` may
separately record a finite-box scalar energy or radius-moment spectrum if its
twice-frequency coefficient and higher-line hierarchy pass all numerical
gates. A regular l=2 result would require its own oracle-specific claim or a
recorded proposal revision; it cannot be bundled into the scalar theorem.
Dependencies must be the smallest subset of `C-PDE-001`, `C-MOM-003`,
`C-PDE-005`, and `C-PDE-006`, with `C-PDE-003` through `C-GW-006` admitted only
if Candidate C is actually opened. Expected consumers are the QB2 disposition
and later QB3/QB4 units. No FFT line is promoted as exact full-PDE periodicity,
physical radiation, gravitational power, detector strain, particle identity,
absolute scale, or substrate realization.

## Implementation and Oracle Plan

A pure package surface will reconstruct field, time and radial derivatives,
canonical energy density, direct periodic Fourier coefficients, and declared
radial scalar observables without simulation at import. It will reuse the
accepted harmonic solution and shared version-independent quadrature helper.
SymPy or direct exact algebra is appropriate for half-period invariance,
odd-line nulls, the spherical STF guard, phase conventions, and Fourier
normalization. NumPy/SciPy is appropriate for finite-box coefficient and
quadrature evidence.

Numerical evidence will record float64, branch parameters, harmonic set,
radial interpolation and quadrature, temporal sampling, coefficient
normalization, line metric, and residual norm. It will refine retained
harmonics, temporal samples, radial mesh, outer wall, and solver tolerance
independently, and will distinguish coefficient stability from radiative-tail
wall stability. Mutations will break half-period symmetry, the kinetic half,
potential sign or evenness, time-derivative omega factor, Fourier factor two,
radial measure, phase origin, and spherical STF projection. An independently
implemented analytic convolution or high-order quadrature transform will
rederive the load-bearing line coefficients. Candidate C, if needed, must add
regular-origin, PDE, time-resolution, domain, energy, solver-status, and
independent-method gates rather than inherit Candidate B's scalar evidence.

## Attempts and Continuation

Seven append-only attempts complete the campaign. Attempt 0001 reproduces
QB2's five checks and diagnoses its standalone branch, incomplete coefficient,
false purity oracle, and scalar/STF conflation. Attempts 0002 and 0004 build
and refine Candidate B; attempt 0003 preserves an exact-cutoff grid-alignment
failure. Attempt 0005 preserves an unjustified absolute odd-bin quadrature
threshold. Attempt 0006 repairs it through 96/192/384-node convergence and a
scale-relative roundoff model while retaining the exact null separately.
Attempt 0007 passes the 38-check primary theorem, spectrum, refinement,
mutation, wall, and source-adjudication verifier. Candidate C is not opened:
the requested positive scalar object is complete, while a nonzero STF source
would be a separate nonspherical claim rather than a repair to Candidate B.

## Debt Ledger

This ledger tracks source reproduction, energy and transform normalization,
observable identity, symmetry, finite-box spectrum, residual and tail effects,
moment and radiation interpretation, independent evidence, consumers, and
canonical state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| QB2's literal field, observable, transform, threshold, and current-environment behavior are unaudited | Hash-check, run, and preserve its complete result or failure | discharged by attempt 0001 and source reproduction |
| No canonical energy-spectrum API consumes the harmonic branch | Implement pure derivative, energy-density, radial-observable, and Fourier-coefficient APIs with tests | discharged by the radial harmonic observable module and focused tests |
| Exact even-harmonic selection may be conflated with a dominant or nonzero 2*omega line | Derive the selection rule and supply zero or cancellation counterexamples separately from numerical amplitude evidence | discharged by C-PDE-007 and both verifiers |
| Finite-box line stability and truncation error are unknown | Refine harmonics, time samples, radial quadrature, wall, and tolerance and compare with the nonlinear remainder and radiative tail | discharged by attempts 0002, 0004, 0006, and 0007 |
| A radial scalar line may be mislabeled as an STF radiating line | Apply C-MOM-003 and audit any nonspherical construction against C-PDE-003 regularity and conditional gravity ceilings | discharged by the exact STF null and QB2 qualification |
| Consumers and generated state are unreplayed | Complete impact analysis, targeted consumers, one final repository gate, and queue regeneration | discharged by the P053 impact review and promotion transaction |

## Review and Promotion Plan

Exact selection and any numerical finite-box spectrum receive separate
four-axis claim reviews from raw source, mutation, refinement, and independent-
transform artifacts. Accepted reusable logic moves under
`src/substrate_framework/` with focused tests. QB2 receives a structured
terminal disposition in `migration/dispositions.yaml`, preserving every
unaccepted radiation, periodicity, frequency, and ontology subclaim. Promotion
requires registry and release closure, generated docs and accepted memory,
affected-consumer replay, one final `scripts/validate.sh`, and `git diff
--check`.

## Done Gate

P053 is accepted. The positive importable energy-spectrum object, exact
selection theorem, qualified finite-box coefficient, source adjudication,
sensitive exact and numerical oracles, refinements, independent normalization,
claim-level reviews, consumer replay, terminal QB2 disposition, synchronized
canonical transaction, and empty campaign debt ledger pass. The parent
migration remains active and continues to QB3.
