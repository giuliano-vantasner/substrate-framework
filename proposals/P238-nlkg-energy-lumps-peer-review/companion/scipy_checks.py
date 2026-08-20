"""Independent floating-point, domain, and characteristic-surface probes."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import numpy as np
from scipy.linalg import inv, norm
from scipy.optimize import brentq


@dataclass(frozen=True)
class Check:
    claim: str
    name: str
    passed: bool
    value: float
    threshold: str


def run() -> list[Check]:
    checks: list[Check] = []

    def record(claim: str, name: str, passed: bool, value: float, threshold: str) -> None:
        checks.append(Check(claim, name, bool(passed), float(value), threshold))

    # P238-S03: equal determinant does not imply equal normal impedance.
    reflection = (2.0 - 1.0) / (2.0 + 1.0)
    record("P238-S03", "determinant-matched interface reflection", abs(reflection) > 0.3, reflection, "absolute value > 0.3")

    # P238-S05: sweep directions away from the principal axes.
    angles = np.linspace(0.0, np.pi / 2.0, 1001)
    directions = np.stack((np.cos(angles), np.sin(angles)), axis=1)
    acoustic = np.diag([1.0, 4.0])
    index_tensor = np.diag([1.0, 0.5])
    true_index = 1.0 / np.sqrt(np.einsum("ni,ij,nj->n", directions, acoustic, directions))
    tensor_quadratic = np.einsum("ni,ij,nj->n", directions, index_tensor, directions)
    directional_gap = np.max(np.abs(true_index - tensor_quadratic))
    record("P238-S05", "off-axis directional-index gap", directional_gap > 1e-3, directional_gap, "> 1e-3")

    # P238-S11: matrix inversion at a generic anisotropic flowing point.
    n_matrix = np.diag([2.0, 3.0])
    nbar = np.sqrt(np.linalg.det(n_matrix))
    velocity = np.array([0.1, -0.2])
    b_matrix = inv(n_matrix @ n_matrix)
    contra = np.block(
        [
            [np.array([[-1.0]]), -velocity.reshape(1, 2)],
            [-velocity.reshape(2, 1), b_matrix - np.outer(velocity, velocity)],
        ]
    )
    paper_covariant = np.block(
        [
            [np.array([[-1.0 / nbar + velocity @ n_matrix @ velocity]]), (n_matrix @ velocity).reshape(1, 2)],
            [(n_matrix @ velocity).reshape(2, 1), n_matrix],
        ]
    )
    paper_residual = norm((nbar * contra) @ paper_covariant - np.eye(3), ord=np.inf)
    correct_covariant = inv(nbar * contra)
    correct_residual = norm((nbar * contra) @ correct_covariant - np.eye(3), ord=np.inf)
    record("P238-S11", "paper inverse residual", paper_residual > 0.1, paper_residual, "> 0.1")
    record("P238-S11", "correct block inverse residual", correct_residual < 1e-12, correct_residual, "< 1e-12")

    # P238-S14: profiles are SPD and determinant-matched on an exterior grid.
    radii = np.geomspace(1.000001, 100.0, 2000)
    factor = 1.0 - 1.0 / radii
    rho = factor ** (-0.75)
    theta_r = factor ** 1.25
    theta_t = factor ** 0.25
    matching_residual = np.max(np.abs(rho * np.sqrt(theta_r * theta_t) - 1.0))
    minimum_profile = np.min(np.stack((rho, theta_r, theta_t)))
    record("P238-S14", "exterior determinant matching", matching_residual < 5e-13, matching_residual, "< 5e-13")
    record("P238-S14", "exterior profile positivity", minimum_profile > 0.0, minimum_profile, "> 0")

    # P238-S16/S17: compare the minimal rotating model with Kerr and locate its
    # two characteristic surfaces for the paper's plotted a=0.1*rs example.
    rs = 1.0
    spin = 0.1

    def rotating_factor(radius: float) -> float:
        return 1.0 - rs / radius + spin**2 / radius**2

    outer_horizon = brentq(rotating_factor, rs / 2.0, 2.0 * rs)

    def ergo_function(radius: float) -> float:
        return spin**2 / radius**2 - rotating_factor(radius)

    ergosurface = brentq(ergo_function, outer_horizon * (1.0 + 1e-8), 2.0 * rs)
    analytic_outer = (rs + np.sqrt(rs**2 - 4.0 * spin**2)) / 2.0
    record("P238-S17", "outer horizon root", abs(outer_horizon - analytic_outer) < 1e-12, outer_horizon - analytic_outer, "absolute error < 1e-12")
    record("P238-S17", "equatorial ergosurface", abs(ergosurface - rs) < 1e-12, ergosurface - rs, "absolute error < 1e-12")

    inside_ergo = 0.5 * (outer_horizon + ergosurface)
    outside_ergo = 1.5 * rs
    counter_inside = spin / inside_ergo - np.sqrt(rotating_factor(inside_ergo))
    counter_outside = spin / outside_ergo - np.sqrt(rotating_factor(outside_ergo))
    co_inside = spin / inside_ergo + np.sqrt(rotating_factor(inside_ergo))
    record("P238-S17", "counter-rotating root reverses inside ergoregion", counter_inside > 0.0 and counter_outside < 0.0, counter_inside, "inside > 0 and outside < 0")
    record("P238-S17", "co-rotating root does not reverse", co_inside > 0.0, co_inside, "> 0")

    sample_radius = 2.0 * rs
    acoustic_tphi = -spin
    kerr_tphi = -spin * rs / sample_radius
    cross_gap = abs(acoustic_tphi - kerr_tphi)
    acoustic_phiphi = sample_radius**2
    kerr_phiphi = sample_radius**2 + spin**2 + spin**2 * rs / sample_radius
    angular_gap = abs(acoustic_phiphi - kerr_phiphi)
    record("P238-S16", "minimal-model Kerr cross-term mismatch", cross_gap > 1e-3, cross_gap, "> 1e-3")
    record("P238-S16", "minimal-model Kerr angular mismatch", angular_gap > 1e-3, angular_gap, "> 1e-3")

    return checks


def main() -> int:
    checks = run()
    print(json.dumps({"oracle": "scipy", "checks": [asdict(item) for item in checks]}, indent=2))
    return 0 if all(item.passed for item in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
