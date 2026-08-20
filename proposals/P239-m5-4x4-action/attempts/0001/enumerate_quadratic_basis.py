"""Exhaust the quadratic Lorentz contractions of the M5 double two-form.

The pinned M5 source defines ``F_abcd`` with only
``F_abcd=-F_bacd=-F_abdc``.  This verifier enumerates every complete metric
pairing of two copies of that tensor and every contraction containing one
Levi-Civita tensor plus two metrics.  It derives the ranks rather than assuming
Riemann pair exchange or a Bianchi identity, both of which are explicitly
broken by source-admissible symmetric derivative matrices.
"""

from __future__ import annotations

import json
from itertools import combinations, permutations, product
from pathlib import Path
import random

import sympy as sp

from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent
ETA_DIAGONAL = (-1, 1, 1, 1)
PAIR_SLOTS = ((0, 1), (2, 3), (4, 5), (6, 7))
FORBIDDEN_SELF_TRACES = {tuple(sorted(pair)) for pair in PAIR_SLOTS}
TWO_FORM_PAIRS = tuple(combinations(range(4), 2))

# Six parity-even basis contractions. A matching pair means contraction by
# eta inverse. Slots 0..3 are the first F and slots 4..7 the second F.
EVEN_BASIS = {
    "I1_norm": ((0, 4), (1, 5), (2, 6), (3, 7)),
    "I2_pair_exchange": ((0, 6), (1, 7), (2, 4), (3, 5)),
    "I3_cross": ((0, 4), (1, 6), (2, 5), (3, 7)),
    "I4_ricci_norm": ((1, 3), (5, 7), (0, 4), (2, 6)),
    "I5_ricci_transpose": ((1, 3), (5, 7), (0, 6), (2, 4)),
    "I6_scalar_squared": ((0, 2), (1, 3), (4, 6), (5, 7)),
}

# Four deterministic pivots spanning every one-epsilon quadratic contraction.
# Each entry is (four epsilon slots, two eta matchings).
ODD_BASIS = {
    "J1_pseudoscalar_times_scalar": (
        (0, 1, 2, 3),
        ((4, 6), (5, 7)),
    ),
    "J2_mixed_trace_left": (
        (0, 1, 2, 4),
        ((3, 6), (5, 7)),
    ),
    "J3_mixed_trace_right": (
        (0, 1, 2, 6),
        ((3, 4), (5, 7)),
    ),
    "J4_pair_pontryagin": (
        (0, 1, 4, 5),
        ((2, 6), (3, 7)),
    ),
}

FORMULAS = {
    "I1_norm": "F_abcd F^abcd",
    "I2_pair_exchange": "F_abcd F^cdab",
    "I3_cross": "F_abcd F^acbd",
    "I4_ricci_norm": "R_ac R^ac, R_ac=F_abc^b",
    "I5_ricci_transpose": "R_ac R^ca, R_ac=F_abc^b",
    "I6_scalar_squared": "R^2, R=R_a^a",
    "J1_pseudoscalar_times_scalar": "epsilon^abcd F_abcd R",
    "J2_mixed_trace_left": "epsilon^abce F_abcd F_efg^f eta^dg",
    "J3_mixed_trace_right": "epsilon^abcg F_abcd F_efgh eta^de eta^fh",
    "J4_pair_pontryagin": "epsilon^abef F_abcd F_ef^cd",
}


def _perfect_matchings(items: tuple[int, ...]):
    if not items:
        yield ()
        return
    first = items[0]
    for position in range(1, len(items)):
        second = items[position]
        remainder = items[1:position] + items[position + 1 :]
        for tail in _perfect_matchings(remainder):
            yield ((first, second),) + tail


def _random_double_two_form(seed: int) -> list[list[list[list[int]]]]:
    rng = random.Random(seed)
    tensor = [
        [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)
    ]
    for a, b in TWO_FORM_PAIRS:
        for c, d in TWO_FORM_PAIRS:
            value = rng.randrange(-7, 8)
            tensor[a][b][c][d] = value
            tensor[b][a][c][d] = -value
            tensor[a][b][d][c] = -value
            tensor[b][a][d][c] = value
    return tensor


def _evaluate_metric_matching(tensor, matching) -> int:
    total = 0
    for values in product(range(4), repeat=4):
        indices = [None] * 8
        weight = 1
        for pair, value in zip(matching, values, strict=True):
            indices[pair[0]] = value
            indices[pair[1]] = value
            weight *= ETA_DIAGONAL[value]
        total += (
            weight
            * tensor[indices[0]][indices[1]][indices[2]][indices[3]]
            * tensor[indices[4]][indices[5]][indices[6]][indices[7]]
        )
    return total


def _permutation_sign(values: tuple[int, ...]) -> int:
    inversions = sum(
        values[left] > values[right]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    return -1 if inversions % 2 else 1


EPSILON_ASSIGNMENTS = tuple(
    (values, _permutation_sign(values)) for values in permutations(range(4))
)


def _evaluate_epsilon_contraction(tensor, expression) -> int:
    epsilon_slots, matching = expression
    total = 0
    for epsilon_values, epsilon_sign in EPSILON_ASSIGNMENTS:
        indices = [None] * 8
        for slot, value in zip(epsilon_slots, epsilon_values, strict=True):
            indices[slot] = value
        for metric_values in product(range(4), repeat=2):
            weight = epsilon_sign
            for pair, value in zip(matching, metric_values, strict=True):
                indices[pair[0]] = value
                indices[pair[1]] = value
                weight *= ETA_DIAGONAL[value]
            total += (
                weight
                * tensor[indices[0]][indices[1]][indices[2]][indices[3]]
                * tensor[indices[4]][indices[5]][indices[6]][indices[7]]
            )
    return total


def _all_even_contractions():
    return tuple(
        matching
        for matching in _perfect_matchings(tuple(range(8)))
        if not any(tuple(sorted(pair)) in FORBIDDEN_SELF_TRACES for pair in matching)
    )


def _all_odd_contractions():
    expressions = []
    for epsilon_slots in combinations(range(8), 4):
        remainder = tuple(slot for slot in range(8) if slot not in epsilon_slots)
        for matching in _perfect_matchings(remainder):
            if any(tuple(sorted(pair)) in FORBIDDEN_SELF_TRACES for pair in matching):
                continue
            expressions.append((epsilon_slots, matching))
    return tuple(expressions)


def _tensor_from_pair_matrix(matrix: sp.Matrix):
    tensor = [
        [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for _ in range(4)
    ]
    for row, (a, b) in enumerate(TWO_FORM_PAIRS):
        for column, (c, d) in enumerate(TWO_FORM_PAIRS):
            value = matrix[row, column]
            tensor[a][b][c][d] = value
            tensor[b][a][c][d] = -value
            tensor[a][b][d][c] = -value
            tensor[b][a][d][c] = value
    return tensor


def _pair_transform(covector_transform: sp.Matrix) -> sp.Matrix:
    transform = sp.zeros(6, 6)
    for new, (a, b) in enumerate(TWO_FORM_PAIRS):
        for old, (p, q) in enumerate(TWO_FORM_PAIRS):
            transform[new, old] = sp.expand(
                covector_transform[p, a] * covector_transform[q, b]
                - covector_transform[q, a] * covector_transform[p, b]
            )
    return transform


def _transform_tensor(tensor, transformation: sp.Matrix):
    pair_matrix = sp.Matrix(
        6,
        6,
        lambda row, column: tensor[TWO_FORM_PAIRS[row][0]][TWO_FORM_PAIRS[row][1]][
            TWO_FORM_PAIRS[column][0]
        ][TWO_FORM_PAIRS[column][1]],
    )
    covector_transform = transformation.inv()
    pair_transform = _pair_transform(covector_transform)
    return _tensor_from_pair_matrix(pair_transform * pair_matrix * pair_transform.T)


def _source_curvature(seed: int = 239):
    rng = random.Random(seed)
    eta = sp.diag(*ETA_DIAGONAL)
    derivatives = []
    for _ in range(4):
        raw = sp.Matrix(4, 4, [rng.randrange(-5, 6) for _ in range(16)])
        derivatives.append(raw + raw.T)
    tensor = [
        [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for _ in range(4)
    ]
    for mu in range(4):
        for nu in range(4):
            curvature = (
                derivatives[mu] * eta * derivatives[nu]
                - derivatives[nu] * eta * derivatives[mu]
            )
            for a in range(4):
                for b in range(4):
                    tensor[mu][nu][a][b] = sp.expand(curvature[a, b])
    return tensor


def _embedded_spatial_sample(seed: int):
    rng = random.Random(seed)
    matrix = sp.zeros(6, 6)
    for row in (3, 4, 5):
        for column in (3, 4, 5):
            matrix[row, column] = rng.randrange(-7, 8)
    return _tensor_from_pair_matrix(matrix)


def _source_clock_witness():
    """One symmetric-derivative negative mode sufficient for the no-go.

    ``D_0=omega diag(1,0,0,0)`` and
    ``D_1=E_01+E_10`` are legitimate derivatives of a real symmetric M5
    field at a point. Their curvature has one spacetime and one internal
    time-space pair. The source action ``-I1`` is negative on this mode.
    """

    omega = sp.symbols("omega", real=True)
    eta = sp.diag(*ETA_DIAGONAL)
    derivatives = [sp.diag(omega, 0, 0, 0), sp.zeros(4), sp.zeros(4), sp.zeros(4)]
    derivatives[1][0, 1] = derivatives[1][1, 0] = 1
    tensor = [
        [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for _ in range(4)
    ]
    for mu, nu in product(range(4), repeat=2):
        value = (
            derivatives[mu] * eta * derivatives[nu]
            - derivatives[nu] * eta * derivatives[mu]
        )
        for internal_a, internal_b in product(range(4), repeat=2):
            tensor[mu][nu][internal_a][internal_b] = sp.expand(
                value[internal_a, internal_b]
            )
    return omega, tensor


def _source_symmetry_evidence(tensor):
    spacetime_antisymmetry = all(
        tensor[a][b][c][d] == -tensor[b][a][c][d]
        for a, b, c, d in product(range(4), repeat=4)
    )
    internal_antisymmetry = all(
        tensor[a][b][c][d] == -tensor[a][b][d][c]
        for a, b, c, d in product(range(4), repeat=4)
    )
    pair_exchange_residuals = [
        sp.expand(tensor[a][b][c][d] - tensor[c][d][a][b])
        for a, b, c, d in product(range(4), repeat=4)
    ]
    bianchi_residuals = [
        sp.expand(tensor[a][b][c][d] + tensor[b][c][a][d] + tensor[c][a][b][d])
        for a, b, c, d in product(range(4), repeat=4)
    ]
    return {
        "spacetime_antisymmetry": spacetime_antisymmetry,
        "internal_antisymmetry": internal_antisymmetry,
        "pair_exchange_counterexample": any(
            value != 0 for value in pair_exchange_residuals
        ),
        "bianchi_counterexample": any(value != 0 for value in bianchi_residuals),
        "pair_exchange_max_abs": max(
            abs(int(value)) for value in pair_exchange_residuals
        ),
        "bianchi_max_abs": max(abs(int(value)) for value in bianchi_residuals),
    }


def main():
    ledger = CheckLedger("P239/quadratic-invariant-basis")
    samples = tuple(_random_double_two_form(seed) for seed in range(20))
    even_contractions = _all_even_contractions()
    odd_contractions = _all_odd_contractions()

    even_matrix = sp.Matrix(
        [
            [
                _evaluate_metric_matching(sample, contraction)
                for contraction in even_contractions
            ]
            for sample in samples
        ]
    )
    even_basis_matrix = sp.Matrix(
        [
            [
                _evaluate_metric_matching(sample, contraction)
                for contraction in EVEN_BASIS.values()
            ]
            for sample in samples
        ]
    )
    odd_matrix = sp.Matrix(
        [
            [
                _evaluate_epsilon_contraction(sample, contraction)
                for contraction in odd_contractions
            ]
            for sample in samples
        ]
    )
    odd_basis_matrix = sp.Matrix(
        [
            [
                _evaluate_epsilon_contraction(sample, contraction)
                for contraction in ODD_BASIS.values()
            ]
            for sample in samples
        ]
    )

    ledger.check(
        "60 nonzero eta-pairing diagrams enumerated", len(even_contractions) == 60
    )
    ledger.check("eta-only quadratic space has rank six", even_matrix.rank() == 6)
    ledger.check("named even basis has rank six", even_basis_matrix.rank() == 6)
    ledger.check(
        "named even basis spans every eta pairing",
        sp.Matrix.hstack(even_basis_matrix, even_matrix).rank() == 6,
    )
    ledger.check("156 one-epsilon diagrams enumerated", len(odd_contractions) == 156)
    ledger.check("one-epsilon quadratic space has rank four", odd_matrix.rank() == 4)
    ledger.check("named odd basis has rank four", odd_basis_matrix.rank() == 4)
    ledger.check(
        "named odd basis spans every one-epsilon contraction",
        sp.Matrix.hstack(odd_basis_matrix, odd_matrix).rank() == 4,
    )
    ledger.check(
        "parity-even and parity-odd sectors give ten independent invariants",
        sp.Matrix.hstack(even_basis_matrix, odd_basis_matrix).rank() == 10,
    )

    source_evidence = _source_symmetry_evidence(_source_curvature())
    for name in (
        "spacetime_antisymmetry",
        "internal_antisymmetry",
        "pair_exchange_counterexample",
        "bianchi_counterexample",
    ):
        ledger.check(f"source {name.replace('_', ' ')}", source_evidence[name])

    rational_boost = sp.eye(4)
    rational_boost[0, 0] = rational_boost[1, 1] = sp.Rational(5, 3)
    rational_boost[0, 1] = rational_boost[1, 0] = sp.Rational(4, 3)
    rational_rotation = sp.eye(4)
    rational_rotation[2, 2] = rational_rotation[3, 3] = sp.Rational(3, 5)
    rational_rotation[2, 3] = -sp.Rational(4, 5)
    rational_rotation[3, 2] = sp.Rational(4, 5)
    proper_lorentz = rational_boost * rational_rotation
    eta = sp.diag(*ETA_DIAGONAL)
    ledger.check(
        "proper rational Lorentz map preserves eta",
        sp.simplify(proper_lorentz.T * eta * proper_lorentz - eta) == sp.zeros(4),
    )
    exact_sample = _tensor_from_pair_matrix(
        sp.Matrix(
            6, 6, lambda row, column: (7 * row - 3 * column + row * column) % 11 - 5
        )
    )
    transformed = _transform_tensor(exact_sample, proper_lorentz)
    for name, contraction in EVEN_BASIS.items():
        ledger.check(
            f"{name} exact proper-Lorentz invariance",
            sp.simplify(
                _evaluate_metric_matching(transformed, contraction)
                - _evaluate_metric_matching(exact_sample, contraction)
            )
            == 0,
        )
    for name, contraction in ODD_BASIS.items():
        ledger.check(
            f"{name} exact proper-Lorentz invariance",
            sp.simplify(
                _evaluate_epsilon_contraction(transformed, contraction)
                - _evaluate_epsilon_contraction(exact_sample, contraction)
            )
            == 0,
        )

    parity = sp.diag(1, -1, 1, 1)
    parity_transformed = _transform_tensor(exact_sample, parity)
    for name, contraction in EVEN_BASIS.items():
        ledger.check(
            f"{name} parity even",
            sp.simplify(
                _evaluate_metric_matching(parity_transformed, contraction)
                - _evaluate_metric_matching(exact_sample, contraction)
            )
            == 0,
        )
    for name, contraction in ODD_BASIS.items():
        ledger.check(
            f"{name} parity odd",
            sp.simplify(
                _evaluate_epsilon_contraction(parity_transformed, contraction)
                + _evaluate_epsilon_contraction(exact_sample, contraction)
            )
            == 0,
        )

    spatial_samples = tuple(_embedded_spatial_sample(seed) for seed in range(12))
    spatial_basis_matrix = sp.Matrix(
        [
            [
                _evaluate_metric_matching(sample, contraction)
                for contraction in EVEN_BASIS.values()
            ]
            for sample in spatial_samples
        ]
    )
    expected_spatial_nullspace = sp.Matrix.hstack(
        sp.Matrix([sp.Rational(-1, 4), sp.Rational(-1, 4), 1, 0, 0, 0]),
        sp.Matrix([sp.Rational(1, 4), sp.Rational(-1, 4), 0, -1, 1, 0]),
        sp.Matrix([1, 0, 0, -4, 0, 1]),
    )
    ledger.check(
        "purely spatial even basis has rank three", spatial_basis_matrix.rank() == 3
    )
    ledger.check(
        "three displayed 3x3-preserving combinations are null",
        spatial_basis_matrix * expected_spatial_nullspace == sp.zeros(12, 3),
    )
    ledger.check(
        "displayed combinations span the complete spatial nullspace",
        expected_spatial_nullspace.rank() == 3,
    )

    omega, clock_witness = _source_clock_witness()
    clock_vector = sp.Matrix(
        [
            _evaluate_metric_matching(clock_witness, contraction)
            for contraction in EVEN_BASIS.values()
        ]
    )
    ledger.check(
        "clock witness comes from symmetric field derivatives",
        all(
            clock_witness[mu][nu][internal_a][internal_b]
            == -clock_witness[nu][mu][internal_a][internal_b]
            == clock_witness[nu][mu][internal_b][internal_a]
            for mu, nu, internal_a, internal_b in product(range(4), repeat=4)
        ),
    )
    ledger.check(
        "clock witness invariant vector derived exactly",
        clock_vector == omega**2 * sp.Matrix([4, 4, 2, 2, 2, 4]),
    )
    ledger.check(
        "every exact-3x3-preserving quadratic deformation vanishes on the clock witness",
        (clock_vector.T * expected_spatial_nullspace) == sp.zeros(1, 3),
    )
    ledger.check(
        "baseline action has a negative clock coefficient",
        sp.expand(-clock_vector[0]).coeff(omega, 2) < 0,
    )

    result = {
        "campaign": "P239",
        "attempt": "0001",
        "source_symmetries": source_evidence,
        "metric_pairing_diagrams": len(even_contractions),
        "parity_even_rank": even_matrix.rank(),
        "epsilon_metric_diagrams": len(odd_contractions),
        "parity_odd_rank": odd_matrix.rank(),
        "total_quadratic_rank": sp.Matrix.hstack(
            even_basis_matrix, odd_basis_matrix
        ).rank(),
        "parity_even_basis": {name: FORMULAS[name] for name in EVEN_BASIS},
        "parity_odd_basis": {name: FORMULAS[name] for name in ODD_BASIS},
        "spatial_even_rank": spatial_basis_matrix.rank(),
        "spatial_nullspace": {
            "N1": "I3-(I1+I2)/4",
            "N2": "(I1-I2)/4-I4+I5",
            "N3": "I1-4*I4+I6",
        },
        "source_clock_witness": {
            "derivatives": "D0=omega*diag(1,0,0,0), D1=E01+E10, D2=D3=0",
            "even_invariant_vector": "omega^2*(4,4,2,2,2,4)",
            "N1_N2_N3": "(0,0,0)",
            "baseline_action_coefficient": "-4",
        },
        "scope": (
            "Complete quadratic basis for a four-dimensional double two-form "
            "with only within-pair antisymmetry. The parity-even issue-147 "
            "candidate family has six coefficients before reductions; its "
            "complete 3x3-preserving subspace is blind to an explicit negative "
            "clock mode built from symmetric field derivatives. Four additional "
            "proper-Lorentz pseudoscalars are classified but not selected."
        ),
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
