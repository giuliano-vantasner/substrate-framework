from __future__ import annotations

import os
from pathlib import Path
import subprocess

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE_SCRIPT = REPO_ROOT / "scripts" / "validate.sh"


@pytest.fixture
def validation_environment(tmp_path: Path) -> tuple[dict[str, str], Path]:
    command_log = tmp_path / "commands.log"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()

    python_stub = bin_dir / "python-stub"
    python_stub.write_text(
        "#!/usr/bin/env bash\n"
        "printf 'python' >> \"$VALIDATE_TEST_LOG\"\n"
        "for arg in \"$@\"; do printf '|%s' \"$arg\" >> \"$VALIDATE_TEST_LOG\"; done\n"
        "printf '\\n' >> \"$VALIDATE_TEST_LOG\"\n"
        "case \"$*\" in\n"
        "  *'from agent_memory import __version__'*) printf '0.0\\n' ;;\n"
        "esac\n",
        encoding="utf-8",
    )
    python_stub.chmod(0o755)

    memory_stub = bin_dir / "memory"
    memory_stub.write_text(
        "#!/usr/bin/env bash\n"
        "printf 'memory' >> \"$VALIDATE_TEST_LOG\"\n"
        "for arg in \"$@\"; do printf '|%s' \"$arg\" >> \"$VALIDATE_TEST_LOG\"; done\n"
        "printf '\\n' >> \"$VALIDATE_TEST_LOG\"\n"
        "if [ \"${1:-}\" = '--version' ]; then printf 'memory 0.0\\n'; fi\n",
        encoding="utf-8",
    )
    memory_stub.chmod(0o755)

    environment = os.environ.copy()
    environment.update(
        {
            "PATH": f"{bin_dir}:{environment['PATH']}",
            "PYTHON": str(python_stub),
            "VALIDATE_TEST_LOG": str(command_log),
        }
    )
    return environment, command_log


def run_validation(
    environment: dict[str, str], *arguments: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(VALIDATE_SCRIPT), *arguments],
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("arguments", [(), ("--full",)])
def test_full_validation_runs_unscoped_pytest(
    validation_environment: tuple[dict[str, str], Path],
    arguments: tuple[str, ...],
) -> None:
    environment, command_log = validation_environment

    result = run_validation(environment, *arguments)

    assert result.returncode == 0, result.stderr
    assert "ALL REPOSITORY WORKFLOW CHECKS PASS (full pytest suite)" in result.stdout
    pytest_calls = [
        line
        for line in command_log.read_text(encoding="utf-8").splitlines()
        if line.startswith("python|-m|pytest|")
    ]
    assert pytest_calls == ["python|-m|pytest|-q"]


def test_scoped_validation_passes_selectors_verbatim_to_pytest(
    validation_environment: tuple[dict[str, str], Path],
) -> None:
    environment, command_log = validation_environment
    selectors = (
        "tests/test_governance.py",
        "tests/test_numerics.py::test_trapezoid_integral",
    )

    result = run_validation(environment, "--pytest-scope", *selectors)

    assert result.returncode == 0, result.stderr
    assert "ALL FIXED REPOSITORY CHECKS AND REQUESTED PYTEST SCOPE PASS" in result.stdout
    pytest_calls = [
        line
        for line in command_log.read_text(encoding="utf-8").splitlines()
        if line.startswith("python|-m|pytest|")
    ]
    assert pytest_calls == [f"python|-m|pytest|-q|--|{'|'.join(selectors)}"]


def test_scoped_validation_requires_a_selector(
    validation_environment: tuple[dict[str, str], Path],
) -> None:
    environment, command_log = validation_environment

    result = run_validation(environment, "--pytest-scope")

    assert result.returncode == 2
    assert "requires at least one pytest selector" in result.stderr
    assert not command_log.exists()


@pytest.mark.parametrize("selector", ["--collect-only", "src/substrate_framework"])
def test_scoped_validation_rejects_non_test_selectors(
    validation_environment: tuple[dict[str, str], Path], selector: str
) -> None:
    environment, command_log = validation_environment

    result = run_validation(environment, "--pytest-scope", selector)

    assert result.returncode == 2
    assert "ERROR:" in result.stderr
    assert not command_log.exists()
