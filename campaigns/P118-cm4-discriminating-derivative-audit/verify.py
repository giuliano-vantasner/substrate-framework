"""Primary exact verifier for P118's CM4 derivative-bar audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import Callable

import numpy as np
import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-31/"
    "bridge_CM4_discriminating_bar.py"
)
BARRIER_SOURCE = Path("/home/dan/substrate/engineering/barrier_scaling.py")
SOURCE_SHA256 = "984b5a1495c0d17095b127cc79eceb9625592051b0e5ab099bc66683b418c019"
BARRIER_SHA256 = "8aff859aeff9bd2d317f3c458faa9e617e3865d3c8e12a6b198c15d92cf85014"
CONTRACT_SHA256 = "41bccffea4bb1ece5651116b441731257fc487c44da843b5e0d11aee8cd644eb"
FREEZE_SHA256 = "41bccffea4bb1ece5651116b441731257fc487c44da843b5e0d11aee8cd644eb"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P118-cm4-discriminating-derivative-audit"),
        Path("proposals/P118-cm4-discriminating-derivative-audit"),
    )
    return next(path for path in candidates if path.exists())


def _extract_source_gate(source_tree: ast.Module) -> Callable[..., bool]:
    function = next(
        node
        for node in source_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "clears_bar"
    )
    module = ast.fix_missing_locations(
        ast.Module(body=[function], type_ignores=[])
    )
    namespace: dict[str, object] = {"np": np}
    exec(compile(module, str(SOURCE), "exec"), namespace)
    return namespace["clears_bar"]  # type: ignore[return-value]


def main() -> int:
    checks = CheckLedger("CM4-EXACT-AUDIT")
    root = _campaign_root()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "CM4 source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "the imported barrier helper hash is pinned",
        hashlib.sha256(BARRIER_SOURCE.read_bytes()).hexdigest() == BARRIER_SHA256,
    )
    normalized_contract = (
        (root / "proposal.yaml")
        .read_bytes()
        .replace(b"status: accepted\n", b"status: draft\n")
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-source contract is immutable",
        hashlib.sha256((root / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "ten static predicates match the runtime tally",
        len(source_checks) == 10
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "CM4 has no sampled-integration compatibility event",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "trapezoid_integral" not in source_text
        and "scipy.integrate" not in source_text,
    )

    count, loading, barrier, temperature, prefactor = sp.symbols(
        "N L C Theta nu",
        positive=True,
    )
    exponent = sp.simplify(barrier / (loading * temperature))
    response = sp.simplify(prefactor * count * sp.exp(-exponent))
    checks.check(
        "the declared conditional response is exact and positive",
        response.is_positive is True,
    )

    count_derivative = sp.diff(response, count)
    checks.check(
        "the continuous count extension is exactly linear and increasing",
        sp.simplify(count_derivative - prefactor * sp.exp(-exponent)) == 0
        and count_derivative.is_positive is True
        and sp.diff(response, count, 2) == 0,
    )
    integer_count = sp.symbols("m", integer=True, positive=True)
    forward_difference = sp.simplify(
        response.subs(count, integer_count + 1)
        - response.subs(count, integer_count)
    )
    checks.check(
        "integer count variation has an exact positive forward difference",
        sp.simplify(forward_difference - count_derivative) == 0
        and forward_difference.is_positive is True,
    )
    checks.check(
        "comparison with count one is conditional algebra rather than a two-body theorem",
        sp.simplify(
            response - response.subs(count, 1)
            - prefactor * sp.exp(-exponent) * (count - 1)
        )
        == 0,
    )

    loading_derivative = sp.factor(sp.diff(response, loading))
    expected_loading_derivative = sp.simplify(
        response * barrier / (loading**2 * temperature)
    )
    checks.check(
        "the loading-coordinate derivative is exact and positive",
        sp.simplify(loading_derivative - expected_loading_derivative) == 0
        and loading_derivative.is_positive is True,
    )
    checks.check(
        "temperature opens and barrier height closes the conditional response",
        sp.diff(response, temperature).is_positive is True
        and sp.diff(response, barrier).is_negative is True,
    )
    checks.check(
        "the exact log elasticities expose every held-fixed convention",
        sp.simplify(count * sp.diff(sp.log(response), count)) == 1
        and sp.simplify(loading * sp.diff(sp.log(response), loading) - exponent)
        == 0
        and sp.simplify(
            temperature * sp.diff(sp.log(response), temperature) - exponent
        )
        == 0
        and sp.simplify(barrier * sp.diff(sp.log(response), barrier) + exponent)
        == 0
        and sp.simplify(prefactor * sp.diff(sp.log(response), prefactor)) == 1,
    )
    checks.check(
        "loading limits run from zero to a finite prefactor ceiling",
        sp.limit(response, loading, 0, dir="+") == 0
        and sp.limit(response, loading, sp.oo) == prefactor * count,
    )
    second_loading_derivative = sp.factor(sp.diff(response, loading, 2))
    expected_second = sp.simplify(
        response * exponent * (exponent - 2) / loading**2
    )
    checks.check(
        "the loading response changes curvature at exponent two",
        sp.simplify(second_loading_derivative - expected_second) == 0
        and second_loading_derivative.subs(
            {prefactor: 1, count: 1, barrier: 1, loading: 1, temperature: 1}
        ).is_negative
        is True
        and second_loading_derivative.subs(
            {prefactor: 1, count: 1, barrier: 3, loading: 1, temperature: 1}
        ).is_positive
        is True,
    )

    scale = sp.symbols("rho", positive=True)
    checks.check(
        "common barrier and temperature scaling leaves the response invariant",
        sp.simplify(
            response.subs(
                {barrier: scale * barrier, temperature: scale * temperature},
                simultaneous=True,
            )
            - response
        )
        == 0,
    )
    checks.check(
        "co-scaling loading and its barrier numerator is another exact convention",
        sp.simplify(
            response.subs(
                {barrier: scale * barrier, loading: scale * loading},
                simultaneous=True,
            )
            - response
        )
        == 0,
    )
    target = sp.symbols("R_target", positive=True)
    checks.check(
        "a free positive prefactor fits any selected response magnitude",
        sp.simplify(
            response.subs(prefactor, target / (count * sp.exp(-exponent)))
            - target
        )
        == 0,
    )
    checks.check(
        "zero interaction is a zero-rate countermodel outside the positive surrogate",
        0 * response == 0 and response.is_positive is True,
    )

    power_count, power_loading = sp.symbols("p q", positive=True)
    generalized = sp.simplify(
        prefactor
        * count**power_count
        * sp.exp(-barrier / (loading**power_loading * temperature))
    )
    checks.check(
        "an infinite alternative monomial family shares both positive derivative signs",
        sp.diff(generalized, count).is_positive is True
        and sp.diff(generalized, loading).is_positive is True,
    )

    source_gate = _extract_source_gate(source_tree)
    checks.check(
        "the source gate accepts its selected increasing count sweep",
        source_gate([2, 3, 4, 5], [2.0, 3.0, 4.0, 5.0]) is True,
    )
    checks.check(
        "the source gate rejects its selected flat decreasing and singleton fakes",
        source_gate([2, 3], [1.0, 1.0]) is False
        and source_gate([2, 3], [2.0, 1.0]) is False
        and source_gate([1], [1.0]) is False,
    )
    checks.check(
        "reversed and duplicated controls can pass because only response order is tested",
        source_gate([4, 3, 2], [1.0, 2.0, 3.0]) is True
        and source_gate([2, 2], [1.0, 2.0]) is True,
    )
    checks.check(
        "mismatched control and response lengths can pass",
        source_gate([2, 3], [1.0, 2.0, 3.0]) is True,
    )
    checks.check(
        "the A-squared route can pass reversed or nonpositive controls",
        source_gate(
            [1],
            [1.0],
            A2_points=[2.0, 1.0],
            R_of_A2=[1.0, 2.0],
        )
        is True
        and source_gate(
            [1],
            [1.0],
            A2_points=[-2.0, -1.0],
            R_of_A2=[1.0, 2.0],
        )
        is True,
    )
    checks.check(
        "the A-squared OR route bypasses the claimed count sweep requirement",
        source_gate(
            [1],
            [1.0],
            A2_points=[1.0, 2.0],
            R_of_A2=[1.0, 2.0],
        )
        is True,
    )
    checks.check(
        "one floating-point ulp is treated as a discriminating positive sweep",
        source_gate(
            [2.0, 3.0],
            [1.0, np.nextafter(1.0, 2.0)],
        )
        is True,
    )
    checks.check(
        "an unrelated affine response clears the same source bar",
        source_gate([2, 3, 4], [5.0, 7.0, 9.0]) is True,
    )

    checks.mutation_sensitive(
        "count and loading response conventions are load bearing",
        lambda candidate: sp.simplify(sp.diff(candidate, count) - count_derivative)
        == 0
        and sp.simplify(sp.diff(candidate, loading) - loading_derivative) == 0,
        response,
        (
            prefactor * count * sp.exp(exponent),
            prefactor * count**2 * sp.exp(-exponent),
            prefactor * count * sp.exp(-barrier * loading / temperature),
            prefactor * sp.exp(-exponent),
        ),
    )
    checks.mutation_sensitive(
        "integer forward sign and unit step are load bearing",
        lambda candidate: sp.simplify(candidate - forward_difference) == 0,
        forward_difference,
        (-forward_difference, 2 * forward_difference, response.subs(count, integer_count)),
    )

    proposal = yaml.safe_load((root / "proposal.yaml").read_text())
    checks.check(
        "the frozen novelty gate proposes no claim before nonduplication review",
        proposal["claims_proposed"] == [],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
