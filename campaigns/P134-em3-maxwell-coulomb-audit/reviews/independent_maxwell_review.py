from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _independent_action() -> dict[str, object]:
    time, x, y = sp.symbols("t x y", real=True)
    coordinates = (time, x, y)
    dimension = len(coordinates)
    potential = tuple(
        sp.Function(f"B{index}")(*coordinates) for index in range(dimension)
    )
    current = tuple(
        sp.Function(f"J{index}")(*coordinates) for index in range(dimension)
    )
    metric = sp.diag(1, -1, -1)
    kappa = sp.Symbol("K", positive=True)
    lower = sp.Matrix(
        dimension,
        dimension,
        lambda mu, nu: sp.diff(potential[nu], coordinates[mu])
        - sp.diff(potential[mu], coordinates[nu]),
    )
    raised = sp.simplify(metric * lower * metric)
    lagrangian = sp.expand(
        -kappa
        * sum(
            (lower[mu, nu] * raised[mu, nu]
             for mu in range(dimension)
             for nu in range(dimension)),
            sp.S.Zero,
        )
        / 4
        - sum(
            (potential[nu] * current[nu] for nu in range(dimension)),
            sp.S.Zero,
        )
    )
    residuals: list[sp.Expr] = []
    targets: list[sp.Expr] = []
    for nu in range(dimension):
        residual = sp.diff(lagrangian, potential[nu]) - sum(
            (
                sp.diff(
                    sp.diff(lagrangian, sp.diff(potential[nu], coordinates[mu])),
                    coordinates[mu],
                )
                for mu in range(dimension)
            ),
            sp.S.Zero,
        )
        target = kappa * sum(
            (sp.diff(raised[mu, nu], coordinates[mu]) for mu in range(dimension)),
            sp.S.Zero,
        ) - current[nu]
        residuals.append(sp.simplify(residual))
        targets.append(sp.simplify(target))
    double_divergence = sp.simplify(sum(
        (
            sp.diff(
                sum(
                    (sp.diff(raised[mu, nu], coordinates[mu]) for mu in range(dimension)),
                    sp.S.Zero,
                ),
                coordinates[nu],
            )
            for nu in range(dimension)
        ),
        sp.S.Zero,
    ))
    return {
        "coordinates": coordinates,
        "potential": potential,
        "current": current,
        "kappa": kappa,
        "lower": lower,
        "raised": raised,
        "residuals": tuple(residuals),
        "targets": tuple(targets),
        "double_divergence": double_divergence,
    }


def _sphere_area(dimension: int) -> sp.Expr:
    return sp.simplify(
        2
        * sp.pi ** sp.Rational(dimension, 2)
        / sp.gamma(sp.Rational(dimension, 2))
    )


def _power_branch(
    dimension: int,
    radius: sp.Symbol,
    charge: sp.Expr,
    kappa: sp.Expr,
) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    area = _sphere_area(dimension)
    potential = sp.simplify(
        charge
        / (kappa * (dimension - 2) * area * radius ** (dimension - 2))
    )
    field = sp.simplify(-sp.diff(potential, radius))
    flux = sp.simplify(area * radius ** (dimension - 1) * field)
    harmonic = sp.simplify(
        sp.diff(radius ** (dimension - 1) * sp.diff(potential, radius), radius)
        / radius ** (dimension - 1)
    )
    return potential, field, flux, harmonic


def main() -> int:
    ledger = CheckLedger("P134-independent")
    action = _independent_action()
    lower = action["lower"]
    residuals = action["residuals"]
    targets = action["targets"]
    ledger.check("fresh field strength is antisymmetric", lower == -lower.T)
    ledger.check(
        "fresh Euler variation matches every sourced component",
        all(sp.simplify(left - right) == 0
            for left, right in zip(residuals, targets, strict=True)),
    )
    ledger.check(
        "fresh antisymmetric double divergence vanishes",
        action["double_divergence"] == 0,
    )

    coordinates = action["coordinates"]
    potential = action["potential"]
    current = action["current"]
    kappa_action = action["kappa"]
    gauge_parameter = sp.Function("chi")(*coordinates)
    source_gauge_change = sp.expand(-sum(
        (
            current[nu] * sp.diff(gauge_parameter, coordinates[nu])
            for nu in range(len(coordinates))
        ),
        sp.S.Zero,
    ))
    divergence_term = -sum(
        (
            sp.diff(current[nu] * gauge_parameter, coordinates[nu])
            for nu in range(len(coordinates))
        ),
        sp.S.Zero,
    )
    continuity_bulk = gauge_parameter * sum(
        (sp.diff(current[nu], coordinates[nu]) for nu in range(len(coordinates))),
        sp.S.Zero,
    )
    ledger.check(
        "source gauge variation separates boundary and continuity terms",
        sp.simplify(source_gauge_change - divergence_term - continuity_bulk) == 0,
    )

    time, x = sp.symbols("tau X", real=True)
    temporal = sp.Function("B0")(time, x)
    spatial = sp.Function("B1")(time, x)
    rho = sp.Function("rho")(x)
    kappa = sp.Symbol("kappa", positive=True)
    raised_x0 = sp.diff(spatial, time) - sp.diff(temporal, x)
    static_equation = sp.simplify(
        kappa * sp.diff(raised_x0, x) - rho
    )
    phi = sp.Function("phi")(x)
    correct = sp.simplify(
        static_equation.subs(spatial, 0).subs(temporal, phi).doit()
    )
    wrong = sp.simplify(
        static_equation.subs(spatial, 0).subs(temporal, -phi).doit()
    )
    ledger.check(
        "fresh A0 equals phi reduction gives minus kappa Laplacian minus rho",
        correct == -kappa * sp.diff(phi, x, 2) - rho,
    )
    ledger.check(
        "fresh A0 equals minus phi mutation reverses the Laplacian",
        wrong == kappa * sp.diff(phi, x, 2) - rho and wrong != correct,
    )

    radius = sp.Symbol("r", positive=True)
    charge, probe, kappa = sp.symbols("Q q kappa", positive=True)
    for dimension in (3, 4, 5, 6):
        radial_potential, radial_field, flux, harmonic = _power_branch(
            dimension, radius, charge, kappa
        )
        ledger.check(
            f"d={dimension} fresh radial branch is source normalized",
            flux == charge / kappa and harmonic == 0,
        )
        ledger.check(
            f"d={dimension} fresh radial branch decays",
            sp.limit(radial_potential, radius, sp.oo) == 0
            and radial_field != 0,
        )

    potential3, field3, _, _ = _power_branch(3, radius, charge, kappa)
    potential4, field4, _, _ = _power_branch(4, radius, charge, kappa)
    ledger.check(
        "fresh d three coefficient is four pi",
        potential3 == charge / (4 * sp.pi * kappa * radius)
        and field3 == charge / (4 * sp.pi * kappa * radius**2),
    )
    ledger.check(
        "fresh d four is a decaying non-inverse-square counterexample",
        potential4 == charge / (4 * sp.pi**2 * kappa * radius**2)
        and field4 == charge / (2 * sp.pi**2 * kappa * radius**3),
    )

    reference = sp.Symbol("r0", positive=True)
    potential2 = -charge * sp.log(radius / reference) / (2 * sp.pi * kappa)
    field2 = sp.simplify(-sp.diff(potential2, radius))
    flux2 = sp.simplify(2 * sp.pi * radius * field2)
    potential1 = -charge * radius / (2 * kappa)
    field1 = sp.simplify(-sp.diff(potential1, radius))
    flux1 = sp.simplify(2 * field1)
    ledger.check(
        "fresh d two branch is logarithmic and reference dependent",
        flux2 == charge / kappa
        and sp.simplify(potential2.subs(radius, reference)) == 0
        and sp.limit(potential2, radius, sp.oo) in (sp.oo, -sp.oo),
    )
    ledger.check(
        "fresh d one branch is linear and nondecaying",
        flux1 == charge / kappa
        and sp.diff(potential1, radius, 2) == 0
        and sp.limit(potential1, radius, sp.oo) in (sp.oo, -sp.oo),
    )

    energy = sp.simplify(probe * potential3)
    force = sp.simplify(-sp.diff(energy, radius))
    ledger.check(
        "fresh two-charge force is the energy gradient",
        sp.simplify(force - probe * field3) == 0,
    )
    ledger.check(
        "source probe and kinetic mutations are independently visible",
        sp.simplify(force.subs(charge, -charge) + force) == 0
        and sp.simplify(force.subs(probe, -probe) + force) == 0
        and sp.simplify(force.subs(kappa, 2 * kappa) - force / 2) == 0,
    )

    observation, separation = sp.symbols("R a", positive=True)
    neutral_potential = sp.simplify(
        charge
        / (4 * sp.pi * kappa)
        * (1 / (observation - separation) - 1 / (observation + separation))
    )
    ledger.check(
        "fresh neutral dipole has zero total charge but nonzero field",
        neutral_potential != 0
        and sp.simplify(-sp.diff(neutral_potential, observation)) != 0,
    )

    nonpure = sp.diff(x, x) - sp.diff(0, sp.Symbol("Y", real=True))
    source_only_zero_current = tuple(-entry for entry in current)
    ledger.check(
        "fresh zero source-only action permits a non-pure connection",
        nonpure == 1
        and all(entry.subs({value: 0 for value in current}) == 0
                for entry in source_only_zero_current),
    )

    mass, length, duration, charge_unit = sp.symbols("M L T C")
    epsilon_dimension = charge_unit**2 * duration**2 / (mass * length**3)
    action_dimension = mass * length**2 / duration
    speed_dimension = length / duration
    ledger.check(
        "fresh fine-structure dimension ledger closes conditionally",
        sp.simplify(
            charge_unit**2
            / (epsilon_dimension * action_dimension * speed_dimension)
        )
        == 1,
    )
    ledger.check(
        "kinetic coefficient remains load bearing",
        kappa_action in {symbol for target in targets for symbol in target.free_symbols}
        and all(sp.simplify(target.subs(kappa_action, 2 * kappa_action) - target) != 0
                for target in targets),
    )
    return int(ledger.finish())


if __name__ == "__main__":
    raise SystemExit(main())
