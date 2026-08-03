"""Primary exact verifier for the P092 LB2 threshold adjudication."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.damped_oscillator import (
    damped_oscillator_characteristic_roots,
    damped_oscillator_discriminant,
    damped_oscillator_regime,
    mechanical_energy_derivative_on_shell,
    nominal_cycles_per_quadratic_envelope_efold,
    normalized_damped_sine_gordon_mode_residual,
    normalized_sine_gordon_mode_critical_damping,
    normalized_sine_gordon_mode_natural_frequency,
    oscillator_amplitude_envelope_factor,
    oscillator_mechanical_energy,
    oscillator_quadratic_envelope_factor,
    period_integrated_energy_change,
    underdamped_angular_frequency,
    underdamped_cycles_per_quadratic_envelope_efold,
    underdamped_oscillator_solution,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-26/"
    "bridge_LB2_coherence_threshold.py"
)
LB3 = SOURCE.with_name("bridge_LB3_damped_sg_ringdown.py")
LB4 = SOURCE.with_name("bridge_LB4_thermal_decoherence_gwindow.py")
LIFETIME_KERNEL = Path("/home/dan/substrate/engineering/lifetime_kernel.py")
DBD_PIPELINE = LIFETIME_KERNEL.parent / "dbd" / "pipeline.py"

SOURCE_SHA256 = "ae159aee3c076c1f86d77628a6bbbf206ad7e28dccd832e397250b71a981b28d"
LB3_SHA256 = "1b54ef5704fce1502464f44bd675c01824cfa48b6b98688b1df8f000d1030a2b"
LB4_SHA256 = "e33361e6985002e76342203716fd00ca72c22f905590825a6c064fe472b0d103"
LIFETIME_KERNEL_SHA256 = "51bd4f46593363ac37d99b4e95ca0bef1b572a3b075505968adf77404db4cac5"
DBD_PIPELINE_SHA256 = "5354b39d3bc25439a7f6e83c175474358b3104b2f844cc6aa3a2ee2a84439669"
CONTRACT_SHA256 = "e924970e0f0cfe6df2cddebf81fb3bdde8908efc395c8c2f6b00fa3bf2bc8f9f"
FREEZE_SHA256 = "b1b6ae491a99681ba56d5bdd4df0387c0d81095c167870a12f03d390c7440cf0"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P092-lb2-coherence-threshold"),
        Path("proposals/P092-lb2-coherence-threshold"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("C-DYN-001")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("LB2 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check(
        "direct and engineering consumers are hash pinned",
        _sha256(LB3) == LB3_SHA256
        and _sha256(LB4) == LB4_SHA256
        and _sha256(LIFETIME_KERNEL) == LIFETIME_KERNEL_SHA256
        and _sha256(DBD_PIPELINE) == DBD_PIPELINE_SHA256,
    )
    normalized_contract = (campaign_dir / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n",
        b"status: draft\n",
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
        "source has exactly seventeen literal checks",
        len(literal_checks) == 17
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    imported_modules = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "source imports no accepted oscillator, field, or material API",
        imported_modules == {"sys", "sympy"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body),
    )

    omega_0, gamma, root = sp.symbols(
        "omega_0 Gamma r",
        positive=True,
        real=True,
    )
    roots = damped_oscillator_characteristic_roots(omega_0, gamma)
    polynomial = root**2 + gamma * root + omega_0**2
    checks.check(
        "characteristic roots solve the declared abstract oscillator",
        all(sp.simplify(polynomial.subs(root, item)) == 0 for item in roots),
    )
    checks.check(
        "discriminant gives all three exact oscillator regimes",
        damped_oscillator_discriminant(1, sp.Rational(1, 2))
        == -sp.Rational(15, 4)
        and damped_oscillator_regime(1, sp.Rational(1, 2)) == "underdamped"
        and damped_oscillator_regime(1, 2) == "critical"
        and damped_oscillator_regime(1, 3) == "overdamped",
    )
    checks.mutation_sensitive(
        "critical discriminant factor is load bearing",
        lambda factor: sp.simplify(
            gamma**2
            - factor * omega_0**2
            - damped_oscillator_discriminant(omega_0, gamma)
        )
        == 0,
        4,
        (1, 2, 8),
    )

    time = sp.symbols("t", real=True)
    cosine, sine = sp.symbols("A B", real=True)
    solution = underdamped_oscillator_solution(
        time,
        omega_0,
        gamma,
        cosine,
        sine,
    )
    residual = (
        sp.diff(solution, time, 2)
        + gamma * sp.diff(solution, time)
        + omega_0**2 * solution
    )
    checks.check(
        "general underdamped solution has zero exact ODE residual",
        sp.simplify(sp.expand_trig(residual)) == 0,
    )
    checks.check(
        "damped frequency and coordinate envelope are distinct factors",
        underdamped_angular_frequency(1, 1) == sp.sqrt(3) / 2
        and oscillator_amplitude_envelope_factor(gamma, time)
        == sp.exp(-gamma * time / 2)
        and oscillator_quadratic_envelope_factor(gamma, time)
        == sp.exp(-gamma * time),
    )

    displacement = sp.Function("q")(time)
    velocity = sp.diff(displacement, time)
    energy = oscillator_mechanical_energy(displacement, velocity, omega_0)
    on_shell_derivative = sp.diff(energy, time).subs(
        sp.diff(displacement, time, 2),
        -gamma * velocity - omega_0**2 * displacement,
    )
    checks.check(
        "mechanical energy has the exact phase-dependent damping balance",
        sp.simplify(
            on_shell_derivative
            - mechanical_energy_derivative_on_shell(velocity, gamma)
        )
        == 0,
    )
    checks.check(
        "pointwise exponential mechanical energy is refuted at a turning point",
        mechanical_energy_derivative_on_shell(0, gamma) == 0
        and -gamma * oscillator_mechanical_energy(1, 0, omega_0) != 0,
    )
    checks.mutation_sensitive(
        "damping sign is load bearing in the energy balance",
        lambda sign: sp.simplify(
            sign * gamma * velocity**2
            - mechanical_energy_derivative_on_shell(velocity, gamma)
        )
        == 0,
        -1,
        (0, 1),
    )

    actual_cycles = underdamped_cycles_per_quadratic_envelope_efold(1, gamma)
    nominal_cycles = nominal_cycles_per_quadratic_envelope_efold(1, gamma)
    checks.check(
        "actual and nominal cycle conventions differ away from weak damping",
        underdamped_cycles_per_quadratic_envelope_efold(1, 1)
        == sp.sqrt(3) / (4 * sp.pi)
        and nominal_cycles_per_quadratic_envelope_efold(1, 1)
        == 1 / (2 * sp.pi)
        and sp.simplify(actual_cycles - nominal_cycles) != 0,
    )
    checks.check(
        "actual cycles vanish at critical damping while source nominal cycles do not",
        sp.limit(actual_cycles, gamma, 2, dir="-") == 0
        and nominal_cycles.subs(gamma, 2) == 1 / (4 * sp.pi),
    )

    k = sp.symbols("k", real=True)
    mode_frequency = normalized_sine_gordon_mode_natural_frequency(k)
    checks.check(
        "normalized damped sine-Gordon modes have the exact gap-one dispersion",
        mode_frequency == sp.sqrt(1 + k**2)
        and normalized_sine_gordon_mode_natural_frequency(0) == 1
        and normalized_sine_gordon_mode_critical_damping(k)
        == 2 * sp.sqrt(1 + k**2),
    )
    mode = underdamped_oscillator_solution(time, 1, sp.Rational(6, 5), 1, 0)
    checks.check(
        "the band-edge field mode satisfies its derived damped mode equation",
        sp.simplify(
            normalized_damped_sine_gordon_mode_residual(
                mode,
                time,
                0,
                sp.Rational(6, 5),
            )
        )
        == 0,
    )
    checks.check(
        "exact countermodel reverses the source classification",
        damped_oscillator_regime(1, sp.Rational(6, 5)) == "underdamped"
        and damped_oscillator_regime(
            sp.Rational(1, 2),
            sp.Rational(6, 5),
        )
        == "overdamped",
    )
    checks.mutation_sensitive(
        "sine-Gordon mass gap is load bearing",
        lambda mass_squared: sp.simplify(
            sp.sqrt(mass_squared + k**2) - mode_frequency
        )
        == 0,
        1,
        (0, 2, 4),
    )

    loss_integral = sp.symbols("I", positive=True, real=True)
    checks.check(
        "period-integrated positive damping has strict negative energy change",
        period_integrated_energy_change(gamma, loss_integral)
        == -gamma * loss_integral
        and period_integrated_energy_change(1, 3) == -3,
    )
    checks.check(
        "zero-flux periodicity forces the velocity-square integral to vanish",
        sp.solve(
            sp.Eq(period_integrated_energy_change(gamma, loss_integral), 0),
            loss_integral,
        )
        == [],
        "a positive loss integral cannot coexist with zero periodic energy change",
    )
    checks.mutation_sensitive(
        "boundary flux hypothesis is load bearing",
        lambda flux: period_integrated_energy_change(1, 3, flux) == -3,
        0,
        (3, -3),
    )

    canonical_text = Path(
        "src/substrate_framework/damped_oscillator.py"
    ).read_text(encoding="utf-8")
    checks.check(
        "canonical exact implementation uses no version-specific quadrature alias",
        "np.trapz" not in canonical_text and "numpy.trapz" not in canonical_text,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
