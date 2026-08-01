# Substrate Framework Agent Contract

This repository turns a sequential physics corpus into a self-consistent, importable, review-governed framework. Apply these rules to the entire framework. They are not a special cleanup rule for any particular late campaign.

## Definition of success

Honesty is mandatory, but honesty about failure is not completion. A failed candidate, no-go, contradiction, residual, bound, inconclusive simulation, or well-documented obstruction is attempt evidence. Preserve it and continue; never present it as the victory requested by the user.

An effort succeeds only when all of the following are true:

1. The requested positive object, mechanism, derivation, or implementation exists in its intended scope.
2. Its dependency closure comes from accepted framework claims and explicitly approved imports; no hidden fitted constant, borrowed answer, or undeclared premise remains.
3. It fits the framework's accepted invariants naturally, or a separate foundational-revision proposal has shown—independently of the favored candidate—that the invariants themselves require the smallest coherent change.
4. The strongest practical oracle validates the actual claim, and the verifier is shown to be sensitive through mutation, counterexample, convergence, limiting-case, or independent-rederivation tests as appropriate.
5. Plausible competing concepts were registered before selection and compared using predeclared structural criteria. Numerical closeness to a comparator cannot select the concept.
6. Every affected claim has been reviewed individually; an accepted proposal is not a blanket promotion of every sentence in a campaign.
7. The full downstream dependency replay passes, including units, conventions, known limits, import inventories, formal statements, tests, and generated consumers.
8. Reusable definitions and derivations live in importable modules with tests. Campaign code calls them rather than duplicating functions, constants, or proof-shaped prose.
9. The accepted claim registry, release manifest, generated documentation, and durable memory agree.
10. The debt ledger is empty: no unresolved assumptions, residuals, broken consumers, or narrative inconsistencies remain.  Resolve imported parameters when appropriate.

Only the user may change the objective or accept a reduced scope. Runtime interruption, missing authority, or an external dependency may pause execution, but it does not turn incomplete work into success.

## Authority and provenance

Use this authority order:

1. A pinned accepted release.
2. The accepted entries in `governance/claims.yaml`.
3. Adjudicated immutable campaigns supporting those entries.
4. Active proposals.
5. Append-only attempts and exploratory memory.

Chronology, commit status, prose confidence, check count, and empirical agreement do not create authority. A commit establishes provenance, not truth. A later campaign may challenge an earlier claim but cannot supersede it until review promotes the replacement claim.

Never silently edit an earlier campaign. Never edit files under `docs/generated/`. Generate canonical documentation from the registry with `scripts/render_docs.py`.

## Start every durable task this way

1. Load `.agents/skills/physics-erdos-loop/SKILL.md` for physics, derivation, simulation, formalization, campaign, claim, or framework-reconciliation work.
2. Read `governance/releases/current.yaml`, `governance/claims.yaml`, and the relevant accepted source modules.
3. Search durable memory with the bundled `memory` CLI, then verify every reused fact at its source. Memory is an index and work record, not authority.
4. Inspect git status and history. Separate committed baseline, uncommitted work, generated outputs, and attempt artifacts.
5. Instantiate the appropriate contract from `memory-templates/` before substantive work.
6. Record the exact base release, question, invariants, permitted imports, claim delta, candidate set, selection criteria, and comparator-blinding point.

If an existing result appears to solve the task, reproduce and audit it. Reuse it only if its exact claim, assumptions, and dependency closure match the current objective.

## Candidate-first, framework-fit workflow

Do not choose a concept and then retrofit the framework around it.

Before implementation:

- Define what must be explained and what remains invariant.
- Register at least two plausible candidate approaches unless a uniqueness theorem genuinely removes alternatives.
- State selection criteria before inspecting comparison values: structural fit, assumption cost, parameter economy, symmetry, dimensional consistency, limiting behavior, compatibility with accepted sectors, and predictive reach.
- Separate derivation inputs from empirical comparators. When practical, keep comparator values blinded until equations, conventions, tests, and selection criteria are frozen.

When a candidate conflicts with accepted structure, diagnose the mismatch and reject or reformulate that candidate first. Try another concept. Do not rewrite unrelated earlier claims, rename quantities, mix conventions, or add compensating assumptions merely to preserve the chosen candidate.

A foundational revision is exceptional. Open it as a separate proposal and require:

- evidence that the inconsistency exists without assuming the new candidate;
- at least two repair alternatives;
- a minimum-change rationale;
- an explicit claim and consumer migration map;
- independent review or rederivation;
- complete downstream replay before promotion.

## Claims, proposals, campaigns, and releases

Use four independent status axes for every claim:

- verification: unverified, symbolic/formal verified, numeric evidence, or simulation evidence;
- review: unaudited, audited, accepted, or rejected;
- compatibility: unassessed, native, compatible extension, or conflict;
- epistemic: proposed, active, qualified, superseded, or refuted.

Proposals use `challenges` relationships. Only an accepted replacement may use `supersedes`. A proposal may be partly accepted: promote claims individually and retain rejected candidates as historical attempt evidence.

Once adjudicated, move the campaign record into `campaigns/` without rewriting it. Create a release manifest pinning the exact claim set and source commit. `current` means the latest accepted release, never the newest directory or working-tree prose.

## Implementation architecture

- Put canonical equations, constants, units, transformations, solvers, and derivations under `src/substrate_framework/`.
- Give modules pure, documented APIs. Imports must not execute simulations or print tallies.
- Put reusable verifier machinery in shared modules; do not redefine `PASS`, `check`, solvers, or profile functions in every campaign.
- Keep exploration and orchestration in proposals/campaigns. Once accepted, extract reusable logic into the package and test it there.
- Formal developments must import shared framework definitions where practical rather than restating the entire theory in each capstone.
- Encode conventions once and test conversions explicitly. Never mix parameterizations from different readings inside one calculation.

Run impact analysis before changing a canonical symbol. Record direct consumers, indirect consumers, generated documents, formal theorems, and memory entries. After editing, replay every affected path—not only the proposing script.

## Verification is necessary, not sufficient

An `ALL N CHECKS PASS` tail proves only that those assertions executed successfully. It does not prove that the assertions test the headline claim.

For each serious claim:

- derive the checked quantity rather than hard-coding the expected result;
- confirm clean process exit and the terminal tally;
- mutate load-bearing inputs and require the relevant check to fail;
- include counterexamples or wrong-convention probes;
- run resolution/timestep/domain/tolerance refinement for numeric work;
- check dimensions, signs, symmetries, conservation laws, and known limits;
- separate exact verification from resolution-bounded evidence;
- independently rederive load-bearing normalization factors;
- inspect the precise formal theorem—proof of a weak encoding is not proof of its intended physics interpretation.

Use `src/substrate_framework/verification.py` rather than copying local check helpers.

## Continuation after failure

Attempts are bounded; the effort is not. Record attempts append-only and preserve enough detail to avoid repeating them. After any failed route:

1. Identify whether the failure belongs to the implementation, numerical method, representation, candidate concept, target statement, or accepted foundation.
2. Repair the method if it is technical.
3. Reformulate or change formalism if the representation is obstructive.
4. Reject the candidate and try another when the concept does not fit.
5. Revisit the target when it was misstated, while preserving the user's actual objective.
6. Open a separately governed foundational revision only when independent evidence requires it.

Do not lower the bar, inflate tolerances, convert a comparator into an input, or celebrate a no-go. A failure improves the next attempt; it does not finish the task.

## Memory discipline

Use memory contracts as executable working state, not as a parallel source of scientific truth.

- `efforts`: active plan, attempts, debt, and continuation state.
- `proposals`: unaccepted candidate reasoning and claim deltas.
- `claims` and `releases`: generated or synchronized summaries of accepted registry state.
- `attempts`: reusable failure mechanisms and reproduction commands, clearly noncanonical.

Never merge old and new prose into a single timeless memory entry. Preserve provenance and status. Generate canonical memory from accepted claims; keep proposal and attempt memory visibly separate. Re-source paths, commits, equations, and verdicts before updating memory.

Do not copy personal or historical memory into this repository. The bundled CLI is code only.

## Required validation before commit or promotion

Run:

```bash
scripts/validate.sh
python3 -m pytest
git diff --check
```

Also run every targeted scientific verifier and downstream consumer named by the claim delta. Before promotion, ensure generated files are current, the registry validates, the release claim set is closed, and the working-tree diff contains no unrelated or host-specific artifacts.
