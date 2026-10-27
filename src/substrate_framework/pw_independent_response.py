"""Isolated full-PW physical response to +v + g*u, with both q branches.

For exp(-i*z*t), the density-matrix equation is
    z*delta_rho - [h0, delta_rho] = [delta_h, rho0].
Expanding the two terms of the right commutator in occupied source columns
produces the plus ket and minus bra below. In particular the second ket uses
conj(z), then its bra is conjugated; neither branch has an extra minus sign.
The returned ionic observable is delta<g_-q>, not force or positive chi to -xB.
No thermal population derivative, screening, or physical damping is added.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .pw_response_data import PWResponseChannel, PWResponseModel, PWResponseValue


def _finite_array(value, shape: tuple[int, ...], name: str) -> NDArray:
    array = np.asarray(value)
    if array.shape != shape or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must be finite with shape {shape}")
    return array


class PWIndependentResponse:
    """Reusable retarded response at one energy z (Ry), strictly Im(z)>0.

    Source occupations already include k quadrature and their explicit spin.
    Full target eigenvectors have PW rows and eigenstate columns. Target FFT
    slots are zero-based storage offsets, independently mapped for each branch.
    Models are treated as immutable for the lifetime of this response object.
    """

    def __init__(self, model: PWResponseModel, z: complex):
        self.model = model
        self.z = complex(z)
        if not np.isfinite(self.z) or self.z.imag <= 0:
            raise ValueError("z must be finite with strictly positive imaginary part")
        fft = model.fft
        if not np.isfinite(fft.omega) or fft.omega <= 0:
            raise ValueError("FFT volume must be finite and positive")
        if len(fft.physical) != 3 or len(fft.storage) != 3 or any(
                p < 1 or s < p for p, s in zip(fft.physical, fft.storage)):
            raise ValueError("FFT physical/storage dimensions are inconsistent")
        if fft.nnr != int(np.prod(fft.storage)):
            raise ValueError("FFT nnr must equal the storage size")
        _finite_array(model.q_cart_2pi_alat, (3,), "q")
        self._maps = tuple(self._validate_channel(channel) for channel in model.channels)

    def _coordinates(self, slots, count: int, name: str) -> tuple[NDArray, ...]:
        slots = np.asarray(slots)
        fft = self.model.fft
        if slots.shape != (count,) or slots.dtype.kind not in "iu":
            raise ValueError(f"{name} must contain {count} integer FFT offsets")
        if np.any(slots < 0) or np.any(slots >= fft.nnr) or np.unique(slots).size != count:
            raise ValueError(f"{name} contains invalid or duplicated FFT offsets")
        coordinates = np.unravel_index(slots, fft.storage, order="F")
        if any(np.any(c >= n) for c, n in zip(coordinates, fft.physical)):
            raise ValueError(f"{name} maps into FFT padding")
        return coordinates

    def _validate_channel(self, channel: PWResponseChannel):
        if channel.spin not in (0, 1):
            raise ValueError("channel spin must be zero-based 0 or 1")
        energies = np.asarray(channel.source_energies)
        if energies.ndim != 1 or energies.dtype.kind not in "fiu":
            raise ValueError("source energies must be a real vector")
        count = energies.size
        _finite_array(energies, (count,), "source energies")
        weights = _finite_array(channel.weighted_occupations, (count,), "occupations")
        if weights.dtype.kind not in "fiu" or np.any(weights < 0):
            raise ValueError("weighted occupations must be real and nonnegative")
        _finite_array(channel.source_grid, (self.model.fft.nnr, count), "source grid")
        maps = []
        for branch in ("plus", "minus"):
            target = np.asarray(getattr(channel, f"{branch}_energies"))
            if target.ndim != 1 or target.dtype.kind not in "fiu":
                raise ValueError(f"{branch} target energies must be a real vector")
            size = target.size
            _finite_array(target, (size,), f"{branch} energies")
            _finite_array(getattr(channel, f"{branch}_vectors"), (size, size),
                          f"{branch} full target eigenvectors")
            _finite_array(getattr(channel, f"g_{branch}"), (6, size, count),
                          f"{branch} ionic operators")
            maps.append(self._coordinates(getattr(channel, f"{branch}_slots"),
                                          size, f"{branch} slots"))
        return tuple(maps)

    def _to_pw(self, grid: NDArray, coordinates: tuple[NDArray, ...]) -> NDArray:
        spectrum = np.fft.fftn(self.model.fft.physical_view(grid),
                               axes=(0, 1, 2), norm="forward")
        return spectrum[coordinates]

    def _to_grid(self, coefficients: NDArray, coordinates: tuple[NDArray, ...]) -> NDArray:
        fft = self.model.fft
        spectrum = np.zeros((*fft.physical, coefficients.shape[1]), dtype=np.complex128)
        spectrum[coordinates] = coefficients
        physical = np.fft.ifftn(spectrum, axes=(0, 1, 2), norm="forward")
        return fft._embed(physical)

    def _ket(self, channel: PWResponseChannel, branch: str, potential: NDArray,
             displacement: NDArray, coordinates: tuple[NDArray, ...]) -> NDArray:
        vectors = getattr(channel, f"{branch}_vectors")
        energies = getattr(channel, f"{branch}_energies")
        drive = np.einsum("atn,a->tn", getattr(channel, f"g_{branch}"), displacement,
                          dtype=np.complex128)
        drive += self._to_pw(potential[:, None] * channel.source_grid, coordinates)
        shift = self.z if branch == "plus" else -self.z.conjugate()
        denominator = channel.source_energies[None, :] + shift - energies[:, None]
        return vectors @ ((vectors.conj().T @ drive) / denominator)

    def apply(self, local_potential, displacement) -> PWResponseValue:
        """Return physical spin density (bohr^-3) and ionic gradient (Ry/bohr).

        Complex amplitudes enter linearly: minus-branch conjugation belongs to
        its ket construction and is undone in the observable bra contraction.
        Padding is not physical volume and contributes no density integral.
        """
        fft = self.model.fft
        potential = _finite_array(local_potential, (fft.nnr, 2), "local potential")
        u = _finite_array(displacement, (6,), "displacement")
        density = np.zeros((fft.nnr, 2), dtype=np.complex128)
        gradient = np.zeros(6, dtype=np.complex128)
        for channel, (plus_map, minus_map) in zip(self.model.channels, self._maps):
            v = potential[:, channel.spin]
            weights = channel.weighted_occupations
            plus = self._ket(channel, "plus", v, u, plus_map)
            density[:, channel.spin] += np.einsum(
                "rn,rn,n->r", channel.source_grid.conj(),
                self._to_grid(plus, plus_map), weights) / fft.omega
            gradient += np.einsum("atn,tn,n->a", channel.g_plus.conj(), plus, weights)
            minus = self._ket(channel, "minus", v.conj(), u.conj(), minus_map)
            density[:, channel.spin] += np.einsum(
                "rn,rn,n->r", self._to_grid(minus, minus_map).conj(),
                channel.source_grid, weights) / fft.omega
            gradient += np.einsum("tn,atn,n->a", minus.conj(), channel.g_minus, weights)
        return PWResponseValue(density, gradient)

    def ionic_matrix(self) -> NDArray[np.complex128]:
        """Six-column physical electronic curvature; no Cfrozen or screening."""
        potential = np.zeros((self.model.fft.nnr, 2), dtype=np.complex128)
        unit = np.eye(6, dtype=np.complex128)
        return np.column_stack([self.apply(potential, u).ionic_gradient for u in unit])
