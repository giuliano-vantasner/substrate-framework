# P236 self-adversarial audit (development record, pre-freeze)

Auditor: the proposing agent, against its own development record (the
REFUTE-first discipline of openwave AI_HYGIENE.md). Every finding below was
either repaired before the production run or is disclosed in the findings
note. The independent-audit companion is `independent-force-audit.md`.

## F1 — the two-center frame blend (REPAIRED)

The development two-center texture interpolated the two hedgehog FRAMES
(linear blend). Measured symptom: a non-decaying +O(1000) EM interaction
background with no clean 1/d in any sector; the pair-vs-single frame
mismatch fills the box. Root cause: a frame blend is not a solution of the
two-charge structure — the merged openwave construction superposes the
ANGLE field, not the frames. Repair: adopt the m5_17_two_charge.py
angle-superposition construction (Θ = θ₁ + q₂θ₂) verbatim in the biaxial
(1, δ, 0) form; the +O(1000) artifact disappears and the EM channel returns
the M5.17 Coulomb structure (like charges repel, +C_em/d).

## F2 — the boost-product composition (REPAIRED)

Composing per-center radial boosts as Q₁Q₂M₀Q₂ᵀQ₁ᵀ produced a non-decaying
EM artifact: composing non-aligned boosts generates rotations (the Wigner
channel), which the quartic curvature reads as large EM structure.
Repair: the additive shared field θ(x) = θ_clock(r₁) + θ_clock(r₂) on the
engine's single fixed boost axis (the seed_M class — the issue's own
object), i.e. the boost-angle superposition, the boost-channel analog of
the M5.17 tilt superposition.

## F3 — the LdG-well confinement artifact (REPAIRED)

Static relaxation of the boost dressing with the development amplitude well
(κ > 0) collapsed the dressing to the core: the well pins the undressed
trace t* and fights every boost. This produced the "no smooth decaying
mediator exists" development conclusion — an artifact of the added well,
not of the engine functional. Repair: κ = 0 (the N-3 record object
u + 1.558u²); the non-decaying branch reappears and settles at the M5.21.8
attractor band (0.10–0.11 vs the measured 0.10254).

## F4 — the scale-free oscillatory channel (GUARDED)

Unconstrained FIRE on the κ = 0 functional rides the known unbounded
oscillatory boost channel (M5.21.14 §4; M5.20.3): measured energy dives
with growing zigzag amplitude and forward/central blowup. Guard: band-limited
(sigma = 2 px) descent directions (the M5.8.2f doctrine), zigzag and
fwd/cen monitors recorded. The frozen-branch protocol avoids the channel
by construction (the tail is the engine-measured attractor profile).

## F5 — the fit window (REPAIRED)

Including separations out to 2(L − 4h) admits box-edge contamination and
degraded the fit (R² 0.84, exponent −2.5 at 48³ in one development run).
Repair: the mid-range window [4.1, 0.9L] with a disclosed small-box
extension to four points at 24³. A rounding mismatch between the stored
row separations and the unrounded window bounds dropped the last point
from the ladder fits; repaired by fitting on the stored values' own range.

## Residual honesty items (disclosed, not repaired)

- The forward-stencil twin's force exponent at 48³ deviates 0.116 from −2
  (pre-registered band 0.08): the one-sided quadrature's known overestimate
  of textured gradients dominates the exponent uncertainty; the sign, the
  1/d form, and R² survive (see the findings note § 5, G9 row).
- |C| still drifts +13% from 32³ to 48³ (window-bounded); the exponent is
  the converged quantity.
- The wiring dictionary's unit-identity (grid ↔ physical units) is out of
  scope by the issue text and not claimed.
