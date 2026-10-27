"""Actual QE 7.5 longitudinal-spin Hartree + native PBE-GGA Hessian action.

Equation map: dv_of_drho.f90:179-205 (Hartree and full serial Rho transforms),
:282-298 (dmuxc and dgradcorr); dgradcorr.f90:133-203 (all a,b,c,ps spin
contractions and negative divergence); gradutils.f90:106-163,497-554
(i*tpiba*(G+q) derivatives). setup_dmuxc/setup_dgc already evaluated the
selected native PBE derivative coefficients, including its finite-difference
and density-threshold conventions. They are not fitted Hubbard parameters.

Input response columns are up/down, although stored background rho columns are
total density/magnetization. Native coefficients have Ry conventions already;
there is no extra e2 on XC and no spin multiplicity. Kernel validation alone
licenses neither finite-z response nor material coherence/loss/nuclear claims.
"""
from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .qe_response_bundle import QEResponseBundle
from .qe_response_fft import NativeRhoFFT


def _coefficient(bundle: QEResponseBundle, name: str, nnr: int,
                 cross_spin: bool) -> NDArray[Any]:
    field = bundle.background.array(name, (nnr, 2, 2), "float64")
    if cross_spin:
        return field
    field = field.copy()
    field[:, 0, 1] = 0
    field[:, 1, 0] = 0
    return field


def _gga_action(bundle: QEResponseBundle, fft: NativeRhoFFT,
                density: NDArray[Any], cross_spin: bool) -> NDArray[Any]:
    """Literal collinear dgradcorr contractions, without a conjugated gradient."""
    grho = bundle.background.array("grho", (3, fft.nnr, 2), "float64")
    rr, sr, ss, s = (_coefficient(bundle, name, fft.nnr, cross_spin)
                     for name in ("dvxc_rr", "dvxc_sr", "dvxc_ss", "dvxc_s"))
    gradient = fft.gradient(density)
    ps = np.einsum("cni,cnj->nij", grho, gradient)
    result = np.einsum("nij,nj->ni", rr, density)
    h = np.einsum("nij,cnj->cni", s, gradient)
    # The a/c/b tensors are not simply rank-two matrix products: QE repeats
    # its off-diagonal sr/ss entries across every mixed-spin index tuple.
    for i in range(2):
        for j in range(2):
            for k in range(2):
                same3 = i == j == k
                a = sr[:, i, i] if same3 else sr[:, i, 1 - i]
                c = sr[:, i, i] if same3 else sr[:, j, 1 - j]
                result[:, i] += a * ps[:, j, k]
                h[:, :, i] += (c * density[:, j])[None, :] * grho[:, :, k]
                for l in range(2):
                    b = ss[:, i, i] if same3 and k == l else ss[:, i, 1 - i]
                    h[:, :, i] += (b * ps[:, j, k])[None, :] * grho[:, :, l]
    return result - fft.divergence(h)


def _apply(bundle: QEResponseBundle, delta_n: ArrayLike, *,
           gga: bool = True, cross_spin: bool = True) -> NDArray[np.complex128]:
    fft = NativeRhoFFT.from_bundle(bundle)
    density = np.asarray(delta_n)
    if density.shape != (fft.nnr, 2) or not np.iscomplexobj(density):
        raise ValueError("delta_n must be complex up/down envelopes of shape (nnr,2)")
    if not np.isfinite(density).all():
        raise ValueError("delta_n must contain finite complex envelopes")
    bg = bundle.background
    if bg.metadata["lrpa"]:
        xc = np.zeros((fft.nnr, 2), dtype=np.complex128)
    else:
        dmuxc = _coefficient(bundle, "dmuxc", fft.nnr, cross_spin)
        xc = np.einsum("nij,nj->ni", dmuxc, density)
        if gga:
            xc += _gga_action(bundle, fft, density, cross_spin)
    # Serial Rho transforms are full cfft3d (fft_fwinv.f90:98-100,201-203).
    # The final XC forward/inverse pair is identity, NOT a G/nl projection.
    # Native G/nl projection applies to derivatives and Coulomb addition only.
    total_g = fft.to_g(density[:, :1] + density[:, 1:2])[:, 0]
    qg2 = np.sum(fft.wavevectors ** 2, axis=0) / bg.metadata["tpiba"] ** 2
    admitted = qg2 > 1e-8  # Native dimensionless threshold, not exact-zero only.
    if bg.metadata["lnolr"]:
        g = bg.array("g", (3, bg.metadata["ngm"]), "float64")
        admitted &= np.sum(g ** 2, axis=0) > 1e-8
    hartree = np.zeros(total_g.shape, dtype=np.complex128)
    hartree[admitted] = (bg.metadata["e2"] * 4 * np.pi * total_g[admitted] /
                         (bg.metadata["tpiba"] ** 2 * qg2[admitted]))
    return xc + fft.from_g(hartree[:, None])


def apply_spin_pbe_kernel(bundle: QEResponseBundle, delta_n: ArrayLike) -> NDArray[np.complex128]:
    """Return K_q delta_n in Ry on native padded storage (up/down columns).

    G+q=0 is omitted from Hartree with QE's 1e-8 dimensionless threshold, while
    XC at that mode is retained. lrpa/lnolr follow captured native flags; other
    electrostatic, gamma-packed-wavefunction, noncollinear and core variants are out of scope.
    Neither the bundle nor the input is modified.
    """
    return _apply(bundle, delta_n)


def density_potential_pairing(bundle: QEResponseBundle, delta_n: ArrayLike,
                               delta_v: ArrayLike) -> complex:
    """Omega/N sum_r,spin conj(delta_n)*delta_v, excluding storage padding."""
    return NativeRhoFFT.from_bundle(bundle).pair(np.asarray(delta_n), np.asarray(delta_v))


def kernel_sensitivity_actions(bundle: QEResponseBundle, delta_n: ArrayLike) -> dict[str, NDArray[Any]]:
    """Scientific wrong constructions, only exposing where a probe separates them.

    These are oracle mutations, not alternative material-kernel API settings.
    Wrong basis applies the erroneous total/magnetization→up/down conversion to
    response columns which were already up/down. Dropped cross-spin zeroes every
    off-diagonal native coefficient, including mixed-index GGA contractions.
    """
    density = np.asarray(delta_n)
    wrong_basis = np.column_stack(((density[:, 0] + density[:, 1]) / 2,
                                  (density[:, 0] - density[:, 1]) / 2))
    return {
        "wrong_spin_basis": _apply(bundle, wrong_basis),
        "dropped_gga": _apply(bundle, density, gga=False),
        "dropped_cross_spin": _apply(bundle, density, cross_spin=False),
    }
