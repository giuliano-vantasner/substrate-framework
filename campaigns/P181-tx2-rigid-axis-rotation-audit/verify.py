#!/usr/bin/env python3
"""Primary exact verifier for TX2 and proposed C-GW-009."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.conditional_triaxial_radiation import (
    conditional_scaled_stf_power,
    conditional_scaled_stf_waveform,
)
from substrate_framework.rigid_quadrupole_rotation import (
    rigid_axisymmetric_stf_rotation,
    rodrigues_rotation_matrix,
    symmetric_tensor_characteristic_polynomial,
    tilted_axisymmetric_stf_rotation_about_z,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.tt_angular import frobenius_norm_squared
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-40/"
    "bridge_TX2_rotating_triaxial_quadrupole.py"
)
SOURCE_SHA256 = "7dd6852af20ef060ffa2f17950219fb79d7943e50fc64235a75a10d098f7d3b7"
RELEASE_SHA256 = "370471d17be24a34f909c34cfa42e8a33b8e92ce66ea1e9057ccdc72199d26bd"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _zero(expression: sp.Expr) -> bool:
    return sp.simplify(sp.expand(sp.trigsimp(expression))) == 0


def main() -> int:
    checks = CheckLedger("P181/TX2/C-GW-009")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.132.0.yaml") == RELEASE_SHA256,
    )
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    lexical_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source lexical and assertion inventory is exact",
        len(lexical_checks) == 7 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "TX2 has no NumPy integration compatibility surface",
        compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    time = sp.symbols("t", real=True)
    q, omega, scale, coupling, distance, spectral = sp.symbols(
        "q Omega s G R lambda", nonzero=True, real=True
    )
    angle = omega * time
    source_rotation = rodrigues_rotation_matrix([1, 0, 0], angle)
    checks.check(
        "source rotation convention is proper orthogonal",
        sp.simplify(source_rotation.T * source_rotation) == sp.eye(3)
        and sp.simplify(source_rotation.det()) == 1,
    )

    aligned = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[0, 0, 1],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    perpendicular = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[1, 0, 0],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    checks.check(
        "aligned rotation is an exact constant quadrupole path",
        aligned.tensor == aligned.body_tensor
        and aligned.first_derivative == sp.zeros(3)
        and aligned.third_derivative == sp.zeros(3),
    )

    expected = scale * q * sp.Matrix(
        [
            [1, 0, 0],
            [0, 1 - 3 * sp.sin(angle) ** 2, 3 * sp.sin(angle) * sp.cos(angle)],
            [0, 3 * sp.sin(angle) * sp.cos(angle), -2 + 3 * sp.sin(angle) ** 2],
        ]
    )
    checks.check(
        "perpendicular component tensor is exact",
        sp.simplify(perpendicular.tensor - expected) == sp.zeros(3),
    )
    checks.check(
        "implemented off-diagonal sign contradicts the source prose sign",
        _zero(perpendicular.tensor[1, 2] - 3 * scale * q * sp.sin(2 * angle) / 2)
        and "Q_yz = -3q sin cos" in source_text,
    )

    expected_characteristic = (spectral - scale * q) ** 2 * (
        spectral + 2 * scale * q
    )
    checks.check(
        "orthogonal conjugation preserves the repeated eigenvalue exactly",
        _zero(
            symmetric_tensor_characteristic_polynomial(
                perpendicular.tensor, spectral
            )
            - expected_characteristic
        ),
    )
    checks.check(
        "the rotating symmetry axis remains the unique axial eigenvector",
        sp.simplify(
            perpendicular.tensor * perpendicular.instantaneous_symmetry_axis
            + 2 * scale * q * perpendicular.instantaneous_symmetry_axis
        )
        == sp.zeros(3, 1),
    )
    generic_phase = {time: sp.Rational(1, 2), omega: 1, q: 1, scale: 1}
    diagonals = [sp.N(perpendicular.tensor[i, i].subs(generic_phase)) for i in range(3)]
    checks.check(
        "distinct coordinate diagonals do not imply triaxial eigenstructure",
        len(set(diagonals)) == 3
        and _zero(
            symmetric_tensor_characteristic_polynomial(
                perpendicular.tensor, spectral
            )
            - expected_characteristic
        ),
    )

    sine_squared = sp.symbols("x", real=True)
    diagonal_polynomials = (
        scale * q,
        scale * q * (1 - 3 * sine_squared),
        scale * q * (-2 + 3 * sine_squared),
    )
    coincidence_sets = []
    for first, second in ((0, 1), (0, 2), (1, 2)):
        coincidence_sets.append(
            sp.solve(sp.Eq(diagonal_polynomials[first], diagonal_polynomials[second]), sine_squared)
        )
    checks.check(
        "coordinate diagonal coincidences are zero one-half and one",
        coincidence_sets == [[0], [1], [sp.Rational(1, 2)]],
    )

    cosine_two = sp.cos(2 * angle)
    sine_two = sp.sin(2 * angle)
    harmonic_form = scale * q * sp.Matrix(
        [
            [1, 0, 0],
            [0, -sp.Rational(1, 2) + 3 * cosine_two / 2, 3 * sine_two / 2],
            [0, 3 * sine_two / 2, -sp.Rational(1, 2) - 3 * cosine_two / 2],
        ]
    )
    checks.check(
        "perpendicular tensor is DC plus a pure twice-frequency harmonic",
        sp.trigsimp(perpendicular.tensor - harmonic_form) == sp.zeros(3),
    )
    checks.check(
        "half-period and non-quarter-period limits are both exact",
        sp.simplify(
            perpendicular.tensor.subs(time, time + sp.pi / omega)
            - perpendicular.tensor
        )
        == sp.zeros(3)
        and sp.simplify(
            perpendicular.tensor.subs(time, time + sp.pi / (2 * omega))
            - perpendicular.tensor
        )
        != sp.zeros(3),
    )

    second_norm = sp.trigsimp(
        frobenius_norm_squared(perpendicular.second_derivative)
    )
    third_norm = sp.trigsimp(
        frobenius_norm_squared(perpendicular.third_derivative)
    )
    checks.check(
        "perpendicular derivative norms are exact",
        second_norm == 72 * scale**2 * q**2 * omega**4
        and third_norm == 288 * scale**2 * q**2 * omega**6,
    )
    checks.check(
        "the third derivative has three distinct eigenvalues when q Omega is nonzero",
        _zero(
            symmetric_tensor_characteristic_polynomial(
                perpendicular.third_derivative, spectral
            )
            - spectral * (spectral**2 - 144 * scale**2 * q**2 * omega**6)
        ),
    )
    checks.check(
        "zero anisotropy and zero angular speed mutations break nonzero derivatives",
        perpendicular.third_derivative.subs(q, 0) == sp.zeros(3)
        and perpendicular.third_derivative.subs(omega, 0) == sp.zeros(3),
    )

    conditional_power = conditional_scaled_stf_power(
        perpendicular.third_derivative, coupling, scale
    )
    wrong_power = conditional_scaled_stf_power(
        3 * perpendicular.third_derivative.subs(scale, 1), coupling, 1
    )
    checks.check(
        "conditional power is convention safe and the wrong scale gives factor nine",
        conditional_power == 288 * coupling * q**2 * omega**6 / 5
        and wrong_power == 9 * conditional_power,
    )
    waveform = conditional_scaled_stf_waveform(
        perpendicular.second_derivative,
        [1, 0, 0],
        coupling,
        distance,
        scale,
        [0, 1, 0],
    )
    checks.check(
        "rotation-axis conditional readout is equal-amplitude quadrature",
        _zero(
            waveform.conventional_plus
            + 12 * coupling * q * omega**2 * cosine_two / distance
        )
        and _zero(
            waveform.conventional_cross
            + 12 * coupling * q * omega**2 * sine_two / distance
        )
        and _zero(
            waveform.conventional_plus**2
            + waveform.conventional_cross**2
            - 144 * coupling**2 * q**2 * omega**4 / distance**2
        ),
    )

    tilt = sp.symbols("beta", real=True)
    tilted = tilted_axisymmetric_stf_rotation_about_z(
        q, omega, time, tilt, scale
    )
    checks.check(
        "generic tilt has independent fundamental and twice-frequency components",
        _zero(
            tilted.tensor[0, 2]
            + 3 * scale * q * sp.sin(tilt) * sp.cos(tilt) * sp.cos(angle)
        )
        and _zero(
            tilted.tensor[0, 1]
            + 3 * scale * q * sp.sin(tilt) ** 2 * sp.sin(2 * angle) / 2
        ),
    )
    tilt_norm = frobenius_norm_squared(tilted.third_derivative)
    expected_tilt_norm = (
        18
        * scale**2
        * q**2
        * omega**6
        * sp.sin(tilt) ** 2
        * (sp.cos(tilt) ** 2 + 16 * sp.sin(tilt) ** 2)
    )
    checks.check(
        "generic tilt derivative norm and perpendicular maximum are exact",
        _zero(tilt_norm - expected_tilt_norm)
        and _zero(tilt_norm.subs(tilt, 0))
        and _zero(
            tilt_norm.subs(tilt, sp.pi / 2)
            - 288 * scale**2 * q**2 * omega**6
        ),
    )
    x = sp.symbols("x", nonnegative=True, real=True)
    reduced_tilt_norm = 18 * scale**2 * q**2 * omega**6 * x * (1 + 15 * x)
    checks.check(
        "tilt norm is monotone in sine-squared tilt under nonzero real inputs",
        sp.simplify(
            sp.diff(reduced_tilt_norm, x)
            - 18 * scale**2 * q**2 * omega**6 * (1 + 30 * x)
        )
        == 0,
    )

    triaxial_body = sp.diag(q, 0, -q)
    checks.check(
        "a genuine triaxial counterexample has three distinct principal values",
        _zero(
            symmetric_tensor_characteristic_polynomial(triaxial_body, spectral)
            - spectral * (spectral - q) * (spectral + q)
        ),
    )
    checks.check(
        "the accepted result remains explicitly kinematic and conditional",
        "do not establish that the path solves a field equation"
        in (ROOT / "src/substrate_framework/rigid_quadrupole_rotation.py").read_text(
            encoding="utf-8"
        )
        and "conditional on the wave"
        in (
            ROOT / "src/substrate_framework/conditional_triaxial_radiation.py"
        ).read_text(encoding="utf-8"),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
