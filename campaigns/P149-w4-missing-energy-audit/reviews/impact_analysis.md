# P149 impact analysis

P149 is an additive exact-kinematics extension with low blast radius. After a
fresh GitNexus index, the upstream impact query for
`two_body_threshold_ledger` reported LOW risk, zero direct callers, zero
affected modules, and zero affected execution flows. The repository's seven
indexed flows are verifier `Run/Main -> Check` paths and do not include the new
ledger.

The implementation adds one immutable ledger dataclass and one pure exact
function in a new module, exports both from the package, and adds focused
tests. It changes no existing function body, signature, normalization,
integration rule, or accepted convention. It performs no quadrature and has no
NumPy integration compatibility shape.

The initial post-edit `detect_changes(scope=unstaged)` reports LOW risk, one
changed symbol (`__all__`) in one tracked file, zero affected symbols, and zero
processes; at that point its diff mapper does not include untracked new files.
After staging the complete transaction, the required pre-commit replay maps 48
symbols across 34 files, including the ledger class, constructor, properties,
verifiers, graph constants, and package export. It still reports LOW risk, zero
affected symbols, and zero affected processes. Thirteen focused tests, the
33-check primary verifier, a fresh 15-check matrix and exponential-coordinate
derivation, the 25-check frozen source graph, explicit package-import replay,
and the final integrated gate cover the scientific and new-file surfaces.

The source graph covers four declared dependencies and two reverse consumers.
Pending W5 and NA1 must not import W4's rejected hidden-kink, charge-conditioned
missing-energy, neutrino, weak, or gauge readings. GitNexus-generated host
integration files were removed after indexing; the index was retained and no
host-specific artifact remains in the worktree.
