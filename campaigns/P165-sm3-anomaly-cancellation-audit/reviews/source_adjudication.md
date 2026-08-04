# P165 SM3 Source Adjudication

## Decision

SM3 is qualified. Its supplied left-handed five-row table gives exact zeroes
for the four displayed Abelian/gravitational local coefficients, the supplied
SU3 cubic balance, and the supplied fundamental-SU2 doublet parity. Its two
coordinate mutations and common-rescaling check are also correct as local
facts. They do not establish the headline that anomaly freedom uniquely forces
the displayed hypercharge ratios up to scale.

## Source Predicates

SM3.1 through SM3.4 are exact conditional coefficient evaluations under
explicitly imported four-dimensional chiral anomaly criteria. SM3.5 is a valid
four-fundamental-doublet parity evaluation, not a generic higher-SU2-
representation classifier. SM3.6 is valid after interpreting the supplied
signed integer as a fundamental/antifundamental cubic anomaly coefficient, not
as a derivation from representation dimension. SM3.7 proves only that two
chosen coordinate directions leave the zero set. SM3.8 proves homogeneous
common rescaling of a zero point, while its “one true freedom” prose is false.

All eight assertions execute natively and the terminal tally is genuine. The
tally is regression evidence for those predicates, not a uniqueness oracle.

## Complete Exact Solution

For charges `(q,u,d,l,e)` on the fixed rows `(Q_L,u_R^c,d_R^c,L,e_R^c)`, zero
mixed-SU3, mixed-SU2, mixed-gravity, and cubic-U1 coefficients are equivalent,
up to harmless nonzero normalizations of the first two equations, to

```text
2q + u + d = 0
3q + l = 0
6q + 3u + 3d + 2l + e = 0
6q^3 + 3u^3 + 3d^3 + 2l^3 + e^3 = 0.
```

Linear elimination gives `l=-3q`, `e=6q`, and `d=-2q-u`. The remaining
polynomial factors exactly as

```text
18 q (2q-u) (4q+u).
```

The complete real affine zero set is therefore the union of three lines:

```text
(q,u,d,l,e) = t (1,-4, 2,-3,6)   displayed line
(q,u,d,l,e) = t (1, 2,-4,-3,6)   row-exchanged line
(q,u,d,l,e) = t (0, 1,-1, 0,0)   vectorlike line.
```

The source point is the first line at `t=1/6`. The other two lines are exact
counterexamples to uniqueness up to common scale with fixed row labels. The
origin is their common intersection. The charge-independent SU3 cubic balance
and four-doublet parity hold on every line and therefore select none of them.

## Positive Object

`src/substrate_framework/chiral_anomalies.py` adds a pure exact ledger for a
separately supplied `G_a x SU(2) x U(1)` chiral table. It evaluates the two
mixed non-Abelian/Abelian coefficients, cubic U1, mixed gravitational U1,
signed `G_a^3`, and supplied fundamental-doublet parity. It also maps charge
conjugation, specializes the fixed five-row carrier, returns all three solution
lines, and classifies exact points. Marked fundamental doublets must have
dimension two; higher-SU2-representation global anomaly classification is
explicitly outside the API.

## Independence and Sensitivity

The primary route passes 25 checks. The independent route imports no P165
anomaly API and separately performs linear solving, a Gröbner-basis check,
factorization, three parameter substitutions, and exact finite-grid equality
with the bounded branch union; it passes 12 checks. Electron-charge removal,
wrong cubic conjugation sign, removal of a fundamental doublet, common scaling,
row exchange, the zero-q branch, and neutral-singlet extension are load-bearing
mutations or scope counterexamples.

## Provenance and Boundaries

The quantum anomaly conditions are explicit external theory pinned in the
literature audit. C-REP-001 and C-REP-003 supply exact finite-table,
normalization, conjugation, and incompleteness boundaries. C-REP-002 and
C-LIE-001 supply the fixed Pauli-half and Gell-Mann-half fundamental
normalizations. P165 derives the sums and complete solution set, not the
external quantum theorem or the carrier.

No physical Standard Model generation, observed charge table, unique
hypercharge assignment, Yukawa or scalar constraint, representation
completeness, global U1 period, charge lattice, global gauge group,
renormalizability, unitarity, general-covariance theorem, coupling value,
running, or substrate mechanism is promoted.

## Consumers and Compatibility

The fifteen-node source graph replays 132 lexical and 132 runtime predicates
plus fifteen assertions; every node is native and has no legacy NumPy
integration reference. Downstream scripts retype or reuse supplied tables or
cite SM3 in prose. Existing accepted claims already qualify those surfaces and
do not depend on the rejected uniqueness inference. GitNexus rates the additive
API LOW risk with one internal caller and no affected execution flow.

## Four-Axis Disposition

- Verification: symbolic verified for the exact ledger and solution variety.
- Review: claim-level acceptance proposed for C-ANO-001; source qualified.
- Compatibility: compatible extension.
- Epistemic: active exact conditional mathematics; physical readings excluded.

The debt ledger is ready for governance synchronization and the terminal gate.
