---
description: Audit GW2's quadrupole-power formula and normalization closure
author: vantasner
created: '2026-08-01T17:50:10Z'
updated: '2026-08-01T18:00:51Z'
tags:
- substrate-framework
- campaign-proposal
- quadrupole-power
- linear-spin-2
- migration-GW2
category: proposals
confidence: exploratory
status: archived
---
# P037 GW2 Quadrupole-Power Audit

## Question and Positive Deliverable

P037 must determine whether a convention-complete quadrupole radiation-power
theorem can be derived from an explicitly declared linear massless spin-2 model
and the accepted conserved-source moments. The positive deliverable is either
that full conditional theorem or, if its normalization cannot be closed, the
strongest reusable exact quadrupole-derivative and averaging theorem; merely
rejecting GW2's physical interpretation is not completion.

## Base Release and Provenance

The accepted base is `v0.32.0` at framework commit `bb60762`. Its forty-five
claims include `C-MOM-001`, which derives the localized conserved-stress moment
ladder while explicitly excluding a gravitational field equation, TT
projection, radiative multipole ordering, waveform, and power. The pending
hash-pinned candidate is GW2 at
`merged-framework/bridges/phase-12/bridge_GW2_quadrupole_power.py`, SHA-256
`b41bf49ed7c13e22defc4c70003dad400ffcebcb6c04e852883e2e331badc1d7`.
Bundled-memory search found no accepted quadrupole-power theorem.

## Invariants, Conventions, and Allowed Imports

The accepted source quadrupole convention is
`Q_ij=integral rho*(3*x_i*x_j-r^2*delta_ij) d^3x=3*I_STF`. P037 may import
exact flat-space tensor calculus, retarded Green-function methods, and periodic
averaging. A linear massless spin-2 action and source coupling may be declared
only as a conditional model; its normalization must remain visible from action
through flux. No observed gravitational constant, named Einstein formula, or
GW2 comparator may be used to select or normalize a candidate.

## Candidate Preregistration

The alternatives are frozen from queue metadata before the full GW2 executable
body or any source comparator is inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Full conditional quadrupole radiation theorem | Declared quadratic massless spin-2 action, conserved localized slow source, retarded solution, wave-zone and periodic hypotheses | Explicit action/source coupling and units | Compatible extension if every normalization closes | Derive field, TT amplitude, flux, angular average, and source convention coefficient independently |
| B | Exact declared-functional and periodic-average algebra | Accepted source moments plus a declared nonnegative quadratic functional | Free prefactor and source motion | Native mathematics with weaker physical reach | Exact derivatives, averaging, positivity, dimensions, mutations, and limiting cases |
| C | Direct Einstein power and lowest physical radiative order | Conservation plus the formula named in GW2 | Inserted `G_eff/5` | Dependency conflict | Accepted-claim closure and countermodels with different field/flux normalizations |

## Selection Criteria and Blinding

Selection is ordered by dependency closure, explicit premise cost, action-to-
flux convention closure, exact derivative and trace factors, dimensional and
positivity checks, static/translation/periodic limits, independent coefficient
derivation, and mutation sensitivity. Comparator values and GW2's reported
formula coefficient remain blinded until those equations and criteria are
frozen by this contract.

## Proposed Claim Delta

Provisional `C-GW-001` would be a conditional theorem for an explicitly
normalized linear spin-2 model, or a narrower exact power-functional theorem if
the action-to-flux derivation does not close. It will distinguish the normalized
STF moment from the triple-normalized source convention and exclude physical
general relativity, a measured coupling, nonlinear corrections, arbitrary-
source radiation, universal lowest-multipole claims, and substrate realization
unless separately established.

## Implementation and Oracle Plan

Pure APIs will encode the chosen quadrupole convention, exact derivatives,
periodic contractions, and—only if Candidate A closes—the declared model's
field and flux normalization. SymPy will verify analytic identities and angular
integrals; numerical quadrature may independently check nontrivial sphere or
period averages with refinement. Mutations will change the STF factor,
derivative order, angular projector, flux coefficient, and averaging period.
Static, uniform-translation, axisymmetric periodic, and convention-rescaling
cases will guard the interpretation.

## Attempts and Continuation

Attempt `0001` will reproduce GW2 and inventory which steps are derived,
declared, imported, or only checked by substitution. If its physical
normalization is borrowed, Candidate A will be rebuilt independently rather
than patched around the source; if that cannot close, Candidate B remains a
positive exact deliverable while the unresolved physical claim is preserved as
qualified evidence.

## Debt Ledger

This ledger tracks the field premise, normalization chain, source convention,
averaging, multipole interpretation, and verifier sensitivity.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| No accepted field equation or radiation flux exists | Derive both from one declared conditional action or exclude physical power | discharged: C-GW-001 retains both prefactors as conditional inputs and excludes physical gravity |
| The source quadrupole differs by a factor of three from normalized STF | Carry the convention through every derivative and coefficient | discharged: exact rescaling gives G/5 for I_STF and G/45 for Q=3*I_STF |
| A named coefficient may be inserted as the answer | Independently derive every load-bearing normalization and mutate it | discharged: 8*pi/5 is independently integrated while waveform/flux mutations change the conditional coefficient |
| A periodic example may substitute for a general theorem | Separate general conditional identities from example-specific averaging | discharged: exact single-harmonic averaging is general within its stated class and the circular path is only a checked example |
| Conservation may be overread as completeness of radiative multipoles | State the additional field, gauge, wave-zone, and approximation premises | discharged: the claim excludes physical and lowest-multipole conclusions |

## Review and Promotion Plan

The provisional claim receives an independent normalization and limiting-case
review. Promotion requires pure APIs and tests, immutable attempt evidence,
claim-level adjudication, terminal GW2 disposition, release/docs/memory
synchronization, targeted downstream replay, and one unchanged full repository
gate.

## Done Gate

P037 closes only when the selected positive theorem, conventions, action/flux
boundary, derivative order, averaging, limits, mutations, source disposition,
consumers, and all campaign debt satisfy the framework contract.

## Adjudication Result

Candidate B is accepted as `C-GW-001`. Thirty-four main checks derive the exact
TT projector, `8*pi/5` sphere contraction, conditional prefactor dependence,
quadrupole-convention covariance, harmonic average, and circular-source limit;
nine independent checks reproduce the angular factor with refined quadrature
and rederive the factor-nine defect. GW2 is qualified because its waveform and
flux are imported, its `Q=3*I_STF` is paired with the wrong waveform
normalization, its time average is symbolic, and no lowest physical radiating
multipole is established. All campaign debt is discharged.
