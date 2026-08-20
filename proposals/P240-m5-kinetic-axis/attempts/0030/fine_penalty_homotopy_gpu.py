"""Fine penalty continuation for the P240 order-4 Galerkin branch."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import least_squares
import torch


ATTEMPTS = Path(__file__).resolve().parents[1]
SOURCE = ATTEMPTS / "0029" / "track_order4_penalty_homotopy_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0029_homotopy", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
H = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = H
SPEC.loader.exec_module(H)
G = H.G
M = H.M


def main() -> int:
    M.configure_device("cuda")
    parameters = M.Parameters(
        spacing=1 / 3,
        rho_cells=12,
        z_cells=24,
        projector_stiffness=2.0,
    )
    radial_order = 4
    axial_modes = 4
    seed = G.P.T.ORIGINAL_INITIAL_FIELD(parameters, 1.0)
    radial_basis, axial_bases, envelope = G.basis_data(
        parameters, radial_order, axial_modes
    )
    with np.load(ATTEMPTS / "0029" / "coefficients-mu-10000.npz") as state:
        values = np.asarray(state["coefficients"], dtype=np.float64).ravel()
    mask_tensor = np.zeros(
        (len(G.COMPONENTS), radial_order, axial_modes), dtype=np.float64
    )
    mask_tensor[:, -1, :] = 1.0
    mask_tensor[:, :, -1] = 1.0
    mask = mask_tensor.ravel()
    function_args = (
        parameters,
        radial_order,
        axial_modes,
        seed,
        radial_basis,
        axial_bases,
        envelope,
    )
    rows = []
    complete = True
    for penalty in (8000.0, 6000.0, 5000.0, 4000.0, 3000.0, 2500.0, 2000.0, 1750.0, 1500.0, 1250.0, 1000.0):
        oracle = H.PenalizedOracle(function_args, mask, penalty)
        initial_energy, _, _ = oracle.evaluate(values)
        reference_scale = max(1.0, abs(initial_energy))

        def residual(current: np.ndarray) -> np.ndarray:
            return oracle.evaluate(current)[1] / reference_scale

        def jacobian(current: np.ndarray) -> np.ndarray:
            return oracle.evaluate(current)[2] / reference_scale

        solved = least_squares(
            residual,
            values,
            jac=jacobian,
            method="lm",
            ftol=1.0e-14,
            xtol=1.0e-14,
            gtol=1.0e-14,
            max_nfev=80,
        )
        values = np.asarray(solved.x, dtype=np.float64)
        modified_energy, gradient, hessian = oracle.evaluate(values)
        normalized_gradient = float(
            np.max(np.abs(gradient)) / max(1.0, abs(modified_energy))
        )
        eigenvalues = np.linalg.eigvalsh((hessian + hessian.T) / 2)
        closest = float(eigenvalues[np.argmin(np.abs(eigenvalues))])
        stage_pass = bool(solved.success and normalized_gradient <= 1.0e-8)
        artifact = ATTEMPTS / "0030" / f"coefficients-mu-{penalty:g}.npz"
        np.savez_compressed(
            artifact,
            coefficients=values.reshape(
                len(G.COMPONENTS), radial_order, axial_modes
            ),
            penalty=np.array(penalty),
        )
        rows.append(
            {
                "penalty": penalty,
                "success": bool(solved.success),
                "message": str(solved.message),
                "normalized_modified_gradient_inf": normalized_gradient,
                "function_evaluations": int(solved.nfev),
                "exact_hessian_evaluations": oracle.evaluations,
                "minimum_hessian_eigenvalue": float(eigenvalues[0]),
                "hessian_eigenvalue_closest_to_zero": closest,
                "new_mode_coefficient_norm": float(np.linalg.norm(mask * values)),
                "stage_gate_pass": stage_pass,
                "artifact": str(artifact),
            }
        )
        if not stage_pass:
            complete = False
            break
    payload = {
        "campaign": "P240",
        "attempt": "0030",
        "environment": {
            "torch": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "stages": rows,
        "reached_penalty_1000": bool(complete and rows[-1]["penalty"] == 1000.0),
        "physical_action_verdict": "none_penalty_never_zero",
    }
    print("P240_FINE_HOMOTOPY_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if payload["reached_penalty_1000"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
