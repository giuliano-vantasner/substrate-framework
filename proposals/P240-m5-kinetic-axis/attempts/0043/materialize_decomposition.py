"""Materializes the generator-decomposition numbers cited in attempt 0043
AMEND-3/S3 (review follow-up: provenance).  Reproduces the regional split of
the kinetic-matrix integrand at d=20 base level on the FULL domain (no ball
mask): matched-generator vs misaligned-generator contributions.

Expected reproduction (base level): I11 in ball1 ~ 27.0, I11 in ball2 ~ 321.7,
I11 outside ~ 1053; static ball1 = ball2 ~ 61.4, outside ~ 8.9.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / ".." / "0041"))

from cpu_energy import commutator, frobenius_squared, DTYPE  # noqa: E402
from pair_oracle import (
    build_field, deriv_matrix_of, gauss_grid, load_root, summed_angle, ROTATION_Z,
)

RESULTS = HERE / "generator-decomposition.json"


def main():
    root, order, _ = load_root()
    separation, box_radius = 20.0, 8.0
    radial_nodes, angular_nodes = 80, 40
    domain_radius = separation / 2 + 8.0

    radial, radial_weight, mu, angular_weight = gauss_grid(
        radial_nodes, angular_nodes, domain_radius
    )
    r = radial[:, None].repeat(1, angular_nodes).clone().requires_grad_(True)
    mu_g = mu[None, :].repeat(radial_nodes, 1).clone().requires_grad_(True)

    rho = r * torch.sqrt(torch.clamp(1 - mu_g**2, min=0.0))
    zc = r * mu_g
    half = separation / 2.0
    offsets = (-half, half)
    ra_list = [torch.sqrt(rho**2 + (zc - off) ** 2 + 1e-300) for off in offsets]
    theta_sum = summed_angle(rho, zc, offsets, (True, True))
    spatial = build_field(root, order, ra_list, box_radius, theta_sum, (True, True))

    dr = deriv_matrix_of(spatial, r)
    dmu = deriv_matrix_of(spatial, mu_g)
    sin_g = torch.sqrt(torch.clamp(1 - mu_g**2, min=1e-300))
    dth = -sin_g[..., None, None] * dmu / r[..., None, None]
    dph = (ROTATION_Z @ spatial + spatial @ ROTATION_Z.T) / ((r * sin_g)[..., None, None])
    derivatives = (dr, dth, dph)

    weights = 2 * torch.pi * r**2 * radial_weight[:, None] * angular_weight[None, :]
    in_ball = [(ra <= box_radius).to(DTYPE) for ra in ra_list]
    outside = (1.0 - in_ball[0] - in_ball[1]).clamp(min=0)

    zero = torch.zeros_like(r)
    responses = []
    for a in range(2):
        na = torch.stack(
            (rho / ra_list[a], zero, (zc - offsets[a]) / ra_list[a]), dim=-1
        )
        nx, ny, nz = na.unbind(-1)
        gen = torch.stack(
            (
                torch.stack((zero, -nz, ny), dim=-1),
                torch.stack((nz, zero, -nx), dim=-1),
                torch.stack((-ny, nx, zero), dim=-1),
            ),
            dim=-2,
        )
        responses.append(gen @ spatial + spatial @ gen.transpose(-1, -2))

    ks = [[commutator(resp, d) for d in derivatives] for resp in responses]

    def density(a, b):
        return 4 * sum(
            torch.sum(ks[a][idx] * ks[b][idx], dim=(-2, -1)) for idx in range(3)
        )

    static_density = 4 * sum(
        frobenius_squared(commutator(derivatives[i], derivatives[j]))
        for i in range(3)
        for j in range(i + 1, 3)
    )

    def region_total(dens, mask):
        return float(torch.sum(weights * mask * dens).detach())

    out = {
        "configuration": "d=20 base level (80x40), full domain (no ball mask)",
        "purpose": "provenance for attempt-0043 AMEND-3/S3 misaligned-generator diagnosis",
        "regions": ["ball1", "ball2", "outside"],
        "I11_by_region": [
            region_total(density(0, 0), m) for m in (in_ball[0], in_ball[1], outside)
        ],
        "I22_by_region": [
            region_total(density(1, 1), m) for m in (in_ball[0], in_ball[1], outside)
        ],
        "static_by_region": [
            region_total(static_density, m) for m in (in_ball[0], in_ball[1], outside)
        ],
        "I12_by_region": [
            region_total(density(0, 1), m) for m in (in_ball[0], in_ball[1], outside)
        ],
    }
    RESULTS.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
