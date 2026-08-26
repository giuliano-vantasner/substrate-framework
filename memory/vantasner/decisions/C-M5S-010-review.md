---
description: Constructive review of C-M5S-010
author: ox-alpha
reviewer_session: 'omp task subagent Reviewer244; parent session 01a03a51-b156-70ab-99a6-6977b6c63609 (started 2026-08-25T19:07:07Z, review duration 7m16s); transcript history://Reviewer244'
created: '2026-08-25T20:55:00Z'
updated: '2026-08-25T20:55:00Z'
tags:
- substrate-framework
- claim-review
- P244
- confined-clock-spectrum
category: decisions
confidence: working
status: active
---
# Review of C-M5S-010

## Claim and Positive Role

The proposed statement certifies the full-band kinetic-normalized fluctuation
spectrum of the confined-clock sector. About the frozen committed R=12 family-S
window root (order-16 basis, coefficient data read read-only from
`proposals/P240-m5-kinetic-axis/attempts/0042/largeR-roots.json`), the
kinetic-normalized pencil (H, M) — H the autograd-exact static energy Hessian,
M the exact-quadratic kinetic metric with the corrected per-cell reduction — is
certified across all 32 kinetically non-singular modes (48 modal directions
minus the 16-dimensional exact tangent-null family) by two independent
quadrature families applied to verbatim committed constructions:
Gauss-Legendre 96x48 versus interior second-kind Chebyshev 160x80 with solved
polynomial-exactness weights. The useful framework question it answers is
C-M5S-009's named missing construction (the certified complete spectrum table)
and issue #170 frontier item 2: whether any infrared propagating mode survives
about the window background at adjudicable resolution. The answer is no:
omega_min = 1.046406, so every certified frequency is O(1) or larger and the
census multiplicity N=3 of C-M5S-001 is unaffected at frequency level. This is
a meaningful positive object, not a restated definition.

## Frozen Transaction

Base/head: main tip `dbf44fa80f3616f061f44147dcb2832fe7adb316` (release
v0.165.0), working tree adds only the untracked proposal directory
`proposals/P244-clock-full-band-spectrum/` and its prose-contract memory file.
Claim delta: one new claim C-M5S-010 (numeric_evidence). Changed evidence
records: append-only attempts 0001..0008 under the proposal directory, with the
registered artifact `attempts/0008/spectrum-table-final.json` and verdict
`attempts/0008/final-verdict.json`. Accepted dependency propositions actually
used: C-M5S-006 (root provenance for R=12 family-S with s_b =
2.982251210281484, artifact-adjudication protocol) and, via C-M5S-009's blocked
half, the named missing construction. Committed infrastructure consumed
read-only: P243-0008 `kinetic_stage2.py` (with its documented reduction defect),
P240-0041 `cpu_energy.py`/`solve_radial_1d.py`, P240-0042 roots. Affected
consumers inside the boundary: C-M5S-011 (proposed, same transaction), issue
#170 item 2. Existing validation receipt: none yet; this review precedes
promotion, and each attempt carries first-execution captured stdout plus verdict
JSON as its own record. Unchanged accepted dependencies (C-M5S-001/002/007/008)
and adjacent corpus records are outside this review.

## Strongest Supported Positive Statement

Stronger than a bare gate tally, and fully supported by the artifacts: every
one of the 32 kinetically non-singular modes about the frozen R=12 family-S
root carries a certified frequency with an itemized budget
sigma_i = max(float64 entry jitter, cross-family pencil spread), each satisfying
omega_i >= 10*sigma_i, where the two quadrature families share no node set and
no weight rule while keeping every other construction byte-identical. All 32
certified modes are stiff-band (stiffness Rayleigh in [1.09497, 305.534], i.e.
>= ~1.09 = 0.367*s_b decades above the soft/mid cut); the soft and mid bands
are empty at certification resolution, omega_min = 1.046406, and therefore no
infrared propagating fluctuation exists about the window root at adjudicable
resolution. This is exactly the proposed scope; no narrowing is warranted, and
none is needed. The only inaccuracy found is one attached numeral, corrected
under Findings.

## Evidence Map

The evidence groups below are classified once each; no attachment is credited
beyond the proposition it actually establishes.

| Evidence | Proposition established | Role: exact proof / corroborating subclaim / regression / applicability / provenance | Bridge to claim | Limit |
| --- | --- | --- | --- | --- |
| attempts/0008/spectrum-table-final.json + final-verdict.json (4/4) | Registered artifact: 32 rows, all certified_margin_ok, band stiff, budgets, zero-point composition | corroborating subclaim | The certified table itself, with per-mode sigma from jitter and cross-family spread | float64 numeric evidence; not exact |
| attempts/0007/stdout-g6-final.txt + final-certified-result.json | Cross-family measurement: H entries 4.508e-07 rel, M entries 3.147e-14 rel, pencil 1.037e-07 rel, delta-E replicates to 9.06e-10 rel; H-floor mechanism named (algebraic pole content of azimuthal channel densities) | corroborating subclaim | Independent-discretization agreement at declared scale-relative tolerance; M machine-exact | G6 preregistered 1e-13 H-entry hypothesis refuted-as-hypothesis and recorded; Chebyshev-family G0B energy transfer 3.912e-06 failed its own strict check (see Findings) |
| attempts/0002/route-a-corrected-verdict.json + attempts/0004 rungs | Corrected per-cell reduction converges: entry drifts fall to 1.43e-15 (H) / 1.54e-15 (M); energy transfer <= 7.4694e-12 at every GL ladder rung; symmetry defects ~1e-16 < 1e-12; M PSD defect ~1.6e-17 < 1e-11 | regression | Gates G0/G1 on route A across the refinement ladder | Route A only; does not bound family B' transfer |
| attempts/0001/diag-bugid.txt + stdout-route-a.txt | Reduction-defect identity: committed T == 4*(sum w)*(sum rho) = 2.3421812502e+04 exactly, while correct per-cell value is 2.9918291132e+01 | provenance | Justifies the "corrected per-cell reduction" premise without editing P243 canon | Diagnostic only; positive-scalar scaling argument for unaffected stage-2 verdicts lives in the prose contract |
| attempts/0003/certified-table-verdict.json (6/7, global-normalizer sensitivity flaw recorded) | Repaired mp congruence via Z^T H Z with L Z = I; all 32 modes certified pre-budget-revision | regression | Intermediate repair step en route to 0008 | Superseded by 0008 budgets |
| attempts/0004/final-verdict.json (7/7) + spectrum-table.json | Mutation moves the pencil (max shift 4.43e-04 on single-coefficient mutation); R10-root change shifts some mode relatively more than 10% (max 0.2528, 4 modes beyond 10%) | regression | Load-bearing input mutations fail the checks, excluding a false green | Scale-free form of the R10 gate introduced here after 0003's normalizer-dependent form failed honestly |
| attempts/0005/, 0006/ FD ladders | FD radial route floors near median 4 percent regardless of stencil order | applicability | Demotes FD to supplementary consistency; justifies Chebyshev rule injection as the second family | Not load-bearing for the certified numbers |

## Oracle Audit

The strongest practical oracle is the attempt-0008 registered run: identical
committed constructions evaluated under two quadrature families differing only
in node set and weight rule, with gates frozen before any route-B number
existed (manifest `comparators_blinded_until`). Audited facts: (i) the
zero-point machinery uses math.fsum over certified rows only — recomputed
independently from `spectrum-table-final.json`: fsum over the 32 certified rows
gives 72.58859645998888, matching the verdict bit-for-bit, and the RSS budget
recomputes to 3.8507623645951665e-07 exactly; (ii) cross-family numbers match
the claim text: max pencil rel diff 1.0371137873931903e-07 <= 1.04e-07, H-entry
4.508430649983332e-07 <= 4.6e-07, M-entry 3.1472586074135847e-14 <= 3.2e-14;
(iii) band structure: no row labeled soft or mid, min stiffness Rayleigh
1.0949654830201405 >= ~1.09, consistent with omega_min = 1.04640598384407;
(iv) mutation and R10 sensitivity numbers in final-verdict.json reproduce the
claim's requirements (pencil moves; r10_max_relative_shift 0.2528 > 0.1 with 4
modes beyond 10 percent); (v) certification margin G5 passes with empty
uncertified list. Solver/error facts are recorded per AGENTS.md numerics
discipline (pinned threads, float64, declared tolerances, scale-relative
thresholds).

## Findings

Findings are classified once each against the blocking test of AGENTS.md
(counterexample or contradiction, absent/circular load-bearing step,
dependency not supplying what is used, affected-consumer failure); everything
else is recorded once as follow-up.

| Finding | Direct evidence | Blocking in boundary / minimum correction / follow-up | What would resolve or overturn it |
| --- | --- | --- | --- |
| F1: The quoted uncertainty "omega_min = 1.046406 plus minus 3.9e-08" is unsupported by the registered artifact. Table mode 0 carries sigma_omega = 2.12027173596141e-09 (cross-family spread 1.94e-09 absolute, jitter 8.0e-10); no artifact attaches 3.9e-08 to omega_min. Nearest figures are delta-E budgets (0004 RSS half 3.74e-08; prose "plus minus 3.9e-7"). | spectrum-table-final.json row 0 vs claim text | minimum correction (in place): state omega_min = 1.046406 with its artifact-backed budget sigma_omega(mode 0) = 2.1e-09, 10-sigma margin satisfied a fortiori; or drop the numeral and cite the table row | Registry entry quoting the table value resolves it; a future artifact showing a larger min-mode budget would overturn |
| F2: The energy-transfer figure "<= 7.5e-12 relative against the committed energy at every ladder rung" was measured on the Gauss-Legendre route-A ladder only (rungs 48x24..96x48: 0, 7.466e-12, 7.469e-12, 7.467e-12). The Chebyshev family B' has G0B energy transfer 3.912e-06 relative, which failed its own preregistered check in attempt 0007 and is disclosed only in the attempt docstring, not in the claim's exclusions. | 0004/0002 rungs vs 0007 final-certified-result.json G0B | minimum correction (in place): scope the 7.5e-12 sentence to the route-A refinement ladder and add to the exclusions that the Chebyshev family's internal energy-transfer check measured 3.9e-06 with its recorded pole-content mechanism; the physics conclusion is untouched because family B' enters the claim through pencil/delta-E agreement (1.04e-07 / 9.1e-10), not through its raw-energy transfer | A registry wording carrying both scoping and the B' number closes it; a mechanism showing B' transfer contaminating certified frequencies would escalate it to blocking |
| F3: Attempt 0002's budget head lists soft/mid candidates (stiffness down to 7.45e-05, uncertified_count 32) that vanish in the registered table (all stiff). This is the recorded wrong-mp-congruence defect population, correctly superseded; noted once so later readers do not read the two tables as contradictory. | 0002 budget_head vs 0008 table | follow-up (documentation provenance already adequate in attempt docstrings) | Nothing further required; already resolved by the 0003 congruence repair |

No finding demonstrates a counterexample, an absent or circular load-bearing
step, an undeclared dependency gap, or a failed affected consumer; none blocks.
No prior review of this claim narrowed its scope, so no recursive-weakening
escalation applies.

## Compatibility and Consumers

Assumptions are explicit and honored: frozen background never re-solved;
committed functional conventions verbatim; tangent channel deflated analytically
as the exact 16-dimensional kinetic null (kept 32 of 48, dropped 16);
kappa projector-current term excluded with its bias toward STATIC classification
recorded; de-boxed tail out of scope; no fitted constants; Route-2 no-go
respected. C-M5S-006 is not contradicted: its declared soft omega^2 values stay
uncertified there, and this campaign certifies frequencies, not the old
stiffness-artifact question; the empty soft band independently reinforces its
no-fourth-species verdict at frequency level. Consumer replay inside the
boundary: C-M5S-011 consumes exactly the certified rows and reproduces their
sum (audited under the C-M5S-011 review); issue #170 item 2 is the named
external consumer and receives the certified result at promotion. No defect is
introduced inside this transaction.

## Four-Axis Decision

The decision is stated without inflating one axis from another.

- Verification: numeric_evidence (proposed -> audited)
- Review: audited
- Compatibility: native
- Epistemic: active
- Relationship: depends on C-M5S-006; feeds C-M5S-011 and issue #170 item 2; challenges and supersedes none
- Strongest accepted or proposed statement: all 32 kinetically non-singular modes about the frozen R=12 family-S window root certified by two independent quadrature families at omega >= 10 sigma with itemized budgets; soft and mid bands empty; omega_min = 1.046406; no infrared propagating fluctuation exists about the window root at adjudicable resolution.

## Promotion Transaction

Registry entry for C-M5S-010 incorporating corrections F1 and F2 verbatim;
release-manifest addition pinning this claim set at the current base commit;
rendered documentation regeneration via scripts/render_docs.py; memory
synchronization from the registry; scoped validation receipt covering the new
proposal artifacts and registry/docs/memory diff. No implementation or test
changes are required by this claim beyond what the attempts already contain.

## Correction Check

Not needed (no correction requested before this review; F1/F2 are named
minimum corrections carried into promotion, not post-correction re-audit
items).

## Result and Frontier

The positive result stands in full proposed scope: the certified full-band
kinetic-normalized spectrum table exists, is registered, survives independent
recomputation, and answers the framework question — the window background
carries no infrared propagating mode at adjudicable resolution. Accepted with
two minimum wording corrections (F1 uncertainty numeral, F2 energy-transfer
scoping plus B' disclosure), neither of which weakens scope. Frontier remains
as declared: whether a genuinely de-boxed realization exists (issue #170 item
3) is outside this transaction and stays open.

## Cross-References

Proposal `proposals/P244-clock-full-band-spectrum/proposal.yaml` and prose
contract `memory/vantasner/proposals/P244-clock-full-band-spectrum.md`;
registered evidence `proposals/P244-clock-full-band-spectrum/attempts/0008/`
(spectrum-table-final.json, final-verdict.json, stdout-final.txt,
H96corr.npy/M96corr.npy) with the 0001..0007 defect-and-repair ladder;
dependencies governance/claims.yaml C-M5S-006 (~line 12671) and C-M5S-009
(~line 12862); committed infrastructure proposals/P240-m5-kinetic-axis
attempts 0041/0042; consumers C-M5S-011 (see C-M5S-011-review.md) and issue
#170 items 2-3.
