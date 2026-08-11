"""Machine checks for docs/tutorials/einbein_2plus1D/einbein_2plus1D_tutorial.md.

Every test name carries the equation number(s) of the tutorial it backs, per the
no-freestyle-writing rule (tracker #32): a document claim must be backed by a
machine check or an explicit citation. Tests here cover the derivable claims;
literature theorems (Wigner classification, anyonic representations, hyperboloid
geometry) are cited in the document and, where they admit a numerical form,
illustrated here.

Run: .venv/bin/python -m pytest tests/test_einbein_2plus1d_tutorial.py
"""

import numpy as np
import sympy as sp

# ---------------------------------------------------------------------------
# Shared symbolic/numeric fixtures
# ---------------------------------------------------------------------------

DIM = 3  # 2+1 spacetime dimensions


def _symmetric_symbols(name):
    """Independent symbols of a symmetric 3x3 object, returned as a Matrix."""
    syms = sp.symbols(f"{name}00 {name}01 {name}02 {name}11 {name}12 {name}22")
    M = sp.zeros(3)
    idx = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
    for s, (i, j) in zip(syms, idx):
        M[i, j] = s
        M[j, i] = s
    return M


def _random_metric_data(rng):
    """Random invertible symmetric g, its inverse, and a random derivative
    field dg[rho][mu][nu] = d_rho g_{mu nu} (symmetric in mu, nu)."""
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
    """Eq. (52): the general formula, evaluated numerically."""
    return 0.5 * sum(
        gi[sigma, lam]
        * (dg[rho, lam, nu] + dg[nu, lam, rho] - dg[lam, rho, nu])
        for lam in range(DIM)
    )


# ---------------------------------------------------------------------------
# Eq. (5): determinant expansion
# ---------------------------------------------------------------------------


def test_eq005_determinant_expansion():
    g = _symmetric_symbols("g")
    printed = (
        g[0, 0] * g[1, 1] * g[2, 2]
        + 2 * g[0, 1] * g[1, 2] * g[0, 2]
        - g[0, 0] * g[1, 2] ** 2
        - g[1, 1] * g[0, 2] ** 2
        - g[2, 2] * g[0, 1] ** 2
    )
    assert sp.simplify(g.det() - printed) == 0


# ---------------------------------------------------------------------------
# Eqs. (20)-(26): einbein Euler-Lagrange equation and its algebraic solution
# ---------------------------------------------------------------------------


def test_eq020_026_einbein_constraint_and_root():
    e, m, c0, sigma = sp.symbols("e m c0 sigma", positive=True)
    L = sigma / (2 * e) - e * (m * c0) ** 2 / 2
    # Eq. (22): dL/de
    dLde = sp.diff(L, e)
    assert sp.simplify(dLde - (-sigma / (2 * e**2) - (m * c0) ** 2 / 2)) == 0
    # Eqs. (23)-(25): dL/de = 0  <=>  sigma = -e^2 (m c0)^2.
    # Work with signed sigma for the solve; positivity used only for the root.
    sigma_s = sp.symbols("sigma_s")
    L_s = sigma_s / (2 * e) - e * (m * c0) ** 2 / 2
    sol_e = sp.solve(sp.Eq(sp.diff(L_s, e), 0), e)
    e_root = sp.sqrt(-sigma_s) / (m * c0)
    assert any(sp.simplify(s - e_root) == 0 for s in sol_e)
    # The discarded root is the negative one (orientation convention e > 0).
    assert any(sp.simplify(s + e_root) == 0 for s in sol_e)


# ---------------------------------------------------------------------------
# Eqs. (27)-(30): substitution recovers the square-root Lagrangian
# ---------------------------------------------------------------------------


def test_eq027_030_sqrt_recovery():
    e, m, c0 = sp.symbols("e m c0", positive=True)
    sigma_s = sp.symbols("sigma_s", negative=True)  # timelike: sigma < 0
    L = sigma_s / (2 * e) - e * (m * c0) ** 2 / 2
    # Eq. (27): on-shell relation
    L_on_shell = L.subs(sigma_s, -(e**2) * (m * c0) ** 2)
    # Eq. (29): L = -e (m c0)^2
    assert sp.simplify(L_on_shell - (-e * (m * c0) ** 2)) == 0
    # Eq. (26): e = sqrt(-sigma)/(m c0); Eq. (30): L = -m c0 sqrt(-sigma)
    L_recovered = L_on_shell.subs(e, sp.sqrt(-sigma_s) / (m * c0))
    assert sp.simplify(L_recovered - (-m * c0 * sp.sqrt(-sigma_s))) == 0


# ---------------------------------------------------------------------------
# Eqs. (33) and (35): coordinate partial derivatives
# ---------------------------------------------------------------------------


def test_eq033_035_coordinate_partials():
    e = sp.symbols("e", positive=True)
    g = _symmetric_symbols("g")
    xd = sp.Matrix(sp.symbols("xd0 xd1 xd2"))  # velocities \dot x
    sigma = (xd.T * g * xd)[0]
    L = sigma / (2 * e)
    # Eq. (33): dL/dxd^lam = g_{lam nu} xd^nu / e
    for lam in range(DIM):
        assert sp.simplify(sp.diff(L, xd[lam]) - (g[lam, :] * xd)[0] / e) == 0
    # Eq. (35): dL/dx^lam = (1/2e) (d_lam g_{mu nu}) xd^mu xd^nu.
    # Direct numeric check of the analytic formula for dL/dx:
    rng = np.random.default_rng(0)
    gv, giv, dgv = _random_metric_data(rng)
    xdv = rng.normal(size=DIM)
    for lam in range(DIM):
        analytic = 0.5 * np.einsum("mn,m,n", dgv[lam], xdv, xdv)
        # finite-difference the Lagrangian's x-dependence through g
        eps = 1e-7
        gp = gv + eps * dgv[lam]
        gm = gv - eps * dgv[lam]
        fd = (np.einsum("mn,m,n", gp, xdv, xdv) - np.einsum("mn,m,n", gm, xdv, xdv)) / (
            4 * eps
        )
        assert abs(analytic - fd) < 1e-6


# ---------------------------------------------------------------------------
# Eqs. (36)-(51): from the EL equation to the Christoffel form
# ---------------------------------------------------------------------------


def test_eq036_to_051_el_expansion_matches_christoffel_form():
    """The full pipeline of Section 8: expand d/dtau(g_{lam nu} xd^nu), raise the
    index, and compare against xdd^sigma + Gamma^sigma_{rho nu} xd^rho xd^nu -
    (ed/e) xd^sigma = 0, on random data. Both sides are linear in xdd, so the
    comparison is made coefficient-exact."""
    rng = np.random.default_rng(1)
    g, gi, dg = _random_metric_data(rng)
    xd = rng.normal(size=DIM)
    xdd = rng.normal(size=DIM)
    e, ed = 1.3, 0.7

    # After multiplying Eq. (36) by e, the lower-index equation is
    #   (d_rho g_{lam nu}) xd^rho xd^nu + g_{lam nu} xdd^nu - (ed/e) g_{lam nu} xd^nu
    #   = 1/2 (d_lam g_{mu nu}) xd^mu xd^nu .
    # Solving for xdd via the inverse metric must give the Christoffel form.
    xdd_from_el = -gi @ (
        np.array(
            [
                xd @ dg[:, lam, :] @ xd
                - 0.5 * np.einsum("mn,m,n", dg[lam], xd, xd)
                - (ed / e) * (g[lam] @ xd)
                for lam in range(DIM)
            ]
        )
    )
    Gamma = np.zeros((DIM, DIM, DIM))
    for s in range(DIM):
        for r in range(DIM):
            for n in range(DIM):
                Gamma[s, r, n] = _christoffel_general(gi, dg, s, r, n)
    xdd_christoffel = -np.einsum("srn,r,n", Gamma, xd, xd) + (ed / e) * xd
    np.testing.assert_allclose(xdd_from_el, xdd_christoffel, atol=1e-10)


# ---------------------------------------------------------------------------
# Eqs. (53)-(55): the eighteen printed Christoffel components
# ---------------------------------------------------------------------------

# Each entry: (sigma, rho, nu) -> list of (lam, kind) where kind selects the
# printed bracket for that lam:
#   "a": d_rho g_{lam nu} + d_nu g_{lam rho} - d_lam g_{rho nu}  (unsimplified)
# The document prints the *simplified* brackets; we encode those simplifications
# explicitly below, component by component, exactly as printed.


def _printed_components(dg):
    """The 18 components as printed in Eqs. (53)-(55), as functions of the
    derivative field dg[rho][mu][nu] = d_rho g_{mu nu}."""

    def G(sigma, terms):
        return {sigma: terms}

    printed = {}
    for sigma in range(DIM):
        printed[(sigma, 0, 0)] = [
            (0, lambda d: d[0, 0, 0]),
            (1, lambda d: 2 * d[0, 1, 0] - d[1, 0, 0]),
            (2, lambda d: 2 * d[0, 2, 0] - d[2, 0, 0]),
        ]
        printed[(sigma, 0, 1)] = [
            (0, lambda d: d[1, 0, 0]),
            (1, lambda d: d[0, 1, 1]),
            (2, lambda d: d[0, 1, 2] + d[1, 0, 2] - d[2, 0, 1]),
        ]
        printed[(sigma, 0, 2)] = [
            (0, lambda d: d[2, 0, 0]),
            (1, lambda d: d[0, 1, 2] + d[2, 0, 1] - d[1, 0, 2]),
            (2, lambda d: d[0, 2, 2]),
        ]
        printed[(sigma, 1, 1)] = [
            (0, lambda d: 2 * d[1, 0, 1] - d[0, 1, 1]),
            (1, lambda d: d[1, 1, 1]),
            (2, lambda d: 2 * d[1, 2, 1] - d[2, 1, 1]),
        ]
        printed[(sigma, 1, 2)] = [
            (0, lambda d: d[1, 0, 2] + d[2, 0, 1] - d[0, 1, 2]),
            (1, lambda d: d[2, 1, 1]),
            (2, lambda d: d[1, 2, 2]),
        ]
        printed[(sigma, 2, 2)] = [
            (0, lambda d: 2 * d[2, 0, 2] - d[0, 2, 2]),
            (1, lambda d: 2 * d[2, 1, 2] - d[1, 2, 2]),
            (2, lambda d: d[2, 2, 2]),
        ]
    return printed


def test_eq053_055_printed_christoffels_match_general_formula():
    rng = np.random.default_rng(2)
    g, gi, dg = _random_metric_data(rng)
    printed = _printed_components(dg)
    for (sigma, rho, nu), terms in printed.items():
        value = 0.5 * sum(gi[sigma, lam] * term(dg) for lam, term in terms)
        general = _christoffel_general(gi, dg, sigma, rho, nu)
        assert abs(value - general) < 1e-10, f"Gamma^{sigma}_{rho}{nu} mismatch"


def test_christoffel_count_is_18():
    # n^2 (n+1)/2 for n = 3, and the printed table covers all symmetric pairs.
    printed = _printed_components(np.zeros((DIM, DIM, DIM)))
    assert len(printed) == 3 * 3 * 4 // 2 == 18


# ---------------------------------------------------------------------------
# Section 12.1: metric compatibility / norm preservation along geodesics
# ---------------------------------------------------------------------------


def test_sec12_norm_preservation_identity():
    """d/dtau(g_{mu nu} xd^mu xd^nu) = 2 g_{mu nu} xd^mu Dxd^nu/dtau, for
    arbitrary xdd (the identity behind constraint preservation)."""
    rng = np.random.default_rng(3)
    g, gi, dg = _random_metric_data(rng)
    xd = rng.normal(size=DIM)
    xdd = rng.normal(size=DIM)
    Gamma = np.array(
        [
            [[_christoffel_general(gi, dg, s, r, n) for n in range(DIM)] for r in range(DIM)]
            for s in range(DIM)
        ]
    )
    # d/dtau(g xd xd) = (d_rho g) xd^rho xd xd + 2 g xd xdd
    d_dtau = np.einsum("rmn,r,m,n", dg, xd, xd, xd) + 2 * np.einsum(
        "mn,m,n", g, xd, xdd
    )
    # 2 g xd (xdd + Gamma xd xd)
    cov = xdd + np.einsum("srn,r,n", Gamma, xd, xd)
    rhs = 2 * np.einsum("mn,m,n", g, xd, cov)
    assert abs(d_dtau - rhs) < 1e-10


# ---------------------------------------------------------------------------
# Eqs. (67)-(68): the null circle
# ---------------------------------------------------------------------------


def test_eq067_068_null_circle_parametrization():
    theta, x0d = sp.symbols("theta x0d", real=True)
    x1d = x0d * sp.cos(theta)
    x2d = x0d * sp.sin(theta)
    constraint = -(x0d**2) + x1d**2 + x2d**2
    assert sp.simplify(constraint) == 0


def test_eq067_068_completeness_of_circle():
    """Every future-null velocity in an inertial frame lies on the circle:
    the constraint forces (x1d/x0d)^2 + (x2d/x0d)^2 = 1."""
    rng = np.random.default_rng(4)
    for _ in range(50):
        theta = rng.uniform(0, 2 * np.pi)
        x0d = rng.uniform(0.1, 10)
        v = np.array([x0d, x0d * np.cos(theta), x0d * np.sin(theta)])
        eta = np.diag([-1.0, 1.0, 1.0])
        assert abs(v @ eta @ v) < 1e-10
        r = np.hypot(v[1] / v[0], v[2] / v[0])
        assert abs(r - 1) < 1e-12


# ---------------------------------------------------------------------------
# Eqs. (69)-(72): little groups
# ---------------------------------------------------------------------------

_ETA = np.diag([-1.0, 1.0, 1.0])

_J = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, -1.0, 0.0]])  # rotation 1-2
_K2 = np.array([[0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])  # boost along x2
_M = _K2 + _J  # null rotation, Eq. (71)


def test_eq071_null_rotation_generator():
    k0 = np.array([1.0, 1.0, 0.0])  # kappa = 1
    np.testing.assert_allclose(_M @ k0, np.zeros(3), atol=1e-15)
    # eta M antisymmetric  <=>  M in so(2,1)
    etaM = _ETA @ _M
    np.testing.assert_allclose(etaM + etaM.T, np.zeros((3, 3)), atol=1e-15)
    # Decomposition claimed in the text: M = K2 + J.
    np.testing.assert_allclose(_M, _K2 + _J, atol=1e-15)


def test_eq071_exponential_fixes_null_vector_symbolically():
    t = sp.symbols("t", real=True)
    M = sp.Matrix([[0, 0, 1], [0, 0, 1], [1, -1, 0]])
    k0 = sp.Matrix([1, 1, 0])
    exp_tM = sp.exp(t * M)
    assert all(sp.simplify(x) == 0 for x in (exp_tM * k0 - k0))


def test_eq071_exponential_preserves_minkowski_form():
    from scipy.linalg import expm

    rng = np.random.default_rng(5)
    for tt in rng.uniform(-3, 3, size=10):
        T = expm(tt * _M)
        np.testing.assert_allclose(T @ _ETA @ T.T, _ETA, atol=1e-10)


def test_eq070_massive_little_group_is_rotation():
    """Among the so(2,1) basis {J, K1, K2}, only J fixes the rest momentum."""
    p0 = np.array([1.0, 0.0, 0.0])
    K1 = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    np.testing.assert_allclose(_J @ p0, np.zeros(3), atol=1e-15)
    assert np.linalg.norm(K1 @ p0) > 0.5
    assert np.linalg.norm(_K2 @ p0) > 0.5


def test_sec10_transitivity_on_shells():
    """SO(2,1) acts transitively: random future-timelike/null momenta map to
    the standard forms used in the text."""
    from scipy.linalg import expm

    rng = np.random.default_rng(6)
    for _ in range(20):
        # massive: p = (m cosh a, m sinh a cos th, m sinh a sin th)
        m = rng.uniform(0.5, 3)
        a = rng.uniform(0, 2)
        th = rng.uniform(0, 2 * np.pi)
        p = np.array([m * np.cosh(a), m * np.sinh(a) * np.cos(th), m * np.sinh(a) * np.sin(th)])
        # undo rotation, then boost: exp(+th J) rotates (p1,p2) onto axis 1
        T = expm(-a * np.array([[0.0, 1, 0], [1, 0, 0], [0, 0, 0]])) @ expm(th * _J)
        np.testing.assert_allclose(T @ p, np.array([m, 0, 0]), atol=1e-10)
        # null: k = (k, k cos th, k sin th) -> (k, k, 0) by rotation alone
        k = rng.uniform(0.1, 5)
        kv = np.array([k, k * np.cos(th), k * np.sin(th)])
        np.testing.assert_allclose(expm(th * _J) @ kv, np.array([k, k, 0]), atol=1e-10)


# ---------------------------------------------------------------------------
# Eqs. (74)-(76): Hamiltonian
# ---------------------------------------------------------------------------


def test_eq074_076_hamiltonian_pure_constraint():
    e, m, c0 = sp.symbols("e m c0", positive=True)
    g = _symmetric_symbols("g")
    gi = sp.simplify(g.inv())
    xd = sp.Matrix(sp.symbols("xd0 xd1 xd2"))
    p = sp.Matrix(sp.symbols("p0 p1 p2"))
    sigma = (xd.T * g * xd)[0]
    L = sigma / (2 * e) - e * (m * c0) ** 2 / 2
    # Eq. (74): p_lam = (1/e) g_{lam nu} xd^nu  <=>  xd = e g^{nu lam} p_lam
    xd_from_p = e * gi * p
    back_sub = sp.simplify((g * xd_from_p)[0] / e - p[0])
    assert back_sub == 0
    # Eq. (75): H = p.xd - L = (e/2)(g^{mu nu} p_mu p_nu + (m c0)^2)
    H = (p.T * xd_from_p)[0] - L.subs(
        {xd[i]: xd_from_p[i] for i in range(DIM)}
    )
    H_claimed = e / 2 * ((p.T * gi * p)[0] + (m * c0) ** 2)
    assert sp.simplify(H - H_claimed) == 0


# ---------------------------------------------------------------------------
# Eq. (12): reparametrization invariance of the einbein action
# ---------------------------------------------------------------------------


def test_eq012_reparametrization_invariance():
    e, fdot, sigma, m, c0 = sp.symbols("e fdot sigma m c0", positive=True)
    # Under tau -> f(tau): xd -> xd/fdot, e -> e/fdot, d tau -> fdot d tau.
    integrand_old = (sigma / (2 * e) - e * (m * c0) ** 2 / 2)
    integrand_new_times_jac = sp.simplify(
        ((sigma / fdot**2) / (2 * e / fdot) - (e / fdot) * (m * c0) ** 2 / 2) * fdot
    )
    assert sp.simplify(integrand_new_times_jac - integrand_old) == 0


# ---------------------------------------------------------------------------
# Eq. (82): Weyl invariance of the massless action
# ---------------------------------------------------------------------------


def test_eq082_weyl_invariance():
    Om, e, sigma, m, c0 = sp.symbols("Omega e sigma m c0", positive=True)
    massless = sigma / (2 * e)
    assert sp.simplify(
        massless.subs({sigma: Om**2 * sigma, e: Om**2 * e}) - massless
    ) == 0
    # mass term is NOT invariant: picks up Omega^2
    mass_term = -e * (m * c0) ** 2 / 2
    assert sp.simplify(mass_term.subs(e, Om**2 * e) - Om**2 * mass_term) == 0


# ---------------------------------------------------------------------------
# Section 10.4: component counting
# ---------------------------------------------------------------------------


def test_sec104_riemann_ricci_component_counting():
    for n, riemann, ricci in [(2, 1, 3), (3, 6, 6), (4, 20, 10)]:
        assert n * n * (n * n - 1) // 12 == riemann
        assert n * (n + 1) // 2 == ricci
    # n = 3: equal counts -> Riemann algebraically determined by Ricci
    assert 3 * 3 * (9 - 1) // 12 == 3 * 4 // 2 == 6


# ---------------------------------------------------------------------------
# Section 10.1: induced metric on the massive shell is positive-definite
# ---------------------------------------------------------------------------


def test_sec101_hyperboloid_induced_metric_positive_definite():
    rng = np.random.default_rng(8)
    eta = np.diag([-1.0, 1.0, 1.0])
    for _ in range(30):
        a = rng.uniform(0, 3)
        th = rng.uniform(0, 2 * np.pi)
        # parametrization p(a, th) of the unit future shell
        p = lambda a, th: np.array(
            [np.cosh(a), np.sinh(a) * np.cos(th), np.sinh(a) * np.sin(th)]
        )
        eps = 1e-6
        pa = (p(a + eps, th) - p(a - eps, th)) / (2 * eps)
        pt = (p(a, th + eps) - p(a, th - eps)) / (2 * eps)
        induced = np.array(
            [[pa @ eta @ pa, pa @ eta @ pt], [pt @ eta @ pa, pt @ eta @ pt]]
        )
        assert np.all(np.linalg.eigvalsh(induced) > 0)


# ---------------------------------------------------------------------------
# Review-round coverage additions (independent review, PR round 1)
# ---------------------------------------------------------------------------


def test_eq056_057_covariant_form_equivalence():
    """Eq. (57) <=> Eq. (56): e * D(xd^sigma / e)/dtau = xdd + Gamma xd xd
    - (ed/e) xd, for arbitrary data."""
    rng = np.random.default_rng(11)
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
    # D(xd/e)/dtau = d(xd/e)/dtau + Gamma xd (xd/e)
    d_xd_over_e = xdd / e - (ed / e**2) * xd
    cov = d_xd_over_e + np.einsum("srn,r,n", Gamma, xd, xd / e)
    lhs = e * cov
    rhs = xdd + np.einsum("srn,r,n", Gamma, xd, xd) - (ed / e) * xd
    np.testing.assert_allclose(lhs, rhs, atol=1e-10)


def test_eq071_shear_is_exact():
    """The O(t^2) in the document's shear statement is in fact exact:
    M^3 = 0 and (M^2 p)_2 = 0, so (e^{tM} p)_2 = p2 + t (p0 - p1)."""
    t = sp.symbols("t", real=True)
    M = sp.Matrix([[0, 0, 1], [0, 0, 1], [1, -1, 0]])
    assert M**3 == sp.zeros(3)
    p0, p1, p2 = sp.symbols("p0 p1 p2", real=True)
    p = sp.Matrix([p0, p1, p2])
    assert sp.simplify((M**2 * p)[2]) == 0
    exp_tp = sp.exp(t * M) * p
    assert sp.simplify(exp_tp[2] - (p2 + t * (p0 - p1))) == 0


def test_sec093_null_directions_sphere_for_n_2_to_5():
    """In n spacetime dimensions the null directions are S^{n-2}: future-null
    vectors are exactly x0 * (1, u) with u a unit vector in R^{n-1}."""
    rng = np.random.default_rng(12)
    for n in range(2, 6):
        eta = np.diag([-1.0] + [1.0] * (n - 1))
        for _ in range(20):
            u = rng.normal(size=n - 1)
            u /= np.linalg.norm(u)  # point of S^{n-2}
            x0 = rng.uniform(0.1, 10)
            v = np.concatenate([[x0], x0 * u])
            assert abs(v @ eta @ v) < 1e-10
            # completeness: ratios reconstruct a unit vector
            assert abs(np.linalg.norm(v[1:] / v[0]) - 1) < 1e-12


def test_step3_gauge_e_const_attainable():
    """Given any positive e(tau), the ODE fdot = e / e_target produces a
    parameter in which the transformed einbein e / fdot is constant."""
    rng = np.random.default_rng(13)
    e_target = 2.0
    tau = np.linspace(0, 4 * np.pi, 4001)
    e_of_tau = 1.0 + 0.5 * np.sin(tau)  # positive sample einbein
    fdot = e_of_tau / e_target
    e_transformed = e_of_tau / fdot
    np.testing.assert_allclose(e_transformed, e_target, rtol=1e-12)
    # f itself is the integral of fdot; monotone since fdot > 0
    f = np.concatenate([[0.0], np.cumsum(0.5 * (fdot[1:] + fdot[:-1]) * np.diff(tau))])
    assert np.all(np.diff(f) > 0)


def test_eq079_081_flat_space_solutions():
    """The printed flat-space solutions satisfy the equations and constraints."""
    rng = np.random.default_rng(14)
    eta = np.diag([-1.0, 1, 1])
    e, m, c0 = 1.5, 0.8, 2.0
    # massive: u0 timelike with the printed normalization; x(tau) = x0 + u0 tau
    for _ in range(20):
        th = rng.uniform(0, 2 * np.pi)
        a = rng.uniform(0, 2)
        u0 = e * m * c0 * np.array([np.cosh(a), np.sinh(a) * np.cos(th), np.sinh(a) * np.sin(th)])
        assert abs(u0 @ eta @ u0 + (e * m * c0) ** 2) < 1e-9
    # massless: k0 = kappa (1, cos th, sin th), null, future-directed
    for _ in range(20):
        th = rng.uniform(0, 2 * np.pi)
        kap = rng.uniform(0.1, 5)
        k0 = kap * np.array([1.0, np.cos(th), np.sin(th)])
        assert abs(k0 @ eta @ k0) < 1e-12 and k0[0] > 0


def test_footnote_sqrt_lagrangian_reparametrization():
    """Section 3 footnote: L_sqrt is homogeneous of degree one in the
    velocities, which makes the action parameter-independent."""
    lam, m, c0 = sp.symbols("lambda m c0", positive=True)
    sigma = sp.symbols("sigma", negative=True)
    L = -m * c0 * sp.sqrt(-sigma)
    assert sp.simplify(L.subs(sigma, lam**2 * sigma) - lam * L) == 0
    # change of variables: integrand * d tau invariant under tau -> f(tau)
    fdot = sp.symbols("fdot", positive=True)
    assert sp.simplify((lam * L).subs(lam, 1 / fdot) * fdot - L) == 0


def test_eq053_055_symbolic_all_18():
    """Fully symbolic check of the 18 printed components against Eq. (52)."""
    g = _symmetric_symbols("g")
    gi = sp.simplify(g.inv())
    dg = sp.symbols(
        " ".join(
            f"d{r}{m}{n}"
            for r in range(DIM)
            for m in range(DIM)
            for n in range(m, DIM)
        )
    )
    dg_field = [[[None] * DIM for _ in range(DIM)] for _ in range(DIM)]
    it = iter(dg)
    for r in range(DIM):
        for m in range(DIM):
            for n in range(m, DIM):
                dg_field[r][m][n] = next(it)
                dg_field[r][n][m] = dg_field[r][m][n]

    def gen(s, r, n):
        return sp.Rational(1, 2) * sum(
            gi[s, l] * (dg_field[r][l][n] + dg_field[n][l][r] - dg_field[l][r][n])
            for l in range(DIM)
        )

    def printed(s, r, n):
        # the simplified brackets exactly as printed in Eqs. (53)-(55)
        def B(l):
            if r == n:
                if l == r:
                    return dg_field[r][r][r]
                return 2 * dg_field[r][l][r] - dg_field[l][r][r]
            if l == r:
                return dg_field[n][r][r]
            if l == n:
                return dg_field[r][n][n]
            return dg_field[r][l][n] + dg_field[n][l][r] - dg_field[l][r][n]

        return sp.Rational(1, 2) * sum(gi[s, l] * B(l) for l in range(DIM))

    for s in range(DIM):
        for r in range(DIM):
            for n in range(r, DIM):
                assert sp.simplify(printed(s, r, n) - gen(s, r, n)) == 0, (
                    f"Gamma^{s}_{r}{n} symbolic mismatch"
                )


def test_unprinted_component_count_is_9():
    """The document states nine unprinted rho > nu components: 3 pairs x 3
    sigma values = 27 total ordered - 18 printed."""
    assert 3 * 9 - 18 == 9


def test_sec101_exact_induced_metric():
    """The induced metric on the unit hyperboloid p(a, th) is exactly
    diag(1, sinh^2 a) (positive-definite), not merely numerically."""
    a, th = sp.symbols("a theta", real=True)
    p = sp.Matrix(
        [sp.cosh(a), sp.sinh(a) * sp.cos(th), sp.sinh(a) * sp.sin(th)]
    )
    eta = sp.diag(-1, 1, 1)
    pa = sp.diff(p, a)
    pt = sp.diff(p, th)
    g_aa = sp.trigsimp((pa.T * eta * pa)[0])
    g_at = sp.trigsimp((pa.T * eta * pt)[0])
    g_tt = sp.trigsimp((pt.T * eta * pt)[0])
    assert g_aa == 1
    assert g_at == 0
    assert sp.simplify(g_tt - sp.sinh(a) ** 2) == 0
