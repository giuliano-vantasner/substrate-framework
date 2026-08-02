"""Primary exact verifier for the P087 SA1 seeding-transfer audit."""

from __future__ import annotations

import ast
import hashlib
import inspect
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.numerics import trapezoid_integral
from substrate_framework.sine_gordon import (
    breather_core_fundamental_sine_coefficient,
    breather_field,
    breather_period,
    breather_temporal_argument_amplitude,
    breather_temporal_fundamental_sine_coefficient,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-25/"
    "bridge_SA1_seeding_transfer_function.py"
)
CONSUMER = Path("/home/dan/substrate/engineering/seeding_kernel.py")
RUNG174 = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
    "rung174_c035_spark_discharge_coherence_channel.py"
)
RUNG175 = RUNG174.with_name("rung175_c035_physical_engine_ionization_flow.py")
SOURCE_SHA256 = "b2cefcedb8c507b41defa4e43001bc7f4af052db39fc4b7481fd9a510514c72b"
CONSUMER_SHA256 = "6e771b3bf20f6c9cc91b19987b28220b867540ed089a9df6a13ea94ac820bca5"
RUNG174_SHA256 = "e0f470201313c76c77c54c0e027a01189180561d49f94fe1ef88bfe2f18a317d"
RUNG175_SHA256 = "b895622627bece5a154717b7aaab06cd0add9ed80a7c1643035c06c91fb3499c"
CONTRACT_SHA256 = "6489d7d64f1c1c2b50abea71a069fc8c85465e0fd63913b48adbec58325eb724"
FREEZE_SHA256 = "661eef14180dd4e8936a8ebaf056efea15ee4920794b72f444890d297c1189c2"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P087-sa1-seeding-transfer-audit/proposal.yaml"),
        Path("proposals/P087-sa1-seeding-transfer-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _has_symmetry(trace: sp.Expr, phase: sp.Symbol) -> bool:
    odd = sp.simplify(trace.subs(phase, -phase) + trace) == 0
    half_wave = sp.simplify(trace.subs(phase, phase + sp.pi) + trace) == 0
    return odd and half_wave


def main() -> int:
    checks = CheckLedger("P087")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    consumer_bytes = CONSUMER.read_bytes()
    consumer_text = consumer_bytes.decode("utf-8")
    rung174_text = RUNG174.read_text(encoding="utf-8")
    rung175_text = RUNG175.read_text(encoding="utf-8")

    checks.check("SA1 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check(
        "external engineering mirror hash is pinned",
        _sha256(CONSUMER) == CONSUMER_SHA256,
    )
    checks.check(
        "named C035 trigger consumers are hash pinned",
        _sha256(RUNG174) == RUNG174_SHA256
        and _sha256(RUNG175) == RUNG175_SHA256,
    )
    normalized_contract = (
        _contract_path().read_bytes().replace(b"status: accepted\n", b"status: draft\n")
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
        "source has eighteen literal sites producing twenty-one runtime checks",
        len(literal_checks) == 18
        and "for k, term in enumerate(series_terms):" in source_text
        and "series_terms = [z, -z**3 / 3, z**5 / 5, -z**7 / 7]" in source_text
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "SA1 source uses a manual trapezoid loop rather than a NumPy alias",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "wt = 0.5 if (i == 0 or i == N_pts - 1) else 1.0" in source_text,
    )

    coordinate, time = sp.symbols("x t", real=True)
    frequency = sp.Rational(3, 5)
    period = breather_period(frequency)
    field = breather_field(coordinate, time, frequency)
    checks.check(
        "accepted breather trace is odd at every fixed position",
        sp.simplify(field.subs(time, -time) + field) == 0,
    )
    checks.check(
        "accepted breather has exact half-period antisymmetry",
        sp.simplify(field.subs(time, time + period / 2) + field) == 0,
    )

    phase, amplitude = sp.symbols("y a", real=True, positive=True)
    abstract_trace = 4 * sp.atan(amplitude * sp.sin(phase))
    checks.mutation_sensitive(
        "oddness and half-wave support have distinct load-bearing hypotheses",
        lambda candidate: _has_symmetry(sp.sympify(candidate), phase),
        abstract_trace,
        (
            abstract_trace + sp.cos(phase),
            abstract_trace + sp.sin(2 * phase),
            abstract_trace + 1,
        ),
    )
    checks.check(
        "full-period mean cancels by half-period pairing",
        sp.simplify(
            abstract_trace.subs(phase, phase + sp.pi) + abstract_trace
        )
        == 0,
    )
    harmonic = sp.Symbol("n", integer=True, positive=True)
    checks.check(
        "oddness removes every cosine coefficient",
        sp.simplify(
            abstract_trace.subs(phase, -phase) * sp.cos(-harmonic * phase)
            + abstract_trace * sp.cos(harmonic * phase)
        )
        == 0,
    )
    even_index = 2 * harmonic
    shifted_even_integrand = sp.simplify(
        abstract_trace.subs(phase, phase + sp.pi)
        * sp.sin(even_index * (phase + sp.pi))
    )
    checks.check(
        "half-wave antisymmetry removes every even sine coefficient",
        sp.simplify(
            shifted_even_integrand
            + abstract_trace * sp.sin(even_index * phase)
        )
        == 0,
    )

    tangent = sp.Symbol("u", nonnegative=True)
    quarter_integral = sp.integrate(
        1 / (1 + (1 + amplitude**2) * tangent**2),
        (tangent, 0, sp.oo),
    )
    full_reciprocal_integral = 4 * quarter_integral
    checks.check(
        "tangent substitution fixes the reciprocal trigonometric integral",
        full_reciprocal_integral == 2 * sp.pi / sp.sqrt(1 + amplitude**2),
    )
    cosine_squared_integral = sp.simplify(
        ((1 + amplitude**2) * full_reciprocal_integral - 2 * sp.pi)
        / amplitude**2
    )
    derived_coefficient = sp.simplify(
        4 * amplitude * cosine_squared_integral / sp.pi
    )
    exact_coefficient = 8 * amplitude / (sp.sqrt(1 + amplitude**2) + 1)
    checks.check(
        "integration by parts gives the exact fundamental coefficient",
        sp.simplify(derived_coefficient - exact_coefficient) == 0,
    )

    def coefficient_oracle(candidate: object) -> bool:
        expression = sp.sympify(candidate)
        return (
            sp.limit(expression / (4 * amplitude), amplitude, 0, dir="+") == 1
            and sp.simplify(expression.subs(amplitude, 1) - 8 * (sp.sqrt(2) - 1))
            == 0
            and sp.simplify(sp.diff(expression, amplitude) - sp.diff(exact_coefficient, amplitude))
            == 0
        )

    checks.mutation_sensitive(
        "fundamental normalization and nonlinear correction are load bearing",
        coefficient_oracle,
        exact_coefficient,
        (
            4 * amplitude,
            4 * exact_coefficient,
            exact_coefficient + amplitude**3,
        ),
    )
    canonical = breather_temporal_fundamental_sine_coefficient(
        coordinate, frequency
    )
    canonical_amplitude = breather_temporal_argument_amplitude(coordinate, frequency)
    checks.check(
        "canonical fixed-position API implements the derived coefficient",
        sp.simplify(
            canonical
            - exact_coefficient.subs(amplitude, canonical_amplitude)
        )
        == 0,
    )
    eta = sp.Rational(4, 5)
    checks.check(
        "core specialization is exact and differs from SA1's leading term",
        breather_core_fundamental_sine_coefficient(frequency) == 4
        and 4 * eta / frequency == sp.Rational(16, 3)
        and breather_core_fundamental_sine_coefficient(frequency)
        != 4 * eta / frequency,
    )
    omega_symbol = sp.Symbol("omega", positive=True)
    eta_symbol = sp.sqrt(1 - omega_symbol**2)
    checks.check(
        "SA1's coefficient is only the omega-to-one asymptotic form",
        sp.limit(
            breather_core_fundamental_sine_coefficient(omega_symbol)
            / (4 * eta_symbol / omega_symbol),
            omega_symbol,
            1,
            dir="-",
        )
        == 1,
    )

    kernel_frequency, width, kernel_amplitude, center = sp.symbols(
        "Omega tau A omega_b", positive=True
    )
    gaussian_pair = kernel_amplitude * (
        sp.exp(-(kernel_frequency - center) ** 2 * width**2)
        + sp.exp(-(kernel_frequency + center) ** 2 * width**2)
    )
    finite_dc = sp.simplify(gaussian_pair.subs(kernel_frequency, 0))
    checks.check(
        "declared finite-width Gaussian pair is strictly positive at DC",
        finite_dc == 2 * kernel_amplitude * sp.exp(-center**2 * width**2)
        and finite_dc.is_positive,
    )
    checks.check(
        "zero occurs only in a separate sharp-width limit",
        sp.limit(finite_dc, width, sp.oo) == 0
        and sp.limit(gaussian_pair, kernel_frequency, 0) == finite_dc,
    )
    checks.check(
        "the Gaussian pair contains no third-harmonic line",
        sp.limit(gaussian_pair.subs(kernel_frequency, 3 * center), width, sp.oo)
        == 0
        and sp.limit(gaussian_pair.subs(kernel_frequency, center), width, sp.oo)
        == kernel_amplitude,
    )

    spectrum_scale, kernel_scale, overlap, energy = sp.symbols(
        "c_S c_chi O E", positive=True
    )
    target = sp.Symbol("N_target", positive=True)
    unnormalized_population = spectrum_scale * kernel_scale * overlap / energy
    per_unit_spectrum_coordinate = sp.simplify(
        unnormalized_population / spectrum_scale
    )
    checks.check(
        "per-spectrum normalization erases deposition magnitude",
        spectrum_scale not in per_unit_spectrum_coordinate.free_symbols
        and sp.diff(per_unit_spectrum_coordinate, spectrum_scale) == 0,
    )
    checks.check(
        "free kernel amplitude scales the reported coordinate arbitrarily",
        sp.diff(per_unit_spectrum_coordinate, kernel_scale) == overlap / energy
        and sp.solve(
            sp.Eq(per_unit_spectrum_coordinate, target),
            kernel_scale,
        )
        == [energy * target / overlap],
    )
    checks.check(
        "integer counting is absent from the continuous overlap coordinate",
        per_unit_spectrum_coordinate.subs(
            {kernel_scale: 1, overlap: 1, energy: 3}
        )
        == sp.Rational(1, 3),
    )

    drive_frequency, response_scale = sp.symbols("w Omega_0", real=True, positive=True)
    derivative_kernel = sp.I * drive_frequency
    rational_high_pass = drive_frequency**2 / (
        response_scale**2 + drive_frequency**2
    )
    gaussian_high_pass = 1 - sp.exp(-drive_frequency**2 / response_scale**2)
    checks.check(
        "zero DC does not uniquely imply a derivative coupling",
        derivative_kernel.subs(drive_frequency, 0) == 0
        and rational_high_pass.subs(drive_frequency, 0) == 0
        and gaussian_high_pass.subs(drive_frequency, 0) == 0
        and rational_high_pass != derivative_kernel
        and gaussian_high_pass != derivative_kernel,
    )
    shift = sp.pi / 2
    checks.check(
        "sine versus cosine phase is time-origin dependent",
        sp.expand_trig(sp.sin(phase - shift)) == -sp.cos(phase),
    )

    checks.check(
        "source declares susceptibility semantics without a driven response construction",
        "fact IS the seeding susceptibility" in source_text
        and "def chi_b(w):" in source_text
        and "retarded" not in source_text.lower()
        and "causal" not in source_text.lower(),
    )
    checks.check(
        "source normalization contradicts its claimed spectrum-magnitude input",
        "S's magnitude is an input" in source_text
        and "overlap(S_resonant) / tot_res" in source_text
        and "overlap(S_adiabatic) / tot_adi" in source_text,
    )
    checks.check(
        "external mirror carries the same physical overclaim and six legacy aliases",
        "That odd-in-t fact IS the" in consumer_text
        and "seeding susceptibility" in consumer_text
        and consumer_text.count("np.trapz") == 6,
    )
    checks.check(
        "C035 rungs retain inserted Michaelis triggers rather than consuming SA1",
        "return dVdt / (dVdt + DVDT_SAT)" in rung174_text
        and "return excess / (excess + DVDT_SAT)" in rung175_text
        and "seeding_kernel" not in rung174_text
        and "seeding_kernel" not in rung175_text,
    )
    helper_source = inspect.getsource(trapezoid_integral)
    checks.check(
        "canonical sampled integration uses the shared version-compatible helper",
        'getattr(np, "trapezoid", None)' in helper_source
        and 'getattr(np, "trapz", None)' in helper_source
        and "np.trapz" not in Path("src/substrate_framework/sine_gordon.py").read_text(),
    )
    checks.check(
        "current NumPy exposes the consumer's version-specific failure",
        not hasattr(np, "trapz") and hasattr(np, "trapezoid"),
    )
    checks.check(
        "canonical implementation promotes only field Fourier content",
        Path("src/substrate_framework/sine_gordon.py").exists()
        and not Path("src/substrate_framework/seeding_transfer.py").exists()
        and not Path("src/substrate_framework/seeding_susceptibility.py").exists(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
