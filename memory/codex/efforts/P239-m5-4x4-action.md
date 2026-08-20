---
description: Resolve issue 147 with a promoted local Lorentz-covariant M5 4x4 action
author: codex
created: '2026-08-20T11:06:43+02:00'
updated: '2026-08-20T18:40:00+02:00'
tags:
- substrate-framework
- research-arc
- m5
- issue-147
category: efforts
confidence: exploratory
status: active
---

## Positive Objective and Success

Resolve #147 by selecting one explicit local Lorentz-covariant M5 4x4 action
which retains the spatial 3x3 and Coulomb sectors, has a finite nonzero
fixed-angular-momentum electron-hedgehog frequency, and produces an attractive
inverse-square interaction between fully relaxed mass defects. Completion
requires C-M5-001 through C-M5-004 to pass their exact/numeric oracles,
individual review, accepted dependency closure, impact replay, importable
implementation, registry and release promotion, generated docs and memory
synchronization, and an empty in-boundary debt ledger.

## Authority and Prior Work

Authority starts at accepted release `v0.163.0`, source baseline
`6e5a4ba001bfdb41ea6e5157a43b0a854d118e1a`.

- Accepted claims reused: C-LOR-002, C-KRN-001, C-VAR-003, C-IGR-004, C-GRV-002; C-GSK-001 is structural precedent only.
- Source modules read: `lorentz_little_groups.py`, `lorentz_orbits.py`, `variational.py`, `numerics.py`, `verification.py`, and `total_gravitational_coupling.py`; further exact M5 source reading follows the validated freeze.
- Memory searches: M5 4x4/Lorentz/finite omega/Newton/Coulomb; exact C-IGR-004 and C-GRV-002 grep; P236 corrective-review memory.
- Campaign evidence: immutable P236 plus its reopened issue and corrective branch; public OpenWave M5.21.14-16 at pinned commits.
- Genuine unresolved objective: no accepted claim or canonical module supplies the complete M5 action or any of the four P239 conclusions.

## Definitions and Invariants

The exact source tensor definitions will be copied into a hashed source freeze
before candidate evaluation. The immutable conventions already fixed are
mostly-plus `eta=diag(-1,1,1,1)`, local Lorentz-scalar action terms, one common
action/admissible space/boundary set for all relaxed sectors, direct relaxed
energy differences for interactions, and fixed nonzero angular momentum for
frequency selection. The spatial restriction must recover the audited 3x3
functional without coefficient reinterpretation. Numerical work will freeze
binary precision, discretization, domain, boundary data, residual norm, energy
scale, refinement ladders, and stopping rules before production values open.

## Permitted Imports and Assumptions

Permitted inputs are exactly those in the P239 manifest. Pinned OpenWave
equations and Jarek Duda's direction are approved proposal imports but are not
accepted framework authority. C-IGR-004 supplies a conditional coupling and no
unique number. C-GRV-002 supplies its exact sign regimes and no sourced M5
geometry. A fixed-J state constraint is explicit and not a hidden free-omega
claim.

## Candidate Set

Four local mechanisms remain live until structural selection.

| Candidate | Construction | New objects/parameters | Natural-fit case | Expected falsifier | Status |
| --- | --- | --- | --- | --- | --- |
| A | Complete quadratic contraction basis | Independent ratios after overall normalization | Same derivative order and Lorentz covariance | Empty simultaneous sign/boundedness region | rejected: exact 3x3-preserving nullspace vanishes on a negative symmetric-derivative clock witness |
| B | A plus minimal quartic stabilizer | One local higher-order coefficient | Bounds time mixing while preserving infrared sectors | Alters 3x3/Coulomb coefficient or remains noncoercive | untested |
| C | A plus sextic and spectral-potential terms | Minimum sextic/potential coefficients | Supplies scale and regular core | Extra parameters fail exact selection or tails become massive | untested |
| D | Local auxiliary mediator with exact elimination | Minimal auxiliary kernel/coupling | Explicit exchange sign and common frequency channel | Nonlocal elimination, fitted kernel, or new untyped field | untested |
| E | M-derived spectral-Cartan internal metric | No new field; simple real timelike eigenline continuously connected to the vacuum g branch | Covariant version of the healthy Frobenius contraction | Projector loses its isolated timelike branch or relaxed branches miss the frequency/force gates | selected for stationary testing: exact action gates pass |
| F | E plus `-kappa eta^munu q(partial_mu P_t,partial_nu P_t)` | One positive projector stiffness; no new field | Supplies the absent boost-sector quadratic kernel and Derrick `R` term while remaining exactly inactive in 3x3 | Fails covariance/positivity, projector branch, stationary branch, or relaxed force gates | registered; structural scaling attempt next |

## Selection Criteria and Comparator Gate

Selection is ordered by Lorentz/index validity, bounded regular stationarity,
exact 3x3/charge recovery, common explanatory reach, assumption/parameter
economy, dimensions/topology/limits, accepted-sector composition, numerical
robustness, then empirical comparison. Prior issue/OpenWave values were public
before the campaign and cannot be blinded retroactively; no new P239 output is
opened until the basis, reductions, coefficient domains, solver, thresholds,
and mutations freeze.

## Claim Delta

The campaign proposes four new leaf claims and changes no accepted statement.

| Claim id | Exact statement | Dependencies | Relationship | Oracle | Consumers |
| --- | --- | --- | --- | --- | --- |
| C-M5-001 | Selected local 4x4 action, complete basis, exact E-L equations and sector reductions, bounded fixed-J domain | approved M5 source, C-LOR-002 convention | additive | SymPy plus independent explicit components | all P239 claims and APIs |
| C-M5-002 | Regular relaxed fixed-J hedgehog has finite nonzero strict-minimum omega | C-M5-001 | additive | exact derivative/Hessian plus refined SciPy and independent solver | electron branch API |
| C-M5-003 | Relaxed charges have positive-coefficient 1/r Coulomb tail | C-M5-001, C-KRN-001, C-VAR-003 | additive | exact IR kernel plus refined relaxed pairs | charge interaction API |
| C-M5-004 | Relaxed masses have negative-coefficient 1/r Newton tail and typed conditional coupling bridge | C-M5-001, C-KRN-001, C-VAR-003, C-IGR-004, C-GRV-002 | additive | exact IR sign plus refined relaxed pairs and independent representation | mass interaction API |

## Frozen Review Transaction

The eventual promotion transaction is limited to the four new claim entries,
new P239 implementation/evidence/reviews, their direct consumers and tests,
the new release, generated docs, and synchronized accepted memory. Existing
accepted statements and P236 artifacts remain unchanged. The base is
`6e5a4ba001bfdb41ea6e5157a43b0a854d118e1a`; the head/tree and one final
receipt will be recorded after the last correction.

## Claim Ladder

The ladder moves from exact structure to unresolved numerical branches.

| Step | Claim | Oracle | Sensitivity/counterexample | Prerequisites | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Complete invariant basis and exact reductions | SymPy tensor identities plus explicit-component reconstruction | signature flip, omitted trace, index permutation | source freeze | complete: 41/41, six even plus four odd invariants, spatial nullspace, and clock no-go |
| 2 | Bounded fixed-J coefficient domain | exact polynomial/inequality and scaling analysis | replace M-derived Cartan metric by fixed Euclidean metric; wrong kinetic sign | step 1 | complete at action level: 23/23 exact checks plus 6 unit tests; branch existence remains step 3 |
| 3 | Finite nonzero hedgehog branch | exact fixed-J stationarity plus SciPy BVP/refinement and second method | J=0, sign flip, boundary mutation | steps 1-2 | pending |
| 4 | Coulomb tail | exact massless IR kernel plus relaxed pair simulation/refinement | source deletion and charge sign mutation | steps 1-2 | pending |
| 5 | Newton tail and coupling bridge | exact boost IR sign plus relaxed pair simulation/refinement and independent representation | source deletion, boost sign, coupling-branch mutation | steps 1-4 | pending |

## Importable Implementation

Planned modules are `src/substrate_framework/m5_covariant_action.py` for pure
tensor/action/reduction APIs and `m5_stationary_fields.py` for claim-owned
stationary equations and solver wrappers. Shared SciPy evidence and
`trapezoid_integral` come from `numerics`; check reporting comes from
`verification`. The exact operator, boundary data, meshes, tolerances, and
norms are frozen in P239 evidence before production. No import executes a
simulation.

## Harvest Checkpoints

Issue #147 is the canonical goal and PRs use `Advances #147` until every
promotion gate passes.

- Canonical goal issue: https://github.com/vantasnerdan/substrate-framework/issues/147
- PR issue reference: `Advances #147` until complete; `Fixes #147` only for final promotion.
- Source PR lifecycle: no PR yet.
- Refactor owner/handoff, live PR, and landing test: codex owns the isolated P239 branch; distinct merger required by default.
- Terminal-close evidence: not applicable.
- Final issue handoff: pending.

| Unit | Local claim | Independent of headline? | Evidence | Commit/PR | Disposition |
| --- | --- | --- | --- | --- | --- |
| Source and invariant basis ledger | Exact tensor definitions, contraction independence, and Candidate-A no-go | yes | attempt 0001, 41/41 | pending | ready for focused harvest if the headline later stalls |
| Spectral-Cartan action API | Conditional local Lorentz scalar, positive Hamiltonian, exact 3x3 reduction | yes, with explicit simple-timelike-branch hypothesis | attempt 0002, 23/23; unit tests 6/6 | pending | active, stationary applicability not yet established |

## Attempts

The first attempt starts only after schema and memory validation.

| Attempt | Candidate/method | Artifact | Verdict | Diagnosed layer | Next materially different route |
| --- | --- | --- | --- | --- | --- |
| 0001 | Wave-0 source/invariant reconstruction and Candidate A | `proposals/P239-m5-4x4-action/attempts/0001/` | six even/four odd basis complete; A rejected | candidate concept | covariant spectral-Cartan contraction |
| 0002 | Candidate E spectral-Cartan contraction | `proposals/P239-m5-4x4-action/attempts/0002/` | exact local action gates pass conditionally on the simple timelike branch | candidate concept repaired | derive E-L/stationary reduction and solve fixed-J branch |

## Framework-Fit Audit

The source freeze and quadratic-basis audit are complete. Candidate A preserves
the 3x3 sector only through three exact null combinations, and all three vanish
on an explicit negative clock direction generated by symmetric M5 field
derivatives, so A fails boundedness without any comparator. Candidate E uses
M's own timelike spectral projector and no external preferred vector. On the
simple timelike branch its inverse Cartan metric is positive, follows M under
Lorentz transformations, recovers the internal Frobenius metric in the vacuum
frame, and makes the Hamiltonian nonnegative. Exact tests also recover the
full spatial action coefficient and reject the fixed-Frobenius mutation.
Candidate E alone still has no quadratic operator around the vacuum orbit:
`F=[partial M,partial M]` begins at second order, `F^2` at fourth order, and
its three-dimensional static energy scales as `1/R`. Candidate F adds the
minimum projector current. It is exactly zero for uniform-time-row fields,
but its boost energy scales as `R` and its linearized equation is Laplace.
The remaining framework-fit question is applicability: relaxed hedgehog and
pair solutions must stay on the simple timelike branch and pass the full
force/frequency gates. A candidate conflict is diagnosed before any
foundational revision is considered.

## Verifier Audit

Attempt 0001 executes 41 exact checks and records its own terminal tally;
attempt 0002 executes 23 exact checks and the canonical module has six unit
tests. The load-bearing mutation replaces the M-derived Cartan metric by a
fixed Euclidean metric and correctly breaks boost covariance. A separate
source-admissible clock witness changes from negative to positive coefficient.
These establish action structure only. Numerical branches still require
solver success, scale-relative residuals, domain, mesh, representation, and
tolerance refinement, variational stationarity, and an independent method or
soluble limit.

## Impact-Bounded Dependency Replay

Initial source discovery finds no existing canonical M5 module. Planned new
modules are additive; shared `numerics`, `verification`, accepted claims, and
P236 are consumers/imports but will not be modified. GitNexus indexing and
symbol impact are required before the first canonical symbol edit.

| Consumer | Why affected | Command or proof | Result | Repair if needed |
| --- | --- | --- | --- | --- |
| New M5 unit tests | direct consumer | `PYTHONPATH=src python -m pytest -q tests/test_m5_covariant_action.py` | 6 passed | none |
| P239 verifier | direct consumer | attempts 0001 and 0002 commands | 41/41 and 23/23 | none |
| P236 machinery | source-reuse compatibility only | targeted replay if code is extracted | pending | pending |
| C-IGR-004/C-GRV-002 tests | typed coupling bridge | `pytest tests/test_total_gravitational_coupling.py` | pending | pending |

## Foundational Revision Gate

No foundational revision is open. A mismatch must first survive independently
of the favored candidate and then be routed through a separate challenge with
two repairs and a full migration map.

## Debt Ledger

The active ledger contains no in-boundary debt. Unknown candidate outcomes are
frontier, not defects in a promoted statement.

| Debt | Source | Effect | Discharge | Status |
| --- | --- | --- | --- | --- |
| none | initial freeze | none | not applicable | clear |

## Independent Claim Review

One review record will be instantiated for each of C-M5-001 through C-M5-004
after the transaction freezes. One correction check is allowed for requested
changes. No reviewer is assigned yet.

## Results and Continuation

Two conditional positive results now exist but are not accepted claims. The
complete constant-coefficient basis is classified, with an exact no-go for
retaining all 3x3 coefficients while curing every clock direction. Candidate
E supplies an explicit local Lorentz-scalar replacement on a simple timelike
spectral branch, with a nonnegative Hamiltonian, exact static reduction, and
positive clock witness. The immediate decisive action is to derive the full
variation including `delta h(M)`, freeze the stationary equations and branch
applicability oracle, and solve the fixed-J hedgehog before any two-body force
claim.

## Promotion and Materialization

Pending successful claims. Planned materialization includes the two canonical
modules and tests, immutable P239 campaign, registry entries, next accepted
release, rendered docs, accepted memory, and final validation receipt.

## Done Gate

Open. No success gate has yet been claimed.

## Cross-References

Issue #147; RFC #146; issue #96; P236; accepted release `v0.163.0`;
C-LOR-002; C-KRN-001; C-VAR-003; C-IGR-004; C-GRV-002; P239 proposal manifest
and proposal memory.

## Current frontier after attempts 0003-0014

- `0003-0006`: the projector current supplies a vector kernel, but its boost
  relaxes to zero; the radial biaxial frame is pole-singular.
- `0005`: the exact projected M5.17 potential passes 14 checks.
- `0007`: the timelike scalar completion passes 14 checks and gives the exact
  attractive coefficient `alpha^2/(pi*kappa_tau)`.
- `0008-0010`: a principal spectral clock closes through the retained melt
  sector; a clock-only rational guard cannot prohibit isotropic melt.
- `0011-0012`: the covariant auxiliary clock-axis lift passes 12 checks, but
  without an axis lock it becomes extensive ordinary rotation.
- `0013`: the aligned auxiliary-axis lock passes 8 exact checks and is exactly
  inactive on the pure-director/Coulomb family.
- `0014`: active. At `zeta=cscale`, the best corrected coarse result has
  positive inertia and negative scalar response but relative gradient
  `1.95e-3`, above the `5e-4` stationarity gate. It is attempt evidence only.

Next: finish the preregistered `zeta` ladder and classify Candidate K. Only a
stationary one-body branch opens refinement and the common-action two-body
solve. The canonical issue remains open.
