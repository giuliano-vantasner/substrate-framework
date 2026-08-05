#!/usr/bin/env python3
"""Independent dyadic and transverse-contraction review of C-GW-010."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(expression: sp.Expr) -> bool:
    return sp.simplify(sp.expand_trig(sp.trigsimp(expression))) == 0


def main() -> int:
    checks = CheckLedger("P182-INDEPENDENT-C-GW-010")
    phase = sp.Symbol("psi", real=True)
    time = sp.Symbol("t", nonzero=True, real=True)
    q, omega, scale, coupling, distance = sp.symbols(
        "q Omega s G R", nonzero=True, real=True
    )
    inclination, azimuth, frame = sp.symbols("iota phi alpha", real=True)

    axis = sp.Matrix([0, -sp.sin(phase), sp.cos(phase)])
    moment = scale * q * (sp.eye(3) - 3 * axis * axis.T)
    second = sp.simplify(omega**2 * sp.diff(moment, phase, 2))
    expected_second = 6 * scale * q * omega**2 * sp.Matrix(
        [
            [0, 0, 0],
            [0, -sp.cos(2 * phase), -sp.sin(2 * phase)],
            [0, -sp.sin(2 * phase), sp.cos(2 * phase)],
        ]
    )
    checks.check(
        "dyadic phase differentiation independently gives the source tensor",
        sp.trigsimp(second - expected_second) == sp.zeros(3),
    )
    checks.check(
        "load-bearing derivative formula rejects normalization and sign mutations",
        sp.trigsimp(3 * second - expected_second) != sp.zeros(3)
        and sp.trigsimp(second / omega - expected_second) != sp.zeros(3)
        and sp.trigsimp(
            second.copy().subs(second[1, 2], -second[1, 2]) - expected_second
        )
        != sp.zeros(3),
    )

    cosine = sp.cos(inclination)
    sine = sp.sin(inclination)
    direction = sp.Matrix(
        [cosine, sine * sp.cos(azimuth), sine * sp.sin(azimuth)]
    )
    meridian = sp.Matrix(
        [sine, -cosine * sp.cos(azimuth), -cosine * sp.sin(azimuth)]
    )
    azimuthal = sp.Matrix([0, sp.sin(azimuth), -sp.cos(azimuth)])
    triad = sp.Matrix.hstack(direction, meridian, azimuthal)
    checks.check(
        "independent observer triad is right-handed orthonormal",
        sp.trigsimp(triad.T * triad) == sp.eye(3)
        and sp.trigsimp(meridian.cross(azimuthal) - direction)
        == sp.zeros(3, 1),
    )

    source_plus = sp.simplify(
        (meridian.dot(second * meridian) - azimuthal.dot(second * azimuthal))
        / 2
    )
    source_cross = sp.simplify(meridian.dot(second * azimuthal))
    prefactor = 2 * coupling / (scale * distance)
    h_plus = sp.trigsimp(prefactor * source_plus)
    h_cross = sp.trigsimp(prefactor * source_cross)
    harmonic = 2 * (phase - azimuth)
    common = 12 * coupling * q * omega**2 / distance
    semimajor = (1 + cosine**2) / 2
    checks.check(
        "direct transverse contractions give the generic natural-frame waveform",
        _zero(h_plus + common * semimajor * sp.cos(harmonic))
        and _zero(h_cross + common * cosine * sp.sin(harmonic)),
    )

    coefficients = sp.Matrix.hstack(
        sp.Matrix([h_plus, h_cross]).subs(phase, azimuth),
        sp.Matrix([h_plus, h_cross]).subs(phase, azimuth + sp.pi / 4),
    )
    expected_coefficients = sp.diag(-common * semimajor, -common * cosine)
    checks.check(
        "quadrature sampling independently derives the coefficient matrix",
        sp.trigsimp(coefficients - expected_coefficients) == sp.zeros(2),
    )
    gram = sp.simplify(coefficients.T * coefficients)
    determinant = sp.trigsimp(sp.expand_trig(coefficients.det()))
    checks.check(
        "determinant and Gram matrix independently derive ellipse invariants",
        _zero(determinant - common**2 * semimajor * cosine)
        and sp.trigsimp(
            gram
            - sp.diag(common**2 * semimajor**2, common**2 * cosine**2)
        )
        == sp.zeros(2),
    )
    checks.check(
        "circularity defect is a perfect square and edge-on rank is one",
        _zero(semimajor**2 - cosine**2 - (1 - cosine**2) ** 2 / 4)
        and _zero(determinant.subs(inclination, sp.pi / 2))
        and not _zero(coefficients[0, 0].subs(inclination, sp.pi / 2))
        and _zero(
            (semimajor**2 - cosine**2).subs(inclination, 0)
        ),
    )

    sample_cosine = 1 / sp.sqrt(3)
    sample_major_squared = common**2 * (1 + sample_cosine**2) ** 2 / 4
    sample_minor_squared = common**2 * sample_cosine**2
    checks.check(
        "the source sample direction has exact noncircular ellipse ratio",
        _zero(sample_minor_squared / sample_major_squared - sp.Rational(3, 4)),
    )

    ratio = sp.simplify(h_cross / h_plus)
    checks.check(
        "fixed-phase ratio cancels scales but retains phase poles",
        not ({q, omega, coupling, distance, scale} & ratio.free_symbols)
        and _zero(h_plus.subs(phase, azimuth + sp.pi / 4))
        and not _zero(h_cross.subs(phase, azimuth + sp.pi / 4)),
    )
    checks.check(
        "fixed-time substitution restores exact angular-speed dependence",
        not _zero(sp.diff(ratio.subs(phase, omega * time), omega)),
    )

    coordinate_rotation = sp.Matrix(
        [
            [sp.cos(2 * frame), sp.sin(2 * frame)],
            [-sp.sin(2 * frame), sp.cos(2 * frame)],
        ]
    )
    rotated_coefficients = coordinate_rotation * coefficients
    checks.check(
        "independent double-angle frame rotation preserves singular values",
        sp.trigsimp(
            rotated_coefficients.T * rotated_coefficients - gram
        )
        == sp.zeros(2)
        and _zero(rotated_coefficients.det() - determinant),
    )

    representative = {
        inclination: sp.pi / 3,
        azimuth: 0,
        frame: sp.pi / 6,
    }
    rep_direction = direction.subs(representative)
    rep_meridian = meridian.subs(representative)
    rep_azimuthal = azimuthal.subs(representative)
    rep_first = (
        sp.cos(2 * frame / 2) * rep_meridian
        + sp.sin(2 * frame / 2) * rep_azimuthal
    ).subs(representative)
    rep_second = rep_direction.cross(rep_first)
    projector = sp.eye(3) - rep_direction * rep_direction.T
    projected = sp.simplify(
        projector * second * projector
        - projector * sp.trace(projector * second * projector) / 2
    )
    rep_plus = sp.simplify(
        (rep_first.dot(projected * rep_first) - rep_second.dot(projected * rep_second))
        / 2
    )
    rep_cross = sp.simplify(rep_first.dot(projected * rep_second))
    rotated_coordinates = (
        coordinate_rotation * sp.Matrix([source_plus, source_cross])
    ).subs(representative)
    checks.check(
        "separate full projector reconstruction matches direct contractions",
        _zero(rep_plus - rotated_coordinates[0])
        and _zero(rep_cross - rotated_coordinates[1])
        and sp.simplify(rep_direction.T * projected) == sp.zeros(1, 3)
        and _zero(sp.trace(projected)),
    )

    triple_second = second.subs(scale, 3)
    normalized_wave = sp.simplify(2 * coupling * second.subs(scale, 1) / distance)
    triple_wave = sp.simplify(2 * coupling * triple_second / (3 * distance))
    checks.check(
        "independent convention rescaling leaves the conditional tensor unchanged",
        sp.simplify(triple_second - 3 * second.subs(scale, 1)) == sp.zeros(3)
        and sp.simplify(triple_wave - normalized_wave) == sp.zeros(3),
    )

    proportional_plus = sp.cos(2 * phase)
    proportional_cross = 2 * sp.cos(2 * phase)
    checks.check(
        "two instantaneous nonzeros do not imply temporal rank two",
        proportional_plus.subs(phase, 0) != 0
        and proportional_cross.subs(phase, 0) != 0
        and sp.Matrix([[1, 0], [2, 0]]).det() == 0
        and _zero(sp.diff(proportional_cross / proportional_plus, phase)),
    )
    circular_proxy = lambda plus, cross: (
        _zero(sp.diff(plus**2 + cross**2, phase))
        and plus != 0
        and cross != 0
    )
    checks.check(
        "source circular proxy admits a static false positive",
        circular_proxy(sp.cos(2 * phase), sp.sin(2 * phase))
        and circular_proxy(sp.Integer(1), sp.Integer(1)),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
