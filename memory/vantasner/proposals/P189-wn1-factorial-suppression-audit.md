---
description: Audit WN1 and derive a normalization-complete exact factorial-suppression ledger
author: vantasner
created: '2026-08-11T14:58:00Z'
updated: '2026-08-11T15:52:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-WN1
- factorial-suppression
- cosine-vertices
category: proposals
confidence: established
status: archived
---
# P189 WN1 Factorial-Suppression Audit

## Question and Positive Deliverable

P189 must determine whether WN1 adds a distinct reusable exact theorem for the
squared magnitude and rigorous decimal suppression of factorial cosine
coefficients. The positive deliverable is a normalization-complete exact ledger
that either promotes a genuinely new universal bound with an importable API or
proves that accepted C-SG-019 and elementary mathematics already own the full
surviving object. Merely observing a tiny value, underflow, or an unsupported
physical rate interpretation does not close the campaign.

## Base Release and Provenance

The accepted base is v0.139.0 at clean framework commit
`33fd27ca4f523536fec08e01a644c15b1e473f96`, with 179 accepted claims and
current-manifest SHA-256
`0617c10955594b30c6d0d122476e360494d9e1b065efdf4f5c67728583388bb8`.
The registry SHA-256 is
`0281b2d981c20237bcf25271a3ae601aa5202787760921ecdb78c685168a3f7d`.
The predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.

WN1 is pending at
`merged-framework/bridges/phase-37/bridge_WN1_vertex_coefficient_magnitude.py`,
SHA-256
`3764b29955c3bd51c10278159e08a52ff616a7041510e56917b091f1a802cdde`,
size 13,511 bytes, blob `c154cf916571b8e7e07c0ac19771123165fc5f6e`,
and sole history commit `7222eed`. The target source path is clean at the
governed predecessor commit.

PN1 is qualified through C-SG-019 at SHA-256
`f2fcd58c97b9e9aa0b92e0ece9d92ff6c7ddaddec1b385b10a68a156ac3df985`.
PN2 is qualified without an accepted claim at SHA-256
`66eaa13faaba5bc3ff22d3515e04136b48a1f5a885f7ebfdc980931063c07b3a`.
PN3 is qualified through C-SPN-002 at SHA-256
`da472079f418368926e27d22567cdf3ad8f32c836146ed8107ae2874f377b58b`.
Their adjudications, the accepted claim statements, `cosine_vertices.py`, its
focused tests, durable decisions, queue, and memory search results were checked
at source before this contract.

No fresh blinding is possible. While identifying the regenerated next queue
unit after P188, WN1's body was accidentally displayed before P189's contract.
The queue and prior records already exposed the unit coefficient square,
factorial inequality, PN2 decade band, arbitrary-precision exponents, and
underflow demonstration. This exposure is preserved rather than concealed;
candidate selection is structural and freezes before implementation or source
execution.

## Invariants, Conventions, and Allowed Imports

C-SG-019 owns the exact classical coefficient of
`A*(1-cos(phi0+a_H*H+a_L*L))`. At zero background the one-high coefficient is
zero for even `n` and, for odd `n`, equals
`A*(-1)^((n-1)/2)*a_H*a_L^n/n!`. Its squared magnitude therefore retains
`A^2*a_H^2*a_L^(2n)/(n!)^2`; WN1's `1/(n!)^2` is only the unit specialization.
C-SG-019 explicitly supplies no quantization, matrix element, phase space,
transition rate, material realization, or nuclear process.

PN2 supplies qualified quotient/remainder bookkeeping only. It constructs no
quantum subdivision process, physical mode, energy band, state, or channel.
C-SPN-002 supplies exact normalized symmetric-spin algebra but states that a
squared ladder coefficient is not a rate and leaves the interaction,
resonance, spectral density, linewidth, Golden-rule regime, and material map
free. C-BRN-001 likewise treats a proposed weight as supplied rather than
derived.

For every positive integer `n`, the positive exponential series contains the
term `n^n/n!`, so `e^n>n^n/n!`, `n!>(n/e)^n`, and
`1/(n!)^2<(e/n)^(2n)`. A finite grid is regression evidence, not the proof.
Exact rational and integer inequalities are the preferred oracle. In
particular, an exact rational upper bound on `e` plus an integer power
comparison can prove the three decade exponents without treating mpmath digits
as rigorous merely because their precision is high.

P189 may use exact positive-integer factorial, exponential-series, rational,
logarithm, monotonicity, and integer-power algebra. Amplitude, coordinate
scales, background, order, decade inputs, and any physical mapping remain
separately supplied. Float underflow or overflow is representation evidence;
the exact rational stays positive. Mutable quadrature uses `np.trapezoid` or
`trapezoid_integral`; any immutable legacy-name stop is alias-replayed and
cannot reject a scientific candidate.

## Candidate Preregistration

The candidate set separates literal reproduction, accepted composition, a
possible distinct factorial theorem, an exact decimal route, numerical
regression, physical-typing countermodels, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Hash-pinned WN1 reproduction | Source conventions | Source symbols and literals | Tally may pass while universal and physical predicates remain weaker than claimed | AST, runtime, import, assertion, and conclusion-edge audit |
| B | Accepted composition only | C-SG-019 plus approved elementary mathematics | General coefficient coordinates | No new claim if the bound adds no reusable semantics | Claim, API, test, campaign, and consumer nonduplication review |
| C | Exact factorial-suppression theorem | Positive integer order and declared coefficient magnitude | Order and normalization coordinates | C-CMB-001 only if universal squared, exponential, decimal, and representation ceilings are distinct | Exact API, symbolic proof, consumers, and mutations |
| D | Exact decade bound | Rational upper bound on `e` and integer block comparison | Integer decade | Source exponent thresholds follow without decimal trust | Rational series proof and exact integer inequality |
| E | High-precision numeric route | Declared precision and enclosure | Evaluation precision | Regression only, subordinate to exact D | Precision refinement and independent log-gamma comparison |
| F | Physical-typing countermodels | Same coefficient with missing or varied quantum data | Amplitude, scales, states, spectral factor | Magnitude does not become a rate or physical band | Zero interaction, zero spectral density, coordinate rescaling, and background mutations |
| G | Governed closure | Authority and evidence paths | None | Terminal status only after complete source and consumer replay | Registry, queue, release, memory, compatibility, and debt checks |

## Selection Criteria and Blinding

Selection is ordered by exact universal quantifier and bound direction;
compatibility with C-SG-019's normalization, background, and coordinate scales;
rational or integer proof before decimal evaluation; correct typing of
amplitude, matrix element, rate, and probability; PN2 and C-SPN-002 ceilings;
the `n=1`, even-order, large-order, rescaling, and underflow limits; assumption
and API economy; independent derivation and mutation sensitivity; and novelty
plus consumer closure. Familiarity with Stirling's formula, the smallness of a
number, a green tally, or agreement with exposed exponents cannot select a
candidate.

No comparator blinding is claimed because WN1's source result was exposed
before this freeze. The meaningful freeze point is this contract before any
P189 code, exact proof object, source execution, predicate decision, or
consumer selection is created.

## Proposed Claim Delta

P189 provisionally reserves C-CMB-001 for a distinct exact positive-integer
factorial-suppression theorem only if Candidate C adds reusable semantics and
consumers beyond C-SG-019. Registry, campaign, proposal, package, test, and
durable-memory searches find no identifier collision. If the surviving result
is only accepted composition plus standard elementary mathematics, the
identifier remains reserved and unpromoted. No `supersedes` edge is proposed.

Likely consumers include WN1, later WN magnitude and branching units, PN/CM/GB
weight narratives, exact-asymptotic helpers, governance, generated records,
and durable memory. Physical rate or subdivision narratives cannot count as
accepted consumers unless their missing states, interaction, and spectral
premises are independently governed.

## Implementation and Oracle Plan

The source audit will pin syntax, imports, compatibility, native execution,
every coefficient, factorial, square, exponential-series statement, finite
grid, decimal exponent, underflow path, predicate, and headline conclusion.
Reusable code is added only if nonduplication establishes a distinct theorem.

SymPy exact rational and integer algebra is the strongest practical oracle for
the coefficient square, exponential-series term bound, bound direction,
normalization dependence, rational upper bound on `e`, and integer decade
exponents. A candidate package API may expose the exact normalized weight,
general normalization ledger, exponential upper bound, and exact decade
exponent ceiling. A raw independent route will reconstruct the proof without
importing the new API or the primary verifier.

The exact decade route will prove a rational upper bound on `e` from a finite
series plus a geometric tail, prove the required fixed integer power
comparison, and group `n=10^d` into exact blocks. Mpmath or log-gamma values,
if replayed, receive declared precision, independent comparison, and an error
enclosure and remain numeric regression evidence only. No numeric check is
promoted to a universal exact theorem.

Mutations change coefficient versus derivative normalization, parity,
background, amplitude, high and low coordinate scales, the square, factorial
power, inequality direction, exponential base, decade block length, and
threshold exponent. Zero interaction and zero spectral density preserve the
classical coefficient while nulling a conditional rate. Exact positivity at
the float-underflow order separates mathematics from representation.

Compatibility preflight audits direct, imported, dynamic, and eager-default
legacy NumPy access. Mutable code is repaired to the current API or shared
helper before science; immutable source receives alias-only replay if needed.
The source reverse graph, affected canonical APIs and tests, generated queue,
claim/release state, documentation, memory, and every propagated physical
ceiling replay before terminal promotion or disposition. One integrated gate
runs only at that scientific boundary.

## Attempts and Continuation

Attempt 0001 will freeze v0.139.0, the framework and source commits, WN1 hash,
the unavoidable pre-contract exposure, provisional C-CMB-001, seven
candidates, ordered criteria, exact oracle hierarchy, compatibility policy,
and debt before any P189 implementation or source execution. Subsequent failed
proof, representation, source, novelty, or verifier routes remain append-only
and must name the layer and materially different continuation.

Attempt 0002 passes native reproduction in 0.35 seconds with 44 runtime checks
from twenty static call sites, fourteen literal labels, six dynamic labels, and
zero assertions. WN1 imports only sys, SymPy, and mpmath and has no NumPy
compatibility surface. The unit-background coefficient grid, selected inverse-
square factorial values, exact finite decimal floors, and exact positivity at
the float-zero order survive.

The source tally does not encode three headline quantifiers. Eight exact
partial sums are regression evidence for the exponential-series argument, not
a universal proof. Four moderate-order and three decade comparisons use
sixty-digit mpmath values without an interval enclosure. The function named
`decays_superpolynomially` checks only order 21 against powers two, four, and
eight. P189 will replace those finite predicates with an analytic positive-
series proof, an exact rational/integer decade proof, and a geometric tail
proof for every fixed nonnegative power. The Golden-rule weight and physical
PN2-band readings remain rejected unless their missing state, interaction, and
spectral premises are supplied.

Attempt 0003 freezes the distinct exact candidate before implementation.
For `q_n=1/(n!)^2`, the recurrence is
`q_(n+1)/q_n=1/(n+1)^2` and positivity of the exponential series gives the
strict universal bound `q_n<(e/n)^(2n)`. For every fixed nonnegative integer
`p`, the ratio of `n^p q_n` at consecutive orders is at most
`2^p/(n+1)^2`; beyond an exact integer threshold it is at most one-half, which
proves superpolynomial decay by a geometric tail rather than selected samples.

The exposed decimal thresholds also admit an exact route. The exponential
series through order three plus a geometric tail gives
`e<49/18<11/4`, and the integer inequality `(11/4)^20<10^9` has positive
numerator margin 426,761,632,843,439,990,799. For `n=10^d`, grouping the
power into blocks of twenty yields
`q_n<10^-((20d-9)n/10)`, exactly reproducing the conservative exponents
-131,000,000, -17,100,000,000, and -2,110,000,000,000 for decades seven,
nine, and eleven. C-CMB-001 is provisionally distinct from C-SG-019 and has
four direct plus eight transitive source consumers; implementation and
independent verification remain open.

Attempt 0004 implements the distinct surface in the pure
`factorial_suppression.py` module and exports eight public names. The API
composes the accepted general cosine coefficient rather than copying it, uses
exact rational or integer comparisons for decimal floors and decade bounds,
and exposes a constructive half-tail certificate for arbitrary fixed
nonnegative powers. Seventy-six focused tests and all eight public imports
pass.

The 67-check primary oracle and a raw 27-check independent rederivation pass.
They derive the rational exponential tail, twentieth-power integer margin,
recurrence, universal reciprocal direction, general normalization, background
sensitivity, exact decade exponents, geometric limit, and zero-interaction and
zero-spectral-density countermodels. The independent route imports neither the
new module nor `cosine_vertices.py`. The first primary run stopped only because
two structurally equal SymPy ratio forms were compared by raw equality; the
repair uses `combsimp` and changes no scientific statement.

This pass also removed validation theater discovered during implementation:
three hard-coded proof-verdict booleans were deleted from the data objects, a
nonempty symbolic inequality probe was replaced by the explicit positive
reciprocal-gap identity, and twenty-five repeated per-power review tallies were
collapsed into one constructive check. Compatibility audit finds no NumPy
surface in WN1 or the mutable implementation and verifiers. GitNexus reports
low process risk but does not see the untracked new files or known pytest
consumers, so its limitation is recorded and cannot substitute for source and
test replay.

Attempt 0005 promotes C-CMB-001 individually in v0.140.0 and qualifies WN1
through C-SG-019 plus the new theorem. All thirteen hash-pinned source nodes
replay 568 native checks, while the final governed graph adds 47 checks that
prove every one of the twelve consumers remains pending and unpromoted. The
queue closes at 35 pending and 170 qualified units, and generated documentation
and accepted memory agree with the 180-claim registry.

The single integrated boundary validates 773 memory records and passes all
1,659 repository tests in 178.29 wall-clock seconds with exit zero and 214,836
KiB peak RSS. The unchanged full suite is not rerun after this record-only
closure. No equation, predicate, tolerance, compatibility decision, or
scientific threshold changes during promotion.

## Debt Ledger

The P189 ledger tracks source reachability, coefficient normalization,
factorial powers, universal quantifiers, exact versus decimal bounds, underflow,
physical rate typing, dependency and consumer authority, compatibility, and
governed-state agreement.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Source body was exposed before the P189 contract | Record exposure and make no blinding claim | disclosed in base provenance and comparator freeze |
| WN1 predicates, imports, runtime, and conclusion edges are unaudited | Pin and adjudicate every executable and narrative edge | discharged by attempt 0002 and the source, reproduction, compatibility, and check audits |
| Unit normalization may erase amplitude and coordinate scales | Derive the general C-SG-019 magnitude ledger and mutate every scale | discharged by exact API, background and scale mutations, and both oracles |
| A finite exponential grid may masquerade as a universal proof | Supply an analytic positive-series proof and sensitive direction countercheck | discharged by the positive-series and reciprocal-gap proof with mutations |
| Arbitrary-precision digits may masquerade as a rigorous bound | Derive exact rational and integer exponent bounds or give explicit enclosures | discharged by 49/18, 11/4, and the integer twentieth-power proof |
| Squared classical coefficient may be called a Golden-rule rate | Type every state, interaction, normalization, spectral, and validity premise or reject the reading | discharged by two null countermodels and explicit ceilings across all twelve consumers |
| PN2 decade inputs may be called a physical subdivision prediction | Preserve PN2's qualified bookkeeping ceiling and treat band values as supplied examples only | discharged by the API, claim review, and consumer graph |
| C-CMB-001 may duplicate C-SG-019 or elementary math | Complete claim, API, test, and consumer nonduplication review before implementation or promotion | discharged by individual claim review, exact API, and twelve-consumer ceiling replay |
| Legacy NumPy access may masquerade as science | Repair mutable code or alias-replay immutable legacy access without candidate rejection | discharged across WN1, all twelve consumers, and mutable P189 code with zero version events |
| Dependencies, consumers, disposition, generated state, and memory may disagree | Replay the graph and synchronize every terminal record with materialized evidence | discharged by the 47-check governed graph and v0.140.0 transaction |

## Review and Promotion Plan

C-CMB-001 receives individual four-axis review only if the exact novelty, API,
and consumer gates pass. Otherwise its identifier remains reserved and the
accepted composition is reviewed without registry sprawl. WN1 receives a
predicate-level verdict for each coefficient, factorial, bound, finite sample,
decimal exponent, underflow result, imported band, rate label, and physical
conclusion.

If a distinct theorem survives, its pure package API and exact tests precede
claim promotion, followed by primary and independent exact verification,
impact analysis, complete reverse-consumer replay, registry and release
closure, generated documentation, accepted memory, and one integrated gate.
A no-new-claim route still requires terminal WN1 disposition, queue, memory,
compatibility, consumer, and debt closure with materialized evidence paths.

## Done Gate

P189 closes only when the normalization-complete factorial ledger exists, the
universal inequality is proven rather than sampled, decimal exponent claims
have exact or enclosed support, underflow is correctly typed, every physical
rate and subdivision premise has a verdict, competing candidates and
mutations are adjudicated, consumers replay, governed state is synchronized,
and the debt ledger is empty. A failed physical interpretation is attempt
evidence and cannot substitute for the positive exact object.

This gate is satisfied by attempts 0004 and 0005. C-CMB-001 is accepted in
v0.140.0, WN1 is qualified, all debt rows are discharged, and the parent
migration continues with WN2.

## Cross-References

See C-SG-012, C-SG-019, C-SPN-002, C-BRN-001, P090, P109 through P111,
PN1 through PN3, WN1 and its reverse consumers, `cosine_vertices.py`, and the
framework-migration effort.
