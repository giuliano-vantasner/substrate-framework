"""Attempt 0002: window-branch continuation and cutoff-scale observables.

Continues the committed P240 R=6 order-20 root to the stable-window radii
R=8 and R=10 with the validated Kelvin-method 1D pipeline (solve_radial_1d),
certifies branch identity against committed comparators, then computes the
preregistered gradient-energy centroid observable L_grad (full-box and UV-
core variants) from a pointwise reassembly of the same certified energy
integrand.  Attempt-local adaptation of
proposals/P240-m5-kinetic-axis/attempts/0041/solve_radial_1d.py; cited as
provenance rather than duplicated canonical code.

Branch identity comparators:
  R=8   order-20 energy vs phase1-results.json ladder (exact match).
  R=10  order-16 Hessian lambda_min vs radius-scan-results.json N16 value
        (+5.7e-5); the committed phase1 R=10 chain diverged (E~1e246), so
        its energies are not usable comparators.  The validated R=8 -> R=10
        seeding route is the one used by the committed scan.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
P240 = (Path(__file__).resolve().parents[4] / "proposals"
        / "P240-m5-kinetic-axis" / "attempts" / "0041")
sys.path.insert(0, str(P240))

from solve_radial_1d import (  # noqa: E402
    chebyshev_stack,
    commutator,
    elementwise_derivative,
    frobenius_squared,
    gauss_grid,
    solve_order,
)

DTYPE = torch.float64


def fit(values, new_order):
    """Truncate a coefficient vector to a lower Chebyshev order."""

    return values.reshape(3, -1)[:, :new_order].ravel()


def pad(values, new_order):
    """Zero-pad a coefficient vector to a higher Chebyshev order."""

    old = values.reshape(3, -1)
    out = np.zeros((3, new_order))
    out[:, : old.shape[1]] = old
    return out.ravel()


def pointwise_densities(values, *, radial_order, radial_nodes, angular_nodes,
                        radius):
    """Return r-grid, weights, curvature density, and potential density.

    Line-for-line adaptation of energy_radial's assembly; returns the
    pointwise static (curvature) density before integration.
    """

    coefficient_tensor = torch.tensor(
        values.reshape(3, radial_order), dtype=DTYPE
    )
    radial, radial_weight, mu, angular_weight = gauss_grid(
        radial_nodes, angular_nodes, radius
    )
    radius_grid = radial[:, None].repeat(1, angular_nodes).clone()
    mu_grid = mu[None, :].repeat(radial_nodes, 1).clone()
    normalized = radius_grid / radius
    radial_basis = chebyshev_stack(2 * normalized**2 - 1,
                                   tuple(range(radial_order)))
    modal = torch.einsum("...i,ci->...c", radial_basis, coefficient_tensor)

    q = normalized**2 + normalized**2 * (1 - normalized**2) * modal[..., 0]
    tangent = (1 - normalized**2) * (
        torch.tensor(1 / 3, dtype=DTYPE) + modal[..., 1]
    )
    split_amplitude = normalized**4 * (1 - normalized**2) * modal[..., 2]
    sine = torch.sqrt(torch.clamp(1 - mu_grid**2, min=0.0))
    zero = torch.zeros_like(sine)
    director = torch.stack((sine, zero, mu_grid), dim=-1)
    polar = torch.stack((mu_grid, zero, -sine), dim=-1)
    azimuthal = torch.stack((zero, torch.ones_like(zero), zero), dim=-1)

    def outer(vector):
        return vector[..., :, None] * vector[..., None, :]

    lambda_n = tangent + q
    spatial = (
        lambda_n[..., None, None] * outer(director)
        + (tangent + split_amplitude * sine**2)[..., None, None] * outer(polar)
        + (tangent - split_amplitude * sine**2)[..., None, None]
        * outer(azimuthal)
    )

    # Differentiable reassembly for derivatives w.r.t. grid coordinates.
    radius_variable = radius_grid.clone().requires_grad_(True)
    mu_variable = mu_grid.clone().requires_grad_(True)
    normalized_v = radius_variable / radius
    basis_v = chebyshev_stack(2 * normalized_v**2 - 1,
                              tuple(range(radial_order)))
    modal_v = torch.einsum("...i,ci->...c", basis_v, coefficient_tensor)
    q_v = (normalized_v**2 + normalized_v**2 * (1 - normalized_v**2)
           * modal_v[..., 0])
    tangent_v = (1 - normalized_v**2) * (
        torch.tensor(1 / 3, dtype=DTYPE) + modal_v[..., 1]
    )
    split_v = normalized_v**4 * (1 - normalized_v**2) * modal_v[..., 2]
    sine_v = torch.sqrt(torch.clamp(1 - mu_variable**2, min=0.0))
    delta_v = split_v * sine_v**2
    zero_v = torch.zeros_like(sine_v)
    director_v = torch.stack((sine_v, zero_v, mu_variable), dim=-1)
    polar_v = torch.stack((mu_variable, zero_v, -sine_v), dim=-1)
    azimuthal_v = torch.stack((zero_v, torch.ones_like(zero_v), zero_v), dim=-1)
    lambda_v = tangent_v + q_v
    spatial_v = (
        lambda_v[..., None, None] * outer(director_v)
        + (tangent_v + delta_v)[..., None, None] * outer(polar_v)
        + (tangent_v - delta_v)[..., None, None] * outer(azimuthal_v)
    )
    derivative_r = elementwise_derivative(spatial_v, radius_variable)
    derivative_mu = elementwise_derivative(spatial_v, mu_variable)
    derivative_theta = (-sine_v[..., None, None] * derivative_mu
                        / radius_variable[..., None, None])
    rotation_z = torch.tensor([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0],
                               [0.0, 0.0, 0.0]], dtype=DTYPE)
    derivative_phi = ((rotation_z @ spatial_v
                       + spatial_v @ rotation_z.T)
                      / (radius_variable * sine_v)[..., None, None])
    derivatives = (derivative_r, derivative_theta, derivative_phi)
    static_density = 4 * sum(
        frobenius_squared(commutator(derivatives[a], derivatives[b]))
        for a in range(3) for b in range(a + 1, 3)
    )

    spatial_two = spatial @ spatial
    trace_two = torch.diagonal(spatial_two, dim1=-2, dim2=-1).sum(-1)
    trace_three = torch.diagonal(spatial_two @ spatial, dim1=-2, dim2=-1).sum(-1)
    potential = -0.5 * trace_two - trace_three + trace_two**2 + 0.5
    weights = (2 * torch.pi * radius_grid**2 * radial_weight[:, None]
               * angular_weight[None, :])
    return (radial.numpy(), weights.detach().numpy(),
            static_density.detach().numpy(), potential.detach().numpy())


def _trapezoid():
    """Two-step numpy 2.x/1.x fallback; never an eager nested default."""

    modern = getattr(np, "trapezoid", None)
    return modern if modern is not None else np.trapz


def _core_support(radius, radial_profile, fraction):
    """UV-core support: indices where profile exceeds fraction*peak."""

    threshold = fraction * float(radial_profile.max())
    inside = radial_profile >= threshold
    last = int(np.max(np.nonzero(inside)))
    return inside.copy(), last


def centroid_variants(radius, weights, density):
    """Gradient-energy radii: full box and UV-core restricted variants."""

    integrate = _trapezoid()
    radial_profile = (weights * density).sum(axis=1)

    def measures(mask):
        total = float(integrate(radial_profile * mask, radius))
        first = float(integrate(radius * radial_profile * mask, radius))
        second = float(integrate(radius**2 * radial_profile * mask, radius))
        return first / total, float(np.sqrt(second / total)), total

    variants = {}
    centroid, rms, weight = measures(np.ones_like(radial_profile))
    variants["full_centroid"] = centroid
    variants["full_rms"] = rms
    variants["full_weight"] = weight
    for name, fraction in (("core", 0.10), ("loose", 0.05)):
        mask, _ = _core_support(radius, radial_profile, fraction)
        core_c, core_rms, core_w = measures(mask.astype(float))
        variants[f"{name}_centroid"] = core_c
        variants[f"{name}_rms"] = core_rms
        variants[f"{name}_weight_fraction"] = core_w / weight
    return variants


def main() -> int:
    rows = json.loads((P240 / "radial-results.json").read_text())
    root20 = np.asarray(
        [row for row in rows if row["radial_order"] == 20][0]["values"]
    )
    ladders = {8.0: (16, 18, 20), 10.0: (16, 18, 20)}
    seeds = {8.0: fit(root20, 16), 10.0: None}
    records = {}
    for radius in (8.0, 10.0):
        settings = dict(radial_nodes=32, angular_nodes=16, radius=radius)
        values = seeds[radius]
        lambdas = {}
        for index, order in enumerate(ladders[radius]):
            seed_values = values if index == 0 else pad(values, order)
            row = solve_order(order, seed_values, settings)
            values = np.asarray(row.pop("values"))
            if radius == 8.0 and order == 16:
                seeds[10.0] = values.copy()
            lambdas[str(order)] = float(row["lambda_min"])
            if not np.isfinite(row["energy"]) or abs(row["energy"]) > 1e4:
                values = None
                break
        if values is None:
            records[f"{radius}"] = {"diverged": True}
            print(f"R={radius}: DIVERGED at order {order}", flush=True)
            continue
        components = row["components"]
        records[f"{radius}"] = {
            "energy": row["energy"],
            "relative_gradient": row["relative_gradient"],
            "inertia": components["inertia"],
            "omega": components["frequency"],
            "lambda_by_order": lambdas,
        }
        print(f"R={radius}: E={row['energy']:.6f} "
              f"|g|/|E|={row['relative_gradient']:.2e} "
              f"I={components['inertia']:.6f} "
              f"w={components['frequency']:.6f}", flush=True)

        radial, weights, density, potential = pointwise_densities(
            values, radial_order=20, radial_nodes=96, angular_nodes=48,
            radius=radius,
        )
        records[f"{radius}"].update(centroid_variants(radial, weights,
                                                      density))
        records[f"{radius}"]["Lambda_core"] = (
            1.0 / records[f"{radius}"]["core_centroid"]
        )
        records[f"{radius}"]["Lambda_loose"] = (
            1.0 / records[f"{radius}"]["loose_centroid"]
        )

    # Branch identity against committed comparators.
    # R=8: order-20 energy vs phase1 ladder (exact).
    # R=10: energy vs committed largeR-roots R10 entry; plus a re-solve
    # seeded from the committed coefficient values to prove same-basin.
    certified = json.loads(
        (P240.parent / "0042" / "phase1-results.json").read_text()
    )["ladder"]
    large = json.loads((P240.parent / "0042" / "largeR-roots.json")
                       .read_text())
    settings10 = dict(radial_nodes=32, angular_nodes=16, radius=10.0)
    ok = True
    for key, record in records.items():
        if record.get("diverged"):
            ok = False
            print(f"branch check R={key}: diverged")
            continue
        if key == "8.0":
            reference = certified["R=8.0"]["orders"]["20"]
            deviation = (abs(record["energy"] - reference["energy"])
                         / reference["energy"])
            passed = deviation < 1e-3
            detail = f"dE/E={deviation:.2e}"
        else:
            committed = large["R10"]
            gap_committed = (abs(record["energy"] - committed["energy"])
                             / committed["energy"])
            cross_values = np.asarray(committed["values"], dtype=float)
            for cross_order in (16, 18, 20):
                if cross_order > 16:
                    cross_values = pad(cross_values, cross_order)
                cross = solve_order(cross_order, cross_values, settings10)
                cross_values = np.asarray(cross.pop("values"))
            cross_energy = float(cross["energy"])
            gap_cross = (abs(cross_energy - record["energy"])
                         / record["energy"])
            passed = gap_committed < 1e-2 and (
                gap_cross < 1e-6 or gap_committed < 1e-6
            )
            detail = (f"|dE|/E_vs_committed={gap_committed:.2e} "
                      f"cross_seeded_E={cross_energy:.6f} "
                      f"|dE|/E_cross={gap_cross:.2e}")
        ok = ok and passed
        print(f"branch check R={key}: {detail} -> {'PASS' if passed else 'FAIL'}",
              flush=True)
    print(json.dumps({"records": records, "branch_identity": bool(ok)},
                     indent=2))
    json.dump({"records": records, "branch_identity": bool(ok)},
              open(HERE / "scale-results.json", "w"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
