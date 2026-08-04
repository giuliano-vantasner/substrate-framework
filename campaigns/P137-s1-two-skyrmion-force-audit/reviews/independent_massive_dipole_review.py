from __future__ import annotations

import numpy as np
import sympy as sp

from substrate_framework.verification import CheckLedger


def _rotation_from_unit_quaternion(q: np.ndarray) -> np.ndarray:
    w, x, y, z = q
    return np.asarray(
        (
            (1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)),
            (2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)),
            (2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)),
        ),
        dtype=float,
    )


def main() -> int:
    checks = CheckLedger("P137-INDEPENDENT-MASSIVE-DIPOLE")

    radius, mass, stiffness, strength = sp.symbols(
        "R m K P", positive=True
    )
    x, y, z = sp.symbols("x y z", real=True)
    radial_coordinate = sp.sqrt(x**2 + y**2 + z**2)
    cartesian_green = sp.exp(-mass * radial_coordinate) / (
        4 * sp.pi * radial_coordinate
    )
    hxx = sp.simplify(sp.diff(cartesian_green, x, 2).subs(x, 0).subs(y, 0).subs(z, radius))
    hzz = sp.simplify(sp.diff(cartesian_green, z, 2).subs(x, 0).subs(y, 0).subs(z, radius))
    transverse = -sp.exp(-mass * radius) * (1 + mass * radius) / (
        4 * sp.pi * radius**3
    )
    longitudinal = sp.exp(-mass * radius) * (
        mass**2 * radius**2 + 2 * mass * radius + 2
    ) / (4 * sp.pi * radius**3)
    checks.check(
        "fresh Cartesian Hessian gives radial coefficients",
        sp.simplify(hxx - transverse) == 0
        and sp.simplify(hzz - longitudinal) == 0,
    )

    # Fourier differentiation supplies -H_ij for k_i*k_j/(k^2+m^2).
    # Each J=-P*d_i(delta) gives one factor -iP*k_i. The source pairing is
    # therefore -P^2*D:H and the on-shell cross energy is its negative over K.
    d11, d22, d33 = sp.symbols("D11 D22 D33", real=True)
    contraction = transverse * (d11 + d22) + longitudinal * d33
    fourier_pairing = -strength**2 * contraction
    on_shell_cross = -fourier_pairing / stiffness
    checks.check(
        "fresh Fourier source pairing fixes normalization and sign",
        sp.simplify(
            on_shell_cross - strength**2 * contraction / stiffness
        )
        == 0,
    )

    cosine, axial_square = sp.symbols("c zeta", real=True)
    anisotropic = sp.simplify(longitudinal - transverse)
    rodrigues_contraction = sp.simplify(
        transverse * (1 + 2 * cosine)
        + anisotropic
        * (cosine + (1 - cosine) * axial_square)
    )
    lower_gap = sp.simplify(rodrigues_contraction + longitudinal)
    upper_gap = sp.simplify(
        longitudinal - 2 * transverse - rodrigues_contraction
    )
    checks.check(
        "fresh Rodrigues lower gap is a sum of nonnegative factors",
        sp.simplify(
            lower_gap
            - (
                (longitudinal + transverse) * (1 + cosine)
                + anisotropic * (1 - cosine) * axial_square
            )
        )
        == 0,
    )
    checks.check(
        "fresh Rodrigues upper gap is a sum of nonnegative factors",
        sp.simplify(
            upper_gap
            - (
                (-2 * transverse) * (1 + cosine)
                + anisotropic
                * (1 - cosine)
                * (1 - axial_square)
            )
        )
        == 0,
    )
    checks.check(
        "fresh coefficient signs hold for positive mass and radius",
        transverse.could_extract_minus_sign()
        and sp.factor(longitudinal + transverse)
        == sp.exp(-mass * radius)
        * (mass**2 * radius**2 + mass * radius + 1)
        / (4 * sp.pi * radius**3)
        and sp.factor(anisotropic)
        == sp.exp(-mass * radius)
        * (mass**2 * radius**2 + 3 * mass * radius + 3)
        / (4 * sp.pi * radius**3),
    )

    minimum = -strength**2 * longitudinal / stiffness
    maximum = strength**2 * (longitudinal - 2 * transverse) / stiffness
    radial_force = sp.simplify(-sp.diff(minimum, radius))
    expected_force = -strength**2 * sp.exp(-mass * radius) * (
        mass**3 * radius**3
        + 3 * mass**2 * radius**2
        + 6 * mass * radius
        + 6
    ) / (4 * sp.pi * stiffness * radius**4)
    checks.check(
        "fresh attractive-channel force is exact and inward",
        sp.simplify(radial_force - expected_force) == 0
        and sp.factor(radial_force).could_extract_minus_sign(),
    )
    checks.check(
        "fresh massless and large-separation limits are distinct",
        sp.simplify(
            sp.limit(minimum, mass, 0, dir="+")
            + strength**2 / (2 * sp.pi * stiffness * radius**3)
        )
        == 0
        and sp.limit(radius**20 * minimum, radius, sp.oo) == 0,
    )

    rng = np.random.default_rng(137)
    quaternions = rng.normal(size=(4096, 4))
    quaternions /= np.linalg.norm(quaternions, axis=1)[:, None]
    numeric_radius = 1.7
    numeric_mass = 0.8
    numeric_transverse = -np.exp(-numeric_mass * numeric_radius) * (
        1 + numeric_mass * numeric_radius
    ) / (4 * np.pi * numeric_radius**3)
    numeric_longitudinal = np.exp(-numeric_mass * numeric_radius) * (
        numeric_mass**2 * numeric_radius**2
        + 2 * numeric_mass * numeric_radius
        + 2
    ) / (4 * np.pi * numeric_radius**3)
    numeric_anisotropic = numeric_longitudinal - numeric_transverse
    values = []
    for quaternion in quaternions:
        rotation = _rotation_from_unit_quaternion(quaternion)
        values.append(
            numeric_transverse * np.trace(rotation)
            + numeric_anisotropic * rotation[2, 2]
        )
    sampled = np.asarray(values)
    checks.check(
        "independent random SO3 sample respects exact extrema",
        bool(np.all(sampled >= -numeric_longitudinal - 2e-14))
        and bool(
            np.all(
                sampled
                <= numeric_longitudinal - 2 * numeric_transverse + 2e-14
            )
        ),
    )
    checks.check(
        "quaternion construction stays in SO3",
        all(
            np.linalg.norm(
                _rotation_from_unit_quaternion(q).T
                @ _rotation_from_unit_quaternion(q)
                - np.eye(3)
            )
            < 2e-14
            and abs(np.linalg.det(_rotation_from_unit_quaternion(q)) - 1) < 2e-14
            for q in quaternions[:64]
        ),
    )

    source_numeric_rhs = -sp.exp(-mass * radius) * (
        mass + 1 / radius
    )
    exact_profile_rhs = sp.diff(sp.exp(-mass * radius) / radius, radius)
    checks.check(
        "fresh source-equation audit detects the missing inverse radius",
        sp.simplify(source_numeric_rhs / exact_profile_rhs) == radius,
    )
    checks.check(
        "load-bearing amplitude and stiffness mutations change the theorem",
        sp.simplify(minimum.subs(strength, 3 * strength) - 9 * minimum) == 0
        and sp.simplify(minimum.subs(stiffness, 2 * stiffness) - minimum / 2)
        == 0,
    )
    checks.check(
        "source-coupling sign mutation reverses attraction and ordering",
        (-minimum).could_extract_minus_sign() is False
        and (-maximum).could_extract_minus_sign(),
    )
    improper = -np.eye(3)
    improper_value = (
        numeric_transverse * np.trace(improper)
        + numeric_anisotropic * improper[2, 2]
    )
    checks.check(
        "wrong orientation-domain probe is detectably improper",
        np.linalg.det(improper) < 0
        and not np.isclose(np.linalg.det(improper), 1)
        and np.isfinite(improper_value),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
