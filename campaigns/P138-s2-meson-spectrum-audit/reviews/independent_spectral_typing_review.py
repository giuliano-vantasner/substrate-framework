from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "48a9eadf6fbc1e3ebe7fcd6b98c2d60cc10a3f5282404c84e4626910f296eaf7"
DOSSIER_SHA256 = "74e77d5130c9f2f96132572bd9720d90b8da0902130dfb0866b4b4035de783ed"
FROZEN_PROPOSAL_SHA256 = "8e54ead36c74e87475abebb019f151740999a0216518b296a0af1ebd3546e608"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_file: str, dossier_file: str) -> int:
    source_path = Path(source_file)
    dossier_path = Path(dossier_file)
    frozen_path = Path(__file__).parents[1] / "evidence" / "frozen-proposal.yaml"
    source_text = source_path.read_text(encoding="utf-8")
    dossier_text = dossier_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(source_path))
    checks = CheckLedger("P138-INDEPENDENT-SPECTRAL-TYPING")

    checks.check("fresh source hash", _sha256(source_path) == SOURCE_SHA256)
    checks.check("fresh dossier hash", _sha256(dossier_path) == DOSSIER_SHA256)
    checks.check(
        "fresh frozen proposal hash",
        _sha256(frozen_path) == FROZEN_PROPOSAL_SHA256,
    )

    radius = sp.Symbol("r", positive=True)
    field, field_prime, field_second = sp.symbols("f fp fpp", real=True)
    mode, mode_prime = sp.symbols("eta etap", real=True)
    density = (
        (radius**2 + 2 * sp.sin(field) ** 2) * field_prime**2
        + 2 * sp.sin(field) ** 2
        + sp.sin(field) ** 4 / radius**2
    )
    gradient = sp.simplify(sp.diff(density, field_prime, 2) / 2)
    mixed = sp.simplify(sp.diff(density, field, field_prime))
    local = sp.simplify(sp.diff(density, field, 2) / 2)
    mixed_derivative = sp.simplify(
        sp.diff(mixed, field) * field_prime
        + sp.diff(mixed, field_prime) * field_second
        + sp.diff(mixed, radius)
    )
    correction = sp.simplify(-mixed_derivative / 2)

    checks.check(
        "fresh density differentiation gives the radial gradient coefficient",
        sp.simplify(gradient - radius**2 - 2 * sp.sin(field) ** 2) == 0,
    )
    checks.check(
        "fresh density differentiation gives the mixed coefficient",
        sp.simplify(mixed - 4 * sp.sin(2 * field) * field_prime) == 0,
    )
    checks.check(
        "fresh integration by parts gives a nonzero correction",
        sp.simplify(
            correction
            + 4 * sp.cos(2 * field) * field_prime**2
            + 2 * sp.sin(2 * field) * field_second
        )
        == 0
        and correction != 0,
    )
    checks.check(
        "source potential equals the local term rather than the complete term",
        "C_pot = 0.5 * (d2_sin2f + d2_skyrme_grad + d2_sin4f / fr ** 2)"
        in source_text
        and "mixed_boundary_correction" not in source_text,
    )

    far_gradient = sp.simplify(gradient.subs({field: 0, field_prime: 0}))
    far_local = sp.simplify(local.subs({field: 0, field_prime: 0}))
    far_correction = sp.simplify(
        correction.subs({field: 0, field_prime: 0, field_second: 0})
    )
    checks.check(
        "fresh far-field reduction has zero continuum edge",
        far_gradient == radius**2
        and far_local + far_correction == 2
        and sp.limit((far_local + far_correction) / far_gradient, radius, sp.oo)
        == 0,
    )

    wall = sp.Symbol("R", positive=True)
    box_level = sp.pi**2 / wall**2
    checks.check(
        "positive massless box levels collapse without becoming bound",
        box_level > 0
        and sp.limit(box_level, wall, sp.oo) == 0,
    )

    inertia = sp.Symbol("I", positive=True)
    j_low, j_high = sp.Rational(1, 2), sp.Rational(3, 2)
    quantum_split = sp.simplify(
        (j_high * (j_high + 1) - j_low * (j_low + 1)) / (2 * inertia)
    )
    classical_split = sp.simplify((j_high**2 - j_low**2) / (2 * inertia))
    checks.check(
        "fresh rotor arithmetic separates declared quantum and classical laws",
        quantum_split == sp.Rational(3, 2) / inertia
        and classical_split == 1 / inertia,
    )
    target = sp.Symbol("Delta", positive=True)
    fitted_inertia = sp.Rational(3, 2) / target
    checks.check(
        "fresh fit counterfamily reproduces every chosen splitting",
        sp.simplify(sp.Rational(3, 2) / fitted_inertia - target) == 0,
    )

    tail_coefficient = sp.Symbol("c", positive=True)
    tail_field = tail_coefficient / radius**2
    tail_derivative = sp.diff(tail_field, radius)
    tail_density = sp.simplify(
        radius**2
        * tail_field**2
        * (1 + tail_derivative**2 + tail_field**2 / radius**2)
    )
    checks.check(
        "fresh inertia tail has a nonzero inverse-wall contribution",
        sp.limit(radius**2 * tail_density, radius, sp.oo) == tail_coefficient**2
        and sp.limit(
            wall
            * sp.integrate(tail_coefficient**2 / radius**2, (radius, wall, sp.oo)),
            wall,
            sp.oo,
        )
        == tail_coefficient**2,
    )

    first = sp.diag(1, 4)
    second = sp.diag(1, 9)
    checks.check(
        "fresh equal-value countermodel rejects operator identity",
        first[0, 0] == second[0, 0]
        and first.charpoly().as_expr() != second.charpoly().as_expr(),
    )

    eigenvalue, shift = sp.symbols("lambda shift")
    checks.check(
        "fresh generalized-matrix shift makes the tachyon guard tautological",
        sp.expand((eigenvalue - shift) - eigenvalue + shift) == 0,
    )

    executable_names = {
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    }
    checks.check(
        "fresh AST finds no resonance or width computation",
        not ({"phase_shift", "resonance_width", "pole", "quasinormal"} & executable_names),
    )
    checks.check(
        "source explicitly imports the collective and particle dictionaries",
        "Finkelstein-Rubinstein J=I constraint" in source_text
        and "pion-as-Goldstone identification" in source_text,
    )
    checks.check(
        "dossier requests a bound state but provides no scattering oracle",
        "REAL bound state" in dossier_text
        and "phase shift" not in dossier_text.lower(),
    )

    checks.check(
        "a shared lift scalar does not type a meson or fluctuation spectrum",
        sp.simplify(
            16 * sp.sqrt(1 - sp.Symbol("w", positive=True) ** 2)
            / sp.sqrt(sp.Symbol("N", positive=True))
            - 16
            * sp.sqrt(1 - sp.Symbol("w", positive=True) ** 2)
            * sp.Symbol("N", positive=True) ** sp.Rational(-1, 2)
        )
        == 0
        and first != second,
    )

    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    parser.add_argument("dossier_file")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_file, arguments.dossier_file))
