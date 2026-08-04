# P136 impact analysis

The pre-edit GitNexus query for `riesz_green_kernel` was LOW risk: its only
direct canonical caller was `static_maxwell_point_source`, with no indexed
process. P136 leaves that function and the Maxwell API behavior unchanged.

The index was initially stale at `4cea232` and could not see the additive
functions. That UNKNOWN result is preserved as a tool-state limitation, not
used as coverage. After indexing the P136 working tree at freeze commit
`49a9161`, both `critical_riesz_log_kernel` and `riesz_radial_force_law` report
LOW risk, zero upstream dependents, and zero affected processes. Direct search
finds only package exports, focused tests, and P136 campaign consumers.

No canonical symbol is renamed or removed. The existing subcritical API keeps
its domain rejection. The additive critical API requires positive `r0` and a
nonzero inverse-kernel coefficient; the additive force API delegates to that
unchanged subcritical domain check and keeps source and probe inputs explicit.
Twenty-two focused momentum-kernel and Maxwell tests pass, including d=2 and
d=3 cross-module comparisons and source/probe/reference/coefficient mutations.

The hash-pinned source graph has thirteen unique nodes and 140 predicates. All
replay successfully; immutable YM2 and QCD2 receive alias-only legacy NumPy
compatibility. No source imports the new APIs executably. The remaining impact
surface is governance, generated documentation, generated accepted memory, and
the parent migration queue. All are included in the integrated promotion gate.
