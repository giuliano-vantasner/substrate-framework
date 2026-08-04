"""Independent GB6 review without importing the P127 primary verifier."""

from __future__ import annotations

import ast
import hashlib
import math
from pathlib import Path
import re
import unicodedata

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate/merged-framework/bridges/phase-32")
CAMPAIGN = Path("campaigns/P127-gb6-honesty-firewall-audit")
GB6 = ROOT / "bridge_GB6_honesty_firewall_guard.py"
GB6_SHA = "edcfc0fafad48dbfc88ebf97613d45c1b6cf7e85b95548ae4006b373a2cfc49a"
FREEZE_SHA = "28ca23f3f2184f5dc5e68859c4006a85b0f7f765689f4c81c864775ecd5f35c4"
WN7 = Path("/home/dan/substrate/merged-framework/bridges/phase-37/bridge_WN7_honesty_firewall_guard.py")
WN7_SHA = "88844689bf682ca5ff524378f4e5e46a25bcab54b1a3a6e59afe69b990694d50"
NAMES = (
    "bridge_GB1_channel_definitions.py",
    "bridge_GB2_subdivision_kinematics.py",
    "bridge_GB3_dicke_asymmetry.py",
    "bridge_GB4_branching_ratio.py",
    "bridge_GB5_spectral_peak.py",
)
WORDS = ("u_e", "gamow", "screening_enhancement", "gamow_energy_kev")
NUMBERS = ("0.0362", "90.35", "0.999757")
EMPIRICAL = ("excess_heat_watts", "cop_measured", "transmutation_yield")


def fresh_scan(text: str, words: tuple[str, ...]) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), 1):
        if re.search(r"\[IMPORT\]", line) is not None:
            continue
        folded = line.casefold()
        found.extend((number, word) for word in words if folded.find(word) >= 0)
    return found


def fresh_clamps(text: str) -> list[int]:
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        code = line.partition("#")[0]
        if ("min(" in code and ("cap" in code.lower() or "ceil" in code.lower())) or (
            "CEILING" in code
        ):
            hits.append(number)
    return hits


def module_imports(text: str) -> set[str]:
    tree = ast.parse(text)
    names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    names.update(node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom))
    return names


def condition_mentions(text: str, names: set[str]) -> bool:
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            and len(node.args) >= 2
        ):
            used = {child.id for child in ast.walk(node.args[1]) if isinstance(child, ast.Name)}
            if used & names:
                return True
    return False


def sampled_derivative(expr: sp.Expr, population: sp.Symbol, weight: sp.Symbol, ratio: sp.Symbol) -> bool:
    value = sp.diff(expr, population).subs(
        {population: 3, weight: 2, ratio: sp.Rational(1, 4)}
    )
    return bool(value < 0)


BAND = (1.0e-3, 3.0e-3, 1.0e-2, 3.0e-2, 1.0e-1, 3.0e-1, 1.0)
TOTAL = 24.0e6


def sampled_count(candidate) -> bool:
    values = [candidate(TOTAL, point) for point in BAND]
    return bool(
        min(values) != max(values)
        and all(values[index] >= values[index + 1] for index in range(6))
        and all(
            0.0 <= TOTAL - values[index] * BAND[index] < BAND[index]
            for index in range(7)
        )
    )


def main() -> int:
    checks = CheckLedger("GB6-INDEPENDENT-FIREWALL-REVIEW")
    gb6_bytes = GB6.read_bytes()
    gb6_text = gb6_bytes.decode("utf-8")
    sources = {name: (ROOT / name).read_text() for name in NAMES}

    checks.check(
        "fresh source read is hash pinned",
        hashlib.sha256(gb6_bytes).hexdigest() == GB6_SHA,
    )
    checks.check(
        "fresh preregistration read is hash pinned",
        hashlib.sha256((CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA,
    )
    checks.check(
        "fresh consumer read is hash pinned",
        hashlib.sha256(WN7.read_bytes()).hexdigest() == WN7_SHA,
    )
    tree = ast.parse(gb6_text)
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check("fresh AST count finds sixteen static checks", len(calls) == 16)
    checks.check(
        "fresh loop expansion gives twenty-nine runtime checks",
        len(NAMES) * 3 + 2 + 7 + 5 == 29,
    )
    checks.check(
        "fresh matchers reproduce all four empty finite scans",
        all(fresh_scan(text, WORDS) == [] for text in sources.values())
        and all(fresh_scan(text, NUMBERS) == [] for text in sources.values())
        and all(fresh_scan(text, EMPIRICAL) == [] for text in sources.values())
        and fresh_clamps(sources[NAMES[3]]) == []
        and fresh_clamps(sources[NAMES[4]]) == [],
    )

    all_imports = set().union(*(module_imports(text) for text in sources.values()))
    checks.check(
        "fresh import graph finds standard and symbolic modules rather than zero imports",
        all_imports == {"sys", "math", "sympy"},
    )
    checks.check(
        "the numeric-string detector ignores actual Python imports",
        fresh_scan("from nuclear_data import matrix_element", NUMBERS) == [],
    )
    checks.check(
        "GB6 imports no GB module and evaluates local duplicate expressions",
        module_imports(gb6_text) == {"os", "sys", "sympy", "math"}
        and "import bridge_GB" not in gb6_text
        and "from bridge_GB" not in gb6_text,
    )
    checks.check(
        "GB6 source reads are unhashed and use default decoding",
        "sha256" not in gb6_text.casefold()
        and "encoding=" not in gb6_text
        and 'open(os.path.join(HERE, fn))' in gb6_text,
    )
    checks.check(
        "the scanner's own file is outside the five-file scope and would self-flag",
        GB6.name not in NAMES and fresh_scan(gb6_text, WORDS) != [],
    )

    checks.check(
        "the exemption is case-sensitive line-wide and accepts tag smuggling",
        fresh_scan("value=U_e # [IMPORT]", WORDS) == []
        and fresh_scan("value=U_e # [import]", WORDS) == [(1, "u_e")]
        and fresh_scan('tag="[IMPORT]"; value=U_e', WORDS) == [],
    )
    checks.check(
        "concatenation getattr and equivalent algebra evade the matcher",
        fresh_scan('n="U_"+"e"; value=getattr(obj,n)', WORDS) == []
        and fresh_scan("value=exp(-sqrt(scale/(energy+shift)))", WORDS) == [],
    )
    unicode_name = "U\uff3fe"
    checks.check(
        "Unicode normalization exposes a name the source matcher misses",
        fresh_scan(f"value={unicode_name}", WORDS) == []
        and unicodedata.normalize("NFKC", unicode_name) == "U_e",
    )
    checks.check(
        "prose and benign identifier collisions refute semantic specificity",
        fresh_scan("# U_e is absent", WORDS) == [(1, "u_e")]
        and fresh_scan('"No Gamow machinery"', WORDS) == [(1, "gamow")]
        and fresh_scan("tau_evolution=1", WORDS) == [(1, "u_e")],
    )
    checks.check(
        "the longer Gamow token is redundant with the shorter substring",
        fresh_scan("x=gamow_energy_keV(pair)", WORDS)
        == [(1, "gamow"), (1, "gamow_energy_kev")],
    )

    saturation = (
        "y=min (x, limit)",
        "y=np.clip(x,0,limit)",
        "y=x if x<limit else limit",
        "y=x/(1+abs(x))",
        "y=tanh(x)",
        "y=bounded_helper(x)",
    )
    checks.check(
        "fresh clamp matcher misses six ordinary bounded constructions",
        all(fresh_clamps(form) == [] for form in saturation),
    )
    checks.check(
        "absence of clamp spellings does not imply unbounded output",
        100 / (1 + abs(100)) < 1 and math.tanh(100) <= 1,
    )
    checks.check(
        "capacity prose collides and a hash in string data hides a literal clamp",
        fresh_clamps("remaining_capacity=min(raw, available)") == [1]
        and fresh_clamps('label="#"; y=min(x, cap)') == [],
    )

    checks.check(
        "numeric and imported pass comparators evade the empirical names",
        fresh_scan('check("fit", abs(model-30.0)<0.01)', EMPIRICAL) == []
        and fresh_scan('target=config["observed"]; check("fit", model==target)', EMPIRICAL)
        == [],
    )
    checks.check(
        "GB5's catalog tuples themselves occur in check conditions",
        condition_mentions(sources[NAMES[4]], {"KLIMOV_BAND_keV"})
        and condition_mentions(sources[NAMES[4]], {"NAMED_OPTICAL_LINES_eV"}),
    )
    checks.check(
        "GB2 and GB3 named magnitudes feed condition expressions",
        condition_mentions(sources[NAMES[1]], {"Omega_eV", "per_q"})
        and condition_mentions(
            sources[NAMES[2]], {"lambda_gamma_pm", "d_nuclear_pm", "phonon_coherence_pm"}
        ),
    )
    checks.check(
        "an empirical-name comment is a false positive and a tagged use is hidden",
        fresh_scan("# excess_heat_watts is absent", EMPIRICAL)
        == [(1, "excess_heat_watts")]
        and fresh_scan("target=excess_heat_watts # [IMPORT]", EMPIRICAL) == [],
    )

    N, w, rho = sp.symbols("N w rho", positive=True)
    baseline = rho / (w * N + rho)
    symmetric = rho / (w + rho)
    checks.check(
        "fresh algebra reproduces the exact symmetric fixture rejection",
        sampled_derivative(baseline, N, w, rho)
        and not sampled_derivative(symmetric, N, w, rho),
    )
    local_mutant = baseline + (N - 3) ** 2
    checks.check(
        "fresh counterexample passes the sampled derivative but rises elsewhere",
        sampled_derivative(local_mutant, N, w, rho)
        and sp.diff(local_mutant, N).subs({N: 4, w: 2, rho: sp.Rational(1, 4)}) > 0,
    )

    checks.check(
        "fresh kinematic route accepts floor and rejects the selected constant fake",
        sampled_count(lambda total, omega: math.floor(total / omega))
        and not sampled_count(lambda _total, _omega: int(1e8)),
    )

    def table_only(total: float, omega: float) -> int:
        return math.floor(total / omega) if omega in BAND else 1

    checks.check(
        "fresh off-band counterexample passes all seven source samples",
        sampled_count(table_only)
        and not (0 <= TOTAL - table_only(TOTAL, 0.2) * 0.2 < 0.2),
    )

    hbar = sp.symbols("hbar", positive=True)
    exact_n2 = (hbar * N) ** 2
    n3 = hbar**2 * N**3
    checks.check(
        "the exact N-squared fake differs from linear at N=4",
        sp.simplify((exact_n2 - hbar**2 * N).subs(N, 4)) != 0
        and sp.simplify(exact_n2 - hbar**2 * N**2) == 0,
    )
    checks.check(
        "a different superlinear law lies outside that exact identity test",
        sp.simplify(n3 - hbar**2 * N**2) != 0 and sp.diff(n3, N, 2) != 0,
    )

    w1 = sp.symbols("w1", positive=True)
    source_floor = w * N / w1
    other_floor = source_floor + (N - 1) ** 2
    checks.check(
        "the exact floor is true but does not identify a unique global expression",
        sp.simplify(source_floor.subs({N: 1, w: w1}) - 1) == 0
        and sp.simplify(other_floor.subs({N: 1, w: w1}) - 1) == 0
        and sp.simplify(other_floor - source_floor) != 0,
    )

    checks.check(
        "the strongest independent verdict is finite lexical evidence only",
        all(fresh_scan(text, WORDS) == [] for text in sources.values())
        and fresh_scan('n="U_"+"e"', WORDS) == []
        and fresh_clamps("y=np.clip(x,0,limit)") == []
        and sampled_count(table_only),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
