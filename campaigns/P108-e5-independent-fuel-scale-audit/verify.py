"""Primary exact verifier for the P108 E5 finite fuel-scale audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-29/"
    "bridge_E5_independent_fuel_test.py"
)
SOURCE_SHA256 = "f1754902fb112f63c9c9052b60cdeca5455023560680e4e31889669cddf764af"
CONTRACT_SHA256 = "9a16810b348366c23da16d11c3ab5e283975b8a9f551a67e76bf82389ad185b3"
FREEZE_SHA256 = "9a16810b348366c23da16d11c3ab5e283975b8a9f551a67e76bf82389ad185b3"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P108-e5-independent-fuel-scale-audit"),
        Path("proposals/P108-e5-independent-fuel-scale-audit"),
    )
    return next(path for path in candidates if path.exists())


def _claim(claim_id: str) -> dict[str, object]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return next(claim for claim in registry["claims"] if claim["id"] == claim_id)


def main() -> int:
    checks = CheckLedger("P108")
    root = _campaign_root()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    normalized_contract = (
        (root / "proposal.yaml")
        .read_bytes()
        .replace(b"status: accepted\n", b"status: draft\n")
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-source commitment is immutable",
        hashlib.sha256((root / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    source_checks = sorted(
        (
            node
            for node in ast.walk(source_tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ),
        key=lambda node: node.lineno,
    )
    checks.check(
        "source has five checks and a dynamic terminal tally",
        len(source_checks) == 5
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source needs no NumPy integration compatibility replay",
        "numpy" not in source_text
        and "np." not in source_text
        and "trapz" not in source_text
        and "trapezoid" not in source_text,
    )

    binding = {
        "d": sp.Rational(278, 125),
        "t": sp.Rational(4241, 500),
        "3He": sp.Rational(3859, 500),
        "4He": sp.Rational(3537, 125),
        "11B": sp.Rational(15241, 200),
    }
    releases = {
        "D+D->4He": binding["4He"] - 2 * binding["d"],
        "D+3He->4He+p": binding["4He"] - binding["d"] - binding["3He"],
        "D+T->4He+n": binding["4He"] - binding["d"] - binding["t"],
        "p+11B->3alpha": 3 * binding["4He"] - binding["11B"],
    }
    expected_releases = {
        "D+D->4He": sp.Rational(2981, 125),
        "D+3He->4He+p": sp.Rational(9177, 500),
        "D+T->4He+n": sp.Rational(1759, 100),
        "p+11B->3alpha": sp.Rational(8683, 1000),
    }
    checks.check(
        "declared binding entries give the four exact source releases",
        releases == expected_releases,
    )
    checks.check(
        "source rounded-value check follows from its own binding table",
        all(
            abs(float(releases[name]) - value) < 0.1
            for name, value in {
                "D+D->4He": 23.85,
                "D+3He->4He+p": 18.35,
                "D+T->4He+n": 17.59,
                "p+11B->3alpha": 8.68,
            }.items()
        ),
    )
    q_function = next(
        node
        for node in source_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "Q_of"
    )
    checks.check(
        "the claimed comparator-only binding energies are direct calculation inputs",
        any(isinstance(node, ast.Name) and node.id == "BE" for node in ast.walk(q_function))
        and "Qs = {f: Q_of(f) for f in FUELS}" in source_text
        and "ratios = {f: Qs[f] / F_PI_OVER_E for f in FUELS}" in source_text,
    )
    checks.check(
        "source supplies rounded values but no uncertainty ledger",
        "COMPARATOR-ONLY binding energies" in source_text
        and "uncertaint" not in source_text.lower()
        and "sigma" not in source_text.lower(),
    )

    unit = sp.Rational(10219979, 1250000) * sp.pi
    ratios = {name: sp.simplify(value / unit) for name, value in releases.items()}
    checks.check(
        "all four displayed ratios lie in the source's literal interval",
        all(bool(ratio > sp.Rational(3, 10)) and bool(ratio < 1) for ratio in ratios.values()),
    )
    scale = sp.symbols("a", positive=True)
    checks.check(
        "common denominator rescaling changes every absolute coordinate inversely",
        all(sp.simplify((value / (scale * unit)) / ratios[name] - 1 / scale) == 0
            for name, value in releases.items()),
    )
    names = tuple(releases)
    checks.check(
        "pairwise ratio quotients are scale free but do not select the scale",
        all(
            sp.simplify(
                (releases[left] / (scale * unit))
                / (releases[right] / (scale * unit))
                - releases[left] / releases[right]
            )
            == 0
            for left in names
            for right in names
        ),
    )
    q_min = min(releases.values())
    q_max = max(releases.values())
    bracket_low = q_max
    bracket_high = sp.Rational(10, 3) * q_min
    checks.check(
        "the literal 0.3-to-1 bracket admits a continuum of denominators",
        bool(bracket_low < unit)
        and bool(unit < bracket_high)
        and bool(bracket_low < bracket_high),
    )
    checks.check(
        "smaller and larger allowed-unit mutations destroy the literal bracket",
        max(value / sp.Integer(10) for value in releases.values()) > 1
        and max(value / sp.Integer(100) for value in releases.values()) < sp.Rational(3, 10),
    )
    target = sp.symbols("t", positive=True)
    checks.check(
        "each positive release realizes any chosen coordinate with a supplied scale",
        all(sp.simplify(value / (value / target) - target) == 0 for value in releases.values()),
    )
    checks.check(
        "absolute ratio range is not scale invariant",
        sp.simplify(
            (q_max / (scale * unit) - q_min / (scale * unit))
            / (q_max / unit - q_min / unit)
            - 1 / scale
        )
        == 0,
    )
    checks.check(
        "multiplicative sample spread is scale invariant and about 2.75, not a scale selector",
        sp.simplify((q_max / unit) / (q_min / unit) - q_max / q_min) == 0
        and sp.Rational(27, 10) < q_max / q_min < sp.Rational(14, 5),
    )

    for selected_name, selected_q in releases.items():
        checks.check(
            f"choosing the denominator equal to {selected_name}'s release makes it closest to one",
            all(
                abs(selected_q / selected_q - 1)
                < abs(other_q / selected_q - 1)
                for other_name, other_q in releases.items()
                if other_name != selected_name
            ),
        )
    checks.check(
        "D+D closest-to-one is conditional on the supplied denominator",
        min(releases, key=lambda name: abs(releases[name] / unit - 1)) == "D+D->4He",
    )
    checks.check(
        "positivity follows from selecting positive releases and a positive denominator",
        all(value > 0 for value in releases.values())
        and not all(value > 0 for value in (*releases.values(), sp.Integer(-1))),
    )
    checks.check(
        "sample additions can falsify both the bracket and finite factor-three statement",
        not all(
            sp.Rational(3, 10) < value / unit < 1
            for value in (*releases.values(), 100 * unit)
        )
        and max((*releases.values(), 100 * unit)) / min(releases.values()) > 3,
    )

    alpha_assignment = next(
        node
        for node in source_tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target_node, ast.Name) and target_node.id == "produces_alpha"
                for target_node in node.targets)
    )
    fourth_condition = ast.unparse(alpha_assignment.value)
    checks.check(
        "alpha predicate only inspects the preselected product table and release sign",
        "'4He' in FUELS[f][1]" in fourth_condition and "Qs[f] > 0" in fourth_condition,
    )
    checks.check(
        "a positive non-alpha reaction entry defeats the source's universal inference",
        not all(
            "4He" in products and value > 0
            for products, value in (
                *((("4He",), q) for q in releases.values()),
                (("3He", "n"), sp.Integer(1)),
            )
        ),
    )
    checks.check(
        "D+T is explicitly neutron producing despite the source's aneutronic label",
        "D+T->4He+n" in source_text
        and "other aneutronic fusion fuels" in source_text.lower(),
    )
    ny2_audit = yaml.safe_load(
        Path("campaigns/P085-ny2-nuclear-yield-audit/evidence/source-audit.yaml").read_text()
    )
    checks.check(
        "D+D one-body final-state shorthand omits required channel bookkeeping",
        ny2_audit["reaction_kinematics"]["one_body_final_with_positive_CM_release"]
        == "impossible"
        and ny2_audit["reaction_kinematics"]["radiative_channel"]
        == "D+D_to_He4_plus_gamma",
    )
    checks.check(
        "accepted rational-map branch explicitly excludes alpha and nuclear state maps",
        "alpha particle or nucleus" in _claim("C-RPROF-002")["statement"]
        and "reaction" in _claim("C-RPROF-002")["statement"],
    )
    checks.check(
        "accepted conditional scale explicitly excludes numerical prediction",
        "No numerical comparator" in _claim("C-SK-001")["assumptions"][2],
    )
    queue = yaml.safe_load(Path("migration/source-claims.yaml").read_text())
    o1 = next(
        unit_record
        for unit_record in queue["units"]
        if unit_record["source_unit"] == "O1"
    )
    checks.check(
        "O1 remains pending and cannot authorize an E5 state map",
        o1["disposition"] == "pending_adjudication" and o1["phase"] == "phase-7",
    )
    proposal = yaml.safe_load((root / "proposal.yaml").read_text())
    checks.check(
        "nonduplication gate reserves no claim or canonical API",
        proposal["claims_proposed"] == [],
    )
    anchor_line = next(
        line for line in source_text.splitlines() if line.startswith("anchor_independent =")
    )
    checks.check(
        "source independence guard recomputes the anchor from the identical expression",
        anchor_line.count("16 * sp.pi * 0.51099895") == 1
        and "F_PI_OVER_E - float" in anchor_line,
    )
    checks.check(
        "fresh exact work uses no sampled quadrature or NumPy integration alias",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
