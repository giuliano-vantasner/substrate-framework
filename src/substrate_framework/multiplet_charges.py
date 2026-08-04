"""Exact charge spectra for separately supplied finite product multiplets.

This module expands supplied isospin weights and spectator multiplicities into
grouped and flattened charge ledgers.  It does not derive a representation
table, chirality, anomaly cancellation, generation completeness, a global
gauge group, physical matter, or a Standard Model interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

import sympy as sp

from .charge_traces import (
    AbelianNormalizationLedger,
    FiniteChargeTraceLedger,
    WeightedChargeState,
    abelian_normalization_ledger,
    finite_charge_trace_ledger,
)


@dataclass(frozen=True)
class ChargeMultiplet:
    """One supplied product multiplet in a fixed charge convention.

    ``spectator_multiplicity`` counts equal copies of every listed isospin
    weight, such as a separately supplied color dimension.  The integer does
    not identify the spectator representation or distinguish conjugate
    representations of equal dimension.
    """

    label: str
    spectator_multiplicity: int
    t3_weights: tuple[Any, ...]
    abelian_charge: Any


@dataclass(frozen=True)
class ChargeMultipletSpectrum:
    """Exact component charges and flattened trace states for one multiplet."""

    multiplet: ChargeMultiplet
    electric_charges: tuple[sp.Expr, ...]
    state_count: int
    flattened_states: tuple[WeightedChargeState, ...]


@dataclass(frozen=True)
class FiniteMultipletChargeLedger:
    """Grouped and flattened charge data for a supplied finite table."""

    multiplets: tuple[ChargeMultiplet, ...]
    electric_coefficient: sp.Expr
    spectra: tuple[ChargeMultipletSpectrum, ...]
    state_count: int
    flattened_states: tuple[WeightedChargeState, ...]
    trace_ledger: FiniteChargeTraceLedger


@dataclass(frozen=True)
class ChargeSpectrumInversion:
    """Solve one supplied spectrum for a common Abelian coordinate."""

    t3_weights: tuple[sp.Expr, ...]
    target_charges: tuple[sp.Expr, ...]
    electric_coefficient: sp.Expr
    candidate_abelian_charge: sp.Expr
    reconstruction: tuple[sp.Expr, ...]
    residuals: tuple[sp.Expr, ...]
    consistent: bool


@dataclass(frozen=True)
class MultipletAbelianNormalizationLedger:
    """A multiplet-level Abelian coordinate change and flattened evidence."""

    base: FiniteMultipletChargeLedger
    generator_rescaling: sp.Expr
    rescaled_multiplets: tuple[ChargeMultiplet, ...]
    rescaled_electric_coefficient: sp.Expr
    rescaled_abelian_coupling: sp.Expr
    fixed_coefficient: FiniteMultipletChargeLedger
    covariant: FiniteMultipletChargeLedger
    charge_residuals: tuple[tuple[sp.Expr, ...], ...]
    flattened_normalization: AbelianNormalizationLedger


def _exact_real(value: Any, name: str) -> sp.Expr:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an exact real scalar")
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact rather than floating")
    if expression.is_real is not True:
        raise ValueError(f"{name} must be provably real")
    return sp.simplify(expression)


def _positive_exact(value: Any, name: str) -> sp.Expr:
    expression = _exact_real(value, name)
    if expression.is_positive is not True:
        raise ValueError(f"{name} must be positive")
    return expression


def _positive_integer(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a positive integer")
    expression = sp.sympify(value)
    if (
        expression.is_number is not True
        or expression.is_integer is not True
        or expression.is_positive is not True
    ):
        raise ValueError(f"{name} must be a positive integer")
    return int(expression)


def _normalize_multiplet(multiplet: ChargeMultiplet, index: int) -> ChargeMultiplet:
    if not isinstance(multiplet, ChargeMultiplet):
        raise TypeError("multiplets must contain ChargeMultiplet records")
    if not isinstance(multiplet.label, str) or not multiplet.label.strip():
        raise ValueError("multiplet labels must be non-empty strings")
    weights = tuple(
        _exact_real(value, f"multiplets[{index}].t3_weights[{weight_index}]")
        for weight_index, value in enumerate(multiplet.t3_weights)
    )
    if not weights:
        raise ValueError("each multiplet must contain at least one isospin weight")
    return ChargeMultiplet(
        label=multiplet.label,
        spectator_multiplicity=_positive_integer(
            multiplet.spectator_multiplicity,
            f"multiplets[{index}].spectator_multiplicity",
        ),
        t3_weights=weights,
        abelian_charge=_exact_real(
            multiplet.abelian_charge,
            f"multiplets[{index}].abelian_charge",
        ),
    )


def _normalize_multiplets(
    multiplets: Iterable[ChargeMultiplet],
) -> tuple[ChargeMultiplet, ...]:
    table = tuple(
        _normalize_multiplet(multiplet, index)
        for index, multiplet in enumerate(multiplets)
    )
    if not table:
        raise ValueError("at least one multiplet is required")
    labels = tuple(multiplet.label for multiplet in table)
    if len(set(labels)) != len(labels):
        raise ValueError("multiplet labels must be unique provenance keys")
    return table


def finite_multiplet_charge_ledger(
    multiplets: Iterable[ChargeMultiplet],
    *,
    electric_coefficient: Any = 1,
) -> FiniteMultipletChargeLedger:
    """Expand a supplied finite multiplet table for ``Q=t3+c*y``.

    The output composes :func:`finite_charge_trace_ledger` after retaining the
    multiplet grouping that the flattened accepted API intentionally omits.
    """

    table = _normalize_multiplets(multiplets)
    coefficient = _exact_real(electric_coefficient, "electric_coefficient")
    spectra: list[ChargeMultipletSpectrum] = []
    flattened: list[WeightedChargeState] = []
    for multiplet in table:
        charges = tuple(
            sp.simplify(weight + coefficient * multiplet.abelian_charge)
            for weight in multiplet.t3_weights
        )
        states = tuple(
            WeightedChargeState(
                label=f"{multiplet.label}[{component}]",
                multiplicity=multiplet.spectator_multiplicity,
                t3=weight,
                abelian_charge=multiplet.abelian_charge,
            )
            for component, weight in enumerate(multiplet.t3_weights)
        )
        flattened.extend(states)
        spectra.append(
            ChargeMultipletSpectrum(
                multiplet=multiplet,
                electric_charges=charges,
                state_count=multiplet.spectator_multiplicity * len(charges),
                flattened_states=states,
            )
        )
    flattened_tuple = tuple(flattened)
    return FiniteMultipletChargeLedger(
        multiplets=table,
        electric_coefficient=coefficient,
        spectra=tuple(spectra),
        state_count=sum(spectrum.state_count for spectrum in spectra),
        flattened_states=flattened_tuple,
        trace_ledger=finite_charge_trace_ledger(
            flattened_tuple,
            electric_coefficient=coefficient,
        ),
    )


def infer_common_abelian_charge(
    t3_weights: Sequence[Any],
    target_charges: Sequence[Any],
    *,
    electric_coefficient: Any = 1,
) -> ChargeSpectrumInversion:
    """Invert ``Q=t3+c*y`` for one supplied common multiplet value.

    The coefficient must be exact and provably nonzero.  A single component
    always fixes one candidate.  Additional components test whether the target
    charge separations fit the supplied isospin weights.
    """

    weights = tuple(
        _exact_real(value, f"t3_weights[{index}]")
        for index, value in enumerate(t3_weights)
    )
    targets = tuple(
        _exact_real(value, f"target_charges[{index}]")
        for index, value in enumerate(target_charges)
    )
    if not weights or len(weights) != len(targets):
        raise ValueError("weights and target charges must have equal nonzero length")
    coefficient = _exact_real(electric_coefficient, "electric_coefficient")
    if coefficient.is_zero is not False:
        raise ValueError("electric_coefficient must be provably nonzero")
    candidate = sp.simplify((targets[0] - weights[0]) / coefficient)
    reconstruction = tuple(
        sp.simplify(weight + coefficient * candidate) for weight in weights
    )
    residuals = tuple(
        sp.simplify(reconstructed - target)
        for reconstructed, target in zip(reconstruction, targets, strict=True)
    )
    return ChargeSpectrumInversion(
        t3_weights=weights,
        target_charges=targets,
        electric_coefficient=coefficient,
        candidate_abelian_charge=candidate,
        reconstruction=reconstruction,
        residuals=residuals,
        consistent=all(residual == 0 for residual in residuals),
    )


def charge_conjugate_multiplet(
    multiplet: ChargeMultiplet,
    *,
    label: str,
) -> ChargeMultiplet:
    """Return the exact charge-conjugate weight row under ``Q=t3+c*y``.

    Both the isospin-generator weights and Abelian coordinate change sign.  A
    spectator dimension is retained but is not enough to name its conjugate
    representation; the caller must supply a new provenance label.
    """

    normalized = _normalize_multiplet(multiplet, 0)
    if not isinstance(label, str) or not label.strip():
        raise ValueError("conjugate label must be a non-empty string")
    return ChargeMultiplet(
        label=label,
        spectator_multiplicity=normalized.spectator_multiplicity,
        t3_weights=tuple(sp.simplify(-weight) for weight in normalized.t3_weights),
        abelian_charge=sp.simplify(-normalized.abelian_charge),
    )


def multiplet_abelian_normalization_ledger(
    multiplets: Iterable[ChargeMultiplet],
    generator_rescaling: Any,
    abelian_coupling: Any,
    *,
    electric_coefficient: Any = 1,
) -> MultipletAbelianNormalizationLedger:
    """Map ``y'=rho*y``, ``c'=c/rho``, and ``g'=g/rho`` together."""

    base = finite_multiplet_charge_ledger(
        multiplets,
        electric_coefficient=electric_coefficient,
    )
    rho = _positive_exact(generator_rescaling, "generator_rescaling")
    coupling = _positive_exact(abelian_coupling, "abelian_coupling")
    rescaled_coefficient = sp.simplify(base.electric_coefficient / rho)
    rescaled_multiplets = tuple(
        ChargeMultiplet(
            label=multiplet.label,
            spectator_multiplicity=multiplet.spectator_multiplicity,
            t3_weights=multiplet.t3_weights,
            abelian_charge=sp.simplify(rho * multiplet.abelian_charge),
        )
        for multiplet in base.multiplets
    )
    fixed = finite_multiplet_charge_ledger(
        rescaled_multiplets,
        electric_coefficient=base.electric_coefficient,
    )
    covariant = finite_multiplet_charge_ledger(
        rescaled_multiplets,
        electric_coefficient=rescaled_coefficient,
    )
    charge_residuals = tuple(
        tuple(
            sp.simplify(rescaled - original)
            for original, rescaled in zip(
                base_spectrum.electric_charges,
                covariant_spectrum.electric_charges,
                strict=True,
            )
        )
        for base_spectrum, covariant_spectrum in zip(
            base.spectra, covariant.spectra, strict=True
        )
    )
    flattened = abelian_normalization_ledger(
        base.flattened_states,
        rho,
        coupling,
        electric_coefficient=base.electric_coefficient,
    )
    return MultipletAbelianNormalizationLedger(
        base=base,
        generator_rescaling=rho,
        rescaled_multiplets=rescaled_multiplets,
        rescaled_electric_coefficient=rescaled_coefficient,
        rescaled_abelian_coupling=sp.simplify(coupling / rho),
        fixed_coefficient=fixed,
        covariant=covariant,
        charge_residuals=charge_residuals,
        flattened_normalization=flattened,
    )
