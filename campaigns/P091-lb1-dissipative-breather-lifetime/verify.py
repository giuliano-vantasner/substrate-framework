"""Primary exact verifier for the P091 LB1 lifetime adjudication."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.sine_gordon import (
    breather_action,
    breather_damping_form_factor,
    breather_energy,
    breather_instantaneous_energy_decay_time,
    breather_mean_kinetic_integral,
    phase_averaged_breather_energy_efold_time,
    phase_averaged_damped_breather_action,
    phase_averaged_damped_breather_energy,
    phase_averaged_damped_breather_frequency,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-26/"
    "bridge_LB1_dissipative_lifetime.py"
)
LB2 = SOURCE.with_name("bridge_LB2_coherence_threshold.py")
LB3 = SOURCE.with_name("bridge_LB3_damped_sg_ringdown.py")
LB4 = SOURCE.with_name("bridge_LB4_thermal_decoherence_gwindow.py")
LIFETIME_KERNEL = Path("/home/dan/substrate/engineering/lifetime_kernel.py")
NUCLEATION = LIFETIME_KERNEL.with_name("nucleation_efficiency_model.py")
DBD_PIPELINE = LIFETIME_KERNEL.parent / "dbd" / "pipeline.py"

SOURCE_SHA256 = "d2e36e0d9d8ff831bcd58efb264b68dc156f7f87eca7a104f53a6f287eed2b80"
LB2_SHA256 = "ae159aee3c076c1f86d77628a6bbbf206ad7e28dccd832e397250b71a981b28d"
LB3_SHA256 = "1b54ef5704fce1502464f44bd675c01824cfa48b6b98688b1df8f000d1030a2b"
LB4_SHA256 = "e33361e6985002e76342203716fd00ca72c22f905590825a6c064fe472b0d103"
LIFETIME_KERNEL_SHA256 = "51bd4f46593363ac37d99b4e95ca0bef1b572a3b075505968adf77404db4cac5"
NUCLEATION_SHA256 = "bad798b39d850ecf92a97e25bfb0341ef7ae80b036c26a88037efdd618d8d3b8"
DBD_PIPELINE_SHA256 = "5354b39d3bc25439a7f6e83c175474358b3104b2f844cc6aa3a2ee2a84439669"
CONTRACT_SHA256 = "9c5299c34c662998543608a953aa5d3e4f8968ecc1e771cb7c13328c480a4863"
FREEZE_SHA256 = "88bfabda080f1543a4a5e444b98d885c750b4a93dd708f011099027daa2aa5af"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P091-lb1-dissipative-breather-lifetime"),
        Path("proposals/P091-lb1-dissipative-breather-lifetime"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P091")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("LB1 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check(
        "direct bridge consumers are hash pinned",
        _sha256(LB2) == LB2_SHA256
        and _sha256(LB3) == LB3_SHA256
        and _sha256(LB4) == LB4_SHA256,
    )
    checks.check(
        "engineering consumers are hash pinned",
        _sha256(LIFETIME_KERNEL) == LIFETIME_KERNEL_SHA256
        and _sha256(NUCLEATION) == NUCLEATION_SHA256
        and _sha256(DBD_PIPELINE) == DBD_PIPELINE_SHA256,
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
        "source has twenty-two literal sites and a twenty-seven-check runtime path",
        len(literal_checks) == 22
        and "for omv in omega_table:" in source_text
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    imported_modules = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "source imports no accepted damping-to-material or consumer map",
        imported_modules == {"sys", "sympy", "mpmath"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body),
    )

    omega = sp.symbols("omega", positive=True, real=True)
    exact_mean_kinetic = 16 * omega * sp.acos(omega)
    exact_form_factor = omega * sp.acos(omega) / sp.sqrt(1 - omega**2)
    checks.check(
        "canonical action gives the exact undamped mean kinetic integral",
        sp.simplify(
            breather_mean_kinetic_integral(omega) - exact_mean_kinetic
        )
        == 0
        and sp.simplify(
            breather_mean_kinetic_integral(omega)
            - omega * breather_action(omega)
        )
        == 0,
    )
    checks.check(
        "closed form replaces the source nested form-factor quadrature",
        sp.simplify(breather_damping_form_factor(omega) - exact_form_factor) == 0,
    )

    source_table = {
        sp.Rational(999, 1000): sp.Float("0.999333"),
        sp.Rational(9, 10): sp.Float("0.931254"),
        sp.Rational(7, 10): sp.Float("0.779647"),
        sp.Rational(1, 2): sp.Float("0.604600"),
        sp.Rational(3, 10): sp.Float("0.398171"),
        sp.Rational(1, 10): sp.Float("0.147804"),
    }
    checks.check(
        "exact form factor reproduces every printed source value",
        all(
            abs(float(sp.N(breather_damping_form_factor(point), 30)) - float(value))
            < 5.1e-7
            for point, value in source_table.items()
        ),
    )
    checks.check(
        "working-point form factor is pi over four",
        breather_damping_form_factor(1 / sp.sqrt(2)) == sp.pi / 4,
    )

    theta = sp.symbols("theta", positive=True, real=True)
    theta_form_factor = theta / sp.tan(theta)
    monotonicity_numerator = sp.simplify(
        sp.diff(theta_form_factor, theta) * sp.sin(theta) ** 2
    )
    checks.check(
        "form factor has exact endpoint limits",
        sp.limit(theta_form_factor, theta, 0, dir="+") == 1
        and sp.limit(theta_form_factor, theta, sp.pi / 2, dir="-") == 0,
    )
    checks.check(
        "form factor is strictly decreasing with action angle",
        sp.simplify(
            monotonicity_numerator - (sp.sin(theta) * sp.cos(theta) - theta)
        )
        == 0
        and sp.simplify(
            sp.diff(theta - sp.sin(theta) * sp.cos(theta), theta)
            - 2 * sp.sin(theta) ** 2
        )
        == 0,
    )
    checks.check(
        "small-action correction is not identically zero",
        sp.series(theta_form_factor, theta, 0, 6)
        == 1 - theta**2 / 3 - theta**4 / 45 + sp.Order(theta**6),
    )
    checks.mutation_sensitive(
        "kinetic normalization is load bearing",
        lambda factor: sp.simplify(
            factor * breather_mean_kinetic_integral(sp.Rational(3, 5))
            - sp.Rational(48, 5) * sp.acos(sp.Rational(3, 5))
        )
        == 0,
        1,
        (sp.Rational(1, 2), 2),
    )

    gamma, time = sp.symbols("Gamma t", positive=True, real=True)
    omega_initial = 1 / sp.sqrt(2)
    action = phase_averaged_damped_breather_action(
        omega_initial,
        gamma,
        time,
    )
    frequency = phase_averaged_damped_breather_frequency(
        omega_initial,
        gamma,
        time,
    )
    energy = phase_averaged_damped_breather_energy(
        omega_initial,
        gamma,
        time,
    )
    checks.check(
        "phase-averaged action satisfies its conditional ODE and zero-loss limit",
        sp.simplify(sp.diff(action, time) + gamma * action) == 0
        and action.subs(gamma, 0) == 4 * sp.pi,
    )
    checks.check(
        "reduced frequency rises while energy follows the nonlinear action map",
        frequency == sp.cos(sp.pi * sp.exp(-gamma * time) / 4)
        and energy == 16 * sp.sin(sp.pi * sp.exp(-gamma * time) / 4)
        and sp.simplify(
            sp.diff(frequency, time)
            - sp.pi
            * gamma
            * sp.exp(-gamma * time)
            * sp.sin(sp.pi * sp.exp(-gamma * time) / 4)
            / 4
        )
        == 0
        and sp.diff(frequency, time).subs({gamma: 1, time: 1}).is_positive,
    )
    checks.check(
        "reduced energy balance uses the evolving mean kinetic integral",
        sp.simplify(sp.diff(energy, time) + gamma * frequency * action) == 0,
    )

    instantaneous_time = breather_instantaneous_energy_decay_time(
        omega_initial,
        gamma,
    )
    integrated_efold_time = phase_averaged_breather_energy_efold_time(
        omega_initial,
        gamma,
    )
    checks.check(
        "source full-amplitude formula is the initial tangent time",
        instantaneous_time == 4 / (sp.pi * gamma)
        and sp.simplify(
            -breather_energy(omega_initial)
            / sp.diff(energy, time).subs(time, 0)
            - instantaneous_time
        )
        == 0,
    )
    checks.check(
        "integrated energy e-fold time solves the actual reduced crossing",
        sp.simplify(
            phase_averaged_damped_breather_energy(
                omega_initial,
                gamma,
                integrated_efold_time,
            )
            - breather_energy(omega_initial) / sp.E
        )
        == 0,
    )
    checks.check(
        "finite-amplitude tangent and integrated e-fold times differ",
        abs(
            float(sp.N(instantaneous_time.subs(gamma, 1), 30))
            - float(sp.N(integrated_efold_time.subs(gamma, 1), 30))
        )
        > 0.1,
    )
    checks.mutation_sensitive(
        "the e-fold check distinguishes the evolving law from frozen D",
        lambda candidate_time: abs(
            float(
                sp.N(
                    (
                        energy.subs(time, candidate_time)
                        / breather_energy(omega_initial)
                        - sp.exp(-1)
                    ).subs(gamma, 1),
                    30,
                )
            )
        )
        < 1e-12,
        integrated_efold_time,
        (instantaneous_time, 1 / gamma),
    )
    checks.check(
        "small-action energy e-fold tends to one over Gamma",
        sp.limit(
            gamma * phase_averaged_breather_energy_efold_time(omega, gamma),
            omega,
            1,
            dir="-",
        )
        == 1,
    )

    time_dimension, rate_dimension = sp.symbols("d_t d_Gamma")
    checks.check(
        "normalized trajectory fixes Gamma as inverse time but no physical map",
        sp.solve(sp.Eq(rate_dimension + time_dimension, 0), rate_dimension)
        == [-time_dimension]
        and "n*sigma" not in source_text
        and "cross-section" not in source_text,
    )
    checks.check(
        "LB2 consumes only the valid small-amplitude lifetime convention",
        "small-amplitude" in LB2.read_text(encoding="utf-8")
        and "tau = 1 / Gamma" in LB2.read_text(encoding="utf-8"),
    )
    checks.check(
        "LB3 distinguishes the instantaneous current-frequency rate",
        "instantaneous energy e-folding rate" in LB3.read_text(encoding="utf-8")
        and "CURRENT frequency" in LB3.read_text(encoding="utf-8"),
    )
    checks.check(
        "engineering kernel globalizes the small-amplitude exponential",
        "dE_b/dt = -Gamma E_b" in LIFETIME_KERNEL.read_text(encoding="utf-8")
        and "AMPLITUDE ~ exp(-Gamma t/2)" in LIFETIME_KERNEL.read_text(encoding="utf-8"),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
