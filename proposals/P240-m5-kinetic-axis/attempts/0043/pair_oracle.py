"""P240 attempt 0043: relaxed fixed-J pair oracle (issue #151 Phase 2, item 4).

Certified cpu_energy chart. Composition per manifest AMEND-1/AMEND-2:
deviation-additive profiles (q = q1+q2-1, tangent = t1+t2, split = s1+s2)
evaluated per center at r_a = |x - x_a| on the committed P236 summed-angle
frame Theta(x) = sum_a active_a * arctan2(rho, z - z_a), activity-weighted.
Near core a, Theta = theta_a + pi + O(R/d); all frame vectors enter as outer
products, so the pi offset leaves defect a's certified field exactly invariant.
Pole rule: delta = split * sin^2(Theta). Profiles pinned to vacuum beyond each
defect ball; observables integrated over the union-ball mask (AMEND-1).

Meridian path for pair axis = z (configuration axisymmetric; density
phi-invariance makes the 2*pi factor exact); full 3D Cartesian path for the
pair-along-x covariance gate. First derivatives only, no create_graph.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "../0041"))

from cpu_energy import DTYPE, chebyshev_stack, commutator, frobenius_squared  # noqa: E402

VACUUM_Q = 1.0
ROTATION_Z = torch.tensor(
    [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=DTYPE
)


def gauss_grid(radial_nodes: int, angular_nodes: int, radius: float):
    radial_x, radial_w = np.polynomial.legendre.leggauss(radial_nodes)
    angular_x, angular_w = np.polynomial.legendre.leggauss(angular_nodes)
    radial = radius * (radial_x + 1.0) / 2.0
    radial_weight = radius * radial_w / 2.0
    return tuple(
        torch.tensor(value, dtype=DTYPE)
        for value in (radial, radial_weight, angular_x, angular_w)
    )


def profiles_at(coeff: torch.Tensor, x: torch.Tensor, order: int):
    """Radial profiles (q, tangent, split); pinned to vacuum for x > 1."""
    clamped = torch.clamp(x, max=1.0)
    basis = chebyshev_stack(2 * clamped**2 - 1, tuple(range(order)))
    modal = torch.einsum("...i,ci->...c", basis, coeff)
    q = x**2 + x**2 * (1 - x**2) * modal[..., 0]
    tangent = (1 - x**2) * (torch.tensor(1 / 3, dtype=DTYPE) + modal[..., 1])
    split = x**4 * (1 - x**2) * modal[..., 2]
    one = torch.ones_like(q)
    zero = torch.zeros_like(q)
    return (
        torch.where(x <= 1.0, q, one),
        torch.where(x <= 1.0, tangent, zero),
        torch.where(x <= 1.0, split, zero),
    )


def summed_angle(rho, axis_coord, offsets, active):
    """Theta = sum_a active_a * arctan2(rho, axis_coord - offset_a)."""
    theta = None
    for a in range(2):
        if not active[a]:
            continue
        t_a = torch.arctan2(rho, axis_coord - offsets[a])
        theta = t_a if theta is None else theta + t_a
    if theta is None:
        theta = torch.zeros_like(rho)
    return theta


def build_field(root, order, ra_list, box_radius, theta_sum, active):
    """Deviation-additive field on the summed-angle frame."""
    coeff = torch.tensor(root.reshape(3, order), dtype=DTYPE)
    prof = []
    for a in range(2):
        if active[a]:
            prof.append(profiles_at(coeff, ra_list[a] / box_radius, order))
        else:
            one = torch.ones_like(theta_sum)
            zero = torch.zeros_like(theta_sum)
            prof.append((one, zero, zero))
    q = prof[0][0] + prof[1][0] - VACUUM_Q
    tangent = prof[0][1] + prof[1][1]
    split = prof[0][2] + prof[1][2]

    sin_t = torch.sin(theta_sum)
    cos_t = torch.cos(theta_sum)
    delta = split * sin_t**2
    zero = torch.zeros_like(sin_t)
    director = torch.stack((sin_t, zero, cos_t), dim=-1)
    polar = torch.stack((cos_t, zero, -sin_t), dim=-1)
    azimuthal = torch.stack((zero, torch.ones_like(zero), zero), dim=-1)

    def outer(v):
        return v[..., :, None] * v[..., None, :]

    lambda_n = tangent + q
    spatial = (
        lambda_n[..., None, None] * outer(director)
        + (tangent + delta)[..., None, None] * outer(polar)
        + (tangent - delta)[..., None, None] * outer(azimuthal)
    )
    return spatial


def deriv_matrix_of(spatial, wrt):
    rows = []
    for left in range(3):
        columns = []
        for right in range(3):
            g = torch.autograd.grad(
                spatial[..., left, right].sum(),
                wrt,
                retain_graph=True,
                allow_unused=True,
            )[0]
            columns.append(g if g is not None else torch.zeros_like(wrt))
        rows.append(torch.stack(columns, dim=-1))
    return torch.stack(rows, dim=-2)


def evaluate_pair(
    root: np.ndarray,
    *,
    order: int,
    separation: float,
    box_radius: float,
    domain_radius: float,
    radial_nodes: int,
    angular_nodes: int,
    active: tuple[bool, bool] = (True, True),
    want_diagnostics: bool = False,
    ball_mask: bool = False,
):
    """Meridian-path evaluation (pair axis = z): statics and kinetic matrix."""
    radial, radial_weight, mu, angular_weight = gauss_grid(
        radial_nodes, angular_nodes, domain_radius
    )
    r = radial[:, None].repeat(1, angular_nodes).clone().requires_grad_(True)
    mu_g = mu[None, :].repeat(radial_nodes, 1).clone().requires_grad_(True)

    rho = r * torch.sqrt(torch.clamp(1 - mu_g**2, min=0.0))
    zc = r * mu_g
    half = separation / 2.0
    offsets = (-half, half)
    ra_list = [
        torch.sqrt(rho**2 + (zc - off) ** 2 + 1e-300) for off in offsets
    ]
    theta_sum = summed_angle(rho, zc, offsets, active)
    spatial = build_field(root, order, ra_list, box_radius, theta_sum, active)

    dr_spatial = deriv_matrix_of(spatial, r)
    dmu_spatial = deriv_matrix_of(spatial, mu_g)
    sin_g = torch.sqrt(torch.clamp(1 - mu_g**2, min=1e-300))
    dtheta_spatial = -sin_g[..., None, None] * dmu_spatial / r[..., None, None]
    dphi_spatial = (ROTATION_Z @ spatial + spatial @ ROTATION_Z.T) / (
        (r * sin_g)[..., None, None]
    )
    derivatives = (dr_spatial, dtheta_spatial, dphi_spatial)

    weights = 2 * torch.pi * r**2 * radial_weight[:, None] * angular_weight[None, :]
    if ball_mask:
        mask = torch.zeros_like(r)
        for ra in ra_list:
            mask = mask + (ra <= box_radius).to(DTYPE)
        weights = weights * mask

    static_density = 4 * sum(
        frobenius_squared(commutator(derivatives[i], derivatives[j]))
        for i in range(3)
        for j in range(i + 1, 3)
    )
    curvature = torch.sum(weights * static_density)

    spatial_two = spatial @ spatial
    trace_two = torch.diagonal(spatial_two, dim1=-2, dim2=-1).sum(-1)
    trace_three = torch.diagonal(spatial_two @ spatial, dim1=-2, dim2=-1).sum(-1)
    potential_density = -0.5 * trace_two - trace_three + trace_two**2 + 0.5
    potential = torch.sum(weights * potential_density)

    # clock generators: N_a = cross(n_a), n_a radial from center a (y=0 plane)
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

    def kk(a, b):
        return torch.sum(
            weights
            * 4
            * sum(
                torch.sum(ks[a][idx] * ks[b][idx], dim=(-2, -1))
                for idx in range(3)
            )
        )

    result = {
        "curvature": float(curvature.detach()),
        "potential": float(potential.detach()),
        "static": float((curvature + potential).detach()),
        "I11": float(kk(0, 0).detach()),
        "I22": float(kk(1, 1).detach()),
        "I12": float(kk(0, 1).detach()),
    }
    if want_diagnostics:
        shell = 0.25
        mask = torch.zeros_like(r)
        for ra in ra_list:
            mask = mask + ((ra - box_radius).abs() < shell).to(DTYPE)
        c_density = 4 * sum(
            torch.sum(ks[0][idx] * ks[1][idx], dim=(-2, -1)) for idx in range(3)
        )
        result["kink_abs_I12"] = float(
            torch.sum(weights * mask * c_density.abs()).detach()
        )
    return result


def evaluate_pair_3d(
    root: np.ndarray,
    *,
    order: int,
    separation: float,
    box_radius: float,
    domain_radius: float,
    n_r: int,
    n_mu: int,
    n_phi: int,
    axis: str = "z",
    ball_mask: bool = False,
):
    """Full 3D Cartesian quadrature path (covariance gate; any pair axis)."""
    rx, rw = np.polynomial.legendre.leggauss(n_r)
    mx, mw = np.polynomial.legendre.leggauss(n_mu)
    px = np.linspace(0.0, 2 * np.pi, n_phi, endpoint=False)
    rr = domain_radius * (rx + 1) / 2
    r_w = domain_radius * rw / 2

    Rg = torch.tensor(rr, dtype=DTYPE)[:, None, None].expand(n_r, n_mu, n_phi).clone().requires_grad_(True)
    Mg = torch.tensor(mx, dtype=DTYPE)[None, :, None].expand(n_r, n_mu, n_phi).clone().requires_grad_(True)
    Pg = torch.tensor(px, dtype=DTYPE)[None, None, :].expand(n_r, n_mu, n_phi).clone().requires_grad_(True)

    sp, cp = torch.sin(Pg), torch.cos(Pg)
    s_th = torch.sqrt(torch.clamp(1 - Mg**2, min=0.0))
    xs, ys, zs = Rg * s_th * sp, Rg * s_th * cp, Rg * Mg
    half = separation / 2.0
    if axis == "z":
        offs = ((0.0, 0.0, -half), (0.0, 0.0, half))
        rho_ax = torch.sqrt(xs**2 + ys**2 + 1e-300)
        ax_c = zs
    else:
        offs = ((-half, 0.0, 0.0), (half, 0.0, 0.0))
        rho_ax = torch.sqrt(ys**2 + zs**2 + 1e-300)
        ax_c = xs
    ra = [
        torch.sqrt((xs - o[0]) ** 2 + (ys - o[1]) ** 2 + (zs - o[2]) ** 2 + 1e-300)
        for o in offs
    ]
    theta_sum = summed_angle(rho_ax, ax_c, (offs[0][0] if axis == "x" else offs[0][2],
                                            offs[1][0] if axis == "x" else offs[1][2]),
                             (True, True))

    coeff = torch.tensor(root.reshape(3, order), dtype=DTYPE)
    prof = [profiles_at(coeff, ra[a] / box_radius, order) for a in range(2)]
    q = prof[0][0] + prof[1][0] - VACUUM_Q
    tangent = prof[0][1] + prof[1][1]
    split = prof[0][2] + prof[1][2]
    delta = split * torch.sin(theta_sum) ** 2

    st, ct = torch.sin(theta_sum), torch.cos(theta_sum)
    zero = torch.zeros_like(st)
    if axis == "z":
        director = torch.stack((st * sp, st * cp, ct), dim=-1)
        polar = torch.stack((ct * sp, ct * cp, -st), dim=-1)
        azimuthal = torch.stack((-cp, sp, zero), dim=-1)
    else:  # pair axis = x; transverse angle is Pg measured from +y
        director = torch.stack((ct, st * cp, st * sp), dim=-1)
        polar = torch.stack((-st, ct * cp, ct * sp), dim=-1)
        azimuthal = torch.stack((zero, -sp, cp), dim=-1)

    def outer(v):
        return v[..., :, None] * v[..., None, :]

    lambda_n = tangent + q
    spatial = (
        lambda_n[..., None, None] * outer(director)
        + (tangent + delta)[..., None, None] * outer(polar)
        + (tangent - delta)[..., None, None] * outer(azimuthal)
    )

    dr = deriv_matrix_of(spatial, Rg)
    dmu = deriv_matrix_of(spatial, Mg)
    dph = deriv_matrix_of(spatial, Pg)
    sin_safe = torch.clamp(s_th, min=1e-300)
    if axis == "z":
        e_r, e_th, e_ph = director, polar, azimuthal
        dth_scale = -Rg * sin_safe
        dph_scale = Rg * sin_safe
    else:
        e_r, e_th, e_ph = director, polar, azimuthal
        dth_scale = -Rg * sin_safe
        dph_scale = Rg * sin_safe
    ex = (
        e_r[..., 0][..., None, None] * dr
        + e_th[..., 0][..., None, None] * dmu / dth_scale[..., None, None]
        + e_ph[..., 0][..., None, None] * dph / dph_scale[..., None, None]
    )
    ey = (
        e_r[..., 1][..., None, None] * dr
        + e_th[..., 1][..., None, None] * dmu / dth_scale[..., None, None]
        + e_ph[..., 1][..., None, None] * dph / dph_scale[..., None, None]
    )
    ez = (
        e_r[..., 2][..., None, None] * dr
        + e_th[..., 2][..., None, None] * dmu / dth_scale[..., None, None]
        + e_ph[..., 2][..., None, None] * dph / dph_scale[..., None, None]
    )
    derivs = (ex, ey, ez)

    weights = (
        torch.tensor(r_w, dtype=DTYPE)[:, None, None]
        * torch.tensor(mw, dtype=DTYPE)[None, :, None]
        * (2 * np.pi / n_phi)
        * torch.ones_like(Pg)
        * Rg**2
    )
    if ball_mask:
        mask = torch.zeros_like(Rg)
        for ra_v in ra:
            mask = mask + (ra_v <= box_radius).to(DTYPE)
        weights = weights * mask

    static_density = 4 * sum(
        frobenius_squared(commutator(derivs[i], derivs[j]))
        for i in range(3)
        for j in range(i + 1, 3)
    )
    curvature = torch.sum(weights * static_density)
    spatial_two = spatial @ spatial
    trace_two = torch.diagonal(spatial_two, dim1=-2, dim2=-1).sum(-1)
    trace_three = torch.diagonal(spatial_two @ spatial, dim1=-2, dim2=-1).sum(-1)
    potential_density = -0.5 * trace_two - trace_three + trace_two**2 + 0.5
    potential = torch.sum(weights * potential_density)

    k_resp = []
    for a in range(2):
        rel = torch.stack(
            (xs - offs[a][0], ys - offs[a][1], zs - offs[a][2]), dim=-1
        )
        na = rel / ra[a][..., None]
        nx, ny, nz = na.unbind(-1)
        gen = torch.stack(
            (
                torch.stack((zero, -nz, ny), dim=-1),
                torch.stack((nz, zero, -nx), dim=-1),
                torch.stack((-ny, nx, zero), dim=-1),
            ),
            dim=-2,
        )
        response = gen @ spatial + spatial @ gen.transpose(-1, -2)
        k_resp.append([commutator(response, d) for d in derivs])

    def kk(a, b):
        return torch.sum(
            weights
            * 4
            * sum(
                torch.sum(k_resp[a][i] * k_resp[b][i], dim=(-2, -1))
                for i in range(3)
            )
        )

    return {
        "curvature": float(curvature.detach()),
        "potential": float(potential.detach()),
        "static": float((curvature + potential).detach()),
        "I11": float(kk(0, 0).detach()),
        "I22": float(kk(1, 1).detach()),
        "I12": float(kk(0, 1).detach()),
    }


def load_root():
    rows = json.load(open(HERE / "../0041/radial-results.json"))
    entry = [r for r in rows if r["radial_order"] == 20][0]
    root = np.asarray(entry["values"], dtype=np.float64)
    return root, root.reshape(3, -1).shape[1], entry


def main():
    """G1 certification: one-body limit must reproduce cpu_energy exactly."""
    root, order, entry = load_root()
    import cpu_energy

    flat = np.zeros((3, order, 1))
    flat[:, :, 0] = root.reshape(3, order)
    ref_total, ref_comps = cpu_energy.energy(
        torch.tensor(flat.ravel(), dtype=DTYPE),
        radial_order=order,
        angular_modes=1,
        radial_nodes=48,
        angular_nodes=16,
        radius=8.0,
    )
    mine = evaluate_pair(
        root, order=order, separation=0.0, box_radius=8.0,
        domain_radius=8.0, radial_nodes=48, angular_nodes=16,
        active=(True, False),
    )
    g1 = {
        "cpu_energy_total": float(ref_total),
        "pair_eval_total": mine["static"] + 1.0 / (4.0 * mine["I11"]),
        "curvature_ref": float(ref_comps["curvature"]),
        "curvature_mine": mine["curvature"],
        "potential_ref": float(ref_comps["potential"]),
        "potential_mine": mine["potential"],
        "inertia_ref": float(ref_comps["inertia"]),
        "inertia_mine": mine["I11"],
    }
    g1["rel_err_total"] = abs(g1["pair_eval_total"] - g1["cpu_energy_total"]) / abs(
        g1["cpu_energy_total"]
    )
    g1["rel_err_inertia"] = abs(g1["inertia_mine"] - g1["inertia_ref"]) / abs(
        g1["inertia_ref"]
    )
    g1["pass"] = bool(
        g1["rel_err_total"] < 1e-10
        and g1["rel_err_inertia"] < 1e-10
        and abs(g1["curvature_mine"] - g1["curvature_ref"])
        < 1e-9 * abs(g1["curvature_ref"])
        and abs(g1["potential_mine"] - g1["potential_ref"])
        < 1e-9 * abs(g1["potential_ref"])
    )
    out = {
        "order": order,
        "reference": {"energy": entry.get("energy"), "inertia": entry.get("inertia")},
        "G1_certification": g1,
    }
    print("G1:", json.dumps(g1, indent=2), flush=True)
    json.dump(out, open(HERE / "pair-results.json", "w"), indent=2)
    if not g1["pass"]:
        raise SystemExit(1)
    print("certification passed", flush=True)


def run_measurement():
    out = json.load(open(HERE / "pair-results.json"))
    if not out.get("G1_certification", {}).get("pass"):
        raise SystemExit("G1 certification not passed; measurement forbidden")
    root, order, _ = load_root()

    separations = [18.0, 20.0, 24.0, 28.0, 32.0]
    levels = {"base": (80, 40), "fine": (120, 60)}
    grid = []
    for d in separations:
        for name, (nr, nm) in levels.items():
            L = d / 2 + 8.0
            common = dict(
                root=root, order=order, separation=d, box_radius=8.0,
                domain_radius=L, radial_nodes=nr, angular_nodes=nm,
            )
            pair = evaluate_pair(**common, want_diagnostics=True, ball_mask=True)
            single = evaluate_pair(**common, active=(True, False), ball_mask=True)
            row = {
                "d": d, "level": name, "L": L, "mask": "balls",
                "C": pair["I12"],
                "I11_pair": pair["I11"], "I22_pair": pair["I22"],
                "I11_single": single["I11"],
                "E_int": pair["static"] - 2 * single["static"],
                "kink_ratio": abs(pair["kink_abs_I12"]) / max(abs(pair["I12"]), 1e-300),
            }
            grid.append(row)
            print(json.dumps(row), flush=True)
    out["grid"] = grid

    top = [r for r in grid if r["d"] == 32.0 and r["level"] == "fine"][0]
    ref_I0 = out["G1_certification"]["inertia_ref"]
    out["G2_self_recovery"] = {
        "I11_pair_ball_d32": top["I11_pair"],
        "I11_single_ball": top["I11_single"],
        "one_body_I0": ref_I0,
        "single_vs_I0_rel": abs(top["I11_single"] - ref_I0) / ref_I0,
        "structural_check_E_int_d32_fine": top["E_int"],
    }
    print("G2:", json.dumps(out["G2_self_recovery"], indent=2), flush=True)

    z3 = evaluate_pair_3d(root, order=order, separation=20.0, box_radius=8.0,
                          domain_radius=18.0, n_r=40, n_mu=20, n_phi=40,
                          axis="z", ball_mask=True)
    x3 = evaluate_pair_3d(root, order=order, separation=20.0, box_radius=8.0,
                          domain_radius=18.0, n_r=40, n_mu=20, n_phi=40,
                          axis="x", ball_mask=True)
    base = [r for r in grid if r["d"] == 20.0 and r["level"] == "base"][0]
    out["G3_rotational_covariance"] = {
        "meridian_z_C": base["C"],
        "path3d_z_C": z3["I12"],
        "path3d_x_C": x3["I12"],
        "z_vs_x_rel": abs(x3["I12"] - z3["I12"]) / max(abs(z3["I12"]), 1e-300),
        "meridian_vs_3d_rel": abs(base["C"] - z3["I12"]) / max(abs(z3["I12"]), 1e-300),
    }
    print("G3:", json.dumps(out["G3_rotational_covariance"], indent=2), flush=True)

    fine = sorted((r for r in grid if r["level"] == "fine"), key=lambda r: r["d"])
    ds = np.array([r["d"] for r in fine])
    Cs = np.array([r["C"] for r in fine])

    def rss(model):
        return float(np.sum((model - Cs) ** 2))

    inv = ds ** -1
    a_pure = float(np.sum(inv * Cs) / np.sum(inv * inv))
    X = np.stack([np.ones_like(ds), inv], axis=1)
    coef, *_ = np.linalg.lstsq(X, Cs, rcond=None)
    logC = np.log(np.abs(Cs))
    slope, intercept = np.polyfit(ds, logC, 1)
    out["model_comparison"] = {
        "fine_points": [{"d": float(d), "C": float(c)} for d, c in zip(ds, Cs)],
        "pure_inv_A": a_pure,
        "rss_pure_inv": rss(a_pure * inv),
        "const_plus_inv_Cinf": float(coef[0]),
        "const_plus_inv_A": float(coef[1]),
        "rss_const_plus_inv": rss(coef[0] + coef[1] * inv),
        "exp_log_slope": float(slope),
        "rss_exp": rss(intercept * np.exp(slope * ds)),
    }
    out["analysis_fine"] = [
        {"d": r["d"], "C": r["C"], "A_scaled": r["C"] * r["d"]} for r in fine
    ]
    json.dump(out, open(HERE / "pair-results.json", "w"), indent=2)
    print("measurement complete", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "measure":
        run_measurement()
    else:
        main()
