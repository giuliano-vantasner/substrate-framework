"""Primary exact verifier for P067 pure-spin-1 orbit selection."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.spin1_mean_field import (
    cartesian_to_spin1,
    fixed_density_spin1_selection,
    spin1_cartesian_spin,
    spin1_expectation,
    spin1_invariant_residual,
    spin1_magnitude_squared,
    spin1_matrices,
    spin1_orbit_ledger,
    spin1_singlet_amplitude,
    spin1_to_cartesian,
)
from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_ME1_polar_phase_selection.py"
)
SOURCE_SHA256 = "54d34a026b45d7ae01b53dae022cbcab61f380f4cda289d6a5862d2cc72adc71"


def main() -> int:
    ledger = CheckLedger("P067")
    ledger.check("hash-pinned ME1 source exists", SOURCE.is_file())
    ledger.check(
        "hash-pinned ME1 source integrity",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    source_text = SOURCE.read_text(encoding="utf-8")
    ledger.check(
        "ME1 upper-bound oracle is finite random sampling rather than an SOS proof",
        "for _ in range(4000):" in source_text
        and "upper_nonneg = min_seen >= -1e-9" in source_text,
    )
    ledger.check(
        "ME1 endpoint check supplies representatives but no equality-set exhaustion",
        "polar_subs =" in source_text
        and "ferro_subs =" in source_text
        and "(F2_at_polar == 0)" in source_text
        and "(gap_at_ferro == 0)" in source_text,
    )
    ledger.check(
        "ME1 interpolation verdict checks endpoints only",
        "interp_in_range = (interp_at_polar == 0) and (interp_at_ferro == 1)"
        in source_text,
    )

    fx, fy, fz = spin1_matrices()
    zero_matrix = sp.zeros(3)
    ledger.check(
        "spin-1 matrices are Hermitian",
        all(matrix.conjugate().T == matrix for matrix in (fx, fy, fz)),
    )
    ledger.check(
        "spin-1 matrices obey the su2 commutators",
        sp.simplify(fx * fy - fy * fx - sp.I * fz) == zero_matrix
        and sp.simplify(fy * fz - fz * fy - sp.I * fx) == zero_matrix
        and sp.simplify(fz * fx - fx * fz - sp.I * fy) == zero_matrix,
    )
    ledger.check(
        "spin-1 Casimir normalization is two",
        sp.simplify(fx**2 + fy**2 + fz**2) == 2 * sp.eye(3),
    )

    ar, ai, br, bi, cr, ci = sp.symbols(
        "a_r a_i b_r b_i c_r c_i", real=True
    )
    generic = sp.ImmutableMatrix(
        [ar + sp.I * ai, br + sp.I * bi, cr + sp.I * ci]
    )
    ledger.check(
        "general complex spinor obeys the exact singlet invariant",
        sp.expand(spin1_invariant_residual(generic)) == 0,
    )
    amplitude = spin1_singlet_amplitude(generic)
    wrong_amplitudes = (
        generic[1] ** 2 + 2 * generic[0] * generic[2],
        generic[1] ** 2 - generic[0] * generic[2],
        generic[1] ** 2 - 2 * sp.conjugate(generic[0]) * generic[2],
    )
    norm = sp.simplify((generic.conjugate().T * generic)[0])
    spin_squared = spin1_magnitude_squared(generic)
    invariant_predicate = lambda candidate: sp.expand(
        spin_squared + sp.conjugate(candidate) * candidate - norm**2
    ) == 0
    ledger.mutation_sensitive(
        "singlet identity fixes sign factor and conjugation placement",
        invariant_predicate,
        amplitude,
        wrong_amplitudes,
    )

    ux, uy, uz, vx, vy, vz = sp.symbols("u_x u_y u_z v_x v_y v_z", real=True)
    u = sp.ImmutableMatrix([ux, uy, uz])
    v = sp.ImmutableMatrix([vx, vy, vz])
    cartesian = u + sp.I * v
    spherical = cartesian_to_spin1(cartesian)
    ledger.check(
        "spherical-Cartesian maps are exact inverses",
        spin1_to_cartesian(spherical).applyfunc(sp.simplify) == cartesian,
    )
    expected_spin = 2 * u.cross(v)
    ledger.check(
        "matrix spin equals twice the Cartesian cross product",
        all(
            sp.simplify(left - right) == 0
            for left, right in zip(spin1_expectation(spherical), expected_spin)
        )
        and spin1_cartesian_spin(cartesian) == tuple(expected_spin),
    )
    ledger.check(
        "singlet amplitude is the complex Cartesian self-dot-product",
        sp.expand(spin1_singlet_amplitude(spherical) - cartesian.dot(cartesian))
        == 0,
    )
    ledger.check(
        "Cartesian identity is the Lagrange cross-product identity",
        sp.expand(
            4 * u.cross(v).dot(u.cross(v))
            + ((u.dot(u) - v.dot(v)) ** 2 + 4 * u.dot(v) ** 2)
            - (u.dot(u) + v.dot(v)) ** 2
        )
        == 0,
    )

    qx, qy, qz, alpha, beta = sp.symbols(
        "q_x q_y q_z alpha beta", real=True
    )
    polar_cartesian = (alpha + sp.I * beta) * sp.ImmutableMatrix([qx, qy, qz])
    polar_family = cartesian_to_spin1(polar_cartesian)
    ledger.check(
        "parallel Cartesian real and imaginary parts give the full polar normal form",
        all(value == 0 for value in spin1_expectation(polar_family))
        and spin1_magnitude_squared(polar_family) == 0,
    )
    density = sp.Symbol("n", positive=True)
    ferro_cartesian = sp.sqrt(density / 2) * sp.ImmutableMatrix([1, sp.I, 0])
    ferro_family = cartesian_to_spin1(ferro_cartesian)
    ledger.check(
        "orthogonal equal-norm Cartesian parts saturate the ferromagnetic endpoint",
        sp.simplify(spin1_singlet_amplitude(ferro_family)) == 0
        and sp.simplify(spin1_magnitude_squared(ferro_family) - density**2) == 0,
    )
    ledger.check(
        "exact orbit ledger classifies rotated endpoint representatives",
        spin1_orbit_ledger((1 / sp.sqrt(2), 0, 1 / sp.sqrt(2))).projective_orbit
        == "polar"
        and spin1_orbit_ledger((sp.Rational(1, 2), 1 / sp.sqrt(2), sp.Rational(1, 2))).projective_orbit
        == "ferromagnetic",
    )

    angle = sp.symbols("theta", real=True)
    exact_path = sp.ImmutableMatrix([sp.cos(angle), 0, sp.sin(angle)])
    ledger.check(
        "an exact normalized path attains the full spin-squared interval",
        sp.trigsimp(spin1_magnitude_squared(exact_path) - sp.cos(2 * angle) ** 2)
        == 0
        and spin1_magnitude_squared(exact_path.subs(angle, 0)) == 1
        and spin1_magnitude_squared(exact_path.subs(angle, sp.pi / 4)) == 0,
    )
    source_path = sp.ImmutableMatrix([sp.cos(angle), sp.sin(angle), 0])
    ledger.check(
        "ME1's asserted cos-squared interpolation formula is false away from endpoints",
        sp.simplify(
            spin1_magnitude_squared(source_path.subs(angle, sp.pi / 4))
            - sp.cos(sp.pi / 4) ** 2
        )
        != 0,
    )

    cplus = sp.Symbol("c_plus", positive=True)
    cminus = sp.Symbol("c_minus", negative=True)
    positive = fixed_density_spin1_selection(3, cplus)
    negative = fixed_density_spin1_selection(3, cminus)
    boundary = fixed_density_spin1_selection(3, 0)
    ledger.check(
        "positive coupling selects precisely the polar projective orbit",
        positive.minimizing_projective_orbits == ("polar",)
        and positive.minimum_energy == 0
        and positive.maximum_energy == 9 * cplus / 2,
    )
    ledger.check(
        "negative coupling selects precisely the ferromagnetic projective orbit",
        negative.minimizing_projective_orbits == ("ferromagnetic",)
        and negative.minimum_energy == 9 * cminus / 2
        and negative.maximum_energy == 0,
    )
    ledger.check(
        "zero coupling leaves every pure spin-1 ray degenerate",
        boundary.minimizing_projective_orbits == ("all_pure_spin1_rays",)
        and boundary.minimum_energy == boundary.maximum_energy == 0,
    )
    ledger.mutation_sensitive(
        "endpoint energy gap carries the density-squared factor and sign",
        lambda candidate: sp.simplify(candidate + 9 * cplus / 2) == 0,
        positive.polar_minus_ferromagnetic_energy,
        [-cplus / 2, -3 * cplus / 2, 9 * cplus / 2],
    )
    malformed_rejections = []
    for operation in (
        lambda: spin1_orbit_ledger((0, 0, 0)),
        lambda: spin1_orbit_ledger(sp.eye(3)),
        lambda: fixed_density_spin1_selection(1, sp.Symbol("c", real=True)),
        lambda: fixed_density_spin1_selection(0, 1),
    ):
        try:
            operation()
        except ValueError:
            malformed_rejections.append(True)
    ledger.check(
        "pure-state and exact-sign APIs reject zero mixed malformed and undecidable inputs",
        malformed_rejections == [True, True, True, True],
    )
    canonical_source = Path("src/substrate_framework/spin1_mean_field.py").read_text(
        encoding="utf-8"
    )
    ledger.check(
        "P067 exact finite algebra uses no NumPy quadrature alias",
        "np." + "trapz" not in canonical_source
        and "np." + "trapezoid" not in canonical_source,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
