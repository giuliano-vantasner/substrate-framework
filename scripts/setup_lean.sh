#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
toolchain="$(tr -d '[:space:]' < "$repo_root/formal/lean-toolchain")"
elan_bin_dir="${ELAN_HOME:-${HOME}/.elan}/bin"

if ! command -v elan >/dev/null 2>&1; then
  if [ -x "$elan_bin_dir/elan" ]; then
    export PATH="$elan_bin_dir:$PATH"
  else
    if ! command -v curl >/dev/null 2>&1; then
      echo "ERROR: curl is required to install the pinned Lean toolchain." >&2
      exit 1
    fi
    echo "Installing elan for the repository-pinned Lean toolchain."
    curl --proto '=https' --tlsv1.2 -sSf \
      https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
      | sh -s -- -y --default-toolchain none
    export PATH="$elan_bin_dir:$PATH"
  fi
fi

if ! elan toolchain list | grep -Fqx "$toolchain"; then
  elan toolchain install "$toolchain"
fi

cd "$repo_root/formal"
if [ ! -f lake-manifest.json ]; then
  lake update
fi
if [ ! -f .lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ]; then
  lake exe cache get
fi
lake build

echo "Lean setup complete: $toolchain"
echo "Run: $repo_root/scripts/check_lean.sh"
