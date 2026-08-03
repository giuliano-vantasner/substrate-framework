---
description: Exact finite-scanner semantics, AST comparison, and CM6 honesty-firewall audit
author: vantasner
created: '2026-08-08T09:00:00Z'
updated: '2026-08-08T09:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- source-audit
- honesty-firewall
category: proposals
confidence: exploratory
status: active
---
# P120 CM6 Honesty Firewall Audit

## Question and Positive Deliverable

This campaign must produce an exact independently checked account of CM6's
finite scanner: its files, bytes, normalization, tokens, exemptions, match
locations, error behavior, and all twenty runtime predicates. It must compare
that proposition with AST and data-flow-sensitive alternatives and terminally
adjudicate CM6. A passing source tally or a catalog of scanner evasions does
not replace the positive semantic ledger and source disposition.

## Base Release and Provenance

The accepted base is v0.97.0 at parent checkpoint
`5a2be849f9599d1ed71c6e8784d1e716e792c9f1`, whose latest scientific
adjudication is `cb08beb439f15c65f1994739cac542ef8ad427c3`. CM6 is the next
pending unit at
`merged-framework/bridges/phase-31/bridge_CM6_honesty_firewall_guard.py` in
source commit `6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, pinned by SHA-256
`60a8d1de7693783c7859d32b5d7b90bd46c6304cbd7c14fd06fb5235acadf3c5`, git
blob `7d6d3b0d3229941efa54dad7fa2480258f79851f`, and size 10,963 bytes.

Fresh body and output blinding is impossible. Provenance searches partially
exposed CM6, and P116, P118, and P119 repeatedly executed its twenty checks as
a downstream consumer. The generated queue exposes its forbidden-token,
clamp-token, empirical-token, partition, exemption, injection, and tally
summaries. P120 records that exposure rather than disguising it and freezes
all structural gates before renewed line-by-line inspection or execution.

The direct accepted authority read for the freeze is v0.97.0, C-SCR-001 and
`screened_barrier.py`, C-CMP-001 and `composite_factors.py`, C-RES-001 and
`paired_resolvent.py`, plus the exact claims mapped to CM4 and CM5. CM1, CM2,
CM4, CM5, and CM7 become pinned scan inputs only after freeze; CM7 remains
pending and grants no authority. Memory search found the parent done gate and
accepted review cross-references, which were rechecked at their registry and
module sources. Unrelated dirty Phase 47/48 work and the source compatibility
overlay remain excluded from authority.

## Invariants, Conventions, and Allowed Imports

A literal scanner establishes only a proposition over its declared finite
bytes, paths, decoding, normalization, token list, exemption rule, and matcher.
Case folding, Unicode normalization, whitespace, punctuation, substring versus
token matching, line splitting, comments, docstrings, string constants,
identifiers, imports, generated names, aliases, runtime attribute access, and
external data are distinct conventions or locations.

An `[IMPORT]` marker is metadata only and cannot authorize executable code or
all other content on its line. Constructed strings, aliases, equivalent
formulas, helper calls, `getattr`, imported constants, configuration files, and
data-flow dependencies can preserve semantics while evading a token list.
Conversely, benign identifiers, quoted or negated prose, documentation, and
counterexamples can collide with substring matching. Both directions require
mutations.

Missing `min(cap)`, `cap=`, or `ceiling=` text cannot establish an uncapped
function: clipping, maxima, branches, helpers, bounded nonlinearities,
denominators, domains, and lookup tables are alternatives. Missing empirical
words or numeric literals cannot establish data independence: a closed input
inventory and provenance or data-flow audit is required. File lists and hashes
are part of the proposition, and unscanned imports, generated files, dynamic
loads, read errors, symlinks, or later revisions remain outside it.

C-SCR-001, C-RG-002, C-SPN-002, C-CMP-001, C-GW-001, C-COH-001, C-SG-017,
and C-RES-001 retain their exact scopes and physical ceilings. Python lexical
rules, `ast`, finite-set logic, explicit counterexample programs, and pinned
source bytes are allowed. Dependency cycles are provenance only, and prior
source executions may regress frozen behavior but cannot select a conclusion.

## Candidate Preregistration

The candidate set separates literal reproduction, an exact finite lexical
statement, AST location classes, evasion and collision mutations, scope
closure, semantic clamp and empirical audits, novelty, and independent review.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Reproduce all twenty CM6 predicates | Pinned source conventions only | Source file lists and tokens | Regression evidence only | Clean hash-pinned exit plus predicate ledger |
| B | Exact finite lexical theorem | Declared decoding, normalization, line, substring, token and exemption rules | File bytes and token sets | Valid only at its stated finite scope | Independent matcher and exhaustive match-location comparison |
| C | AST location classification | Syntactically valid scanned Python | Node and source-location classes | Better separates executable syntax from prose | Names, attributes, calls, constants, comments and docstrings compared |
| D | Evasion and collision suite | Explicit mutated programs | Construction, aliases, case, Unicode, whitespace, prose and tags | Literal scanner is incomplete and nonspecific semantically | Each mutation changes the appropriate oracle verdict |
| E | Scope-closure audit | Declared files, imports, loads and error policy | Paths, hashes and dependency edges | Fixed source list is not transitive closure | Omitted module, configuration, dynamic-load and read-error probes |
| F | Clamp and empirical semantic audit | Explicit alternative programs and input graphs | Saturator and external-data forms | Token absence does not prove uncapped or data-free behavior | Equivalent saturation and imported-input countermodels |
| G | Governance reuse or campaign-local result | Exact accepted-state comparison | no new parameter | Preferred if no scientific theorem or consumer remains | Claim and validator nonduplication audit |
| H | Independent rederivation and closure | No P120 implementation reuse | none | Required for terminal disposition | Fresh matcher, AST classification, predicate and consumer replay |

## Selection Criteria and Blinding

Candidates are ranked first by exact closure over files, hashes, decoding,
normalization, token sets, exemptions, matching locations, and errors. Next
come sensitivity to semantic evasions and specificity against prose or benign
collisions, relevance to executable behavior, honest separation from physical
claims, accepted dependency closure, parameter economy, reusable API value,
mathematical or governance novelty, and complete consumer review. The green
twenty-check tally cannot select a candidate.

No fresh source-output blinding is claimed. File, byte, case, substring, line,
tag, comment, AST, alias, construction, Unicode, clamp, empirical, data-flow,
scope, error, cycle, predicate, and consumer gates are frozen before dedicated
line-by-line CM6 inspection, renewed execution, or more consumer output review.

## Proposed Claim Delta

No claim identifier is proposed at freeze. Candidate G predicts that a finite
lexical scan is governance evidence rather than a scientific theorem and that
the surviving physical ceilings are already governed by accepted claims. A
new identifier or canonical API will be considered only if a distinct positive
statement has reusable consumers and complete semantic scope.

The mandatory source delta is a terminal CM6 disposition with all twenty
predicates, token lists, exemptions, files, dependencies, cycles, and direct
and transitive consumers reviewed. Existing accepted claims are reviewed
individually and never blanket-promoted through a scanner tally.

## Implementation and Oracle Plan

The primary route will reproduce CM6's exact matcher and independently compute
every match location over the pinned source bytes. It will expose case,
substring, line, tag, comment, decoding, missing-file, and error semantics. A
separate AST route will classify imports, names, attributes, calls, literals,
comments, and docstrings without importing or executing scanned modules.

Load-bearing mutations construct forbidden text by concatenation, use aliases,
`getattr`, equivalent formulas, case and Unicode variants, whitespace and
punctuation, comments, docstrings, quotations, negation, benign substring
collisions, and `[IMPORT]` smuggling. Scope mutations move behavior into an
unscanned helper, configuration file, dynamic import, generated module, and
read failure. Clamp mutations use `np.clip`, `max`, conditionals, helpers,
bounded nonlinearities, denominators, domains, and tables. Empirical mutations
load identical values through imports, environment, configuration, or arrays.

The exact source matcher and independent implementation are the right finite
oracles; AST supplies a stronger syntactic comparison but is not full semantic
data flow. Explicit counterexample programs decide the overclaims. Numerical
integration, SymPy, SciPy, and Lean are unnecessary because the obligations
are finite text, syntax, provenance, and governance statements.

If a reusable repository-wide scanner survives, it must live in an importable
module with focused tests and explicit limitations. Otherwise the logic stays
inside immutable P120 evidence to avoid inventing a canonical API with no
scientific consumer. Compatibility preflight still searches executed scripts:
mutable numerical code must use `np.trapezoid`, canonical integration uses
`trapezoid_integral`, and immutable `np.trapz` receives alias-only replay. CM6
itself is expected to require no quadrature, and an API-version abort cannot be
classified as scientific failure.

The primary and independent verifiers, targeted accepted tests, hash-pinned
direct and transitive consumers, governance validator, regenerated queue and
memory checks, one final `scripts/validate.sh`, and `git diff --check` form the
terminal boundary. The full workflow runs once at adjudication, not after each
preserved attempt.

## Attempts and Continuation

Every failed route is appended under P120 with its command, diagnosis,
scientific effect, and next candidate. Matcher, AST, fixture, or governance
defects are repaired without weakening the intended statement; semantic
failure rejects the overclaim while preserving the exact finite result.

## Debt Ledger

The ledger tracks source bytes and paths, decoding, normalization, token and
substring rules, exemptions, comments, docstrings, strings, executable
locations, aliases, construction, Unicode, errors, file closure, imports,
dynamic loads, external inputs, clamp semantics, empirical provenance,
dependency cycles, false positives, false negatives, parameters, residuals,
and broken consumers. It is empty at freeze and must be empty at adjudication.

## Review and Promotion Plan

Claim-level review will compare both scanner routes and the counterexample
suite with accepted claims and existing repository validators before any
registry edit. The source audit will classify all twenty predicates and every
barrier, clamp, empirical, partition, import-exemption, self-test, and honesty
statement separately. Direct and transitive candidate consumers replay from
pinned hashes, and cycles remain provenance only.

If a distinct scientific claim survives, promotion requires a canonical
module and tests, immutable P120, a release, generated documentation and
accepted memory, CM6's disposition, regenerated queue, and complete validation.
If the exact finite result is governance evidence only, P120 closes as an
immutable no-release campaign with CM6 qualified through accepted claims and
explicit semantic ceilings. A final gate attempt starts in progress, is
finalized after clean exit, and receives only record-sensitive checks later.

## Done Gate

P120 closes only when exact finite-scanner and AST-location ledgers exist; all
evasion, collision, scope, clamp, empirical, and error mutations are decided;
every predicate, dependency, cycle, input, and consumer is audited; novelty is
decided against accepted claims and validators; the physical and governance
ceilings are explicit; canonical state agrees; validation is sensitive; and
the debt ledger is empty. A green lexical self-test, a scanner no-go, or a
well-documented overclaim alone is not completion.
