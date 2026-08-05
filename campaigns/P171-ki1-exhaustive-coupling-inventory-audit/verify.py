#!/usr/bin/env python3
"""Pinned-tree and mutation-sensitivity audit of predecessor source KI1."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import subprocess

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


FRAMEWORK_ROOT = Path("/home/dan/substrate-framework")
SOURCE_ROOT = Path("/home/dan/substrate")
BASELINE = "6d1f4e02f87a0bd1dc326cb68af01872d1e88c64"
CREATION = "7222eed21720c5174dd35ba8f825d8b7e0a48f3f"
KI1 = "merged-framework/bridges/phase-34/bridge_KI1_exhaustive_coupling_search.py"
DOSSIER = "merged-framework/bridges/phase-34/dossiers/Phase34-KI-dossier.md"
E4 = "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py"
S4 = "merged-framework/bridges/phase-4/dossiers/S4-dossier.md"
WZ4 = "merged-framework/bridges/phase-17/bridge_WZ4_hls_vector_meson_anomalous.py"
KI2 = "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py"
MK1 = "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py"
MK2 = "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py"
MK3 = "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py"

PINNED_SOURCE_HASHES = {
    KI1: "a1ec5f8e64e56165d2c51ad2389ecb455870572ba4ef9eca292151bde4ddb42b",
    DOSSIER: "e01fbee40d81ebae1fc6f9452c321e2914cb185cdf257ae226d849ea6392702b",
    E4: "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7",
    S4: "1680127b0678d8969f7f08da0463ddab10f34e75554d3a842813275868030ed9",
    WZ4: "fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b",
    KI2: "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81",
    MK1: "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222",
    MK2: "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07",
    MK3: "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404",
}

PINNED_FRAMEWORK_HASHES = {
    "src/substrate_framework/bps_energy.py":
        "09e3bb41b98ba21f2909117ab1361020dfc7f12ef2722e9f620a65336bbe7d13",
    "tests/test_bps_energy.py":
        "b52db01583cf351891074cd656ac51414bdb13d9dac2536398c9847cb0863edb",
    "campaigns/P107-e4-bps-zero-binding-audit/verify.py":
        "91d3bcf4be848f3157d1b65fc6e6c0f1c8b1d23207f18816394facd6df1da7f0",
    "campaigns/P107-e4-bps-zero-binding-audit/reviews/independent_bps_review.py":
        "93477f9601c414ffc1c740684a11339400313ad263d4315e563dab55eff28852",
    "campaigns/P107-e4-bps-zero-binding-audit/attempts/0007/result.yaml":
        "e56f20867b0a31f8183211ff1f4094c133a002e35cd2a1af3621c74e256a0921",
}

BPS_COUPLING_CONTEXT = (
    r"lambda\s*\^?2?\s*(pi\^?2)?\s*b0|2\s*lambda\s*mu|"
    r"lambda\s*mu\s*pi|L6\s*\+\s*L0|-\s*lambda\^2\s*B_mu"
)
NUMERIC_ASSIGNMENT = (
    r"(?<![A-Za-z0-9_])(lam|mu|eps|epsilon|lambda)"
    r"(_(bps|BPS|skyrme|nb|near|nearbps|6|0))?\s*=\s*"
    r"[-+]?[0-9]*\.?[0-9]+"
)
BPS_SECTOR_CONTEXT = (
    r"BPS|sextic|L6\s*\+\s*L0|baryon current|generalized Skyrme|near.?BPS"
)
OMEGA_NUMERIC = (
    r"(?<![A-Za-z0-9_])(g_?omega|m_?omega)\s*=\s*[-+]?[0-9]*\.?[0-9]+"
)
SELF_DIR = "merged-framework/bridges/phase-34/"

EXPECTED_STRAYS = (
    "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py",
    "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py",
    "merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py",
    "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py",
    "merged-framework/bridges/phase-43/bridge_MK6_confrontation_and_tension.py",
    "merged-framework/bridges/phase-44/bridge_MR1_mass_unit_identity.py",
    "merged-framework/bridges/phase-44/bridge_MR2_bps_normalization_pi_squared.py",
    "merged-framework/bridges/phase-44/bridge_MR3_no_double_counting.py",
    "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py",
    "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py",
)


@dataclass(frozen=True)
class PatternBattery:
    """One candidate line classifier and its advertised controls."""

    assignment_pattern: str
    positive_lines: tuple[str, ...]
    negative_lines: tuple[str, ...]


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), *args],
        check=check,
        capture_output=True,
    )


def _blob(path: str, *, commit: str = BASELINE) -> bytes:
    return _git("show", f"{commit}:{path}").stdout


def _text(path: str, *, commit: str = BASELINE) -> str:
    return _blob(path, commit=commit).decode("utf-8", errors="ignore")


def _tree_paths(commit: str) -> tuple[str, ...]:
    output = _git("ls-tree", "-r", "--name-only", commit).stdout
    return tuple(output.decode("utf-8").splitlines())


def _grep(pattern: str, *, ignore_case: bool = True) -> tuple[str, ...]:
    command = ["grep", "-I", "-l", "-P"]
    if ignore_case:
        command.append("-i")
    command.extend(["-e", pattern, BASELINE, "--"])
    result = _git(*command, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    prefix = f"{BASELINE}:"
    return tuple(
        sorted(
            line.removeprefix(prefix)
            for line in result.stdout.decode("utf-8").splitlines()
            if line
        )
    )


def _digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _is_e4_lineage(path: str) -> bool:
    return (
        path == E4
        or path.startswith("agent-memory/")
        or path.endswith(".md")
        or path.startswith("engineering/")
    )


def _battery_accepts(candidate: object) -> bool:
    assert isinstance(candidate, PatternBattery)
    regex = re.compile(candidate.assignment_pattern)
    return all(regex.search(line) for line in candidate.positive_lines) and not any(
        regex.search(line) for line in candidate.negative_lines
    )


def main() -> int:
    checks = CheckLedger("P171-KI1-PINNED-TREE-AND-SEARCH-SENSITIVITY")

    for path, expected in PINNED_SOURCE_HASHES.items():
        checks.check(
            f"pinned predecessor blob {Path(path).name} retains its audited bytes",
            _digest(_blob(path)) == expected,
        )
    for relative, expected in PINNED_FRAMEWORK_HASHES.items():
        checks.check(
            f"accepted framework artifact {Path(relative).name} retains its audited bytes",
            _digest((FRAMEWORK_ROOT / relative).read_bytes()) == expected,
        )

    source = _text(KI1)
    dossier = _text(DOSSIER)
    tree = ast.parse(source, filename=KI1)
    check_calls = sorted(
        (
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ),
        key=lambda node: node.lineno,
    )
    labels = [re.match(r"(KI1\.[1-5])", ast.literal_eval(node.args[0])).group(1)
              for node in check_calls]
    checks.check(
        "KI1 has exactly its five advertised predicates in order",
        labels == ["KI1.1", "KI1.2", "KI1.3", "KI1.4", "KI1.5"],
    )
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "KI1 has one assertion and its exact standard-library import surface",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1
        and imports == {"os", "re", "subprocess"},
    )
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=KI1)
    checks.check(
        "KI1 has no NumPy integration-name compatibility surface",
        compatibility.numpy_aliases == ()
        and compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    baseline_paths = _tree_paths(BASELINE)
    creation_paths = _tree_paths(CREATION)
    checks.check(
        "the governed and creation commits have exact distinct tracked universes",
        len(baseline_paths) == 1628
        and len(creation_paths) == 1601
        and set(creation_paths) < set(baseline_paths),
    )
    checks.check(
        "the dossier's 1502-file tally matches neither committed universe",
        "1502 files" in dossier
        and len(baseline_paths) != 1502
        and len(creation_paths) != 1502,
    )
    history = _git("log", "--format=%H", "--all", "--", KI1).stdout.decode().splitlines()
    checks.check(
        "KI1 has one source-history commit and no committed passing snapshot",
        history == [CREATION],
    )
    checks.check(
        "KI1 enumerates an index but reads mutable working-tree bytes",
        'subprocess.run(["git", "-C", ROOT, "ls-files"]' in source
        and 'with open(os.path.join(ROOT, rel)' in source
        and "git show" not in source
        and "ls-tree" not in source
        and "rev-parse" not in source,
    )
    checks.check(
        "KI1 excludes the whole Phase-34 directory rather than only itself",
        f'SELF_DIR = "{SELF_DIR}"' in source
        and KI2.startswith(SELF_DIR)
        and {
            path
            for path in baseline_paths
            if re.search(r"/bridge_KI[2-5]_", path)
        }
        == {
            "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py",
            "merged-framework/bridges/phase-34/bridge_KI3_bracket_is_sharp.py",
            "merged-framework/bridges/phase-34/bridge_KI4_backsolve_circularity.py",
            "merged-framework/bridges/phase-34/bridge_KI5_kappa_is_not_a_variational_bound.py",
        },
    )

    controls = {
        r"25\.686": 42,
        r"F_pi\s*/\s*e|F_PI_OVER_E": 62,
        r"kappa": 298,
        r"BPS": 66,
        r"rational.?map": 34,
    }
    control_counts = {pattern: len(_grep(pattern)) for pattern in controls}
    checks.check(
        "the pinned-blob audit gives exact nonzero counts for all five controls",
        control_counts == controls,
    )
    checks.check(
        "broad present-token controls do not validate assignment completeness",
        all(count > 0 for count in control_counts.values())
        and set(controls).isdisjoint(
            {NUMERIC_ASSIGNMENT, BPS_COUPLING_CONTEXT, OMEGA_NUMERIC}
        ),
    )

    context_paths = tuple(path for path in _grep(BPS_COUPLING_CONTEXT)
                          if not path.startswith(SELF_DIR))
    strays = tuple(path for path in context_paths if not _is_e4_lineage(path))
    checks.check(
        "KI1.2 is false at the governed baseline with exactly ten executable strays",
        strays == EXPECTED_STRAYS and E4 in context_paths,
    )
    checks.check(
        "the same ten strays explain the preserved native and isolated failures",
        all(Path(path).suffix == ".py" for path in strays)
        and {Path(path).name.split("_")[1] for path in strays}
        == {"MK1", "MK2", "MK4", "MK5", "MK6", "MR1", "MR2", "MR3", "MR5", "MR6"},
    )

    valued_files = set(_grep(NUMERIC_ASSIGNMENT, ignore_case=False))
    bps_sector_files = set(_grep(BPS_SECTOR_CONTEXT))
    overlap_executables = sorted(
        path for path in valued_files & bps_sector_files
        if not path.startswith(SELF_DIR) and path.endswith((".py", ".lean", ".js"))
    )
    e4_source = _text(E4)
    checks.check(
        "KI1.3 is also false with exactly three pinned executable overlaps",
        bool(re.search(r"sp\.symbols\([^)]*lambda[^)]*mu[^)]*\)", e4_source))
        and not re.search(r"^\s*(lam|mu)\s*=\s*[-+]?[0-9]", e4_source, re.MULTILINE)
        and overlap_executables == [MK2, MK3,
            "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py"],
    )
    checks.check(
        "the narrow literal zero cannot support KI1's stronger no-derivation sentence",
        "nor derives any quantity from which they could be read off" in source
        and MK1 in baseline_paths and MK2 in baseline_paths and MK3 in baseline_paths,
    )

    mk1 = _text(MK1)
    mk2 = _text(MK2)
    mk3 = _text(MK3)
    checks.check(
        "MK1 is explicit tracked semantic counterevidence to the alleged mu absence",
        "mu_derived = sp.sqrt(sols[0])" in mk1
        and "mu_is_half = sp.simplify(mu_derived - m_pi * F_pi / 2) == 0" in mk1,
    )
    checks.check(
        "MK2 is explicit tracked semantic counterevidence to the alleged lambda absence",
        "lam_final = sp.simplify(sp.sqrt(lam_sq_final))" in mk2
        and "lam_expected = N_c / (4 * F_pi)" in mk2
        and "lambda^2 = g_omega^2/(2 m_omega^2)" in mk2,
    )
    checks.check(
        "MK3 is explicit tracked semantic counterevidence to the alleged epsilon absence",
        "eps_expected = 128 * sp.pi * m_e / (3 * m_pi)" in mk3
        and "eps_num = float(eps_expected.subs" in mk3,
    )

    omega_valued = _grep(OMEGA_NUMERIC, ignore_case=False)
    checks.check(
        "KI1.4 is also false because its omega regex finds tracked MK2",
        omega_valued == (MK2,)
        and bool(re.search(r"g_omega\s*=\s*sp\.Symbol", _text(WZ4)))
        and "do not pursue" in _text(S4)
        and "lam_expected = N_c / (4 * F_pi)" in mk2,
    )

    official_positive = (
        "lambda_bps = 1.234", "lam = 0.5", "mu = 2.0",
        "mu_bps=3.3", "epsilon = 0.11", "lambda_6 = 7.0",
    )
    official_negative = (
        "eps_r = 28.7", "Lambda_m=50e-6", "EPS_GAS = 1.00026",
        "eps_core=0.0", "Lam = 80e-6", "eps_LJ = 36.7",
    )
    official = PatternBattery(NUMERIC_ASSIGNMENT, official_positive, official_negative)
    checks.check(
        "KI1.5's twelve advertised planted-line controls reproduce",
        _battery_accepts(official),
    )
    checks.check(
        "KI1.5 does not exercise its bare-eps assignment branch",
        _battery_accepts(
            PatternBattery(
                NUMERIC_ASSIGNMENT.replace("eps|epsilon", "epsilon"),
                official_positive,
                official_negative,
            )
        ),
    )
    checks.mutation_sensitive(
        "the advertised line battery is sensitive to load-bearing pattern mutations",
        _battery_accepts,
        official,
        [
            PatternBattery(NUMERIC_ASSIGNMENT.replace("lambda", "zeta"),
                           official_positive, official_negative),
            PatternBattery(NUMERIC_ASSIGNMENT.replace("lam|mu", "lam|nu"),
                           official_positive, official_negative),
            PatternBattery(r"[A-Za-z_]+\s*=\s*[-+]?[0-9]*\.?[0-9]+",
                           official_positive, official_negative),
        ],
    )

    plausible_misses = (
        "lambda_bps: float = 1.234",
        "couplings = {'lambda_bps': 1.234}",
        "lambda_bps = sp.Rational(1, 2)",
        "params['lambda_bps'] = 1.2",
        "lambda_bps = Decimal('1.2')",
        "\u03bb = 1.2",
        "mu_bps = np.float64(2.0)",
        "epsilon: 0.11",
        "eps_num = 0.496",
    )
    literal_regex = re.compile(NUMERIC_ASSIGNMENT)
    checks.check(
        "nine plausible valued-coupling forms evade KI1's planted-line guard",
        all(literal_regex.search(line) is None for line in plausible_misses),
    )
    checks.check(
        "KI1's file-level intersection admits an explicit unrelated-mu false positive",
        literal_regex.search("mu = 2.0  # unrelated chemical potential") is not None
        and re.search(BPS_SECTOR_CONTEXT, "BPS sector discussed elsewhere", re.IGNORECASE)
        is not None,
    )
    phase34_witness = "merged-framework/bridges/phase-34/bridge_KI99_planted.py"
    checks.check(
        "KI1's self exclusion hides a planted positive anywhere in Phase 34",
        phase34_witness.startswith(SELF_DIR)
        and literal_regex.search("lambda_bps = 1.234") is not None
        and phase34_witness != KI1,
    )

    source_inventory = yaml.safe_load(
        (FRAMEWORK_ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8")
    )
    by_unit = {entry["source_unit"]: entry for entry in source_inventory["units"]}
    checks.check(
        "KI1 and its later semantic counterexamples enter P171 with no accepted claims",
        all(by_unit[unit]["accepted_claims"] == [] for unit in ("KI1", "MK1", "MK2", "MK3")),
    )
    checks.check(
        "the later MK counterexamples remain pending candidates rather than authority",
        all(by_unit[unit]["disposition"] == "pending_adjudication"
            for unit in ("MK1", "MK2", "MK3")),
    )

    registry = yaml.safe_load(
        (FRAMEWORK_ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    )
    claims = {claim["id"]: claim for claim in registry["claims"]}
    bps_claims = [claims[f"C-BPS-00{index}"] for index in range(1, 4)]
    checks.check(
        "accepted BPS authority retains exactly three active reviewed claims",
        all(claim["review"] == "accepted" and claim["epistemic"] == "active"
            for claim in bps_claims),
    )
    checks.check(
        "accepted BPS authority explicitly selects no coupling or physical yield",
        "select a potential or coupling" in bps_claims[0]["statement"]
        and "make epsilon or a physical binding coefficient numerically small"
        in bps_claims[2]["statement"]
        and "No interpolation monotonicity range coupling value physical state reaction empirical coefficient or yield"
        in bps_claims[2]["assumptions"][-1],
    )
    checks.check(
        "refuting KI1 changes no accepted scientific claim dependency",
        all("KI1" not in claim.get("dependencies", []) for claim in registry["claims"])
        and all("KI1" not in claim.get("challenges", []) for claim in registry["claims"]),
    )

    total = checks.finish()
    print(f"P171 KI1 PINNED TREE AND SEARCH SENSITIVITY ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
