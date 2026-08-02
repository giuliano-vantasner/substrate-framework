"""Primary exact verifier for P066 sign-character classification and OM1 audit."""

from __future__ import annotations

import hashlib
from itertools import product
from pathlib import Path

import sympy as sp

from substrate_framework.topological_labels import (
    binary_product_character,
    binary_product_character_kernel,
    binary_product_character_ledger,
    cyclic_sign_character,
    cyclic_sign_character_ledger,
    winding_parity,
)
from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-19/"
    "bridge_OM1_single_minus_one_identity.py"
)
SOURCE_SHA256 = "c5af6786d4873675ddb552c4a0ae222e4ee3ab7472b74844b28dc4d257358007"


def main() -> int:
    ledger = CheckLedger("P066")
    ledger.check("hash-pinned OM1 source exists", SOURCE.is_file())
    ledger.check(
        "hash-pinned OM1 source integrity",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    source_text = SOURCE.read_text(encoding="utf-8")
    ledger.check(
        "OM1 collapse is implemented as scalar set equality",
        "one_value = len(set(readings + [chi_g])) == 1" in source_text,
    )
    ledger.check(
        "OM1 copies each pending oracle into its local executable",
        all(
            token in source_text
            for token in (
                "def holonomy(",
                "def wilson_W(",
                "def berry_holonomy(",
                "def fermionParity(",
                "def skyrmionFermionParity(",
            )
        ),
    )
    ledger.check(
        "OM1 Z4 guard selects only the primitive generator image i",
        "z4_gen = sp.simplify(chi_n(4, 1))" in source_text
        and "only_z2_fits" in source_text,
    )

    c2 = cyclic_sign_character_ledger(2)
    ledger.check(
        "C2 has exactly trivial and faithful sign characters",
        c2.generator_images == (1, -1)
        and c2.nontrivial_kernel == (0,)
        and c2.nontrivial_quotient_order == 2
        and c2.nontrivial_faithful,
    )
    for order in range(1, 13):
        result = cyclic_sign_character_ledger(order)
        ledger.check(
            f"order {order} generator images obey the exact parity classification",
            result.generator_images == ((1, -1) if order % 2 == 0 else (1,))
            and result.nontrivial_exists == (order % 2 == 0),
        )
        ledger.check(
            f"order {order} classified maps satisfy the full Cayley table",
            all(
                cyclic_sign_character(
                    order, first + second, generator_image=image
                )
                == cyclic_sign_character(order, first, generator_image=image)
                * cyclic_sign_character(order, second, generator_image=image)
                for image in result.generator_images
                for first in range(order)
                for second in range(order)
            ),
        )

    c4 = cyclic_sign_character_ledger(4)
    ledger.check(
        "C4 nonfaithful sign character passes both OM1 displayed values",
        cyclic_sign_character(4, 1, generator_image=-1) == -1
        and cyclic_sign_character(4, 2, generator_image=-1) == 1
        and c4.nontrivial_kernel == (0, 2)
        and not c4.nontrivial_faithful,
    )
    c6 = cyclic_sign_character_ledger(6)
    ledger.check(
        "every higher even cyclic sign character has an even-residue kernel",
        c6.nontrivial_kernel == (0, 2, 4)
        and cyclic_sign_character(6, 1, generator_image=-1) == -1
        and cyclic_sign_character(6, 2, generator_image=-1) == 1,
    )
    ledger.mutation_sensitive(
        "faithful nontrivial sign character selects source order two",
        lambda order: cyclic_sign_character_ledger(order).nontrivial_faithful,
        2,
        [4, 6, 8],
    )
    odd_rejections = []
    for order in (1, 3, 5, 7):
        try:
            cyclic_sign_character(order, 1, generator_image=-1)
        except ValueError:
            odd_rejections.append(True)
    ledger.check(
        "odd cyclic relations reject a minus-one generator image",
        odd_rejections == [True, True, True, True],
    )
    ledger.check(
        "even cyclic sign quotient agrees with accepted integer winding parity",
        all(
            cyclic_sign_character(order, value, generator_image=-1)
            == winding_parity(value)
            for order in (2, 4, 6, 10)
            for value in range(-12, 13)
        ),
    )

    for rank in range(1, 5):
        result = binary_product_character_ledger(rank)
        selectors = tuple(product((0, 1), repeat=rank))
        points = selectors
        truth_tables = {
            tuple(binary_product_character(point, selector) for point in points)
            for selector in selectors
        }
        ledger.check(
            f"binary rank {rank} has exactly two-to-rank distinct characters",
            result.character_count == 2**rank
            and result.nontrivial_character_count == 2**rank - 1
            and len(truth_tables) == 2**rank,
        )
        ledger.check(
            f"binary rank {rank} dot-product characters obey the full group law",
            all(
                binary_product_character(
                    tuple((left[index] + right[index]) % 2 for index in range(rank)),
                    selector,
                )
                == binary_product_character(left, selector)
                * binary_product_character(right, selector)
                for selector in selectors
                for left in points
                for right in points
            ),
        )

    first_selector = (1, 0)
    second_selector = (0, 1)
    shared_point = (1, 1)
    ledger.check(
        "equal minus-one evaluation does not identify two product characters",
        binary_product_character(shared_point, first_selector) == -1
        and binary_product_character(shared_point, second_selector) == -1
        and binary_product_character((1, 0), first_selector) == -1
        and binary_product_character((1, 0), second_selector) == 1,
    )
    ledger.check(
        "distinct product characters expose distinct kernels",
        binary_product_character_kernel(first_selector) == ((0, 0), (0, 1))
        and binary_product_character_kernel(second_selector) == ((0, 0), (1, 0)),
    )
    ledger.check(
        "nontrivial binary-product characters are nonfaithful above rank one",
        all(
            len(binary_product_character_kernel(selector)) == 2 ** (rank - 1)
            for rank in (2, 3, 4)
            for selector in product((0, 1), repeat=rank)
            if any(selector)
        )
        and all(
            not binary_product_character_ledger(rank).faithful_character_exists
            for rank in (2, 3, 4)
        ),
    )
    ledger.mutation_sensitive(
        "character identity binds the full truth table rather than one value",
        lambda selector: tuple(
            binary_product_character(point, selector)
            for point in ((0, 0), (0, 1), (1, 0), (1, 1))
        )
        == (1, 1, -1, -1),
        first_selector,
        [second_selector, (1, 1), (0, 0)],
    )

    typed_reading_one = ("domain-A", "quotient-A", "representation-A", -1)
    typed_reading_two = ("domain-B", "quotient-B", "representation-B", -1)
    ledger.check(
        "typed readings can share a scalar while retaining distinct source objects",
        typed_reading_one[-1] == typed_reading_two[-1] == -1
        and typed_reading_one != typed_reading_two,
    )
    invalid_guards = []
    for operation in (
        lambda: cyclic_sign_character_ledger(0),
        lambda: cyclic_sign_character(4, 1, generator_image=sp.I),
        lambda: binary_product_character((0, 1), (1,)),
        lambda: binary_product_character((0, 2), (1, 0)),
    ):
        try:
            operation()
        except ValueError:
            invalid_guards.append(True)
    ledger.check(
        "classification refuses malformed groups images and binary coordinates",
        invalid_guards == [True, True, True, True],
    )
    quadrature_aliases = ("np." + "trapz", "np." + "trapezoid")
    canonical_source = Path(
        "src/substrate_framework/topological_labels.py"
    ).read_text(encoding="utf-8")
    ledger.check(
        "P066 finite algebra uses no NumPy quadrature alias",
        all(alias not in canonical_source for alias in quadrature_aliases),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
