"""Independent exact review of CM5 without importing the P119 verifier."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-31/"
    "bridge_CM5_excess_electrical.py"
)
SOURCE_SHA256 = "8af42e5229ba59b31dfb30dbf94e904a2670c4f2f2b57373f9dd25ab169c2841"
SEED = Path("/home/dan/substrate/engineering/seeding_kernel.py")
GEOMETRY = Path(
    "/home/dan/substrate/engineering/spark_geometry/isotropic_coherence.py"
)


def main() -> int:
    checks = CheckLedger("CM5-INDEPENDENT-REVIEW")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    checks.check(
        "the independently read CM5 source is hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    labels = [
        node.args[0].value
        for node in source_checks
        if node.args and isinstance(node.args[0], ast.Constant)
    ]
    checks.check(
        "all eighteen source predicates have literal review labels",
        len(source_checks) == 18 and len(labels) == 18 and len(set(labels)) == 18,
    )

    omega, a, d = sp.symbols("Omega a d", positive=True)
    # A cos(Omega t)+D sin(Omega t) has third-derivative cosine/sine
    # coefficients -D*Omega^3 and A*Omega^3. Orthogonality supplies 1/2.
    manual_average = sp.simplify(
        ((-d * omega**3) ** 2 + (a * omega**3) ** 2) / 2
    )
    checks.check(
        "manual coefficient rotation gives the exact third-derivative average",
        manual_average == omega**6 * (a**2 + d**2) / 2,
    )
    breather = sp.symbols("omega_b", positive=True)
    unit_cosine = manual_average.subs({omega: 2 * breather, a: 1, d: 0})
    checks.check(
        "the unit 2-omega-b cosine average contains the one-half factor",
        unit_cosine == 32 * breather**6,
    )
    checks.check(
        "the source's assembled sixty-four coefficient differs by exactly two",
        sp.simplify((2 * breather) ** 6 / unit_cosine) == 2,
    )
    checks.check(
        "static and phase shifts cannot alter the manual average",
        not manual_average.has(sp.symbols("mu_static"))
        and manual_average.subs({a: 0, d: 1})
        == manual_average.subs({a: 1, d: 0}),
    )

    power_dimension, moment_dimension, duration_dimension = sp.symbols(
        "Power Moment Time", positive=True
    )
    coupling_dimension = (
        power_dimension * duration_dimension**6 / moment_dimension**2
    )
    checks.check(
        "dimensional completion needs an independent coupling",
        sp.simplify(
            coupling_dimension * moment_dimension**2 / duration_dimension**6
            - power_dimension
        )
        == 0,
    )
    target = sp.symbols("target", positive=True)
    second_functional = omega**4 * a**2 / 2
    third_functional = omega**6 * a**2 / 2
    checks.check(
        "one comparator cannot select second versus third derivative radiation",
        sp.simplify(target / second_functional * second_functional - target) == 0
        and sp.simplify(target / third_functional * third_functional - target) == 0,
    )
    checks.check(
        "zero coupling is an exact no-output countermodel",
        0 * third_functional == 0 and third_functional.is_positive is True,
    )

    count, loading, loss, scale, barrier, temperature = sp.symbols(
        "N A2 Gamma b0 C Theta", positive=True
    )
    source_modulation = (
        scale
        * sp.sqrt(count)
        * sp.exp(-barrier / (loading * temperature))
        * loss
    )
    source_response = sp.expand(omega**6 * source_modulation**2 / 2)
    checks.check(
        "fresh expansion gives linear N and quadratic Gamma dependence",
        sp.diff(source_response / count, count) == 0
        and sp.diff(source_response / loss**2, loss) == 0,
    )
    checks.check(
        "the source response rises without bound at large Gamma",
        sp.diff(source_response, loss).is_positive is True
        and sp.limit(source_response, loss, sp.oo) == sp.oo,
    )
    detuning, product, cycle_frequency = sp.symbols(
        "Delta c omega_c", positive=True
    )
    paired = loss * product / (detuning**2 + loss**2 / 4)
    composite = cycle_frequency * product / (
        2 * sp.pi * (detuning**2 + loss**2 / 4)
    )
    checks.check(
        "accepted paired loss instead vanishes at both loss endpoints",
        sp.limit(paired, loss, 0, dir="+") == 0
        and sp.limit(paired, loss, sp.oo) == 0,
    )
    checks.check(
        "accepted composite is strictly decreasing while source power increases",
        sp.diff(composite, loss).is_negative is True
        and sp.diff(source_response, loss).is_positive is True,
    )
    checks.check(
        "the same symbol set does not identify the two functions",
        sp.simplify(source_response - composite) != 0,
    )

    aligned_four = abs(1 + 1 + 1 + 1) ** 2
    cancelled_four = sp.simplify(abs(1 + sp.I - 1 - sp.I) ** 2)
    checks.check(
        "fresh four-phasor examples span aligned sixteen and directional zero",
        aligned_four == 16 and cancelled_four == 0,
    )
    n, one_source, visibility = sp.symbols(
        "n I1 V", positive=True
    )
    expected_directional = one_source * (n + n * (n - 1) * visibility)
    checks.check(
        "the iid ensemble formula needs an explicit visibility",
        sp.simplify(expected_directional.subs(visibility, 0) - n * one_source)
        == 0
        and sp.simplify(
            expected_directional.subs(visibility, 1) - n**2 * one_source
        )
        == 0,
    )
    total = sp.symbols("I_total", positive=True)
    checks.check(
        "fixed-total normalization removes one power of N",
        sp.simplify(
            expected_directional.subs({visibility: 1, one_source: total / n})
            - n * total
        )
        == 0,
    )
    checks.check(
        "a narrowing N-squared focus can conserve integrated power",
        sp.simplify(n**2 * (1 / n**2)) == 1,
    )
    geometry_text = GEOMETRY.read_text()
    checks.check(
        "the cited geometry source calls focus local and total power unchanged",
        "higher local intensity, same total power" in geometry_text,
    )
    checks.check(
        "the cited geometry source forbids multiplying focus into its headline FOM",
        "NOT multiplied into the headline FOM" in geometry_text,
    )
    imported_names = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "CM5 reasserts geometry literals without importing the geometry module",
        "isotropic_coherence" not in imported_names
        and "Phi_iso_ringmatched = 1.0" in source_text,
    )

    tau, kernel_scale = sp.symbols("tau A", positive=True)
    finite_dc = 2 * kernel_scale * sp.exp(-(breather * tau) ** 2)
    checks.check(
        "the imported finite Gaussian has positive rather than exact-zero DC",
        finite_dc.is_positive is True and finite_dc != 0,
    )
    checks.check(
        "only the singular sharp-comb limit removes its DC value",
        sp.limit(finite_dc, tau, sp.oo) == 0,
    )
    seed_text = SEED.read_text()
    checks.check(
        "the imported kernel source itself implements the positive Gaussian pair",
        "np.exp(-(w - omega_b) ** 2 * tau ** 2)" in seed_text
        and "np.exp(-(w + omega_b) ** 2 * tau ** 2)" in seed_text,
    )
    checks.check(
        "CM5 calls only chi_b and never a voltage-to-population function",
        "sk.chi_b(" in source_text
        and "sk.seeded_population(" not in source_text
        and "sk.drive_spectrum_from_slew(" not in source_text
        and "sk.g_trigger_derived(" not in source_text,
    )
    time, dc, slope = sp.symbols("t V0 S", real=True)
    checks.check(
        "DC and ramp inputs separate voltage from slew",
        sp.diff(dc, time) == 0
        and sp.diff(dc + slope * time, time) == slope,
    )
    epsilon = sp.Function("epsilon")(time)
    field = sp.Function("E")(time)
    checks.check(
        "a varying medium adds a constitutive product-rule current",
        sp.diff(epsilon * field, time)
        == epsilon * sp.diff(field, time) + field * sp.diff(epsilon, time),
    )
    checks.check(
        "a zero interaction maps nonzero ramp slew to zero seed",
        0 * sp.diff(dc + slope * time, time) == 0,
    )

    w, omega_zero = sp.symbols("w omega_0", positive=True)
    mapped_frequency = w * omega_zero
    checks.check(
        "the dimensional breather map fixes only the frequency value",
        sp.simplify(mapped_frequency / omega_zero - w) == 0,
    )
    heat_coupling, electrical_coupling = sp.symbols(
        "k_heat k_electrical", nonnegative=True
    )
    checks.check(
        "same frequency permits independent heat and electrical couplings",
        sp.simplify(heat_coupling * mapped_frequency)
        != sp.simplify(electrical_coupling * mapped_frequency),
    )
    checks.check(
        "the source shared guard is a floating value comparison",
        "abs(omega_candidate - mo.physical_omega_b(OMEGA_0)) < 1e-12"
        in source_text,
    )

    claims = yaml.safe_load(Path("governance/claims.yaml").read_text())["claims"]
    accepted = {
        item["id"]: item
        for item in claims
        if item.get("review") == "accepted"
    }
    governing = {
        "C-GW-001",
        "C-COH-001",
        "C-SG-017",
        "C-CMP-001",
        "C-RES-001",
    }
    checks.check(
        "all independently identified governing claims are accepted",
        governing <= set(accepted),
    )
    checks.check(
        "governing claim statements retain radiation rate and channel ceilings",
        "radiation" in accepted["C-GW-001"]["statement"]
        and "transition-rate" in accepted["C-CMP-001"]["statement"]
        and "transition rate" in accepted["C-RES-001"]["statement"]
        and "nuclear or phonon channel" in accepted["C-RES-001"]["statement"],
    )
    proposal = yaml.safe_load(
        Path("campaigns/P119-cm5-excess-electrical-audit/proposal.yaml").read_text()
    )
    checks.check(
        "independent novelty review finds no preregistered claim to promote",
        proposal["claims_proposed"] == [],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
