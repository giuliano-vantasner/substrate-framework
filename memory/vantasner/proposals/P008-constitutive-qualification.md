---
description: Extract S5's exact constitutive content and qualify its unsupported closures
author: vantasner
created: '2026-08-01T12:01:53Z'
updated: '2026-08-01T12:07:29Z'
tags:
- substrate-framework
- campaign-proposal
- constitutive-scaling
- migration-S5
category: proposals
confidence: exploratory
status: archived
---
# P008 Constitutive Cancellation and S5 Qualification

## Question and Positive Deliverable
This campaign extracts two positive exact results from S5 while adjudicating its headline honestly. `C-MED-001` states when common density/temperature scaling cancels from electromagnetic wave speed. `C-SK-001` states the exact coefficient cancellation obtained if two explicitly conditional mass formulas are equated.

Neither result establishes S5's claimed Option-C physical realization. The constitutive cancellation proves that the specified microscopic density-only route produces no index; it does not derive the separate continuum declaration `1/e_eff^2=(1/e_0^2)/n_eff`. The mass identity composes two premises; it does not derive either premise, the hedgehog coefficient, a proton/electron ratio, or individual `F_pi` and `e` values.

## Base Release and Provenance
The accepted base is `v0.7.0` at framework commit `d8ea969`. `C-VIR-001` already contains S5's exact conditional solution of the two virial slope equations, so P008 will not duplicate it.

The hash-pinned source unit is S5 at `merged-framework/bridges/phase-4/bridge_S5_realizability_magnitude.py`, SHA-256 `b92a9db67940169fcd9919f83fda6ae8c56b9b9e40b0d2cbebef5539a5dccde6`. Its file contains later AS1/AS6/AS7 annotations that contradict one another about the operating coupling and length hierarchy. Those annotations are evidence of unresolved provenance, not dependencies P008 may silently accept.

The source exposes all numerical comparators before P008 could blind them. They are therefore quarantined: no numerical closeness, tolerance band, CODATA value, fitted `B1`, assumed soliton length, or historic atomic length participates in candidate selection or acceptance.

## Invariants, Conventions, and Allowed Imports
For `C-MED-001`, density `rho`, thermal scale `Theta`, and reference speed `c` are positive. The declared ansatz is `epsilon=rho*Theta/c^2` and `mu^{-1}=rho*Theta`; the same factor and exponent in both responses are load-bearing. The conclusion is confined to this co-scaling ansatz.

For `C-SK-001`, `B1`, `m_e c^2`, `F_pi`, and `e` are positive symbolic quantities. The formulas `M_top=48*pi^3*B1*m_e*c^2` and `M_ANW=3*pi^2*B1*F_pi/e` are premises. Equality may be solved exactly, but no formula provenance or empirical accuracy is inherited.

## Candidate Preregistration
Three routes are registered after source values were already visible but before implementation.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Generalize the constitutive cancellation to matched response exponents | Declared positive response laws | common scale and exponent | Produces a reusable exact theorem and a clear failure mutation | Wave-speed logarithmic sensitivity vanishes iff exponents match |
| B | Eliminate the shared hedgehog coefficient between the two mass premises | Both mass formulas | symbolic positive inputs | Preserves the exact algebra without calling it a prediction | Solve equality in both directions and mutate a `B1` power |
| C | Accept S5's layer-separation and numerical-closeness narrative as closure | Unproved continuum law, fitted/imported values, assumed length choice | several visible comparators | Conflicts with dependency closure and comparator-blind selection | No derivation connects the co-scaling cancellation to the declared continuum law |

## Selection Criteria and Blinding
The frozen order is dependency closure, exact sensitivity, dimensional transparency, comparator independence, then API reuse. Candidates A and B are complementary positive results. Candidate C is structurally rejected before any recomputation of source errors because it inserts the desired continuum law and relies on imported/declared mass formulas. Previously visible comparator values remain excluded from all verdicts.

## Proposed Claim Delta
P008 proposes two additive conditional claims.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-MED-001 | Under the declared co-scaling response laws, `epsilon*mu=1/c^2` and local wave speed is independent of density and thermal scale; unequal response exponents generally restore dependence | none | exact algebra, logarithmic sensitivity, exponent mutations | medium and effective-index campaigns |
| C-SK-001 | Equality of the two conditional mass formulas is equivalent to `F_pi/e=16*pi*m_e*c^2`, with exact `B1` cancellation; a changed `B1` power does not cancel | none; both formulas are assumptions | exact elimination, inverse substitution, dimensional check, power mutation | future governed Skyrme formula campaigns |

## Implementation and Oracle Plan
Pure `constitutive.py` APIs will expose the co-scaled responses and local wave speed. Pure `skyrme_relations.py` APIs will expose the two conditional mass expressions and matched ratio, with docstrings that name their premise status. Tests will exercise exact identities and numeric domain guards.

The main verifier will prove cancellation, zero logarithmic sensitivities, and mutation failure for unequal density/thermal exponents. It will solve the mass equality rather than insert the ratio, verify the reverse implication and dimensions, and reject a squared-`B1` formula. The independent review will derive the wave-speed exponent vector directly and eliminate `B1` by coefficient ratios without importing the new modules.

P008 will also strengthen migration validation so `qualified`, `refuted`, `duplicate_evidence`, and `out_of_scope` dispositions require disposition-specific evidence fields. The inventory generator must preserve those fields, preventing queue completion by unsupported labels.

## Attempts and Continuation
Attempt `0001` implements Candidates A/B. If either conditional identity fails, repair the algebra or reject the claim. Candidate C is not revived by numerical closeness. Any supportable later AS statement must be proposed from its own hash-pinned unit rather than retroactively treated as S5 authority.

## Debt Ledger
P008 begins with four debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| S5 infers a continuum realization from a microscopic no-index result | Review states the missing bridge and qualified disposition records it | discharged |
| S5 calls premise composition a numerical prediction | Claim remains conditional and excludes every visible comparator | discharged |
| Later AS annotations contradict within the same source unit | Qualification evidence names the contradiction without choosing by chronology | discharged |
| Terminal migration labels currently need no structured evidence | Validator, generator, tests, and templates require disposition-specific support | discharged |

## Review and Promotion Plan
Two claim reviews will audit the exact results separately. A source-adjudication review will map S5 to the accepted narrow claims and a `qualified` terminal disposition whose evidence identifies the unsupported closures. T2B's remaining S5 annotation will likewise move from partial to qualified, because it is now adjudicated rather than pending. Promotion will freeze P008, update APIs/tests/governance, regenerate the queue/docs/memory, replay validators, and run the full boundary suite once.

## Results and Promotion
Attempt `0001` passed 20 exact checks; independent exponent and coefficient elimination passed six checks. No empirical value appears in either verifier. `C-MED-001` and `C-SK-001` were accepted as symbolically verified conditional extensions in `v0.8.0`.

The source adjudication audits every S5 check family. S5 and T2B now have terminal `qualified` dispositions backed by that durable evidence. The exact narrow content is mapped to accepted claims, while physical realizability, mass prediction, correct length selection, and later AS annotations remain unaccepted. Migration validation now rejects terminal labels lacking their structured reason or evidence paths.

## Done Gate
P008 is complete. Both positive claims are independently verified, S5 and T2B carry evidence-backed qualified dispositions, unsupported closures remain unaccepted, the migration validator prevents empty terminal labels, all consumers replay, and campaign debt is empty.
