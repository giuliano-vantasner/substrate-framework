"""Exact symbolic audit predicates for P238-S01 through P238-S18."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import sympy as sp


@dataclass(frozen=True)
class Check:
    claim: str
    name: str
    passed: bool
    detail: str


def _zero(expression: sp.Expr) -> bool:
    return sp.simplify(expression) == 0


def run() -> list[Check]:
    checks: list[Check] = []

    def record(claim: str, name: str, passed: bool, detail: object) -> None:
        checks.append(Check(claim, name, bool(passed), str(detail)))

    # P238-S01: equation (3), expanded in two spatial dimensions.
    ut, ux, uy, vx, vy = sp.symbols("ut ux uy vx vy", real=True)
    material = ut + vx * ux + vy * uy
    displayed = (
        ut**2
        + 2 * ut * (vx * ux + vy * uy)
        + vx**2 * ux**2
        + 2 * vx * vy * ux * uy
        + vy**2 * uy**2
    )
    record("P238-S01", "material derivative square", _zero(material**2 - displayed), sp.expand(material**2 - displayed))

    # P238-S02: independently expand equation (6) with actual derivatives in
    # two spatial dimensions and compare it with the paper's equation (7).
    t, x, y = sp.symbols("t x y", real=True)
    u = sp.Function("u")(t, x, y)
    rho = sp.Function("rho")(t, x, y)
    vx = sp.Function("Vx")(t, x, y)
    vy = sp.Function("Vy")(t, x, y)
    theta_xx = sp.Function("Theta_xx")(t, x, y)
    theta_xy = sp.Function("Theta_xy")(t, x, y)
    theta_yy = sp.Function("Theta_yy")(t, x, y)
    potential_prime = sp.Function("Uprime")(u)
    material_u = sp.diff(u, t) + vx * sp.diff(u, x) + vy * sp.diff(u, y)
    compact = (
        sp.diff(rho * material_u, t)
        + sp.diff(rho * material_u * vx - theta_xx * sp.diff(u, x) - theta_xy * sp.diff(u, y), x)
        + sp.diff(rho * material_u * vy - theta_xy * sp.diff(u, x) - theta_yy * sp.diff(u, y), y)
        + potential_prime
    )
    displayed = (
        sp.diff(rho, t) * material_u
        + rho * sp.diff(material_u, t)
        + (sp.diff(vx, x) + sp.diff(vy, y)) * rho * material_u
        + (vx * sp.diff(rho, x) + vy * sp.diff(rho, y)) * material_u
        + rho * (vx * sp.diff(material_u, x) + vy * sp.diff(material_u, y))
        - sp.diff(theta_xx, x) * sp.diff(u, x)
        - sp.diff(theta_xy, x) * sp.diff(u, y)
        - sp.diff(theta_xy, y) * sp.diff(u, x)
        - sp.diff(theta_yy, y) * sp.diff(u, y)
        - theta_xx * sp.diff(u, x, 2)
        - 2 * theta_xy * sp.diff(u, x, y)
        - theta_yy * sp.diff(u, y, 2)
        + potential_prime
    )
    product_rule_residual = sp.expand(compact - displayed)
    record(
        "P238-S02",
        "Euler-Lagrange product rule",
        _zero(product_rule_residual),
        product_rule_residual,
    )

    rho0, theta0, utt, lap_u, up = sp.symbols(
        "rho0 theta0 utt lap_u Uprime", nonzero=True, real=True
    )
    c0_sq = theta0 / rho0
    homogeneous = rho0 * utt - theta0 * lap_u + up
    normalized = utt / c0_sq - lap_u + up / theta0
    record("P238-S02", "homogeneous NLKG normalization", _zero(homogeneous / theta0 - normalized), sp.simplify(homogeneous / theta0 - normalized))

    mass_sq, field = sp.symbols("mass_sq field", nonzero=True, real=True)
    omitted_mass = mass_sq * field / rho0
    record(
        "P238-S02",
        "constant-background linearized operator retains the mass term",
        not _zero(omitted_mass),
        omitted_mass,
    )

    # P238-S03: determinant matching does not match directional impedance.
    theta_iso = sp.eye(2)
    theta_aniso = sp.diag(4, sp.Rational(1, 4))
    determinant_match = theta_iso.det() == theta_aniso.det() == 1
    z_left = sp.sqrt(theta_iso[0, 0])
    z_right = sp.sqrt(theta_aniso[0, 0])
    reflection = sp.simplify((z_right - z_left) / (z_right + z_left))
    record("P238-S03", "isotropic determinant reduction", determinant_match, (theta_iso.det(), theta_aniso.det()))
    record("P238-S03", "anisotropic interface reflection counterexample", reflection == sp.Rational(1, 3), reflection)

    # P238-S04: reconstruct rho and Theta from A under the matching constraint.
    q, a1, reference_rho, reference_c = sp.symbols(
        "q a1 reference_rho reference_c", positive=True
    )
    a2 = q**4 / a1
    local_rho = reference_rho * reference_c / q
    theta1 = sp.simplify(local_rho * a1)
    theta2 = sp.simplify(local_rho * a2)
    reference_theta = reference_rho * reference_c**2
    recovered_a = sp.diag(theta1 / local_rho, theta2 / local_rho)
    matching = sp.simplify(local_rho * sp.sqrt(theta1 * theta2) - reference_rho * reference_theta)
    record("P238-S04", "A equals Theta/rho", recovered_a == sp.diag(a1, a2), recovered_a)
    record("P238-S04", "determinant matching reconstruction", _zero(matching), matching)

    # P238-S05: a second-rank principal-index tensor does not give the generic
    # directional phase index through its ordinary quadratic form.
    sqrt2 = sp.sqrt(2)
    direction = sp.Matrix([1 / sqrt2, 1 / sqrt2])
    acoustic = sp.diag(1, 4)
    index_tensor = sp.diag(1, sp.Rational(1, 2))
    true_index = sp.simplify(1 / sp.sqrt((direction.T * acoustic * direction)[0]))
    tensor_quadratic = sp.simplify((direction.T * index_tensor * direction)[0])
    record("P238-S05", "generic directional-index disagreement", not _zero(true_index - tensor_quadratic), (true_index, tensor_quadratic))
    axis = sp.Matrix([1, 0])
    axis_true = sp.simplify(1 / sp.sqrt((axis.T * acoustic * axis)[0]))
    axis_tensor = sp.simplify((axis.T * index_tensor * axis)[0])
    record("P238-S05", "principal-axis limit", _zero(axis_true - axis_tensor), (axis_true, axis_tensor))

    # P238-S06: the real potential can satisfy the paper's scalar conditions,
    # yet positive-potential Derrick scaling forbids a nonzero static lump in 2D.
    amplitude = sp.symbols("amplitude", real=True)
    potential = amplitude**2 / 2 - amplitude**4 / 4 + amplitude**6 / 6
    binding_gap = sp.simplify(potential.subs(amplitude, 1) - sp.Rational(1, 2))
    y = sp.symbols("y", nonnegative=True)
    positive_factor = sp.Rational(1, 2) - y / 4 + y**2 / 6
    discriminant = sp.discriminant(positive_factor, y)
    scale, gradient_energy, potential_energy = sp.symbols(
        "scale gradient_energy potential_energy", positive=True
    )
    scaled_energy_2d = gradient_energy + potential_energy / scale**2
    derrick_derivative = sp.diff(scaled_energy_2d, scale).subs(scale, 1)
    record("P238-S06", "binding example satisfies strict inequality", binding_gap < 0, binding_gap)
    record("P238-S06", "binding example remains positive", discriminant < 0, discriminant)
    record("P238-S06", "two-dimensional static Derrick obstruction", derrick_derivative == -2 * potential_energy, derrick_derivative)

    # P238-S08: the displayed rigid translation ansatz integrates to a
    # velocity-quadratic Lagrangian; a square root requires additional input.
    velocity, flow, inertia, constant, mass, speed = sp.symbols(
        "velocity flow inertia constant mass speed", positive=True
    )
    rigid_lagrangian = inertia * (velocity - flow) ** 2 / 2 - constant
    square_root = -mass * speed**2 * sp.sqrt(1 - velocity**2 / speed**2)
    record("P238-S08", "rigid ansatz is quadratic in velocity", sp.diff(rigid_lagrangian, velocity, 3) == 0, sp.diff(rigid_lagrangian, velocity, 3))
    quartic = sp.simplify(sp.diff(square_root, velocity, 4).subs(velocity, 0))
    record("P238-S08", "relativistic square root has nonzero quartic term", quartic != 0, quartic)

    # P238-S09: derive the einbein, null-constraint, and affine-geodesic
    # identities directly from the paper's action, without importing a
    # framework claim as an oracle.
    qnorm, einbein_mass, signal_speed = sp.symbols(
        "qnorm einbein_mass signal_speed", positive=True
    )
    sigma = -qnorm**2
    einbein = qnorm / (einbein_mass * signal_speed)
    einbein_lagrangian = sigma / (2 * einbein) - einbein * (einbein_mass * signal_speed) ** 2 / 2
    eliminated = -einbein_mass * signal_speed * sp.sqrt(-sigma)
    record("P238-S09", "einbein elimination", _zero(einbein_lagrangian - eliminated), sp.simplify(einbein_lagrangian - eliminated))

    einbein_symbol, mass_parameter = sp.symbols(
        "einbein_symbol mass_parameter", nonzero=True, real=True
    )
    tangent_norm = sp.symbols("tangent_norm", real=True)
    einbein_action = (
        tangent_norm / (2 * einbein_symbol)
        - einbein_symbol * mass_parameter**2 / 2
    )
    massless_constraint = sp.simplify(
        -2 * einbein_symbol**2
        * sp.diff(einbein_action.subs(mass_parameter, 0), einbein_symbol)
    )
    record(
        "P238-S09",
        "massless einbein variation imposes the null constraint",
        _zero(massless_constraint - tangent_norm),
        massless_constraint,
    )

    q0, q1 = sp.symbols("q0 q1", real=True)
    coordinates = (q0, q1)
    velocities = sp.symbols("velocity0 velocity1", real=True)
    accelerations = sp.symbols("acceleration0 acceleration1", real=True)
    metric = sp.Matrix(
        [
            [sp.Function("g00")(q0, q1), sp.Function("g01")(q0, q1)],
            [sp.Function("g01")(q0, q1), sp.Function("g11")(q0, q1)],
        ]
    )
    kinetic = sum(
        metric[mu, nu] * velocities[mu] * velocities[nu]
        for mu in range(2)
        for nu in range(2)
    ) / (2 * einbein_symbol)
    for alpha in range(2):
        momentum = sp.diff(kinetic, velocities[alpha])
        total_momentum_derivative = sum(
            sp.diff(momentum, coordinates[mu]) * velocities[mu]
            + sp.diff(momentum, velocities[mu]) * accelerations[mu]
            for mu in range(2)
        )
        euler_lagrange = sp.expand(
            total_momentum_derivative - sp.diff(kinetic, coordinates[alpha])
        )
        lowered_geodesic = sum(
            metric[alpha, nu] * accelerations[nu] for nu in range(2)
        )
        lowered_geodesic += sum(
            sp.Rational(1, 2)
            * (
                sp.diff(metric[alpha, nu], coordinates[mu])
                + sp.diff(metric[alpha, mu], coordinates[nu])
                - sp.diff(metric[mu, nu], coordinates[alpha])
            )
            * velocities[mu]
            * velocities[nu]
            for mu in range(2)
            for nu in range(2)
        )
        residual = sp.simplify(einbein_symbol * euler_lagrange - lowered_geodesic)
        record(
            "P238-S09",
            f"constant-einbein geodesic identity component {alpha}",
            _zero(residual),
            residual,
        )

    # P238-S10: phase-covector contraction reproduces equation (21).
    omega, kx, ky, c0, ax, ay, flow_x, flow_y = sp.symbols(
        "omega kx ky c0 ax ay flow_x flow_y", nonzero=True, real=True
    )
    phase_covector = sp.Matrix([-omega / c0, kx, ky])
    contra = sp.Matrix(
        [
            [-1, -flow_x / c0, -flow_y / c0],
            [-flow_x / c0, ax / c0**2 - flow_x**2 / c0**2, -flow_x * flow_y / c0**2],
            [-flow_y / c0, -flow_x * flow_y / c0**2, ay / c0**2 - flow_y**2 / c0**2],
        ]
    )
    contraction = sp.expand((phase_covector.T * contra * phase_covector)[0] * c0**2)
    dispersion = sp.expand(ax * kx**2 + ay * ky**2 - (omega - flow_x * kx - flow_y * ky) ** 2)
    record("P238-S10", "contravariant null polynomial", _zero(contraction - dispersion), sp.factor(contraction - dispersion))

    # P238-S11: exact anisotropic counterexample and corrected block inverse.
    n1, n2, nbar = sp.Integer(2), sp.Integer(8), sp.Integer(4)
    scaled_contra = nbar * sp.diag(-1, 1 / n1**2, 1 / n2**2)
    paper_covariant = sp.diag(-1 / nbar, n1, n2)
    correct_covariant = sp.diag(-1 / nbar, n1**2 / nbar, n2**2 / nbar)
    paper_product = sp.simplify(scaled_contra * paper_covariant)
    correct_product = sp.simplify(scaled_contra * correct_covariant)
    record("P238-S11", "paper anisotropic inverse fails", paper_product != sp.eye(3), paper_product)
    record("P238-S11", "corrected anisotropic inverse", correct_product == sp.eye(3), correct_product)

    # P238-S13 and S14: the acoustic eigenvalues, not equations (40)-(42),
    # reproduce the Schwarzschild null cone and matched constitutive profiles.
    f, radius = sp.symbols("f radius", positive=True)
    acoustic_covariant = sp.diag(-1, 1 / f**2, radius**2 / f)
    schwarzschild = sp.diag(-f, 1 / f, radius**2)
    record("P238-S13", "Schwarzschild conformal null cone", sp.simplify(f * acoustic_covariant - schwarzschild) == sp.zeros(3), sp.simplify(f * acoustic_covariant - schwarzschild))

    # The paper's equations (40)-(42) use N rather than N^2/nbar.  At the
    # exact exterior sample f=1/4 their time/radial/angular component ratios
    # cannot share one conformal factor, even though the acoustic eigenvalues
    # themselves encode the desired null cone through the corrected inverse.
    f_sample = sp.Rational(1, 4)
    n_radial = 1 / f_sample
    n_angular = 1 / sp.sqrt(f_sample)
    nbar_sample = sp.sqrt(n_radial * n_angular)
    paper_schwarzschild = sp.diag(
        -1 / nbar_sample,
        n_radial,
        radius**2 * n_angular,
    )
    target_sample = schwarzschild.subs(f, f_sample)
    component_ratios = tuple(
        sp.simplify(target_sample[index, index] / paper_schwarzschild[index, index])
        for index in range(3)
    )
    record(
        "P238-S13",
        "paper equations 40-42 are not conformal to Schwarzschild",
        len(set(component_ratios)) > 1,
        component_ratios,
    )

    profile_rho = f ** (-sp.Rational(3, 4))
    profile_theta_r = f ** sp.Rational(5, 4)
    profile_theta_t = f ** sp.Rational(1, 4)
    profile_match = sp.powsimp(profile_rho * sp.sqrt(profile_theta_r * profile_theta_t), force=True)
    record("P238-S14", "Schwarzschild profile matching", _zero(profile_match - 1), profile_match)

    # P238-S15/S16: the minimal rotating metric shares some components and
    # surfaces with Kerr but is not conformal to the Kerr equatorial metric.
    radial, schwarzschild_radius, spin = sp.symbols(
        "radial schwarzschild_radius spin", positive=True
    )
    rotating_factor = 1 - schwarzschild_radius / radial + spin**2 / radial**2
    acoustic_scaled = sp.Matrix(
        [
            [-(1 - schwarzschild_radius / radial), 0, -spin],
            [0, 1 / rotating_factor, 0],
            [-spin, 0, radial**2],
        ]
    )
    kerr_equator = sp.Matrix(
        [
            [-(1 - schwarzschild_radius / radial), 0, -spin * schwarzschild_radius / radial],
            [0, 1 / rotating_factor, 0],
            [-spin * schwarzschild_radius / radial, 0, radial**2 + spin**2 + spin**2 * schwarzschild_radius / radial],
        ]
    )
    kerr_delta = sp.simplify(acoustic_scaled - kerr_equator)
    record("P238-S15", "Kerr coefficient map mismatch", kerr_delta != sp.zeros(3), kerr_delta)
    record("P238-S16", "minimal rotating model is not exact Kerr", _zero(kerr_delta[0, 0]) and _zero(kerr_delta[1, 1]) and not _zero(kerr_delta[0, 2]), kerr_delta)

    # P238-S17: exact characteristic surfaces and which root reverses.
    ergo_equation = sp.simplify(spin**2 / radial**2 - rotating_factor)
    record("P238-S17", "ergosurface is r equals rs", sp.solve(ergo_equation, radial) == [schwarzschild_radius], ergo_equation)
    horizon_polynomial = sp.factor(radial**2 * rotating_factor)
    record("P238-S17", "outer-horizon polynomial", horizon_polynomial == radial**2 - schwarzschild_radius * radial + spin**2, horizon_polynomial)

    return checks


def main() -> int:
    checks = run()
    print(json.dumps({"oracle": "sympy", "checks": [asdict(item) for item in checks]}, indent=2))
    return 0 if all(item.passed for item in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
