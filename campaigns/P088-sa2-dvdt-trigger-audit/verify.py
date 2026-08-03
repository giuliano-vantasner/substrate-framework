"""Primary exact verifier for the P088 SA2 dV/dt-trigger audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-25/"
    "bridge_SA2_dvdt_not_v_emerges.py"
)
SA4 = SOURCE.with_name("bridge_SA4_threshold_saturation_guard.py")
ENGINEERING = Path("/home/dan/substrate/engineering/seeding_kernel.py")
NUCLEATION = ENGINEERING.with_name("nucleation_efficiency_model.py")
RUNG174 = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
    "rung174_c035_spark_discharge_coherence_channel.py"
)
RUNG175 = RUNG174.with_name("rung175_c035_physical_engine_ionization_flow.py")
CONSTITUTIVE = Path("src/substrate_framework/constitutive.py")
CLAIMS = Path("governance/claims.yaml")

SOURCE_SHA256 = "4772f0e52f08e68197662383efe2ee91426769b1281dc2db1d20aa40c8a8398e"
SA4_SHA256 = "55243c459d40fded73ec03260e2b66c79a60e29e47ec3d363145d25538507f6e"
ENGINEERING_SHA256 = "6e771b3bf20f6c9cc91b19987b28220b867540ed089a9df6a13ea94ac820bca5"
NUCLEATION_SHA256 = "bad798b39d850ecf92a97e25bfb0341ef7ae80b036c26a88037efdd618d8d3b8"
RUNG174_SHA256 = "e0f470201313c76c77c54c0e027a01189180561d49f94fe1ef88bfe2f18a317d"
RUNG175_SHA256 = "b895622627bece5a154717b7aaab06cd0add9ed80a7c1643035c06c91fb3499c"
CONTRACT_SHA256 = "2254bfa45353d7e21b20876ff84fc8a4c169218a3dfa5ed730f43ee7fdc71c41"
FREEZE_SHA256 = "bd3ae087eb10f348daf02b6fb944266584bddf5d4d5ba84bb68f2e36735b74ac"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P088-sa2-dvdt-trigger-audit"),
        Path("proposals/P088-sa2-dvdt-trigger-audit"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assigned_expression_names(tree: ast.AST, target: str) -> set[str]:
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(item, ast.Name) and item.id == target for item in node.targets)
        ):
            return {
                item.id for item in ast.walk(node.value) if isinstance(item, ast.Name)
            }
    raise AssertionError(f"assignment for {target!r} not found")


def _function(tree: ast.AST, name: str) -> ast.FunctionDef:
    return next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name
    )


def main() -> int:
    checks = CheckLedger("P088")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)
    engineering_text = ENGINEERING.read_text(encoding="utf-8")
    engineering_tree = ast.parse(engineering_text)
    nucleation_text = NUCLEATION.read_text(encoding="utf-8")
    rung174_text = RUNG174.read_text(encoding="utf-8")
    rung175_text = RUNG175.read_text(encoding="utf-8")
    sa4_text = SA4.read_text(encoding="utf-8")

    checks.check("SA2 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("pending SA4 dependency hash is pinned", _sha256(SA4) == SA4_SHA256)
    checks.check(
        "external engineering consumers are hash pinned",
        _sha256(ENGINEERING) == ENGINEERING_SHA256
        and _sha256(NUCLEATION) == NUCLEATION_SHA256,
    )
    checks.check(
        "named C035 consumers are hash pinned",
        _sha256(RUNG174) == RUNG174_SHA256
        and _sha256(RUNG175) == RUNG175_SHA256,
    )
    normalized_contract = (campaign_dir / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-source freeze record remains immutable",
        _sha256(campaign_dir / "evidence/frozen-proposal.yaml") == FREEZE_SHA256,
    )

    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has nine literal sites producing twelve runtime checks",
        len(literal_checks) == 9
        and "for s_num in [sp.Rational(1, 4), sp.Rational(1, 2), sp.Integer(1), sp.Integer(2)]"
        in source_text
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source quadrature is an explicit midpoint loop rather than a version-specific NumPy alias",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and source_text.count("Npts = 4000") == 2
        and "w = (i + 0.5) * h" in source_text,
    )
    delta_names = _assigned_expression_names(source_tree, "delta_N")
    checks.check(
        "source delta_N contains neither the declared voltage offset nor a waveform",
        "c" not in delta_names
        and "V" not in delta_names
        and delta_names == {"offset_overlap_delta", "sp"},
    )
    imported_modules = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "source imports no accepted cell, constitutive, interaction, response, or seeding module",
        imported_modules == {"sys", "sympy", "math"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body),
    )

    observed, width, packet_width, packet_center, band_center, scale = sp.symbols(
        "omega tau e mu omega_b A", real=True, positive=True
    )
    quadratic = width**2 + 1 / (2 * packet_width**2)
    linear = width**2 * band_center + packet_center / (2 * packet_width**2)
    constant = (
        width**2 * band_center**2
        + packet_center**2 / (2 * packet_width**2)
    )
    completed_square_overlap = sp.simplify(
        scale
        / (packet_width * sp.sqrt(2 * quadratic))
        * sp.exp(linear**2 / quadratic - constant)
    )
    exact_overlap = (
        scale
        / sp.sqrt(1 + 2 * packet_width**2 * width**2)
        * sp.exp(
            -width**2
            * (packet_center - band_center) ** 2
            / (1 + 2 * packet_width**2 * width**2)
        )
    )
    checks.check(
        "completion of the square fixes the exact Gaussian overlap",
        sp.simplify(completed_square_overlap / exact_overlap) == 1,
    )
    finite_dc = 2 * scale * sp.exp(-band_center**2 * width**2)
    checks.check(
        "the inherited finite-width Gaussian pair is positive at DC",
        finite_dc.is_positive
        and sp.limit(finite_dc, width, sp.oo) == 0,
    )
    source_dc_order = sp.limit(
        exact_overlap.subs(packet_center, 0), width, sp.oo
    )
    source_resonant_order = sp.limit(
        exact_overlap.subs(packet_center, band_center), width, sp.oo
    )
    checks.check(
        "SA2 sharpens an unnormalised lobe until every fixed input overlap vanishes",
        source_dc_order == 0 and source_resonant_order == 0,
    )
    correct_resonant_order = sp.limit(
        sp.limit(
            exact_overlap.subs(packet_center, band_center),
            packet_width,
            0,
            dir="+",
        ),
        width,
        sp.oo,
    )
    checks.check(
        "delta-sequence-first evaluation distinguishes resonance from DC",
        correct_resonant_order == scale
        and sp.limit(
            sp.limit(
                exact_overlap.subs(packet_center, 0),
                packet_width,
                0,
                dir="+",
            ),
            width,
            sp.oo,
        )
        == 0,
    )

    def source_limit_oracle(center: object) -> bool:
        return sp.limit(
            exact_overlap.subs(packet_center, sp.sympify(center)),
            width,
            sp.oo,
        ) == 0

    checks.check(
        "source DC predicate is insensitive to moving the packet onto resonance",
        source_limit_oracle(0) and source_limit_oracle(band_center),
    )

    offset, kernel_at_zero = sp.symbols("c K_0", real=True)
    linear_shift = 2 * sp.pi * offset * kernel_at_zero
    checks.check(
        "infinite-domain offset invariance is only a conditional linear distribution identity",
        linear_shift.subs(kernel_at_zero, 0) == 0
        and sp.diff(linear_shift, offset) == 2 * sp.pi * kernel_at_zero,
    )
    record_length, frequency = sp.symbols("T Omega", real=True, positive=True)
    finite_window_shift = (
        2
        * offset
        * sp.exp(-sp.I * frequency * record_length / 2)
        * sp.sin(frequency * record_length / 2)
        / frequency
    )
    checks.check(
        "a finite rectangular record leaks a constant at generic nonzero frequency",
        sp.simplify(
            finite_window_shift.subs(frequency, sp.pi / record_length)
            + 2 * sp.I * offset * record_length / sp.pi
        )
        == 0
        and sp.simplify(
            finite_window_shift.subs(frequency, 2 * sp.pi / record_length)
        )
        == 0,
    )
    real_part, imaginary_part = sp.symbols("x y", real=True)
    power_change = sp.expand(
        (real_part + offset) ** 2
        + imaginary_part**2
        - (real_part**2 + imaginary_part**2)
    )
    checks.check(
        "a power spectrum does not inherit the linear offset proof",
        power_change == offset**2 + 2 * offset * real_part
        and sp.diff(power_change, real_part) == 2 * offset,
    )

    time = sp.Symbol("t", real=True)
    epsilon = sp.Function("epsilon")(time)
    field = sp.Function("E")(time)
    displacement_current = sp.diff(epsilon * field, time)
    checks.check(
        "the displacement-current product rule retains time-varying constitutive response",
        sp.simplify(
            displacement_current
            - epsilon * sp.diff(field, time)
            - field * sp.diff(epsilon, time)
        )
        == 0
        and field * sp.diff(epsilon, time) != 0,
    )
    epsilon_constant = sp.Symbol("epsilon_0", positive=True)
    voltage = sp.Function("V")(time)
    gap = sp.Symbol("d", positive=True)
    fixed_cell_current = sp.diff(epsilon_constant * voltage / gap, time)
    checks.check(
        "epsilon*dV/dt/d follows only after constant-response and fixed-gap declarations",
        fixed_cell_current == epsilon_constant * sp.diff(voltage, time) / gap,
    )
    endpoint_term, voltage_transform = sp.symbols("B V_tilde")
    derivative_transform = endpoint_term + sp.I * frequency * voltage_transform
    checks.check(
        "Fourier differentiation requires a vanishing endpoint term",
        derivative_transform.subs(endpoint_term, 0)
        == sp.I * frequency * voltage_transform
        and sp.diff(derivative_transform, endpoint_term) == 1,
    )

    slew = sp.Symbol("s", positive=True)
    source_density = observed**2 * sp.exp(-(observed / slew) ** 2)
    source_derivative = sp.diff(source_density, slew)
    checks.check(
        "the inserted source family is pointwise increasing by exact algebra",
        sp.simplify(
            source_derivative
            - 2
            * observed**4
            * sp.exp(-(observed / slew) ** 2)
            / slew**3
        )
        == 0
        and source_derivative.is_positive,
    )
    checks.check(
        "the inserted source family has a fixed-band ceiling",
        sp.limit(source_density, slew, sp.oo) == observed**2
        and sp.limit(source_density, slew, 0, dir="+") == 0,
    )
    fixed_peak_density = source_density / slew**2
    fixed_peak_derivative = sp.factor(sp.diff(fixed_peak_density, slew))
    expected_fixed_peak_derivative = (
        2
        * observed**2
        * (observed**2 - slew**2)
        * sp.exp(-(observed / slew) ** 2)
        / slew**5
    )
    checks.check(
        "fixed-time-domain-peak normalization reverses the large-slew trend",
        sp.simplify(fixed_peak_derivative - expected_fixed_peak_derivative) == 0
        and sp.limit(fixed_peak_density, slew, sp.oo) == 0
        and expected_fixed_peak_derivative.subs({observed: 1, slew: 2}) < 0,
    )
    checks.mutation_sensitive(
        "source monotonicity depends on its spectral normalization",
        lambda candidate: sp.diff(sp.sympify(candidate), slew).subs(
            {observed: 1, slew: 2}
        )
        > 0,
        source_density,
        (fixed_peak_density,),
    )
    time_peak = slew / sp.sqrt(2 * sp.pi)
    maximum_time_derivative = slew**2 / sp.sqrt(2 * sp.pi * sp.E)
    checks.check(
        "the source Gaussian spectrum does not keep time-domain voltage amplitude fixed",
        sp.diff(time_peak, slew) != 0
        and sp.diff(maximum_time_derivative, slew) != 0,
    )

    common_slew = sp.Symbol("S", positive=True)
    first_frequency = sp.Integer(1)
    second_frequency = sp.Integer(3)
    kernel = lambda item: sp.exp(-4 * (item - first_frequency) ** 2)
    first_overlap = (common_slew / first_frequency) ** 2 * kernel(first_frequency)
    second_overlap = (common_slew / second_frequency) ** 2 * kernel(second_frequency)
    checks.check(
        "same-maximum-slew sinusoids can have different band overlap",
        first_frequency * (common_slew / first_frequency) == common_slew
        and second_frequency * (common_slew / second_frequency) == common_slew
        and sp.simplify(first_overlap / second_overlap) == 9 * sp.exp(16)
        and 9 * sp.exp(16) > 1,
    )

    trigger_function = _function(engineering_tree, "g_trigger_derived")
    threshold_if = next(node for node in trigger_function.body if isinstance(node, ast.If))
    tail_nodes = trigger_function.body[trigger_function.body.index(threshold_if) + 1 :]
    tail_names = {
        node.id
        for statement in tail_nodes
        for node in ast.walk(statement)
        if isinstance(node, ast.Name)
    }
    checks.check(
        "engineering mirror inserts breakdown and then ignores voltage",
        isinstance(threshold_if.test, ast.Compare)
        and {"V", "Vbd"}.issubset(
            {node.id for node in ast.walk(threshold_if.test) if isinstance(node, ast.Name)}
        )
        and "V" not in tail_names
        and "Vbd" not in tail_names,
    )
    checks.check(
        "engineering mirror has six current-NumPy-incompatible trapz calls",
        engineering_text.count("np.trapz") == 6
        and "np.trapezoid" not in engineering_text,
    )
    checks.check(
        "nucleation consumer maps slew through the old design knob and restores a nonzero floor",
        "SLEW_SCALE_PER_KVUS = 1.0 / DVDT_SAT_KVUS" in nucleation_text
        and "return max(0.05, min(m, 5.0))" in nucleation_text
        and "slew_kvus / (slew_kvus + sat_kvus)" in nucleation_text,
    )
    checks.check(
        "named C035 consumers retain inserted trigger laws and import no SA2 implementation",
        "return dVdt / (dVdt + DVDT_SAT)" in rung174_text
        and "return excess / (excess + DVDT_SAT)" in rung175_text
        and "bridge_SA2" not in rung174_text
        and "bridge_SA2" not in rung175_text,
    )
    checks.check(
        "pending SA4 repeats the inserted waveform family, gain, threshold floor, and fit",
        "exp(-(omega/s)^2)" in sa4_text
        and "G_BIG = 900.0" in sa4_text
        and "math.floor(es / E_b)" in sa4_text
        and "best_ssat" in sa4_text,
    )

    constitutive_text = CONSTITUTIVE.read_text(encoding="utf-8")
    claims_text = CLAIMS.read_text(encoding="utf-8")
    checks.check(
        "accepted constitutive API supplies no cell voltage map or displacement-current mechanism",
        "def co_scaled_permittivity" in constitutive_text
        and "displacement" not in constitutive_text.lower()
        and "voltage" not in constitutive_text.lower(),
    )
    checks.check(
        "accepted C-SG-015 remains an undriven field-trace ceiling",
        "C-SG-015" in claims_text
        and "susceptibility" in claims_text
        and "seeded population" in claims_text,
    )
    checks.check(
        "no physical seeding claim can close from SA2's executable dependency graph",
        "substrate_framework" not in source_text
        and "solve_ivp" not in source_text
        and "Green" not in source_text
        and "retarded" not in source_text
        and "absorption" not in source_text.lower(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
