# P160 Additive SU(3) Algebra and Finite-Lie Scalar-Loop Impact Analysis

P160 adds `SU3SymmetricTensorEvidence`, `symmetric_structure_constant`, and
`symmetric_tensor_evidence` to the existing SU(3) module. It generalizes the
canonical conditional scalar theorem through
`FiniteLieScalarVacuumPolarization` and
`finite_lie_scalar_qed2_vacuum_polarization`, while retaining the public
`SU2ScalarVacuumPolarization` class and `su2_scalar_qed2_vacuum_polarization`
signature and return shape as an exact specialization. It changes no accepted
generator matrices, structure constants, connection sign, Abelian kernel, or
coefficient convention.

A fresh GitNexus index at implementation commit `da12a2b` contains 23,253
nodes, 36,604 edges, 344 clusters, and six execution flows. The new generic
loop function has LOW upstream risk with one direct canonical caller: the
preserved SU(2) wrapper. The new symmetric-tensor evidence function has LOW
risk and no graph caller outside its review surface. The preserved SU(2)
wrapper has LOW risk and no graph caller. The shared unchanged
`fundamental_generators` function has MEDIUM structural reach: six direct and
fourteen depth-four symbols in SU(3) invariants and WZW algebra, but no affected
execution process. Change detection from `d5b76e8` reports 36 P160 files, 137
symbols, LOW aggregate risk, and zero affected processes. Indexer-created
Claude configuration artifacts were removed and are not part of the diff.

Exact lexical inspection supplements the graph. The existing SU(2) wrapper is
consumed by P158 and P159 verifiers and its focused tests. The generator API is
consumed by P024, P028, WZW code, and their tests. Initial downstream replay
found one real regression: `sp.Matrix` passes exact `sympy.Integer` indices,
which an overly narrow built-in-`int` validator rejected. The repair admits
only built-in and SymPy exact integers, explicitly rejecting booleans, floats,
symbols, and out-of-range values. P024 then passed 27 checks; P028 passed 23;
P158 passed 32; P159 passed 31; the P160 primary and independent oracles passed
38 and 27; and the focused and adjacent suite passed 71 tests.

The pinned 17-node source graph separately replays 170 source predicates
through 28 graph checks. QCD2 is the only immutable node with a version-only
`np.trapz` reference and runs through the exact alias to `np.trapezoid`; this
has no scientific effect. Accepted CF3, WM1, and WM5 consumers use only already
accepted SU(3) algebra. Pending QCD2, SM1, SM3, SM4, GK1, WM7, GK3D1, and GK3D4
gain no loop, physical-sector, unique-coupling, or dimensional authority. No
impact-analysis debt remains.
