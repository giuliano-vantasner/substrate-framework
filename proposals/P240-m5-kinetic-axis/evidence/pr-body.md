## Objective and issue

Publish the current P240 spectral-Cartan fixed-$J$ two-clock candidate, its
conditional reusable API, all 40 fresh P240 attempt scripts/results, and the
independent-validation handoff so external contributors can inspect the actual
tests and numerical methodology.

Canonical issue: #146

Issue relationship: Advances #146

Candidate source issue: #147

Authoring agent: Codex primary agent (material implementer)

Intended merger: distinct repository owner or review agent; no self-merge is
requested by this PR.

- [x] The canonical issue existed before this PR was submitted.
- [x] A distinct merger is intended.

## Current candidate

$$
\mathcal{L}=-\frac{1}{2}F_{\mu\nu ab}F_{\rho\sigma cd}
\eta^{\mu\rho}\eta^{\nu\sigma}h^{ac}(M)h^{bd}(M)
-V_{\mathrm{M5.17}}(M),
\qquad
h^{ab}=\eta^{ab}-2P_t{}^a{}_c\eta^{cb}.
$$

The interaction mechanism is evaluated in the fixed-$J$ two-clock sector:

$$
E_J=E_{\mathrm{stat}}+\frac{1}{4}J^{T}I^{-1}J.
$$

This is a selected candidate for independent validation, not an accepted claim.

## Change classification

- [x] Reusable implementation or tooling
- [ ] Documentation or workflow
- [x] Scientific proposal or campaign evidence
- [ ] Claim promotion transaction
- [ ] Harvest from an incomplete research PR
- [ ] Compatibility-only repair

## Authority and scope

Base release and commit: `v0.163.0` from
`a34b5f584165b86d1fc62af0ede5fbf37b0aa5b7`.

Accepted claims and canonical sources used: C-LOR-002, C-KRN-001, C-VAR-003,
C-IGR-004, and C-GRV-002 only at their registered scopes. The merged P239
`m5_covariant_action.py` implementation is an audited conditional input, not
accepted C-M5 authority and not inherited validation evidence.

Declared imports, assumptions, and conventions: mostly-plus Minkowski metric;
$P_t$ is a simple real timelike spectral projector continuously connected to
the vacuum timelike line; fixed $J$, not fixed $\omega$, is the interaction
ensemble; numerical stationary-field results are resolution-bounded
applicability evidence.

Files or concerns intentionally out of scope: the local 4.9 GB PyTorch/CUDA
virtual environment, bytecode caches, P239/P236 receipts and numerical values,
claim registry or release changes, and any assertion that #146 is complete.

New or materially changed public interfaces:

| Symbol or module | Authority status | Accepted claim IDs | Owning issue/PR | Conditional boundary |
| --- | --- | --- | --- | --- |
| `substrate_framework.m5_kinetic_axis` (14 public symbolic helpers) | conditional unpromoted | none | #146 / this PR | Exact algebraic APIs on declared projector, metric, self-adjointness, and fixed-$J$ premises; no existence, empirical, or accepted-claim inference |

## Useful-unit disposition

| Unit | Local claim or purpose | Dependencies | Evidence and tests | Proposed disposition |
| --- | --- | --- | --- | --- |
| Conditional kinetic-axis symbolic API | Reusable exact contractions, current densities, and fixed-$J$ scale ledger | Conditional P239 tensor API | `tests/test_m5_kinetic_axis.py` | merge candidate after distinct review |
| Attempts 0032–0035 | Exact source-restricted no-go, candidate contraction, two-clock Legendre algebra, and regular chart | SymPy plus canonical conditional APIs | 76/76 exact checks | merge as candidate evidence |
| Attempts 0036–0040 | Reproducible CUDA stationary-branch continuation and saved coefficients | PyTorch 2.4.1+cu124, SciPy, RTX-class CUDA device | 6x5 root and independent centered-curvature check | merge as applicability evidence, not proof |
| Attempts 0001–0031 | Append-only route comparison, corrections, and numerical-method history | Per-attempt manifests | Scripts, results, and small state snapshots | public PR evidence; reviewer may retain as history rather than a canonical API |

Answer each decision independently:

- Artifact merge: the conditional API and exact/applicability evidence are
  locally complete as a candidate review surface; a distinct reviewer should
  decide whether the complete attempt trail lands or remains PR history.
- Claim promotion: none.
- Goal completion: no. P240 has not established a stable continuum one-body
  solution or the separately relaxed two-body Coulomb/cross-inertia tails.

## Validation receipt

The content-addressed receipt is
`proposals/P240-m5-kinetic-axis/evidence/validation-receipt.yaml`.

```text
PYTHONPATH=src python proposals/P240-m5-kinetic-axis/attempts/0032/verify_source_restricted_quadratic_family.py
# exit 0; 25/25 exact checks pass

PYTHONPATH=src python proposals/P240-m5-kinetic-axis/attempts/0033/verify_contraction_endpoints.py
# exit 0; 21/21 exact checks pass

PYTHONPATH=src python proposals/P240-m5-kinetic-axis/attempts/0034/verify_two_clock_legendre.py
# exit 0; 18/18 exact checks pass

PYTHONPATH=src python proposals/P240-m5-kinetic-axis/attempts/0035/verify_smooth_hedgehog_chart.py
# exit 0; 12/12 exact checks pass

PYTHONPATH=src python -m pytest -q tests/test_m5_kinetic_axis.py
# exit 0; 10 passed

scripts/validate.sh --pytest-scope tests/test_m5_kinetic_axis.py
# exit 0; all fixed repository checks and requested pytest scope pass

memory validate --base "$PWD" "$PWD/memory/codex/proposals/P240-m5-kinetic-axis.md"
# exit 0; all 1 memory files valid

YAML/JSON parse preflight for proposals/P240-m5-kinetic-axis
# exit 0; 94 YAML and 4 JSON files parse

git diff --cached --check
# exit 0
```

Attempt 0040 itself records the completed float64 PyTorch 2.4.1/CUDA run:
relative root gradient $6.80\times10^{-15}$, inertia $0.460713$, frequency
$1.085274$, and a branch-specific saddle with lowest Hessian eigenvalue
$-2.868074$ corroborated by centered curvature $-2.867967$. This numerical
result is preserved rather than rerun as a new selection hurdle.

## GitNexus impact

The baseline index was current at `a34b5f5` and was refreshed to include the
new worktree files. Upstream impact for `kinetic_axis_lagrangian_density` is
LOW: zero direct existing dependents, zero affected processes, and zero affected
modules. Final staged change detection reports no affected execution process;
its symbol mapping sees the proposal-memory sections but does not enumerate
symbols added in the new Python file. An independent `rg` consumer inventory
finds only this P240 attempt suite and `tests/test_m5_kinetic_axis.py`. The
repository's sole indexed execution flow is an unrelated P227 verifier flow.

## Memory, governance, and generated state

Durable contract or decision entry:
`memory/codex/proposals/P240-m5-kinetic-axis.md`.

Proposal/campaign/claim/release changes: active P240 proposal and append-only
attempt evidence only; no claim registry, accepted campaign, or release change.

Generated outputs and synchronization commands: none.

Debt remaining inside the proposed merge unit: none inside the explicitly
conditional API/evidence statements. Native compatibility aborts and rejected
routes are labeled in their own attempt records rather than hidden.

Campaign frontier outside this merge unit: independent continuum stability;
another stationary branch if it exists; separately relaxed charge pair; sign
and asymptotic exponent of $I_{12}(r)$; Newton-tail claim review and promotion.

## Validation boundary

- [x] Targeted tests and named scientific verifiers pass.
- [x] Load-bearing mutations, counterexamples, and wrong-convention probes fail as expected.
- [x] Affected consumers (P240 verifier imports and focused package tests) replay.
- [x] `scripts/validate.sh --pytest-scope tests/test_m5_kinetic_axis.py` passes; the additive single-module boundary agrees with `scripts/validate_changed.py` selection logic.
- [x] The pytest scope remains valid against merge base `a34b5f5`.
- [x] `git diff --cached --check` passes in a separate invocation.
- [x] No unrelated, generated-by-hand, or host-specific artifacts are included.

## Author handoff

The reviewer should reproduce attempts 0032–0035 and inspect attempt 0040's
action, basis, root residual, Hessian, centered-energy mutation, withheld-mode
diagnostic, and saved 6x5 coefficients. The riskiest open assumption is not an
algebraic identity: it is whether the tangential-split negative mode persists
for the continuum admissible hedgehog or is specific to this representation and
branch. The next decisive action is one materially independent stationary-field
or validated-numerics calculation, followed by the fixed-$J$ pair oracle only
if a stable branch exists.

---

## Reviewer disposition

To be completed by a distinct reviewer.
