from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.topological_labels import (
    binary_product_character,
    binary_product_character_kernel,
    binary_product_character_ledger,
    combined_winding_parity,
    cyclic_sign_character,
    cyclic_sign_character_ledger,
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


def test_cyclic_sign_characters_are_classified_by_order_parity() -> None:
    assert cyclic_sign_character_ledger(1).generator_images == (1,)
    assert cyclic_sign_character_ledger(3).generator_images == (1,)
    for order in (2, 4, 6, 8):
        result = cyclic_sign_character_ledger(order)
        assert result.generator_images == (1, -1)
        assert result.nontrivial_exists
        assert result.nontrivial_kernel == tuple(range(0, order, 2))
        assert result.nontrivial_quotient_order == 2
        assert result.nontrivial_faithful == (order == 2)


def test_every_classified_cyclic_character_obeys_the_full_cayley_table() -> None:
    for order in range(1, 11):
        for image in cyclic_sign_character_ledger(order).generator_images:
            for first in range(order):
                for second in range(order):
                    assert cyclic_sign_character(
                        order, first + second, generator_image=image
                    ) == (
                        cyclic_sign_character(order, first, generator_image=image)
                        * cyclic_sign_character(order, second, generator_image=image)
                    )


def test_order_four_is_a_counterexample_to_om1_source_group_uniqueness() -> None:
    result = cyclic_sign_character_ledger(4)
    assert result.nontrivial_kernel == (0, 2)
    assert not result.nontrivial_faithful
    assert cyclic_sign_character(4, 1, generator_image=-1) == -1
    assert cyclic_sign_character(4, 2, generator_image=-1) == 1
    assert all(
        cyclic_sign_character(4, value, generator_image=-1)
        == winding_parity(value)
        for value in range(-8, 9)
    )


def test_odd_order_refuses_a_minus_one_generator_image() -> None:
    with pytest.raises(ValueError, match="cyclic relation"):
        cyclic_sign_character(3, 1, generator_image=-1)


def test_binary_product_has_two_to_rank_distinct_characters() -> None:
    for rank in range(1, 5):
        result = binary_product_character_ledger(rank)
        assert result.character_count == 2**rank
        assert result.nontrivial_character_count == 2**rank - 1
        assert result.faithful_character_exists == (rank == 1)


def test_equal_minus_one_values_do_not_identify_product_characters() -> None:
    first_selector = (1, 0)
    second_selector = (0, 1)
    shared_point = (1, 1)
    assert binary_product_character(shared_point, first_selector) == -1
    assert binary_product_character(shared_point, second_selector) == -1
    assert binary_product_character((1, 0), first_selector) == -1
    assert binary_product_character((1, 0), second_selector) == 1
    assert binary_product_character_kernel(first_selector) == ((0, 0), (0, 1))
    assert binary_product_character_kernel(second_selector) == ((0, 0), (1, 0))


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: cyclic_sign_character_ledger(0), "positive"),
        (lambda: cyclic_sign_character_ledger(sp.Symbol("n", positive=True, integer=True)), "concrete"),
        (lambda: cyclic_sign_character(4, 1, generator_image=sp.I), "generator_image"),
        (lambda: binary_product_character((), ()), "non-empty"),
        (lambda: binary_product_character((0, 1), (1,)), "equal length"),
        (lambda: binary_product_character((0, 2), (1, 0)), "zero or one"),
        (lambda: binary_product_character_ledger(sp.Rational(3, 2)), "integer"),
    ],
)
def test_character_classifiers_reject_invalid_domains(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
