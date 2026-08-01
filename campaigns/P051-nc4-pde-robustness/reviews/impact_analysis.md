# P051 canonical API impact analysis

The pre-change GitNexus analysis was run after refreshing the stale repository
index at framework commit `033e9c7`. The planned public change was additive: a
new `sine_gordon_1d` module and new package exports, with no modification to an
accepted equation or existing callable.

The upstream query on `src/substrate_framework/__init__.py::__all__` reported
LOW risk, zero direct or indirect dependents, zero affected processes, and zero
affected modules. The processes resource named no relevant flow. This is
consistent with an additive API whose consumers are new focused tests and the
P051 verifier.

Post-change `detect_changes(scope=all)` also reported LOW risk and zero affected
processes. Its graph-backed diff recognized the tracked `__all__` edit but, as
expected, could not map the untracked new module and tests before commit. It
also reported previously committed `AGENTS.md` differences because the MCP
server retained an older graph snapshot; direct `git status` confirmed that
`AGENTS.md` is clean. The indexer's generated `CLAUDE.md`, `.claude/`, and
injected `AGENTS.md` block were removed as unrelated tool artifacts. Direct
consumer replay therefore covers the new module, NumPy compatibility helper,
accepted sine-Gordon and boundary APIs, and P048-P050 campaign verifiers.
