"""Analytic-track diagnostics (Kelvin's variational sign program, stage 1).

1. Magnitude of the background split profile delta_0 at the N=20 root
   (the smallness premise for channel decoupling).
2. Identification of the lambda_2 ~ +2.5e-7 mode: shape, nodes, overlap with
   natural soft directions of the split channel.
3. Basis-free trial-function Rayleigh quotient: for an explicit admissible
   polynomial trial eta(x) = x^4 (1-x^2) psi(x^2), exactly representable in the
   Chebyshev(2x^2-1) basis, evaluate
       Q[eta] = d^2/d eps^2 E[M0 + eps eta] |_{eps=0}
   by exact autograd at the frozen stationary profile.  This is the continuum
   second variation along ONE admissible direction -- no basis truncation, no
   min-max extrapolation.  Q[eta] < 0 proves the continuum infimum < 0 (saddle)
   representation-independently, modulo quadrature/float64 control, which we
   report across three quadrature orders and two step sizes.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

import sys

sys.path.insert(0, str(HERE))
import torch

from solve_radial_1d import Oracle, energy_radial  # noqa: E402


def load_root(order=20):
    rows = json.loads((HERE / "radial-results.json").read_text())
    row = [r for r in rows if r["radial_order"] == order][0]
    return np.asarray(row["values"], dtype=np.float64)


def pad(values: np.ndarray, new_order: int):
    old = values.reshape(3, -1)
    out = np.zeros((3, new_order), dtype=np.float64)
    out[:, : old.shape[1]] = old
    return out.ravel()


def poly_in_s_to_chebyshev_coeffs(monomial_coeffs):
    """Convert monomial coefficients in s (= x^2) to coefficients of
    T_i(2s-1).  Exact to machine precision for degree <= 20 at this grid."""
    s = np.linspace(0.0, 1.0, 20001)
    values = sum(c * s**k for k, c in enumerate(monomial_coeffs))
    angle = np.arccos(np.clip(2 * s - 1, -1, 1))
    basis = np.cos(np.outer(angle, np.arange(len(monomial_coeffs))))
    sol, *_ = np.linalg.lstsq(basis, values, rcond=None)
    residual = float(np.max(np.abs(basis @ sol - values)))
    return sol, residual


def main():
    root20 = load_root(20)
    order = 20

    # ---- 1. background split magnitude -------------------------------------
    old = root20.reshape(3, order)
    x = np.linspace(0.0, 1.0, 4001)
    angle = np.arccos(np.clip(2 * x**2 - 1, -1, 1))
    basis = np.cos(np.outer(angle, np.arange(order)))
    prof = basis @ old.T  # columns: q-modal D, t-modal T, split-modal S(x)
    delta_phys = x**4 * (1 - x**2) * prof[:, 2]
    t_phys = (1 - x**2) * (1 / 3 + prof[:, 1])
    q_phys = x**2 + x**2 * (1 - x**2) * prof[:, 0]
    print("== background profile magnitudes at N=20 root ==")
    print(f"max|delta_0(x)| = {np.max(np.abs(delta_phys)):.6f} at x={x[np.argmax(np.abs(delta_phys))]:.3f}")
    print(f"max|t_0(x)|     = {np.max(np.abs(t_phys)):.6f}")
    print(f"max|q_0(x)|     = {np.max(np.abs(q_phys)):.6f}")

    # ---- 2. lambda_2 identification ----------------------------------------
    M = 32
    settings = dict(radial_order=M, radial_nodes=48, angular_nodes=16, radius=6.0)
    oracle = Oracle(settings)
    v = pad(root20, M)
    total, grad, hess, comp = oracle.evaluate(v)
    sym = (hess + hess.T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(sym)
    print()
    print("== lowest six eigenvalues at M=32 frozen profile ==")
    print([round(float(e), 9) for e in eigenvalues[:6]])

    angleM = np.arccos(np.clip(2 * x**2 - 1, -1, 1))
    basisM = np.cos(np.outer(angleM, np.arange(M)))
    dD_x = x**4 * (1 - x**2) * prof[:, 2]  # background physical delta shape
    for which, name in ((0, "lambda_min mode"), (1, "lambda_2 mode")):
        vec = eigenvectors[:, which]
        m3 = vec.reshape(3, M)
        prof_mode = basisM @ m3.T
        frac = np.linalg.norm(m3, axis=1) ** 2 / np.linalg.norm(vec) ** 2
        phys = x**4 * (1 - x**2) * prof_mode[:, 2]
        phys *= np.sign(phys[np.argmax(np.abs(phys))])
        interior = np.where((np.diff(np.sign(phys[:-1])) != 0) & (x[1:-1] > 1e-3))[0]
        # cosine similarity with the background delta profile direction
        cos_bg = float(
            abs(np.trapz(phys * dD_x, x))
            / (np.sqrt(np.trapz(phys**2, x)) * np.sqrt(np.trapz(dD_x**2, x)))
        )
        print(
            f"{name}: lam={eigenvalues[which]:+.3e}  "
            f"fractions={np.round(frac, 5).tolist()}  "
            f"interior nodes={len(interior)} at x~{np.round(x[interior + 1], 3).tolist()}  "
            f"|cos| vs background delta shape={cos_bg:.4f}"
        )

    # ---- 3. basis-free trial-function Rayleigh quotient --------------------
    print()
    print("== basis-free trial function Q[eta] at frozen profile ==")

    def energy_value_only(values, rq, aq):
        variable = torch.tensor(values, dtype=torch.float64, requires_grad=True)
        total, _ = energy_radial(
            variable,
            radial_order=M,
            radial_nodes=rq,
            angular_nodes=aq,
            radius=6.0,
        )
        return float(total.detach())

    def rayleigh(direction, eps, rq, aq):
        d = direction / np.linalg.norm(direction)
        t0 = energy_value_only(v, rq, aq)
        tp = energy_value_only(v + eps * d, rq, aq)
        tm = energy_value_only(v - eps * d, rq, aq)
        return (tp - 2 * t0 + tm) / eps**2

    # Trial functions: the computed eigenmode itself and its degree-16
    # truncation.  Provenance is irrelevant to a variational bound -- any
    # admissible eta with Q[eta] < 0 proves the continuum infimum is negative.
    trials = {}
    for deg in (32, 16):
        block = eigenvectors[:, 0].reshape(3, M).copy()
        block[:, deg:] = 0.0
        trials[f"eigenmode truncated to degree {deg}"] = block.ravel()

    for name, direction in trials.items():
        line = f"{name:>34s}:"
        for rq, aq in ((48, 16), (80, 28)):
            q1 = rayleigh(direction, 1e-3, rq, aq)
            q2 = rayleigh(direction, 3e-3, rq, aq)
            line += f"  [{rq}x{aq}] Q(1e-3)={q1:+.8f} Q(3e-3)={q2:+.8f};"
        print(line, flush=True)


if __name__ == "__main__":
    main()
