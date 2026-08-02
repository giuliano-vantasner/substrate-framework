"""Independent finite P066 review without importing topological_labels."""

from __future__ import annotations

from itertools import product

from substrate_framework.verification import CheckLedger

SIGNS = (1, -1)


def _cyclic_homomorphisms(order: int) -> tuple[tuple[int, ...], ...]:
    maps = []
    for values in product(SIGNS, repeat=order):
        if values[0] != 1:
            continue
        if all(
            values[(left + right) % order] == values[left] * values[right]
            for left in range(order)
            for right in range(order)
        ):
            maps.append(values)
    return tuple(maps)


def _binary_add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a + b) % 2 for a, b in zip(left, right))


def _all_binary_homomorphisms(rank: int) -> tuple[tuple[int, ...], ...]:
    points = tuple(product((0, 1), repeat=rank))
    identity_index = points.index((0,) * rank)
    maps = []
    for values in product(SIGNS, repeat=len(points)):
        if values[identity_index] != 1:
            continue
        table = dict(zip(points, values))
        if all(
            table[_binary_add(left, right)] == table[left] * table[right]
            for left in points
            for right in points
        ):
            maps.append(values)
    return tuple(maps)


def main() -> int:
    ledger = CheckLedger("P066-INDEPENDENT")
    for order in range(1, 9):
        homomorphisms = _cyclic_homomorphisms(order)
        ledger.check(
            f"fresh full-function enumeration classifies C{order} sign maps",
            len(homomorphisms) == (2 if order % 2 == 0 else 1),
        )
        generator_values = {mapping[1 % order] for mapping in homomorphisms}
        ledger.check(
            f"fresh C{order} generator images match the cyclic relation",
            generator_values == ({1, -1} if order % 2 == 0 else {1}),
        )

    c4_maps = _cyclic_homomorphisms(4)
    c4_sign = next(mapping for mapping in c4_maps if mapping[1] == -1)
    ledger.check(
        "fresh enumeration finds OM1's omitted C4 sign quotient",
        c4_sign == (1, -1, 1, -1),
    )
    c4_kernel = tuple(index for index, value in enumerate(c4_sign) if value == 1)
    ledger.check(
        "fresh C4 kernel proves the omitted character is nonfaithful",
        c4_kernel == (0, 2) and len(c4_kernel) > 1,
    )
    c2_sign = next(mapping for mapping in _cyclic_homomorphisms(2) if mapping[1] == -1)
    ledger.check(
        "fresh kernel comparison makes only the C2 sign map faithful",
        tuple(index for index, value in enumerate(c2_sign) if value == 1) == (0,)
        and all(
            len(tuple(index for index, value in enumerate(
                next(mapping for mapping in _cyclic_homomorphisms(order) if mapping[1] == -1)
            ) if value == 1)) > 1
            for order in (4, 6, 8)
        ),
    )

    for rank in (1, 2, 3):
        homomorphisms = _all_binary_homomorphisms(rank)
        ledger.check(
            f"fresh full-function enumeration gives two-to-{rank} binary characters",
            len(homomorphisms) == 2**rank,
        )
    points2 = tuple(product((0, 1), repeat=2))
    maps2 = _all_binary_homomorphisms(2)
    nontrivial = [mapping for mapping in maps2 if mapping != (1, 1, 1, 1)]
    ledger.check(
        "fresh rank-two enumeration has three separate nontrivial characters",
        len(nontrivial) == 3 and len(set(nontrivial)) == 3,
    )
    first = tuple((-1) ** point[0] for point in points2)
    second = tuple((-1) ** point[1] for point in points2)
    shared_index = points2.index((1, 1))
    discriminating_index = points2.index((1, 0))
    ledger.check(
        "fresh truth tables share minus one at one point but are different functions",
        first[shared_index] == second[shared_index] == -1
        and first[discriminating_index] == -1
        and second[discriminating_index] == 1
        and first != second,
    )
    first_kernel = {point for point, value in zip(points2, first) if value == 1}
    second_kernel = {point for point, value in zip(points2, second) if value == 1}
    ledger.check(
        "fresh distinct kernels retain independent binary source factors",
        first_kernel == {(0, 0), (0, 1)}
        and second_kernel == {(0, 0), (1, 0)},
    )

    source_records = (
        ("holonomy-domain", "holonomy-map", -1),
        ("wilson-domain", "wilson-map", -1),
        ("parity-domain", "parity-map", -1),
    )
    ledger.check(
        "fresh typed countermodel preserves equal values and distinct source records",
        len({record[-1] for record in source_records}) == 1
        and len(set(source_records)) == 3,
    )
    ledger.mutation_sensitive(
        "fresh function equality oracle inspects every domain element",
        lambda table: table == first,
        first,
        [second, tuple(1 for _ in points2)],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
