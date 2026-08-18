---
name: physics-erdos-loop
description: Run persistent, verifier-backed physics research and framework reconciliation from candidate generation through claim-level promotion. Use for physics derivations, equations, ODE/PDE work, symbolic or numeric checks, simulations, Lean formalization, campaign design, claim migration, framework-wide consistency audits, or any proposal that might change accepted scientific claims. Enforces recall, preregistered competing concepts, natural framework fit, append-only attempts, mutation-sensitive verification, global dependency replay, no early stopping, and generated canonical records.
---

# Physics Erdős Loop

Use this loop to produce a positive, framework-consistent, verified result—not merely an articulate account of why one attempt failed. It adapts the Erdős-style persistent proof loop to physics while adding claim governance and software reuse.

## Non-negotiable outcome

Honesty is required but is not itself success. Classify a failed candidate, no-go, obstruction, residual, bound, or inconclusive computation as attempt evidence and continue. Do not close the effort on it.

Success requires the requested object plus all of these gates:

- accepted dependency closure and declared imports;
- natural compatibility with framework invariants, or a separately accepted minimal foundational revision;
- strongest practical oracle and verifier-sensitivity evidence;
- preregistered comparison of plausible candidates;
- full downstream replay;
- reusable importable implementation;
- claim-by-claim review and release promotion;
- synchronized generated docs and memory;
- empty debt ledger.

Read [governance.md](references/governance.md) before changing a claim, convention, invariant, or canonical API. Read [oracles.md](references/oracles.md) when selecting or auditing verification.

## Core distinctions

- A campaign is an immutable research event, not canonical truth.
- A proposal can challenge a claim; only an accepted claim can supersede one.
- Accepted canon governs release and promotion decisions, but remains falsifiable and reviewable; a conflict is a diagnosis to investigate, not a reason to erase evidence or halt conditional artifact work.
- A verifier passing is necessary, but proves only its asserted predicate.
- A campaign completion decision, scientific claim decision, and PR merge decision are independent. Use `research-pr-harvest` for the merge decision.
- Numeric agreement is a comparator, never a concept-selection mechanism or hidden derivation input.
- A failed concept is evidence about that concept. It is not permission to retrofit the framework around it.
- An attempt is bounded and append-only. The effort continues until the success contract is met or the user changes the objective.

## Phase 0 — establish authority and recall

Before deriving anything:

1. Read `AGENTS.md`, `governance/releases/current.yaml`, and `governance/claims.yaml`.
2. Inspect git status and history. Distinguish accepted release, committed provenance, uncommitted proposal work, and generated files.
3. Search repository memory with `memory search ... --base "$PWD/memory"` and `memory grep ... --base "$PWD/memory"`; treat hits as pointers and verify facts at source. Validate repo-local memory with an explicit repository base and absolute target, `memory validate --base "$PWD" "$PWD/memory"`, so host configuration cannot redirect relative paths.
4. Search importable source, campaign artifacts, tests, and dependency consumers. For predecessor migration, start from the hash-pinned unit in `migration/source-claims.yaml`; do not double-count its dossiers, frozen rungs, formalizations, or memory entries as independent claims.
5. Record the last accepted boundary and the genuine unresolved objective in a contract from `memory-templates/`.

Run `.agents/skills/physics-erdos-loop/scripts/preflight.sh` to check the local tools and governance surfaces.

## Phase 1 — write the success contract

Instantiate `memory-templates/research-arc.md` for physics work or `campaign-proposal.md` for a campaign. State:

- the exact positive deliverable;
- the accepted base release;
- definitions, variables, units, domains, quantifiers, and conventions;
- invariants that must survive;
- permitted imports and assumptions;
- the claim delta and downstream consumers;
- each proposed claim identifier and a repository-wide registry, campaign, and durable-memory collision search, because rejected provisional identifiers remain reserved;
- what each oracle must establish;
- the empty-debt and canonicalization gates.

Do not include failure, no-go, residual, or “best effort” as an accepted outcome.

Validate the matching proposal manifest with `PYTHONPATH=src .venv/bin/python scripts/validate_repository.py` before opening a predecessor source body or comparator values. The frozen prose and YAML must agree, and a schema failure is an append-only attempt rather than permission to proceed informally.

## Phase 2 — preregister competing concepts

Register at least two plausible candidates unless uniqueness is already proved. For each, record its new objects, assumptions, parameters, expected limits, affected claims, and likely consumers.

Freeze selection criteria before inspecting comparison values:

1. consistency with accepted invariants;
2. explanatory and predictive reach;
3. fewer new assumptions, imports, and parameters;
4. correct symmetries, dimensions, topology, and limits;
5. compatibility with other accepted sectors;
6. numerical robustness and implementability.

Keep empirical comparators blinded until equations, conventions, criteria, and structural tests are frozen when practical. Record and justify any exception.

## Phase 3 — derive through importable APIs

Build the smallest dependency-first claim ladder. Implement reusable equations, constants, units, solvers, and transformations under `src/substrate_framework/`. Keep proposal scripts thin: import canonical functions and evaluate a candidate.

Match implementation to the claim. Use exact symbolic algebra when an exact residual or identity is available, formal proof when the encoded theorem is the real obligation, and SciPy numerical methods when the claim is an IVP, BVP, spectral, optimization, integration, or PDE problem without a usable closed form. Reuse `substrate_framework.numerics` for common IVP, method-of-lines, BVP, refinement evidence, and sampled trapezoidal integration; canonical modules call its `trapezoid_integral` compatibility API, while mutable standalone scripts targeting the current environment call `np.trapezoid`, never removed `np.trapz`. Preflight executable syntax for direct, imported, and dynamic legacy access. Never use an eager nested fallback such as `getattr(np, "trapezoid", getattr(np, "trapz"))`; use the canonical helper or a two-step `None` fallback. The claim implementation must still own and expose its equation, discretization, boundary data, error norm, and physical acceptance thresholds.

Do not:

- execute simulations at import time;
- duplicate `check()` helpers, profiles, constants, or convention conversions;
- encode the expected answer as an input;
- reinterpret earlier variables to make a new concept fit;
- edit generated documentation;
- weaken the target after a failed attempt without creating a distinct claim.

Use [verify_claim.py](assets/verify_claim.py) for exact or general claim checks and [verify_pde.py](assets/verify_pde.py) for a SciPy method-of-lines and mesh-refinement pattern. Both use shared framework APIs rather than campaign-local solver or tally copies.

## Phase 4 — run append-only attempts

Create `attempts/0001/`, `0002/`, and so on. Preserve candidate source, command, environment, stdout, stderr, elapsed time, verdict, and diagnosed mechanism. Never overwrite an attempt.

After failure, choose the next action from the diagnosis:

- legacy-library alias only → detect direct `np.trapz`, imported `trapz`, dynamic `getattr(np, "trapz")`, and eager nested-default access; repair the mutable script to `np.trapezoid` or a safe two-step fallback and rerun the same scientific route; for immutable hash-pinned source, preserve the native abort and run an explicit alias-only compatibility replay, without counting the environment abort as a rejected scientific candidate;
- implementation defect → repair and rerun;
- unstable numerics → change discretization, solver, precision, or oracle;
- bad representation → change variables, gauge, basis, coordinates, or formalism;
- concept conflicts with the framework → determine whether the defect belongs to the candidate or is independent evidence against accepted structure; reject or reformulate a defective candidate, otherwise open a `challenges` or foundational-revision proposal and keep the frontier active;
- target was misstated → correct the claim while preserving the user's objective;
- accepted foundation appears inconsistent → open a separate foundational-revision proposal.

Before inventing a replacement, inspect the nearest accepted campaign or
canonical module with a related obligation. Verify its source, extract the
construction and selection logic that actually worked, and record the
transferable assumptions and the present mismatch. External research may
supplement this step but does not replace framework-context reconciliation.

Do not stop because routes are difficult or numerous. Generate another materially different route.

## Phase 5 — audit the verifier

Choose the strongest practical oracle using [oracles.md](references/oracles.md). Then audit the audit:

Do not count a weaker oracle as independent evidence when a stronger result already fixes its input. In particular, after exact algebra removes a parameter from an ODE right-hand side, local uniqueness proves same-initial-data trajectory independence; integrating that identical right-hand side twice is only regression coverage. Likewise, eliminate shared intermediate variables before calling a downstream tail, dispersion, or normalization check independent: if it yields the same equation or positive solution set, record it as a dependent regression. Cross-sector matching additionally requires explicit field, kinetic-metric, action-measure, and coefficient maps; equal names, shapes, or dimensions do not supply them. Use exact sensitivity or initial Taylor coefficients for analytically accessible counterexamples, and reserve simulation for behavior the exact result does not decide.

- confirm process status zero and terminal tally independently; record lexical check-call sites, runtime check executions, and assertion nodes as distinct inventories, without demanding equality when loops or dynamic dispatch multiply executions; with `CheckLedger`, preserve the formatted tally while returning its status-zero success token rather than a positive count as an OS exit code;
- pin a verifier's own source, claim, and release evidence, but do not freeze unrelated future queue dispositions or require mutable `current` to remain a historical release; historical replay uses durable snapshots when available and otherwise targets canonical modules/tests rather than rewriting an adjudicated campaign;
- mutate each load-bearing input and require a relevant check to fail;
- test wrong signs, normalizations, conventions, and counterexamples;
- check dimensions, symmetries, conserved quantities, and known limits;
- run resolution, timestep, domain, and tolerance refinement for numerics;
- compare against an independently implemented or analytically solvable case;
- inspect the exact statement of formal theorems and their axioms.
- reject structural predicates implemented as literal booleans, stand-in constants, copied periods, or samples that do not evaluate the defining object;
- for differential forms, expand all graded Leibniz and cyclic terms and audit nonvanishing, closedness, global non-exactness, periods, extension dependence, and gauge descent independently.

For SciPy work, record the routine and algorithm (`solve_ivp`, `solve_bvp`, sparse eigensolver, optimizer, quadrature, or another justified method), floating-point precision, mesh and domain, initial/boundary data, tolerances, stopping status, and error norm. Tie near-zero and agreement thresholds to a declared dimensional or scale-relative error model. When an absolute threshold fails at roundoff scale, preserve the attempt, show refinement or conditioning evidence, and repair the oracle with a justified scale-sensitive bound; do not blur a separately exact null into a floating-point claim. Treat solver success as a prerequisite, not the verdict. A PDE claim additionally needs spatial and temporal refinement, stability evidence, conservation or controlled-dissipation checks, and a method cross-check or soluble limit appropriate to the equation.

A large pass tally with insensitive predicates does not promote a claim.

## Phase 6 — assess framework fit before data fit

Compare candidates using the preregistered criteria. Structural fit precedes empirical closeness. If the favored candidate requires reinterpretation of unrelated claims, convention mixing, compensating imports, or narrative edits merely to preserve it, reject it and continue the search. If the mismatch is reproduced independently of that candidate, treat it as evidence about canon and route it through a separate challenge rather than assuming acceptance status resolves the science.

Do not revise foundations merely to save a candidate. A foundational revision is nevertheless a legitimate advancement route when it demonstrates an independent pre-existing inconsistency, compares at least two repairs, selects the minimum coherent change, enumerates the migration, and passes global replay. Until adjudication, the conflict blocks promotion and accepted downstream use, not truthful conditional APIs or continued investigation.

Only after the structural choice is frozen should you open the comparator gate and report predictive agreement or disagreement.

## Phase 7 — replay the dependency graph

Before review:

1. Enumerate direct and indirect consumers of every changed claim and canonical symbol.
2. Re-run targeted unit, symbolic, numeric, simulation, and formal checks. If a mutable consumer aborts on direct or dynamic access to removed `np.trapz`—including an eagerly evaluated nested `getattr` default—repair it to `np.trapezoid` or a safe two-step fallback and rerun before classifying the consumer or campaign; use an alias-only recorded replay for immutable source.
3. Re-check units, conventions, signs, limits, free-symbol sets, imported constants, and parameter counts.
4. Compare generated outputs and narrative consumers.
5. Record every new debt and discharge it in the same effort.

Local success with broken downstream consumers is failure.

## Phase 8 — independent claim review

Use `memory-templates/claim-review.md`. Review claims individually, not the proposal as a single package. The reviewer must have the raw artifacts and acceptance criteria, not the proposing agent's preferred conclusion.

Assign each claim independent verification, review, compatibility, and epistemic statuses. Unaccepted work stays under `proposals/`. Use `challenges` until a replacement claim is accepted; only then add `supersedes`.

## Phase 9 — promote and materialize

For accepted claims:

1. Extract reusable logic into `src/substrate_framework/` and tests.
2. Update `governance/claims.yaml` and a pinned release manifest. Compute release closure from accepted registry membership (`review: accepted` / non-null `accepted_in`), not from `epistemic: active`; accepted qualified claims remain release members. Use the governance validator rather than a verifier-local status filter. If predecessor units were consumed, edit only `migration/dispositions.yaml`, preserve any unmigrated subclaims explicitly, and regenerate `migration/source-claims.yaml`; never hand-edit that generated queue. Materialize every evidence path before registering it. A final attempt that summarizes the promotion gate may begin with an explicit in-progress status, then be finalized after the gate and checked with only record-sensitive repository/generation validation.
   Terminal `qualified`, `refuted`, `duplicate_evidence`, and `out_of_scope` dispositions require their structured reason and durable evidence paths; use `qualified` when a mixed unit also maps accepted claims.
3. Move the adjudicated campaign record into the immutable `campaigns/` log.
4. Run `scripts/render_docs.py`; never hand-edit `docs/generated/`.
5. Generate or synchronize accepted claim/release memory. Keep proposal and attempt memory separate.
6. Run targeted scientific checks, `scripts/validate.sh --full`, and `git diff --check`; promotion is a full-validation boundary, so do not repeat that unchanged suite separately. Run validation and commit in separate process invocations so an unguarded shell cannot continue past a failed gate and mask it with a later successful command.

## Phase 10 — done gate

Declare the campaign objective complete only when every item in the success contract passes and the debt ledger is empty. An honest failure leaves the objective active with a new candidate or repair queued. It does not prevent an individual PR or agent run from ending at a clean harvest checkpoint: use `research-pr-harvest` to merge independently correct, novel, reusable units, name and keep open the canonical goal issue, update that issue with the merged/refactor/history disposition and unit-level rationale, and hand the exact frontier to a fresh run. Keep a source PR open while a finite repair or harvest is live; close it unmerged only after the harvest skill's terminal-close test. Missing work toward the larger goal is frontier rather than debt unless a merged or promoted unit promises it. A pause caused by user authority or an external dependency preserves the active contract and exact next executable action; it is not scientific completion. When a repeated workflow defect or tooling gotcha is discovered, correct and consolidate the relevant instruction in `AGENTS.md`, this skill, and the applicable memory template; do not merely append another overlapping rule.

## Working with delegated agents

When delegation is authorized, give each worker one child contract and a disjoint write surface. Fresh reviewers receive sourced inputs, the claim, and criteria—not the parent agent's interpretation or expected answer. Reconcile worker findings into the parent contract and rerun the same promotion gates.
