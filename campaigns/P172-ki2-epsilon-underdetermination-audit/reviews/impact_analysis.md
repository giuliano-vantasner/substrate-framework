# P172 impact analysis

P172 is a record-only qualification of pending source unit KI2. It changes no
canonical symbol, scientific API, accepted claim statement, dependency, release
manifest, or generated accepted documentation.

The accepted scientific surface is C-BPS-001, C-SK-001, C-BPS-003,
`src/substrate_framework/bps_energy.py`, `tests/test_bps_energy.py`, and
`tests/test_skyrme_relations.py`. Those artifacts and the accepted P008/P107
evidence are hash-identical. P172 reuses the hashes, calls the canonical BPS API
in its new transformation oracle, and replays focused tests rather than
ceremonially repeating the unchanged accepted derivation matrices.

The pinned executable graph contains E3, E4, S4, NY1, NY2, KI1 through KI4,
and MK1 through MK3. It covers 81 predicates and ten assertions. Eleven nodes
retain clean local tallies; KI1 alone fails at its governed refutation. This
typing matters more than tally color: KI2 is qualified, and every KI3/KI4/MK
reverse consumer remains pending.

The exact Phase-34 Lean file remains valid but weakly encoded for the disputed
claim: it proves local ratio scaling and `F/e` invariance while omitting the
accepted BPS energy and bound. No formal theorem or source file is rewritten.

The mutable transaction consists of the P172 campaign, archived proposal and
source-review memory, KI2's qualified disposition, regenerated source queue,
and parent migration effort. The accepted registry, v0.127.0 manifest,
accepted claim memory, and `docs/generated/` remain byte-unchanged.
