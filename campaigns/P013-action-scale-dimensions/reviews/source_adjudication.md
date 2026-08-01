# Source adjudication: HE2 action-scale and Buckingham bridge

## Decision

HE2 is qualified. Its generic harmonic/rotor algebra maps to `C-ACT-001`, its
breather secant ratios map to `C-SG-006`, and its exact dimension kernels map to
`C-DIM-001`. The named medium-object identification and “permanent ceiling”
language exceed what HE2's local primitive-set calculation establishes.

## Check-family audit

HE2.1 and HE2.2 correctly compute the raw rotor contour and show that normalized
action is `I*omega`, while `E/omega=I*omega/2`. The source alternates between
`J` as raw contour and normalized action; `C-ACT-001` fixes the convention as
`(1/(2*pi))*closed_integral(p dq)`. HE2.3 is the harmonic linear-energy case.
HE2.4's “harmonic iff” is replaced by the exact general theorem: on a connected
positive-action interval, `E/E'=J` iff `E=CJ`.

HE2.5 and HE2.6 correctly find a zero kernel for the declared two-column
dimension matrix. `C-DIM-001` records exactly that result. Empty kernel means no
nontrivial dimensionless monomial can be formed from that primitive set; it does
not prove a permanent impossibility after new independent primitives or dynamics
are admitted.

HE2.7 and HE2.8 repeat the unit-invariant ratio and anchors already controlled
globally by `C-SG-006`. Their nonconstancy is exact, but calling it physical
content requires a physical interpretation beyond dimensional algebra.

HE2.9 and HE2.10 add an independent action primitive and correctly obtain the
one-dimensional kernel spanned by `(-1,1,1)`, representing `S*omega/E`.
This directly demonstrates why the earlier empty-kernel verdict is set-local,
not permanent. Setting `S` to the accepted breather action recovers C-SG-006's
ratio, but Buckingham analysis alone does not identify which action object is
physically supplied.

## Exact qualification

Accepted mappings are `C-ACT-001`, `C-DIM-001`, and `C-SG-006`. HE2 is
terminally qualified because its exact generic and dimensional content is now
represented, while the named `hbar_med` corpus identity, absolute-value
“permanent ceiling,” and physical measuring-unit interpretation are not derived
from HE2's accepted dependency closure.
