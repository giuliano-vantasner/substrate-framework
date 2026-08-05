#!/usr/bin/env python3
"""Primary exact verifier for TX3 and proposed C-GW-010."""

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
)
from substrate_framework.rotating_quadrupole_polarization import (
    conditional_perpendicular_rotation_polarization,
    perpendicular_axisymmetric_stf_second_derivative,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.tt_angular import tt_polarization_basis
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-40/"
    "bridge_TX3_two_polarizations_omega_free.py"
)
SOURCE_SHA256 = "ce6db5f59e61829c287e7cced5a53506838d31c77ba9e651dbceb9a241275837"
RELEASE_SHA256 = "b54f12b9dad95df4a225f980df6f74f58458ac174e312f5276c7bd1fe4ad1c8e"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _zero(expression: sp.Expr) -> bool:
    return sp.simplify(sp.expand_trig(sp.trigsimp(expression))) == 0


def main() -> int:
    checks = CheckLedger("P182/TX3/C-GW-010")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.133.0.yaml") == RELEASE_SHA256,
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
        "TX3 has no NumPy integration compatibility surface",
        compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "advertised perpendicular linear view has no source predicate",
        "n_perp" not in source_text
        and source_text.count("n_spin") == 2
        and "LINEAR in-plane" in source_text,
    )

    time = sp.Symbol("t", real=True)
    phase = sp.Symbol("psi", real=True)
    q, omega, scale, coupling, distance = sp.symbols(
        "q Omega s G R", nonzero=True, real=True
    )
    inclination, azimuth, frame = sp.symbols(
        "iota phi alpha", real=True
    )
    direct_derivative = perpendicular_axisymmetric_stf_second_derivative(
        q, omega, omega * time, scale
    )
    rotated = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[1, 0, 0],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    checks.check(
        "phase-parametrized second derivative matches direct time differentiation",
        sp.simplify(direct_derivative - rotated.second_derivative) == sp.zeros(3),
    )
    checks.check(
        "the exact source derivative is one pure twice-frequency harmonic",
        _zero(sp.diff(direct_derivative[1, 1], time, 2) + 4 * omega**2 * direct_derivative[1, 1])
        and _zero(sp.diff(direct_derivative[1, 2], time, 2) + 4 * omega**2 * direct_derivative[1, 2]),
    )

    generic = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
        observer_azimuth=azimuth,
        transverse_frame_angle=frame,
        quadrupole_scale=scale,
    )
    triad_gram = sp.Matrix.hstack(
        generic.line_of_sight,
        generic.first_transverse,
        generic.second_transverse,
    ).T * sp.Matrix.hstack(
        generic.line_of_sight,
        generic.first_transverse,
        generic.second_transverse,
    )
    checks.check(
        "observer and transverse frame are oriented orthonormal",
        sp.trigsimp(triad_gram) == sp.eye(3)
        and sp.trigsimp(
            generic.first_transverse.cross(generic.second_transverse)
            - generic.line_of_sight
        )
        == sp.zeros(3, 1),
    )

    common = 12 * coupling * q * omega**2 / distance
    cosine = sp.cos(inclination)
    semimajor = (1 + cosine**2) / 2
    natural = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
        observer_azimuth=azimuth,
        quadrupole_scale=scale,
    )
    harmonic = 2 * (phase - azimuth)
    checks.check(
        "natural-frame generic-observer readouts are exact",
        _zero(
            natural.waveform.conventional_plus
            + common * semimajor * sp.cos(harmonic)
        )
        and _zero(
            natural.waveform.conventional_cross
            + common * cosine * sp.sin(harmonic)
        ),
    )
    expected_matrix = sp.diag(-common * semimajor, -common * cosine)
    checks.check(
        "harmonic coefficient matrix and determinant derive temporal rank",
        sp.trigsimp(natural.coefficient_matrix - expected_matrix) == sp.zeros(2)
        and _zero(
            natural.coefficient_determinant
            - common**2 * cosine * semimajor
        ),
    )
    expected_gram = sp.diag(common**2 * semimajor**2, common**2 * cosine**2)
    checks.check(
        "phase Gram matrix gives the exact ellipse semiaxes",
        sp.trigsimp(natural.phase_gram_matrix - expected_gram) == sp.zeros(2),
    )

    axis = conditional_perpendicular_rotation_polarization(
        q, omega, phase, 0, coupling, distance, quadrupole_scale=scale
    )
    edge = conditional_perpendicular_rotation_polarization(
        q, omega, phase, sp.pi / 2, coupling, distance, quadrupole_scale=scale
    )
    oblique = conditional_perpendicular_rotation_polarization(
        q, omega, phase, sp.pi / 3, coupling, distance, quadrupole_scale=scale
    )
    checks.check(
        "axis edge and oblique views are circular linear and elliptical",
        _zero(axis.phase_gram_matrix[0, 0] - axis.phase_gram_matrix[1, 1])
        and axis.coefficient_determinant != 0
        and _zero(edge.coefficient_determinant)
        and edge.coefficient_matrix[0, 0] != 0
        and edge.coefficient_matrix[1, 1] == 0
        and oblique.coefficient_determinant != 0
        and not _zero(
            oblique.phase_gram_matrix[0, 0]
            - oblique.phase_gram_matrix[1, 1]
        ),
    )
    checks.check(
        "generic nonzero amplitude has rank two exactly off the edge-on great circle",
        _zero(
            natural.coefficient_determinant
            - common**2 * sp.cos(inclination) * (1 + sp.cos(inclination) ** 2) / 2
        )
        and _zero(edge.coefficient_determinant)
        and axis.coefficient_determinant != 0,
    )

    source_sample = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        sp.acos(1 / sp.sqrt(3)),
        coupling,
        distance,
        observer_azimuth=sp.pi / 4,
        quadrupole_scale=scale,
    )
    checks.check(
        "source sample direction is rank two elliptical rather than circular",
        _zero(
            source_sample.coefficient_determinant
            - 2 * common**2 / (3 * sp.sqrt(3))
        )
        and _zero(
            source_sample.phase_gram_matrix[1, 1]
            / source_sample.phase_gram_matrix[0, 0]
            - sp.Rational(3, 4)
        ),
    )

    ratio = sp.simplify(
        natural.waveform.conventional_cross
        / natural.waveform.conventional_plus
    )
    checks.check(
        "fixed-phase ratio cancels common scales only on its domain",
        not ({q, omega, coupling, distance, scale} & ratio.free_symbols)
        and _zero(natural.waveform.conventional_plus.subs(phase, azimuth + sp.pi / 4))
        and not _zero(natural.waveform.conventional_cross.subs(phase, azimuth + sp.pi / 4)),
    )
    fixed_time_ratio = ratio.subs(phase, omega * time)
    checks.check(
        "fixed-physical-time ratio retains angular-speed phase dependence",
        not _zero(sp.diff(fixed_time_ratio, omega)),
    )
    checks.check(
        "angular speed controls amplitude and frequency despite fixed-phase cancellation",
        natural.waveform.waveform_tensor.subs(omega, 0) == sp.zeros(3)
        and natural.source_second_derivative.subs(q, 0) == sp.zeros(3)
        and natural.waveform.conventional_plus.has(omega**2)
        and _zero(
            sp.diff(
                natural.waveform.conventional_plus.subs(phase, omega * time),
                time,
                2,
            )
            + 4
            * omega**2
            * natural.waveform.conventional_plus.subs(phase, omega * time)
        ),
    )

    coordinate_rotation = sp.Matrix(
        [
            [sp.cos(2 * frame), sp.sin(2 * frame)],
            [-sp.sin(2 * frame), sp.cos(2 * frame)],
        ]
    )
    checks.check(
        "transverse-frame rotation is double-angle and preserves ellipse invariants",
        generic.coefficient_matrix == coordinate_rotation * natural.coefficient_matrix
        and generic.phase_gram_matrix == natural.phase_gram_matrix
        and generic.coefficient_determinant == natural.coefficient_determinant,
    )
    shifted = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase + azimuth,
        inclination,
        coupling,
        distance,
        observer_azimuth=azimuth,
        quadrupole_scale=scale,
    )
    unshifted = conditional_perpendicular_rotation_polarization(
        q, omega, phase, inclination, coupling, distance, quadrupole_scale=scale
    )
    checks.check(
        "observer azimuth is an exact orbit-phase shift in the natural frame",
        shifted.waveform.conventional_plus == unshifted.waveform.conventional_plus
        and shifted.waveform.conventional_cross == unshifted.waveform.conventional_cross,
    )

    normalized = conditional_perpendicular_rotation_polarization(
        q, omega, phase, inclination, coupling, distance, quadrupole_scale=1
    )
    triple = conditional_perpendicular_rotation_polarization(
        q, omega, phase, inclination, coupling, distance, quadrupole_scale=3
    )
    checks.check(
        "normalized and triple moment conventions give one conditional waveform",
        triple.source_second_derivative == 3 * normalized.source_second_derivative
        and triple.waveform.waveform_tensor == normalized.waveform.waveform_tensor
        and triple.coefficient_matrix == normalized.coefficient_matrix,
    )

    representative = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        sp.pi / 3,
        coupling,
        distance,
        observer_azimuth=0,
        transverse_frame_angle=sp.pi / 6,
        quadrupole_scale=scale,
    )
    direct_waveform = conditional_scaled_stf_waveform(
        representative.source_second_derivative,
        representative.line_of_sight,
        coupling,
        distance,
        scale,
        representative.first_transverse,
    )
    checks.check(
        "full canonical TT projector independently matches a generic closed readout",
        sp.trigsimp(
            direct_waveform.waveform_tensor
            - representative.waveform.waveform_tensor
        )
        == sp.zeros(3)
        and _zero(
            direct_waveform.conventional_plus
            - representative.waveform.conventional_plus
        )
        and _zero(
            direct_waveform.conventional_cross
            - representative.waveform.conventional_cross
        ),
    )

    source_direction = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    source_basis = tt_polarization_basis(source_direction, [0, 0, 1])
    source_frame_waveform = conditional_scaled_stf_waveform(
        perpendicular_axisymmetric_stf_second_derivative(q, omega, phase, 1),
        source_direction,
        coupling,
        distance,
        1,
        source_basis.first_transverse,
    )
    checks.check(
        "source-frame sample traces share one twice-frequency line",
        _zero(sp.diff(source_frame_waveform.conventional_plus, phase, 2) + 4 * source_frame_waveform.conventional_plus)
        and _zero(sp.diff(source_frame_waveform.conventional_cross, phase, 2) + 4 * source_frame_waveform.conventional_cross)
        and "incommensurate phases" in source_text,
    )

    source_circular_predicate = lambda plus, cross: (
        _zero(sp.diff(plus**2 + cross**2, phase))
        and plus != 0
        and cross != 0
    )
    checks.check(
        "source circular predicate is insensitive without harmonic checks",
        source_circular_predicate(
            axis.waveform.conventional_plus,
            axis.waveform.conventional_cross,
        )
        and source_circular_predicate(sp.Integer(1), sp.Integer(1)),
    )
    plus_only_basis = tt_polarization_basis([1, 0, 0], [0, 1, 0])
    plus_only = plus_only_basis.plus * sp.cos(2 * phase)
    checks.check(
        "transverse tracelessness alone does not prove temporal rank two",
        sp.simplify(sp.Matrix([1, 0, 0]).T * plus_only) == sp.zeros(1, 3)
        and sp.trace(plus_only) == 0
        and sp.Matrix([[1, 0], [0, 0]]).det() == 0,
    )

    conditional_power = conditional_scaled_stf_power(
        rotated.third_derivative, coupling, scale
    )
    checks.check(
        "source power coefficient is an accepted conditional duplicate",
        conditional_power == 288 * coupling * q**2 * omega**6 / 5
        and "P_avg = sp.simplify(sp.Rational(1, 5) * lum)" in source_text,
    )
    module_text = (
        ROOT / "src/substrate_framework/rotating_quadrupole_polarization.py"
    ).read_text(encoding="utf-8")
    checks.check(
        "accepted implementation keeps kinematic and physical ceilings explicit",
        "supplies no source dynamics" in module_text
        and "detector observable" in module_text
        and "fixed-phase scale" in module_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
