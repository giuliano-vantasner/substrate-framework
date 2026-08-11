# Substrate Framework Agent Contract

This repository turns a sequential physics corpus into a self-consistent, importable, review-governed framework. Apply these rules to the entire framework. They are not a special cleanup rule for any particular late campaign.

New contributors begin with [`AGENTS_START_HERE.md`](AGENTS_START_HERE.md) for
the operational collaboration, memory, GitNexus, skill-selection, PR, and
review workflow. This file remains the normative scientific and governance
contract when the two documents differ.

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

These gates govern declaring the objective complete and promoting its headline claims. They are not a universal pull-request merge gate. Use `.agents/skills/research-pr-harvest/SKILL.md` to extract locally correct, novel, reusable units from an incomplete campaign while leaving its goal open. A merge creates provenance and reusable code, not accepted scientific authority. Missing parts of the larger goal are campaign frontier, not debt; debt is an unresolved defect, hidden assumption, broken consumer, or unsupported promise inside the scope being merged or promoted. Every harvest PR must name its canonical goal issue, and the final disposition must update that issue with unit-level lists and rationales for what merged, what requires refactor, and what remains only in PR history, plus landed links and the next decisive action.

Every pull request, including documentation, tooling, compatibility, harvest, and scientific work, must name exactly one canonical issue that existed before the PR was submitted. A contributing agent may create that issue. There are no standalone-PR exceptions. The issue must state the positive objective, scope, success gate, dependencies, and coordination boundary; use `Advances #N` while work remains and `Fixes #N` only when the full objective is complete.

An agent must never merge a PR that it opened, authored a commit for, or materially implemented. The PR must be reviewed and merged by a distinct agent or repository owner. If the authoring agent also performs substantive corrective work during review, merge authority remains with another actor. When no distinct merger is available, leave the validated PR ready for handoff rather than self-merging it.

Merged same-repository PR head branches are transient and must not accumulate as a parallel discovery surface. Repository GitHub settings delete them automatically after merge; the distinct merger must verify that cleanup and may delete only the exact merged head if automation did not. Durable provenance lives in the merge commit, PR, canonical issue handoff, and landed `main` history. Preserve `main`, protected branches, open PR heads, and closed-unmerged or failed branches by default; deleting or retiring any of those requires an explicit owner decision. Branch cleanup never permits force-pushing, deleting an unverified or unrelated branch, or treating branch deletion as scientific adjudication.

When the user supplies a pull-request URL or number to an agent that did not author or materially implement that PR, treat it as standing authorization to process the PR autonomously through the normal repository lifecycle: inspect, review, comment, correct PR metadata, create a focused harvest branch or follow-up PR, merge or close according to the evidence, and update the linked issue. Do not pause for routine operator confirmation. This authorization never overrides the non-self-merge rule and does not permit force-pushing a contributor branch, deleting unrelated branches, changing the user's objective, or promoting a claim that has not passed governance.

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
2. Read `governance/releases/current.yaml`, `governance/claims.yaml`, and the relevant accepted source modules. For predecessor migration, also locate the source unit in `migration/source-claims.yaml` and read its current disposition and scope policy.
3. Search durable memory with the bundled `memory` CLI, then verify every reused fact at its source. Memory is an index and work record, not authority.
4. Inspect git status and history. Separate committed baseline, uncommitted work, generated outputs, and attempt artifacts.
5. Instantiate the appropriate contract from `memory-templates/` before substantive work, validate its matching proposal manifest with `scripts/validate_repository.py`, and do not open the source body or comparator values until that schema gate passes.
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

Claim identifiers are durable provenance keys even when a proposal was rejected and never entered `governance/claims.yaml`. Before allocating an identifier, search the registry, campaigns, and durable memory; never reuse a provisional, rejected, refuted, superseded, or accepted identifier for a different statement.

Migration dispositions are decisions, not queue labels. `qualified`, `refuted`, `duplicate_evidence`, and `out_of_scope` units must name their disposition-specific reason and durable evidence paths; use `qualified` for mixed units that also map accepted claims. Never clear a source unit with an unsupported terminal word.

Once adjudicated, move the campaign record into `campaigns/` without rewriting it. Create a release manifest pinning the exact accepted claim set and source commit. Release membership follows the independent review/acceptance decision (and `accepted_in`), not an `epistemic: active` filter: a current release may retain accepted `qualified` claims. Use the registry/release validator for closure instead of an ad hoc status subset. `current` means the latest accepted release, never the newest directory or working-tree prose. When a campaign migrates predecessor material, edit only `migration/dispositions.yaml` and regenerate `migration/source-claims.yaml`; never hand-edit that generated queue. Partial migration must name the unaccepted remainder rather than marking a whole bridge complete.

## Implementation architecture

- Put canonical equations, constants, units, transformations, solvers, and derivations under `src/substrate_framework/`.
- Give modules pure, documented APIs. Imports must not execute simulations or print tallies.
- Put reusable verifier machinery in shared modules; do not redefine `PASS`, `check`, solvers, or profile functions in every campaign.
- Campaign verifiers execute with `PYTHONPATH=src`; do not import repository `scripts/` as Python modules. Extract reusable logic into `src/substrate_framework/` and keep scripts as CLI adapters. Pin the campaign's own source and accepted release, but do not assert that unrelated queue units remain pending or that mutable `current` forever equals a historical release. Replay an immutable historical verifier only against durable snapshots it was designed to consume; otherwise replay its canonical modules and tests without rewriting the campaign.
- Reuse `src/substrate_framework/numerics.py` for SciPy IVP, BVP, method-of-lines, refinement evidence, and sampled trapezoidal integration. Canonical modules call `trapezoid_integral`; mutable standalone scripts targeting the current environment call `np.trapezoid`, never the removed `np.trapz`. Compatibility preflight must inspect executable syntax for both direct `np.trapz` and dynamic `getattr(np, "trapz")` access. In particular, never write `getattr(np, "trapezoid", getattr(np, "trapz"))`: Python evaluates that legacy default eagerly. Use the canonical helper or a two-step `None` fallback. Keep exact tractable integrals symbolic, and keep the spatial operator, boundary data, error metric, and physical pass criteria explicit in the claim module.
- Keep exploration and orchestration in proposals/campaigns. Once accepted, extract reusable logic into the package and test it there.
- Formal developments must import shared framework definitions where practical rather than restating the entire theory in each capstone.
- Encode conventions once and test conversions explicitly. Never mix parameterizations from different readings inside one calculation.

Run impact analysis before changing a canonical symbol. Record direct consumers, indirect consumers, generated documents, formal theorems, and memory entries. After editing, replay every affected path—not only the proposing script.

## Verification is necessary, not sufficient

An `ALL N CHECKS PASS` tail proves only that those assertions executed successfully. It does not prove that the assertions test the headline claim.

Choose the oracle by the mathematical claim, not by a preferred tool. Use SymPy for exact identities, substitutions, series, and analytic limits; Lean for finite formal statements whose exact encoding and axioms can be audited; and NumPy/SciPy for roots, spectra, quadrature, optimization, ODEs, boundary-value problems, and discretized PDEs without a tractable closed form. Not every proof obligation belongs in SymPy or Lean. Conversely, a SciPy result earns numeric or simulation evidence only: it never becomes exact merely because tolerances are tight.

Do not simulate a conclusion already fixed by stronger exact evidence. If exact elimination removes a parameter from an ODE right-hand side, local uniqueness—not duplicate integrations with two parameter values—establishes same-data trajectory independence. Before calling a downstream tail, dispersion, normalization, or consistency check independent, eliminate its shared intermediate variables and compare the resulting equations or positive solution sets; an algebraically equivalent condition is regression coverage, even when presented in different coordinates. Prefer exact parameter sensitivity or an initial Taylor-coefficient separation for a counterexample; simulate only behavior that remains analytically unresolved.

Cross-sector coefficient matching must type the fields, kinetic metrics, action measures, and coefficient conversions on both sides. A shared symbol, functional shape, or mass dimension is necessary evidence at most; it is not a field map, dimensional-reduction theorem, physical identification, or parameter derivation.

Structural checks must evaluate the actual construction. A literal `True`, a stand-in constant that omits the claimed object, a copied expected period, or a bounded sample unrelated to the defining predicate is provenance evidence at most, not a verifier. For differential forms, enumerate every graded Leibniz and cyclic-reordering term before combining coefficients. Test pointwise nonvanishing, local closedness, global non-exactness, period normalization, extension ambiguity, and gauge descent as separate obligations; none implies the next merely because a familiar formula is printed.

For ODE, BVP, PDE, quadrature, and spectral work, state the equations, domain, initial/boundary data, discretization, floating-point precision, solver, tolerances, mesh, timestep or sampling policy, stopping rule, and error norm. Predeclare thresholds against a dimensional or scale-relative error model; an absolute near-zero threshold is not meaningful without the observable scale. If such a threshold fails, preserve it, demonstrate refinement or roundoff behavior, and only then replace it with a justified scale-sensitive oracle while keeping any exact null as a separate analytic claim. Check solver success before using its output. Run mesh/timestep/domain/tolerance refinement, test conservation or controlled dissipation, compare an independent method or soluble limit, and show that load-bearing input mutations break the relevant verdict. Use sparse operators and method-of-lines or an appropriate finite-difference, finite-volume, finite-element, or spectral method when the PDE requires them; tool choice follows the equation and claim.

Before FFT differentiation or line-power attribution, prove that the sampled window is periodic for every active frequency or quantify endpoint closure and use a nonperiodic method. Multiplying a coefficient from the same FFT by `(i*omega)^n` is an internal identity, not an independent derivative oracle. Resolve mixed or incommensurate frequencies and show the claimed line carries the preregistered fraction of the checked norm or power.

For each serious claim:

- derive the checked quantity rather than hard-coding the expected result;
- confirm process status zero and the terminal tally independently; inventory lexical check-call sites, runtime check executions, and assertion nodes separately, and never force those counts to agree when loops or dynamic dispatch legitimately multiply executions; never pass a positive check count through `SystemExit` as though it were a success code;
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

Classify environment compatibility before scientific failure. Detect direct `np.trapz`, imported `trapz`, and dynamic `getattr(np, "trapz")` access before execution; an eager nested default such as `getattr(np, "trapezoid", getattr(np, "trapz"))` still aborts when the legacy name is absent. If a run aborts solely for one of these version-only reasons, replace the mutable access with `np.trapezoid` or a safe two-step fallback and rerun the unchanged scientific route. For hash-pinned immutable source, preserve the native hash and diagnostic, then make an explicitly recorded alias-only compatibility replay. The native abort is compatibility provenance—not a rejected candidate, refuted claim, or terminal source disposition—and the repaired replay supplies the scientific verdict.

1. Identify whether the failure belongs to the implementation, numerical method, representation, candidate concept, target statement, or accepted foundation.
2. Repair the method if it is technical.
3. Reformulate or change formalism if the representation is obstructive.
4. Reject the candidate and try another when the concept does not fit.
5. Revisit the target when it was misstated, while preserving the user's actual objective.
6. Open a separately governed foundational revision only when independent evidence requires it.

Before inventing a replacement route, locate the nearest accepted campaign or
canonical module that solved a related obligation. Verify it at source, extract
the construction and selection logic that actually succeeded, and record both
what transfers and what does not. External research may supplement that
reconciliation, but a generic method is not a substitute for restoring the
framework's dependency, invariant, convention, and consumer context.

Do not lower the bar, inflate tolerances, convert a comparator into an input, or celebrate a no-go. A failure improves the next attempt; it does not finish the task.

Do not make durable progress wait for the final capstone. When a utility, exact local result, solver, source construction, or verifier becomes independently correct and reusable, harvest it through a focused PR or commit. Keep speculative composition and failed-route narration in PR history unless they yield a separately reusable object. An individual agent run may hand off at the last strong milestone; the campaign objective remains open for a fresh run.

## Memory discipline

Use memory contracts as executable working state, not as a parallel source of scientific truth.

- `efforts`: active plan, attempts, debt, and continuation state.
- `proposals`: unaccepted candidate reasoning and claim deltas.
- `claims` and `releases`: generated or synchronized summaries of accepted registry state.
- `attempts`: reusable failure mechanisms and reproduction commands, clearly noncanonical.

Never merge old and new prose into a single timeless memory entry. Preserve provenance and status. Generate canonical memory from accepted claims; keep proposal and attempt memory visibly separate. Re-source paths, commits, equations, and verdicts before updating memory.

For repository-local memory, pass `--base "$PWD/memory"` to search and grep. Validate one target per invocation, using an explicit repository base and an absolute target, for example `memory validate --base "$PWD" "$PWD/memory"`; use the same absolute-path form for an individual memory file. A host-level `AGENT_MEMORY_PATH` can otherwise redirect a relative target outside this repository or make a repository-relative path resolve twice.

Do not copy personal or historical memory into this repository. The bundled CLI is code only.

## Required validation before commit or promotion

For a bounded commit or pull request, run all fixed repository checks plus the
pytest files or node IDs selected from the diff, GitNexus impact analysis,
direct imports, named scientific verifiers, and affected consumers:

```bash
scripts/validate.sh --pytest-scope tests/test_affected_module.py [more selectors ...]
git diff --check
```

The non-pytest repository, generated-state, memory, skill, import, and compile
checks run in both modes. A scoped pass is evidence only for the declared
pytest scope; record the exact selectors in the PR. Use
`scripts/validate.sh --full` for a claim promotion or release and whenever the
change reaches shared numerics, verification machinery, claim or release
governance semantics, public exports, dependencies, conventions, multiple
framework sectors, or has an uncertain dependency boundary. Calling
`scripts/validate.sh` without arguments remains a backward-compatible alias for
`--full`.

Do not run the full suite a second time at the same unchanged boundary. Use
targeted tests while developing, then run the appropriate scoped or full
workflow validation once before commit, review, or promotion. A bounded PR can
remain scoped through merge when the impact boundary is still valid against
the current base. Do not duplicate an equivalent validation independently by
the author, reviewer, and merger. Run the full suite periodically on integrated
`main` as an additional backstop, not as a substitute for PR impact analysis.

Run validation and commit as separate process invocations. An unguarded multi-command shell can continue after a failed validator and let a later successful commit mask the failure; never treat the combined process's final status as proof that every earlier gate passed.

The bootstrap installs `memory` with `pipx`; agents call it directly without activating `.venv`. Also run every targeted scientific verifier and downstream consumer named by the claim delta. Before promotion, ensure generated files are current, the registry validates, the release claim set is closed, and the working-tree diff contains no unrelated or host-specific artifacts.

Materialize every evidence path before adding it to an accepted registry or disposition. When a final attempt record summarizes the promotion gate, create it explicitly as in progress before registry validation, finalize it after the gate, and rerun only record-sensitive repository and generation checks; do not repeat the unchanged full suite.

## Self improvement

Modify your AGENTS.md, your memory task templates, and your skill to refine your process, improve accuracy, handle usage and gotchas.  Keep the goal of this project in mind, all instructions and files and workflows and skills and AGENT files should be self tuned toward that goal.  That does not mean that you should just sprawl skills and add new sections.  It means you should address the problems in your AGENTS, SKILLS and TEMPLATES, correct the language and correct the process, not just append new rules.  Do not fall into the trap of validation theater. If you have already validated a script several times, or many many times, why are you revalidating it with every new effort. So also optimize your validation scripts for honesty, but also for efficiency.
