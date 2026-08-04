"""Primary exact and source-ceiling verifier for P133/T2C."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.collective_dynamics import (
    slow_optical_collective_acceleration,
    slow_optical_profile_width_correction,
)
from substrate_framework.optical_geometry import (
    optical_metric_1d,
    optical_ricci_scalar_1d,
)
from substrate_framework.sine_gordon import breather_energy_second_moment
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path("campaigns/P133-t2c-tidal-mpd-audit")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-2/"
    "bridge_T2C_tidal_MP.py"
)
SOURCE_SHA = "651fd75287dd25b5c34208ea5789df89be50f5050ec139ae2d99f4962440c369"
DOSSIER = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-2/dossiers/"
    "T2C-dossier.md"
)
DOSSIER_SHA = "45708ca99880207c5da6dfcfc1bef2e6d6f7f3ec8d5b99055f7ae795dfaacb66"
PHASE3 = Path(
    "/home/dan/substrate/soliton-shadow/cut-and-project-shadow/sympy/"
    "phase3_finite_size_correction.py"
)
PHASE3_SHA = "19738d784a86b1ce4831d2ee1133154fd58d33b60b28e3c12cf62885a8efd7f4"
NOTE11 = Path(
    "/home/dan/substrate/soliton-shadow/cut-and-project-shadow/"
    "11-stochastic-periodic-background.md"
)
NOTE11_SHA = "4d28b7a42f730a2ee476050095cc14d5c4a50592b1b2edd685e7d1514e1b6fcf"
FREEZE_SHA = "5e404c5d159f4ada91d3db0ed1547bddb6208729554c10854bfec53f56c5af4e"


def source_check_calls(tree: ast.AST) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]


def imported_modules(tree: ast.AST) -> set[str]:
    modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    modules.update(
        node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    )
    return modules


def assigned_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for target in targets:
            if isinstance(target, ast.Name):
                names.add(target.id)
    return names


def connection_and_riemann(
    metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]
) -> tuple[list[list[list[sp.Expr]]], object]:
    dimension = len(coordinates)
    inverse = metric.inv()
    gamma = [
        [[sp.Integer(0) for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for rho in range(dimension):
        for mu in range(dimension):
            for nu in range(dimension):
                gamma[rho][mu][nu] = sp.simplify(
                    sum(
                        inverse[rho, sigma]
                        * (
                            sp.diff(metric[sigma, nu], coordinates[mu])
                            + sp.diff(metric[sigma, mu], coordinates[nu])
                            - sp.diff(metric[mu, nu], coordinates[sigma])
                        )
                        for sigma in range(dimension)
                    )
                    / 2
                )

    def riemann(rho: int, sigma: int, mu: int, nu: int) -> sp.Expr:
        value = sp.diff(gamma[rho][nu][sigma], coordinates[mu]) - sp.diff(
            gamma[rho][mu][sigma], coordinates[nu]
        )
        value += sum(
            gamma[rho][mu][lam] * gamma[lam][nu][sigma]
            - gamma[rho][nu][lam] * gamma[lam][mu][sigma]
            for lam in range(dimension)
        )
        return sp.simplify(value)

    return gamma, riemann


def main() -> int:
    checks = CheckLedger("T2C-TIDAL-MPD-AUDIT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    phase3_bytes = PHASE3.read_bytes()
    phase3_text = phase3_bytes.decode("utf-8")

    checks.check(
        "T2C source bytes are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    checks.check(
        "T2C dossier bytes are separately hash pinned",
        hashlib.sha256(DOSSIER.read_bytes()).hexdigest() == DOSSIER_SHA,
    )
    checks.check(
        "phase-three kernel source and note are hash pinned",
        hashlib.sha256(phase3_bytes).hexdigest() == PHASE3_SHA
        and hashlib.sha256(NOTE11.read_bytes()).hexdigest() == NOTE11_SHA,
    )
    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: active\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "immutable preregistration remains byte identical",
        hashlib.sha256(
            (CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    checks.check(
        "thirteen source predicates match the terminal tally",
        len(source_check_calls(tree)) == 13,
    )
    checks.check(
        "the executable import surface is SymPy only",
        imported_modules(tree) == {"sympy"},
    )
    checks.check(
        "T2C has no NumPy compatibility event",
        all(
            token not in source_text
            for token in ("np.trapz", "np.trapezoid", "trapezoid_integral", "numpy")
        ),
    )

    t, x = sp.symbols("t x", real=True)
    c0 = sp.symbols("c0", positive=True)
    n = sp.Function("n", positive=True)(x)
    metric = optical_metric_1d(n, c0)
    gamma, riemann = connection_and_riemann(metric, (t, x))
    n_x = sp.diff(n, x)
    n_xx = sp.diff(n, x, 2)
    expected_r1001 = c0**2 * (n * n_xx / 2 - n_x**2) / n**4
    r1001 = riemann(1, 0, 0, 1)
    r1010 = riemann(1, 0, 1, 0)
    checks.check(
        "fresh connection has the fixed nonzero optical components",
        sp.simplify(gamma[0][0][1] + n_x / (2 * n)) == 0
        and sp.simplify(gamma[1][0][0] + c0**2 * n_x / (2 * n**3)) == 0
        and sp.simplify(gamma[1][1][1] - n_x / (2 * n)) == 0,
    )
    checks.check(
        "fresh Riemann component agrees with the source geometry",
        sp.simplify(r1001 - expected_r1001) == 0,
    )
    checks.check(
        "last-slot antisymmetry fixes the companion component",
        sp.simplify(r1010 + r1001) == 0,
    )
    ricci_scalar = optical_ricci_scalar_1d(n, x, c0)
    checks.check(
        "accepted scalar curvature reproduces the fresh component",
        sp.simplify(r1001 - ricci_scalar / (2 * n)) == 0,
    )
    checks.mutation_sensitive(
        "Riemann sign and coefficient",
        lambda candidate: sp.simplify(candidate - expected_r1001) == 0,
        expected_r1001,
        [-expected_r1001, c0**2 * (n * n_xx - n_x**2) / n**4],
    )

    k = sp.symbols("k", real=True)
    m0, m1, m2, m3, m4 = sp.symbols("m0 m1 m2 m3 m4", real=True)
    transform_jet = m0 - sp.I * m1 * k - m2 * k**2 / 2 + sp.I * m3 * k**3 / 6 + m4 * k**4 / 24
    checks.check(
        "Fourier second derivative is the signed raw second moment",
        sp.simplify(-sp.diff(transform_jet, k, 2).subs(k, 0) - m2) == 0,
    )
    checks.check(
        "centering removes the first derivative but does not define a force",
        sp.simplify(sp.diff(transform_jet, k).subs({k: 0, m1: 0})) == 0,
    )
    checks.mutation_sensitive(
        "Fourier derivative order and sign",
        lambda candidate: sp.simplify(candidate - m2) == 0,
        -sp.diff(transform_jet, k, 2).subs(k, 0),
        [sp.diff(transform_jet, k, 2).subs(k, 0), -sp.diff(transform_jet, k, 4).subs(k, 0)],
    )
    exact_kernel_mass = 4 * sp.sqrt(2)
    exact_kernel_second_moment = sp.sqrt(2) * sp.pi**2
    checks.check(
        "phase-three decimal moments have exact normalized relation",
        sp.simplify(
            exact_kernel_second_moment / exact_kernel_mass - sp.pi**2 / 4
        )
        == 0,
    )
    accepted_hamiltonian_minimum = breather_energy_second_moment(
        1 / sp.sqrt(2), sp.Integer(0)
    )
    checks.check(
        "the phase-three coupling moment is not C-SG-009's Hamiltonian moment",
        sp.simplify(accepted_hamiltonian_minimum - exact_kernel_second_moment) != 0,
    )
    checks.check(
        "phase-three source uses current NumPy trapezoid API",
        "np.trapezoid" in phase3_text and "np.trapz" not in phase3_text,
    )
    checks.check(
        "phase-three derivation states the first width correction uses the third background derivative",
        "correction couples to the THIRD derivative xi'''(X)" in phase3_text
        and "correction starts at xi'''" in phase3_text,
    )

    normalized_width = sp.symbols("sigma2", positive=True)
    point_acceleration = slow_optical_collective_acceleration(x, n, c0)
    second_derivative = sp.simplify(sp.diff(point_acceleration, x, 2))
    expected_second_derivative = c0**2 * (
        sp.diff(n, x, 3) / n**3
        - 9 * n_x * n_xx / n**4
        + 12 * n_x**3 / n**5
    ) / 2
    checks.check(
        "Taylor averaging derives the normalized leading width correction",
        sp.simplify(second_derivative - expected_second_derivative) == 0,
    )
    averaged_correction = sp.simplify(normalized_width * second_derivative / 2)
    checks.check(
        "canonical profile-width API returns the derived second-order term",
        sp.simplify(
            slow_optical_profile_width_correction(
                x, n, c0, normalized_width
            )
            - averaged_correction
        )
        == 0,
    )
    epsilon = sp.symbols("epsilon", real=True)
    profile_shape = sp.Function("xi", real=True)(x)
    weak_profile = 1 + epsilon * profile_shape
    weak_point_acceleration = slow_optical_collective_acceleration(
        x, weak_profile, c0
    )
    weak_average = sp.simplify(
        normalized_width * sp.diff(weak_point_acceleration, x, 2) / 2
    )
    weak_t2c = sp.simplify(
        normalized_width
        * optical_ricci_scalar_1d(weak_profile, x, c0)
        / (2 * weak_profile)
    )
    checks.check(
        "linear finite-width response uses xi triple prime",
        sp.simplify(
            sp.diff(weak_average, epsilon).subs(epsilon, 0)
            - c0**2 * normalized_width * sp.diff(profile_shape, x, 3) / 4
        )
        == 0,
    )
    checks.check(
        "T2C instead uses xi double prime at linear order",
        sp.simplify(
            sp.diff(weak_t2c, epsilon).subs(epsilon, 0)
            - c0**2 * normalized_width * sp.diff(profile_shape, x, 2) / 2
        )
        == 0,
    )
    checks.check(
        "source curvature coupling differs from the derived averaged acceleration",
        sp.simplify(
            sp.diff(weak_average - weak_t2c, epsilon).subs(epsilon, 0)
        )
        != 0,
    )
    checks.mutation_sensitive(
        "finite-width derivative order",
        lambda derivative_order: derivative_order == 3,
        3,
        [2, 1, 0],
    )

    beta = sp.symbols("beta", positive=True)
    even_profile = 1 + beta * x**2 / 2
    even_point_acceleration = slow_optical_collective_acceleration(
        x, even_profile, c0
    )
    even_average_correction = sp.simplify(
        normalized_width * sp.diff(even_point_acceleration, x, 2) / 2
    )
    even_t2c = sp.simplify(
        normalized_width
        * optical_ricci_scalar_1d(even_profile, x, c0)
        / (2 * even_profile)
    )
    checks.check(
        "reflection-symmetric profile has odd point acceleration",
        sp.simplify(even_point_acceleration.subs(x, -x) + even_point_acceleration)
        == 0,
    )
    checks.check(
        "Taylor-averaged correction respects the symmetry center",
        sp.simplify(even_average_correction.subs(x, 0)) == 0,
    )
    checks.check(
        "T2C predicts a forbidden nonzero acceleration at the symmetry center",
        sp.simplify(
            even_t2c.subs(x, 0) - c0**2 * beta * normalized_width / 2
        )
        == 0,
    )
    linear_profile = 1 + epsilon * x
    linear_average = sp.simplify(
        normalized_width
        * sp.diff(
            slow_optical_collective_acceleration(x, linear_profile, c0), x, 2
        )
        / 2
    )
    linear_t2c = sp.simplify(
        normalized_width
        * optical_ricci_scalar_1d(linear_profile, x, c0)
        / (2 * linear_profile)
    )
    checks.check(
        "linear profile separates cubic averaged response from quadratic T2C response",
        sp.simplify(
            linear_average.subs(x, 0)
            - 3 * c0**2 * epsilon**3 * normalized_width
        )
        == 0
        and sp.simplify(
            linear_t2c.subs(x, 0)
            + c0**2 * epsilon**2 * normalized_width
        )
        == 0,
    )

    curvature_dimension = (0, -2)
    width_dimension = (2, 0)
    acceleration_dimension = (1, -2)
    curvature_width_dimension = tuple(
        left + right
        for left, right in zip(curvature_dimension, width_dimension, strict=True)
    )
    gradient_curvature_width_dimension = (
        curvature_width_dimension[0] - 1,
        curvature_width_dimension[1],
    )
    checks.check(
        "curvature times normalized width is not an acceleration dimension",
        curvature_width_dimension == (2, -2)
        and curvature_width_dimension != acceleration_dimension,
    )
    checks.check(
        "a curvature gradient times normalized width closes acceleration units",
        gradient_curvature_width_dimension == acceleration_dimension,
    )

    external = yaml.safe_load(
        (CAMPAIGN / "evidence/external-provenance.yaml").read_text()
    )
    displayed = next(
        item["displayed_equation"]
        for item in external["sources"]
        if item.get("displayed_equation")
    )
    checks.check(
        "primary MPD provenance records the curvature-gradient rank-four term",
        "nabla_a R_bcde J^bcde" in displayed
        and "-(1/6)" in displayed,
    )
    r01, j00, j01, j11 = sp.symbols("R01 J00 J01 J11", real=True)
    antisymmetric_curvature_slots = sp.Matrix([[0, r01], [-r01, 0]])
    symmetric_rank_two_moment = sp.Matrix([[j00, j01], [j01, j11]])
    symmetric_contraction = sp.simplify(
        sum(
            antisymmetric_curvature_slots[a, b]
            * symmetric_rank_two_moment[a, b]
            for a in range(2)
            for b in range(2)
        )
    )
    checks.check(
        "a symmetric rank-two moment cannot replace spin in the antisymmetric slots",
        symmetric_contraction == 0,
    )
    names = assigned_names(tree)
    checks.check(
        "T2C executes no typed MPD momentum spin or rank-four quadrupole object",
        all(name not in names for name in ("p", "u", "S", "J", "J4", "nabla_R")),
    )
    checks.check(
        "T2C's displayed component and J11 do not share contracted slot labels",
        "R^1_{010}*J^{11}" in source_text
        and "J^{11} = -w~''(0)" in source_text,
    )
    curvature_gradient_center = sp.simplify(
        sp.diff(optical_ricci_scalar_1d(even_profile, x, c0), x).subs(x, 0)
    )
    checks.check(
        "the symmetric-center curvature gradient vanishes while T2C remains nonzero",
        curvature_gradient_center == 0 and sp.simplify(even_t2c.subs(x, 0)) != 0,
    )

    arbitrary_coefficient = sp.symbols("A", nonzero=True)
    source_point_guard = sp.simplify(ricci_scalar * normalized_width / (2 * n))
    alternative_point_guard = sp.simplify(
        arbitrary_coefficient * ricci_scalar * normalized_width / n**2
    )
    checks.check(
        "the point-limit guard accepts inequivalent unproved couplings",
        source_point_guard.subs(normalized_width, 0) == 0
        and alternative_point_guard.subs(normalized_width, 0) == 0
        and sp.simplify(source_point_guard - alternative_point_guard) != 0,
    )
    checks.check(
        "nonzero and linear source predicates are true only by construction",
        sp.diff(source_point_guard, normalized_width, 2) == 0
        and sp.simplify(source_point_guard.subs(normalized_width, 1)) != 0,
    )
    checks.check(
        "T2C annotation cannot import rejected predecessor ceilings",
        "SINCE DONE by Phase-13's FS1+FS4" in source_text
        and "Phase-14's P3D3 then solving" in source_text,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
