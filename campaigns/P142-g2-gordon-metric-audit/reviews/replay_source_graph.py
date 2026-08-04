from __future__ import annotations

import argparse
import ast
import hashlib
from dataclasses import dataclass
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class SourceNode:
    unit: str
    path: str
    sha256: str
    static_checks: int
    role: str


NODES = (
    SourceNode("G2", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6, "primary"),
    SourceNode("B1", "merged-framework/bridges/phase-7/bridge_B1_disclination_berry_connection.py", "2de4faa60ecc1f87ca356afd55c2a531a89327c3c46e4296176052113de7b0b6", 8, "pending_dependency"),
    SourceNode("C1", "merged-framework/bridges/phase-7/bridge_C1_Aeff_optical_metric_coupling.py", "6c0b625cbfd8396104f185e4e3785956f66989a10d9fddf9d553fe433c39f0f5", 9, "pending_dependency_consumer"),
    SourceNode("T2C", "merged-framework/bridges/phase-2/bridge_T2C_tidal_MP.py", "651fd75287dd25b5c34208ea5789df89be50f5050ec139ae2d99f4962440c369", 13, "qualified_dependency"),
    SourceNode("T1E", "merged-framework/bridges/phase-1/bridge_T1E_E0_triple_oracle.py", "bdd57d929b7bed2436ad5803f0a614d4887a35a7eab5ecd78b23041888e48a97", 11, "qualified_consumer"),
    SourceNode("EM3", "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py", "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9", 11, "qualified_consumer"),
    SourceNode("S1", "merged-framework/bridges/phase-4/bridge_S1_nn_force_two_skyrmion.py", "ebe1ba930be26f17671d8e82779d14fc00e7a8b988a4aada722a32d0d9328ddd", 11, "qualified_consumer"),
    SourceNode("G1", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10, "qualified_consumer"),
    SourceNode("G3", "merged-framework/bridges/phase-5/bridge_G3_horndeski_scalar_tensor.py", "8d462ce2bfd57bfced9fdedd511e9d2711e0c2454bc0d0441c681288495719ba", 11, "pending_consumer"),
    SourceNode("G4", "merged-framework/bridges/phase-5/bridge_G4_radiation_reaction_self_force.py", "308c8d82aff062fb0f0254498fb2bdb19fe6bdc207036cb0fa73643d3608c799", 10, "pending_consumer"),
    SourceNode("G5", "merged-framework/bridges/phase-5/bridge_G5_Geff_medium_density.py", "38a28bb452b055e7aa7894e1c31e3fcc98bfc5c6a8cbee2040aa003c62a4071a", 15, "pending_consumer"),
    SourceNode("W3", "merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py", "b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17", 7, "pending_consumer"),
    SourceNode("W4", "merged-framework/bridges/phase-6/bridge_W4_neutrino_missing_energy.py", "afa341c860ba89889d8d0a9fe6cd62948b5303f243e3884abf7d3acf24a7f602", 8, "pending_consumer"),
    SourceNode("W5", "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py", "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a", 27, "pending_consumer"),
    SourceNode("YM2", "merged-framework/bridges/phase-7/bridge_YM2_yang_mills_3plus1_lift.py", "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c", 10, "pending_consumer"),
    SourceNode("QCD1", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11, "pending_consumer"),
    SourceNode("QCD2", "merged-framework/bridges/phase-8/bridge_QCD2_su3_3plus1_lift.py", "64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f", 10, "pending_consumer"),
    SourceNode("SM1", "merged-framework/bridges/phase-9/bridge_SM1_combined_gauge_group.py", "bb7b70bc2ac0dd703f95ccbbaf843d40e78279f357795b9be74d6eee484749f2", 6, "pending_consumer"),
    SourceNode("GW1", "merged-framework/bridges/phase-12/bridge_GW1_multipole_lowest_quadrupole.py", "3aba56675f887f98c015de7caad1834893ffdbc27ca1daf3c7056694953102fc", 24, "qualified_consumer"),
    SourceNode("NC3", "merged-framework/bridges/phase-15/bridge_NC3_nonlinear_rectification.py", "dceed4b3d8f59daa75bbd6b31e9a726de99f180e252accb19f7d0ae625c5c9bd", 18, "qualified_consumer"),
    SourceNode("NC4", "merged-framework/bridges/phase-15/bridge_NC4_pde_robustness.py", "9efa788da093213f354cbd9e26b7bd0be81129d6f966128b5c0fd10fe0081570", 15, "qualified_consumer"),
    SourceNode("WZ4", "merged-framework/bridges/phase-17/bridge_WZ4_hls_vector_meson_anomalous.py", "fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b", 9, "qualified_consumer"),
    SourceNode("OD", "merged-framework/bridges/phase-19/bridge_OD_over_determination_test.py", "300259218ca36063625d42487dc1d8f00def4b5d58ef6ffc0b4dc174852fdeb6", 8, "qualified_consumer"),
    SourceNode("OM1", "merged-framework/bridges/phase-19/bridge_OM1_single_minus_one_identity.py", "c5af6786d4873675ddb552c4a0ae222e4ee3ab7472b74844b28dc4d257358007", 5, "qualified_consumer"),
    SourceNode("AS1", "merged-framework/bridges/phase-21/bridge_AS1_two_length_transmutation.py", "baca25e9b2b999088c1dc2969f9979cd341c582b3bdcfd009432db0eae9ea6cf", 10, "qualified_consumer"),
    SourceNode("AS3", "merged-framework/bridges/phase-21/bridge_AS3_sakharov_kappa_reduce.py", "f88cc85a3fb64d1b8aabdf53ced29168d78fce9470e586dc19564288a120903b", 8, "qualified_consumer"),
    SourceNode("AS4", "merged-framework/bridges/phase-21/bridge_AS4_over_determination_v2.py", "cdcfea3ac26c932a3db792c864baa026c761555d3c0e34c7b1bc025ea962745f", 7, "duplicate_consumer"),
    SourceNode("AS6", "merged-framework/bridges/phase-22/bridge_AS6_beta_self_dual_pin.py", "2f6c76d8aedde25b343f85cb54b2618cd03c816a29553fa70a523909265dd7f0", 9, "qualified_consumer"),
    SourceNode("OD3", "merged-framework/bridges/phase-22/bridge_OD3_beta_pinned.py", "af96fa76a30c9ebb863e0a50b605ade5003a7595f28188ce7ca4d0884d67910c", 8, "duplicate_consumer"),
    SourceNode("MC4", "merged-framework/bridges/phase-27/bridge_MC4_physical_units_pde.py", "db001de1fde9684282bb5353ec0a5ef4ddcf168809e0c02ca99878fb3f5ff698", 5, "qualified_consumer"),
    SourceNode("SC1", "merged-framework/bridges/phase-36/bridge_SC1_gordon_coupled_overdetermined.py", "70799bff934f1f6986545a0bde0cb94fe016dd4b468b36614ac3e5d9bb74aec0", 5, "pending_consumer"),
)


EXPECTED_COMPATIBILITY = {
    "B1": (0, 1, 0, 1, 1),
    "G1": (2, 0, 0, 0, 0),
    "G4": (1, 0, 0, 0, 0),
    "W3": (2, 0, 0, 0, 0),
    "YM2": (0, 1, 0, 1, 1),
    "QCD2": (0, 1, 0, 1, 1),
    "NC4": (1, 0, 0, 0, 0),
    "MC4": (1, 0, 0, 1, 0),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    root = Path(source_root)
    checks = CheckLedger("P142-G2-SOURCE-GRAPH")
    observed_predicates = 0
    observed_compatibility: dict[str, tuple[int, int, int, int, int]] = {}

    checks.check("thirty-one frozen dependency and reverse-consumer nodes", len(NODES) == 31)
    checks.check(
        "frozen authority classes are complete",
        {
            role: sum(node.role == role for node in NODES)
            for role in {node.role for node in NODES}
        }
        == {
            "primary": 1,
            "pending_dependency": 1,
            "pending_dependency_consumer": 1,
            "qualified_dependency": 1,
            "qualified_consumer": 14,
            "pending_consumer": 11,
            "duplicate_consumer": 2,
        },
    )

    for node in NODES:
        path = root / node.path
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
        static_checks = sum(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "check"
            for item in ast.walk(tree)
        )
        observed_predicates += static_checks
        checks.check(f"{node.unit} pinned source hash", _sha256(path) == node.sha256)
        checks.check(f"{node.unit} frozen predicate inventory", static_checks == node.static_checks)
        compatibility = audit_numpy_trapezoid_compatibility(text, filename=str(path))
        shape = (
            compatibility.direct_legacy_attributes,
            compatibility.dynamic_legacy_getattrs,
            compatibility.imported_legacy_names,
            compatibility.current_references,
            compatibility.eager_legacy_default_fallbacks,
        )
        if any(shape[index] for index in (0, 1, 2, 4)):
            observed_compatibility[node.unit] = shape

    checks.check("frozen graph inventories 325 source predicates", observed_predicates == 325)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        observed_compatibility == EXPECTED_COMPATIBILITY,
    )
    for unit, expected in EXPECTED_COMPATIBILITY.items():
        checks.check(
            f"{unit} retains exact alias-only compatibility shape",
            observed_compatibility[unit] == expected,
        )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
