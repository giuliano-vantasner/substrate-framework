# Source adjudication: EL1 imported mass coordinate

## Decision

EL1 is qualified. Its exact primitive-basis and imported-mass coordinate
content supports `C-DIM-002` and new `C-DIM-003`; its conditional unit equality
also restates `C-SK-001`. The source does not prove a value for the coordinate,
eliminate the physical input, derive a mass ratio, or establish that every
corpus consumer uses electron mass in one semantic role.

## Check-family audit

EL1.1 exactly recomputes the full rank and zero kernel already accepted in
`C-DIM-002`. The conclusion that dimensional analysis supplies no pure number
from the primitive set is correct and preserves rather than eliminates the
need for dimensionless physical input.

EL1.2 and EL1.2b correctly derive the unique set-local mass monomial
`S/(c0*a)` and check its units. This is duplicate evidence for `C-DIM-002`.
The source's suggestion that a second monomial representation would make a mass
carry more than one datum is not generally valid; it would instead expose a
dimensionless primitive-group freedom. That counterfactual is outside the
accepted full-rank case.

EL1.3 proves the positive bijection now accepted as `C-DIM-003`:
`N_m=m*c0*a/S` with inverse `m=N_m*S/(c0*a)`. P018's APIs and review correct the
source phrase “not a physical mass.” The map changes coordinates while retaining
the same physical input and one arbitrary dimensionless number; it does not
predict that number.

EL1.4 algebraically reconstructs `m_e=U_sky/(4*pi)` from both conditional chain
members. This is exactly the relation already accepted as conditional
`C-SK-001`, as P017 established for MR1. It does not prove either mass premise,
that the electron scale is a medium unit in nature, or that no lepton property
is used elsewhere.

EL1.5 is a useful counterexample showing that a fabricated inverse-square mass
consumer would not reduce to the linear unit relation. It cannot upgrade the
actual-consumer census or establish the physical meaning of the existing
formula.

EL1.6 correctly notes that two masses expressed in the same primitive basis
have ratio `m_1/m_2=N_1/N_2`; the dimensionful scale cancels. Its stronger claim
that the framework can therefore derive the ratio is false without equations
fixing the two coordinates. P018 explicitly differentiates the ratio with
respect to both free inputs. Absolute reconstruction depends on the retained
primitive values, including `a`, but an external absolute mass can still be
supplied as an import.

EL1.7 is a file-level regex co-occurrence test. Its predicate checks only that
files containing an electron-mass numeral also contain a unit-expression token
somewhere, and its asserted all-consumer condition filters only phase 4 and
phase 44 even though its own run reports hits in phases 24 and 29. A comment-only
fixture passes the same two regexes, proving the oracle cannot establish semantic
role, adjacency, or exclusivity.

EL1.9 is a working narrow forbidden-literal guard for EL1's own executable AST.
It does not repair EL1.7's semantic reach or turn the uninspected mass values
found at runtime into accepted inputs. No numerical value is needed for
`C-DIM-003`.

## Exact qualification

Accepted content is limited to the set-local mass unit, the lossless
dimensionless-coordinate bijection, its arbitrary-input ceiling, and the
already-conditional Skyrme equality. EL1 does not establish an electron
ontology, a medium energy unit in nature, a universal one-role consumer census,
a derived electron/hadron ratio, an absolute length or mass, or removal of the
physical import. These remainders are preserved as source history while later
campaigns seek positive dynamics that could determine a coordinate.
