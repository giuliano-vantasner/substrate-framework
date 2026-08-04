"""Primary predicate and semantic-ceiling verifier for P127/GB6."""

from __future__ import annotations

import ast
import hashlib
import io
import math
from pathlib import Path
import tokenize
import unicodedata

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


SOURCE_ROOT = Path("/home/dan/substrate/merged-framework/bridges/phase-32")
CAMPAIGN = Path("campaigns/P127-gb6-honesty-firewall-audit")
FILES = {
    "GB1": "bridge_GB1_channel_definitions.py",
    "GB2": "bridge_GB2_subdivision_kinematics.py",
    "GB3": "bridge_GB3_dicke_asymmetry.py",
    "GB4": "bridge_GB4_branching_ratio.py",
    "GB5": "bridge_GB5_spectral_peak.py",
    "GB6": "bridge_GB6_honesty_firewall_guard.py",
}
HASHES = {
    "GB1": "ace0515d7ea362ef45a55db22308aecffdad9a003d03f2b1209c0a11874b489b",
    "GB2": "e76bf26d134f48b74ba1d23bc90c5ee49d3e980edc10304a24b85af421c2b54c",
    "GB3": "a168a03545312409cd41cb9b5217f54759c8564eba0e7d8ad2252faf8bcee70d",
    "GB4": "497ed6deda4a0f11562baeaef0ec7bc21cc20b38d3d11c69ed07728ed33faeb0",
    "GB5": "0f7f1a4a1ba4ab548b27de1924c84af984971eb84f50de3544045a3150dbec3e",
    "GB6": "edcfc0fafad48dbfc88ebf97613d45c1b6cf7e85b95548ae4006b373a2cfc49a",
}
FREEZE_HASH = "28ca23f3f2184f5dc5e68859c4006a85b0f7f765689f4c81c864775ecd5f35c4"
WN7 = Path("/home/dan/substrate/merged-framework/bridges/phase-37/bridge_WN7_honesty_firewall_guard.py")
WN7_HASH = "88844689bf682ca5ff524378f4e5e46a25bcab54b1a3a6e59afe69b990694d50"
IMPORT_MARK = "[IMPORT]"
BARRIER = ("u_e", "gamow", "screening_enhancement", "gamow_energy_kev")
NUCLEAR_LITERALS = ("0.0362", "90.35", "0.999757")
EMPIRICAL = ("excess_heat_watts", "cop_measured", "transmutation_yield")
GB_FILES = tuple(FILES[unit] for unit in ("GB1", "GB2", "GB3", "GB4", "GB5"))


def literal_scan(text: str, forbidden: tuple[str, ...]) -> list[tuple[int, str]]:
    """Reproduce GB6's case-insensitive substring and line-exemption matcher."""

    violations: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if IMPORT_MARK in line:
            continue
        lowered = line.lower()
        violations.extend(
            (line_number, literal) for literal in forbidden if literal in lowered
        )
    return violations


def clamp_scan(text: str) -> list[str]:
    """Reproduce GB6's two-spelling clamp matcher."""

    matches = []
    for line in text.splitlines():
        code = line.split("#", 1)[0]
        if ("min(" in code and ("cap" in code.lower() or "ceil" in code.lower())) or (
            "CEILING" in code
        ):
            matches.append(line)
    return matches


def _constant_expression(node: ast.AST, known: dict[str, object]) -> object:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name) and node.id in known:
        return known[node.id]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _constant_expression(node.left, known) + _constant_expression(
            node.right, known
        )
    if isinstance(node, (ast.List, ast.Tuple)):
        return tuple(_constant_expression(item, known) for item in node.elts)
    raise ValueError(ast.dump(node))


def constant_assignments(tree: ast.Module) -> dict[str, object]:
    values: dict[str, object] = {}
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            try:
                values[node.targets[0].id] = _constant_expression(node.value, values)
            except (TypeError, ValueError):
                pass
    return values


def imports(text: str) -> set[str]:
    tree = ast.parse(text)
    modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    modules.update(
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    )
    return modules


def identifiers(text: str) -> set[str]:
    tree = ast.parse(text)
    result = {node.id.lower() for node in ast.walk(tree) if isinstance(node, ast.Name)}
    result.update(
        node.attr.lower()
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    )
    return result


def comments(text: str) -> tuple[str, ...]:
    tokens = tokenize.generate_tokens(io.StringIO(text).readline)
    return tuple(token.string for token in tokens if token.type == tokenize.COMMENT)


def numeric_check_dependencies(text: str) -> set[int | float | complex]:
    """Collect numeric literals in or transitively assigned into check conditions."""

    tree = ast.parse(text)
    assigned: dict[str, ast.AST] = {}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            assigned[node.targets[0].id] = node.value

    def collect(node: ast.AST, active: frozenset[str] = frozenset()) -> set[int | float | complex]:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, complex)):
            return set() if isinstance(node.value, bool) else {node.value}
        if isinstance(node, ast.Name) and node.id in assigned and node.id not in active:
            return collect(assigned[node.id], active | {node.id})
        values: set[int | float | complex] = set()
        for child in ast.iter_child_nodes(node):
            values.update(collect(child, active))
        return values

    numbers: set[int | float | complex] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            and len(node.args) >= 2
        ):
            numbers.update(collect(node.args[1]))
    return numbers


def source_suppression_guard(expr: sp.Expr, N: sp.Symbol, w: sp.Symbol, rho: sp.Symbol) -> bool:
    derivative = sp.diff(expr, N)
    value = derivative.subs(
        {w: 2, N: 3, rho: sp.Rational(1, 4), sp.Symbol("r_s", positive=True): 1,
         sp.Symbol("r_gamma", positive=True): sp.Rational(1, 4)}
    )
    return bool(value < 0)


OMEGA_EV = 24.0e6
OMEGA_BAND = (1.0e-3, 3.0e-3, 1.0e-2, 3.0e-2, 1.0e-1, 3.0e-1, 1.0)


def source_count_guard(count_fn) -> bool:
    counts = [count_fn(OMEGA_EV, omega) for omega in OMEGA_BAND]
    varies = min(counts) != max(counts)
    monotone = all(counts[index] >= counts[index + 1] for index in range(6))
    bounded = all(
        0.0 <= OMEGA_EV - counts[index] * OMEGA_BAND[index] < OMEGA_BAND[index]
        for index in range(7)
    )
    return bool(varies and monotone and bounded)


def main() -> int:
    checks = CheckLedger("GB6-HONESTY-FIREWALL-AUDIT")
    payloads = {unit: (SOURCE_ROOT / path).read_bytes() for unit, path in FILES.items()}
    texts = {unit: payload.decode("utf-8") for unit, payload in payloads.items()}

    for unit, expected in HASHES.items():
        checks.check(
            f"{unit} source bytes are hash pinned",
            hashlib.sha256(payloads[unit]).hexdigest() == expected,
        )
    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_HASH,
    )
    checks.check(
        "immutable preregistration remains byte identical",
        hashlib.sha256((CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_HASH,
    )

    tree = ast.parse(texts["GB6"])
    assignments = constant_assignments(tree)
    checks.check(
        "GB6's exact exemption and three finite token lists are recovered",
        assignments["IMPORT_MARK"] == IMPORT_MARK
        and assignments["FORBIDDEN_BARRIER"] == BARRIER
        and assignments["FORBIDDEN_IMPORTS"] == NUCLEAR_LITERALS
        and assignments["FORBIDDEN_EMPIRICAL"] == EMPIRICAL,
    )
    checks.check(
        "GB6's hard-coded five-file scope is recovered exactly",
        assignments["GB_FILES"] == GB_FILES,
    )
    check_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "sixteen static calls expand to twenty-nine runtime predicates",
        len(check_calls) == 16 and 5 + 5 + 5 + 2 + 7 + 5 == 29,
    )
    checks.check(
        "GB6 requires no numerical-integration compatibility path",
        all(
            token not in texts["GB6"]
            for token in ("np.trapz", "np.trapezoid", "trapezoid_integral", "scipy.integrate")
        ),
    )

    scanned = tuple(texts[unit] for unit in ("GB1", "GB2", "GB3", "GB4", "GB5"))
    checks.check(
        "the exact barrier matcher is empty on the declared five files",
        all(literal_scan(text, BARRIER) == [] for text in scanned),
    )
    checks.check(
        "the exact three-number matcher is empty on the declared five files",
        all(literal_scan(text, NUCLEAR_LITERALS) == [] for text in scanned),
    )
    checks.check(
        "the exact empirical-name matcher is empty on the declared five files",
        all(literal_scan(text, EMPIRICAL) == [] for text in scanned),
    )
    checks.check(
        "the exact two-spelling clamp matcher is empty on GB4 and GB5",
        clamp_scan(texts["GB4"]) == [] and clamp_scan(texts["GB5"]) == [],
    )
    checks.check(
        "forbidden barrier names are also absent from executable identifiers",
        all(not (set(BARRIER) & identifiers(text)) for text in scanned),
    )

    source_imports = {unit: imports(texts[unit]) for unit in FILES}
    checks.check(
        "fresh AST inventory finds only sys math and sympy imports in GB1 through GB5",
        set().union(*(source_imports[unit] for unit in ("GB1", "GB2", "GB3", "GB4", "GB5")))
        == {"sys", "math", "sympy"},
    )
    checks.check(
        "the three numeric strings are not a Python import-graph oracle",
        literal_scan("from nuclear_matrix import element", NUCLEAR_LITERALS) == []
        and literal_scan("coefficient = 0.0362", NUCLEAR_LITERALS) == [(1, "0.0362")],
    )
    checks.check(
        "GB6 imports no GB implementation and re-embeds all four physics fixtures locally",
        source_imports["GB6"] == {"os", "sys", "sympy", "math"}
        and all(not module.startswith("bridge_GB") for module in source_imports["GB6"]),
    )
    gb6_functions = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    checks.check(
        "GB6 only reads source text and never calls GB1-GB5 functions",
        gb6_functions
        == {
            "check",
            "read_src",
            "scan_violations",
            "suppression_strengthens",
            "passes_kinematic_count",
        },
    )

    gb2_numbers = numeric_check_dependencies(texts["GB2"])
    gb3_numbers = numeric_check_dependencies(texts["GB3"])
    gb5_numbers = numeric_check_dependencies(texts["GB5"])
    checks.check(
        "AST dependency tracing finds the 24 MeV conversion in GB2 check conditions",
        24.0 in gb2_numbers and 1.0e6 in gb2_numbers,
    )
    checks.check(
        "AST dependency tracing finds wavelength and coherence magnitudes in GB3 checks",
        {1239.84, 3.0e6, 100.0, 1.0e4} <= gb3_numbers,
    )
    checks.check(
        "AST dependency tracing finds the inert comparison tuples in GB5 checks",
        {1.0, 2.0, 23.0, 27.0} <= gb5_numbers,
    )
    checks.check(
        "three absent empirical names do not close numeric or imported comparator data flow",
        literal_scan('check("fit", abs(output - 30.0) < 0.01)', EMPIRICAL) == []
        and literal_scan('target = config["observed"]; check("fit", output == target)', EMPIRICAL)
        == [],
    )
    checks.check(
        "an empirical-name comment collides while a tagged executable use is exempt",
        literal_scan("# excess_heat_watts is not used", EMPIRICAL)
        == [(1, "excess_heat_watts")]
        and literal_scan("target = excess_heat_watts  # [IMPORT]", EMPIRICAL) == [],
    )

    checks.check(
        "the line-wide case-sensitive exemption can hide executable barrier syntax",
        literal_scan('tag = "[IMPORT]"; value = U_e', BARRIER) == []
        and literal_scan("value = U_e  # [import]", BARRIER) == [(1, "u_e")],
    )
    checks.check(
        "construction aliases and equivalent algebra evade the finite barrier matcher",
        literal_scan('name = "U_" + "e"; value = getattr(model, name)', BARRIER) == []
        and literal_scan("value = exp(-sqrt(scale / (energy + shift)))", BARRIER) == [],
    )
    fullwidth = "value = U\uff3fe"
    checks.check(
        "lack of Unicode normalization creates an equivalent-name evasion",
        literal_scan(fullwidth, BARRIER) == []
        and "u_e" in unicodedata.normalize("NFKC", fullwidth).lower(),
    )
    checks.check(
        "comments docstrings negation and benign substrings create false positives",
        literal_scan("# never use U_e", BARRIER) == [(1, "u_e")]
        and literal_scan('"""No Gamow term is present."""', BARRIER) == [(1, "gamow")]
        and literal_scan("tau_evolution = 0", BARRIER) == [(1, "u_e")],
    )
    checks.check(
        "AST and token routes separate executable names from prose occurrences",
        "u_e" in identifiers("value = U_e\n# Gamow")
        and "u_e" not in identifiers("value = 1\n# U_e")
        and any("U_e" in comment for comment in comments("value = 1\n# U_e")),
    )

    clamp_evasions = (
        "reported = min (raw, limit)",
        "reported = max(lower, min(raw, upper))",
        "reported = np.clip(raw, 0, limit)",
        "reported = raw if raw < limit else limit",
        "reported = saturate(raw)",
        "reported = raw / (1 + abs(raw))",
        "reported = math.tanh(raw)",
    )
    checks.check(
        "seven ordinary bounded constructions evade the two-spelling clamp matcher",
        all(clamp_scan(snippet) == [] for snippet in clamp_evasions),
    )
    checks.check(
        "the clamp evasions include genuinely bounded numerical maps",
        min(10, 1) == 1 and 10 / (1 + abs(10)) < 1 and math.tanh(10) < 1,
    )
    checks.check(
        "a benign capacity identifier creates a clamp false positive",
        clamp_scan("remaining_capacity = min(raw, available)")
        == ["remaining_capacity = min(raw, available)"],
    )
    checks.check(
        "a hash character in string data hides a later literal clamp",
        clamp_scan('label = "#"; reported = min(raw, cap)') == [],
    )

    N, w, rho = sp.symbols("N w rho", positive=True)
    B_true = rho / (w * N + rho)
    B_symmetric = sp.simplify((rho * N) / (w * N + rho * N))
    checks.check(
        "the exact symmetric-N fixture is rejected while the source formula passes",
        source_suppression_guard(B_true, N, w, rho)
        and not source_suppression_guard(B_symmetric, N, w, rho),
    )
    local_only = B_true + (N - 3) ** 2
    checks.check(
        "a nonmonotone expression passes GB6's one-point derivative oracle",
        source_suppression_guard(local_only, N, w, rho)
        and sp.diff(local_only, N).subs({N: 4, w: 2, rho: sp.Rational(1, 4)}) > 0,
    )
    checks.check(
        "the accepted allocation derivative itself is globally negative for positive symbols",
        sp.simplify(sp.diff(B_true, N) + rho * w / (w * N + rho) ** 2) == 0,
    )

    checks.check(
        "the exact floor count passes and the exact constant fixture fails",
        source_count_guard(lambda total, omega: math.floor(total / omega))
        and not source_count_guard(lambda _total, _omega: int(1e8)),
    )

    def band_lookup(total: float, omega: float) -> int:
        if omega in OMEGA_BAND:
            return math.floor(total / omega)
        return 7

    checks.check(
        "a lookup that is correct only on seven samples passes the kinematic guard",
        source_count_guard(band_lookup)
        and not (0.0 <= OMEGA_EV - band_lookup(OMEGA_EV, 0.2) * 0.2 < 0.2),
    )

    hbar = sp.symbols("hbar", positive=True)
    linear = hbar**2 * N
    quadratic = (hbar * N) ** 2
    cubic = hbar**2 * N**3

    def exact_n2_rejected(candidate: sp.Expr) -> bool:
        return bool(
            sp.simplify((candidate - linear).subs(N, 4)) != 0
            and sp.simplify(candidate - hbar**2 * N**2) == 0
        )

    checks.check(
        "the N-squared fixture is detected by its exact polynomial identity",
        exact_n2_rejected(quadratic),
    )
    checks.check(
        "a cubic collective rate is outside the exact N-squared fixture predicate",
        not exact_n2_rejected(cubic) and sp.diff(cubic, N, 2) != 0,
    )

    w1 = sp.symbols("w1", positive=True)
    floor_expression = w * N / w1
    checks.check(
        "the declared N=1 and w=w1 floor identity is exact",
        sp.simplify(floor_expression.subs({N: 1, w: w1}) - 1) == 0,
    )
    alternative = floor_expression + (N - 1) * (w - w1)
    checks.check(
        "the single floor point does not uniquely select the enhancement expression",
        sp.simplify(alternative.subs({N: 1, w: w1}) - 1) == 0
        and sp.simplify(alternative - floor_expression) != 0,
    )

    prior = {
        "GB1": Path("campaigns/P122-gb1-channel-branching-audit/adjudication.yaml"),
        "GB2": Path("campaigns/P123-gb2-subdivision-kinematics-audit/adjudication.yaml"),
        "GB3": Path("campaigns/P124-gb3-collective-asymmetry-audit/adjudication.yaml"),
        "GB4": Path("campaigns/P125-gb4-weighted-branching-audit/adjudication.yaml"),
        "GB5": Path("campaigns/P126-gb5-spectral-peak-audit/adjudication.yaml"),
    }
    prior_records = {unit: yaml.safe_load(path.read_text()) for unit, path in prior.items()}
    checks.check(
        "all five scanned dependencies have individual terminal qualifications",
        all(record["source_disposition"][unit] == "qualified" for unit, record in prior_records.items()),
    )
    checks.check(
        "only GB1 promoted a claim and that claim is exact allocation algebra",
        [item["id"] for item in prior_records["GB1"]["claims"]] == ["C-BRN-001"]
        and all(prior_records[unit]["claims"] == [] for unit in ("GB2", "GB3", "GB4", "GB5")),
    )
    p120 = yaml.safe_load(Path("campaigns/P120-cm6-honesty-firewall-audit/adjudication.yaml").read_text())
    checks.check(
        "CM6 supplies a qualified method ceiling but no scientific claim",
        p120["source_disposition"]["CM6"] == "qualified" and p120["claims"] == [],
    )
    checks.check(
        "the only direct consumer remains hash pinned to durable 59-check replay evidence",
        hashlib.sha256(WN7.read_bytes()).hexdigest() == WN7_HASH
        and "ALL {len(PASS)} CHECKS PASS" in WN7.read_text(),
    )
    checks.check(
        "the strongest surviving result is a pinned finite theorem with explicit ceilings",
        all(literal_scan(text, BARRIER) == [] for text in scanned)
        and literal_scan('name="U_"+"e"', BARRIER) == []
        and clamp_scan("value = np.clip(raw, 0, limit)") == []
        and source_count_guard(band_lookup),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
