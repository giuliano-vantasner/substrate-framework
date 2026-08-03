# P116 Canonical Impact Analysis

The proposed change is additive and LOW risk in the indexed framework graph.
`conditional_composite_factor` has no upstream caller, while
`nominal_loss_cycle_product` has one direct caller inside the same new module.
No indexed process is affected.

GitNexus was refreshed with `gitnexus analyze --index-only` at framework commit
`172c86e`. `gitnexus impact conditional_composite_factor --repo
substrate-framework --depth 3` reports zero impacted symbols, zero processes,
and zero modules. The corresponding nominal-product query reports one direct
internal caller, zero processes, and one module. Change detection reports no
pre-existing changed consumer because the new module is additive.

The scientific source graph is wider than the code-call graph. Seven direct
and fourteen indirect hash-pinned bridge consumers replay 692 checks. Those
candidate edges are provenance and replay scope only; none imports the new
canonical module or gains accepted authority from its own passing tally.
