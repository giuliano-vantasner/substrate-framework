"""Analytic coefficient-Hessian exploration for TX4 candidate D.

This append-only attempt differentiates the rational-map integrand by a
second-order real jet.  It does not use TX4's finite differences of integrated
values and does not assign a claim verdict.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Jet2:
    value: np.ndarray
    gradient: np.ndarray
    hessian: np.ndarray

    @staticmethod
    def constant(value: np.ndarray, dimension: int) -> "Jet2":
        array = np.asarray(value, dtype=np.complex128)
        return Jet2(
            array,
            np.zeros((dimension,) + array.shape, dtype=np.complex128),
            np.zeros((dimension, dimension) + array.shape, dtype=np.complex128),
        )

    def __add__(self, other: "Jet2") -> "Jet2":
        return Jet2(
            self.value + other.value,
            self.gradient + other.gradient,
            self.hessian + other.hessian,
        )

    def __neg__(self) -> "Jet2":
        return Jet2(-self.value, -self.gradient, -self.hessian)

    def __sub__(self, other: "Jet2") -> "Jet2":
        return self + (-other)

    def __mul__(self, other: "Jet2") -> "Jet2":
        cross = np.einsum(
            "i...,j...->ij...", self.gradient, other.gradient, optimize=True
        )
        return Jet2(
            self.value * other.value,
            self.gradient * other.value + self.value * other.gradient,
            self.hessian * other.value
            + self.value * other.hessian
            + cross
            + np.swapaxes(cross, 0, 1),
        )

    def reciprocal(self) -> "Jet2":
        outer = np.einsum(
            "i...,j...->ij...", self.gradient, self.gradient, optimize=True
        )
        return Jet2(
            1.0 / self.value,
            -self.gradient / self.value**2,
            2.0 * outer / self.value**3 - self.hessian / self.value**2,
        )

    def __truediv__(self, other: "Jet2") -> "Jet2":
        return self * other.reciprocal()

    def conjugate(self) -> "Jet2":
        return Jet2(
            np.conjugate(self.value),
            np.conjugate(self.gradient),
            np.conjugate(self.hessian),
        )

    def square(self) -> "Jet2":
        return self * self

    def fourth_power(self) -> "Jet2":
        squared = self.square()
        return squared.square()


def parameter(dimension: int, index: int, shape: tuple[int, ...]) -> Jet2:
    gradient = np.zeros((dimension,) + shape, dtype=np.complex128)
    gradient[index] = 1.0
    return Jet2(
        np.zeros(shape, dtype=np.complex128),
        gradient,
        np.zeros((dimension, dimension) + shape, dtype=np.complex128),
    )


def hessian_evidence(n_u: int, n_phi: int, chunk_size: int = 1024):
    u, wu = np.polynomial.legendre.leggauss(n_u)
    phi = (np.arange(n_phi) + 0.5) * 2.0 * np.pi / n_phi
    uu, pp = np.meshgrid(u, phi, indexing="ij")
    weights = np.outer(wu, np.full(n_phi, 2.0 * np.pi / n_phi)).ravel()
    z_all = (
        np.sqrt((1.0 - uu) / (1.0 + uu)) * np.exp(1j * pp)
    ).ravel()
    dimension = 10
    total_value = 0.0j
    total_gradient = np.zeros(dimension, dtype=np.complex128)
    total_hessian = np.zeros((dimension, dimension), dtype=np.complex128)

    for start in range(0, z_all.size, chunk_size):
        z = z_all[start : start + chunk_size]
        weight = weights[start : start + chunk_size]
        shape = z.shape
        p = [parameter(dimension, index, shape) for index in range(dimension)]
        const = lambda value: Jet2.constant(np.asarray(value), dimension)
        one = const(np.ones(shape, dtype=np.complex128))
        z_jet = const(z)
        z2 = z_jet.square()
        a1 = p[0] + p[1] * const(1j * np.ones(shape))
        a0 = p[2] + p[3] * const(1j * np.ones(shape))
        b2 = p[4] + p[5] * const(1j * np.ones(shape))
        b1 = p[6] + p[7] * const(1j * np.ones(shape))
        b0 = one + p[8] + p[9] * const(1j * np.ones(shape))
        numerator = z2 + a1 * z_jet + a0
        denominator = b2 * z2 + b1 * z_jet + b0
        numerator_prime = const(2.0 * z) + a1
        denominator_prime = b2 * const(2.0 * z) + b1
        rational_map = numerator / denominator
        derivative = (
            numerator_prime * denominator - numerator * denominator_prime
        ) / denominator.square()
        norm_map = one + rational_map * rational_map.conjugate()
        norm_derivative = derivative * derivative.conjugate()
        sphere_factor = const((1.0 + np.abs(z) ** 2) ** 4)
        integrand = sphere_factor * norm_derivative.square() / norm_map.fourth_power()
        total_value += np.sum(weight * integrand.value) / (4.0 * np.pi)
        total_gradient += (
            np.sum(integrand.gradient * weight, axis=1) / (4.0 * np.pi)
        )
        total_hessian += (
            np.sum(integrand.hessian * weight, axis=2) / (4.0 * np.pi)
        )

    real_hessian = np.real_if_close(total_hessian, tol=1000).real
    real_hessian = (real_hessian + real_hessian.T) / 2.0
    return (
        float(np.real(total_value)),
        np.real_if_close(total_gradient, tol=1000).real,
        real_hessian,
        np.linalg.eigvalsh(real_hessian),
    )


if __name__ == "__main__":
    for grid in ((24, 48), (32, 64), (48, 96), (64, 128)):
        value, gradient, hessian, eigenvalues = hessian_evidence(*grid)
        print("GRID", grid)
        print("VALUE", repr(value))
        print("GRADIENT_MAX", float(np.max(np.abs(gradient))))
        print("EIGENVALUES", np.array2string(eigenvalues, precision=12))
        print("HESSIAN_MAX", float(np.max(np.abs(hessian))))
