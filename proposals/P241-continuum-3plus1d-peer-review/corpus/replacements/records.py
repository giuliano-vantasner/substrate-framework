"""P241 replacement records — corrected statements for revision-required claims.

Standalone module: python3 records.py

Each record names the audited claim, the defect established by the oracle
modules under checks/, and the minimum honest corrected statement. The
`oracle` field points at the module(s) whose passing run substantiates the
record. This file is data + one consistency probe; it re-runs no oracles.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

RECORDS: list[dict[str, object]] = [
    {
        "id": "RP-S02",
        "claim": "P241-S02",
        "defect": "Unit bullets are mutually inconsistent: u dimensionless with "
                  "Theta_ij in N gives c0^2 = Theta0/rho0 the units m^2/s^2 only "
                  "if Theta is J/m^3 * (length/... ) — as printed c0^2 acquires "
                  "m^4/s^2.",
        "replacement": "Declare u a displacement with dimension LENGTH; then "
                       "Theta_ij has dimensions energy density (J m^-3 = Pa), "
                       "rho0 mass density, c0^2 = Theta0/rho0 in m^2 s^-2, and "
                       "Z0 = rho0^(1/3) det(Theta)^(1/3)... in kg m^-2 s^-1 as "
                       "required. Table: [u]=m, [Theta]=Pa, [rho]=kg m^-3, "
                       "[c0]=m/s, [Z0]=kg m^-2 s^-1, [mu0]=m^-1, [M0]=kg.",
        "oracle": "checks/sympy/S02_dimension_declarations.py",
    },
    {
        "id": "RP-S05",
        "claim": "P241-S05/S06",
        "defect": "Cited no-go theorems concern charged/time-dependent classes; "
                  "for the printed convex U the Derrick scaling E(lam) = "
                  "Eg/lam + Ep/lam^3 has E'(lam) < 0 in d=3, so static lumps "
                  "are excluded, and small-amplitude data radiates (no "
                  "sublinear binding).",
        "replacement": "Scope Section 3 to time-dependent localization; state "
                       "the Derrick obstruction explicitly for d=3; require a "
                       "DECLARED nonconvex potential (e.g. sine-Gordon class of "
                       "the cited 1+1D source) for oscillon/pulson existence "
                       "claims, which then remain finite-time numerical "
                       "hypotheses.",
        "oracle": "checks/scipy/N01_oscillon_existence.py",
    },
    {
        "id": "RP-S08",
        "claim": "P241-S08",
        "defect": "Scalar matching rho(det Theta)^(1/3) = Z0 does not make an "
                  "anisotropic interface reflectionless (counterexample at "
                  "impedance ratio r != 1); 'reflectionless' needs directional "
                  "impedances.",
        "replacement": "State reflectionlessness conditionally: an interface is "
                       "reflectionless iff the full impedance tensor is matched "
                       "in every propagation direction, Z(n) = sqrt(<n,rho n> / "
                       "<n,Theta^{-1} n>) equal on both sides; scalar matching "
                       "covers only isotropic slices (verified numerically).",
        "oracle": "checks/sympy/S08_directional_impedance.py; "
                  "checks/scipy/N03_impedance_interface.py",
    },
    {
        "id": "RP-S10",
        "claim": "P241-S10",
        "defect": "M0 = E0/c0^2 constancy along the path is used but never "
                  "hypothesized; counterexamples with position-dependent Theta "
                  "(fixed U) vary M0.",
        "replacement": "Add the explicit hypothesis E0(X) = const (equivalently "
                       "adiabatic invariance of the collective coordinate), or "
                       "derive it from an action-invariance assumption; without "
                       "it trajectories acquire non-geodesic force terms and "
                       "Section 5's conclusion is conditional.",
        "oracle": "checks/sympy/S10_rest_mass_variation.py",
    },
    {
        "id": "RP-S18",
        "claim": "P241-S18",
        "defect": "Displayed Eq. (43) carries the wrong sign and omits the "
                  "1/n^2 factor: geodesics of g00=-1/n give d2X/dt2 = "
                  "+c0^2 grad(n)/(2 n^3) toward INCREASING n.",
        "replacement": "Replace (43) by d2X/dt2 = +c0^2 grad(ln n)/(2 n^2) = "
                       "+c0^2 grad(n)/(2 n^3); keep the (correct) "
                       "M0-independence statement.",
        "oracle": "checks/sympy/S18_newtonian_limit_sign.py; "
                  "checks/scipy/N02_geodesic_universality.py",
    },
    {
        "id": "RP-S19",
        "claim": "P241-S19",
        "defect": "'Every energy concentration ... including the massless case' "
                  "is false: leading transverse-acceleration ratio null/massive "
                  "is exactly 2.",
        "replacement": "Scope the equivalence principle to massive lumps: "
                       "universal free fall across M0 holds; massless probes "
                       "follow Fermat rays of index nbar^2 and curve twice as "
                       "much per unit time (the analogue of GR's light-bending "
                       "factor).",
        "oracle": "checks/sympy/S19_massless_factor_two.py; "
                  "checks/scipy/N05_null_massive_deflection.py",
    },
    {
        "id": "RP-S20",
        "claim": "P241-S20",
        "defect": "Section 9's Schwarzschild profiles are implicit and carry a "
                  "convention ambiguity; no closed conformal realization is "
                  "displayed.",
        "replacement": "Adopt the exact realization Omega^2 = f^(-1/3) with "
                       "f = 1 - rs/r: n_r = f^(-4/3), n_t = n_phi = f^(-1/3), "
                       "lambda_r = c0^2 f^(8/3), lambda_t = lambda_phi = c0^2 "
                       "f^(2/3); induced metric equals Omega^2 x Schwarzschild "
                       "componentwise exactly.",
        "oracle": "checks/sympy/S20_schwarzschild_corrected.py",
    },
    {
        "id": "RP-S21",
        "claim": "P241-S21",
        "defect": "Kerr dictionary defects: printed (56) drops a Sigma^2 from "
                  "its own coordinate determinant and matches no convention; "
                  "spatial exactness forces Omega^2=1 so the temporal component "
                  "cannot match; (57)'s second equality contradicts its first "
                  "(c0-power slip); A^{thth}, A^{phph} are not speed squared.",
        "replacement": "With rs = 2GM/c0^2 use Omega^4 = (Delta r^4/(Sigma Ag))^"
                       "(1/3) * Sigma Ag/(Ag Delta + rs^2 c0^4 a^2 r^2 sin^2 th)"
                       " (rational core identity K(Q+R)=1); n_r = Omega^2 "
                       "Sigma/Delta, n_th = Omega^2 Sigma/r^2, n_phi = Omega^2 "
                       "Ag/(Sigma r^2), V_phi = -rs a c0^3 r^2 sin(th)/Ag; all "
                       "five Kerr components match up to the declared Omega^2.",
        "oracle": "checks/sympy/S21_kerr_dictionary_audit.py; "
                  "checks/sympy/S21_kerr_corrected_dictionary.py",
    },
    {
        "id": "RP-S22",
        "claim": "P241-S22",
        "defect": "The equatorial minimal model coincides verbatim with the "
                  "published 2+1D rotating model but NOT with the paper's own "
                  "full 3+1D construction at theta = pi/2.",
        "replacement": "Rename to 'minimal rotating acoustic model' and cite "
                       "the 2+1D companion as provenance; do not present it as "
                       "the theta = pi/2 slice of Sections 8-9.",
        "oracle": "checks/sympy/S22_minimal_model_published.py",
    },
    {
        "id": "RP-S23",
        "claim": "P241-S23",
        "defect": "Section 10 composes the chain (existence -> kinematics -> "
                  "metric -> equivalence principle) as if each link were "
                  "accepted; several links are conditional or revised above.",
        "replacement": "State the chain conditionally: each implication inherits "
                       "the scope of its predecessors (declared nonconvex "
                       "potential for localization; E0 constancy hypothesis; "
                       "massive-only universality; corrected (43); corrected "
                       "Schwarzschild/Kerr realizations). The headline sentence "
                       "'first fundamental advancement since Einstein 1907' "
                       "must be deleted or restated as the scoped theorem.",
        "oracle": "review/peer-review.md (composition audit)",
    },
]



def main() -> dict[str, object]:
    missing: list[str] = []
    pending_docs: list[str] = []
    for rec in RECORDS:
        for part in str(rec["oracle"]).split(";"):
            part = part.strip()
            if not part:
                continue
            path = HERE.parent / part
            if path.exists():
                continue
            if part.endswith(".py"):
                missing.append(f"{rec['id']}: {part}")
            else:
                pending_docs.append(f"{rec['id']}: {part}")
    report = {"suite": "p241-replacement-records", "records": len(RECORDS),
              "missing_oracles": missing, "pending_doc_refs": pending_docs,
              "passed": not missing}
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    result = main()
    raise SystemExit(0 if result["passed"] else 1)
