# P100 impact analysis

P100 extends the existing thermal module with pure exact APIs for a declared
coth scale, gated activation response, capillary-reduced conditional rate,
reduced temperature shape, stationary residual and bound, and barrier/input
elasticities. The functions are exported from the package root and covered by
focused tests. Existing C-TH-001 APIs and their semantics do not change.

The accepted scientific closure uses C-TH-001, C-RG-001/C-RG-002, and
C-COH-001 only within their stated ceilings. P005, P006, P086, and P099 are the
accepted dependency replay set. No formal theorem, numerical solver, sampled
integration, radial-energy expression, or coherence-gate implementation is
modified.

Pinned source consumers are recorded in `evidence/consumer-audit.yaml`. The
core engineering consumer reproduces 16 checks but hard-codes the refuted
`q/2` optimum. BD3, BD4, BD5, CM2, and CM4 reproduce their source tallies but
remain pending and use distinct unaccepted population, inertia, kinetic,
prefactor, or scale premises. The DBD scaling law and pipeline are broken under
the current NumPy because `pipeline.py` calls `np.trapz`; `l1_plasma.py` has a
second direct call. These source-checkout defects are preserved rather than
laundered into accepted evidence.

P100 exact code imports no NumPy and requires no quadrature. The accepted API
is therefore independent of the `trapz`/`trapezoid` version boundary. Generated
documentation and memory will be updated only through their renderers, and the
qualified BD2 disposition will leave all physical DBD and later bridge units
pending for their own governed audits.
