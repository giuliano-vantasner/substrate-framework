---
description: Validate the selected spectral-Cartan fixed-J two-clock candidate for issue 146
author: codex
created: '2026-08-20T14:30:00+02:00'
updated: '2026-08-20T19:55:16+02:00'
tags:
- substrate-framework
- campaign-proposal
- m5
- issue-146
category: proposals
confidence: exploratory
status: active
---

## Question and Positive Deliverable

P240 asks which ordered issue-147 candidate supplies the smallest explicit
local Lorentz-covariant M5 4x4 action that resolves issue #146. After the
candidate comparison, the current selection is the parameter-free
spectral-Cartan action in its fixed-`J` two-clock sector. The complete positive
deliverable remains the selected action and equations,
exact 3x3 and Coulomb preservation, a refined stationary finite-frequency
fixed-J hedgehog, an attractive common-action relaxed Newton tail, reusable
implementation, individual claim reviews, registry acceptance, and a pinned
release. A no-go, failed solve, or conditional kernel alone is not completion.

## Base Release and Provenance

The accepted base is release `v0.163.0`; the clean implementation baseline is
`substrate-framework@a34b5f584165b86d1fc62af0ede5fbf37b0aa5b7`, the merged
P239 checkpoint. Accepted imports are C-LOR-002, C-KRN-001, C-VAR-003,
C-IGR-004, and C-GRV-002 at their exact registered scopes. P239 is conditional
unpromoted source infrastructure and historical route evidence. Its issue
goal, checks, test counts, validation receipt, and completion status do not
carry into P240.

## Source Inventory and Access Gate

Every load-bearing source needed for the initial structural comparison is in
hand and typed by role.

| Source | Access status | Extracted claims |
| --- | --- | --- |
| Issue #146 and Jarek comment 5352977929 | Open and read | Positive force/frequency target and preference for local Lorentz-covariant kinetic correction |
| Issue #147 comment 5355624676 | Open and read | L1/L2 definitions and frozen ordered gates |
| P239 at merged `a34b5f5` | In hand | Conditional M5 tensors, projectors, timelike scalar, and rejected-route history; no accepted C-M5 authority |
| Release `v0.163.0` | In hand | Exact scopes of the five permitted accepted imports |

## Invariants, Conventions, and Allowed Imports

The full invariant ledger is the matching P240 manifest. The decisive invariant
is identity-level nullity of every new term on every arbitrary static
uniform-time-row 3x3 field, not merely on a hedgehog or uniaxial subset. The
same action and admissible space govern one- and two-body branches. No external
phase charge, imposed profile, fitted coefficient, prior force value, or prior
frequency value is allowed.

## Candidate Preregistration

Two scientifically distinct local completions are frozen before new candidate
output is inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| L1 | Field-dependent kinetic-axis metric from `P_t`, optional constrained `P_N`, `Y`, and covariant derivatives | Simple timelike branch; `P_N` only if exact axis sensitivity requires it | Lowest independent coefficients after identities | Lowest derivative-order route may alter clock inertia while being identically invisible to the full static 3x3 sector | Exact enumeration, arbitrary-symbolic-field null proof, Coulomb coefficient, Hamiltonian/inertia signs, wrong-axis mutation |
| L2 | Quartic, then only if required sextic, timelike-current/Skyrme contractions | At least one genuine time-mixing factor per monomial | Minimum independent quartic/sextic coefficients | Higher order may bound and stabilize the clock while leaving static 3x3/Coulomb unchanged | Same exact gates plus fixed-J Derrick balance and limiting behavior |

## Selection Criteria and Blinding

Selection is structural and ordered: Lorentz/index validity; full arbitrary
static-3x3 recovery; Coulomb coefficient; positive inertia and bounded
Hamiltonian; wrong-axis sensitivity; parameter/derivative economy; fixed-J
Derrick and limits. Numerical comparison opens only after those exact gates
and the one-body numerical contract are frozen. P239 and issue values are
unavoidable prior exposure, never a selection input or tolerance source.

## Proposed Claim Delta

New identifiers avoid reusing P239's reserved C-M5-001 through C-M5-004 and
were collision-searched across governance, campaigns, proposals, memory,
source, and tests before this contract was written.

| Claim | Positive statement | Dependencies | Evidence and consumers |
| --- | --- | --- | --- |
| C-M5-005 | One selected explicit local Lorentz-covariant M5 4x4 action passes the complete exact L1/L2 structural reductions and has typed field equations | approved pinned M5 proposal source; C-LOR-002 convention | SymPy enumeration and variation plus independent explicit components; selected canonical API |
| C-M5-006 | The selected action has a regular refined stationary fixed-J hedgehog with finite positive inertia and finite nonzero strict-minimum frequency | C-M5-005 | exact fixed-J derivative/Hessian plus solver success, scale-relative residual, independent method, wrong-axis mutation, and mesh/domain/tolerance refinement |
| C-M5-007 | Separately relaxed charge defects of the selected action retain a positive-coefficient `1/r` Coulomb tail | C-M5-005, C-KRN-001, C-VAR-003 | exact IR reduction plus common-action relaxed pair refinement and source/sign mutations |
| C-M5-008 | Separately relaxed mass defects of the selected action have a negative-coefficient `1/r` Newton tail with a typed conditional coupling bridge | C-M5-005, C-KRN-001, C-VAR-003, C-IGR-004, C-GRV-002 | exact kernel/sign reduction plus relaxed pair refinement and an independent representation |

## Implementation and Oracle Plan

P240 will add a dedicated conditional module and focused P240 tests rather than
rewrite P239 attempt scripts. SymPy is the primary oracle for invariant
independence, exact Lorentz contractions, arbitrary-field nullity, Coulomb
coefficients, Hamiltonian/inertia signs, axis sensitivity, variation, and
Derrick limits. A separately coded explicit-component contraction is the
normalization cross-check. Only the structurally selected candidate opens
SciPy one-body work; its contract requires declared equations/domain/boundary
data, float precision, sparse or collocation method, tolerances, stopping
status, scale-relative residual, finite outputs, mesh/domain/tolerance
refinement, wrong-axis mutation, and independent reduction or implementation.
Only a passing refined one-body branch opens the common-action relaxed pair
calculation. Canonical quadrature uses `trapezoid_integral`; executable syntax
is preflighted for every direct/imported/dynamic legacy `np.trapz` access.

Validation is newly selected from the P240 diff and impact graph. Prior P239
campaign verifiers, historical test tallies, and validation receipts are not
P240 evidence. Existing canonical tests run only when impact analysis shows
that P240 changed their inputs or public contract; any such replay is recorded
as an affected-consumer check, not inherited campaign validation.

## Attempts and Continuation

Attempts are append-only under `proposals/P240-m5-kinetic-axis/attempts/`.
Attempt 0001 preserves the linked-worktree `.venv` compatibility abort; it
evaluated no candidate. Attempt 0002 performs the exact L1/L2 enumeration and selection. A technical
failure is repaired; a representation failure changes representation; a
candidate failure queues the other preregistered family or its next eligible
order. The effort continues until the positive issue-146 object is promoted or
the user changes the objective.

Attempt 0002 selected L1 at the exact structural boundary. Its density is
`-kappa_1 Tr(P_N Y)^2 P_t^(mu nu) Tr(Z_mu Z_nu)/2`. In the comoving clock
frame it contributes the positive square
`kappa_1 lambda_N^2 (lambda_theta-lambda_phi)^2 omega^2`, is identically zero
on every static uniform-time-row 3x3 field, and gives zero inertia to a
zero-eigenline axis. The quartic L2 current is axis blind and rejected; its
sextic axis-weighted repair is valid but deselected because L1 closes the same
gate at lower field order. The fresh oracle recorded 12 lexical and runtime
checks and 11 pytest assertion nodes; the focused file passed four tests. No
one-body or pair result is yet claimed.

Attempt 0003 made the required constructive correction before numerics. L1
cannot be merely added to the old spectral-Cartan time-curvature inertia,
because that retained axis-blind channel would still carry fixed J on a zero
eigenline. The corrected action contracts curvature externally with
`S=eta^-1-P_t eta^-1`, which is `diag(0,1,1,1)` in the comoving frame, and
uses L1 as the complete clock kinetic term. This replacement passed eight
exact checks plus the one new focused test selector, including Lorentz
covariance, exact static-3x3 recovery, positive spatial energy, deletion of
the old time channel, and a mutation that restores the escape when the old
channel is retained.

Attempt 0004 exhausted L1's remaining boundedness gate and rejected it. A
constant tilted timelike projector plus a one-direction high-frequency static
perturbation gives negative L1 energy growing as `-k^2`; all spatial curvature
commutators vanish and the potential cannot bound the wavenumber. The next
preregistered L2 member is the axis-weighted square of
`epsilon F F (P_N h) h / 8`. External epsilon forces a genuine time-mixing
curvature factor, so the term is exactly absent from every static 3x3/Coulomb
field. Its square is parity even, positive and velocity quadratic; the axis
eigenvalue weight kills the zero-eigenline escape. Eight fresh exact checks
and one focused selector passed. It is now the sole candidate allowed into
the one-body numerical gate.

Attempt 0005 produced two individually stationary, finite, positive-inertia
branches, but failed the fresh one-body gate. The opposite starts differ by
24.19% in total energy and 53.11% in frequency, versus frozen limits `1e-4`
and `0.05`. The lower-energy branch has axis-connection-over-spacing `3.27`,
compared with `0.192` for the higher branch. This is attempt evidence only;
the declared production refinement and every pair calculation remain closed.
Attempt 0006 is one bounded same-domain mesh diagnostic to decide whether the
next repair is numerical multi-start handling or an explicitly regular axis
chart.

Attempt 0006 resolved that diagnostic in favor of the chart repair. At
spacing `0.4`, the start split persisted (38.63% in energy and 9.00% in
frequency). The irregular branch's axis-connection-over-spacing increased
from `3.27` to `3.47`; the regular branch decreased from `0.192` to `0.132`
but hit its iteration limit and missed the frozen stationarity threshold.
This is representation evidence only. The same L2 action next enters an
explicitly rotationally smooth axis chart; production refinements and the
pair calculation remain closed.

Attempt 0007 proved nine exact properties of the regular chart and eliminated
the divergent-axis representation. Its primary solve nevertheless failed:
both starts pinned two non-angle controls at the artificial box, the minus
start exhausted 6000 L-BFGS-B iterations, and the final energy/frequency gaps
were 12.65%/18.98%. The plus start alone met the relative stationarity oracle,
so this is a numerical-box and convergence failure rather than an L2 action
verdict. The next bounded repair widens only optimizer boxes, reports active
components, and continues both starts. Refinements and the pair remain closed.

Attempt 0008 showed that the widened raw-control boxes remain active and that
projected stationarity is therefore misleading: the plus/minus raw gradient
infinity norms are `0.0822` and `0.5818` despite tiny projected values. The
two energies differ by 28.42%. Following the operator's precision challenge,
these descent/minimizer runs are now classified only as warm-start and
conditioning evidence. Seed agreement is also removed as an existence oracle:
separate stable stationary branches may legitimately coexist. The replacement
gate solves the unprojected discrete Euler-Lagrange equations, checks the first
variation independently, and measures the lowest second-variation modes before
any mesh/domain convergence claim.

Attempt 0009 supplied the corrected precision oracle. The plus branch missed
the root threshold at `5.10e-8` and had six negative Hessian modes. The minus
branch was a genuine root (`9.85e-11` relative Euler-Lagrange residual), with
independent AD/centred-difference agreement `4.31e-9`, but ARPACK returned
five converged negative modes from `-14.92` through `-0.716`. Thus both frozen
branches are saddles, not stable one-body solutions. This is a failure of the
tested L2 axis-Pontryagin-square member, not a no-go for the L2 quartic family.
The next decisive action is exact enumeration and screening of the remaining
preregistered quartic invariants. Refinement and pair calculations remain
closed.

Attempt 0010 preregistered polynomial insertions in the external-Pontryagin
family but was withdrawn before execution. The operator correctly noted that
the more natural timelike Skyrme current should first be reduced symbolically
by equivalence, positivity, wrong-axis, and scaling tests. No attempt-0010
symbolic output was opened, and it supplies no selection evidence.

Attempt 0011 completed the requested symbolic equivalence test. The standard
Skyrme forms `Tr(Y^2 Z^2)-Tr(Y Z Y Z)` and `-Tr([Y,Z]^2)/2` are identical and
reduce to a manifest eigenvalue-gap sum of squares. The commuting-null
single-trace class is unique up to normalization. The outer `n^2` is the
unique minimum nonnegative quadratic wrong-axis repair, with
`Tr(P_N Y)^2=Tr(P_N Y^2)` on the constraint surface. The resulting clock
polynomial `kappa*n^2*omega^2*(lambda_theta-lambda_phi)^4` is inequivalent to
L1 and survives a homogeneous clock where every curvature-Pontryagin factor
vanishes. Its inertia scales as `R^3`, so fixed J supplies an `R^-3` collapse
barrier. All fourteen exact checks and two focused selectors pass. This
Skyrme representative is selected for the next residual-and-Hessian one-body
oracle; no descent loss may carry the verdict.

Attempt 0012 applied that precision oracle. The plus and minus branches miss
the root threshold at `3.46e-8` and `2.34e-8`, while independent directional
derivatives agree near `4e-9` and the independent Skyrme trace identity agrees
at `1e-16` or better. The plus branch has a converged Hessian mode `-9.24`;
the minus branch has modes `-5.13` and `-4.24`. Both are saddle neighborhoods,
not stable one-body solutions. This rejects the standard axis-weighted Skyrme
representative on the tested action/ansatz but does not yet dispose of the
entire polynomial-current hierarchy. No refinement or pair gate opens.

Attempt 0013 exhausts the constant-polynomial current subfamily. For
`p(Y)=aY+bY^2`, the exact pair response is
`(x-y)^2(a+b(x+y))^2 Z_xy^2`. Every `b!=0` member therefore has an extra split
blind spectrum; pure `Y^2` fails at `x=-y`. A positive sum of the `Y` and
`Y^2` norms avoids the blind line only by retaining the already-failed
standard current and adding an unfixed coupling ratio. Nine exact checks pass.
This does not cover the inequivalent alternating three-current derivative-
sextic (BPS/topological-current) class, which is the next symbolic screen.

Attempt 0014 screened that derivative-sextic class. With
`K_mu=[Y,Z_mu]` and
`B^mu=epsilon^(mu nu rho sigma)Tr(K_nu K_rho K_sigma)/6`, the density keeps
only the spatial `B` norm orthogonal to the M-derived time line and multiplies
it by the same `n^2` axis repair. Ten exact checks pass: a common-Y symmetric-Z
witness is nonzero; deleting either load-bearing spatial current kills it;
arbitrary static data have only `B^0`, which is projected out; the density is
Lorentz covariant, parity even, positive, and wrong-axis null. Its inertia
scales as `R^-1`, so fixed-J rotation scales as `R` while static curvature and
potential still force both scale endpoints upward. It is selected for one
direct residual/Hessian one-body solve. The BPS-Skyrme paper is motivation
only, not framework authority.

## Debt Ledger

The initial in-boundary debt ledger is empty. Unknown candidate results are
frontier. Any hidden source assumption, fitted coefficient, unsupported bridge,
or changed consumer failure becomes debt and must be discharged before
promotion.

## Review and Promotion Plan

C-M5-005 through C-M5-008 each receive one independent claim review after the
transaction freezes, followed by at most one correction check. Successful
logic moves into importable package APIs with targeted tests. Promotion updates
the registry and next release, renders generated docs, synchronizes accepted
memory, replays only the impact-bounded consumers, and records one
content-addressed P240 receipt. The author leaves the PR to a distinct merger
unless the owner explicitly authorizes self-merge.

## Done Gate

P240 closes issue #146 only when one explicit selected action, its equations
and exact reductions, stationary refined finite-frequency hedgehog, relaxed
Coulomb and attractive Newton tails, reusable APIs, individual reviews,
accepted registry and release, generated docs, synchronized memory, and empty
debt ledger all exist. Any missing gate keeps the objective active.

## Current Candidate Receipt After Attempt 0040

P240 has selected the parameter-free spectral-Cartan curvature action in its
fixed-`J` two-clock sector as the current candidate. Candidate selection no
longer depends on an unwritten future numerical test. The exact evidence
establishes proper Lorentz covariance on the simple timelike branch, a
positive curvature Hamiltonian, coefficient-exact recovery of the complete
static 3x3/Coulomb sector, repair of the explicit negative affine-clock sign,
and the conditional fixed-`J` implication from positive `I12~A/r` to an
attractive Newton-form interaction. Attempt 0035 also supplies an exact
pole-free hedgehog chart.

Smooth direct Euler-Lagrange roots exist through the 6x5 restricted basis. At
attempt 0040 the relative modal residual is `6.80e-15`, inertia is `0.4607`,
and frequency is `1.0853`. That branch is a saddle: the lowest Hessian
eigenvalue is `-2.86807` and centered energy curvature is `-2.86797`. This
refutes local-minimum stability of the tested branch only. It does not demote
the exact action/mechanism candidate or prove that every admissible continuum
branch is unstable. The sizeable withheld 7x6 residual (`0.12096`) is a
diagnostic of representation sensitivity, not a new candidate-selection
hurdle.

The next action is independent validation, not another local basis ladder.
The two open physics questions are whether the tangential-split negative mode
persists in an independent continuum representation and whether separately
relaxed fixed-`J` two-defect fields yield positive `I12(r)=A/r+O(r^-2)`. The
canonical claim-level receipt is
`proposals/P240-m5-kinetic-axis/evidence/current-candidate-receipt.yaml`.
