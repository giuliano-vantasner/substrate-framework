"""P241 numerical oracle N03 — impedance matching at a planar interface.

Standalone module: python3 N03_impedance_interface.py

Section 4 states the matching condition rho*(det Theta)^(1/3) = Z0 and
interprets it as "no reflection". The SymPy audit S08 shows the scalar
condition is insufficient for anisotropic media; here we test the 1D
two-media wave equation with variable coefficients,

    u_tt = (1/rho(x)) d/dx [ Theta(x) u_x ],

where Z(x) = sqrt(rho*Theta) is the mechanical impedance and c = sqrt(Theta/
rho) the wave speed. A Gaussian pulse is launched from medium 1; reflected
and transmitted energy fluxes are measured after the pulse clears the
interface at x = 0.

Pass criteria:
  matched case   Z2 = Z1 (Theta2/Theta1 = rho1/rho2): |R| < 0.02;
  mismatched     Z2 = 2 Z1: measured R within 10% of analytic
                 R = ((Z2 - Z1)/(Z2 + Z1))^2 in energy.
This demonstrates both that the scalar matching works in the isotropic 1D
slice AND that mismatched impedance reflects — the direction-dependent
generalization needs the full tensor condition (see S08 module).
"""

from __future__ import annotations

import json

import numpy as np

from _numerics import trapezoid


def run_interface(z_ratio: float, nx: int = 4000, dt: float = 2.5e-3,
                  t_clear: float = 12.0):
    """Launch Gaussian right-moving pulse; return reflected energy fraction."""
    L, X_INT = 30.0, 0.0
    x = np.linspace(-L, L, nx + 1)
    dx = x[1] - x[0]
    rho1 = theta1 = 1.0
    # Medium 2 chosen so that sqrt(rho2*theta2) = z_ratio * Z1 and the
    # speed changes as well (theta2 = z_ratio^2 * rho1 / rho2 with rho2=1).
    if z_ratio == 1.0:
        rho2, theta2 = rho1, theta1
    else:
        rho2 = 1.0
        theta2 = z_ratio**2 * rho1 / rho2  # Z2 = sqrt(theta2*rho2)

    rho = np.where(x < X_INT, rho1, rho2)
    theta = np.where(x < X_INT, theta1, theta2)
    c = np.sqrt(theta / rho)

    # Incident pulse: right-mover u = f(x - c1 t) needs v = -c1 * u_x at t=0,
    # otherwise the zero-velocity launch splits the pulse and fakes reflection.
    u = np.exp(-((x + 8.0) / 0.8) ** 2)
    v = -np.sqrt(theta1) * np.gradient(u, dx)
    n_steps = int(round(t_clear / dt))
    for _ in range(n_steps):
        g = np.gradient(u, dx)
        a = np.gradient(theta * g, dx) / rho  # (1/rho) d/dx(Theta u_x)
        v += 0.5 * dt * a
        u += dt * v
        g = np.gradient(u, dx)
        a = np.gradient(theta * g, dx) / rho
        v += 0.5 * dt * a


    kin = 0.5 * rho * v**2
    pot = 0.5 * theta * np.gradient(u, dx) ** 2
    left = trapezoid((kin + pot)[x < X_INT], x[x < X_INT])
    total = trapezoid(kin + pot, x)
    return float(left / max(total, 1e-300))


def main() -> dict[str, object]:
    r_matched = run_interface(1.0)
    r_mismatch = run_interface(2.0)
    analytic_mismatch = ((2.0 - 1.0) / (2.0 + 1.0)) ** 2  # energy ratio

    ok = r_matched < 0.02 and abs(r_mismatch - analytic_mismatch) < 0.10 * analytic_mismatch
    detail = (
        f"Matched interface (Z2 = Z1): reflected energy fraction "
        f"{r_matched:.4f} < 0.02 (numerically reflectionless). Mismatched "
        f"(Z2 = 2 Z1): measured {r_mismatch:.4f} vs analytic energy reflection "
        f"{analytic_mismatch:.4f}. The scalar matching condition is exact only "
        "in this isotropic slice; anisotropic interfaces require the full "
        "directional impedance tensor (S08 revision)."
    )
    return {"name": "scipy_impedance_interface", "claim": "P241-S08 support",
            "passed": bool(ok), "detail": detail}


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
