#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_bin="${PYTHON:-python3}"

PYTHONPATH="$repo_root/src" "$python_bin" "$repo_root/scripts/validate_repository.py"
PYTHONPATH="$repo_root/src" "$python_bin" "$repo_root/scripts/render_docs.py" --check
PYTHONPATH="$repo_root/tools/agent-memory/src" "$python_bin" -c \
  'from click.testing import CliRunner; from agent_memory.cli import cli; result=CliRunner().invoke(cli, ["--help"]); assert result.exit_code == 0, result.output'
"$python_bin" "$repo_root/.claude/skills/physics-erdos-loop/scripts/validate_skill.py" \
  "$repo_root/.claude/skills/physics-erdos-loop"
"$python_bin" -m compileall -q "$repo_root/src" "$repo_root/tools/agent-memory/src"
PYTHONPATH="$repo_root/src" "$python_bin" -m pytest -q
echo "ALL REPOSITORY WORKFLOW CHECKS PASS"
