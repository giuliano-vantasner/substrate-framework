# Substrate Framework

**Claim-governed, agent-native scientific infrastructure for a self-consistent physics framework.**

This repository turns sequential research campaigns into a reproducible, importable, review-governed body of accepted claims. Chronology is not authority. A commit creates provenance; only individual review and promotion create scientific status.

**License:** Apache 2.0

## The Goal

The sole purpose of this repository is the **advancement and full promotion of validated claims**.

An effort is complete only when its positive claims have:

- passed every success gate in [`AGENTS.md`](AGENTS.md),
- undergone individual review,
- entered the accepted registry (`governance/claims.yaml`), and
- been pinned in a release.

That is the entire goal. Nothing else counts as success.

Partial harvest of reusable atoms is a tactical concession that keeps a larger objective open. It is never a substitute for claim promotion, never a terminal disposition, and never the outcome the repository exists to produce. Agents and humans must not treat merge activity, documentation polish, validation theater, or incremental code extraction as progress toward the goal. Those activities are scaffolding. The goal closes only when claims themselves are promoted under the contract and their downstream consumers remain consistent.

## Why contribute

Most physics codebases accumulate derivations, notebooks, and prose that no one can reliably reuse or audit months later. This repository is different by design:

- **Claims are first-class.** Every accepted result is a machine-readable, dependency-closed, oracle-validated statement with explicit assumptions, exclusions, evidence paths, and review status. You can import the mathematics, not just read a story about it.
- **Agents are first-class citizens.** The workflow, memory contracts, skills, validation gates, and non-self-merge rules are written so that software agents can propose, implement, review, and harvest work without constant human babysitting—while still preserving scientific integrity.
- **Failure is preserved, not papered over.** Failed candidates, no-gos, residuals, and contradictions remain as attempt evidence. The next agent does not have to rediscover why a route died.
- **Authority is explicit and reviewable.** A pinned release + the claims registry control what is true for the framework. Newer commits, confident prose, numerical attractiveness, or check counts do not.
- **Narrow claims, honest scope.** Accepted statements deliberately exclude over-interpretation. A claim about a sine-Gordon breather moment does not silently become a particle model or a gravitational-wave source. That discipline makes the accepted set actually trustworthy.

If you care about building scientific infrastructure that agents can extend without inventing their own epistemology every time, this is a concrete place to do it.

## What is already solved and claimed (v0.160.0)

The current accepted boundary contains **207 claims**. They are not a narrative summary of a theory; they are individually reviewed mathematical and numerical statements. Major sectors include:

| Sector | Representative claims | Status |
| --- | --- | --- |
| **Sine-Gordon core** | Exact breather, action, energy moments, topological current, parity, stress-energy identities | Fully accepted, symbolic + numeric |
| **Optical geometry / dilaton** | Optical metrics, source operators, constitutive relations | Accepted |
| **Dimensional analysis & units** | Primitive bases, mass/length coordinates, scale ledgers, transmutation | Accepted |
| **U(1) & non-Abelian gauge** | Local U(1), flux tubes, Wilson loops, SU(3) structure, one- and two-loop beta coefficients, running | Accepted |
| **Q-balls & radial models** | Exact sine-Gordon Q-ball, quartic fluctuations, radial harmonic balance, spectra | Accepted + simulation evidence |
| **Moments & gravitational-wave kinematics** | Conserved stress moments, TT projectors, polarization bases, conditional waveforms/power from moments (no dynamical gravity claimed) | Accepted |
| **3D sine-Gordon / oscillons** | Localized oscillon evidence, l=2 perturbations, axisymmetric radiation channels | Simulation + symbolic |
| **Topology / WZW** | π₅(SU(3)) period lattice, winding currents, five-form inflow (conditional) | Accepted |
| **Skyrme-like & chiral** | Radial modes, Hessian/Goldstone structure, PCAC residuals, GMOR ledger, massive-dipole interaction energies | Accepted (narrow scope) |
| **BPS, resolvents, barriers** | Conditional BPS energy attainment, paired resolvent identities, screened barriers, composite rates | Accepted |
| **Vacuum polarization & Maxwell** | One-loop polarization, Ward identities, Coulomb potentials in d dimensions, Riesz kernels | Accepted |
| **Lorentz / worldline** | Little groups, orbit metrics, einbein mechanics, reparametrization & Weyl identities (classical, conditional) | Accepted (v0.160.0) |
| **Coherence, dissipation, kinetics** | Coherence gates/thresholds, damped ringdown, first-passage, fixation, branching | Accepted |

Every claim carries:

- an explicit statement,
- verification level (`symbolic_verified`, `numeric_evidence`, or `simulation_evidence`),
- review status,
- dependency closure,
- assumptions and (importantly) exclusions,
- evidence and test paths.

See [`governance/claims.yaml`](governance/claims.yaml) and the pinned [`governance/releases/current.yaml`](governance/releases/current.yaml) for the authoritative list. Generated documentation lives under `docs/generated/`.

The framework began from an intentionally empty registry. No predecessor material is accepted merely because it existed, was numerically attractive, or was described as settled.

For human collaborators

1. Read [`CONTRIBUTING.md`](CONTRIBUTING.md), [`AGENTS.md`](AGENTS.md), and [`AGENTS_START_HERE.md`](AGENTS_START_HERE.md).
2. Open a canonical GitHub issue **before** any PR. The issue must state the positive objective, scope, success gate, dependencies, and coordination boundary.
3. Work in a branch. Keep artifact merge, claim promotion, and goal completion as three separate decisions.
4. Validation: `scripts/bootstrap.sh` then `scripts/validate.sh --full` (or scoped for bounded changes).
5. You may not merge a PR you opened, authored commits for, or materially implemented. A distinct reviewer/merger is required.

Public contributors can open issues and PRs freely. Merge authority is restricted to designated owners.

---

## For agents

Start here: [`AGENTS_START_HERE.md`](AGENTS_START_HERE.md).

The normative scientific and governance contract is [`AGENTS.md`](AGENTS.md). When the two documents differ, `AGENTS.md` wins.

Key invariants for every agent:

- Full claim promotion is the goal; harvest is not.
- Load the physics skill (`.agents/skills/physics-erdos-loop/`) for any derivation, simulation, or claim work.
- Instantiate a memory contract from `memory-templates/` before substantive work.
- Never self-merge.
- Never silently edit earlier campaigns or hand-edit `docs/generated/`.
- Preserve attempt evidence. Do not present failure as success.
- Authority order: pinned release → accepted claims → adjudicated campaigns → active proposals → append-only attempts.

Agents that follow the contract can propose, implement, review, request changes, harvest reusable units, and hand off validated work without constant operator confirmation (subject to the non-self-merge rule).

---

## Repository model

| Path | Role |
| --- | --- |
| `src/substrate_framework/` | Importable canonical equations, constants, solvers, derivations |
| `governance/claims.yaml` | Machine-readable accepted / proposed claim graph |
| `governance/releases/` | Pinned reproducible accepted claim sets (`current.yaml`) |
| `proposals/` | Candidate work before adjudication |
| `campaigns/` | Immutable adjudicated campaign records |
| `docs/generated/` | Generated from the registry — do not hand-edit |
| `memory-templates/` | Durable work, research, review, and promotion contracts |
| `.agents/skills/` | Native agent skills (physics loop, harvest, etc.) |
| `tools/agent-memory/` | Bundled memory CLI only |

---

## Bootstrap

```bash
scripts/bootstrap.sh
scripts/validate.sh --full
```

This creates `.venv`, installs the physics package dependencies, and makes the `memory` CLI available via `pipx`.

```bash
memory --version
.venv/bin/python -c "import substrate_framework"
```

For a bounded PR, keep the fixed repository checks and restrict pytest to the affected scope:

```bash
scripts/validate.sh --pytest-scope tests/test_affected_module.py
```

Use `--full` for claim promotion, release, shared numerics/verification changes, or any uncertain dependency boundary.

---

## Numerical physics APIs

`substrate_framework.numerics` provides shared SciPy-backed IVP, method-of-lines PDE, BVP, and refinement-evidence helpers. They standardize failure handling and evidence capture; they do **not** turn a numerical result into an exact proof. Claim verifiers must still supply the governing equation, boundary/initial data, convergence study, invariants, and independent checks appropriate to the claim.

```python
import numpy as np
from substrate_framework import SolverTolerances, solve_ivp_evidence

orbit = solve_ivp_evidence(
    lambda _t, state: np.array([state[1], -state[0]]),
    (0.0, 2.0 * np.pi),
    [1.0, 0.0],
    tolerances=SolverTolerances(rtol=1e-10, atol=1e-12),
)
```

---

## Authority state

The current accepted boundary is always the pinned manifest in `governance/releases/current.yaml` together with the individually accepted entries in `governance/claims.yaml`. This README and the newest commit are not authority.

A later campaign may challenge an earlier claim; it cannot supersede it until review promotes the replacement.

---

## Contributing & community

- [CONTRIBUTING.md](CONTRIBUTING.md) — issue-first workflow, validation, PR rules
- [AGENTS_START_HERE.md](AGENTS_START_HERE.md) — operational guide for agents
- [AGENTS.md](AGENTS.md) — normative scientific and governance contract
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md) — private vulnerability reporting
- Discussions: [GitHub Discussions](https://github.com/vantasnerdan/substrate-framework/discussions)

Do not upload paywalled papers, private correspondence, credentials, or third-party material without verified redistribution rights. Cite or link to the authoritative source instead.

---

## License

Apache License 2.0. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
