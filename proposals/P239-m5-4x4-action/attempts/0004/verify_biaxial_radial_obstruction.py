"""Prove the moving-biaxial-frame obstruction in the radial ansatz."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent


def _rotation(generator: sp.Matrix, angle: sp.Expr) -> sp.Matrix:
    return sp.eye(4) + sp.sin(angle) * generator + (1 - sp.cos(angle)) * generator**2


def main():
    ledger = CheckLedger("P239/biaxial-radial-obstruction")
    phi, chi = sp.symbols("phi chi", real=True)
    lambda_radial, lambda_2, lambda_3 = sp.symbols(
        "lambda_1 lambda_2 lambda_3", real=True
    )
    g = sp.symbols("g", positive=True)
    generator_1 = sp.zeros(4)
    generator_1[2, 3], generator_1[3, 2] = -1, 1
    generator_2 = sp.zeros(4)
    generator_2[1, 3], generator_2[3, 1] = 1, -1
    generator_3 = sp.zeros(4)
    generator_3[1, 2], generator_3[2, 1] = -1, 1
    rotation = _rotation(generator_3, phi) * _rotation(generator_2, -sp.pi / 2)

    diagonal = sp.diag(-g, lambda_radial, lambda_2, lambda_3)
    pole_field = sp.simplify(rotation * diagonal * rotation.T)
    pole_field_azimuthal = sp.simplify(sp.diff(pole_field, phi))
    pole_field_norm = sp.trigsimp(
        sp.trace(pole_field_azimuthal * pole_field_azimuthal.T)
    )
    ledger.check(
        "biaxial field has a nonzero azimuthal pole derivative",
        sp.factor(pole_field_norm - 2 * (lambda_2 - lambda_3) ** 2) == 0,
    )
    ledger.check(
        "uniaxial tangent degeneracy removes the field string",
        pole_field_azimuthal.subs(lambda_3, lambda_2) == sp.zeros(4),
    )

    boost_2 = sp.eye(4)
    boost_2[0, 0] = boost_2[2, 2] = sp.cosh(chi)
    boost_2[0, 2] = boost_2[2, 0] = sp.sinh(chi)
    projector_0 = sp.diag(1, 0, 0, 0)
    eigenframe_projector = boost_2.inv() * projector_0 * boost_2
    pole_projector = sp.simplify(rotation * eigenframe_projector * rotation.T)
    projector_azimuthal = sp.simplify(sp.diff(pole_projector, phi))
    projector_target_norm = sp.trigsimp(
        -sp.trace(projector_azimuthal * projector_azimuthal) / 2
    )
    ledger.check(
        "tangential boost has a nonzero azimuthal pole current",
        sp.factor(projector_target_norm - sp.sinh(chi) ** 2) == 0,
    )
    ledger.check(
        "zero boost removes the projector string",
        projector_azimuthal.subs(chi, 0) == sp.zeros(4),
    )

    theta, cutoff = sp.symbols("theta cutoff", positive=True)
    angular_string_integral = sp.integrate(
        1 / sp.sin(theta), (theta, cutoff, sp.pi / 2)
    )
    ledger.check(
        "angular connection energy diverges logarithmically",
        sp.limit(angular_string_integral, cutoff, 0, dir="+") == sp.oo,
    )
    ledger.check(
        "the divergence coefficient is positive for a nonzero tangential boost",
        sp.simplify(projector_target_norm.subs(chi, 1)) > 0,
    )

    result = {
        "campaign": "P239",
        "attempt": "0004",
        "representation": "radial profiles on a moving biaxial eigenframe",
        "field_pole_coefficient": "2*(lambda_2-lambda_3)^2",
        "projector_pole_coefficient": "sinh(chi)^2",
        "angular_integral": "integral dtheta/sin(theta)",
        "verdict": (
            "A nonzero radial-only tangential boost or asymptotically biaxial "
            "tangent frame has logarithmically divergent angular energy. The "
            "single-axis numerical branch is representation-obstructed and "
            "cannot support C-M5-002 or C-M5-004."
        ),
        "strongest_surviving_result": (
            "The exact selected action and projector-current construction from "
            "attempts 0002-0003 survive; the radial biaxial stationary ansatz does not."
        ),
        "next_route": (
            "Use the M5.17 uniaxial exterior and relax angular/axisymmetric "
            "fields so tangent splitting and boost dressing vanish regularly on the axis."
        ),
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
