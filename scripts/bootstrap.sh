#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 -m venv "$repo_root/.venv"
"$repo_root/.venv/bin/pip" install -e "$repo_root" -e "$repo_root/tools/agent-memory"
echo "Bootstrap complete. Run: $repo_root/scripts/validate.sh"
