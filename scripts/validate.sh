#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/validate.sh
  scripts/validate.sh --full
  scripts/validate.sh --fixed-only
  scripts/validate.sh --pytest-scope SELECTOR [SELECTOR ...]

Every mode runs the repository, generated-state, memory, skill, import, and
compile checks. With no arguments or --full, pytest runs the complete suite;
--fixed-only runs no pytest and is appropriate only when impact selection finds
no affected test. Arguments after --pytest-scope must be repository test files,
directories, or node IDs. Pytest options are rejected so collection-only or
similar flags cannot be mistaken for executed validation.
EOF
}

pytest_mode="full"
pytest_args=()
case "${1:-}" in
  "")
    ;;
  --full)
    if [ "$#" -ne 1 ]; then
      echo "ERROR: --full does not accept additional arguments" >&2
      usage >&2
      exit 2
    fi
    ;;
  --fixed-only)
    if [ "$#" -ne 1 ]; then
      echo "ERROR: --fixed-only does not accept additional arguments" >&2
      usage >&2
      exit 2
    fi
    pytest_mode="fixed-only"
    ;;
  --pytest-scope)
    shift
    if [ "$#" -eq 0 ]; then
      echo "ERROR: --pytest-scope requires at least one pytest selector" >&2
      usage >&2
      exit 2
    fi
    pytest_mode="scoped"
    pytest_args=("$@")
    for selector in "${pytest_args[@]}"; do
      case "$selector" in
        -* )
          echo "ERROR: pytest options are not allowed in --pytest-scope: $selector" >&2
          exit 2
          ;;
        tests|tests/*|tools/agent-memory/tests|tools/agent-memory/tests/*)
          ;;
        *)
          echo "ERROR: pytest scope must select repository tests: $selector" >&2
          exit 2
          ;;
      esac
    done
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    echo "ERROR: unknown validation option: $1" >&2
    usage >&2
    exit 2
    ;;
esac

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
memory_log="$(mktemp)"
trap 'rm -f "$memory_log"' EXIT
if memory validate "$repo_root/memory" >"$memory_log" 2>&1; then
  memory_summary="$(grep -E 'All [0-9]+ file\(s\) valid\.' "$memory_log" | tail -n 1 || true)"
  memory_warning_count="$(grep -c '\[warn\]' "$memory_log" || true)"
  if [ -n "$memory_summary" ]; then
    printf '%s\n' "$memory_summary"
  else
    echo "MEMORY VALIDATION PASS"
  fi
  if [ "$memory_warning_count" -gt 0 ]; then
    echo "MEMORY VALIDATION WARNINGS: $memory_warning_count (run 'memory validate $repo_root/memory' for details)"
  fi
else
  cat "$memory_log" >&2
  exit 1
fi
"$python_bin" "$repo_root/.agents/skills/physics-erdos-loop/scripts/validate_skill.py" \
  "$repo_root/.agents/skills/physics-erdos-loop"
"$python_bin" -m compileall -q "$repo_root/src" "$repo_root/tools/agent-memory/src"
if [ "$pytest_mode" = "full" ]; then
  PYTHONPATH="$repo_root/src" "$python_bin" -m pytest -q
  echo "ALL REPOSITORY WORKFLOW CHECKS PASS (full pytest suite)"
elif [ "$pytest_mode" = "fixed-only" ]; then
  echo "ALL FIXED REPOSITORY CHECKS PASS (no affected pytest scope)"
else
  printf 'Running requested pytest scope:'
  printf ' %q' "${pytest_args[@]}"
  printf '\n'
  PYTHONPATH="$repo_root/src" "$python_bin" -m pytest -q -- "${pytest_args[@]}"
  echo "ALL FIXED REPOSITORY CHECKS AND REQUESTED PYTEST SCOPE PASS"
fi
