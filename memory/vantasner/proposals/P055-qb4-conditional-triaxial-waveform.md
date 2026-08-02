---
description: Audit QB4 through convention-safe conditional triaxial waveform and temporal-rank algebra
author: vantasner
created: '2026-08-02T08:38:12Z'
updated: '2026-08-02T13:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- conditional-radiation
- migration-QB4
category: proposals
confidence: established
status: archived
---
# P055 QB4 Conditional Triaxial Waveform Audit

## Question and Positive Deliverable

P055 must produce the strongest positive, reusable waveform and power object
naturally supported by the accepted real-l2 STF map. It must keep physical
radiation conditional, keep the normalized/triple moment conversion explicit,
and distinguish two TT basis coordinates from two independent temporal source
modes. If QB4's inherited source or two-mode interpretation fails, that failure
is preserved while Candidates B through D continue to an exact positive
theorem.

## Base Release and Provenance

The accepted base is `v0.48.0` at framework commit `93e6718`; its scientific
transaction is `f27e2cd`. QB4 is pending at `substrate@6d1f4e0`, path
`merged-framework/bridges/phase-16/bridge_QB4_two_polarization_waveform.py`,
SHA-256 `4523ad68636413bf628cd353e496c61b25af3c7f30bdf3e1e061930054fb9291`.
Its cited GW2, GW3, M2, P3D1, P3D3, P3D4, QB1, QB2, and QB3 results are
navigation evidence only; authority enters through accepted claim mappings.
Memory identifies prospective convention, source, and temporal-rank hazards
but no accepted QB4 result. The executable and all QB4 reported values remain
unopened until this contract is frozen.

## Invariants, Conventions, and Allowed Imports

Write `Q_s=s I_STF`, where `I_STF` is the normalized moment of C-MOM-001 and
the real-l2 map of C-GW-007 uses the triple convention `s=3`. Under the
conditional C-GW-001 premises, the exact tensor formulas must therefore keep
`h R/G=(2/s) TT(Q_s'')` and `P/G=||Q_s'''||_F^2/(5 s^2)` rather than silently
using the normalized coefficient for a triple tensor. C-GW-002 supplies the
two-dimensional transverse STF basis, not a count of independent time traces
or quanta.

C-GW-007 fixes a rank-one counterexample: `Q_s(t)=q(t)T` for one constant STF
tensor. Any plus/cross pair obtained by changing sightline or transverse basis
is then proportional to the same `q''(t)` and can be rotated to a frame with
one zero coordinate. Two-mode or elliptical behavior requires two independent
coefficient traces, not merely a triaxial shape or generic observer. C-PDE-009
and the QB3 disposition provide no accepted localized Floquet eigenmode or
finite-deformation source. No QB3 eigenvalue, amplitude, width, or QB4 output
may enter the derivation.

## Candidate Preregistration

The candidate set is frozen from queue metadata and accepted structure before
the source implementation is opened.

| Candidate | Construction | New assumptions and parameters | Natural-fit prediction | Decisive oracle |
| --- | --- | --- | --- | --- |
| A | Literal QB4 tensor, differentiation, power, sightline, and classifier | Every inherited QB3 datum, source premise, scale, timestep, and frame must be declared | May reproduce printed values but can fail convention, provenance, convergence, or rank | Hash-pinned run, dependency trace, symbolic scale substitution, timestep refinement, frame rotations, and rank counterexamples |
| B | Exact conditional arbitrary-STF waveform and total power with `Q_s=s I_STF` | Symbolic `s`, `G`, and `R`; no source amplitude | Supplies a convention-safe reusable map and independently fixes the factor of nine between normalized and triple power | Tensor contraction, TT angular integral, dimensional checks, `s=1,3` mutations, and independent rederivation from C-GW-001 |
| C | Fixed-orientation theorem `Q_s=qT` | One scalar trace and one constant nonzero STF tensor | Generic plus/cross coordinates are proportional and linearly polarized; coordinate rotation sets cross to zero | Exact projection and spin-2 rotation, coefficient-matrix rank, proportional/wrong-phase mutations, and principal/nodal limits |
| D | Two-component real-m2 comparison `Q_3=q_c T_c+q_s T_s` | Two declared coefficient traces; dynamics remains unspecified | Rank two occurs exactly when the traces are independent; equal quadrature gives circular polarization along the natural axis | Exact tensor norms, waveform/power map, determinant or SVD rank, zero/proportional/quadrature limits, and independent Cartesian calculation |

## Selection Criteria and Blinding

Selection is ordered by moment-scale closure, temporal-rank honesty,
compatibility with conditional radiation premises, independence from rejected
QB3 data, exact frame and symmetry limits, numerical derivative convergence
where needed, source and boundary honesty, assumption economy, and an
independent normalization derivation. Numerical similarity to QB4's reported
power, amplitude, phase, or polarization labels cannot select the concept.
The comparator gate opens only after the symbolic scale, tensor basis,
readouts, power coefficient, rank metric, frame law, derivative gates, and
interpretation ceiling are frozen here and in the manifest.

## Proposed Claim Delta

Provisional `C-GW-008` may state the exact conditional waveform and power map
for a scaled STF quadrupole and specialize it to the real-m2 cosine/sine basis.
For the triple convention, a pure cosine tensor `diag(q,-q,0)` has
`P/G=2(q''')^2/45`; a general natural-axis pair has
`h_+R/G=2q_c''/3`, `h_xR/G=2q_s''/3`, and
`P/G=2[(q_c''')^2+(q_s''')^2]/45`. It may also state that a fixed tensor times
one trace remains rank one in every frame and is linearly polarized despite
two generic nonzero coordinates. A quadrature rank-two comparison is a
conditional kinematic construction, not evidence that accepted scalar
dynamics produces two modes or physical gravitons.

Direct consumers are QB4 and later bridge units that cite its waveform or
graviton language. C-GW-001, C-GW-002, and C-GW-007 remain unchanged and
authoritative; this proposal can only specialize their exact conditional
algebra.

## Implementation and Oracle Plan

A canonical pure module may expose quadrupole-scale-safe waveform and power
coefficients, real-m2 tensor assembly, fixed-orientation rank classification,
and two-trace comparison without simulations or printing at import. Existing
TT and triaxial-l2 APIs are reused after impact analysis. Exact SymPy and
Cartesian tensor algebra fit all promoted obligations; NumPy is limited to
source reproduction, derivative convergence, SVD rank evidence, and
counterexamples.

Load-bearing mutations change `s=3` to `s=1`, remove one factor of `s`, replace
the Frobenius contraction by a single component, alter TT basis normalization,
rotate the transverse frame, make two traces proportional, shift them to
quadrature, or replace `np.trapezoid` by the version-dependent legacy spelling.
The canonical implementation uses `np.trapezoid` with a narrowly scoped
fallback only if compatibility with an older supported NumPy is intentionally
required; a printed tally cannot substitute for an oracle-sensitive failure.

## Attempts and Continuation

Seven append-only attempts complete P055's scientific transaction. Attempt
0001 preserves the initial source-root path failure, resolves the pinned
checkout, and reproduces `ALL 5 CHECKS PASS`. Attempt 0002 rejects the headline
through the nonperiodic FFT window, 4.17-percent twice-frequency fraction,
factor-nine convention error, and missing temporal-rank/ellipse oracle while
recording the literal finite-b array's small second direction. Attempt 0003
passes 21 exact scaled-STF, real-m2, frame, rank, linear, and circular checks.
Attempt 0004 independently passes 23 Cartesian/sphere checks without the
primary reducers. Attempt 0005 passes the 25-check promotion verifier and 68
targeted consumer tests against the assembled v0.49.0 transaction. Attempt
0006 preserves the first repository gate's missing plain-prose debt-ledger
disclosure; its schema-only repair changes no scientific or governance result.
Attempt 0007 passes the repaired complete workflow, all 407 tests both inside
the workflow and in the separately required replay, and the whitespace gate.

## Debt Ledger

This ledger tracks source provenance, convention closure, polarization rank,
numerical differentiation, conditional interpretation, independent evidence,
consumer replay, and canonical synchronization.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| QB4's literal source, dependencies, current-environment behavior, and tally are unaudited | Hash-check, run, and preserve complete output or failure | discharged by attempt 0001 and source reproduction |
| The normalized/triple moment scale may be mixed in waveform or power | Derive with symbolic `s`, specialize `s=1,3`, mutate the scale, and independently rederive | discharged by C-GW-008 and attempts 0003/0004 |
| Generic nonzero plus/cross coordinates may be mislabeled as two temporal modes or elliptical polarization | Exact fixed-tensor proof, frame rotation, rank metric, and proportional/quadrature counterexamples | discharged by C-GW-008 and both exact verifiers |
| QB4 may inherit a rejected QB3 localized eigenmode or finite deformation | Trace every input to accepted claims and exclude unsupported data from promoted objects | discharged by the source review and QB4 qualification |
| Numerical derivatives, integration APIs, or spectral labels may be version- or resolution-sensitive | Record environment, use current `np.trapezoid` policy, refine timestep/tolerances, and mutate estimator inputs | discharged by attempt 0002's structural periodicity rejection and compatibility audit; no numerical source claim is promoted |
| Conditional radiation premises may be narrated as derived scalar gravity or a graviton count | Review conservation, localization, far-zone, flux, and interpretation ceilings claim by claim | discharged by the C-GW-008 review and QB4 disposition |
| Independent exact evidence and consumer replay are absent | Complete a separate Cartesian derivation, targeted tests, impact replay, and one final repository gate | discharged by attempts 0004/0005, low-risk graph detection, and the final workflow gate |
| Registry, release, generated docs, migration queue, and durable memory are unsynchronized | Promote only reviewed claims, regenerate canonical consumers, and empty this ledger | discharged by v0.49.0, rendered state, and the regenerated qualified queue |

## Review and Promotion Plan

Each proposed subclaim receives separate verification, review, compatibility,
and epistemic axes. Accepted definitions move under `src/substrate_framework/`
with focused tests. QB4 receives a structured terminal disposition in
`migration/dispositions.yaml`; `migration/source-claims.yaml` is generated.
Promotion requires a pinned release if claims change, generated docs and
accepted memory, affected-consumer replay, one final `scripts/validate.sh`,
`.venv/bin/python -m pytest`, `git diff --check`, and an empty campaign ledger.

## Done Gate

P055 is accepted in v0.49.0. The positive convention-safe scaled-STF and
real-m2 theorem, independent sphere oracle, fixed-rank and quadrature
counterexamples, qualified QB4 disposition, consumer replay, canonical
synchronization, and empty campaign debt all pass. The parent migration
remains active and advances to WZ1.
