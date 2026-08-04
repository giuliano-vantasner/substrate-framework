"""Independent P131 review without importing its primary verifier or character API."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from itertools import product
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


CAMPAIGN = Path("campaigns/P131-t1z2-cross-oracle-sign-audit")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-1/"
    "bridge_T1Z2_same_minus_one.py"
)
SOURCE_SHA = "d9c08f9440fb79b9ef445ad77aff113db6c7c7f8943c5838180fb5704fd71bed"
FREEZE_SHA = "ab10fe25cab238261beceea1304c2faad44b426b31fb03bc3be5def752f167bb"
RUNG21 = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
    "rung021_spin_statistics_lock.py"
)
RUNG21_SHA = "6094d46bb9119dfc58ed3d7c1a5797c4524e11756068ab298e97b5119e8f7869"


def all_sign_homomorphisms(order: int) -> tuple[tuple[int, ...], ...]:
    tables = []
    for values in product((1, -1), repeat=order):
        if values[0] != 1:
            continue
        if all(values[(a + b) % order] == values[a] * values[b] for a in range(order) for b in range(order)):
            tables.append(values)
    return tuple(tables)


def binary_character(point: tuple[int, ...], selector: tuple[int, ...]) -> int:
    return -1 if sum(a * b for a, b in zip(point, selector, strict=True)) % 2 else 1


@dataclass(frozen=True)
class NamedGroup:
    name: str
    elements: tuple[int, ...]


def main() -> int:
    checks = CheckLedger("T1Z2-INDEPENDENT-CHARACTER-IDENTITY-REVIEW")
    payload = SOURCE.read_bytes()
    text = payload.decode("utf-8")
    tree = ast.parse(text)

    checks.check(
        "fresh source read is hash pinned",
        hashlib.sha256(payload).hexdigest() == SOURCE_SHA,
    )
    checks.check(
        "fresh preregistration read is hash pinned",
        hashlib.sha256((CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA,
    )
    checks.check(
        "fresh cited-rung read is hash pinned",
        hashlib.sha256(RUNG21.read_bytes()).hexdigest() == RUNG21_SHA,
    )
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check("fresh AST finds ten predicates", len(calls) == 10)
    checks.check(
        "fresh AST finds no executable OM1 or S2 dependency",
        {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        == {"sympy"},
    )

    enumerated = {order: all_sign_homomorphisms(order) for order in range(1, 9)}
    checks.check(
        "fresh Cayley-table enumeration finds the exact cyclic classification",
        all(len(enumerated[n]) == (1 if n % 2 else 2) for n in range(1, 9)),
    )
    checks.check(
        "fresh C4 enumeration reproduces selected signs with a nontrivial kernel",
        (1, -1, 1, -1) in enumerated[4]
        and tuple(index for index, value in enumerate((1, -1, 1, -1)) if value == 1)
        == (0, 2),
    )
    first = tuple(binary_character(point, (1, 0)) for point in product((0, 1), repeat=2))
    second = tuple(binary_character(point, (0, 1)) for point in product((0, 1), repeat=2))
    checks.check(
        "fresh binary-product enumeration gives distinct maps sharing minus one",
        first != second
        and binary_character((1, 1), (1, 0)) == -1
        and binary_character((1, 1), (0, 1)) == -1,
    )

    linking_group = NamedGroup("integer linking quotient", (0, 1))
    charge_group = NamedGroup("integer charge quotient", (0, 1))
    checks.check(
        "isomorphic named C2 domains are not literally one typed object",
        linking_group != charge_group
        and linking_group.elements == charge_group.elements,
    )
    q_link = lambda link: link % 2
    q_charge = lambda charge: abs(charge) % 2
    sign = lambda residue: -1 if residue else 1
    checks.check(
        "separate quotient pullbacks reproduce the same parity table without identifying sources",
        all(sign(q_link(n)) == sign(q_charge(n)) for n in range(-10, 11))
        and q_link is not q_charge,
    )
    checks.check(
        "point equality is weaker than full-map equality",
        first[3] == second[3] == -1 and first[1] != second[1],
    )

    half_holonomy = lambda links: sp.simplify(sp.exp(sp.pi * sp.I * links))
    checks.check(
        "fresh half-holonomy derivation gives the accepted integer parity sequence",
        tuple(half_holonomy(k) for k in range(5)) == (1, -1, 1, -1, 1),
    )
    checks.check(
        "fresh non-half strength counterexample leaves the sign codomain",
        sp.simplify(sp.exp(2 * sp.pi * sp.I / 3)) not in (sp.Integer(-1), sp.Integer(1)),
    )

    two_dimensional = -sp.eye(2)
    four_dimensional = -sp.eye(4)
    checks.check(
        "equal central minus-one entries do not make representations equivalent",
        two_dimensional[0, 0] == four_dimensional[0, 0] == -1
        and two_dimensional.shape != four_dimensional.shape,
    )
    checks.check(
        "the cited deck construction is the same string-conditioned assignment",
        'return -I2 if host == "RP2" else I2' in text
        and 'return -I2 if host == "RP2" else I2' in RUNG21.read_text(),
    )
    deck = lambda host: -sp.eye(2) if host == "RP2" else sp.eye(2)
    checks.check(
        "fresh host-label mutations expose the deck assignment's lack of topology",
        deck("RP2") == -sp.eye(2)
        and deck("RP^2") == sp.eye(2)
        and deck("not-a-space") == sp.eye(2),
    )
    checks.check(
        "fresh SU2 rotation arithmetic does not derive the independent deck map",
        sp.simplify(sp.diag(sp.exp(-sp.I * sp.pi), sp.exp(sp.I * sp.pi))) == -sp.eye(2)
        and deck("RP2") == -sp.eye(2),
    )

    claimed = sp.I / 4
    actual = sp.exp(sp.I / 4)
    checks.check(
        "fresh exact comparison rejects i-over-four as the cited phase factor",
        sp.simplify(claimed - actual) != 0,
    )
    checks.check(
        "fresh norm comparison distinguishes a nonphase from a unit phase",
        sp.Abs(claimed) == sp.Rational(1, 4)
        and sp.simplify(actual * sp.conjugate(actual)) == 1,
    )
    checks.check(
        "the source bosonic guard changes both physical inputs",
        "holonomy(sp.Integer(1), 1)" in text
        and "fermionParity(0)" in text,
    )
    checks.check(
        "the source's scalar-set oracle cannot detect typed mutations",
        len({sp.Integer(-1), sp.Integer(-1), sp.Integer(-1)}) == 1
        and len({("link", -1), ("charge", -1)}) == 2,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
