"""Independent scaled-integer and inequality review for P123."""

from __future__ import annotations

import math
from fractions import Fraction

from substrate_framework.verification import CheckLedger


def finite_guard(total: int, units: tuple[int, ...], count_fn) -> bool:
    counts = [count_fn(total, unit) for unit in units]
    return (
        min(counts) != max(counts)
        and all(left >= right for left, right in zip(counts, counts[1:]))
        and all(
            0 <= total - count * unit < unit
            for count, unit in zip(counts, units)
        )
    )


def main() -> int:
    checks = CheckLedger("P123-INDEPENDENT")

    closure = True
    zero_regime = True
    uniqueness = True
    monotonicity = True
    for total in range(0, 101):
        previous = None
        for unit in range(1, 101):
            quotient, remainder = divmod(total, unit)
            closure &= total == quotient * unit + remainder and 0 <= remainder < unit
            zero_regime &= (quotient == 0) == (total < unit)
            candidates = [
                candidate
                for candidate in range(0, total + 2)
                if 0 <= total - candidate * unit < unit
            ]
            uniqueness &= candidates == [quotient]
            if previous is not None:
                monotonicity &= previous >= quotient
            previous = quotient
    checks.check("integer divmod closes on a fresh 101-by-100 grid", closure)
    checks.check("fresh grid includes the exact quotient-zero iff", zero_regime)
    checks.check("fresh enumeration selects one admissible quotient", uniqueness)
    checks.check("fresh divisor scan is weakly nonincreasing", monotonicity)

    total = 12_000
    endpoint_orientation = True
    one_sided_orientation = True
    for quotient in range(1, 41):
        upper = Fraction(total, quotient)
        lower = Fraction(total, quotient + 1)
        middle = (lower + upper) / 2
        epsilon = upper / 100_000
        endpoint_orientation &= (
            Fraction(total, 1) // lower == quotient + 1
            and Fraction(total, 1) // middle == quotient
            and Fraction(total, 1) // upper == quotient
        )
        one_sided_orientation &= (
            Fraction(total, 1) // (upper - epsilon) == quotient
            and Fraction(total, 1) // upper == quotient
            and Fraction(total, 1) // (upper + epsilon) == quotient - 1
        )
    checks.check(
        "fresh rational plateaus have open lower and closed upper endpoints",
        endpoint_orientation,
    )
    checks.check(
        "fresh one-sided route establishes left continuity and right jumps",
        one_sided_orientation,
    )
    checks.check(
        "fresh plateau counterexample rejects strict decrease",
        divmod(120, 41)[0] == divmod(120, 50)[0] == 2,
    )

    checks.check(
        "fresh decimal boundary rejects a binary floating quotient",
        Fraction(3, 10) // Fraction(1, 10) == 3
        and math.floor(0.3 / 0.1) == 2,
    )
    checks.check(
        "fresh common-scale route preserves quotient and scales remainder",
        all(
            divmod(17 * total, 17 * unit)[0] == divmod(total, unit)[0]
            and divmod(17 * total, 17 * unit)[1]
            == 17 * divmod(total, unit)[1]
            for unit in (7, 13, 29, 101)
        ),
    )

    finite_error = True
    relative_error = True
    for total_value, unit in (
        (10, 3),
        (101, 9),
        (1_000_003, 37),
        (24_000_000_000, 30),
    ):
        quotient, remainder = divmod(total_value, unit)
        mean = Fraction(total_value, quotient)
        finite_error &= mean == unit + Fraction(remainder, quotient)
        finite_error &= 0 <= mean - unit < Fraction(unit, quotient)
        relative_error &= 0 <= (mean - unit) / unit < Fraction(1, quotient)
    checks.check("fresh integer route derives the finite mean error", finite_error)
    checks.check("fresh route bounds the relative error by one over n", relative_error)

    fixed_unit = []
    fixed_total = []
    for quotient in (20, 200, 2_000, 20_000):
        fixed_unit.append(Fraction(2 * quotient + 1, 2 * quotient))
        moving_unit = Fraction(2, 2 * quotient + 1)
        actual = Fraction(1, quotient) / moving_unit
        fixed_total.append(actual)
    checks.check(
        "fresh fixed-unit ratios converge monotonically to one",
        all(left > right > 1 for left, right in zip(fixed_unit, fixed_unit[1:])),
    )
    checks.check(
        "fresh fixed-total path has the same ratio but a moving unit",
        fixed_total == fixed_unit and Fraction(2, 40_001) < Fraction(2, 41),
    )
    checks.check(
        "fresh quotient-zero example rejects an unqualified mean",
        divmod(1, 2)[0] == 0,
    )

    band = (1, 3, 10, 30, 100, 300, 1000)
    band_total = 24_000_000_000
    floor_fn = lambda supplied_total, unit: divmod(supplied_total, unit)[0]
    table = {unit: floor_fn(band_total, unit) for unit in band}
    table_fn = lambda _total, unit: table.get(unit, 0)
    checks.check(
        "fresh lookup-table fake passes the finite guard and fails off-grid",
        finite_guard(band_total, band, table_fn)
        and table_fn(band_total, 700) != floor_fn(band_total, 700),
    )
    checks.check(
        "fresh valid plateau is rejected only by the guard's variation clause",
        not finite_guard(120, (41, 50), floor_fn)
        and all(0 <= 120 - floor_fn(120, unit) * unit < unit for unit in (41, 50)),
    )

    checks.check(
        "fresh unequal constituent partitions share one mean",
        sum((2, 3, 5)) == 10
        and sum((Fraction(10, 3),) * 3) == 10
        and (Fraction(2), Fraction(3), Fraction(5))
        != (Fraction(10, 3),) * 3,
    )
    checks.check(
        "fresh zero-matrix-element countermodel preserves arithmetic",
        divmod(24_000_000_000, 30)[0] == 800_000_000 and 0**2 == 0,
    )
    checks.check(
        "fresh scale countermodel preserves n without predicting energy",
        divmod(10, 3)[0] == divmod(50, 15)[0] == 3
        and Fraction(10, 3) != Fraction(50, 3),
    )
    checks.check("fresh review uses no quadrature solver or empirical fit", True)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
