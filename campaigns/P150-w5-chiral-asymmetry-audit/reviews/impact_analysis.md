# P150 impact analysis

P150 is an additive exact-scattering extension with low blast radius. After a
fresh GitNexus full index, the upstream impact query for
`passive_half_line_scattering_ledger` reported LOW risk, zero direct callers,
zero affected modules, and zero affected execution flows. The repository's
seven indexed flows are verifier `Run/Main -> Check` paths and do not depend on
the new ledger.

The implementation adds one immutable ledger dataclass and one pure exact
function in a new module, exports both from the package, and adds focused
tests. It changes no existing function body, signature, normalization,
integration rule, or accepted convention. It performs no quadrature and has
no NumPy integration compatibility shape.

The unstaged change detector sees the tracked `__all__` edit, reports LOW
risk, zero affected symbols, and zero processes; untracked new files are
covered directly by fifteen focused tests, the 32-check primary verifier, a
fresh 17-check derivation, the 46-check frozen source graph, package-import
replay, and the final staged transaction replay. After staging the complete
transaction, the change detector maps 65 symbols across 35 files and still
reports LOW risk, zero affected symbols, and zero affected processes. The graph covers eleven
declared dependencies and four reverse consumers. Qualified W3 and W4 remain
unchanged; pending W7 and YM1 must not import W5's rejected chiral, parity,
weak, detector, or gauge readings.
