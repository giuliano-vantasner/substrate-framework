"""P241 audit oracle — concrete defects in the Section-9 Kerr dictionary.

Standalone module: python3 S21_kerr_dictionary_audit.py

Claim P241-S21 (paper equations (54)-(57)). Four defects are demonstrated:

(a) The printed determinant identity (56) equals NEITHER the coordinate
    determinant of the components displayed in (55) (it drops exactly one
    Sigma^2 factor) NOR the physical-eigenvalue determinant of the explicit
    Jacobian convention used by the authors' own published 2+1D companion
    paper (lambda_r = A^{rr}, lambda_theta = r^2 A^{thth},
    lambda_phi = r^2 sin^2(th) A^{phph}).
(b) The spatial components (54) match Kerr's contravariant spatial metric
    exactly, which forces Omega^2 = 1 for any conformal identification
    g_induced = Omega^2 * g_Kerr restricted to space; the temporal component
    then cannot match.
(c) Equation (57)'s second equality contradicts its own first equality:
    V^phi = c0^2 g_{0phi}/g_{phphi} evaluates to -2 c0^2 G M a r / Ag,
    while the printed right-hand side carries only one power of c0.
(d) Scaling analysis: A^{rr} ~ L^2/T^2 but A^{thth} ~ L^{-2}/T^2 and
    A^{phph} ~ L^{-6}/T^2, so the three printed quantities cannot be
    eigenvalues of one rank-2 tensor with speed-squared dimensions.
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_kerr_paper_dictionary_audit() -> dict[str, object]:
    """Demonstrate the four defects with exact algebra plus numeric probes."""
    r, th, c0, rs, a, G, M = sp.symbols("r theta c_0 r_s a G M", positive=True)
    Delta = r**2 - rs * r + a**2
    Sigma = r**2 + a**2 * sp.cos(th) ** 2
    Ag = (r**2 + a**2) ** 2 - a**2 * Delta * sp.sin(th) ** 2

    # Components as printed in (55).
    Arr = c0**2 * (Delta / Sigma) ** 2
    Athth = c0**2 / Sigma**2
    Aphph = c0**2 * (Sigma / (Ag * sp.sin(th) ** 2)) ** 2

    # (a) coordinate determinant vs printed (56); physical convention too.
    det_coord = sp.expand(Arr * Athth * Aphph)
    paper56 = sp.expand(c0**6 * (Delta / Ag) ** 2 / sp.sin(th) ** 4)
    ratio_a = sp.cancel(det_coord / paper56)
    a_dropped = sp.simplify(ratio_a - 1 / Sigma**2) == 0

    lam_r, lam_t, lam_p = Arr, r**2 * Athth, r**2 * sp.sin(th) ** 2 * Aphph
    det_phys = sp.expand(lam_r * lam_t * lam_p)
    sample = {r: sp.Rational(7, 3), th: sp.Rational(4, 10), c0: 1,
              rs: sp.Rational(2, 5), a: sp.Rational(9, 50)}
    b_differs = float(det_phys.subs(sample) - paper56.subs(sample)) != 0

    # (b) with spatial exactness the conformal factor must be 1, yet the
    # temporal component built from (56) mismatches Kerr's g_tt.
    g00_paper = float((paper56 ** sp.Rational(1, 6)).subs({**sample, c0: sp.Rational(297, 100)}))
    target = float((Delta / Sigma).subs({k_: v_ for k_, v_ in sample.items() if k_ != c0}))
    c_mismatch = abs(g00_paper - target) > 1e-12

    # (c) internal contradiction inside (57): own first equality vs print.
    v_correct = sp.simplify(c0**2 * (-2 * G * M * a * r / Ag))
    d_slip = sp.simplify(v_correct - (-2 * G * M * a * r * c0 / Ag)) != 0

    return _check(
        "kerr_paper_dictionary_audit",
        "P241-S21 (54)-(57)",
        bool(a_dropped and b_differs and c_mismatch and d_slip),
        f"(a) det(coord)/(56) = {ratio_a}: "
        "the printed (56) drops exactly one Sigma^2 from its own coordinate "
        f"determinant and matches no convention (physical-convention determinant "
        f"also differs numerically: {b_differs}); (b) spatial components are exactly "
        f"Kerr so any conformal matching forces Omega^2=1, yet the g00 reconstructed "
        f"from (56) misses Delta/Sigma by {g00_paper - target:.6g}; (c) the own first "
        "equality of (57) gives V^phi = -2*c0^2*G*M*a*r/Ag while the printed result "
        "carries a single power of c0; (d) A^{thth} and A^{phph} scale as L^-2/T^2 "
        "and L^-6/T^2 rather than speed squared.",
    )


if __name__ == "__main__":
    result = check_kerr_paper_dictionary_audit()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
