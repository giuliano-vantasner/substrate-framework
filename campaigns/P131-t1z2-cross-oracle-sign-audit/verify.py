"""Primary exact and semantic-ceiling verifier for P131/T1Z2."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.topological_labels import (
    binary_product_character,
    binary_product_character_kernel,
    cyclic_sign_character,
    cyclic_sign_character_ledger,
    winding_parity,
)
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path("campaigns/P131-t1z2-cross-oracle-sign-audit")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-1/"
    "bridge_T1Z2_same_minus_one.py"
)
SOURCE_SHA = "d9c08f9440fb79b9ef445ad77aff113db6c7c7f8943c5838180fb5704fd71bed"
FREEZE_SHA = "ab10fe25cab238261beceea1304c2faad44b426b31fb03bc3be5def752f167bb"
CHARGE = Path(
    "/home/dan/substrate/sg-breather-ionization/dynamics_lean/"
    "ChargeDiscrimination.lean"
)
CHARGE_SHA = "c692eb12d9aa81f7547f855fe24ed03f7ba2403ac3fc4710c33c42ff80364056"
BRIDGE = Path(
    "/home/dan/substrate/sg-breather-ionization/dynamics_lean/Bridge.lean"
)
BRIDGE_SHA = "2299d6cbc402d91168a07db526bf966f9fe6d8c8cd6cd3198e56cfa4986db47b"


def source_check_calls(tree: ast.AST) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]


def imported_modules(tree: ast.AST) -> set[str]:
    modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    modules.update(
        node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    )
    return modules


def source_holonomy(strength: sp.Expr, links: sp.Expr = sp.Integer(1)) -> sp.Expr:
    return sp.simplify(sp.exp(2 * sp.pi * sp.I * strength * links))


@dataclass(frozen=True)
class TypedEvaluation:
    domain: str
    map_name: str
    element_class: int
    value: int


def one_typed_evaluation(values: tuple[TypedEvaluation, ...]) -> bool:
    return bool(values) and len(set(values)) == 1


def main() -> int:
    checks = CheckLedger("T1Z2-CROSS-ORACLE-SIGN-AUDIT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)

    checks.check(
        "T1Z2 source bytes are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "immutable preregistration remains byte identical",
        hashlib.sha256((CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA,
    )
    checks.check(
        "ten source predicates match the terminal tally",
        len(source_check_calls(tree)) == 10,
    )
    checks.check(
        "the executable dependency inventory is SymPy only",
        imported_modules(tree) == {"sympy"},
    )
    checks.check(
        "T1Z2 has no quadrature compatibility path",
        all(
            token not in source_text
            for token in ("np.trapz", "np.trapezoid", "trapezoid_integral", "scipy.integrate")
        ),
    )

    c2 = cyclic_sign_character_ledger(2)
    checks.check(
        "the unique nontrivial C2 sign character is already canonical",
        c2.generator_images == (1, -1)
        and c2.nontrivial_kernel == (0,)
        and c2.nontrivial_faithful,
    )
    checks.check(
        "the selected C2 identity and generator values are exact",
        cyclic_sign_character(2, 0, generator_image=-1) == 1
        and cyclic_sign_character(2, 1, generator_image=-1) == -1,
    )
    checks.check(
        "the half-strength integer-link holonomy is exactly winding parity",
        all(
            source_holonomy(sp.Rational(1, 2), link) == winding_parity(link)
            for link in range(-12, 13)
        ),
    )
    checks.check(
        "the source kink and antikink evaluations are the same accepted odd class",
        winding_parity(1) == -1
        and winding_parity(-1) == -1
        and winding_parity(2) == 1,
    )
    checks.check(
        "the source's four selected scalar values really coincide",
        len(
            {
                source_holonomy(sp.Rational(1, 2), 1),
                winding_parity(1),
                winding_parity(-1),
                cyclic_sign_character(2, 1, generator_image=-1),
            }
        )
        == 1,
    )
    checks.check(
        "the headline one-object oracle is only a set of scalar expressions",
        "one_value = len({pulson_minus_one, lean_kink, lean_antikink, chi_F(1)}) == 1"
        in source_text,
    )
    z6 = next(
        call
        for call in source_check_calls(tree)
        if isinstance(call.args[0], ast.Constant) and "Z6 [CROSS-ORACLE" in call.args[0].value
    )
    z6_names = {node.id for node in ast.walk(z6.args[1]) if isinstance(node, ast.Name)}
    checks.check(
        "the headline condition contains no domain map generator or intertwiner",
        z6_names == {"bool", "cross_oracle_equal", "one_value"},
    )

    c4 = cyclic_sign_character_ledger(4)
    checks.check(
        "C4 reproduces every selected odd-even sign while remaining a distinct source group",
        c4.nontrivial_kernel == (0, 2)
        and not c4.nontrivial_faithful
        and tuple(cyclic_sign_character(4, k, generator_image=-1) for k in range(4))
        == (1, -1, 1, -1),
    )
    checks.check(
        "two C2-product characters agree at minus one but have different full maps",
        binary_product_character((1, 1), (1, 0)) == -1
        and binary_product_character((1, 1), (0, 1)) == -1
        and binary_product_character((1, 0), (1, 0)) == -1
        and binary_product_character((1, 0), (0, 1)) == 1
        and binary_product_character_kernel((1, 0))
        != binary_product_character_kernel((0, 1)),
    )
    typed_baseline = (
        TypedEvaluation("C2", "chi", 1, -1),
        TypedEvaluation("C2", "chi", 1, -1),
    )
    typed_mutations = (
        (
            TypedEvaluation("linking integers", "holonomy", 1, -1),
            TypedEvaluation("charge integers", "parity", 1, -1),
        ),
        (
            TypedEvaluation("C2xC2", "first_projection", 1, -1),
            TypedEvaluation("C2xC2", "second_projection", 1, -1),
        ),
        (
            TypedEvaluation("C2", "chi", 1, -1),
            TypedEvaluation("C2", "chi", 0, 1),
        ),
    )
    checks.mutation_sensitive(
        "typed object identity",
        one_typed_evaluation,
        typed_baseline,
        typed_mutations,
    )

    checks.check(
        "the unrestricted holonomy formula is not a sign character",
        source_holonomy(sp.Rational(1, 3), 1) not in (sp.Integer(-1), sp.Integer(1))
        and source_holonomy(sp.Rational(1, 2), 1) == -1,
    )
    checks.check(
        "the source character helpers do not enforce their advertised C2 and integer domains",
        "def chi_F(k):" in source_text
        and "return (-1) ** k" in source_text
        and "def fermionParity(Q):" in source_text
        and "return (-1) ** abs(Q)" in source_text,
    )
    checks.check(
        "the deck route assigns rather than derives the host action",
        'return -I2 if host == "RP2" else I2' in source_text
        and 'deck_central("RP2")' in source_text
        and 'deck_central("S2")' in source_text,
    )
    checks.check(
        "renaming the RP2 string flips the source deck verdict",
        (lambda host: -sp.eye(2) if host == "RP2" else sp.eye(2))("RP2")
        != (lambda host: -sp.eye(2) if host == "RP2" else sp.eye(2))("RP^2"),
    )
    rotation = sp.diag(sp.exp(-sp.I * sp.pi), sp.exp(sp.I * sp.pi))
    checks.check(
        "the SU2 two-pi matrix arithmetic survives without the deck interpretation",
        sp.simplify(rotation) == -sp.eye(2),
    )
    checks.check(
        "the bosonic guard changes source inputs instead of mutating one character on fixed inputs",
        "holonomy(sp.Integer(1), 1)" in source_text
        and "fermionParity(0)" in source_text
        and "holonomy(sp.Rational(1, 2), 1)" in source_text,
    )

    charge_bytes = CHARGE.read_bytes()
    bridge_bytes = BRIDGE.read_bytes()
    bridge_text = bridge_bytes.decode("utf-8")
    checks.check(
        "the cited Lean parity and exchange files are hash pinned",
        hashlib.sha256(charge_bytes).hexdigest() == CHARGE_SHA
        and hashlib.sha256(bridge_bytes).hexdigest() == BRIDGE_SHA,
    )
    checks.check(
        "the cited Lean exchange factor is exp(i/4), not the source's i/4 literal",
        "exchangePhaseFactor 1 = Complex.exp (I / 4)" in bridge_text
        and "exchange_phase_beta2_eq_1 = I / 4" in source_text
        and sp.simplify(sp.exp(sp.I / 4) - sp.I / 4) != 0,
    )
    checks.check(
        "the source i/4 has nonunit modulus while the cited phase factor has unit modulus",
        sp.Abs(sp.I / 4) == sp.Rational(1, 4)
        and sp.simplify(sp.exp(sp.I / 4) * sp.conjugate(sp.exp(sp.I / 4))) == 1,
    )
    checks.check(
        "the exact surviving surface is already governed by C-TOP-001 and C-CHR-001",
        all(winding_parity(k) == cyclic_sign_character(2, k, generator_image=-1) for k in range(-8, 9)),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
