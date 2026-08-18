#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v pipx >/dev/null 2>&1; then
  echo "ERROR: pipx is required so the memory CLI is available outside a virtual environment." >&2
  echo "Install pipx with your operating-system package manager, then rerun this script." >&2
  exit 1
fi

python3 -m venv "$repo_root/.venv"
"$repo_root/.venv/bin/python" -m pip install -e "$repo_root[dev]"

# The memory command deliberately lives in its own pipx-managed environment.
# It must remain callable without activating the framework development venv.
pipx install --force "$repo_root/tools/agent-memory"

if ! command -v memory >/dev/null 2>&1; then
  echo "ERROR: pipx installed agent-memory, but its binary directory is not on PATH." >&2
  echo "Run 'pipx ensurepath', start a fresh shell, and rerun this script." >&2
  exit 1
fi

memory --version
"$repo_root/scripts/setup_lean.sh"

echo "Bootstrap complete. No virtual-environment activation is needed for memory or repository Lean commands."
echo "Run: $repo_root/scripts/validate.sh"
echo "Formal developments: $repo_root/scripts/check_lean.sh"
