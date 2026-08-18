"""Internal-consistency tests for the ingested historical Lean corpus.

The external source tree (/home/dan/substrate @ 6d1f4e0) is required only for
the provenance-digest test, which skips gracefully when that tree is absent
(e.g. on a clean CI checkout).  Everything else is repository-internal.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
INGESTED = ROOT / "formal/SubstrateFramework/Ingested"
UMBRELLA = ROOT / "formal/SubstrateFramework/Ingested.lean"
AUDIT = ROOT / "formal/Audit.lean"
PROVENANCE = INGESTED / "provenance.yaml"
SOURCE_REPO = Path("/home/dan/substrate")

ESCAPE_RE = re.compile(r"\b(sorry|admit|axiom|unsafe)\b")
DOC_RE = re.compile(r"/-!.*?-/|/-.*?-/", re.S)


def _manifest() -> dict:
    return yaml.safe_load(PROVENANCE.read_text())


def _lean_files() -> list[Path]:
    return sorted(p for p in INGESTED.glob("*.lean"))


def _strip_comments(text: str) -> str:
    out = DOC_RE.sub("", text)
    out = re.sub(r"/--.*?--/", "", out, flags=re.S)
    out = re.sub(r"(?m)^[ \t]*--.*$", "", out)
    return out


def test_manifest_covers_every_file_exactly() -> None:
    manifest = _manifest()
    listed = {entry["file"] for entry in manifest["files"]}
    on_disk = {p.name for p in _lean_files()}
    assert listed == on_disk
    assert len(manifest["files"]) == len(listed)
    assert manifest["source_commit"] == "6d1f4e0"
    assert manifest["source_repository"] == "/home/dan/substrate"


def test_manifest_entry_schema() -> None:
    required = {"file", "family", "source", "sha256_source", "theorems", "main_theorem", "adaptations"}
    families = {"bridges", "comparsi", "dynamics_lean", "formalization"}
    for entry in _manifest()["files"]:
        missing = required - entry.keys()
        assert not missing, (entry.get("file"), missing)
        assert entry["family"] in families
        assert entry["source"].startswith("/")
        assert re.fullmatch(r"[0-9a-f]{64}", entry["sha256_source"])
        assert isinstance(entry["theorems"], int) and entry["theorems"] >= 0
        assert isinstance(entry["adaptations"], list)


def test_no_proof_escapes_in_ingested_corpus() -> None:
    for path in [ROOT / "formal/SubstrateFramework.lean", *INGESTED.rglob("*.lean")]:
        assert not ESCAPE_RE.search(path.read_text()), path


def test_every_ingested_file_declares_a_namespace() -> None:
    # Uniform policy: root-level declarations are forbidden so future
    # ingestions cannot silently rely on lucky name uniqueness.
    for path in _lean_files():
        assert re.search(r"^\s*namespace\s+\S+", path.read_text(), re.M), path


def test_no_cross_file_fully_qualified_name_collisions() -> None:
    seen: dict[str, str] = {}
    for path in _lean_files():
        stack: list[str] = []
        for line in path.read_text().splitlines():
            ns = re.match(r"\s*namespace\s+(\S+)", line)
            end = re.match(r"\s*end\s+(\S+)?", line)
            decl = re.match(r"\s*(?:theorem|def|lemma|structure|abbrev|instance)\s+(\w+)", line)
            if ns:
                stack.append(ns.group(1))
            elif end and stack:
                if end.group(1):
                    while stack and stack[-1] != end.group(1):
                        stack.pop()
                    if stack:
                        stack.pop()
                else:
                    stack.pop()
            elif decl:
                fqn = ".".join([*stack, decl.group(1)])
                if fqn in seen and seen[fqn] != path.name:
                    raise AssertionError(f"{fqn} declared in both {seen[fqn]} and {path.name}")
                seen[fqn] = path.name


def test_umbrella_imports_exactly_the_corpus() -> None:
    text = UMBRELLA.read_text()
    imports = set(re.findall(r"^import (SubstrateFramework\.Ingested\.\S+)$", text, re.M))
    expected = {f"SubstrateFramework.Ingested.{p.stem}" for p in _lean_files()}
    assert imports == expected
    # the library root must pull the umbrella in
    root_mod = (ROOT / "formal/SubstrateFramework.lean").read_text()
    assert "import SubstrateFramework.Ingested" in root_mod


def test_audit_covers_every_main_theorem() -> None:
    audit = AUDIT.read_text()
    prints = re.findall(r"^#print axioms (\S+)", audit, re.M)
    assert "SubstrateFramework.compose_implications" in prints
    mains = {e["main_theorem"] for e in _manifest()["files"] if not e["main_theorem"].startswith("none")}
    assert mains <= set(prints)
    # one annotation per audited file
    for entry in _manifest()["files"]:
        if not entry["main_theorem"].startswith("none"):
            assert any(l.endswith(f"-- {entry['file']}") for l in audit.splitlines()), entry["file"]


def test_main_theorem_names_resolve_in_file() -> None:
    for entry in _manifest()["files"]:
        if entry["main_theorem"].startswith("none"):
            continue
        path = INGESTED / entry["file"]
        code = _strip_comments(path.read_text())
        local = entry["main_theorem"].split(".")[-1]
        assert re.search(rf"^\s*theorem\s+{re.escape(local)}\b", code, re.M), entry["file"]


def test_recorded_adaptations_match_file_content() -> None:
    for entry in _manifest()["files"]:
        text = (INGESTED / entry["file"]).read_text()
        for adaptation in entry["adaptations"]:
            if adaptation.startswith("namespace wrap:"):
                ns = re.search(r"`namespace (\S+)`", adaptation).group(1)
                assert re.search(rf"^namespace {re.escape(ns)}$", text, re.M), entry["file"]
            if adaptation.startswith("open declaration:"):
                ns = re.search(r"`open (\S+)`", adaptation).group(1)
                assert re.search(rf"^open {re.escape(ns)}$", text, re.M), entry["file"]


@pytest.mark.skipif(not SOURCE_REPO.exists(), reason="historical source tree not present")
def test_provenance_digests_match_sources() -> None:
    checked = 0
    for entry in _manifest()["files"]:
        source = SOURCE_REPO / entry["source"].lstrip("/")
        assert source.exists(), source
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        assert digest == entry["sha256_source"], entry["file"]
        checked += 1
    assert checked == 60


@pytest.mark.skipif(not SOURCE_REPO.exists(), reason="historical source tree not present")
def test_verbatim_files_are_byte_identical() -> None:
    for entry in _manifest()["files"]:
        if entry["adaptations"]:
            continue
        source = SOURCE_REPO / entry["source"].lstrip("/")
        assert (INGESTED / entry["file"]).read_bytes() == source.read_bytes(), entry["file"]


@pytest.mark.skipif(not SOURCE_REPO.exists(), reason="historical source tree not present")
def test_statements_and_proofs_are_unchanged() -> None:
    """Stronger than a diff filter: after removing exactly the adaptation
    surfaces (comments, imports, namespace/open/end lines, blank lines), the
    source and the ingested file must be token-for-token identical, so every
    theorem statement and proof body is provably untouched."""
    def normalize(text: str) -> list[str]:
        out = DOC_RE.sub("", text)
        out = re.sub(r"/--.*?--/", "", out, flags=re.S)
        out = re.sub(r"(?m)^[ \t]*--.*$", "", out)
        kept = []
        for line in out.splitlines():
            s = line.strip()
            if not s:
                continue
            if re.match(r"(?:import|namespace|open)\s", s) or re.match(r"end(?:\s|$)", s):
                continue
            kept.append(s)
        return kept

    compared = 0
    for entry in _manifest()["files"]:
        source = (SOURCE_REPO / entry["source"].lstrip("/")).read_text()
        current = (INGESTED / entry["file"]).read_text()
        assert normalize(source) == normalize(current), entry["file"]
        compared += 1
    assert compared == 60
