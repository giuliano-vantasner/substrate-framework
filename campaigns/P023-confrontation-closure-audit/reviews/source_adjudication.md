# Source adjudication: EL6 confrontation closure

## Decision

EL6 is qualified. Its symbolic derived-side expression is an exact
specialization of `C-DIM-005`, and its conditional ratio maps to `C-SK-001`.
Its comparator arithmetic is preserved as evidence. It does not independently
fix the length, shape, coupling data, or hadronic offset and therefore does not
predict an electron mass or discharge inherited framework debt.

## Check-family audit

EL6.1 correctly inventories six free symbols. “Pre-existing” is provenance, not
derivation: `a`, `b(1)`, `b0`, `beta^2`, and `kappa_h` are not all accepted fixed
inputs. Normalization gives `C-DIM-005` with
`q=kappa_h/(48*pi^3*b(1))`; no new theorem remains.

EL6.2 and EL6.3 reproduce stated comparator arithmetic. The close massless-model
ratio and worse generalized value are empirical evidence conditional on source
models not accepted in this campaign. Numerical closeness cannot promote them.

EL6.4 scans only direct `Assign` nodes whose values are numeric literals. It
misses annotated assignments, constructor calls, aliases, and other equivalent
ways to set a numeric scale. More importantly, finding no assignment does not
derive a value for `a`; it confirms the absolute prediction is unclosed.

EL6.5 imports Planck length, conversion constants, an AS7 coupling value, and
measured masses in its comparator block. It then solves `kappa_h` from measured
electron mass. Agreement between that required offset and a proton-derived
offset is the same conditional ratio comparison, not a no-hadronic-input scale
prediction from accepted premises.

EL6.6 seeds the restricted namespace with the comparator-derived `kappa_h` and
then reconstructs the comparator. The namespace guard correctly rejects a
seventh name but cannot distinguish calibration from prediction; exact inverse
composition proves the reconstruction is tautological once `kappa_h` is set.

EL6.7 is a narrow lexical fact about the other phase-46 files. It does not audit
symbolic offsets, equivalent values, earlier dependency files, or semantic
imports.

EL6.8 proves only that the expression's symbols belong to a declared set and do
not include `m_e`. Removing a symbol name while retaining free `a`, `b(1)`, and
`kappa_h` does not remove physical information. Under the framework contract,
inherited unresolved inputs remain debt until resolved; provenance age does not
make the ledger empty.

## Exact qualification

EL6 adds no distinct accepted claim. Its forward and inverse formulas duplicate
`C-DIM-003`, `C-DIM-005`, and conditional `C-SK-001`; the measured comparisons
remain noncanonical evidence. Absolute mass, particle identity, parameter
closure, and empty-debt conclusions are not established.
