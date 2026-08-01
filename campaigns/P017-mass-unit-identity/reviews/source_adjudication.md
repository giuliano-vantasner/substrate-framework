# Source adjudication: MR1 mass-unit identity

## Decision

MR1 is terminally `duplicate_evidence` for `C-SK-001`. Its exact common-factor
calculation is correct under the two conditional mass premises, but it is the
same iff already accepted in `v0.8.0`, not a new physical calibration or sector
bookkeeping theorem. P017's exact audit passes 17 checks and its independent
coefficient-ratio route passes five. No new claim, package API, or release is
warranted.

## Check-family audit

MR1.1 exactly solves `a*L=c/L` after declaring `a=F_pi^2/8` and
`c=1/(2*e^2)`, and obtains `L=2/(e*F_pi)` and `U_sky=F_pi/(4e)`. That is valid
algebra within the declared L2/L4 convention. The convention and its physical
applicability are premises here; the check does not independently promote the
ANW mass expression that `C-SK-001` already labels conditional.

MR1.2 exactly factors `48*pi^3` as `(12*pi^2)*(4*pi)`. Calling the resulting
expressions one mass formula in two unit systems additionally assumes the same
nonzero reduced shape factor and both mass premises. P017 states and mutates
those assumptions explicitly.

MR1.3 is exactly `C-SK-001`: conditional equality of
`48*pi^3*b*E_e` and `3*pi^2*b*F_pi/e` is equivalent to
`F_pi/e=16*pi*E_e`. Rewriting the same equality as
`F_pi/(4e)=4*pi*E_e` changes its presentation, not its predicate,
dependencies, or consumers.

MR1.4 is a valid sensitivity check. Changing one power of `b` leaves `b` in the
solution. P017 independently repeats this guard and also rejects changes to
either numerical coefficient, the opposite power mismatch, and the zero-factor
case. These are useful duplicate evidence for the accepted theorem.

MR1.5 substitutes two corpus-specific values of `b` into a result already proved
independent of `b`. The identical outputs are regression instances, not an
independent oracle. They do not show invariance under every Lagrangian change:
that conclusion holds only while both conditional formulas retain the same
nonzero shape factor and coefficients.

MR1.6 correctly differentiates the declared expression
`48*pi^3*b` and shows that expression depends on `b`. Its stronger prose that
all model dependence in the entire chain lives there is not established. A
different model could alter a coefficient, shape power, unit definition, or
the applicability of either mass premise. The source's greater-than-15-percent
numeric movement is unnecessary to the exact derivative and uses pending
corpus-specific inputs.

MR1.7 confirms only that a narrow list of measured-ratio literals and identifier
fragments is absent from the executable AST. It does not inventory scientific
imports and does not quarantine the explicit electron scale, Lagrangian
coefficients, or the `B_CL` and `B_GEN` corpus values. Absence of those forbidden
tokens cannot validate the headline interpretation.

## Claim and consumer comparison

The provisional `C-SK-002` cancellation theorem is mathematically exact but is
only multiplication by a nonzero common factor. Its sole proposed consumer is
MR1, whose specialized consequence is already implemented, tested, reviewed,
and accepted as `C-SK-001`. Repository consumer search finds no distinct API or
claim requiring the generic wrapper. Individual review therefore rejects
`C-SK-002` as a separate registry claim without refuting its algebra.

## Exact duplicate disposition

MR1 maps to and duplicates `C-SK-001`. The durable evidence is the hash-pinned
source reproduction, preserved failed attempt `0001`, passing attempt `0002`,
independent ratio review, and this source audit. MR1's physical unit assignment,
arbitrary-model invariance, phase reconciliation, and no-double-counting
narrative remain unaccepted because the exact equations contain no sector
allocation predicate and import neither formula as established physics.
