# P058 impact analysis

P058 adds pure functions and one evidence dataclass to
`src/substrate_framework/wzw.py`; it does not change existing trace-five,
period, phase, or cohomology behavior.

GitNexus reported LOW upstream risk for both `wzw.py` and the reused
`alternating_trace` helper. The helper has two direct canonical callers and
seven total upstream symbols. Its only indexed scientific process is the
existing `su3_trace_five_cohomology` flow; P058 leaves the helper unchanged.
The file-level report found one direct and four total dependents with no
affected process. The required replay surface is therefore the complete WZW
test module, P056/P057 canonical regression paths through those tests, the new
P058 primary and independent verifiers, registry/release validation, and all
generated consumers.

The pre-commit all-change replay reports MEDIUM file-level risk because the
shared WZW module and registry consumers change. Its five affected indexed
processes are all existing `su3_trace_five_cohomology` paths through unchanged
helpers. The new winding APIs have no pre-existing indexed caller. The full
WZW module tests and repository gate therefore exercise both the new surface
and every reported legacy path; no canonical symbol was renamed or removed.

Narrative consumers found in the migration graph include WZ4, QCD7, MK2.2,
MK5, and later units that cite WZ3. They remain pending and acquire no accepted
baryon, anomaly, or `N_c` premise from this campaign. The accepted claim adds a
new dependency only on C-LIE-001.
