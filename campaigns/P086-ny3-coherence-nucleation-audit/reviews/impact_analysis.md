# P086 Impact Analysis

The proposed change adds exact conditional phase-ensemble and activation-
threshold APIs plus C-COH-001; it does not rename or alter an accepted symbol.

## Direct Consumers

The direct consumers are `tests/test_coherence_gates.py`, the P086 primary
verifier, and its source adjudication. The hash-pinned spark-discharge
`coherence_array.py` is a predecessor consumer whose formula is reproduced but
not modified. Pending BD1 and BD3 remain noncanonical and are not promoted by
this claim.

## Indirect Consumers

The package root exports the five new pure functions. Claim and release
generation consumes `governance/claims.yaml` and the new release manifest;
source-queue generation consumes the NY3 disposition. Generated documentation,
accepted claim/release memory, the claim index, source inventory, repository
validator, and parent migration effort are affected indirectly.

## Compatibility

No existing API signature, return value, convention, claim, or fixture changes.
The new functions require exact inputs and preserve explicit distinctions among
positive-integer source count, continuous population coordinate, pair
coherence, directional intensity, activation scale, and dimensionless
activated factor. No rate or nuclear terminology enters an API name.

## Required Replay

Targeted replay covers the new coherence-gate tests and accepted capillary
energy tests. The scientific verifiers cover iid phase expansion, a Gaussian
characteristic integral, normalization changes, deterministic antiphase
counterexamples, threshold roots and ordering, activated-factor signs,
source mutations, and the hash-pinned consumer. The full 61-check engineering
consumer, governance and inventory tests, generation checks, and one integrated
`scripts/validate.sh` gate cover indirect consumers.

## Debt

No unresolved consumer or migration debt is introduced. Physical emitter
preparation, effective temperature, material barrier inputs, stochastic
prefactor, nucleation dynamics, precursor identity, nuclear interaction,
reaction branch, deposition, and event payload are excluded from C-COH-001
rather than borrowed.
