"""Machine checks for docs/tutorials/einbein_3plus1D/einbein_3plus1D_tutorial.md.

Every test name carries the equation number(s) of the tutorial it backs, per the
no-freestyle-writing rule (tracker #32). Derivable claims are checked here;
literature theorems are cited in the document and, where they admit a numerical
form, illustrated here.

Run: .venv/bin/python -m pytest tests/test_einbein_3plus1d_tutorial.py
"""

import re
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.lorentz_little_groups import little_group_algebra_3plus1
from substrate_framework.lorentz_orbits import unit_timelike_vector_orbit_metric
from substrate_framework.relativistic_particle import (
    einbein_hamiltonian_ledger,
    massive_einbein_ledger,
    massive_mass_term_weyl_change,
    massless_worldline_weyl_residual,
    worldline_reparametrization_residual,
)

DIM = 4  # 3+1 spacetime dimensions

TUTORIAL_DIR = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "tutorials"
    / "einbein_3plus1D"
)


def _random_metric_data(rng):
    while True:
        A = rng.normal(size=(DIM, DIM))
        g = (A + A.T) / 2 + np.diag(rng.normal(size=DIM))
        if abs(np.linalg.det(g)) > 1e-3:
            break
    gi = np.linalg.inv(g)
    dg = rng.normal(size=(DIM, DIM, DIM))
    dg = (dg + np.transpose(dg, (0, 2, 1))) / 2
    return g, gi, dg


def _christoffel_general(gi, dg, sigma, rho, nu):
    """Eq. (49): the general formula, evaluated numerically."""
    return 0.5 * sum(
        gi[sigma, lam]
        * (dg[rho, lam, nu] + dg[nu, lam, rho] - dg[lam, rho, nu])
        for lam in range(DIM)
    )


# ---------------------------------------------------------------------------
# Eq. (5): determinant sign from the signature
# ---------------------------------------------------------------------------


def test_eq005_determinant_negative_for_lorentzian_3plus1():
    rng = np.random.default_rng(0)
    eta = np.diag([-1.0, 1, 1, 1])
    for _ in range(20):
        # random Lorentzian metric: eta conjugated by a random invertible matrix
        B = rng.normal(size=(DIM, DIM)) + np.eye(DIM) * 2
        g = B @ eta @ B.T
        assert np.linalg.det(g) < 0
        sig = np.linalg.eigvalsh(g)
        assert (sig < 0).sum() == 1 and (sig > 0).sum() == 3


# ---------------------------------------------------------------------------
# Eqs. (20)-(30): einbein constraint, root, square-root recovery
# ---------------------------------------------------------------------------


def test_eq020_026_einbein_constraint_and_root():
    e, m, c0 = sp.symbols("e m c0", positive=True)
    sigma_s = sp.symbols("sigma_s")
    L = sigma_s / (2 * e) - e * (m * c0) ** 2 / 2
    dLde = sp.diff(L, e)
    assert sp.simplify(dLde - (-sigma_s / (2 * e**2) - (m * c0) ** 2 / 2)) == 0
    sol_e = sp.solve(sp.Eq(dLde, 0), e)
    e_root = sp.sqrt(-sigma_s) / (m * c0)
    assert any(sp.simplify(s - e_root) == 0 for s in sol_e)
    assert any(sp.simplify(s + e_root) == 0 for s in sol_e)


def test_eq027_030_sqrt_recovery():
    e, m, c0 = sp.symbols("e m c0", positive=True)
    sigma_s = sp.symbols("sigma_s", negative=True)
    L = sigma_s / (2 * e) - e * (m * c0) ** 2 / 2
    L_on_shell = L.subs(sigma_s, -(e**2) * (m * c0) ** 2)
    assert sp.simplify(L_on_shell - (-e * (m * c0) ** 2)) == 0
    L_recovered = L_on_shell.subs(e, sp.sqrt(-sigma_s) / (m * c0))
    assert sp.simplify(L_recovered - (-m * c0 * sp.sqrt(-sigma_s))) == 0
    canonical = massive_einbein_ledger(sigma_s, e, m, c0)
    assert sp.simplify(
        canonical.recovered_square_root_lagrangian - L_recovered
    ) == 0


# ---------------------------------------------------------------------------
# Eqs. (33)-(48): coordinate EL equation to Christoffel form
# ---------------------------------------------------------------------------


def test_eq033_momentum_and_eq035_coordinate_derivative():
    rng = np.random.default_rng(1)
    g, gi, dg = _random_metric_data(rng)
    xd = rng.normal(size=DIM)
    e = 1.7
    # Eq. (33): dL/dxd^lam = g_{lam nu} xd^nu / e (finite difference)
    eps = 1e-7
    for lam in range(DIM):
        fd = (
            np.einsum("mn,m,n", g, xd + eps * np.eye(DIM)[lam], xd + eps * np.eye(DIM)[lam])
            - np.einsum("mn,m,n", g, xd - eps * np.eye(DIM)[lam], xd - eps * np.eye(DIM)[lam])
        ) / (4 * eps * e)
        analytic = (g[lam] @ xd) / e
        assert abs(fd - analytic) < 1e-6
    # Eq. (35): dL/dx^lam = (1/2e) (d_lam g_{mu nu}) xd^mu xd^nu — verified by
    # finite-differencing the Lagrangian's x-dependence through g.
    eps = 1e-7
    for lam in range(DIM):
        analytic = 0.5 / e * np.einsum("mn,m,n", dg[lam], xd, xd)
        gp = g + eps * dg[lam]
        gm = g - eps * dg[lam]
        fd = (np.einsum("mn,m,n", gp, xd, xd) - np.einsum("mn,m,n", gm, xd, xd)) / (
            4 * eps * e
        )
        assert abs(analytic - fd) < 1e-6


def test_eq036_to_048_el_expansion_matches_christoffel_form():
    rng = np.random.default_rng(2)
    g, gi, dg = _random_metric_data(rng)
    xd = rng.normal(size=DIM)
    e, ed = 1.3, 0.7
    xdd_from_el = -gi @ np.array(
        [
            xd @ dg[:, lam, :] @ xd
            - 0.5 * np.einsum("mn,m,n", dg[lam], xd, xd)
            - (ed / e) * (g[lam] @ xd)
            for lam in range(DIM)
        ]
    )
    Gamma = np.array(
        [
            [[_christoffel_general(gi, dg, s, r, n) for n in range(DIM)] for r in range(DIM)]
            for s in range(DIM)
        ]
    )
    xdd_christoffel = -np.einsum("srn,r,n", Gamma, xd, xd) + (ed / e) * xd
    np.testing.assert_allclose(xdd_from_el, xdd_christoffel, atol=1e-10)


# ---------------------------------------------------------------------------
# Appendix A: the forty printed components
# ---------------------------------------------------------------------------


def _printed_bracket_value(lam, rho, nu, dg):
    """Numeric value of the simplified bracket as printed by the generator."""
    if rho == nu:
        if lam == rho:
            return dg[rho, rho, rho]
        return 2 * dg[rho, lam, rho] - dg[lam, rho, rho]
    if lam == rho:
        return dg[nu, rho, rho]
    if lam == nu:
        return dg[rho, nu, nu]
    return dg[rho, lam, nu] + dg[nu, lam, rho] - dg[lam, rho, nu]


def test_appendixA_all_40_components_match_general_formula():
    rng = np.random.default_rng(3)
    g, gi, dg = _random_metric_data(rng)
    count = 0
    for sigma in range(DIM):
        for rho in range(DIM):
            for nu in range(rho, DIM):
                printed = 0.5 * sum(
                    gi[sigma, lam] * _printed_bracket_value(lam, rho, nu, dg)
                    for lam in range(DIM)
                )
                general = _christoffel_general(gi, dg, sigma, rho, nu)
                assert abs(printed - general) < 1e-10, (
                    f"Gamma^{sigma}_{rho}{nu} mismatch"
                )
                count += 1
    assert count == 40


def test_appendixA_document_block_matches_generator():
    """The Christoffel block in the .md is byte-identical to the generator
    output (text-to-proof agreement for the lookup table)."""
    import sys

    sys.path.insert(0, str(TUTORIAL_DIR))
    from generate_christoffel_block import generate_block

    text = (TUTORIAL_DIR / "einbein_3plus1D_tutorial.md").read_text()
    pat = re.compile(
        r"<!-- BEGIN GENERATED CHRISTOFFELS -->.*<!-- END GENERATED CHRISTOFFELS -->",
        re.S,
    )
    m = pat.search(text)
    assert m, "generated block not found in document"
    assert m.group(0) == generate_block()


# ---------------------------------------------------------------------------
# Section 12.1: metric compatibility / norm preservation
# ---------------------------------------------------------------------------


def test_sec12_norm_preservation_identity():
    rng = np.random.default_rng(4)
    g, gi, dg = _random_metric_data(rng)
    xd = rng.normal(size=DIM)
    xdd = rng.normal(size=DIM)
    Gamma = np.array(
        [
            [[_christoffel_general(gi, dg, s, r, n) for n in range(DIM)] for r in range(DIM)]
            for s in range(DIM)
        ]
    )
    d_dtau = np.einsum("rmn,r,m,n", dg, xd, xd, xd) + 2 * np.einsum(
        "mn,m,n", g, xd, xdd
    )
    cov = xdd + np.einsum("srn,r,n", Gamma, xd, xd)
    rhs = 2 * np.einsum("mn,m,n", g, xd, cov)
    assert abs(d_dtau - rhs) < 1e-9


# ---------------------------------------------------------------------------
# Eqs. (61)-(62): the celestial sphere
# ---------------------------------------------------------------------------


def test_eq061_062_celestial_sphere_parametrization():
    th, ph, x0d = sp.symbols("theta phi x0d", real=True)
    v = sp.Matrix(
        [x0d, x0d * sp.sin(th) * sp.cos(ph), x0d * sp.sin(th) * sp.sin(ph), x0d * sp.cos(th)]
    )
    eta = sp.diag(-1, 1, 1, 1)
    assert sp.simplify((v.T * eta * v)[0]) == 0


def test_eq061_062_completeness_of_sphere():
    rng = np.random.default_rng(5)
    eta = np.diag([-1.0, 1, 1, 1])
    for _ in range(50):
        th = rng.uniform(0, np.pi)
        ph = rng.uniform(0, 2 * np.pi)
        x0d = rng.uniform(0.1, 10)
        v = np.array(
            [x0d, x0d * np.sin(th) * np.cos(ph), x0d * np.sin(th) * np.sin(ph), x0d * np.cos(th)]
        )
        assert abs(v @ eta @ v) < 1e-10
        assert abs(np.linalg.norm(v[1:]) / v[0] - 1) < 1e-12


# ---------------------------------------------------------------------------
# Eqs. (63)-(68): little groups in 3+1D
# ---------------------------------------------------------------------------

_ETA4 = np.diag([-1.0, 1, 1, 1])


def _K(i):
    M = np.zeros((4, 4))
    M[0, i] = 1
    M[i, 0] = 1
    return M


_J1 = np.array(
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]], float
)
_J2 = np.array(
    [[0, 0, 0, 0], [0, 0, 0, -1], [0, 0, 0, 0], [0, 1, 0, 0]], float
)
_J3 = np.array(
    [[0, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 0]], float
)
_T1 = _K(1) + _J2
_T2 = _K(2) - _J1
_K0 = np.array([1.0, 0, 0, 1])


def _comm(A, B):
    return A @ B - B @ A


def test_eq065_generators_are_so31_valued():
    for M in (_T1, _T2, _J3):
        etaM = _ETA4 @ M
        np.testing.assert_allclose(etaM + etaM.T, np.zeros((4, 4)), atol=1e-15)


def test_eq065_printed_matrices_match_definitions():
    """The matrices printed in Eq. (65) are exactly K1+J2, K2-J1, J3."""
    T1_printed = np.array(
        [[0, 1, 0, 0], [1, 0, 0, -1], [0, 0, 0, 0], [0, 1, 0, 0]], float
    )
    T2_printed = np.array(
        [[0, 0, 1, 0], [0, 0, 0, 0], [1, 0, 0, -1], [0, 0, 1, 0]], float
    )
    J3_printed = np.array(
        [[0, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 0]], float
    )
    np.testing.assert_allclose(T1_printed, _T1, atol=1e-15)
    np.testing.assert_allclose(T2_printed, _T2, atol=1e-15)
    np.testing.assert_allclose(J3_printed, _J3, atol=1e-15)
    canonical = little_group_algebra_3plus1().massless_generators
    for printed, generated in zip((T1_printed, T2_printed, J3_printed), canonical):
        np.testing.assert_array_equal(printed, np.array(generated, dtype=float))


def test_eq066_generators_fix_standard_null_vector():
    for M in (_T1, _T2, _J3):
        np.testing.assert_allclose(M @ _K0, np.zeros(4), atol=1e-15)


def test_eq067_e2_algebra():
    """The printed commutators: [J3,T1] = -T2, [J3,T2] = +T1, [T1,T2] = 0."""
    np.testing.assert_allclose(_comm(_J3, _T1), -_T2, atol=1e-15)
    np.testing.assert_allclose(_comm(_J3, _T2), _T1, atol=1e-15)
    np.testing.assert_allclose(_comm(_T1, _T2), np.zeros((4, 4)), atol=1e-15)


def test_eq064_massive_little_group_is_so3():
    """Among the so(3,1) basis {J1,J2,J3,K1,K2,K3}, exactly the Ji fix the
    rest momentum, and they close into so(3)."""
    p0 = np.array([1.0, 0, 0, 0])
    for J in (_J1, _J2, _J3):
        np.testing.assert_allclose(J @ p0, np.zeros(4), atol=1e-15)
    for i in (1, 2, 3):
        assert np.linalg.norm(_K(i) @ p0) > 0.5
    # closure (sign convention of the printed generators: [Ji,Jj] = -eps_ijk Jk)
    np.testing.assert_allclose(_comm(_J1, _J2), -_J3, atol=1e-15)
    np.testing.assert_allclose(_comm(_J2, _J3), -_J1, atol=1e-15)
    np.testing.assert_allclose(_comm(_J3, _J1), -_J2, atol=1e-15)


def test_sec10_transitivity_on_shells_3plus1():
    from scipy.linalg import expm

    rng = np.random.default_rng(6)
    for _ in range(10):
        m = rng.uniform(0.5, 3)
        a = rng.uniform(0, 2)
        th = rng.uniform(0, np.pi)
        ph = rng.uniform(0, 2 * np.pi)
        p = np.array(
            [m * np.cosh(a),
             m * np.sinh(a) * np.sin(th) * np.cos(ph),
             m * np.sinh(a) * np.sin(th) * np.sin(ph),
             m * np.sinh(a) * np.cos(th)]
        )
        # rotate azimuth to zero (J3 by +ph), then polar angle to zero
        # (J2 by +th), then boost along the 3-axis by -a to reach rest
        T = expm(-a * _K(3)) @ expm(th * _J2) @ expm(ph * _J3)
        np.testing.assert_allclose(T @ p, np.array([m, 0, 0, 0]), atol=1e-9)


# ---------------------------------------------------------------------------
# Eqs. (69)-(70): representation dimensions (cited theorems, numeric form)
# ---------------------------------------------------------------------------


def test_eq069_su2_representation_dimension():
    """The dimension 2s+1 is the number of J3 eigenvalues -s..s; verified here
    for s in {0, 1/2, 1, 3/2, 2} via the explicit spin-s J3 matrix."""
    for two_s in range(5):
        s = two_s / 2
        dim = int(round(2 * s + 1))
        mvals = np.arange(-s, s + 1, 1.0)
        assert len(mvals) == dim
        J3s = np.diag(mvals)
        assert J3s.shape == (dim, dim)


# ---------------------------------------------------------------------------
# Eqs. (71)-(73): Hamiltonian
# ---------------------------------------------------------------------------


def test_eq071_073_hamiltonian_pure_constraint():
    e, m, c0 = sp.symbols("e m c0", positive=True)
    syms = sp.symbols(
        "g00 g01 g02 g03 g11 g12 g13 g22 g23 g33"
    )
    g = sp.zeros(4)
    idx = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
    for s, (i, j) in zip(syms, idx):
        g[i, j] = s
        g[j, i] = s
    gi = sp.simplify(g.inv())
    xd = sp.Matrix(sp.symbols("xd0 xd1 xd2 xd3"))
    p = sp.Matrix(sp.symbols("p0 p1 p2 p3"))
    sigma = (xd.T * g * xd)[0]
    L = sigma / (2 * e) - e * (m * c0) ** 2 / 2
    xd_from_p = e * gi * p
    assert sp.simplify((g * xd_from_p)[0] / e - p[0]) == 0
    H = (p.T * xd_from_p)[0] - L.subs({xd[i]: xd_from_p[i] for i in range(DIM)})
    H_claimed = e / 2 * ((p.T * gi * p)[0] + (m * c0) ** 2)
    assert sp.simplify(H - H_claimed) == 0
    concrete_p = sp.Matrix(sp.symbols("q0:4", real=True))
    canonical = einbein_hamiltonian_ledger(
        sp.diag(-1, 2, 3, 4), concrete_p, e, m, c0
    )
    assert canonical.legendre_transform == canonical.hamiltonian


# ---------------------------------------------------------------------------
# Eq. (12) reparametrization invariance; Eq. (79) Weyl invariance
# ---------------------------------------------------------------------------


def test_eq012_reparametrization_invariance():
    e, fdot, sigma, m, c0 = sp.symbols("e fdot sigma m c0", positive=True)
    integrand_old = sigma / (2 * e) - e * (m * c0) ** 2 / 2
    integrand_new_times_jac = sp.simplify(
        ((sigma / fdot**2) / (2 * e / fdot) - (e / fdot) * (m * c0) ** 2 / 2) * fdot
    )
    assert sp.simplify(integrand_new_times_jac - integrand_old) == 0
    assert worldline_reparametrization_residual(
        sigma, e, m, c0, fdot
    ) == 0


def test_eq079_weyl_invariance():
    Om, e, sigma, m, c0 = sp.symbols("Omega e sigma m c0", positive=True)
    massless = sigma / (2 * e)
    assert sp.simplify(
        massless.subs({sigma: Om**2 * sigma, e: Om**2 * e}) - massless
    ) == 0
    mass_term = -e * (m * c0) ** 2 / 2
    assert sp.simplify(mass_term.subs(e, Om**2 * e) - Om**2 * mass_term) == 0
    assert massless_worldline_weyl_residual(sigma, e, Om) == 0
    assert massive_mass_term_weyl_change(e, m, c0, Om) != 0


# ---------------------------------------------------------------------------
# Section 10.1: induced metric on the massive shell H^3 is positive-definite
# ---------------------------------------------------------------------------


def test_sec101_hyperboloid_induced_metric_positive_definite_3plus1():
    eta_symbol, theta_symbol = sp.symbols("eta theta", positive=True)
    assert unit_timelike_vector_orbit_metric(4) == sp.diag(
        1,
        sp.sinh(eta_symbol) ** 2,
        sp.sinh(eta_symbol) ** 2 * sp.sin(theta_symbol) ** 2,
    )
    rng = np.random.default_rng(7)
    eta = np.diag([-1.0, 1, 1, 1])
    for _ in range(20):
        a = rng.uniform(0, 3)
        th = rng.uniform(0.01, np.pi - 0.01)
        ph = rng.uniform(0, 2 * np.pi)

        def p(a, th, ph):
            return np.array(
                [np.cosh(a),
                 np.sinh(a) * np.sin(th) * np.cos(ph),
                 np.sinh(a) * np.sin(th) * np.sin(ph),
                 np.sinh(a) * np.cos(th)]
            )

        eps = 1e-6
        pa = (p(a + eps, th, ph) - p(a - eps, th, ph)) / (2 * eps)
        pt = (p(a, th + eps, ph) - p(a, th - eps, ph)) / (2 * eps)
        pp = (p(a, th, ph + eps) - p(a, th, ph - eps)) / (2 * eps)
        induced = np.array(
            [[u @ eta @ v for v in (pa, pt, pp)] for u in (pa, pt, pp)]
        )
        assert np.all(np.linalg.eigvalsh(induced) > 0)


# ---------------------------------------------------------------------------
# Review-round coverage additions (independent review, PR round 1)
# ---------------------------------------------------------------------------


def test_eq050_051_covariant_form_equivalence():
    """Eq. (51) <=> Eq. (50): e * D(xd^sigma / e)/dtau = xdd + Gamma xd xd
    - (ed/e) xd."""
    rng = np.random.default_rng(21)
    g, gi, dg = _random_metric_data(rng)
    xd = rng.normal(size=DIM)
    xdd = rng.normal(size=DIM)
    e, ed = 1.3, 0.7
    Gamma = np.array(
        [
            [[_christoffel_general(gi, dg, s, r, n) for n in range(DIM)] for r in range(DIM)]
            for s in range(DIM)
        ]
    )
    d_xd_over_e = xdd / e - (ed / e**2) * xd
    cov = d_xd_over_e + np.einsum("srn,r,n", Gamma, xd, xd / e)
    np.testing.assert_allclose(
        e * cov, xdd + np.einsum("srn,r,n", Gamma, xd, xd) - (ed / e) * xd, atol=1e-10
    )


def test_eq057_060_massless_chain():
    """The m = 0 specialization: dL/de = 0 gives the null constraint (58), and
    the coordinate EL equation collapses to (59) with the same Christoffels;
    in the gauge ed = 0 this is the affine null-geodesic system (60)."""
    e = sp.symbols("e", positive=True)
    sigma_s = sp.symbols("sigma_s")
    L0 = sigma_s / (2 * e)  # Eq. (56)
    assert sp.simplify(sp.diff(L0, e) - (-sigma_s / (2 * e**2))) == 0
    # dL/de = 0 with e > 0 forces sigma = 0 (the null constraint)
    assert sp.solve(sp.Eq(sp.diff(L0, e), 0), sigma_s) == [0]
    # numeric: flat metric, null straight line satisfies (60)
    rng = np.random.default_rng(22)
    eta = np.diag([-1.0, 1, 1, 1])
    for _ in range(20):
        th = rng.uniform(0, np.pi)
        ph = rng.uniform(0, 2 * np.pi)
        kap = rng.uniform(0.1, 5)
        k0 = kap * np.array(
            [1.0, np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)]
        )
        assert abs(k0 @ eta @ k0) < 1e-12  # (58) / (60) right eq
        # in flat space Gamma = 0, so (60) left eq is xdd = 0, solved by the
        # straight null line x(tau) = x0 + k0 tau of Eq. (78): check the
        # second finite difference vanishes
        x0 = rng.normal(size=DIM)
        tau, h = rng.uniform(-3, 3), 1e-3
        xdd_fd = (x0 + k0 * (tau + h) - 2 * (x0 + k0 * tau) + x0 + k0 * (tau - h)) / h**2
        np.testing.assert_allclose(xdd_fd, np.zeros(DIM), atol=1e-8)


def test_sec101_null_shell_transitivity_3plus1():
    """Any future-null vector maps to (kappa, 0, 0, kappa) by rotations alone."""
    from scipy.linalg import expm

    rng = np.random.default_rng(23)
    for _ in range(50):
        th = rng.uniform(0, np.pi)
        ph = rng.uniform(0, 2 * np.pi)
        kap = rng.uniform(0.1, 5)
        k = kap * np.array(
            [1.0, np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)]
        )
        T = expm(th * _J2) @ expm(ph * _J3)
        np.testing.assert_allclose(T @ k, np.array([kap, 0, 0, kap]), atol=1e-9)


def test_eq076_078_flat_space_solutions():
    rng = np.random.default_rng(24)
    eta = np.diag([-1.0, 1, 1, 1])
    e, m, c0 = 1.5, 0.8, 2.0
    for _ in range(20):
        a = rng.uniform(0, 2)
        th = rng.uniform(0, np.pi)
        ph = rng.uniform(0, 2 * np.pi)
        u0 = e * m * c0 * np.array(
            [np.cosh(a),
             np.sinh(a) * np.sin(th) * np.cos(ph),
             np.sinh(a) * np.sin(th) * np.sin(ph),
             np.sinh(a) * np.cos(th)]
        )
        assert abs(u0 @ eta @ u0 + (e * m * c0) ** 2) < 1e-9  # Eq. (76)
        kap = rng.uniform(0.1, 5)
        k0 = kap * np.array(
            [1.0, np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)]
        )
        assert abs(k0 @ eta @ k0) < 1e-12 and k0[0] > 0  # Eq. (78)
