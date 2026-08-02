# P083 Impact Analysis

The proposed change adds exact signed-affine coupling diagnostics and C-RGE-004;
it does not rename or alter an accepted symbol.

## Direct Consumers

The direct consumers are `tests/test_renormalization.py`, the P083 primary
verifier, and its source adjudication. The pending SM4 unit is the next known
corpus consumer of pairwise running-line crossings, but it remains
noncanonical until separately adjudicated.

## Indirect Consumers

The package root exports the new dataclasses and functions. Claim and release
generation consumes `governance/claims.yaml` and the new release manifest;
source-queue generation consumes the WM3 disposition. Generated documentation,
accepted claim/release memory, the claim index, source inventory, repository
validator, and parent migration effort are therefore affected indirectly.

## Compatibility

Existing one-coupling APIs retain their positive-`b0` convention unchanged.
The new API uses the separately declared affine convention `a_i=A+B*b_i` and
permits signed coefficients, preventing a silent sign conversion through
`one_loop_inverse_coupling_squared`. No existing call signature, return value,
claim statement, release membership, or test fixture is changed.

## Required Replay

Targeted replay covers renormalization, linear systems, and scale constraints;
the scientific verifiers cover source reproduction, exact inverse solve,
pairwise inconsistency, degeneracies, mutations, normalization covariance,
thresholds, and independent rederivation. Governance, source inventory, claim
inventory, repository validation, docs/memory generation, and one integrated
`scripts/validate.sh` gate cover indirect consumers.

## Debt

No unresolved consumer or migration debt is introduced. The physical U1/SU2
coefficients, sector identities, embedding, thresholds, weak-angle scheme, and
observations are excluded from C-RGE-004 rather than borrowed.
