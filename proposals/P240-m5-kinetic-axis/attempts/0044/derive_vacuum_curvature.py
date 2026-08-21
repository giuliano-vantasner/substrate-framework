"""P240 attempt 0044, step D1 (gate G1): symbolic vacuum curvature.

Potential (certified chart, verbatim from cpu_energy / solve_radial_1d):

    V(M) = -1/2 tr(M^2) - tr(M^3) + (tr M^2)^2 + 1/2.

Rank-1 projector background P = n n^T (the hedgehog's wall value and the
candidate R -> infinity limit).  Write M = P + eta, eta symmetric, and expand
V to quadratic order in the six eta components in the eigenframe of P
(n = leading, p/a = degenerate):

    V2[eta] = 5/2 nn^2 + 3/2 (pp^2 + aa^2) + 3 pa^2 + 0 * (np^2 + na^2).

The two shear channels (np, na) are EXACTLY FLAT in the potential: their whole
stiffness is gradient-generated (quartic commutator class).  This script
derives that symbolically and checks it against the certified potential
formula pointwise via Richardson extrapolation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / ".." / "0041"))

from cpu_energy import DTYPE, gauss_grid  # noqa: E402

RESULTS = HERE / "derivation-results.json"


def symbolic_quadratic_form():
    nn, pp, aa, np_, na, pa = sp.symbols("nn pp aa np na pa", real=True)
    eta = sp.Matrix([
        [nn, np_, na],
        [np_, pp, pa],
        [na, pa, aa],
    ])
    P = sp.diag(1, 0, 0)
    M = P + eta
    trace_two = sp.trace(M * M)
    trace_three = sp.trace(M * M * M)
    V = -sp.Rational(1, 2) * trace_two - trace_three + trace_two**2 + sp.Rational(1, 2)
    components = {e: (nn, pp, aa, np_, na, pa) for e in ()}
    order = (nn, pp, aa, np_, na, pa)
    quad = sp.Matrix(6, 6, lambda i, j: sp.expand(sp.diff(V, order[i], order[j])))
    linear = sp.Matrix([sp.expand(sp.diff(V, o)) for o in order])
    constant = sp.simplify(V.subs({o: 0 for o in order}))
    return constant, linear, quad, order


def richardson_check(n_radial=24, n_angular=12, seed=7):
    """Pointwise: [V(P + eps*eta) - V(P)] / eps^2 -> V2[eta] on certified grid."""
    rng = np.random.default_rng(seed)

    def potential_density(m):
        trace_two = torch.diagonal(m @ m, dim1=-2, dim2=-1).sum(-1)
        trace_three = torch.diagonal(m @ m @ m, dim1=-2, dim2=-1).sum(-1)
        return -0.5 * trace_two - trace_three + trace_two**2 + 0.5

    radial, radial_weight, mu, angular_weight = gauss_grid(n_radial, n_angular, 1.0)
    r = radial[:, None].repeat(1, n_angular)
    mu_g = mu[None, :].repeat(n_radial, 1)
    sine = torch.sqrt(torch.clamp(1 - mu_g**2, min=0.0))
    zero = torch.zeros_like(sine)
    n_hat = torch.stack((sine, zero, mu_g), dim=-1)
    p_hat = torch.stack((mu_g, zero, -sine), dim=-1)
    a_hat = torch.stack((zero, torch.ones_like(zero), zero), dim=-1)
    outer = lambda v: v[..., :, None] * v[..., None, :]
    P = outer(n_hat)

    # random symmetric eta in the local frame, smooth in (r, mu)
    coeffs = torch.tensor(
        0.3 * rng.normal(size=(6, 3, 2)) / np.sqrt(6.0), dtype=DTYPE
    )
    rb = torch.stack([(2 * r**2 - 1) ** k for k in range(3)], dim=-1)
    mb = torch.stack([mu_g**k for k in range(2)], dim=-1)
    shape = rb[..., :, None] * mb[..., None, :]
    comp = []
    for idx in range(6):
        comp.append((coeffs[idx, :, :] * shape).sum(dim=(-1, -2)))
    nn, pp, aa, np_c, na_c, pa_c = comp
    zero = torch.zeros_like(nn)
    eta_local = torch.stack([
        torch.stack((nn, np_c, na_c), dim=-1),
        torch.stack((np_c, pp, pa_c), dim=-1),
        torch.stack((na_c, pa_c, aa), dim=-1),
    ], dim=-2)
    # symmetric basis transform: E = sum over ALL ordered pairs (i,j) of
    # eta_local[i,j] * e_i e_j^T; eta_local is symmetric by construction.
    frames = (n_hat, p_hat, a_hat)
    eta_global = torch.zeros_like(P)
    for i in range(3):
        for j in range(3):
            ei, ej = frames[i], frames[j]
            eta_global = eta_global + eta_local[..., i, j][..., None, None] * (
                ei[..., :, None] * ej[..., None, :]
            )

    # m(eps) = Q + c1*eps + c2*eps^2 + ...: the flat (np, na) channels make the
    # cubic term dominant at O(eps), so extrapolate it away exactly:
    # Q ~= 2*m(eps) - m(2*eps).
    v_bg = potential_density(P)
    nn_l, pp_l, aa_l = nn.numpy(), pp.numpy(), aa.numpy()
    np_l, na_l, pa_l = np_c.numpy(), na_c.numpy(), pa_c.numpy()
    predicted = (
        2.5 * nn_l**2
        + 1.5 * pp_l**2
        + 1.5 * aa_l**2
        + 0.0 * (np_l**2 + na_l**2)
        + 3.0 * pa_l**2
    )
    def measured(eps):
        return ((potential_density(P + eps * eta_global) - v_bg) / eps**2).numpy()

    m1, m2 = measured(1e-4), measured(2e-4)
    extrapolated = 2 * m1 - m2
    worst = float(np.abs(extrapolated - predicted).max()) / max(
        1e-30, float(np.abs(predicted).max())
    )
    return worst


def main():
    constant, linear, quad, order = symbolic_quadratic_form()
    at_p = {o: 0 for o in order}
    constant = constant.subs(at_p)
    linear = linear.subs(at_p)
    quad = quad.subs(at_p)
    print("V(P) =", constant)
    print("linear terms at P:", list(linear.T))
    print("H_ij = d2V/di dj at P (order nn,pp,aa,np,na,pa):")
    print(quad)
    expected = sp.Matrix([
        [5, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 6],
    ])
    # V_quad = 1/2 eta^T H eta with H = diag(5,3,3,0,0,6): coefficients 2.5,1.5,1.5,0,0,3
    sym_diff = float(sp.Matrix(quad - expected).norm())
    flat_channels = [order[i] for i in range(6) if quad[i, i] == 0]
    print("symbolic vs hand-derived H max diff:", sym_diff)
    print("exactly flat channels:", flat_channels)

    numeric_worst = richardson_check()
    print(f"Richardson pointwise check worst relative deviation: {numeric_worst:.3e}")

    results = {
        "gate": "G1_symbolic_vacuum_curvature",
        "constant_V_at_P": float(constant),
        "linear_max_abs": float(max(abs(x) for x in linear)),
        "hessian_diagonal": [float(quad[i, i]) for i in range(6)],
        "hessian_offdiagonal_max": float(
            max(abs(quad[i, j]) for i in range(6) for j in range(6) if i != j)
        ),
        "flat_channels": [str(c) for c in flat_channels],
        "symbolic_matches_hand_derivation": sym_diff < 1e-12,
        "richardson_worst_rel": float(numeric_worst),
        "passed": bool(
            sym_diff < 1e-12
            and float(max(abs(x) for x in linear)) == 0.0
            and float(constant) == 0.0
            and numeric_worst < 1e-6
        ),
    }
    RESULTS.write_text(json.dumps(results, indent=2))
    print("passed:", results["passed"], "| wrote", RESULTS.name)


if __name__ == "__main__":
    main()
