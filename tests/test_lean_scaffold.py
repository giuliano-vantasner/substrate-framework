from __future__ import annotations

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def test_lean_project_is_pinned_and_imports_repository_glue() -> None:
    assert (ROOT / "formal/lean-toolchain").read_text(encoding="utf-8").strip() == (
        "leanprover/lean4:v4.28.0"
    )
    lakefile = (ROOT / "formal/lakefile.lean").read_text(encoding="utf-8")
    assert 'mathlib4.git" @ "v4.28.0"' in lakefile
    root_module = (ROOT / "formal/SubstrateFramework.lean").read_text(
        encoding="utf-8"
    )
    assert "import SubstrateFramework.Glue" in root_module


def test_formal_source_has_no_proof_escape_and_setup_scripts_parse() -> None:
    glue = (ROOT / "formal/SubstrateFramework/Glue.lean").read_text(encoding="utf-8")
    for token in ("sorry", "admit", "axiom", "unsafe"):
        assert token not in glue
    for relative in ("scripts/setup_lean.sh", "scripts/check_lean.sh"):
        result = subprocess.run(
            ["bash", "-n", str(ROOT / relative)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
    setup = (ROOT / "scripts/setup_lean.sh").read_text(encoding="utf-8")
    assert 'elan toolchain list | grep -Fqx "$toolchain"' in setup
    assert "Mathlib.olean" in setup
    check = (ROOT / "scripts/check_lean.sh").read_text(encoding="utf-8")
    assert "ELAN_HOME" in check


def test_agent_bootstrap_installs_lean_environment() -> None:
    bootstrap = (ROOT / "scripts/bootstrap.sh").read_text(encoding="utf-8")
    assert '"$repo_root/scripts/setup_lean.sh"' in bootstrap
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "/formal/.lake/" in ignore
