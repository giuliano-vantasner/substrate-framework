---
description: Audit GC3's common-phase CP conclusion and one-condensate premise
author: vantasner
created: '2026-08-06T06:23:01Z'
updated: '2026-08-06T07:19:49Z'
tags:
- substrate-framework
- campaign-proposal
- migration-GC3
- common-phase
- CP-invariants
category: proposals
confidence: established
status: archived
---
# P210 GC3 Common-Phase CP Audit

## Question and Positive Deliverable

P210 must derive the strongest exact CP-odd conclusion for common-phase real
matrices, isolate every premise needed to obtain that form from a condensate,
construct decisive countermodels for any universal overreach, and terminally
adjudicate GC3. Rejecting an unsupported universal statement is not completion;
the positive object is a basis-aware theorem, premise and mutation ledger,
claim-level source review, and closed authority graph.

## Base Release and Provenance

The accepted base is v0.151.0 at framework commit `9311c51`, with 191 accepted
claims, 15 pending units, and 190 qualified units. GC3 is pinned at SHA-256
`0e44cc80...6dad8`, 29,123 bytes, source blob `e6c785f`, and one predecessor
commit. EM6, FG2, FG3, FG4, GC1, MH1, MH2, WM7, and WM10 are terminal.
Pending GC4 and GC5 are nonauthoritative cycle edges; GC4, GC5, and GC6 are
reverse consumers and grant no backward authority.

The generated queue exposes nine static check sites, one assertion, and
truncated claims about a common phase times a real matrix, a real Gram matrix,
a real relative basis, a vanishing quartet, and 400 random examples. The source
body, exact matrices, distributions, seeds, tolerances, remaining predicates,
guards, and native output remain unopened through the freeze.

## Invariants, Conventions, and Allowed Imports

C-MIX-001 owns exact complex SVD, Gram spectra, basis freedoms, and relative
basis composition without a physical Yukawa or CP interpretation. C-MIX-002
owns the abstract rephasing quotient and invariant quartets without a physical
CP value or generation map. C-OVL-001 owns normalized overlaps for supplied
profiles and modes without identifying them as Yukawa matrices or deriving a
condensate. The conditional algebra and the physical premise are therefore
separate proof obligations.

## Candidate Preregistration

Eight candidates separate exact common-phase algebra, relative-basis and
weak-basis invariants, the physical premise, countermodels, dimension
provenance, nonduplication, and terminal governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Common-phase Gram theorem | `Y=exp(i theta)R`, real R | theta and R | Gram is real and phase independent | Exact conjugate product |
| B | Two-sector zero-quartet theorem | Two real left bases | R_u and R_d | Relative basis is real orthogonal | General quartet identity |
| C | Weak-basis invariant route | Real symmetric Gram pair | Matrix dimension N | CP-odd commutator traces vanish | Antisymmetry and odd trace |
| D | Universal one-condensate premise | Real couplings and modes plus one phase | Interaction data | Valid only if every premise is derived | Dependency and action audit |
| E | One-condensate countermodels | One additional complex structure | Coupling or phase field | Universal premise fails | Explicit complex Gram or quartet |
| F | N=3 phase slot | Abstract unitary quotient | N | Counts a slot but supplies no phase or N | Dimension mutation |
| G | No new surface | Existing accepted claims suffice | None | Exact result is composition | Registry and API review |
| H | Terminal governance | Accepted dependencies only | None | GC3 closes individually | Graph replay |

## Selection Criteria and Blinding

Selection prioritizes exact factorization, invariant CP diagnostics, dependency
closure for real inputs and a shared phase, global-versus-local phase typing,
degeneracy stability, dimension provenance, assumption economy, novelty, and
graph closure. Source details open only after repository and memory validation
and a clean committed freeze.

## Proposed Claim Delta

P210 initially proposed no new claim or API because C-MIX-001 and C-MIX-002
own the abstract matrix machinery and C-OVL-001 owns the overlap form. Opened
source inspection exposed a compact theorem not stated at those ceilings:
global-phase cancellation for both rectangular Grams, a real relative basis,
all-real quartets, odd commutator-trace nullity, and the degenerate-basis
caveat. P210 therefore proposes C-MIX-003 with dependencies C-MIX-001 and
C-MIX-002 and a canonical `common_phase_matrices` module. It explicitly does
not promote the source's Yukawa, condensate, CKM, or physical CP labels.

## Implementation and Oracle Plan

SymPy is the strongest oracle for the exact identities. For real finite `R`,
`(exp(i theta)R)^dagger(exp(i theta)R)=R^T R`. Two such sector matrices admit
real orthogonal Gram eigenbases, so their relative basis is real and every
rephasing-invariant quartet has zero imaginary part. The commutator of their
real symmetric Gram matrices is real antisymmetric, making odd traces vanish;
in three dimensions its determinant also vanishes. Degenerate eigenspaces
retain nonunique bases and must not turn a coordinate choice into physical CP.

Mutations vary harmless global phases, introduce entrywise and
position-dependent phases, add an independent complex coupling while retaining
one condensate, make a mode complex, force a degenerate Gram matrix, and change
the matrix dimension. Random numeric trials reproduce or regress exact algebra
but do not independently verify it. Compatibility preflight scans direct,
imported, dynamic, and eager legacy NumPy access; mutable code uses
`np.trapezoid` or `trapezoid_integral`, while an immutable version-only event is
recorded with alias-only replay and never counted as scientific failure.

## Attempts and Continuation

Attempt 0001 freezes authority, eight candidates, exact matrix and invariant
obligations, countermodel mutations, physical ceilings, graph scope, and
compatibility policy before source access. Attempt 0002 reproduces all nine
native checks after freeze commit `9e6fb3d` with no quadrature compatibility
surface. Source inspection confirms the exact common-phase algebra but exposes
undeclared physical premises: accepted EM6 does not force a complex substrate
ontology, MH1 does not supply a Yukawa interaction, and FG3/FG4 explicitly do
not establish CKM or physical CP. The finite random ensemble, separate external
wells, and one equal-spacing toy cannot repair that authority gap.

Attempts 0003 through 0009 preserve the scale-relative numeric repair,
GitNexus CLI fallback after its MCP transport closed, source-string casing,
queue-schema and render-anchor repairs, correct inventory entry point, and
terminal-graph root-set repair. The final exact routes pass 42 primary and 27
independent checks; the 13-node terminal graph passes 34 checks over 97 static
predicates and 18 assertions; and 99 focused accepted-API tests pass. Attempt
0010 records the single integrated v0.152.0 boundary: 851 memory files and all
1,837 tests pass in 195.94 pytest seconds and 210.01 seconds total wall time.
Attempt 0011 preserves a record-only relative-path CLI mistake and the
successful absolute-path replay over the same 851 memory files.
Attempt 0012 preserves the failed obsolete proposal pathspec and rename-only
commit `7658d87`; the substantive promotion follows in a separate commit
without rewriting that provenance.

## Debt Ledger

The P210 ledger tracks every phase, coefficient, profile, mode, matrix
dimension, basis freedom, invariant, random comparator, graph edge,
compatibility event, and generated record.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Detailed source predicates remain blinded | Reproduce once after committed freeze | discharged after `9e6fb3d` |
| Real coefficients and modes may be undeclared premises | Audit action, imports, and local assumptions | discharged by source and dependency audits |
| A global phase may be confused with arbitrary complex structure | Run global, entrywise, and local-phase mutations | discharged by exact premise countermodels |
| Degenerate basis freedom may create spurious coordinate phases | Audit invariant and degenerate cases separately | discharged by the identity-Gram Fourier-basis counterexample |
| The N=3 phase slot may be treated as a physical phase or count theorem | Mutate N and source every count premise | discharged by K/N separation and the two-source construction |
| Existing claims may already own all exact content | Complete claim and API nonduplication audit | discharged; C-MIX-003 is the minimum novel surface |
| Pending cycle dependencies may grant authority | Replay GC4 and GC5 without imports | discharged by the terminal graph |
| Reverse consumers may be silently broken | Replay GC4 through GC6 after disposition | discharged by the terminal graph and focused consumers |
| Compatibility may masquerade as science | Audit every executable access shape | discharged with zero quadrature surface and zero scientific version failures |

## Review and Promotion Plan

Every GC3 predicate received an individual verdict. C-MIX-003 has a canonical
API, focused tests, independent review, registry and v0.152.0 release entries,
generated documentation, synchronized memory, and one passing full promotion
gate. GC3 is qualified rather than blanket accepted.

## Done Gate

P210 is closed: the exact common-phase theorem, physical-premise audit,
countermodels, degeneracy treatment, dimension provenance, source-predicate
adjudication, authority graph, compatibility audit, qualified disposition,
generated state, and durable memory agree with an empty debt ledger. Neither a
symbolic identity under declared assumptions nor 400 random examples was used
to close the rejected universal physical claim.
