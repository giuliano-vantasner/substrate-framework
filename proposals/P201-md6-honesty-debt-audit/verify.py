#!/usr/bin/env python3
"""Primary exact and adversarial verifier for the P201 MD6 audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.bosonic_fock import factorial_one_modes
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE_ROOT = Path("/home/dan/substrate/merged-framework/bridges/phase-38")
SOURCE = SOURCE_ROOT / "bridge_MD6_honesty_firewall_and_debt_ledger.py"
MD4 = SOURCE_ROOT / "bridge_MD4_growth_threshold_and_the_rescue.py"
PINS = {
    "source": "08b6d263323e3a09da39152c7409795d97477521f2fcf8d57b295922fefa1cbf",
    "release": "fbb97885d564d6dc57c8b5bdf37cd619484a4f361545ea4ae198917de6b2ed05",
    "freeze": "808c9bd4ffa5865f2d47a5342e9ff5c5829c247be7e00df9755be0a8dea5984a",
    "source_audit": "ee24c7a236dc6b8f70bba3d6cefb42f9b4ca5b206f1643de09438cf61a648cf7",
}
DEPENDENCY_HASHES = {
    "bridge_MD1_mode_count_is_a_counting_theorem.py":
        "e7408667dbb6644e4c88a0a1523b6eb5f9058c628b5650ff0bf72cfa3238e5ba",
    "bridge_MD2_phase_variance_and_the_overparametrization.py":
        "7dee2e731cc957c97ee151d3fd3349080460f2dc5781be8d4fd7869a589d2df0",
    "bridge_MD3_vertex_operator_removes_the_single_vacuum_bound.py":
        "2c50b4cacb8746a35f99c26d9f0edd0227314ab9410677aebc54c29812daf128",
    "bridge_MD4_growth_threshold_and_the_rescue.py":
        "269b275b2eabddc0f2539ecd22b672692de8790316b91c0f264d98e3582bc144",
    "bridge_MD5_phase32_preserved_and_isotope_handshake.py":
        "bcc45611ce87312a11cdc35d2bdc4c1a92b2e9fdb44c427f7676701f69326ecb",
}
NAMED_SCALARS = {
    "beta_sq", "beta_a_sq", "S", "rho", "M", "K", "a", "ell",
    "Omega", "omega_ph", "A2",
}
TAG_PREFIXES = ("ILLUSTRATION_", "COMPARATOR_")
EMPIRICAL = (
    "excess_heat", "excess heat", "cop_", "calorimet", "transmutation",
    "measured_dos", "watts",
)
EXTERNAL = ("huang_rhys", "huang-rhys", "franck_condon", "franck-condon")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scan_valued_exact(source: str) -> list[str]:
    """Reproduce MD6's exact, deliberately narrow assignment matcher."""

    offenders: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            name = target.id
            if name.startswith(TAG_PREFIXES):
                continue
            if (
                name in NAMED_SCALARS
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, (int, float))
            ):
                offenders.append(name)
    return offenders


def executable_text_exact(source: str) -> str:
    """Reproduce MD6's top-level-docstring/full-line-comment filtering."""

    tree = ast.parse(source)
    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        tree.body = tree.body[1:]
    lines: list[str] = []
    for node in tree.body:
        segment = ast.get_source_segment(source, node) or ""
        lines.extend(
            line
            for line in segment.splitlines()
            if not line.strip().startswith("#")
        )
    return "\n".join(lines).lower()


def scan_literals_exact(source: str, needles: tuple[str, ...]) -> list[str]:
    text = executable_text_exact(source)
    return [needle for needle in needles if needle in text]


def check_call(source_tree: ast.AST, prefix: str) -> ast.Call:
    for node in ast.walk(source_tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            and len(node.args) >= 2
        ):
            continue
        label = node.args[0]
        if isinstance(label, ast.Constant) and isinstance(label.value, str):
            if label.value.startswith(prefix):
                return node
    raise LookupError(prefix)


def names_loaded(node: ast.AST) -> set[str]:
    return {
        child.id
        for child in ast.walk(node)
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load)
    }


def flows_to_check(source: str, origin: str) -> bool:
    """Conservative local name-flow witness from an assignment into a check."""

    tree = ast.parse(source)
    assignment_inputs: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            dependencies = names_loaded(node.value)
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignment_inputs.setdefault(target.id, set()).update(dependencies)
    reachable = {origin}
    changed = True
    while changed:
        changed = False
        for target, dependencies in assignment_inputs.items():
            if target not in reachable and dependencies & reachable:
                reachable.add(target)
                changed = True
    return any(
        names_loaded(node.args[1]) & reachable
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
        and len(node.args) >= 2
    )


def unconditional_empty_ledger(source: str) -> bool:
    tree = ast.parse(source)
    call = check_call(tree, "DEBT LEDGER IS EMPTY")
    condition = call.args[1]
    return isinstance(condition, ast.Constant) and condition.value is True


def main() -> int:
    checks = CheckLedger("P201-MD6-PRIMARY")
    checks.check("MD6 source remains pinned", digest(SOURCE) == PINS["source"])
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.149.0.yaml") == PINS["release"],
    )
    checks.check(
        "formula freeze remains pinned",
        digest(CAMPAIGN / "evidence/formula-freeze.yaml") == PINS["freeze"],
    )
    checks.check(
        "reused source-audit module remains pinned",
        digest(ROOT / "src/substrate_framework/source_audit.py") == PINS["source_audit"],
    )
    checks.check(
        "all five scanned dependency bytes remain pinned",
        all(digest(SOURCE_ROOT / name) == expected for name, expected in DEPENDENCY_HASHES.items()),
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    literal_calls = [
        node
        for node in calls
        if node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]
    checks.check(
        "source inventory separates 23 sites from 40 loop executions",
        len(calls) == 23
        and len(literal_calls) == 18
        and not any(isinstance(node, ast.Assert) for node in ast.walk(source_tree)),
    )
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "MD6 has no quadrature compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    dependency_texts = {
        name: (SOURCE_ROOT / name).read_text(encoding="utf-8")
        for name in DEPENDENCY_HASHES
    }
    checks.check(
        "exact valued matcher returns no selected direct numeric assignments",
        all(not scan_valued_exact(text) for text in dependency_texts.values()),
    )
    checks.check(
        "exact lexical matchers return no selected empirical or external substrings",
        all(
            not scan_literals_exact(text, EMPIRICAL)
            and not scan_literals_exact(text, EXTERNAL)
            for text in dependency_texts.values()
        ),
    )
    declared_files = next(
        node.value
        for node in source_tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "FILES" for target in node.targets)
    )
    checks.check(
        "runtime scope is exactly five sibling names without internal hashes or self-scan",
        isinstance(declared_files, ast.List)
        and tuple(item.value for item in declared_files.elts) == tuple(DEPENDENCY_HASHES)
        and "hashlib" not in names_loaded(source_tree)
        and SOURCE.name not in source_text[source_text.find("FILES ="):source_text.find("NAMED_SCALARS")],
    )

    checks.mutation_sensitive(
        "valued scanner recognizes only its direct Assign fixture",
        lambda candidate: scan_valued_exact(str(candidate)) == ["beta_sq"],
        "beta_sq = 0.245",
        (
            "beta_sq: float = 0.245",
            "beta_sq = -0.245",
            "beta_sq = float('0.245')",
            "beta_sq, other = 0.245, 1",
            "(beta_sq := 0.245)",
            "config.beta_sq = 0.245",
            "config['beta_sq'] = 0.245",
        ),
    )
    checks.check(
        "tag prefix exempts a direct numeric assignment without tracing its use",
        scan_valued_exact("ILLUSTRATION_beta_sq = 0.245\ncheck('gate', ILLUSTRATION_beta_sq > 0)") == [],
    )
    checks.mutation_sensitive(
        "literal scanner recognizes only its finite textual vocabulary",
        lambda candidate: scan_literals_exact(str(candidate), EMPIRICAL) == ["excess_heat"],
        "value = excess_heat",
        (
            "value = 'excess_' + 'heat'",
            "calibration = 30\ncheck('gate', result < calibration)",
            "value = imported_comparator",
        ),
    )
    checks.check(
        "nested docstrings and negated string data create lexical false positives",
        scan_literals_exact(
            "def f():\n    '''no measured_dos input is used'''\n    return 1\n",
            EMPIRICAL,
        ) == ["measured_dos"]
        and scan_literals_exact("message = 'no excess_heat input'", EMPIRICAL) == ["excess_heat"],
    )

    md4_text = MD4.read_text(encoding="utf-8")
    checks.check(
        "both tagged MD4 values have executable name-flow into pass conditions",
        flows_to_check(md4_text, "COMPARATOR_WN6_log10_w")
        and flows_to_check(md4_text, "ILLUSTRATION_beta_sq"),
    )
    checks.check(
        "comparator directly controls two substantive inequalities",
        "gain > mp.mpf('5e7')" in md4_text
        and "COMPARATOR_WN6_log10_w < mp.mpf('-1e7')" in md4_text,
    )

    checks.check(
        "empty-ledger verdict is an unconditional literal",
        unconditional_empty_ledger(source_text),
    )
    checks.mutation_sensitive(
        "unconditional-ledger detector is sensitive to an actual predicate",
        lambda condition: unconditional_empty_ledger(
            f"check('DEBT LEDGER IS EMPTY', {condition})"
        ),
        "True",
        ("False", "debt == 0"),
    )
    residual = check_call(source_tree, "NO NEW RESIDUAL").args[1]
    checks.check(
        "no-new-residual condition is only three selected clauses",
        isinstance(residual, ast.BoolOp)
        and isinstance(residual.op, ast.And)
        and len(residual.values) == 3,
    )

    c, omega_0, volume, cell, omega = sp.symbols(
        "c omega_0 V a omega", positive=True
    )
    k_cutoff = (6 * sp.pi**2) ** sp.Rational(1, 3) / cell
    density_3d = (
        volume * omega * sp.sqrt(omega**2 - omega_0**2)
        / (2 * sp.pi**2 * c**3)
    )
    integral = sp.simplify(
        sp.integrate(
            density_3d,
            (omega, omega_0, sp.sqrt(omega_0**2 + c**2 * k_cutoff**2)),
        )
    )
    checks.check(
        "declared three-dimensional one-branch density integrates conditionally",
        sp.simplify(integral - volume / cell**3) == 0,
    )
    checks.check(
        "gap independence does not derive dimension branch count volume or cutoff",
        sp.diff(integral, omega_0) == 0
        and integral.free_symbols == {volume, cell},
    )
    mode_count, coupling, population = sp.symbols("M S n", positive=True)
    checks.check(
        "M cancellation is the conditional substitution A squared equals S over M",
        sp.simplify(
            population - mode_count * (coupling / mode_count) - (population - coupling)
        ) == 0,
    )

    size, rho = sp.symbols("N rho", positive=True)
    fixed_weight = sp.symbols("w", positive=True)
    fixed_response = rho / (size * fixed_weight + rho)
    checks.check(
        "fixed-weight partial derivative is strictly negative",
        sp.diff(fixed_response, size).is_negative,
    )
    checks.check(
        "branching magnitude retains nonzero rho dependence",
        sp.simplify(sp.diff(fixed_response, rho))
        == size * fixed_weight / (size * fixed_weight + rho) ** 2,
    )
    weight = sp.Function("w")
    total_response = rho / (size * weight(size) + rho)
    expected_total = -rho * (
        weight(size) + size * sp.diff(weight(size), size)
    ) / (size * weight(size) + rho) ** 2
    checks.check(
        "population-dependent total derivative retains the C-BRN-002 control",
        sp.simplify(sp.diff(total_response, size) - expected_total) == 0,
    )
    checks.mutation_sensitive(
        "weight-derivative term is load bearing",
        lambda coefficient: sp.simplify(
            weight(size)
            + coefficient * size * sp.diff(weight(size), size)
            - (weight(size) + size * sp.diff(weight(size), size))
        ) == 0,
        1,
        (0, 2),
    )
    checks.check(
        "positive integer intensity has the complete adjacent-mode tie",
        factorial_one_modes(intensity=20, support="all_nonnegative") == (19, 20),
    )
    checks.check(
        "source floor-only mode claim is incomplete",
        '"n* = floor(S)"' in source_text
        and factorial_one_modes(intensity=20, support="all_nonnegative") != (20,),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
