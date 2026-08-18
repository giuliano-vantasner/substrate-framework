---
description: Independent review of C-GW-012
author: vantasner-review
created: '2026-08-18T21:50:00+02:00'
updated: '2026-08-18T21:50:00+02:00'
tags:
- substrate-framework
- claim-review
- lean-promotion
category: decisions
confidence: working
status: archived
---
# Review of C-GW-012

## Claim Under Review
Declare lowestRadiatingMultipole(s)=s on integer spin s, encoding the standard 3+1 multipole-radiation counting fact that the lowest radiating multipole order of a massless field of integer spin equals the spin, ell_min = s - the conservation-law forbidding of the lower orders (energy-momentum conservation kills the gravitational ell=0 monopole and ell=1 dipole; charge conservation kills the electromagnetic monopole) is a declared physics input, not proved here. Evaluated: a massless spin-2 field (gravity) first radiates at the quadrupole ell=2, and 2 is not 1 (the non-tautology guard); a spin-1 field (electromagnetism) first radiates at the dipole ell=1; a scalar (spin 0) radiates at the monopole ell=0; the gravitational radiating order strictly exceeds the electromagnetic one; and both ell=0 and ell=1 lie strictly below the gravitational radiating order, so monopole and dipole gravitational radiation are excluded. Composing with the declared TT count function of C-GW-011, the spin-2 field in D=4 has 2 propagating polarizations and lowest radiating multipole 2. This is a conditional counting theorem on the declared map. It does not prove the conservation-law forbidding, the vector/tensor spherical-harmonic expansion, any radiative dynamics, power, or physical radiation event, and selects no physical field.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Phase12GW_LowestMultipole.lean`),
the P232 census entry, the P233/P234/P235 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P233-lean-discrete-facts/reviews/C-GW-012-claim-review.md`.

## Independence
The theorem statements were re-derived from the file definitions rather than the module-doc
narrative, and each entrypoint was matched clause-by-clause against the claim statement;
every physics premise in the narrative was confirmed to appear in the claim assumptions as
a declared input rather than machine-checked content.

## Verification Status
formal_verified: kernel-checked at the repository-pinned toolchain (Lean v4.28.0, mathlib
8f9d9cff6bd7) inside the library gate that passed at the ingestion commit; the formal
surface is unchanged by the promotion, so the gate carries without a rebuild. Axiom
footprints are subsets of Mathlib standard axioms; no proof escapes.

## Sensitivity and Counterexamples
The promoting file carries its own non-tautology guards (wrong-dimension, wrong-spin,
dropped-VEV, wrong-coupling, wrong-polarity, order-flip witnesses as applicable), matched
to the claim's discriminating clauses in the census. Where a file used pasted values
instead of evaluating the defining object (ProductionAmplitude), the census recorded a
class-4 disposition rather than a promotion; this claim passed that discipline.

## Framework Compatibility
Append-only compatible_extension: no existing claim altered, no new import beyond the
ingested file, conditional premises named, interpretive physics excluded from the
machine-checked statement. Nearest accepted neighbours state different objects.

## Dependency and Consumer Replay
No existing consumer changes; the generated index, release manifest, and accepted claim
memory regenerate from registry state. Replay is the repository validation suite at the
merge boundary.

## Competing Candidate Audit
Fixed theorem, one complete proof route; the alternative classification (corroboration)
was tested against the registry and rejected by statement-level search (census record).

## Four-Axis Decision
- Verification: formal_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active

Accepted into v0.163.0 through campaign P233.
