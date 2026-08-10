"""Exact toronic-bundle topology and the minimal flux background (issue #28).

Authority status: conditional, unpromoted infrastructure linked to open goal
issue #28 (vantasnerdan/substrate-framework), split from the issue #26 audit
per the 2026-08-10 harvest review.  No accepted claim backs these symbols.

The preprint's Sec. 10 globally consistent bundle over T^2 (side L) is
declared by the transition functions (cover lifts, L3 = L/2)

    Omega1(x2) = exp(i pi x2/L3) i sigma3,
    Omega2(x1) = exp(i pi x1/L3) i sigma1,

with gauge group G = (SU(2) x U(1))/K.  Everything below is computed from
these declarations; no verdict is hard-coded.

Exact statements implemented:

[B-1]  The cover cocycle z = Omega1(x2+L) Omega2(x1) [Omega2(x1+L) Omega1(x2)]^-1
       is (-I, +1), computed symbolically in (x1, x2, L).  A flat connection
       exists iff z lies in K.  For the diagonal Z2 kernel K = {(I,1),
       (-I,-1)} (the preprint's SM-like quotient) z is NOT in K: no flat
       connection exists with fundamental matter.  Mutations: the wrong
       kernel {(I,1),(-I,1)} (PSU(2) x U(1)) contains z (positive control);
       the trivial kernel (no quotient) does not.
[B-2]  The cover commutator of the toronic holonomies with arbitrary U(1)
       lift phases a, b is (-I, exp(i(a+b-a-b))) = (-I, 1): no phase choice
       repairs the obstruction.
[B-3]  In G, z = (-I,1) = (I,-1) mod K, so the curvature can be carried by
       either su(2) (|F|L^2 = 2 pi in T = sigma/2 normalization) or u(1)_Y
       (g' Y |F_B| L^2 = pi, Y = 1/2).  The classical energy densities are
       2 pi^2/(g^2 L^4) and 2 pi^2/(g'^2 L^4); the su(2) representative is
       the minimum at SM couplings.  Both are positive and exceed the
       one-loop gauge-sector term by an order of magnitude or more.
[B-4]  Lattice representative of the minimal (constant-curvature su(2))
       connection: U_1 = I, U_2(n1,n2) = exp(i 2 pi T3 n1/N^2).  Interior
       plaquettes are exactly uniform (exp(i 2 pi T3/N^2)); the wrap row
       deviates by O(1/N) and vanishes under refinement; the cycle-2 Wilson
       holonomy winds from +I to -I.  Its spectrum is a magnetic tower whose
       ground converges to the Landau value 1/(4 pi) (dimensionless
       (L/2pi)^2 units), and fits no constant-twist spectrum under
       continuous optimization.
"""

from __future__ import annotations

from typing import Any, Sequence

import numpy as np
import sympy as sp

# ---------------------------------------------------------------------------
# exact bundle topology
# ---------------------------------------------------------------------------


def transition_function_cocycle() -> tuple[sp.Matrix, sp.Expr]:
    """Cover cocycle z of the declared bundle: (-I, +1), exact.

    z = Omega1(x2+L) Omega2(x1) [Omega2(x1+L) Omega1(x2)]^-1, computed as
    the full product of the declared transition functions; the U(1) phase
    reduces via exp(2 pi i) = 1.  Returns (su2 part, u1 phase).
    """

    x1, x2, L = sp.symbols("x1 x2 L", positive=True)
    i = sp.I
    s3 = sp.Matrix([[1, 0], [0, -1]])
    s1 = sp.Matrix([[0, 1], [1, 0]])
    L3 = L / 2

    def om1(v):
        return sp.exp(i * sp.pi * v / L3) * i * s3

    def om2(v):
        return sp.exp(i * sp.pi * v / L3) * i * s1

    full = sp.simplify(om1(x2 + L) * om2(x1) * (om2(x1 + L) * om1(x2)).inv())
    # the product is (u1 phase) x (su2 element); factor via the (0,0) entry
    su2_entry = ((i * s3) * (i * s1) * ((i * s1) * (i * s3)).inv())[0, 0]
    phase = sp.simplify(sp.expand_complex(full[0, 0] / su2_entry))
    su2_part = sp.simplify(full / phase)
    return sp.Matrix(su2_part), phase


def cover_holonomy_commutator() -> tuple[sp.Matrix, sp.Expr]:
    """Cover commutator of toronic holonomies with symbolic U(1) lift phases.

    Lifts (P, e^{ia}), (Q, e^{ib}) of the toronic holonomy classes
    P = i sigma3, Q = i sigma1; the commutator is (-I, e^{i(a+b-a-b)})
    = (-I, 1) for every phase choice.
    """

    i = sp.I
    a, b = sp.symbols("a b", real=True)
    s3 = sp.Matrix([[1, 0], [0, -1]])
    s1 = sp.Matrix([[0, 1], [1, 0]])
    p, q = i * s3, i * s1
    su2_part = sp.simplify(p * q * p.inv() * q.inv())
    phase = sp.simplify(sp.exp(i * a) * sp.exp(i * b) * sp.exp(-i * a) * sp.exp(-i * b))
    return sp.Matrix(su2_part), phase


#: Quotient kernels as (su2 element, u1 phase) pairs.
_QUOTIENT_KERNELS: dict[str, tuple[tuple[sp.Matrix, sp.Expr], ...]] = {
    # the preprint's SM-like diagonal Z2 quotient
    "diagonal_z2": (
        (sp.eye(2), sp.Integer(1)),
        (-sp.eye(2), -sp.Integer(1)),
    ),
    # wrong-kernel mutation: PSU(2) x U(1) (no diagonal identification)
    "psu2_times_u1": (
        (sp.eye(2), sp.Integer(1)),
        (-sp.eye(2), sp.Integer(1)),
    ),
    # no quotient at all: the cocycle must hold exactly in SU(2) x U(1)
    "no_quotient": ((sp.eye(2), sp.Integer(1)),),
}


def quotient_kernel(name: str) -> tuple[tuple[sp.Matrix, sp.Expr], ...]:
    """Return the kernel elements of the named quotient."""

    if name not in _QUOTIENT_KERNELS:
        raise ValueError(f"unknown kernel {name!r}; choose from {sorted(_QUOTIENT_KERNELS)}")
    return _QUOTIENT_KERNELS[name]


def flat_toron_connection_exists(kernel_name: str) -> bool:
    """Structural existence check: is the cover cocycle in the kernel?

    Computed by membership of the exact cocycle [B-1] in the named kernel;
    no case analysis is hard-coded.
    """

    z_su2, z_phase = transition_function_cocycle()
    for k_su2, k_phase in quotient_kernel(kernel_name):
        su2_match = sp.simplify(z_su2 - k_su2) == sp.zeros(2)
        phase_match = sp.simplify(z_phase - k_phase) == 0
        if su2_match and phase_match:
            return True
    return False


# ---------------------------------------------------------------------------
# minimal flux background
# ---------------------------------------------------------------------------


def flux_background_candidates(g: Any, g_prime: Any, L: Any = 1) -> dict[str, sp.Expr]:
    """Classical energy densities of the two minimal flux representatives.

    su2: |F| = 2 pi/L^2 (T = sigma/2 normalization, exp(i |F| L^2 T) = -I),
         density (1/2 g^-2) |F|^2 = 2 pi^2/(g^2 L^4).
    u1_hypercharge: g' Y |F_B| L^2 = pi with Y = 1/2, density
         F_B^2/2 = 2 pi^2/(g'^2 L^4).
    """

    g_val, gp_val, L_val = sp.sympify(g), sp.sympify(g_prime), sp.sympify(L)
    for value, name in ((g_val, "g"), (gp_val, "g_prime"), (L_val, "L")):
        if value.is_number and value.is_positive is not True:
            raise ValueError(f"{name} must be positive")
    su2_density = 2 * sp.pi**2 / (g_val**2 * L_val**4)
    u1_density = 2 * sp.pi**2 / (gp_val**2 * L_val**4)
    return {"su2": sp.simplify(su2_density), "u1_hypercharge": sp.simplify(u1_density)}


def minimal_flux_classical_energy_density(g: Any, g_prime: Any, L: Any = 1) -> sp.Expr:
    """Minimum classical flux energy density over the representatives."""

    candidates = flux_background_candidates(g, g_prime, L)
    return sp.Min(*candidates.values())


# ---------------------------------------------------------------------------
# lattice representative of the minimal su(2) flux connection
# ---------------------------------------------------------------------------


def uniform_flux_links(n_side: int) -> tuple[np.ndarray, np.ndarray]:
    """Landau-gauge links of the constant-curvature su(2) connection.

    U_1 = I everywhere; U_2(n1,n2) = exp(i 2 pi T3 n1 / N^2).  Interior
    plaquettes are exactly exp(i 2 pi T3 / N^2); the wrap row carries the
    O(1/N) lattice artifact of the 2 pi total flux (vanishes in the
    continuum limit).
    """

    if n_side < 4:
        raise ValueError("n_side must be >= 4")
    n = n_side
    u1 = np.broadcast_to(np.eye(2), (n, n, 2, 2)).copy()
    u2 = np.zeros((n, n, 2, 2), dtype=complex)
    for n1 in range(n):
        theta = 2 * np.pi * n1 / n**2  # angle multiplying T3 = sigma3/2
        for n2 in range(n):
            u2[n1, n2] = np.diag([np.exp(1j * theta / 2), np.exp(-1j * theta / 2)])
    return u1, u2


def plaquette_holonomies(
    links: tuple[np.ndarray, np.ndarray],
) -> np.ndarray:
    """Plaquette holonomy U_1(n) U_2(n+e1) U_1(n+e2)^dag U_2(n)^dag per site."""

    u1, u2 = links
    n = u1.shape[0]
    plaquettes = np.zeros((n, n, 2, 2), dtype=complex)
    for n1 in range(n):
        for n2 in range(n):
            plaquettes[n1, n2] = (
                u1[n1, n2]
                @ u2[(n1 + 1) % n, n2]
                @ u1[n1, (n2 + 1) % n].conj().T
                @ u2[n1, n2].conj().T
            )
    return plaquettes


def cycle_two_holonomy(links: tuple[np.ndarray, np.ndarray], n1: int) -> np.ndarray:
    """Wilson holonomy around the x2 cycle at fixed n1."""

    _, u2 = links
    n = u2.shape[0]
    holonomy = np.eye(2, dtype=complex)
    for n2 in range(n):
        holonomy = holonomy @ u2[n1, n2]
    return holonomy


def spectrum_from_links(links: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
    """Dimensionless Laplacian spectrum ((L/2pi)^2 units) of a link field."""

    u1, u2 = links
    n = u1.shape[0]
    dim = 2
    size = n * n * dim
    lap = np.zeros((size, size), dtype=complex)

    def flat(n1: int, n2: int, comp: int) -> int:
        return (n1 * n + n2) * dim + comp

    for n1 in range(n):
        for n2 in range(n):
            for mu, field in ((0, u1), (1, u2)):
                forward = ((n1 + 1) % n, n2) if mu == 0 else (n1, (n2 + 1) % n)
                link = field[n1, n2]
                for a in range(dim):
                    i0 = flat(n1, n2, a)
                    j0 = flat(forward[0], forward[1], a)
                    lap[i0, i0] += 1
                    lap[j0, j0] += 1
                    for b in range(dim):
                        lap[i0, flat(forward[0], forward[1], b)] -= link[a, b]
                        lap[flat(forward[0], forward[1], b), i0] -= np.conj(link[a, b])
    return np.sort(np.linalg.eigvalsh(lap).real) * (n / (2 * np.pi)) ** 2


def landau_ground_dimensionless() -> sp.Expr:
    """Continuum Landau ground of the minimal flux: (L/2pi)^2 |F|/2 = 1/(4 pi).

    Per T3 component the flux is |F|/2 = pi/L^2 (half a flux quantum; the
    doublet resolves the fractional degeneracy), so the lowest level is
    |F|/2 in physical units, i.e. 1/(4 pi) in (L/2pi)^2 units.
    """

    return 1 / (4 * sp.pi)


def best_constant_twist_residual(
    spectrum: np.ndarray, modes: int = 8, *, seed: int = 0
) -> tuple[tuple[float, float], float]:
    """Continuous best fit of a constant-twist spectrum to lattice low modes.

    Minimizes the max relative deviation of the lowest `modes` nonzero
    eigenvalues against analytic |n + alpha|^2 spectra over alpha in
    [0, 1)^2 by differential evolution (continuous, seeded, deterministic).
    Returns (best_alpha, best_relative_residual).
    """

    from scipy.optimize import differential_evolution

    from .twisted_casimir import analytic_twist_spectrum

    lattice_low = spectrum[spectrum > 1e-8][:modes]
    if len(lattice_low) < modes:
        raise ValueError("not enough nonzero lattice modes")

    def residual(alpha: Sequence[float]) -> float:
        analytic = analytic_twist_spectrum(alpha, 4)
        analytic_low = analytic[analytic > 1e-8][:modes]
        if len(analytic_low) < modes:
            return 1e6
        return float(np.max(np.abs(lattice_low - analytic_low) / analytic_low))

    result = differential_evolution(
        residual, bounds=[(0.0, 1.0), (0.0, 1.0)], seed=seed, tol=1e-10
    )
    return (float(result.x[0]), float(result.x[1])), float(result.fun)
