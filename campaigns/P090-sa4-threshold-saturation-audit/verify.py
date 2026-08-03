"""Primary exact verifier for the P090 SA4 threshold/saturation audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-25/"
    "bridge_SA4_threshold_saturation_guard.py"
)
ENGINEERING = Path("/home/dan/substrate/engineering/seeding_kernel.py")
NUCLEATION = ENGINEERING.with_name("nucleation_efficiency_model.py")
DBD_PIPELINE = Path("/home/dan/substrate/engineering/dbd/pipeline.py")
COMMENSURATE = DBD_PIPELINE.with_name("commensurate.py")
RUNG174 = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
    "rung174_c035_spark_discharge_coherence_channel.py"
)
RUNG175 = RUNG174.with_name("rung175_c035_physical_engine_ionization_flow.py")

SOURCE_SHA256 = "55243c459d40fded73ec03260e2b66c79a60e29e47ec3d363145d25538507f6e"
ENGINEERING_SHA256 = "6e771b3bf20f6c9cc91b19987b28220b867540ed089a9df6a13ea94ac820bca5"
NUCLEATION_SHA256 = "bad798b39d850ecf92a97e25bfb0341ef7ae80b036c26a88037efdd618d8d3b8"
DBD_PIPELINE_SHA256 = "5354b39d3bc25439a7f6e83c175474358b3104b2f844cc6aa3a2ee2a84439669"
COMMENSURATE_SHA256 = "6f85aafcb330af6619aa0f98fed36212c573c0e9831ee76b7628143992eeff4f"
RUNG174_SHA256 = "e0f470201313c76c77c54c0e027a01189180561d49f94fe1ef88bfe2f18a317d"
RUNG175_SHA256 = "b895622627bece5a154717b7aaab06cd0add9ed80a7c1643035c06c91fb3499c"
CONTRACT_SHA256 = "c469e191827e6b450f13b4b42022d7b3a936d64494a0dba6bd8fbf1cbd2d0896"
FREEZE_SHA256 = "888dece23cbc2bf73500d3d80fe92a14d86b88cad299ca88f76a5f97d861c399"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P090-sa4-threshold-saturation-audit"),
        Path("proposals/P090-sa4-threshold-saturation-audit"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _function(tree: ast.AST, name: str) -> ast.FunctionDef:
    return next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name
    )


def _assigned_number(tree: ast.AST, name: str) -> int | float:
    for node in tree.body:  # source constants are module-level assignments
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, (int, float))
        ):
            return node.value.value
    raise AssertionError(f"numeric assignment for {name!r} not found")


def _loaded_names(node: ast.AST) -> set[str]:
    return {
        item.id
        for item in ast.walk(node)
        if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Load)
    }


def main() -> int:
    checks = CheckLedger("P090")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)
    engineering_text = ENGINEERING.read_text(encoding="utf-8")
    engineering_tree = ast.parse(engineering_text)
    nucleation_text = NUCLEATION.read_text(encoding="utf-8")
    pipeline_text = DBD_PIPELINE.read_text(encoding="utf-8")
    commensurate_text = COMMENSURATE.read_text(encoding="utf-8")
    rung174_text = RUNG174.read_text(encoding="utf-8")
    rung175_text = RUNG175.read_text(encoding="utf-8")

    checks.check("SA4 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check(
        "external engineering consumers are hash pinned",
        _sha256(ENGINEERING) == ENGINEERING_SHA256
        and _sha256(NUCLEATION) == NUCLEATION_SHA256
        and _sha256(DBD_PIPELINE) == DBD_PIPELINE_SHA256
        and _sha256(COMMENSURATE) == COMMENSURATE_SHA256,
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
        "partial-exposure freeze record remains immutable",
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
        "source has thirteen literal checks and a literal tally",
        len(literal_checks) == 13
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    imported_modules = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "source imports no accepted response, deposition, formation, breakdown, or population module",
        imported_modules == {"sys", "math", "sympy"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body),
    )
    checks.check(
        "source inserts distinct gains for the no-crossing and crossing examples",
        _assigned_number(source_tree, "G") == 1.0
        and _assigned_number(source_tree, "G_BIG") == 900.0,
    )
    count_names = _loaded_names(_function(source_tree, "N_count"))
    big_count_names = _loaded_names(_function(source_tree, "N_big"))
    checks.check(
        "source counts are floor operations on two separately gained energies",
        {"E_seed", "E_b", "math"}.issubset(count_names)
        and {"E_seed_big", "E_b", "math"}.issubset(big_count_names)
        and "G_BIG" in _loaded_names(_function(source_tree, "E_seed_big")),
    )

    omega, width = sp.symbols("omega_b tau", positive=True, real=True)
    chi_zero = 2 * sp.exp(-width**2 * omega**2)
    checks.check(
        "finite-width Gaussian pair is positive at DC rather than zero",
        chi_zero.is_positive
        and chi_zero.subs({omega: 1 / sp.sqrt(2), width: 10}) == 2 * sp.exp(-50)
        and sp.limit(chi_zero, width, sp.oo) == 0,
    )
    checks.check(
        "source DC tolerance is a width-selected approximation",
        chi_zero.subs({omega: 1 / sp.sqrt(2), width: 10}) < sp.Rational(1, 10**9)
        and chi_zero.subs({omega: 1 / sp.sqrt(2), width: 5}) > sp.Rational(1, 10**9),
    )
    checks.mutation_sensitive(
        "source zero-DC verdict depends on the planted sharpness",
        lambda candidate: chi_zero.subs(
            {omega: 1 / sp.sqrt(2), width: sp.sympify(candidate)}
        )
        < sp.Rational(1, 10**9),
        10,
        (5,),
    )

    breather_frequency = sp.Symbol("w", positive=True, real=True)
    breather_energy = 16 * sp.sqrt(1 - breather_frequency**2)
    candidate_energy = sp.Symbol("E", positive=True, real=True)
    inverse_frequency = sp.sqrt(1 - (candidate_energy / 16) ** 2)
    checks.check(
        "accepted breather family has no positive global minimum energy",
        sp.limit(breather_energy, breather_frequency, 1, dir="-") == 0
        and sp.limit(breather_energy, breather_frequency, 0, dir="+") == 16
        and sp.simplify(
            breather_energy.subs(breather_frequency, inverse_frequency)
            - candidate_energy
        )
        == 0,
    )
    checks.check(
        "source working-point energy is an existing-breather coordinate",
        sp.simplify(breather_energy.subs(breather_frequency, 1 / sp.sqrt(2)))
        == 8 * sp.sqrt(2),
    )

    unit, overlap, gain = sp.symbols("E_b F G", positive=True, real=True)
    threshold_gain = unit / overlap
    checks.check(
        "free gain places the crossing at an arbitrary positive overlap",
        sp.simplify((threshold_gain * overlap) / unit) == 1
        and sp.floor((threshold_gain / 2) * overlap / unit) == 0
        and sp.floor(2 * threshold_gain * overlap / unit) == 2,
    )
    population = sp.Symbol("n", integer=True, nonnegative=True)
    arbitrary_gain = (population + sp.Rational(1, 2)) * unit / overlap
    checks.check(
        "free gain realizes every nonnegative integer floor count",
        sp.floor(sp.simplify(arbitrary_gain * overlap / unit)) == population,
    )
    amplitude_scale = sp.Symbol("c", positive=True, real=True)
    checks.check(
        "spectral-amplitude normalization is covariant with inverse gain",
        sp.simplify((gain / amplitude_scale**2) * (amplitude_scale**2 * overlap))
        == gain * overlap,
    )
    input_dimension, kernel_dimension, frequency_dimension, energy_dimension = sp.symbols(
        "d_S d_chi d_omega d_E"
    )
    gain_dimension = sp.solve(
        sp.Eq(
            sp.Symbol("d_G")
            + input_dimension
            + kernel_dimension
            + frequency_dimension
            - energy_dimension,
            0,
        ),
        sp.Symbol("d_G"),
    )
    checks.check(
        "dimensional closure leaves the gain fixed only by undeclared spectrum and kernel units",
        gain_dimension
        == [energy_dimension - frequency_dimension - input_dimension - kernel_dimension],
    )

    checks.check(
        "floor bookkeeping differs from a required-input ceiling convention",
        sp.floor(sp.Rational(3, 2)) == 1
        and sp.ceiling(sp.Rational(3, 2)) == 2
        and sp.floor(sp.Rational(999, 1000)) == 0
        and sp.floor(1) == 1,
    )
    exact_energy = sp.Rational(7, 3) * unit
    completed = sp.floor(exact_energy / unit)
    remainder = sp.simplify(exact_energy - completed * unit)
    checks.check(
        "Euclidean partition retains an unassigned sub-unit remainder",
        completed == 2 and remainder == unit / 3,
    )

    spectral_frequency, slew = sp.symbols("Omega s", positive=True, real=True)
    positive_kernel = sp.Symbol("chi", positive=True, real=True)
    inserted_density = (
        spectral_frequency**2
        * sp.exp(-(spectral_frequency / slew) ** 2)
        * positive_kernel
    )
    inserted_derivative = sp.diff(inserted_density, slew)
    checks.check(
        "inserted spectral family is pointwise strictly increasing",
        sp.simplify(
            inserted_derivative
            - 2
            * spectral_frequency**4
            * sp.exp(-(spectral_frequency / slew) ** 2)
            * positive_kernel
            / slew**3
        )
        == 0
        and inserted_derivative.is_positive,
    )
    checks.check(
        "inserted family has a fixed-band pointwise ceiling",
        sp.limit(inserted_density, slew, 0, dir="+") == 0
        and sp.limit(inserted_density, slew, sp.oo)
        == spectral_frequency**2 * positive_kernel,
    )
    full_line_band_ceiling = sp.sqrt(sp.pi) * (
        omega**2 / width + sp.Rational(1, 2) / width**3
    )
    checks.check(
        "unnormalised Gaussian-band ceiling loses mass as sharpness grows",
        full_line_band_ceiling.is_positive
        and sp.limit(full_line_band_ceiling, width, sp.oo) == 0,
    )
    fixed_peak_density = inserted_density / slew**2
    checks.check(
        "an admissible fixed-peak normalization reverses the large-slew trend",
        sp.diff(fixed_peak_density, slew).subs(
            {spectral_frequency: 1, slew: 2, positive_kernel: 1}
        )
        < 0
        and sp.limit(fixed_peak_density, slew, sp.oo) == 0,
    )
    checks.mutation_sensitive(
        "rising-saturation verdict depends on the waveform normalization",
        lambda candidate: sp.diff(sp.sympify(candidate), slew).subs(
            {spectral_frequency: 1, slew: 2, positive_kernel: 1}
        )
        > 0,
        inserted_density,
        (fixed_peak_density,),
    )

    sharp_lobe_response = sp.exp(-(omega / slew) ** 2)
    half_scale = omega / sp.sqrt(sp.log(2))
    checks.check(
        "sharp-lobe half-saturation scale is set by the center frequency",
        sp.simplify(sharp_lobe_response.subs(slew, half_scale)) == sp.Rational(1, 2)
        and sp.diff(half_scale, width) == 0,
    )
    michaelis_scale = sp.Symbol("a", positive=True, real=True)
    michaelis = slew / (slew + michaelis_scale)
    checks.check(
        "sharp-lobe response is not a Michaelis law at either asymptotic end",
        sp.limit(sharp_lobe_response / slew, slew, 0, dir="+") == 0
        and sp.limit(michaelis / slew, slew, 0, dir="+") == 1 / michaelis_scale
        and sp.limit(slew * (1 - sharp_lobe_response), slew, sp.oo) == 0
        and sp.limit(slew * (1 - michaelis), slew, sp.oo) == michaelis_scale,
    )
    checks.check(
        "source Michaelis fit is a loose sampled regression rather than an identity",
        "best_e < 0.2" in source_text
        and "0.05 < best_ssat < 5.0" in source_text
        and "omega_b/bandwidth" in source_text,
    )

    total_spectrum = sp.Symbol("I_S", positive=True, real=True)
    checks.check(
        "constant-kernel rejection ratio is one by construction",
        sp.simplify(
            (total_spectrum / total_spectrum) / (total_spectrum / total_spectrum)
        )
        == 1,
    )
    ovl_adi_assignment = next(
        node
        for node in source_tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "ovl_adi" for target in node.targets)
    )
    checks.check(
        "adiabatic guard evaluates a normalized overlap rather than source energy or count",
        {"overlap", "total", "S_adiabatic", "chi_b"}.issubset(
            _loaded_names(ovl_adi_assignment.value)
        )
        and "E_seed" not in _loaded_names(ovl_adi_assignment.value)
        and "N_count" not in _loaded_names(ovl_adi_assignment.value),
    )

    trigger_names = _loaded_names(_function(engineering_tree, "g_trigger_derived"))
    trigger_voltage_uses = sum(
        isinstance(node, ast.Name) and node.id == "V"
        for node in ast.walk(_function(engineering_tree, "g_trigger_derived"))
    )
    checks.check(
        "engineering mirror inserts breakdown and uses no voltage above that branch",
        {"V", "Vbd"}.issubset(trigger_names)
        and trigger_voltage_uses == 1
        and engineering_text.count("np.trapz") == 6
        and "if V <= Vbd:" in engineering_text
        and engineering_text.count("V <= Vbd") == 1,
    )
    checks.check(
        "downstream engineering retains inserted unit and population knobs",
        "SLEW_SCALE_PER_KVUS = 1.0 / DVDT_SAT_KVUS" in nucleation_text
        and "M_SAT_BASE = 2.5" in nucleation_text
        and "return max(0.05, min(m, 5.0))" in nucleation_text
        and "SEED_BASE_PER_SITE = 2.5" in pipeline_text
        and "overlap_G=1.0" in pipeline_text,
    )
    checks.check(
        "later units bridge remains conditional on supplied voltage and medium scales",
        "omega_drive = abs(slew_V_per_s) / V_scale" in commensurate_text
        and "return dimensionless_omega(omega_drive, m_phys_rad)" in commensurate_text,
    )
    checks.check(
        "named C035 consumers retain their inserted saturation constants",
        "DVDT_SAT = 1.0" in rung174_text
        and "dVdt / (dVdt + DVDT_SAT)" in rung174_text
        and "DVDT_SAT = 5.0" in rung175_text
        and "excess / (excess + DVDT_SAT)" in rung175_text,
    )
    checks.check(
        "source contains no voltage, breakdown-state, plasma, work, or formation variable",
        not ({"V", "Vbd", "plasma", "work", "phi", "formation"} & {
            node.id for node in ast.walk(source_tree) if isinstance(node, ast.Name)
        }),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
