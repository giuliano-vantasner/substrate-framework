# P238 portable oracle companion

This directory preserves the complete independently written oracle corpus for
the peer review of Tiziano Fulceri's 19 August 2026 draft. It is deliberately
portable: a future author-maintained companion repository can take this subtree
without inheriting Substrate's claim registry or promotion decisions.

The programs test statements and counterexamples, not agreement with printed
outputs. A successful run means the audit predicates behaved as intended; it
does not mean that every paper claim passed. Claim dispositions live in
`../evidence/claim-results.yaml` and the prose review in `../reviews/peer-review.md`.

## Python oracles

From the Substrate repository root:

```bash
.venv/bin/python proposals/P238-nlkg-energy-lumps-peer-review/companion/sympy_checks.py
.venv/bin/python proposals/P238-nlkg-energy-lumps-peer-review/companion/scipy_checks.py
```

For a standalone checkout:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python sympy_checks.py
.venv/bin/python scipy_checks.py
```

## Lean oracle

Inside Substrate, reuse the pinned formal environment:

```bash
cd formal
lake env lean ../proposals/P238-nlkg-energy-lumps-peer-review/companion/P238PaperChecks.lean
```

The included `lean-toolchain` and `lakefile.lean` make the proof file portable
to a standalone repository. Run `lake update && lake build` there.

## Scope

The corpus retains positive identities, exact qualifications, counterexamples,
and numerical sign/domain probes for P238-S01 through P238-S18. Literature and
dependency-closure conclusions are documented alongside the machine oracles;
they are not disguised as numerical proofs.
