# Substrate Framework

This repository is the cohesive, reviewable successor workspace for the Substrate physics framework. It starts with workflow and governance infrastructure; scientific claims are migrated only after claim-by-claim reconciliation.

The central rule is that chronology is not authority. Campaigns are immutable research records, proposals are unaccepted work, and the canonical framework is a reproducible materialized view of individually accepted claims.

## Repository model

- `src/substrate_framework/` contains importable framework definitions and derivations.
- `governance/claims.yaml` is the machine-readable accepted/proposed claim graph.
- `proposals/` contains candidate campaigns before adjudication.
- `campaigns/` contains immutable adjudicated campaign records.
- `governance/releases/` pins reproducible accepted claim sets.
- `docs/generated/` is generated from the accepted registry; agents do not hand-edit it.
- `memory-templates/` contains durable work, research, review, and promotion contracts.
- `tools/agent-memory/` contains the memory CLI program only. No prior memory entries were copied.
- `.agents/skills/physics-erdos-loop/` contains the repository-scoped native Codex physics workflow.

## Bootstrap

```bash
python3 -m venv .venv
.venv/bin/pip install -e . -e tools/agent-memory
scripts/validate.sh
```

Read `AGENTS.md` before starting any research or migration. A fresh effort begins by instantiating the appropriate file from `memory-templates/`; it does not begin by editing canonical prose.

## Initial state

The registry is intentionally empty. No claim from the earlier sequential corpus is accepted here merely because it was late, committed, numerically attractive, or described as settled. Migration begins from a named source release and adjudicates the whole framework for self-consistency.
