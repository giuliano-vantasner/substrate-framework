"""Independent exact review of P063 without importing axial_ward."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(expression: object) -> bool:
    return sp.simplify(sp.sympify(expression)) == 0


def main() -> int:
    ledger = CheckLedger("P063-INDEPENDENT")

    zero2 = sp.zeros(2)
    sigma1 = sp.Matrix([[0, 1], [1, 0]])
    sigma2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sigma3 = sp.diag(1, -1)
    gamma0 = sp.diag(1, 1, -1, -1)

    def spatial_gamma(pauli: sp.Matrix) -> sp.Matrix:
        return sp.Matrix.vstack(
            sp.Matrix.hstack(zero2, pauli),
            sp.Matrix.hstack(-pauli, zero2),
        )

    gamma1, gamma2, gamma3 = tuple(
        spatial_gamma(pauli) for pauli in (sigma1, sigma2, sigma3)
    )
    gamma5 = sp.simplify(sp.I * gamma0 * gamma1 * gamma2 * gamma3)
    ledger.check("explicit gamma-five squares to identity", gamma5**2 == sp.eye(4))
    ledger.check(
        "explicit gamma-five anticommutes with all gamma matrices",
        all(
            sp.simplify(gamma5 * gamma + gamma * gamma5) == sp.zeros(4)
            for gamma in (gamma0, gamma1, gamma2, gamma3)
        ),
    )

    mass, momentum = sp.symbols("M k", positive=True)
    energy = sp.sqrt(mass**2 + momentum**2)
    normalization = sp.sqrt((energy + mass) / (2 * mass))
    initial = normalization * sp.Matrix(
        [1, 0, -momentum / (energy + mass), 0]
    )
    final = normalization * sp.Matrix(
        [1, 0, momentum / (energy + mass), 0]
    )
    final_bar = final.conjugate().T * gamma0
    q_slash = -2 * momentum * gamma3
    direct_divergence = sp.simplify((final_bar * q_slash * gamma5 * initial)[0])
    pseudoscalar = sp.simplify((final_bar * gamma5 * initial)[0])
    ledger.check(
        "explicit Breit spinors derive two-mass on-shell divergence",
        _zero(direct_divergence - 2 * mass * pseudoscalar),
    )
    axial_probe, induced_probe = sp.symbols("A_probe P_probe", real=True)
    minkowski_q_squared = -4 * momentum**2
    contracted_probe = sp.simplify(
        axial_probe * direct_divergence
        + minkowski_q_squared * induced_probe * pseudoscalar / (2 * mass)
    )
    ledger.check(
        "explicit induced term fixes the Minkowski current sign",
        _zero(
            contracted_probe / (2 * mass * pseudoscalar)
            - (
                axial_probe
                - 4 * momentum**2 * induced_probe / (4 * mass**2)
            )
        ),
    )

    q2, pion_mass2, decay = sp.symbols("Q2 mu2 F", positive=True)
    axial, induced, coupling = sp.symbols("G_A G_P G_pi", real=True)
    normalized_divergence = axial - q2 * induced / (4 * mass**2)
    pcac_source = decay * pion_mass2 * coupling / (
        mass * (pion_mass2 + q2)
    )
    ppd = 4 * mass * decay * coupling / (pion_mass2 + q2)
    ledger.check(
        "fresh form-factor contraction matches standard normalization",
        normalized_divergence.has(induced)
        and normalized_divergence.coeff(induced) == -q2 / (4 * mass**2),
    )
    ledger.check(
        "fresh pole substitution reduces generalized identity",
        _zero(
            normalized_divergence.subs(induced, ppd)
            - pcac_source
            - (axial - decay * coupling / mass)
        ),
    )

    coupling0, coupling_slope = sp.symbols("g0 s", real=True)
    coupling_function = coupling0 + coupling_slope * q2
    pole_function = 4 * mass * decay * coupling_function / (pion_mass2 + q2)
    residue = sp.residue(pole_function, q2, -pion_mass2)
    ledger.check(
        "independent complex residue uses pole-point coupling",
        _zero(
            residue
            - 4
            * mass
            * decay
            * (coupling0 - coupling_slope * pion_mass2)
        ),
    )
    ledger.check(
        "zero and pole coupling points differ at nonzero slope",
        sp.simplify(
            coupling_function.subs(q2, 0)
            - coupling_function.subs(q2, -pion_mass2)
        )
        == coupling_slope * pion_mass2,
    )

    regular0, regular1 = sp.symbols("R0 R1", real=True)
    regular = regular0 + regular1 * q2
    full_induced = pole_function + regular
    full_residual = sp.simplify(
        axial
        - q2 * full_induced / (4 * mass**2)
        - decay * pion_mass2 * coupling_function / (mass * (pion_mass2 + q2))
    )
    ledger.check(
        "fresh regular-remainder reduction",
        _zero(
            full_residual
            - (
                axial
                - decay * coupling_function / mass
                - q2 * regular / (4 * mass**2)
            )
        ),
    )
    ledger.check(
        "fresh regular remainder leaves rational residue unchanged",
        _zero(
            sp.residue(full_induced, q2, -pion_mass2)
            - sp.residue(pole_function, q2, -pion_mass2)
        ),
    )

    kernel = pion_mass2 / (pion_mass2 + q2)
    first_order = sp.limit(sp.limit(kernel, q2, 0), pion_mass2, 0)
    second_order = sp.limit(sp.limit(kernel, pion_mass2, 0), q2, 0)
    ledger.check("fresh zero-then-chiral limit is one", first_order == 1)
    ledger.check("fresh chiral-then-zero limit is zero", second_order == 0)
    path = sp.Symbol("c", positive=True)
    ledger.check(
        "fresh proportional path retains path dependence",
        sp.simplify(kernel.subs(q2, path * pion_mass2)) == 1 / (1 + path),
    )

    slope, quadratic = sp.symbols("s_GT R_GT", real=True)
    pole_coupling = coupling0 - slope * pion_mass2 + quadratic * pion_mass2**2
    discrepancy = sp.simplify(1 - coupling0 / pole_coupling)
    discrepancy_series = sp.series(discrepancy, pion_mass2, 0, 3).removeO()
    ledger.check(
        "fresh discrepancy has no constant term",
        sp.simplify(discrepancy_series.subs(pion_mass2, 0)) == 0,
    )
    ledger.check(
        "fresh discrepancy leading coefficient comes from coupling slope",
        sp.simplify(sp.diff(discrepancy_series, pion_mass2).subs(pion_mass2, 0))
        == -slope / coupling0,
    )
    positive_baseline = sp.Symbol("g_positive", positive=True)
    ledger.check(
        "nonanalytic coupling supplies a counterexample to mass-squared scaling",
        sp.limit(
            (
                1
                - positive_baseline
                / (positive_baseline + sp.sqrt(pion_mass2))
            )
            / pion_mass2,
            pion_mass2,
            0,
            dir="+",
        )
        == sp.oo,
    )

    exponent_row = sp.Matrix([[1, 1, -1, -1]])
    ledger.check("fresh GT exponent row has rank one", exponent_row.rank() == 1)
    ledger.check(
        "fresh GT monomial has three-dimensional parameter kernel",
        len(exponent_row.nullspace()) == 3,
    )

    yukawa, vacuum, axial_coefficient = sp.symbols("y v a", positive=True)
    declared_mass = yukawa * vacuum
    declared_pion_coupling = yukawa
    declared_decay_scale = vacuum
    minimal_model_residual = sp.simplify(
        declared_pion_coupling * declared_decay_scale - declared_mass
    )
    generalized_model_residual = sp.simplify(
        declared_pion_coupling * declared_decay_scale
        - axial_coefficient * declared_mass
    )
    ledger.check(
        "declared minimal Yukawa model gives GT only with fixed axial coefficient one",
        minimal_model_residual == 0
        and generalized_model_residual == yukawa * vacuum * (1 - axial_coefficient),
    )
    ledger.check(
        "effective-model route adds premises rather than deriving general physical GT",
        generalized_model_residual.subs(axial_coefficient, 2) != 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
