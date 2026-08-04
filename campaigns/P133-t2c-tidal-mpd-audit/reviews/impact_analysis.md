# P133 Impact Analysis

P133 adds one pure optical collective-dynamics API and one accepted claim. It
does not rename or change any existing metric, curvature, point-acceleration,
moment, or source symbol.

## Direct Framework Consumers

`src/substrate_framework/collective_dynamics.py` now owns
`slow_optical_profile_width_correction`. The package export list and
`tests/test_collective_dynamics.py` are its direct consumers. C-OG-004 depends
on C-CC-001 and transitively C-OG-001; no existing accepted claim changes.

## Governance and Generated Consumers

The affected governed records are `governance/claims.yaml`, release v0.101.0,
`governance/releases/current.yaml`, the T2C disposition, generated claim and
release documentation, accepted claim and release memory, and the migration
queue. The release claim set remains dependency closed.

## Source and Reverse Consumers

T2C is terminally qualified. Pending G2 only reuses generic curvature
machinery. Pending G4's executable path uses the phase-three finite-wave-number
form factor rather than T2C's rejected curvature-width equation. Both source
hashes replay without requiring an accepted T2C force. G4's legacy integration
name is handled by alias-only compatibility and is not imported into mutable
framework code.

## Formal and Numerical Surface

No Lean theorem, PDE solver, numerical mesh, comparator, or fitted parameter is
affected. The new claim is exact symbolic calculus plus an independent Gaussian
Fourier and reflection-symmetry derivation. The full repository gate is still
required once after generated records and campaign evidence are synchronized.

## Risk Decision

The change is additive and narrow. The main semantic risk is overreading a
declared profile average as a physical extended-body or MPD equation; the API
docstring, claim statement, source adjudication, tests, and decision records all
state that ceiling explicitly.
