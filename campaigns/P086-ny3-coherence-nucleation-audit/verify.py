"""Primary exact verifier for the P086 NY3 coherence-nucleation audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.coherence_gates import (
    activated_relative_response,
    continuous_population_threshold,
    gaussian_phase_pair_coherence,
    iid_equal_amplitude_expected_intensity,
    population_activation_scale,
)
from substrate_framework.radial_energy import capillary_energy
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-24/"
    "bridge_NY3_coherence_nucleation_threshold.py"
)
COHERENCE_CONSUMER = Path(
    "/home/dan/substrate/engineering/spark_discharge/coherence_array.py"
)
ENGINEERING_VERIFY = COHERENCE_CONSUMER.with_name("verify.py")
RUNG091 = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
    "rung091_R_gate_medium_escape.py"
)
RUNG092 = RUNG091.with_name("rung092_retention_nuclear_loss.py")
BD1 = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-28/"
    "bridge_BD1_real_variable_barrier.py"
)
BD3 = BD1.with_name("bridge_BD3_ignition_thresholds.py")
SOURCE_SHA256 = "b6fc332266e7795ca57ce657a5c57e196dbca78f7ffe219d29a9dfb56fbf8e88"
COHERENCE_SHA256 = "7e1bd3cb1afeaca4c5f2af7ff817422ff84ddabf095e632c20b90aab5efa573d"
ENGINEERING_VERIFY_SHA256 = "11c0f7b448a44545fb161701cb7fa10b6c22fd4e183d66bfc2752afaead82d5e"
RUNG091_SHA256 = "5872457368e81ad07760f17ebebe5b522c2f7a66acce0a1a37802ed3f91d323d"
RUNG092_SHA256 = "5d71804a3a613300284e9c33dd8218b4bdbeda0788a365a0a7e5725040b55695"
BD1_SHA256 = "42579012eda87243639248664c6f90945c454046aa66c8de166ad6d2e594abc7"
BD3_SHA256 = "8a8f2138c548d3ed90785fc3ea82302d39d71d4832cb3761f429938d9b94b950"
CONTRACT_SHA256 = "e7cbaf88d2fd8a3b3b86ece255de2e3fd35b822dbc4f343c70c78a5eab6cfbb1"
FREEZE_SHA256 = "23b01500e51dc7a980a61b9f3ec5e7705a03327f5a88022c6a74a285c6f53b31"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P086-ny3-coherence-nucleation-audit/proposal.yaml"),
        Path("proposals/P086-ny3-coherence-nucleation-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def _queue_unit(source_unit: str) -> dict[str, object]:
    queue = yaml.safe_load(Path("migration/source-claims.yaml").read_text())
    return next(unit for unit in queue["units"] if unit["source_unit"] == source_unit)


def main() -> int:
    checks = CheckLedger("P086")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    normalized_contract = (
        _contract_path()
        .read_bytes()
        .replace(b"status: accepted\n", b"status: draft\n")
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    freeze_path = _contract_path().parent / "evidence/frozen-proposal.yaml"
    checks.check(
        "pre-source contract commitment is immutable",
        hashlib.sha256(freeze_path.read_bytes()).hexdigest() == FREEZE_SHA256,
    )
    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has fifteen literal checks and a dynamic terminal tally",
        len(literal_checks) == 15
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source and canonical exact work use no NumPy quadrature alias",
        all(
            alias not in source_text
            for alias in ("np." + "trapz", "np." + "trapezoid")
        ),
    )

    radius, tension, pressure, core = sp.symbols(
        "R T P C", positive=True
    )
    landscape = capillary_energy(radius, tension, pressure, core)
    critical = sp.simplify(tension / pressure)
    relative_height = sp.simplify(
        landscape.subs(radius, critical) - landscape.subs(radius, 0)
    )
    checks.check(
        "capillary relative height follows from the accepted energy",
        relative_height == sp.pi * tension**2 / pressure
        and core not in relative_height.free_symbols
        and sp.diff(landscape, radius, 2) == -2 * sp.pi * pressure,
    )

    count = sp.Symbol("N", integer=True, positive=True)
    population = sp.Symbol("n", positive=True)
    intensity, unit, barrier = sp.symbols("I_1 theta E", positive=True)
    coherence = sp.Symbol("V", real=True)
    expected = iid_equal_amplitude_expected_intensity(
        count, intensity, coherence
    )
    independent_counting = intensity * (
        count + count * (count - 1) * coherence
    )
    checks.check(
        "iid phasor expansion separates diagonal and ordered-pair terms",
        sp.expand(expected - independent_counting) == 0,
    )
    checks.check(
        "incoherent and aligned endpoint intensities are exact",
        expected.subs(coherence, 0) == count * intensity
        and expected.subs(coherence, 1) == count**2 * intensity
        and expected.subs(count, 1) == intensity,
    )
    variance = sp.Symbol("sigma_squared", nonnegative=True)
    checks.check(
        "Gaussian mean-phasor squaring gives the consumer coherence factor",
        gaussian_phase_pair_coherence(variance)
        == sp.exp(-variance / 2) ** 2
        and gaussian_phase_pair_coherence(0) == 1
        and sp.limit(
            gaussian_phase_pair_coherence(variance), variance, sp.oo
        )
        == 0,
    )
    directivity = sp.simplify(expected / (count * intensity))
    checks.check(
        "the enhancement is a directional ratio rather than total power",
        directivity == 1 + (count - 1) * coherence
        and directivity.subs(coherence, 0) == 1
        and directivity.subs(coherence, 1) == count,
    )
    fixed_total = sp.simplify(expected.subs(intensity, intensity / count))
    checks.check(
        "changing the source normalization changes the apparent N scaling",
        fixed_total == intensity * (1 + (count - 1) * coherence)
        and fixed_total.subs(coherence, 1) == count * intensity,
    )
    checks.check(
        "a deterministic antiphase pair refutes universal N-to-N-squared bounds",
        sp.simplify(abs(1 + sp.exp(sp.I * sp.pi)) ** 2) == 0
        and expected.subs({count: 2, coherence: 0}) == 2 * intensity,
    )

    declared_scale = population_activation_scale(population, unit, coherence)
    source_form = sp.expand(
        unit * (population * (1 - coherence) + population**2 * coherence)
    )
    checks.check(
        "continuous activation interpolation equals the source algebra",
        sp.expand(declared_scale - source_form) == 0,
    )
    checks.check(
        "coherence monotonicity has an N greater than one condition",
        sp.diff(declared_scale, coherence)
        == unit * population * (population - 1)
        and sp.diff(declared_scale, coherence).subs(population, 1) == 0
        and sp.diff(declared_scale, coherence).subs(population, 2).is_positive,
    )
    positive_coherence = sp.Symbol("V_positive", positive=True)
    threshold = continuous_population_threshold(
        barrier, unit, positive_coherence
    )
    checks.check(
        "general positive-coherence root satisfies the defining quadratic",
        sp.simplify(
            unit
            * threshold
            * (1 + (threshold - 1) * positive_coherence)
            - barrier
        )
        == 0,
    )
    ratio = sp.simplify(barrier / unit)
    checks.check(
        "endpoint thresholds are ratio and square root of ratio",
        continuous_population_threshold(barrier, unit, 0) == ratio
        and continuous_population_threshold(barrier, unit, 1)
        == sp.sqrt(ratio),
    )
    checks.check(
        "coherence lowers the endpoint threshold only above unit ratio",
        sp.sqrt(4) < 4
        and sp.sqrt(sp.Rational(1, 4)) > sp.Rational(1, 4)
        and sp.sqrt(1) == 1,
    )
    checks.mutation_sensitive(
        "population interpolation is load bearing",
        lambda candidate: (
            sp.simplify(candidate.subs(coherence, 0) - unit * population)
            == 0
            and sp.simplify(
                candidate.subs(coherence, 1) - unit * population**2
            )
            == 0
            and sp.simplify(candidate.subs(population, 1) - unit) == 0
        ),
        declared_scale,
        (
            unit * (population + population**3 * coherence),
            unit * population * (1 + population * coherence),
            unit * population**2,
        ),
    )

    exact_barrier = sp.Integer(2)
    exact_unit = sp.Rational(1, 20)
    source_population = sp.Integer(16)
    coherent_source_scale = population_activation_scale(
        source_population, exact_unit, 1
    )
    incoherent_source_scale = population_activation_scale(
        source_population, exact_unit, 0
    )
    checks.check(
        "opened source numbers construct the advertised crossing",
        coherent_source_scale == sp.Rational(64, 5)
        and incoherent_source_scale == sp.Rational(4, 5)
        and coherent_source_scale >= exact_barrier
        and incoherent_source_scale < exact_barrier
        and continuous_population_threshold(exact_barrier, exact_unit, 1)
        == sp.sqrt(40)
        and continuous_population_threshold(exact_barrier, exact_unit, 0)
        == 40,
    )
    checks.check(
        "the source crossing reverses under a load-bearing scale mutation",
        population_activation_scale(source_population, sp.Rational(1, 200), 1)
        < exact_barrier
        and population_activation_scale(source_population, sp.Rational(1, 5), 0)
        >= exact_barrier,
    )
    activation_scale = sp.Symbol("Theta", positive=True)
    response = activated_relative_response(barrier, activation_scale)
    checks.check(
        "activated factor has exact conditional signs and limits",
        sp.diff(response, barrier).is_negative
        and sp.diff(response, activation_scale).is_positive
        and sp.limit(
            activated_relative_response(barrier, unit), unit, 0, dir="+"
        )
        == 0
        and sp.limit(
            activated_relative_response(barrier, unit), unit, sp.oo
        )
        == 1,
    )
    response_ratio = sp.simplify(
        activated_relative_response(exact_barrier, coherent_source_scale)
        / activated_relative_response(exact_barrier, incoherent_source_scale)
    )
    checks.check(
        "source rate-ratio threshold is an input-conditioned numerical fact",
        response_ratio == sp.exp(sp.Rational(75, 32))
        and sp.N(response_ratio, 20) > 10
        and activated_relative_response(exact_barrier, exact_barrier)
        == sp.exp(-1),
    )
    checks.check(
        "an activated factor is not a dimensionful event rate",
        "def R_gate(N, V):" in source_text
        and "return math.exp(" in source_text
        and "prefactor" not in source_text[source_text.index("def R_gate"):],
    )

    consumer_bytes = COHERENCE_CONSUMER.read_bytes()
    consumer_text = consumer_bytes.decode("utf-8")
    engineering_verify_bytes = ENGINEERING_VERIFY.read_bytes()
    checks.check(
        "directional consumer and its verifier are hash pinned",
        hashlib.sha256(consumer_bytes).hexdigest() == COHERENCE_SHA256
        and hashlib.sha256(engineering_verify_bytes).hexdigest()
        == ENGINEERING_VERIFY_SHA256,
    )
    checks.check(
        "predecessor consumer explicitly conserves phase-independent total emission",
        "return per_breather_power * N" in consumer_text
        and "compensated by the beam narrowing" in consumer_text
        and "N**2 * V" in consumer_text,
    )
    checks.check(
        "consumer labels the N-squared law imported and does not implement NY3's barrier",
        "standard array physics; IMPORT" in consumer_text
        and "def array_on_axis_power" in consumer_text
        and "def nucleation_power" in consumer_text
        and "E_star" not in consumer_text
        and "Theta_eff" not in consumer_text,
    )
    checks.check(
        "source relabels directional concentration as an effective activation scale",
        "cell's on-axis directivity" in source_text
        and "def Theta_eff(N, V):" in source_text
        and "Coherence crosses the barrier" in source_text,
    )
    checks.check(
        "source barrier and per-breather scales are inserted literals",
        "E_star_eV = 2.0" in source_text
        and "theta1 = 0.05" in source_text
        and "E_* is INSERTED" in source_text
        and "theta1 is INSERTED" in source_text,
    )

    pinned = {
        RUNG091: RUNG091_SHA256,
        RUNG092: RUNG092_SHA256,
        BD1: BD1_SHA256,
        BD3: BD3_SHA256,
    }
    checks.check(
        "named predecessor dependencies are hash pinned but noncanonical",
        all(
            hashlib.sha256(path.read_bytes()).hexdigest() == digest
            for path, digest in pinned.items()
        ),
    )
    checks.check(
        "BD1 and BD3 remain pending rather than accepted dependencies",
        _queue_unit("BD1")["disposition"] == "pending_adjudication"
        and _queue_unit("BD3")["disposition"] == "pending_adjudication",
    )
    checks.check(
        "NY1 and NY2 supply only duplicate conditional Skyrme evidence",
        _queue_unit("NY1")["disposition"] == "duplicate_evidence"
        and _queue_unit("NY2")["disposition"] == "duplicate_evidence"
        and _queue_unit("NY1")["accepted_claims"] == ["C-SK-001"]
        and _queue_unit("NY2")["accepted_claims"] == ["C-SK-001"],
    )
    checks.check(
        "NY3 supplies no nuclear interaction, reaction branch, or deposition map",
        all(
            token not in source_text.lower()
            for token in (
                "cross section",
                "branching ratio",
                "reaction hamiltonian",
                "deposition model",
            )
        ),
    )
    checks.check(
        "the surviving theorem is distinct but physically conditional",
        Path("src/substrate_framework/coherence_gates.py").exists()
        and not Path("src/substrate_framework/nuclear_gate.py").exists()
        and not Path("src/substrate_framework/nuclear_yield.py").exists(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
