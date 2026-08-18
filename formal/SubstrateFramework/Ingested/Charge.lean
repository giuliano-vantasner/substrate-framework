/-
Half‑line topological charge dynamics and fermion parity.

This file re-exports the canonical charge and fermion-parity
definitions and theorems from `formalization.Formalization`.  It
is kept as a separate module so that pre-bridge charge/parity
investigations (rung27, rung28) and post-bridge dynamics work can
refer to the same statements under the historical name `Charge.lean`.

CANONICAL DEFINITIONS LIVE IN `formalization/Formalization.lean`:
  - `halfLineCharge`
  - `halfLineCharge_deriv_eq_neg_phi_t_div_2pi`
  - `fermionParity`
  - `fermionParity_sq_eq_one`
  - `fermionParity_zero`
  - `fermionParity_one`
  - `fermionParity_neg_one`

Pre-R6, both this file and `Formalization.lean` declared these
theorems separately, leading to duplication: the same statement was
audited twice (in `audits/20260615T160315479Z/` for Formalization and
`audits/20260615T162157670Z/` for Charge), inflating the headline
count.  R6 (2026-06-15 17:30Z) collapses Charge.lean to an import
shim; the audits now apply to the single canonical source.

Note: `dynamics_lean/ChargeDiscrimination.lean` also re-declares
`fermionParity` for self-contained compilation; that duplication
remains a separate issue (R6 ledger).

If you import `formalization.Charge`, you get the same theorems as
importing `formalization.Formalization`.  No mathematical content
has changed.
-/

import Mathlib
import SubstrateFramework.Ingested.Formalization
namespace SGCharge

open SGFormalization

end SGCharge
