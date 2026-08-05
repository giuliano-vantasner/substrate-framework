---
description: Audit KI5's difference-of-variational-upper-bounds and profile-quality claims
author: vantasner
created: '2026-08-11T04:02:00Z'
updated: '2026-08-11T04:31:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-KI5
- variational-bound
category: proposals
confidence: established
status: archived
---
# P175 KI5 Variational-Bound Audit

## Question and Positive Deliverable

P175 must determine exactly what KI5 proves about a signed difference assembled
from two alleged variational upper bounds. The positive deliverable must derive
the exact error ledger, distinguish unconditional from premise-dependent
one-sided and convergence statements, audit whether the source objects are
actually variational bounds, and delimit what finite profile probes can test.

## Base Release and Provenance

The accepted base is v0.127.0 at clean framework commit `184e1b6`, with 163
accepted claims. The source baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. KI5 is pinned at
`merged-framework/bridges/phase-34/bridge_KI5_kappa_is_not_a_variational_bound.py`,
SHA-256 `5db475be67e6668f9064096055b0452bb2a762c435132ae324896cce3f9863fe`.
The shared dossier and Lean capstone remain pinned at SHA-256
`e01fbee40d81ebae1fc6f9452c321e2914cb185cdf257ae226d849ea6392702b`
and `269c2b6b023fb1bfacb7dede2e708f09d3e08cad00bcc933e5149357ef5870f5`.
All three paths are clean at the governed source baseline, and KI5's sole source
history commit is `7222eed21720c5174dd35ba8f825d8b7e0a48f3f`.

Generated inventory, accepted P105/P106 records, earlier graph work, durable
memory, and the parent effort already expose KI5's upper-bound headline, stale
coordinate, selected profile probes, and comparator. P175 claims no fresh
blinding and freezes its criteria before a whole-body KI5 or dossier audit.

## Invariants, Conventions, and Allowed Imports

For exact targets `E_i,E_f` and separately declared upper estimates
`Ehat_i=E_i+delta_i`, `Ehat_f=E_f+delta_f` with nonnegative slacks, the signed
difference error is exactly `n*delta_i-delta_f`. Independent nonnegative slacks
therefore permit either sign. A one-sided bound needs a coupled slack inequality,
while componentwise error control can give two-sided convergence without
monotonicity of the difference.

C-RDIFF-001 already owns this exact algebra and its no-one-sided-bound ceiling.
C-RDIFF-002 owns the corrected conditional reduced-model coordinate
8.482417318795285 and rejects variational, mass, binding, reaction, empirical,
and physical readings. C-RPROF-002 supplies only resolution-bounded stationary
branches and expressly proves no local or global minimum or variational upper
bound. Its full numerical solves need not be repeated when unchanged hashes and
accepted evidence already establish the input scope.

Finite selected profile-width mutations cannot quantify over an unexamined
trial space or establish global approximation quality. Comparator 0.929 may be
reported only after structural adjudication and cannot select an ansatz, error
model, or physical claim. Mutable integration uses `np.trapezoid` or the
canonical helper; immutable legacy-name stops are version-only evidence.

## Candidate Preregistration

The candidates separate execution, exact slack algebra, extra premise families,
variational status, finite mutation scope, accepted composition, formal scope,
comparator isolation, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal KI5 replay | Hash-pinned source environment | Source literals | Execution evidence only | AST and native replay |
| B | Exact signed-slack ledger | Two exact quantities and upper estimates | `n,delta_i,delta_f` | Native and already accepted | Symbolic expansion and sign witnesses |
| C | No universal one-sided difference bound | Independent nonnegative slacks | `delta_i,delta_f` | Native and already accepted | Exact counterexamples on both sides |
| D | Conditional one-sided bounds | Explicit relation between slacks | Coupled error constants | Valid only with added premises | Derive necessary inequality and mutate it |
| E | Difference convergence | Separately controlled component errors | Error sequences | Valid without monotone direction | Exact norm bound and alternating examples |
| F | Variational-bound premise audit | Declared trial space and true infimum comparison | Trial families | Expected missing for accepted profiles | Trace C-RPROF scope and source premises |
| G | Finite profile probes | Selected perturbations only | Width or mode samples | Regression evidence only | Counterfamilies outside sampled probes |
| H | Accepted composition | C-RDIFF-001/002 and C-RPROF-002 | No new parameter | Likely nonpromotion ceiling | Exact statement and API comparison |
| I | Comparator firewall | Comparator excluded from structure | `0.929` | Required | Remove and mutate comparator dataflow |
| J | Lean capstone | Exact formal premises and conclusion | Encoded variables | Scope bounded by theorem text | Audit definitions and theorem statement |
| K | Governance closure | Claim-level review and replay | None | No release if content duplicates | Registry, consumers, queue, memory |

## Selection Criteria and Blinding

Selection is ordered by exact signed-error algebra, quantifier scope,
variational trial-space and minimum premises, assumption cost for one-sided or
convergence statements, mutation coverage, dimensional consistency, comparator
separation, accepted dependency fit, consumer reach, and nonduplication. Prior
exposure is explicit; neither the stale coordinate nor 0.929 can select a
candidate.

## Proposed Claim Delta

No claim identifier is proposed at freeze. C-RDIFF-001 already states the exact
upper-bound-difference theorem, C-RDIFF-002 owns the corrected conditional
coordinate and physical ceiling, and C-RPROF-002 owns the stationary-profile
status. A new claim would require distinct reusable content, an importable API,
accepted consumers, and individual four-axis review.

## Implementation and Oracle Plan

The primary route will inventory KI5's checks, definitions, asserted bound
premises, profile probes, comparator dataflow, imports, assertions, and NumPy
compatibility. SymPy and exact rational witnesses are the strongest oracles for
the signed slack identity, feasible error signs, coupled inequalities, and
convergence counterexamples.

The variational audit will require an explicit target functional, admissible
trial spaces, and minimization relation before calling an estimate an upper
bound. Selected width or mode mutations will be typed as finite regression
coverage rather than a universal search. Comparator mutation must change only
comparison predicates and never a structural verdict.

The independent route will reconstruct the strongest valid statement without
importing KI5 or the primary verifier. The Lean theorem will be inspected at
its exact hash-identical scope and its prior execution reused if bytes and proof
obligations are unchanged. Accepted P105 numerical solves and P106 algebra will
be reused at their immutable scopes rather than rerun ceremonially. Direct,
imported, and dynamic NumPy integration names will receive a compatibility
preflight; a version-only stop is repaired or alias-replayed before science.

## Attempts and Continuation

Attempt 0001 freezes release, commits, hashes, prior exposure, allowed imports,
eleven candidates, selection criteria, claim delta, and oracle before P175
opens the KI5 body or shared dossier body.

Attempts 0002-0013 preserve native reproduction, two graph-path failures,
three primary-verifier representation failures, passing 39-check primary and
16-check independent routes, a 31-check typed graph, and reuse of the unchanged
formal execution at its exact abstract sign-witness scope. Thirty-four focused
accepted-consumer tests and both full 1,478-test executions pass with 700 valid
memory records.

## Outcome

KI5 is qualified through C-RDIFF-001, C-RDIFF-002, and C-RPROF-002. Its exact
signed-slack identity and both error signs survive; coupled slacks recover
conditional one-sided bounds, and componentwise error control can converge
without monotonicity. The source does not prove that its stationary BVP branches
are variational minimizers or bound a full model, and finite width probes do not
close that gap. Its source coordinate is stale, comparator 0.929 controls KI5.4,
and physical overbinding and universal profile-quality readings are unaccepted.
No new claim, API, or release survives.

## Debt Ledger

The P175 ledger tracks variational premises, signed error algebra, one-sided
and convergence quantifiers, profile-probe reach, comparator use, formal scope,
consumer propagation, compatibility, and governed-record agreement.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| KI5's exact definitions and predicate reachability are unknown | Pin every definition, check, assertion, import, and runtime result | closed |
| The upper-bound premise may exceed accepted profile evidence | Trace target functional, trial family, infimum, and accepted scope | closed |
| Separate upper bounds may be subtracted incorrectly | Derive the exact slack identity and both sign counterexamples | closed |
| Conditional one-sided or convergence statements may be omitted | State minimal extra premises and exact consequences | closed |
| Finite width mutations may masquerade as a universal profile theorem | Inventory samples and build an unsampled counterfamily | closed |
| Comparator proximity may masquerade as profile quality | Trace and mutate every path from 0.929 | closed |
| Lean prose may exceed its theorem | Inspect exact definitions, hypotheses, and conclusion | closed |
| Reverse consumers may inherit the overclaim | Type and replay affected pending nodes without promotion | closed |
| Governed records may disagree | Synchronize disposition, queue, memory, effort, and release state | closed at adjudication |

## Review and Promotion Plan

Every KI5 predicate receives an individual verdict. Exact slack algebra and
conditional error statements may survive while variational, profile-quality,
physical, empirical, and universal readings are qualified or rejected. A
source tally, finite mutation set, or formal theorem over declared scalars
cannot promote a stronger functional-analytic or physical claim.

## Done Gate

P175 closes only when exact error algebra, upper-bound premises, one-sided and
convergence quantifiers, profile-mutation scope, comparator dataflow, all
predicates and assertions, formal scope, dependencies, consumers,
compatibility, nonduplication, and governed records agree with empty debt.

## Cross-References

See C-RDIFF-001/002, C-RPROF-001/002, C-RMAP-001/002, C-DIM-002, P104-P107,
E2-E4, KI2-KI5, relevant MK/MR consumers, `energy_differences.py`, and the
framework-migration effort.
