#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -n "${PYTHON:-}" ]; then
  python_bin="$PYTHON"
elif [ -x "$repo_root/.venv/bin/python" ]; then
  python_bin="$repo_root/.venv/bin/python"
else
  python_bin="python3"
fi

PYTHONPATH="$repo_root/src" "$python_bin" "$repo_root/scripts/validate_repository.py"
PYTHONPATH="$repo_root/src" "$python_bin" "$repo_root/scripts/render_docs.py" --check
PYTHONPATH="$repo_root/src" "$python_bin" "$repo_root/scripts/render_memory.py" --check
"$python_bin" -c 'import numpy, scipy, sympy, yaml'
if ! command -v memory >/dev/null 2>&1; then
  echo "ERROR: memory is not on PATH; run scripts/bootstrap.sh" >&2
  exit 1
fi
bundled_memory_version="$(PYTHONPATH="$repo_root/tools/agent-memory/src" "$python_bin" -c 'from agent_memory import __version__; print(__version__)')"
installed_memory_version="$(memory --version)"
case "$installed_memory_version" in
  *"$bundled_memory_version"*) ;;
  *)
    echo "ERROR: installed memory CLI does not match bundled version $bundled_memory_version: $installed_memory_version" >&2
    exit 1
    ;;
esac
memory --help >/dev/null
memory validate "$repo_root/memory"
"$python_bin" "$repo_root/.agents/skills/physics-erdos-loop/scripts/validate_skill.py" \
  "$repo_root/.agents/skills/physics-erdos-loop"
"$python_bin" -m compileall -q "$repo_root/src" "$repo_root/tools/agent-memory/src"
PYTHONPATH="$repo_root/src" "$python_bin" -m pytest -q
echo "ALL REPOSITORY WORKFLOW CHECKS PASS"
