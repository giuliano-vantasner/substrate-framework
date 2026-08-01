from __future__ import annotations

import pytest

from substrate_framework.topological_labels import (
    combined_winding_parity,
    winding_parity,
)


def test_winding_parity_is_a_homomorphism_on_integer_grid() -> None:
    for first in range(-12, 13):
        for second in range(-12, 13):
            assert winding_parity(first + second) == (
                winding_parity(first) * winding_parity(second)
            )


def test_even_and_odd_winding_classes_are_discriminated() -> None:
    assert all(winding_parity(value) == 1 for value in (-4, -2, 0, 2, 4))
    assert all(winding_parity(value) == -1 for value in (-3, -1, 1, 3))


def test_even_dressing_preserves_and_odd_dressing_flips_parity() -> None:
    assert combined_winding_parity(1, 0) == winding_parity(1)
    assert combined_winding_parity(1, 2) == winding_parity(1)
    assert combined_winding_parity(1, 1) == -winding_parity(1)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: winding_parity(0.5), "winding"),
        (lambda: combined_winding_parity(1.5, 0), "anchor_winding"),
        (lambda: combined_winding_parity(1, 0.25), "dressing_winding"),
    ],
)
def test_winding_labels_reject_nonintegers(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
