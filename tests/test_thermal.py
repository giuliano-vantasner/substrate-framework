from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.thermal import (
    symmetric_two_level_gate,
    two_level_occupation_variance,
    two_level_upper_occupation,
)


def test_exact_two_level_values() -> None:
    splitting = sp.log(3)
    assert two_level_upper_occupation(splitting) == sp.Rational(1, 4)
    assert two_level_occupation_variance(splitting) == sp.Rational(3, 16)
    assert symmetric_two_level_gate(splitting) == sp.Rational(3, 8)


def test_gate_has_exact_hyperbolic_form() -> None:
    x = sp.symbols("x", real=True)
    assert sp.simplify(
        (
            symmetric_two_level_gate(x)
            - sp.sech(x / 2) ** 2 / 2
        ).rewrite(sp.exp)
    ) == 0


def test_complex_splitting_is_rejected() -> None:
    with pytest.raises(ValueError, match="real and dimensionless"):
        symmetric_two_level_gate(sp.I)
