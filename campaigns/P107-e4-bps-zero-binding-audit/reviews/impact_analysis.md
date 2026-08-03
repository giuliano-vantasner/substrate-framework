# P107 canonical API impact analysis

GitNexus was refreshed on the P107 working tree from framework commit
`e2f9e92`, yielding 15,643 nodes, 24,618 edges, 266 clusters, and 60 execution
flows. Analyzer-generated `CLAUDE.md`, `.claude/`, and appended `AGENTS.md`
content were removed and are not campaign artifacts.

Direct upstream analysis assigns `LOW` risk to
`bps_topological_lower_bound`: its only direct internal caller is
`conditional_attained_bps_sector_energy`, with no affected execution process.
`near_bps_mass_difference` has no upstream caller outside its tests and
campaign verifier and is also `LOW` risk with no affected process.

The exported `BogomolnyDensityDecomposition` class reaches the package
`__init__.py` and package-importing tests transitively. GitNexus reports 14
symbols at depth two, `LOW` risk, and zero affected execution flows. This is
the expected broad namespace edge rather than a behavioral dependency.

The change is additive: no existing canonical signature, convention, solver,
or execution flow is modified. Final staged-change detection and the focused
package tests remain required before commit.

Final staged-change detection maps 37 files to 88 changed symbols, reports
zero affected execution processes, and assigns overall `low` risk. The changed
symbol count includes claim-review document sections as graph symbols; it does
not indicate 88 executable APIs.
