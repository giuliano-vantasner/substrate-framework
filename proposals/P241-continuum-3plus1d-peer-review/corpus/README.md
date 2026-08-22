# P241 Companion Corpus — Independent Review Oracles

Standalone validation corpus for the peer review of
*2026-08-21_continuum_dynamics_3plus1D_solitonic_matter_equivalence_principle_v1.0*
(SHA-256 `dc23cbd9…`). No substrate-framework imports; every module runs on
its own.

## Layout

    checks/sympy/     21 per-claim exact-audit modules (S*.py) + run_sympy.py
    checks/scipy/      5 numerical modules (N*.py) + run_scipy.py + _numerics.py
    replacements/      10 corrected-statement records (records.py)
    lean/              P241PaperChecks.lean, P241ReplacementProofs.lean
                       (mathlib v4.28.0, lakefile + toolchain pin)

## Running

    python3 checks/run_sympy.py        # exact audits; JSON report
    python3 checks/run_scipy.py        # numerical audits; JSON report
    python3 replacements/records.py    # replacement-record consistency
    cd lean && lake build && lake env lean P241PaperChecks.lean && \
        lake env lean P241ReplacementProofs.lean

Or run the whole boundary: `python3 ../verify.py`.

## Environment

    numpy >= 1.22 (2.x-compatible trapezoid fallback included)
    scipy >= 1.14, sympy == 1.14, pyyaml
    Lean: leanprover/lean4:v4.28.0 + mathlib v4.28.0

## Conventions

* Each check module prints one JSON record `{name, claim, passed, detail}`
  and exits nonzero on failure.
* Counterexamples are stated as positive theorems: proving a displayed
  equation wrong is a verified review result.
* Numerical protocols declare domain, discretization, CFL, tolerances, and
  pass thresholds up front (see each module docstring).
