from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.skyrme_relations import (
    conditional_anw_mass,
    conditional_topological_mass,
    matched_pion_coupling_ratio,
)


def test_conditional_mass_matching_cancels_hedgehog_coefficient() -> None:
    coefficient, rest_energy, coupling = sp.symbols(
        "B1 E_e e", positive=True
    )
    pion_scale = coupling * matched_pion_coupling_ratio(rest_energy)
    assert sp.simplify(
        conditional_topological_mass(coefficient, rest_energy)
        - conditional_anw_mass(coefficient, pion_scale, coupling)
    ) == 0


def test_matched_ratio_is_conditional_exact_expression() -> None:
    rest_energy = sp.symbols("E_e", positive=True)
    assert matched_pion_coupling_ratio(rest_energy) == 16 * sp.pi * rest_energy


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: conditional_topological_mass(0, 1), "hedgehog_coefficient"),
        (lambda: conditional_anw_mass(1, -1, 1), "pion_scale"),
        (lambda: matched_pion_coupling_ratio(0), "electron_rest_energy"),
    ],
)
def test_numeric_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
