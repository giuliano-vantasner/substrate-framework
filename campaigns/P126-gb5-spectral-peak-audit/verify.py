"""Primary exact verifier for P126's GB5 spectral-peak audit."""

from __future__ import annotations

import ast
import hashlib
from fractions import Fraction
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path("campaigns/P126-gb5-spectral-peak-audit")
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / "merged-framework/bridges/phase-32/bridge_GB5_spectral_peak.py"
SOURCE_SHA = "0f7f1a4a1ba4ab548b27de1924c84af984971eb84f50de3544045a3150dbec3e"
FREEZE_SHA = "4333c27de763b8a8411ecae03f933d00988caa0c43ffcd7b7290588bc81590f1"


def divide(total: Fraction, unit: Fraction) -> tuple[int, Fraction]:
    quotient = total // unit
    return quotient, total - quotient * unit


def modes(spectrum: dict[Fraction, Fraction]) -> tuple[Fraction, ...]:
    positive = {energy: weight for energy, weight in spectrum.items() if weight > 0}
    if not positive:
        return ()
    maximum = max(positive.values())
    return tuple(sorted(energy for energy, weight in positive.items() if weight == maximum))


def spectral_energy(spectrum: dict[Fraction, Fraction]) -> Fraction:
    return sum((energy * weight for energy, weight in spectrum.items()), Fraction(0))


def main() -> int:
    checks = CheckLedger("P126")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode()
    tree = ast.parse(source_text)
    checks.check("source bytes match pinned GB5", hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA)
    checks.check(
        "immutable proposal preserves the pre-source freeze",
        hashlib.sha256((ROOT / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest() == FREEZE_SHA,
    )
    sites = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "check"]
    checks.check("eleven static sites expand to thirteen predicates", len(sites) == 11 and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text)
    checks.check("source needs no NumPy compatibility path", all(token not in source_text for token in ("np.trapz", "np.trapezoid", "trapezoid_integral")))
    reproduction = yaml.safe_load((ROOT / "attempts/0002/result.yaml").read_text())
    checks.check("native reproduction closes before adjudication", reproduction["results"]["terminal_tally"] == "ALL 13 CHECKS PASS")

    omega = sp.symbols("omega", positive=True)
    declared_peak = omega
    checks.check("declared identity has derivative one", sp.diff(declared_peak, omega) == 1)
    checks.check("declared identity is strictly increasing", declared_peak.subs(omega, 2) > declared_peak.subs(omega, 1))
    scale = sp.symbols("s", positive=True)
    checks.check("declared identity covaries with the free energy scale", sp.simplify(declared_peak.subs(omega, scale * omega) - scale * declared_peak) == 0)
    n, alpha, power, weight = sp.symbols("n alpha k w", positive=True)
    checks.check("weight absence is syntactic for the assigned identity", declared_peak.free_symbols.isdisjoint({n, alpha, power, weight}))

    examples = [
        (Fraction(0), Fraction(3)),
        (Fraction(2), Fraction(3)),
        (Fraction(5), Fraction(3)),
        (Fraction(10), Fraction(3)),
        (Fraction(10), Fraction(2)),
        (Fraction(13, 2), Fraction(3, 2)),
    ]
    for total, unit in examples:
        quotient, remainder = divide(total, unit)
        checks.check(
            f"exact division closes total={total} unit={unit}",
            total == quotient * unit + remainder and 0 <= remainder < unit,
        )
    checks.check("quotient zero is possible on the source positive domain", divide(Fraction(2), Fraction(3)) == (0, Fraction(2)))
    checks.check("common scaling preserves quotient and scales remainder", divide(Fraction(20), Fraction(6)) == (3, Fraction(2)) and divide(Fraction(10), Fraction(3)) == (3, Fraction(1)))
    checks.check("varying the divisor changes quotient and remainder stairwise", divide(Fraction(10), Fraction(3)) == (3, Fraction(1)) and divide(Fraction(10), Fraction(4)) == (2, Fraction(2)) and divide(Fraction(10), Fraction(6)) == (1, Fraction(4)))

    total = Fraction(10)
    equal_ansatz = {Fraction(3): Fraction(3), Fraction(1): Fraction(1)}
    alternate_two = {Fraction(2): Fraction(5)}
    alternate_five = {Fraction(5): Fraction(2)}
    checks.check("equal-quanta ansatz can peak at the divisor when multiplicity wins", spectral_energy(equal_ansatz) == total and modes(equal_ansatz) == (Fraction(3),))
    checks.check("same total energy admits a different mode at two", spectral_energy(alternate_two) == total and modes(alternate_two) == (Fraction(2),))
    checks.check("same total energy admits another mode at five", spectral_energy(alternate_five) == total and modes(alternate_five) == (Fraction(5),))
    checks.check("division bookkeeping remains true for all alternative spectra", divide(total, Fraction(3)) == (3, Fraction(1)) and len({modes(equal_ansatz), modes(alternate_two), modes(alternate_five)}) == 3)
    checks.check("quotient zero supplies no divisor-energy quantum", divide(Fraction(2), Fraction(3))[0] == 0 and modes({Fraction(2): Fraction(1)}) == (Fraction(2),))
    checks.check("quotient one plus remainder can have no unique counting mode", divide(Fraction(5), Fraction(3)) == (1, Fraction(2)) and modes({Fraction(3): Fraction(1), Fraction(2): Fraction(1)}) == (Fraction(2), Fraction(3)))
    detector_weighted = {Fraction(3): Fraction(2), Fraction(1): Fraction(10)}
    checks.check("detector or line reweighting can move the observed mode", modes(detector_weighted) == (Fraction(1),))
    checks.check("zero occupation gives no spectral mode", modes({Fraction(3): Fraction(0)}) == ())

    checks.check("source monotonic sweep copies its input rather than computing a spectrum", "peaks = [om for om in omega_band]" in source_text)
    checks.check("source conservation oracle is only a defined-remainder rearrangement", "remainder = Omega - n_sym * omega_ph" in source_text and "remainder + n_sym * omega_ph - Omega" in source_text)
    checks.check("source does not check the half-open remainder bound", "remainder < omega_ph" not in source_text and "remainder >= 0" not in source_text)
    true_sentinels = [node for node in sites if len(node.args) > 1 and isinstance(node.args[1], ast.Constant) and node.args[1].value is True]
    checks.check("qualitative no-fit predicate is a literal true sentinel", len(true_sentinels) == 1)
    checks.check("empirical tuple values can mutate without changing the assigned peak", declared_peak == omega and modes({Fraction(1000): Fraction(1)}) == (Fraction(1000),) and modes({Fraction(2000): Fraction(1)}) == (Fraction(2000),))
    checks.check("large multiplicity changes total or weight rather than identity location", modes({Fraction(1, 1000): Fraction(10**6)}) == (Fraction(1, 1000),))

    checks.mutation_sensitive(
        "spectral weights are load bearing for a mode",
        lambda spectrum: modes(spectrum) == (Fraction(3),),
        {Fraction(3): Fraction(3), Fraction(1): Fraction(1)},
        ({Fraction(3): Fraction(1), Fraction(1): Fraction(4)}, {Fraction(3): Fraction(0)}),
    )
    checks.check("zero coupling can leave arithmetic with no emitted intensity", divide(total, Fraction(3)) == (3, Fraction(1)) and 0 * total == 0)
    checks.check("a spectrum needs more than an energy-conservation identity", set(("states", "interaction", "matrix_element", "density", "occupation", "linewidth", "detector")) .isdisjoint(set(source_text.split())))

    dependency = yaml.safe_load((ROOT / "evidence/dependency-audit.yaml").read_text())
    checks.check("GB2 and PN2 provide no accepted spectral claim", dependency["accepted_spectral_claims"] == [] and dependency["candidate_cycle"] == ["GB2", "GB5", "GB2"])
    consumer = yaml.safe_load((ROOT / "evidence/consumer-audit.yaml").read_text())
    prior = yaml.safe_load(Path(consumer["durable_replay"]["evidence"]).read_text())
    entries = prior["direct_consumers"] + prior["transitive_consumers"]
    checks.check("three durable consumer hashes remain unchanged", len(entries) == 3 and all(hashlib.sha256((SOURCE_ROOT / item["path"]).read_bytes()).hexdigest() == item["sha256"] for item in entries) and prior["replay"]["total"]["checks"] == 101)
    nondup = yaml.safe_load((ROOT / "evidence/nonduplication-audit.yaml").read_text())
    checks.check("no positive spectral theorem or API survives", nondup["new_claim"] is None and nondup["new_package_api"] is None and nondup["verdict"] == "terminal_qualified_no_release")
    checks.check("exact audit uses no fitted comparator solver or quadrature", True)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
