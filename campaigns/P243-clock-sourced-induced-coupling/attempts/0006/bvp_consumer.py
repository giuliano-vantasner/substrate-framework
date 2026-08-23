"""Attempt 0006 -- weak-field consumer BVP driven by the selected scale.

Consumer design (registered): the confined-clock sector sources the
linearized Newtonian potential,
    nabla^2 Phi = 4 pi G_total rho(r),
with G_total = 46.80699908016004 (purely induced, xi=0, N=3;
attempts/0003/numeric-unblinded.log) and rho the sector's own static
energy density of a certified background root.

Background: the committed P240 window root at R=12 (order 16, values
in attempts/0042/largeR-roots.json).  Provenance re-verified against
the committed energy before use.  rho(r) is the mu-average of the
static density (commutator + potential pieces of energy_radial)
evaluated on the native basis, so 4 pi int rho r^2 dr equals the
sector STATIC energy by construction.  Declared convention: the
fixed-J constraint term is global, not a radial source, and is
excluded from M.

Boundary value problem on [0, R_box], R_box = 12, second-order
flux-form finite differences:
    origin row:   (-3 Phi_0 + 4 Phi_1 - Phi_2)/(2h) = 0   [Phi'(0)=0]
    interior:     (r^2 Phi')' = 4 pi G rho r^2
    Robin at R:   (3 Phi_N - 4 Phi_{N-1} + Phi_{N-2})/(2h)
                  + Phi_N/R = 0            [exterior -G M/r slope]
Exterior target: linearized_einstein.weak_field_monopole potential
    -G M / r (canonical, mostly-plus harmonic gauge).

Checks: source provenance, mass identity, mesh refinement ladder with
observed convergence order, local Gauss law monitors, monopole
normalization, coupling mutation linearity, weak-field validity
diagnostic epsilon = G M / R reported explicitly.

Environment: system python3 (torch host, numpy 1.x -> two-step
trapezoid fallback per repository rule).
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
import scipy.sparse as sp_sparse
import scipy.sparse.linalg as spla

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "proposals/P240-m5-kinetic-axis/attempts/0041"))

from cpu_energy import (  # noqa: E402
    chebyshev_stack,
    commutator,
    elementwise_derivative,
    frobenius_squared,
    gauss_grid,
)
from solve_radial_1d import Oracle  # noqa: E402

DTYPE = torch.float64
G_TOTAL = 46.80699908016004
RADIUS = 12.0
SETTINGS = dict(radial_nodes=32, angular_nodes=16, radius=RADIUS)

_modern_trapezoid = getattr(np, "trapezoid", None)
trapezoid = _modern_trapezoid if _modern_trapezoid is not None else np.trapz


def sector_density(values, radii, angular_nodes=64):
    """mu-averaged static density of the certified root at radii."""
    order = len(np.asarray(values)) // 3
    coefficients = torch.tensor(
        np.asarray(values, dtype=float).reshape(3, order), dtype=DTYPE)
    _, _, mu_x, mu_w = gauss_grid(8, angular_nodes, RADIUS)
    weights = mu_w.clone().detach()
    rho = np.empty(len(radii))
    for idx, r_val in enumerate(radii):
        radius_grid = torch.full((angular_nodes,), float(r_val),
                                 dtype=DTYPE)
        radius_grid.requires_grad_(True)
        mu_grid = mu_x.clone().detach()
        mu_grid.requires_grad_(True)
        normalized = radius_grid / RADIUS
        radial_coordinate = 2 * normalized**2 - 1
        radial_basis = chebyshev_stack(
            radial_coordinate, tuple(range(order)))
        modal = torch.einsum("...i,ci->...c", radial_basis, coefficients)
        q = normalized**2 * (1.0 + (1.0 - normalized**2) * modal[..., 0])
        tangent = (1.0 - normalized**2) * (
            torch.tensor(1 / 3, dtype=DTYPE) + modal[..., 1])
        split_amplitude = normalized**4 * (1 - normalized**2) * modal[..., 2]
        sine = torch.sqrt(torch.clamp(1 - mu_grid**2, min=0.0))
        delta = split_amplitude * sine**2
        zero = torch.zeros_like(sine)
        director = torch.stack((sine, zero, mu_grid), dim=-1)
        polar = torch.stack((mu_grid, zero, -sine), dim=-1)
        azimuthal = torch.stack((zero, torch.ones_like(zero), zero),
                                dim=-1)

        def outer(vector):
            return vector[..., :, None] * vector[..., None, :]

        lambda_n = tangent + q
        spatial = (
            lambda_n[..., None, None] * outer(director)
            + (tangent + delta)[..., None, None] * outer(polar)
            + (tangent - delta)[..., None, None] * outer(azimuthal)
        )
        derivative_r = elementwise_derivative(spatial, radius_grid)
        derivative_mu = elementwise_derivative(spatial, mu_grid)
        derivative_theta = (-sine[..., None, None]
                            * derivative_mu / radius_grid[..., None, None])
        rotation_z = torch.tensor([[0.0, -1.0, 0.0],
                                   [1.0, 0.0, 0.0],
                                   [0.0, 0.0, 0.0]], dtype=DTYPE)
        derivative_phi = (
            rotation_z @ spatial + spatial @ rotation_z.T
        ) / (radius_grid * sine)[..., None, None]
        derivatives = (derivative_r, derivative_theta, derivative_phi)
        static_density = 4 * sum(
            frobenius_squared(commutator(derivatives[a], derivatives[b]))
            for a in range(3) for b in range(a + 1, 3)
        )
        spatial_two = spatial @ spatial
        trace_two = torch.diagonal(spatial_two, dim1=-2, dim2=-1).sum(-1)
        trace_three = torch.diagonal(
            spatial_two @ spatial, dim1=-2, dim2=-1).sum(-1)
        potential = -0.5 * trace_two - trace_three + trace_two**2 + 0.5
        local = static_density + potential
        rho[idx] = float(torch.sum(weights * local)) / 2.0
    return rho


def solve_poisson(rho, radii, g_total):
    """Second-order flux-form FD solve with regular origin and Robin
    exterior match."""
    n = len(radii)
    h = radii[1] - radii[0]
    r_half = 0.5 * (radii[:-1] + radii[1:])
    rows, cols, vals = [], [], []

    def add(row, col, value):
        rows.append(row)
        cols.append(col)
        vals.append(value)

    # Origin: (-3 P0 + 4 P1 - P2)/(2h) = 0
    add(0, 0, -3.0 / (2.0 * h))
    add(0, 1, 4.0 / (2.0 * h))
    add(0, 2, -1.0 / (2.0 * h))
    # Interior flux form
    for i in range(1, n - 1):
        flux_hi = r_half[i]**2 / h**2
        flux_lo = r_half[i - 1]**2 / h**2
        add(i, i - 1, flux_lo)
        add(i, i, -(flux_lo + flux_hi))
        add(i, i + 1, flux_hi)
    # Robin: (3 PN - 4 P(N-1) + P(N-2))/(2h) + PN/R = 0
    add(n - 1, n - 3, 1.0 / (2.0 * h))
    add(n - 1, n - 2, -4.0 / (2.0 * h))
    add(n - 1, n - 1, 3.0 / (2.0 * h) + 1.0 / RADIUS)

    rhs = np.zeros(n)
    rhs[1:n - 1] = 4.0 * np.pi * g_total * rho[1:n - 1] * radii[1:n - 1]**2
    matrix = sp_sparse.csr_matrix((vals, (rows, cols)), shape=(n, n))
    return spla.spsolve(matrix.tocsc(), rhs)


def main() -> int:
    from substrate_framework.verification import CheckLedger
    ledger = CheckLedger("P243-attempt-0006-consumer-bvp")

    big = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                      "attempts/0042/largeR-roots.json").read_text())
    record = big["R12"]
    values = np.asarray(record["values"])

    oracle = Oracle(dict(SETTINGS, radial_order=16))
    total_energy, _grad, _hess, components_map = oracle.evaluate(values)
    ledger.check(
        "source_root_provenance",
        abs(total_energy - float(record["energy"])) < 1e-9,
        f"recomputed E={total_energy:.12f} "
        f"committed={float(record['energy']):.12f}",
    )
    e_static = float(components_map["static"])

    # Mass identity on the native quadrature nodes (plain GL sum --
    # never trapezoid over weighted values).
    quad_radii_t, quad_w_t, _, _ = gauss_grid(32, 16, RADIUS)
    quad_radii = quad_radii_t.numpy().astype(float)
    quad_w = quad_w_t.numpy().astype(float)
    rho_quad = sector_density(values, quad_radii)
    m_sector = float(np.sum(
        4.0 * np.pi * quad_w * quad_radii**2 * rho_quad))
    ledger.check(
        "mass_identity_ties_density_to_certified_energy",
        abs(m_sector - e_static) / e_static < 1e-6,
        f"M={m_sector:.9f} E_static={e_static:.9f} "
        f"rel={abs(m_sector - e_static) / e_static:.2e}",
    )

    # FD refinement ladder; density evaluated away from r=0 exactly.
    results = {}
    for n_grid in (600, 1200, 2400):
        radii = np.linspace(0.0, RADIUS, n_grid)
        rho_fd = sector_density(values,
                                np.clip(radii, 1e-3, RADIUS - 1e-6))
        rho_fd[0] = rho_fd[1]
        phi = solve_poisson(rho_fd, radii, G_TOTAL)
        results[n_grid] = {"radii": radii, "phi": phi, "rho": rho_fd}
    phi_r = {n: float(results[n]["phi"][-1]) for n in results}
    d1 = abs(phi_r[1200] - phi_r[600]) / abs(phi_r[600])
    d2 = abs(phi_r[2400] - phi_r[1200]) / abs(phi_r[1200])
    observed_order = float(np.log(d1 / d2) / np.log(2.0))
    ledger.check(
        "mesh_refinement_stability",
        d2 < 5e-3 and d2 < d1,
        f"Phi(R): {phi_r[600]:.6f} -> {phi_r[1200]:.6f} -> "
        f"{phi_r[2400]:.6f}; drifts {d1:.2e} -> {d2:.2e} "
        f"(observed order {observed_order:.2f}, degraded below 2 by "
        f"the near-origin row treatment -- documented, not gated); "
        f"the potential scale itself is GM/R = "
        f"{G_TOTAL * e_static / RADIUS:.1f}",
    )

    radii = results[2400]["radii"]
    phi = results[2400]["phi"]
    rho = results[2400]["rho"]
    integrand = 4.0 * np.pi * radii**2 * rho
    m_enc = np.concatenate(
        ([0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1])
                          * np.diff(radii))))
    grad = np.gradient(phi, radii)
    residuals = []
    for r_s in (1.0, 3.0, 6.0, 9.0, 11.0):
        idx = int(np.argmin(np.abs(radii - r_s)))
        expected = G_TOTAL * m_enc[idx] / radii[idx]**2
        residuals.append(abs(grad[idx] - expected)
                         / max(abs(expected), 1e-30))
    ledger.check(
        "local_gauss_law_monitors",
        max(residuals) < 5e-3,
        f"max relative residual over r=(1,3,6,9,11): "
        f"{max(residuals):.2e}",
    )

    m_final = float(m_enc[-1])
    boundary_scale = G_TOTAL * m_final / RADIUS
    ledger.check(
        "monopole_normalization_at_boundary",
        abs(phi[-1] + boundary_scale) / boundary_scale < 1e-3,
        f"Phi(R)+GM/R={phi[-1] + boundary_scale:.3e} "
        f"vs scale {boundary_scale:.3e}",
    )

    phi_mut = solve_poisson(rho, radii, 1.1 * G_TOTAL)
    scale_err = float(np.max(
        np.abs(phi_mut - 1.1 * phi) / np.maximum(np.abs(phi), 1e-12)))
    ledger.check(
        "coupling_mutation_linear_response",
        scale_err < 1e-7,
        f"max deviation from exact 10 percent scaling: {scale_err:.2e} "
        f"(sparse-solve roundoff floor; Poisson linearity is exact)",
    )

    validity = G_TOTAL * m_final / RADIUS
    regime_note = (
        "weak-field expansion parameter >> 1; the linearized consumer "
        "is formally solved but physically outside its regime for this "
        "sector at xi=0" if validity > 0.1 else "regime acceptable")
    ledger.check(
        "validity_diagnostic_recorded",
        True,
        f"G*M/R = {validity:.3f}: {regime_note}",
    )

    print(json.dumps({
        "background": "P240 R12 order-16 window root",
        "E_static": e_static,
        "M_enclosed": m_final,
        "Phi_R": phi[-1],
        "weak_field_epsilon_GM_over_R": validity,
        "regime": regime_note,
    }, indent=2))
    payload = {
        "meta": {"g_total": G_TOTAL, "radius": RADIUS,
                 "grid": len(radii)},
        "e_static": e_static,
        "m_enclosed": m_final,
        "phi_R": phi[-1],
        "weak_field_epsilon": validity,
        "phi_profile_head": [
            float(v) for v in phi[:: max(1, len(phi) // 32)]],
    }
    (HERE / "bvp-consumer.json").write_text(json.dumps(payload, indent=1))
    print("[DONE] bvp-consumer.json written", flush=True)
    ledger.finish()
    return 0


if __name__ == "__main__":
    sys.exit(main())
