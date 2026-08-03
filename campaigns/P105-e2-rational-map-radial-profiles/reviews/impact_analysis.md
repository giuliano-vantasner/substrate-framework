# P105 impact analysis

GitNexus was refreshed at framework commit `52f376f` with the P105 worktree
present. The additive index contained 15,316 nodes, 23,757 edges, 262 clusters,
and 63 flows. The generated `CLAUDE.md`, `.claude/`, and appended AGENTS block
were analyzer residue and were removed; they are not framework changes.

Upstream impact for both `solve_rational_map_radial_profile` and
`rational_map_radial_energy_density` is LOW: zero pre-existing direct callers,
zero affected processes, and zero affected modules. The index records the new
solver flow into shared numerical validation and the internal radial RHS. The
only intended consumers are the new focused tests and P105 verifier. Querying
the solver flow found no accepted pre-existing canonical consumer.

The initial untracked-file limitation of `detect_changes` meant its git-diff
summary reported only analyzer-touched AGENTS sections before residue removal.
After all promotion files were staged, final detection mapped 81 changed
symbols across 37 files and assigned automatic MEDIUM risk because four
processes were affected. Inspection shows that all four are newly introduced
internal solver flows ending at `_real_vector`, `_radial_rhs_unchecked`,
`_positive_symbolic`, or `massless_tail_boundary_residual`; none is a
pre-existing downstream framework process. Direct upstream impact for both
public symbols remained LOW with zero pre-existing callers, processes, or
modules. No canonical symbol is renamed or modified; C-MOD-001/002 remain
unchanged and are exercised through exact and numeric degree-one regression.

Automated staged-change classification: MEDIUM. Assessed downstream breakage
risk: LOW because the detected processes are additive and self-contained.
Required replay is the P105 primary verifier, independent collocation review,
focused rational radial tests, governance/release closure, generated
documentation and memory checks, and the repository gate.
