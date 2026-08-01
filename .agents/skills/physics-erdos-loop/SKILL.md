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
- A verifier passing is necessary, but proves only its asserted predicate.
- Numeric agreement is a comparator, never a concept-selection mechanism or hidden derivation input.
- A failed concept is evidence about that concept. It is not permission to retrofit the framework around it.
- An attempt is bounded and append-only. The effort continues until the success contract is met or the user changes the objective.

## Phase 0 — establish authority and recall

Before deriving anything:

1. Read `AGENTS.md`, `governance/releases/current.yaml`, and `governance/claims.yaml`.
2. Inspect git status and history. Distinguish accepted release, committed provenance, uncommitted proposal work, and generated files.
3. Search memory with `memory search` and `memory grep`; treat hits as pointers and verify facts at source.
4. Search importable source, campaign artifacts, tests, and dependency consumers.
5. Record the last accepted boundary and the genuine unresolved objective in a contract from `memory-templates/`.

Run `scripts/preflight.sh` to check the local tools and governance surfaces.

## Phase 1 — write the success contract

Instantiate `memory-templates/research-arc.md` for physics work or `campaign-proposal.md` for a campaign. State:

- the exact positive deliverable;
- the accepted base release;
- definitions, variables, units, domains, quantifiers, and conventions;
- invariants that must survive;
- permitted imports and assumptions;
- the claim delta and downstream consumers;
- what each oracle must establish;
- the empty-debt and canonicalization gates.

Do not include failure, no-go, residual, or “best effort” as an accepted outcome.

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

Match implementation to the claim. Use exact symbolic algebra when an exact residual or identity is available, formal proof when the encoded theorem is the real obligation, and SciPy numerical methods when the claim is an IVP, BVP, spectral, optimization, integration, or PDE problem without a usable closed form. Reuse `substrate_framework.numerics` for common IVP, method-of-lines, BVP, and refinement evidence; the claim implementation must still own and expose its equation, discretization, boundary data, error norm, and physical acceptance thresholds.

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

- implementation defect → repair and rerun;
- unstable numerics → change discretization, solver, precision, or oracle;
- bad representation → change variables, gauge, basis, coordinates, or formalism;
- concept conflicts with the framework → reject or reformulate it and try another candidate;
- target was misstated → correct the claim while preserving the user's objective;
- accepted foundation appears inconsistent → open a separate foundational-revision proposal.

Do not stop because routes are difficult or numerous. Generate another materially different route.

## Phase 5 — audit the verifier

Choose the strongest practical oracle using [oracles.md](references/oracles.md). Then audit the audit:

- confirm clean exit and terminal tally;
- mutate each load-bearing input and require a relevant check to fail;
- test wrong signs, normalizations, conventions, and counterexamples;
- check dimensions, symmetries, conserved quantities, and known limits;
- run resolution, timestep, domain, and tolerance refinement for numerics;
- compare against an independently implemented or analytically solvable case;
- inspect the exact statement of formal theorems and their axioms.

For SciPy work, record the routine and algorithm (`solve_ivp`, `solve_bvp`, sparse eigensolver, optimizer, quadrature, or another justified method), floating-point precision, mesh and domain, initial/boundary data, tolerances, stopping status, and error norm. Treat solver success as a prerequisite, not the verdict. A PDE claim additionally needs spatial and temporal refinement, stability evidence, conservation or controlled-dissipation checks, and a method cross-check or soluble limit appropriate to the equation.

A large pass tally with insensitive predicates does not promote a claim.

## Phase 6 — assess framework fit before data fit

Compare candidates using the preregistered criteria. Structural fit precedes empirical closeness. If the favored candidate requires reinterpretation of unrelated claims, convention mixing, compensating imports, or narrative edits, reject it and continue the search.

Do not revise foundations merely to save a candidate. A foundational revision must demonstrate an independent pre-existing inconsistency, compare at least two repairs, select the minimum coherent change, enumerate the migration, and pass global replay.

Only after the structural choice is frozen should you open the comparator gate and report predictive agreement or disagreement.

## Phase 7 — replay the dependency graph

Before review:

1. Enumerate direct and indirect consumers of every changed claim and canonical symbol.
2. Re-run targeted unit, symbolic, numeric, simulation, and formal checks.
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
2. Update `governance/claims.yaml` and a pinned release manifest.
3. Move the adjudicated campaign record into the immutable `campaigns/` log.
4. Run `scripts/render_docs.py`; never hand-edit `docs/generated/`.
5. Generate or synchronize accepted claim/release memory. Keep proposal and attempt memory separate.
6. Run `scripts/validate.sh`, targeted scientific checks, tests, and `git diff --check`.

## Phase 10 — done gate

Close only when every item in the success contract passes and the debt ledger is empty. An honest failure remains an active effort with a new candidate or repair queued. A pause caused by user authority or an external dependency preserves the active contract and exact next executable action; it is not scientific completion. When a repeated workflow defect or tooling gotcha is discovered, correct and consolidate the relevant instruction in `AGENTS.md`, this skill, and the applicable memory template; do not merely append another overlapping rule.

## Working with delegated agents

When delegation is authorized, give each worker one child contract and a disjoint write surface. Fresh reviewers receive sourced inputs, the claim, and criteria—not the parent agent's interpretation or expected answer. Reconcile worker findings into the parent contract and rerun the same promotion gates.
