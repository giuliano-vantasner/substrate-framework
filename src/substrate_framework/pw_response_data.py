"""Settled data interface for full-PW isolated two-branch electronic response.

Energies and z are Ry; g is +partial h/partial u (Ry/bohr). Source grids
contain unnormalised periodic PW sums, so physical density uses 1/omega.
Weights already contain the k quadrature and one explicit spin occupation.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import numpy as np
from numpy.typing import NDArray
from .qe_response_fft import NativeRhoFFT

@dataclass(frozen=True)
class PWResponseChannel:
    identity: str
    spin: int  # zero-based up/down column; no additional spin factor
    source_energies: NDArray[Any]  # every numerically nonzero-FD source
    weighted_occupations: NDArray[Any]
    source_grid: NDArray[Any]  # (nnr,nactive), unnormalised periodic sums
    plus_energies: NDArray[Any]  # complete target PW spectrum
    plus_vectors: NDArray[Any]
    plus_slots: NDArray[Any]  # zero-based Native FFT storage slots
    minus_energies: NDArray[Any]
    minus_vectors: NDArray[Any]
    minus_slots: NDArray[Any]
    g_plus: NDArray[Any]  # (6,ntarget_plus,nactive)
    g_minus: NDArray[Any]  # (6,ntarget_minus,nactive), actual reverse sector

@dataclass(frozen=True)
class PWResponseModel:
    fft: NativeRhoFFT
    q_cart_2pi_alat: NDArray[Any]
    channels: tuple[PWResponseChannel, ...]
    metadata: dict[str, Any]

@dataclass(frozen=True)
class PWResponseValue:
    density: NDArray[np.complex128]  # physical up/down density, bohr^-3
    ionic_gradient: NDArray[np.complex128]  # delta<g_-q>, NOT its negative force
