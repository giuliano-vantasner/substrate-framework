# P047 Impact Analysis

The pre-change GitNexus index at commit `6196b44` classified the change as low
risk. `axisymmetric_separable_stf_derivative` had one direct caller,
`axisymmetric_stf_tt_readout`, and that wrapper had no graph callers. Textual
inventory additionally identified P042 and P043 verifiers and the breathing,
separable, and TT tests as compatibility consumers.

P047 preserves both existing separable API signatures and routes them through
the new generic arbitrary-axis implementation. The added APIs have no prior
callers. The l=2 numerical application depends on the unchanged C-PDE-004
solver and moment trace; it adds reusable time-derivative and conditional
coefficient functions without changing the solver interface.

Targeted replay passes 60 tests, P042 with 37 checks, P043 with 26 checks, and
P046 with 31 checks, all with process status zero. Prospective source consumers
are QB3 and QB4; both are still pending and may import only the accepted tensor
conventions and conditional scope. Generated documentation, claim/release
memory, migration inventory, and the full repository gate remain promotion
transaction consumers.

Post-change graph detection reports 26 shifted/touched symbols, six affected
flows, and a nominal high risk. Context inspection shows that the solver,
generic TT power, and circular-pair flows are false positives from line-range
shifts after inserting new helpers; their bodies did not change. The one real
compatibility flow is the preserved separable readout wrapper already covered
by P042/P043 and exact tests. No canonical symbol was removed or renamed.

At the unchanged promotion boundary, `scripts/validate.sh` exits zero with 59
accepted claims, a 218-unit queue with 173 pending units, valid generated docs,
memory, and skill, plus all 335 collected tests passing. `git diff --check`
also exits zero. No unresolved direct or indirect consumer remains.
