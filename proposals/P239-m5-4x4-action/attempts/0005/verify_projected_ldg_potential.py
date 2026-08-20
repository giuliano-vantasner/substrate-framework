"""Verify the exact Lorentz lift of the complete M5.17 potential."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    m5_ldg_coefficients,
    projected_spatial_ldg_potential,
    spectral_projector_from_eigenvalues,
)
from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent
ETA = sp.Matrix(MINKOWSKI_MOSTLY_PLUS)


def _rational_lorentz() -> sp.Matrix:
    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = sp.Rational(4, 3)
    rotation = sp.eye(4)
    rotation[2, 2] = rotation[3, 3] = sp.Rational(3, 5)
    rotation[2, 3] = -sp.Rational(4, 5)
    rotation[3, 2] = sp.Rational(4, 5)
    return boost * rotation


def main() -> int:
    ledger = CheckLedger("P239/projected-M5.17-potential")
    beta, scale, g_value, time_stiffness = sp.symbols("beta c g w_t", positive=True)
    a_value, b_value, c_value, vacuum_value = m5_ldg_coefficients(beta, scale)
    ledger.check("b=beta*c", sp.simplify(b_value - beta * scale) == 0)
    ledger.check(
        "a=(3b-4c)/2",
        sp.simplify(2 * a_value - 3 * b_value + 4 * c_value) == 0,
    )
    ledger.check(
        "vacuum subtraction is a-b+c",
        sp.simplify(vacuum_value - (a_value - b_value + c_value)) == 0,
    )

    x, y, z, u, v, w = sp.symbols("x y z u v w", real=True)
    spatial = sp.Matrix([[x, u, v], [u, y, w], [v, w, z]])
    order_parameter = sp.diag(-g_value, 0, 0, 0)
    order_parameter[1:4, 1:4] = spatial
    projector = sp.diag(1, 0, 0, 0)
    lifted = projected_spatial_ldg_potential(
        order_parameter,
        projector,
        beta,
        scale,
        g_value,
        time_stiffness,
    )
    source_spatial = sp.factor(
        a_value * sp.trace(spatial**2)
        - b_value * sp.trace(spatial**3)
        + c_value * sp.trace(spatial**2) ** 2
        - vacuum_value
    )
    ledger.check(
        "complete off-shell M5.17 potential is recovered",
        sp.simplify(lifted - source_spatial) == 0,
    )

    transformation = _rational_lorentz()
    inverse = transformation.inv()
    covector = inverse.T
    transformed_order_parameter = covector * order_parameter * covector.T
    transformed_projector = transformation * projector * inverse
    transformed_lift = projected_spatial_ldg_potential(
        transformed_order_parameter,
        transformed_projector,
        beta,
        scale,
        g_value,
        time_stiffness,
    )
    ledger.check(
        "projected potential is an exact Lorentz scalar",
        sp.simplify(transformed_lift - lifted) == 0,
    )

    vacuum = sp.diag(-g_value, 1, 0, 0)
    vacuum_potential = projected_spatial_ldg_potential(
        vacuum, projector, beta, scale, g_value, time_stiffness
    )
    ledger.check("uniaxial vacuum has zero potential", vacuum_potential == 0)
    repeated_projector = spectral_projector_from_eigenvalues(
        ETA.inv() * vacuum, g_value, (g_value, 1, 0, 0)
    )
    ledger.check(
        "repeated tangent eigenvalues retain the simple timelike projector",
        repeated_projector == projector,
    )

    radial_amplitude = sp.symbols("s", nonnegative=True)
    radial_path = projected_spatial_ldg_potential(
        sp.diag(-g_value, radial_amplitude, 0, 0),
        projector,
        beta,
        scale,
        g_value,
        time_stiffness,
    )
    ledger.check(
        "uniaxial vacuum is stationary",
        sp.diff(radial_path, radial_amplitude).subs(radial_amplitude, 1) == 0,
    )
    ledger.check(
        "uniaxial radial Hessian is c*(8-3*beta)",
        sp.factor(
            sp.diff(radial_path, radial_amplitude, 2).subs(radial_amplitude, 1)
            - scale * (8 - 3 * beta)
        )
        == 0,
    )
    ledger.check(
        "melt cost is c*(1-beta/2)",
        sp.factor(radial_path.subs(radial_amplitude, 0) - scale * (1 - beta / 2)) == 0,
    )
    ledger.check(
        "radial excess factor has the source global-minimum form",
        sp.factor(
            radial_path
            - scale
            * (radial_amplitude - 1) ** 2
            * (2 * (radial_amplitude + 1) ** 2 - beta * (2 * radial_amplitude + 1))
            / 2
        )
        == 0,
    )

    time_shift = sp.symbols("epsilon", real=True)
    shifted_time = projected_spatial_ldg_potential(
        sp.diag(-(g_value + time_shift), 1, 0, 0),
        projector,
        beta,
        scale,
        g_value,
        time_stiffness,
    )
    ledger.check(
        "time eigenvalue is pinned independently",
        sp.factor(shifted_time - time_stiffness * time_shift**2) == 0,
    )

    mixed = ETA.inv() * order_parameter
    full_trace_mutation = sp.factor(
        a_value * sp.trace(mixed**2)
        - b_value * sp.trace(mixed**3)
        + c_value * sp.trace(mixed**2) ** 2
        - vacuum_value
    )
    ledger.check(
        "deleting the spectral complement fails exact M5.17 reduction",
        sp.simplify(full_trace_mutation - source_spatial) != 0,
    )
    fixed_projector_rejected = False
    try:
        projected_spatial_ldg_potential(
            transformed_order_parameter,
            projector,
            beta,
            scale,
            g_value,
            time_stiffness,
        )
    except ValueError as error:
        fixed_projector_rejected = "must be spectral" in str(error)
    ledger.check(
        "fixed coordinate projector mutation is rejected", fixed_projector_rejected
    )

    result = {
        "campaign": "P239",
        "attempt": "0005",
        "candidate": "G_uniaxial_axisymmetric_completion",
        "potential": ("a Tr(Y^2)-b Tr(Y^3)+c Tr(Y^2)^2-V_vac" "+w_t(Tr(P_t X)-g)^2"),
        "definitions": "X=eta^-1 M; Q=I-P_t; Y=Q X Q",
        "parameter_domain": "c>0, w_t>0, 0<beta=b/c<2",
        "verdict": (
            "The projector-defined potential is an exact Lorentz scalar and "
            "recovers the complete off-shell M5.17 Landau-de Gennes potential. "
            "It has the regular uniaxial exterior spectrum (g,1,0,0), pins g, "
            "and admits the repeated tangent eigenvalues required at a regular "
            "hedgehog axis."
        ),
        "next_route": (
            "Freeze and solve the regular axisymmetric fixed-J field problem "
            "using this potential and the exact M5.17 equivariant derivative channels."
        ),
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
