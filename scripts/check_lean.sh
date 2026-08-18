#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v lake >/dev/null 2>&1; then
  elan_bin_dir="${ELAN_HOME:-${HOME}/.elan}/bin"
  if [ -x "$elan_bin_dir/lake" ]; then
    export PATH="$elan_bin_dir:$PATH"
  else
    echo "ERROR: Lake is unavailable; run scripts/setup_lean.sh." >&2
    exit 1
  fi
fi

if rg -n '\b(sorry|admit|axiom|unsafe)\b' \
  "$repo_root/formal/SubstrateFramework.lean" \
  "$repo_root/formal/SubstrateFramework"; then
  echo "ERROR: formal source contains a forbidden proof escape." >&2
  exit 1
fi

cd "$repo_root/formal"
lake build
audit_output="$(lake env lean Audit.lean 2>&1)"
printf '%s\n' "$audit_output"
case "$audit_output" in
  *"does not depend on any axioms"*) ;;
  *)
    echo "ERROR: infrastructure theorem axiom audit did not report an empty footprint." >&2
    exit 1
    ;;
esac

echo "LEAN CHECK PASS: build and axiom audit"
