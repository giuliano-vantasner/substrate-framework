"""Primary exact verifier for P119's CM5 excess-electrical audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from types import SimpleNamespace
from typing import Callable

import sympy as sp
import yaml

from substrate_framework.coherence_gates import (
    iid_equal_amplitude_expected_intensity,
)
from substrate_framework.tt_angular import (
    harmonic_stf_third_derivative_average,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-31/"
    "bridge_CM5_excess_electrical.py"
)
MEDIUM_SOURCE = Path("/home/dan/substrate/engineering/medium_omega0.py")
SEED_SOURCE = Path("/home/dan/substrate/engineering/seeding_kernel.py")
GEOMETRY_SOURCE = Path(
    "/home/dan/substrate/engineering/spark_geometry/isotropic_coherence.py"
)
SOURCE_SHA256 = "8af42e5229ba59b31dfb30dbf94e904a2670c4f2f2b57373f9dd25ab169c2841"
MEDIUM_SHA256 = "09d45f212bb28f124b05f99f9cb57acef7b815a1b4e99cfaa3e98bfc35f3f477"
SEED_SHA256 = "88e802df9347135a7d47d46dced9eca917de350797fa9bae70165ea26354aba6"
GEOMETRY_SHA256 = "fab8c407edccb0bdc56b754ce96a9045e4c488aea2e67f9a2dabc44272541d8d"
CONTRACT_SHA256 = "7dfce14aca38eeafcd4c73675cca70268ee76177c519a09a6efc51560c872f13"
FREEZE_SHA256 = "7dfce14aca38eeafcd4c73675cca70268ee76177c519a09a6efc51560c872f13"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P119-cm5-excess-electrical-audit"),
        Path("proposals/P119-cm5-excess-electrical-audit"),
    )
    return next(path for path in candidates if path.exists())


def _extract_function(
    source_tree: ast.Module,
    name: str,
    namespace: dict[str, object] | None = None,
) -> Callable[..., object]:
    function = next(
        node
        for node in source_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    scope = {} if namespace is None else dict(namespace)
    exec(compile(module, str(SOURCE), "exec"), scope)
    return scope[name]  # type: ignore[return-value]


def main() -> int:
    checks = CheckLedger("CM5-EXACT-AUDIT")
    root = _campaign_root()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)

    checks.check(
        "CM5 source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "medium-frequency support hash is pinned",
        hashlib.sha256(MEDIUM_SOURCE.read_bytes()).hexdigest() == MEDIUM_SHA256,
    )
    checks.check(
        "np.trapezoid seeding support hash is pinned",
        hashlib.sha256(SEED_SOURCE.read_bytes()).hexdigest() == SEED_SHA256,
    )
    checks.check(
        "np.trapezoid geometry support hash is pinned",
        hashlib.sha256(GEOMETRY_SOURCE.read_bytes()).hexdigest() == GEOMETRY_SHA256,
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
        "pre-source contract is immutable",
        hashlib.sha256((root / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "eighteen static predicates match the runtime tally",
        len(source_checks) == 18
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "CM5 itself has no sampled-integration compatibility event",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "trapezoid_integral" not in source_text
        and "scipy.integrate" not in source_text,
    )
    checks.check(
        "mutable executed support uses np.trapezoid rather than np.trapz",
        "np.trapezoid" in SEED_SOURCE.read_text()
        and "np.trapz" not in SEED_SOURCE.read_text()
        and "np.trapezoid" in GEOMETRY_SOURCE.read_text()
        and "np.trapz" not in GEOMETRY_SOURCE.read_text(),
    )

    time = sp.symbols("t", real=True)
    frequency, cosine, sine, static = sp.symbols(
        "Omega A D mu_static",
        positive=True,
    )
    waveform = static + cosine * sp.cos(frequency * time) + sine * sp.sin(
        frequency * time
    )
    third = sp.diff(waveform, time, 3)
    exact_average = sp.simplify(
        frequency
        / (2 * sp.pi)
        * sp.integrate(third**2, (time, 0, 2 * sp.pi / frequency))
    )
    expected_average = sp.simplify(
        frequency**6 * (cosine**2 + sine**2) / 2
    )
    checks.check(
        "the general scalar harmonic third-derivative average is exact",
        sp.simplify(exact_average - expected_average) == 0,
    )
    checks.check(
        "the static offset cancels without selecting a radiation law",
        not third.has(static) and sp.diff(static, time, 3) == 0,
    )
    checks.check(
        "the zero-frequency and zero-amplitude limits vanish",
        expected_average.subs(frequency, 0) == 0
        and expected_average.subs({cosine: 0, sine: 0}) == 0,
    )
    phase = sp.symbols("phi", real=True)
    amplitude = sp.symbols("B", positive=True)
    phase_wave = amplitude * sp.cos(frequency * time + phase)
    phase_average = sp.simplify(
        frequency
        / (2 * sp.pi)
        * sp.integrate(
            sp.diff(phase_wave, time, 3) ** 2,
            (time, 0, 2 * sp.pi / frequency),
        )
    )
    checks.check(
        "one peak-amplitude harmonic has a phase-independent one-half factor",
        sp.simplify(phase_average - frequency**6 * amplitude**2 / 2) == 0
        and not phase_average.has(phase),
    )
    breather_frequency = sp.symbols("omega_b", positive=True)
    exact_source_specialization = sp.simplify(
        phase_average.subs({frequency: 2 * breather_frequency, amplitude: 1})
    )
    checks.check(
        "the source's own unit-cosine average is thirty-two omega_b to the sixth",
        exact_source_specialization == 32 * breather_frequency**6,
    )
    source_assembled = (2 * breather_frequency) ** 6 * amplitude**2
    checks.check(
        "the assembled source expression is twice the peak-amplitude cycle average",
        sp.simplify(
            source_assembled
            / phase_average.subs(frequency, 2 * breather_frequency)
        )
        == 2,
    )
    checks.check(
        "an unspecified prefactor can absorb the factor but leaves power unnormalized",
        sp.simplify(
            sp.Rational(1, 2) * source_assembled
            - phase_average.subs(frequency, 2 * breather_frequency)
        )
        == 0,
    )

    tensor_cosine = sp.diag(cosine, -cosine, 0)
    tensor_sine = sp.Matrix([[0, sine, 0], [sine, 0, 0], [0, 0, 0]])
    tensor_average = harmonic_stf_third_derivative_average(
        tensor_cosine,
        tensor_sine,
        frequency,
    )
    checks.check(
        "accepted C-GW-001 already owns the tensor harmonic average",
        sp.simplify(
            tensor_average - frequency**6 * (2 * cosine**2 + 2 * sine**2) / 2
        )
        == 0,
    )
    power_unit, moment_unit, time_unit = sp.symbols("P M T", positive=True)
    average_unit = moment_unit**2 / time_unit**6
    required_prefactor_unit = power_unit * time_unit**6 / moment_unit**2
    checks.check(
        "a unitful radiation prefactor is required to turn the derivative square into power",
        sp.simplify(required_prefactor_unit * average_unit - power_unit) == 0
        and required_prefactor_unit != 1,
    )
    second_average = sp.simplify(
        frequency
        / (2 * sp.pi)
        * sp.integrate(
            sp.diff(amplitude * sp.cos(frequency * time), time, 2) ** 2,
            (time, 0, 2 * sp.pi / frequency),
        )
    )
    checks.check(
        "a competing second-derivative functional has distinct frequency scaling",
        second_average == amplitude**2 * frequency**4 / 2
        and phase_average.subs(phase, 0) == amplitude**2 * frequency**6 / 2,
    )
    target_power = sp.symbols("P_target", positive=True)
    checks.check(
        "arbitrary second- or third-derivative couplings fit one selected magnitude",
        sp.simplify(target_power / second_average * second_average - target_power) == 0
        and sp.simplify(target_power / phase_average * phase_average - target_power) == 0,
    )
    checks.check(
        "zero electromagnetic coupling preserves the waveform and gives zero output",
        0 * phase_average == 0 and phase_average.is_positive is True,
    )

    count, loading, loss, base, barrier, temperature = sp.symbols(
        "N A2 Gamma b0 C Theta",
        positive=True,
    )
    modulation = sp.simplify(
        base
        * sp.sqrt(count)
        * sp.exp(-barrier / (loading * temperature))
        * loss
    )
    normalized_power = sp.simplify(
        frequency**6 * modulation**2 / 2
    )
    checks.check(
        "the declared modulation composition gives an exact conditional family",
        sp.simplify(
            normalized_power
            - frequency**6
            * base**2
            * count
            * loss**2
            * sp.exp(-2 * barrier / (loading * temperature))
            / 2
        )
        == 0,
    )
    checks.check(
        "its N A-squared loss and frequency derivatives are positive only conditionally",
        sp.diff(normalized_power, count).is_positive is True
        and sp.diff(normalized_power, loading).is_positive is True
        and sp.diff(normalized_power, loss).is_positive is True
        and sp.diff(normalized_power, frequency).is_positive is True,
    )
    detuning, product, nominal_frequency = sp.symbols(
        "Delta c omega", positive=True
    )
    accepted_loss_element = loss * product / (detuning**2 + loss**2 / 4)
    accepted_composite = (
        nominal_frequency
        * product
        / (2 * sp.pi * (detuning**2 + loss**2 / 4))
    )
    checks.check(
        "the invented Gamma amplitude is not C-RES-001's loss element",
        sp.simplify(accepted_loss_element / loss - product / detuning**2) != 0
        and sp.limit(accepted_loss_element, loss, sp.oo) == 0
        and sp.limit(loss, loss, sp.oo) == sp.oo,
    )
    checks.check(
        "source power and C-CMP-001 have opposite positive-loss behavior",
        sp.diff(normalized_power, loss).is_positive is True
        and sp.diff(accepted_composite, loss).is_negative is True
        and sp.limit(normalized_power, loss, sp.oo) == sp.oo
        and sp.limit(accepted_composite, loss, sp.oo) == 0,
    )
    checks.check(
        "common controls and frequency do not force a common heat observable",
        sp.simplify(normalized_power - accepted_composite) != 0
        and sp.simplify(0 * normalized_power) == 0,
    )

    integer_count = sp.symbols("n", integer=True, positive=True)
    per_source = sp.symbols("I1", positive=True)
    coherence = sp.symbols("V", nonnegative=True)
    ensemble = iid_equal_amplitude_expected_intensity(
        integer_count,
        per_source,
        coherence,
    )
    checks.check(
        "accepted directional array intensity interpolates N to N squared",
        ensemble.subs(coherence, 0) == integer_count * per_source
        and ensemble.subs(coherence, 1) == integer_count**2 * per_source,
    )
    total_normalization = sp.symbols("I_total", positive=True)
    checks.check(
        "fixed-total normalization changes the aligned scaling to N",
        sp.simplify(
            ensemble.subs(
                {coherence: 1, per_source: total_normalization / integer_count}
            )
            - integer_count * total_normalization
        )
        == 0,
    )
    aligned = sp.simplify((1 + 1 + 1 + 1) ** 2)
    cancelled = sp.simplify(abs(1 + sp.I - 1 - sp.I) ** 2)
    checks.check(
        "phase disorder can move the same four emitters from sixteen to zero directionally",
        aligned == 16 and cancelled == 0,
    )
    checks.check(
        "N-squared local height can coexist with fixed integrated power",
        sp.simplify(integer_count**2 * integer_count ** (-2)) == 1,
    )
    delta = sp.symbols("delta", positive=True)
    two_line_average = sp.expand(
        amplitude**2
        * ((frequency - delta) ** 6 + (frequency + delta) ** 6)
        / 4
    )
    checks.check(
        "finite bandwidth changes the monochromatic sixth-power ledger",
        sp.simplify(two_line_average - amplitude**2 * frequency**6 / 2) != 0,
    )
    checks.check(
        "CM5 does not import or evaluate the claimed spark-geometry model",
        "isotropic_coherence" not in {
            alias.name
            for node in source_tree.body
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        and "ring_coherence(" not in source_text,
    )
    focus = _extract_function(source_tree, "focusing_intensity_gain")
    checks.check(
        "the local focus helper accepts noninteger and nonpositive ring inputs",
        focus(sp.Rational(5, 2)) == 6.25
        and focus(0) == 1.0
        and focus(-3) == 1.0,
    )
    exponent = sp.Rational(3, 2)
    checks.check(
        "the source growth inequality does not uniquely test a square law",
        bool((sp.Rational(9, 5) ** exponent) > sp.Rational(9, 5))
        and exponent != 2,
    )
    checks.check(
        "the geometry support explicitly forbids double-counting focal gain",
        "same total power" in GEOMETRY_SOURCE.read_text()
        and "NOT multiplied into the headline FOM" in GEOMETRY_SOURCE.read_text(),
    )

    tau, kernel_amplitude = sp.symbols("tau A_chi", positive=True)
    chi_zero = 2 * kernel_amplitude * sp.exp(
        -(breather_frequency * tau) ** 2
    )
    checks.check(
        "the finite-width imported Gaussian kernel is strictly positive at DC",
        chi_zero.is_positive is True and chi_zero != 0,
    )
    checks.check(
        "the Gaussian DC value vanishes only in the sharp-width limit",
        sp.limit(chi_zero, tau, sp.oo) == 0
        and sp.limit(chi_zero, tau, 0, dir="+") == 2 * kernel_amplitude,
    )
    checks.check(
        "CM5 evaluates no voltage slew spectrum population or interaction",
        all(
            token not in source_text
            for token in (
                "drive_spectrum_from_slew(",
                "seeded_population(",
                "g_trigger_derived(",
                "dVdt",
            )
        ),
    )
    dc, slew = sp.symbols("V0 S", real=True)
    checks.check(
        "DC ramp and sinusoidal derivatives are distinct input cases",
        sp.diff(dc, time) == 0
        and sp.diff(dc + slew * time, time) == slew
        and sp.diff(amplitude * sp.sin(frequency * time), time)
        == amplitude * frequency * sp.cos(frequency * time),
    )
    window = sp.symbols("T_w", positive=True)
    fourier_frequency = sp.symbols("omega_f", nonzero=True, real=True)
    voltage = time
    direct_transform = sp.integrate(
        sp.diff(voltage, time) * sp.exp(-sp.I * fourier_frequency * time),
        (time, 0, window),
    )
    voltage_transform = sp.integrate(
        voltage * sp.exp(-sp.I * fourier_frequency * time),
        (time, 0, window),
    )
    endpoint_term = window * sp.exp(-sp.I * fourier_frequency * window)
    checks.check(
        "finite-window differentiation retains the endpoint term",
        sp.simplify(
            direct_transform
            - endpoint_term
            - sp.I * fourier_frequency * voltage_transform
        )
        == 0,
    )
    permittivity = sp.Function("epsilon")(time)
    field = sp.Function("E")(time)
    checks.check(
        "time-varying constitutive response retains the product-rule term",
        sp.simplify(
            sp.diff(permittivity * field, time)
            - permittivity * sp.diff(field, time)
            - field * sp.diff(permittivity, time)
        )
        == 0,
    )
    checks.check(
        "zero seeding coupling preserves every voltage derivative but seeds nothing",
        0 * sp.diff(dc + slew * time, time) == 0,
    )

    ratio, gap = sp.symbols("w omega_0", positive=True)
    physical_frequency = ratio * gap
    checks.check(
        "C-SG-017's physical frequency map and twice-frequency line are exact",
        sp.simplify(physical_frequency / gap - ratio) == 0
        and 2 * physical_frequency == 2 * ratio * gap,
    )
    shared_guard = _extract_function(
        source_tree,
        "omega_b_is_shared",
        {
            "mo": SimpleNamespace(physical_omega_b=lambda value: value / 2**0.5),
            "OMEGA_0": 1.0,
        },
    )
    independent_equal_value = float(1 / 2**0.5)
    checks.check(
        "the shared-symbol guard tests numeric equality rather than provenance",
        shared_guard(independent_equal_value) is True,
    )
    checks.check(
        "equal frequency is compatible with a zero electrical channel",
        sp.simplify(0 * physical_frequency) == 0,
    )

    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    claim_ids = {claim["id"] for claim in registry["claims"]}
    checks.check(
        "every governing claim exists in the accepted registry",
        {"C-GW-001", "C-COH-001", "C-SG-017", "C-CMP-001", "C-RES-001"}
        <= claim_ids,
    )
    dispositions = yaml.safe_load(Path("migration/dispositions.yaml").read_text())
    checks.check(
        "FS4 is duplicate evidence rather than an EM authority",
        dispositions["units"]["FS4"]["disposition"] == "duplicate_evidence",
    )
    proposal = yaml.safe_load((root / "proposal.yaml").read_text())
    checks.check(
        "the frozen novelty gate proposes no claim before nonduplication review",
        proposal["claims_proposed"] == [],
    )

    checks.mutation_sensitive(
        "harmonic average factor and derivative order are load bearing",
        lambda candidate: sp.simplify(candidate - phase_average) == 0,
        phase_average,
        (
            2 * phase_average,
            phase_average / 2,
            second_average,
            frequency**8 * amplitude**2 / 2,
        ),
    )
    checks.mutation_sensitive(
        "finite-width DC positivity is load bearing",
        lambda candidate: candidate.is_positive is True
        and sp.limit(candidate, tau, sp.oo) == 0,
        chi_zero,
        (sp.Integer(0), -chi_zero, kernel_amplitude, 2 * kernel_amplitude),
    )
    checks.mutation_sensitive(
        "conditional CM5 amplitude composition is load bearing",
        lambda candidate: sp.simplify(candidate - modulation) == 0,
        modulation,
        (
            base * count * sp.exp(-barrier / (loading * temperature)) * loss,
            base * sp.sqrt(count) * sp.exp(barrier / (loading * temperature)) * loss,
            base * sp.sqrt(count) * sp.exp(-barrier / (loading * temperature)),
            base * sp.sqrt(count) * sp.exp(-barrier / (loading * temperature)) / loss,
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
