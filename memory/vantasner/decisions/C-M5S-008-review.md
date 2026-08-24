---
description: Individual claim review record for the P243 continuation batch
author: ox-alpha
created: '2026-08-23T23:20:00+00:00'
updated: '2026-08-23T23:20:00+00:00'
tags:
- substrate-framework
- decision
category: decisions
confidence: established
status: active
---

# C-M5S-008 review — np/nâ shear-channel verdict (corrected)

- claim: C-M5S-008 (numeric_evidence; corrected by review erratum
  0010 -> 0012) — long-range mediated interaction EXISTS, repulsive,
  E_int(d) = +456.6 * d^(-1.696).
- reviewer: distinct reviewer agent (RevC008), 2026-08-23, one substantive
  pass + correction checks at commits 19f1049 and 6299461.
- verification performed: reviewer derived independently (exact sympy) the
  exterior density of the committed three-pair functional,
  rho_ext = 8 sin^2(Theta)(grad Theta)^2 / (r^2 sin^2 theta_p), refuting
  attempt 0010's meridian-surrogate zero-density lemma at source; confirmed
  the committed conventions (cpu_energy.py L106-119 three commutator pairs
  incl. azimuthal channel normalized by 1/(r sin theta_p); pair_oracle.py
  L293 rotated director (st*sp, st*cp, ct)); verified all quoted numbers in
  the claim against artifacts; verified P240 0043 measured the repulsive
  power law at NON-overlapping separations d = 18..32 (> 2*R_box = 16),
  contradicting the original 'lives inside overlap' scope claim.
- blocking findings (both resolved): (1) surrogate lemma false under the
  committed construction — repaired by attempt 0012 (symbolic
  ||[B_n,A]||_F^2 = 2 sin^2(Theta); committed-functional reproduction to
  1.4e-11 relative at rho=12,z=3 matching the reviewer's own exact value;
  scan max 4.3e-03); (2) scope contradiction with the cited source —
  repaired by restating the boxed channel as a different observable class
  per C-M5S-005's accepted review.
- record repairs: C-M5S-008 registry entry rewritten wholesale (no
  superseded clause remains; verified programmatically), structural_gap
  states the two-channel result, erratum chain append-only, verification
  downgraded symbolic_verified -> numeric_evidence.
- final confirmation: "Accept per my original verdict's terms — promotion
  may proceed" (RevC008 @ 6299461).
- verdict: ACCEPTED. epistemic: active, accepted_in v0.165.0.

## Evidence roles

- attempts/0012/shear_channel_repair.py + shear-repair-verdict.json:
  exact_proof (symbolic identity) + regression (committed-functional
  reproduction) for the corrected verdict.
- proposals/P240-m5-kinetic-axis/attempts/0043/{result.yaml,pair_oracle.py}
  + attempts/0041/cpu_energy.py: provenance_only (committed conventions and
  the measured repulsive channel).
- attempts/0010/*: applicability only — superseded erratum history.
