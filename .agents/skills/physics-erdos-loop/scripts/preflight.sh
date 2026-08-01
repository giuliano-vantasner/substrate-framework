#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
ok=0
warn=0

good() { printf '  [ok]   %s\n' "$1"; ok=$((ok + 1)); }
miss() { printf '  [WARN] %s\n' "$1"; warn=$((warn + 1)); }

echo "physics-erdos-loop preflight"
echo "Oracles and tooling:"
if python3 -c 'import sympy,numpy,scipy,yaml' 2>/dev/null; then
  good "Python symbolic/numeric stack"
else
  miss "sympy/numpy/scipy/PyYAML stack incomplete"
fi
if command -v lean >/dev/null 2>&1 && command -v lake >/dev/null 2>&1; then
  good "Lean/Lake available"
else
  miss "Lean/Lake unavailable (needed only for formal claims)"
fi
if command -v memory >/dev/null 2>&1 || [ -x "$repo_root/.venv/bin/memory" ]; then
  good "agent-memory CLI available"
else
  miss "memory CLI unavailable; run scripts/bootstrap.sh"
fi

echo "Governance surfaces:"
for path in AGENTS.md governance/claims.yaml governance/releases/current.yaml memory-templates/research-arc.md; do
  if [ -f "$repo_root/$path" ]; then
    good "$path"
  else
    miss "$path missing"
  fi
done

echo "Repository state:"
git -C "$repo_root" status --short --branch || true
echo "ok=$ok warn=$warn"
