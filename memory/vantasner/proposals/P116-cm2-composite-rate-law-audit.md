---
description: Derive a typed composite loss-cycle theorem and adjudicate CM2's rate and sweet-spot interpretations
author: vantasner
created: '2026-08-08T03:00:00Z'
updated: '2026-08-08T05:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- factor-composition
- loss-boundary
category: proposals
confidence: exploratory
status: archived
---
# P116 CM2 Composite Rate-Law Audit

## Question and Positive Deliverable

This campaign must deliver a reusable exact theorem for the typed product of a
declared activation factor, positive count multipliers, a symmetric paired-
resolvent magnitude, a nominal finite-window cycle factor, and a symmetric
two-level gate. The positive object includes product simplification,
dimensions, scale covariance, parameter sensitivities, identifiability,
one-sided limits, cutoff discontinuities, stationary-point classification, an
actual-cycle comparison, and physical interpretation ceilings. Reproducing a
finite-grid maximum or rejecting a nuclear-rate narrative is not completion.

## Base Release and Provenance

The accepted base is v0.95.0 at framework checkpoint
`734ddec8e3ffa1eb2e127d5601d7b851062ff353`; its scientific base is
`2cbc423215cb24ec1402740a47174e302d7a3828`. The predecessor baseline remains
`/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.

The candidate is CM2 at
`merged-framework/bridges/phase-31/bridge_CM2_coherence_rate_law.py`, SHA-256
`c75fee880740765d3ef3e32634bf05360fd9789e46bd579fd07af60d29a79fa2`, git
blob `10c77e6db3aab923d4f4c6d6945768f954d5eba7`, and 15,745 bytes. The hash
matches the source inventory. Unrelated Phase 47/48 work and the deliberate
current-NumPy compatibility overlay remain uncommitted in the source checkout
and are outside P116.

The accepted authority read for this freeze is the v0.95.0 release,
`governance/claims.yaml`, and the canonical `radial_energy`,
`damped_oscillator`, `thermal`, `symmetric_spin`, and `paired_resolvent`
modules. BD1 is qualified through C-RG-002, LB2 through C-DYN-001, PN3 through
C-SPN-002, PN4 through C-RES-001, and T1G is migrated through C-TH-001. PN2 is
qualified with arithmetic only and no accepted claim. B1 remains pending and
cannot supply a premise.

Queue metadata exposes twenty-one predicates and the complete displayed
six-factor product, including its activation, quotient, occupation,
paired-loss, nominal inverse-loss cycle, and two-level factors. Prior consumer
audits exposed the CM2 source hash and dependency relation. This contract does
not claim pristine formula blinding; it freezes stronger structural gates
before execution, whole-body inspection, or selected-grid review.

Registry, campaign, and durable-memory searches found no C-CMP-001 identifier
or accepted theorem for this cross-sector loss-cycle product. Earlier claims
govern the individual factors but not the exact cancellation and endpoint
classification of their product.

## Invariants, Conventions, and Allowed Imports

Use a positive conditional barrier E_star and positive scale Theta only as
declared inputs to the dimensionless factor `exp(-E_star/Theta)`. Use positive
dimensionless count multipliers without importing PN2's rejected subdivision
process or PN3's rejected rate interpretation. Use a real nonzero detuning
Delta, nonnegative loss Gamma, and a declared coupling product c under
C-RES-001's zero-energy equal-pair convention.

On `0<Gamma<2*omega`, the nominal window-cycle factor is
`omega/(2*pi*Gamma)`. It is not phase coherence, a survival probability, or
an actual oscillation count near criticality. C-DYN-001's actual count instead
uses `sqrt(omega_0^2-Gamma^2/4)/(2*pi*Gamma)` for a declared linear oscillator
natural frequency omega_0. A finite-amplitude sub-gap breather frequency is
not silently substituted for omega_0.

The paired magnitude has the dimension of `c/energy`; all other displayed
factors are dimensionless. The composite inherits that dimension, not a rate
dimension, unless an independently approved action or kinetic prefactor and a
complete state-to-observable map are supplied. B1, forward CM/GB units, source
cycles, numeric grids, and prose labels supply no authority.

## Candidate Preregistration

The candidates separate source reproduction, exact nominal composition, the
accepted actual-cycle alternative, physical and normalization countermodels,
independent derivation, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal CM2 reproduction | Source conventions | Source inputs and grid | Mixed evidence | Hash, tally, and twenty-one-predicate audit |
| B | Exact nominal loss-cycle composite | Declared factors on the open underdamped interval | E_star, Theta, counts, c, Delta, Gamma, omega | Native conditional theorem with no interior maximum | Exact cancellation, derivative, dimensions, limits, jumps, and scale ranks |
| C | Actual-cycle comparison | C-DYN-001 oscillator premises | omega_0 and Gamma | Continuous critical endpoint but still no phase coherence | Independent simplification and endpoint comparison |
| D | Prefactor and physical countermodels | Alternative lawful inputs | interaction, density, spectral, kinetic, loading, and cutoff factors | Exposes nonidentifiability and rate overreach | Zero-rate and arbitrary-target families plus loss-power mutations |
| E | Fresh exact rederivation | Elementary algebra and calculus only | Same exact inputs | Independent confirmation | No import of the new canonical implementation |
| F | Dependency and consumer audit | Complete registry and queue | None | Closed adjudication scope | B1 ceiling, predecessor verdicts, cycles, consumers, and nonduplication explicit |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; explicit domain,
dimension, state, normalization, and cutoff conventions; exact product
simplification; one-sided and endpoint limits; discontinuity and stationary-
point classification; sensitivity to load-bearing factor choices; separation
of nominal cycles, actual oscillations, phase coherence, matrix elements,
probabilities, and rates; scale covariance; identifiability; assumption
economy; reusable API fit; and complete consumer replay.

The source formula and advertised sweet spot are already exposed through the
queue. Selected loss values, finite-grid maximizer, reported product magnitude,
and individual predicate bodies remain blinded until this proposal and its
manifest validate. Numerical closeness cannot select the theorem, rate label,
or optimum claim.

## Proposed Claim Delta

P116 provisionally reserves C-CMP-001 for the exact conditional product of the
C-RES-001 equal-pair magnitude and a declared inverse-loss cycle factor,
including cancellation, dimensions, strict open-interval monotonicity,
one-sided limits, cutoff jumps, actual-cycle comparison, scale freedoms, and
an explicit non-rate ceiling. Its accepted dependencies are C-RES-001 and
C-DYN-001; C-RG-002, C-SPN-002, and C-TH-001 may enter only as typed positive
multipliers whose existing ceilings remain intact.

The proposed implementation is `src/substrate_framework/composite_factors.py`.
No challenge or supersession relationship is proposed. If the exact theorem is
already fully governed by composition, P116 must qualify CM2 without promoting
a duplicate identifier.

## Implementation and Oracle Plan

The canonical module will expose pure exact APIs for the open-interval nominal
loss-cycle product, its explicitly piecewise zero-cutoff extension, the actual-
cycle comparison, and a typed composition ledger. Existing canonical APIs will
supply the paired resolvent, oscillator frequency, barrier factor, spin
coefficient, and thermal gate rather than being copied.

SymPy is the strongest oracle because the load-bearing obligations are exact
products, derivatives, limits, series, dimensions, ranks, and piecewise
boundary values. The primary verifier will mutate the paired-loss numerator,
inverse-loss power, half-width convention, cutoff inequality, damped-frequency
radical, count normalization, coupling scale, activation exponent, and thermal
gate. It will require wrong-convention probes to change the relevant verdict.

An independent reviewer will reconstruct all formulas without importing the
new module. Countermodels will set the interaction or final-state density to
zero, multiply by an arbitrary positive kinetic prefactor, vary coupling
normalization, replace the nominal cycle factor with the accepted actual-cycle
factor, and insert a general `Gamma^p` factor to state exactly when an interior
stationary point can or cannot occur.

CM2 numerical evaluation is regression only after the exact theorem closes.
No solver or quadrature is required. Canonical sampled integration would use
`trapezoid_integral`, a mutable current-environment script would use
`np.trapezoid`, and an immutable source aborting only on `np.trapz` would
receive an alias-only recorded replay before scientific adjudication. Such a
compatibility abort is not candidate rejection.

The dependency and consumer audits will pin every direct and indirect pending
consumer while excluding return edges to CM2 from its own authority. Targeted
module, campaign, dependency, registry, generated-state, and consumer replays
precede one full terminal workflow gate.

## Attempts and Continuation

Every source abort, compatibility event, dimensional mismatch, false
stationary claim, endpoint discontinuity, grid-max artifact, sign or branch
error, physical-prefactor counterexample, dependency leak, and oracle defect
will be preserved before repair. A failing rate narrative changes the next
candidate; it does not end the campaign.

Attempt 0001 preserves the pre-freeze provenance check that caught incorrectly
expanded framework commit suffixes after schema validation but before source
execution or whole-body inspection. The manifests and memory now use the exact
objects returned by `git rev-parse`.

## Debt Ledger

The ledger tracks every factor definition and unit, loss and cutoff domain,
nominal versus actual frequency, count and coupling normalization, barrier and
temperature provenance, endpoint extension, stationary condition,
identifiability, kinetic prefactors, B1 and predecessor ceilings, source
cycles, consumers, all twenty-one predicates, and claim nonduplication. It
begins empty because each item is an explicit frozen gate.

## Review and Promotion Plan

Every CM2 predicate receives an individual verdict. Exact primary and
independent reviewers, source/input/dependency/cycle/consumer audits, mutation
sensitivity, physical-semantic countermodels, and nonduplication determine
whether C-CMP-001 is accepted. Promotion requires an importable module,
focused tests, a claim-level registry entry, release manifest, generated docs
and memory, and an empty debt ledger. CM2 is expected to be qualified if its
factor algebra survives while the coherent-medium nuclear rate and positive-
loss sweet-spot readings do not.

## Done Gate

P116 closes only when the exact typed composite, dimensions, simplification,
scale freedoms, limits, discontinuities, loss derivative and stationary
classification, actual-cycle alternative, physical countermodels, all twenty-
one predicates, dependency and consumer closure, governance records, and
downstream replay pass with no debt.

## Cross-References

See CM2, B1, BD1, LB2, PN2, PN3, PN4, T1G, C-RG-002, C-DYN-001, C-TH-001,
C-SPN-002, C-RES-001, provisional C-CMP-001, v0.95.0, and the framework-
migration effort.

## Terminal Adjudication

P116 accepts C-CMP-001 in v0.96.0 and qualifies CM2. The canonical and fresh
routes prove exact cancellation of the source's linear loss factor against its
nominal inverse-loss cycle count, strict loss decrease, positive one-sided
limits, two source-cutoff jumps, lack of any positive-loss maximizer, the
actual-cycle critical limit, dimension and scale laws, and the general changed-
loss-power stationary surface.

CM2's 21 predicates execute, but its symbolic K_pos substitution, point signs,
definition grid, floating null, lexical scans, same-call repeat, and Boolean
import marker do not validate the headline. Zero and arbitrary kinetic
prefactors block a nuclear-rate or magnitude inference. Twenty-one downstream
source consumers replay 692 checks but inherit only the conditional theorem.
The campaign debt ledger is empty.
