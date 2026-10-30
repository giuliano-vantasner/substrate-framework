"""Fixed-D coherent q/-q frame derivatives and borrowed low-rank densities.

All frames retain every PW row and their ORIGINAL source column rank.  The
mixed coefficient is d²/(dλ dη), not half of it.  On the physical slice η=λ*,
the bra λ derivative is the dagger of the ket η derivative (and conversely).
These are coherent mean variations, NOT population-inclusive quantum noise.

The caller supplies genuine Hamiltonian actions at the current moving stage,
including the nonstationary reference.  This module neither evolves the mean
for the caller nor constructs/replaces any Hamiltonian or self-consistent
mixed potential.  Arrays in density descriptors are borrowed: keep them alive
and unchanged while consuming descriptors.  No PW-squared density, inverse,
rank compression, frame copy, or Hermiticity repair is performed here.
"""
from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np

Action = Callable[[int, np.ndarray], np.ndarray]
Frames = Sequence[np.ndarray]


def _permutations(count, target_plus, target_minus):
    targets = tuple(tuple(p) for p in (target_plus, target_minus))
    for p in targets:
        if (len(p) != count or any(not isinstance(j, (int, np.integer))
                                  or isinstance(j, (bool, np.bool_)) for j in p)
                or sorted(p) != list(range(count))):
            raise ValueError("targets must be explicit endpoint permutations")
    p, m = targets
    if any(m[p[i]] != i or p[m[i]] != i for i in range(count)):
        raise ValueError("q and -q target permutations must be inverses")
    return p, m


def _layout(psi, plus, minus, mixed, target_plus, target_minus):
    count = len(psi)
    if not count or any(len(x) != count for x in (plus, minus, mixed)):
        raise ValueError("complete nonempty mean/plus/minus/mixed tuples required")
    p, m = _permutations(count, target_plus, target_minus)
    for i, frame in enumerate(psi):
        if not isinstance(frame, np.ndarray) or frame.ndim != 2 or min(frame.shape) < 1:
            raise ValueError("mean frames must be full-row two-dimensional arrays")
    for i, frame in enumerate(psi):
        rank = frame.shape[1]
        for name, value, shape in (
                ("plus", plus[i], (psi[p[i]].shape[0], rank)),
                ("minus", minus[i], (psi[m[i]].shape[0], rank)),
                ("mixed", mixed[i], frame.shape)):
            if not isinstance(value, np.ndarray) or value.shape != shape:
                raise ValueError(f"{name}[{i}] must have original-source shape {shape}")
    return p, m


def _action(action, index, vectors, expected):
    result = action(index, vectors)
    if not isinstance(result, np.ndarray) or result.shape != expected:
        raise ValueError(f"Hamiltonian action at endpoint {index} must return {expected}")
    return result


def _rhs_at(i, psi, plus, minus, mixed, p, m, h0, hplus, hminus, hmixed):
    return (
        -1j * (_action(h0, p[i], plus[i], plus[i].shape)
               + _action(hplus, i, psi[i], plus[i].shape)),
        -1j * (_action(h0, m[i], minus[i], minus[i].shape)
               + _action(hminus, i, psi[i], minus[i].shape)),
        -1j * (_action(h0, i, mixed[i], mixed[i].shape)
               + _action(hplus, m[i], minus[i], mixed[i].shape)
               + _action(hminus, p[i], plus[i], mixed[i].shape)
               + _action(hmixed, i, psi[i], mixed[i].shape)))


def frame_rhs_at(index, psi, plus, minus, mixed, *, target_plus, target_minus,
                 h0: Action, hplus: Action, hminus: Action, hmixed: Action):
    """Evaluate one endpoint without allocating other endpoints' RHS arrays."""
    p, m = _layout(psi, plus, minus, mixed, target_plus, target_minus)
    if (not isinstance(index, (int, np.integer)) or isinstance(index, (bool, np.bool_))
            or not 0 <= index < len(psi)):
        raise ValueError("an explicit in-range endpoint index is required")
    if not all(callable(h) for h in (h0, hplus, hminus, hmixed)):
        raise TypeError("all four physical Hamiltonian callbacks are required")
    return _rhs_at(index, psi, plus, minus, mixed, p, m, h0, hplus, hminus, hmixed)


def frame_rhs(psi, plus, minus, mixed, *, target_plus, target_minus,
              h0: Action, hplus: Action, hminus: Action, hmixed: Action):
    """Return (plus_rhs, minus_rhs, mixed_rhs), each an endpoint tuple.

    psi[i],mixed[i] have shape (Npw_i,r_i); plus[i] has
    (Npw_target_plus[i],r_i), minus[i] has (Npw_target_minus[i],r_i).
    h0(i,V),hmixed(i,V) preserve endpoint i; hplus/hminus map i to
    the specified target.  Every callback must accept arbitrary column counts,
    not just the endpoint's native rank.  No callback may mutate its input.
    h0 is the actual reference action, not a stationary energy eigenvalue.
    The reference RHS itself is -1j*h0(i,psi[i]) and remains caller-owned.
    """
    p, m = _layout(psi, plus, minus, mixed, target_plus, target_minus)
    if not all(callable(h) for h in (h0, hplus, hminus, hmixed)):
        raise TypeError("all four physical Hamiltonian callbacks are required")
    rows = tuple(_rhs_at(i, psi, plus, minus, mixed, p, m, h0, hplus, hminus, hmixed)
                 for i in range(len(psi)))
    return tuple(tuple(row[j] for row in rows) for j in range(3))


@dataclass(frozen=True, slots=True)
class DensityDyad:
    """Borrowed contribution weight * left @ D @ right.conj().T.

    source_index identifies the original occupied-column source of ALL three
    factors and its quadrature weight, even after the columns have moved.
    No multiplication is performed on construction.
    """
    left: np.ndarray
    D: np.ndarray
    right: np.ndarray
    source_index: int
    weight: float


@dataclass(frozen=True, slots=True)
class DensityBlock:
    """Sum of dyads in the (target_endpoint, source_endpoint) PW block."""
    target_endpoint: int
    source_endpoint: int
    dyads: tuple[DensityDyad, ...]


def density_dyads(psi, plus, minus, mixed, D, *, target_plus, target_minus,
                  source_weights):
    """Return mean/plus/minus/mixed tuples of copy-free DensityBlock records.

    D[i] is the original fixed complex Hermitian (possibly singular) r_i×r_i
    matrix; source_weights[i] is its explicit positive quadrature weight.
    Weights are NOT averaged across endpoints or absorbed into another D.
    Descriptors retain input array identity.  Consumers contract each dyad
    with their real physical density/moment provider; a dense materialization
    is deliberately absent.  The two mixed cross terms are ket-plus ×
    bra-minus and ket-minus × bra-plus: the swapped bra convention makes
    these plus D plus† and minus D minus† at the appropriate incoming sources.
    """
    p, m = _layout(psi, plus, minus, mixed, target_plus, target_minus)
    count = len(psi)
    if len(D) != count or len(source_weights) != count:
        raise ValueError("one original D and explicit weight per source required")
    for i, (d, weight) in enumerate(zip(D, source_weights)):
        rank = psi[i].shape[1]
        if not isinstance(d, np.ndarray) or d.shape != (rank, rank):
            raise ValueError(f"D[{i}] must retain original rank {rank}")
        if not np.all(np.isfinite(d)) or not np.allclose(d, d.conj().T, atol=1e-12, rtol=1e-12):
            raise ValueError("finite Hermitian fixed D required; no repair is made")
        if not np.isscalar(weight) or not np.isreal(weight) or not np.isfinite(weight) or weight <= 0:
            raise ValueError("explicit finite positive real source weights required")

    def dyad(left, right, source):
        return DensityDyad(left, D[source], right, source, float(source_weights[source]))

    mean_blocks, plus_blocks, minus_blocks, mixed_blocks = [], [], [], []
    for i in range(count):
        mean_blocks.append(DensityBlock(i, i, (dyad(psi[i], psi[i], i),)))
        plus_blocks.append(DensityBlock(p[i], i, (
            dyad(plus[i], psi[i], i), dyad(psi[p[i]], minus[p[i]], p[i]))))
        minus_blocks.append(DensityBlock(m[i], i, (
            dyad(minus[i], psi[i], i), dyad(psi[m[i]], plus[m[i]], m[i]))))
        mixed_blocks.append(DensityBlock(i, i, (
            dyad(mixed[i], psi[i], i), dyad(psi[i], mixed[i], i),
            dyad(plus[m[i]], plus[m[i]], m[i]),
            dyad(minus[p[i]], minus[p[i]], p[i]))))
    return {"mean": tuple(mean_blocks), "plus": tuple(plus_blocks),
            "minus": tuple(minus_blocks), "mixed": tuple(mixed_blocks)}
