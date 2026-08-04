# P134 impact analysis

The graph index was refreshed at freeze commit `9cbd587` with `gitnexus analyze
--index-only`. Pre-edit upstream impact for both accepted helpers that P134
reuses—`u1_field_strength` and `riesz_green_kernel`—reported zero affected
symbols, zero affected processes, and LOW risk. P134 leaves both APIs unchanged
and adds `maxwell.py`, focused tests, package exports, and a source-compatibility
AST audit.

The first post-edit command, `gitnexus detect`, failed because this installed CLI
uses `detect-changes`; attempt 0010 preserves that usage failure. The corrected
command reports 10 tracked files and 28 changed symbols, zero affected
processes, and LOW risk. Untracked new files are not included in that diff-based
count, so this result is not used as evidence that the new API is correct. Its
scientific and consumer evidence instead comes from exact primary and
independent verifiers, focused package tests, and the hash-pinned 18-node source
graph replay.

No canonical symbol is renamed or removed. The direct package consumers are the
new tests, campaign verifiers, package export list, claim registry, release,
generated documentation, and generated memory. The wider predecessor consumer
set is recorded in `evidence/consumer-audit.yaml`; none imports EM3 executably.
The resulting change risk is LOW and additive, conditional on replaying the
named tests and governance consumers before promotion.
