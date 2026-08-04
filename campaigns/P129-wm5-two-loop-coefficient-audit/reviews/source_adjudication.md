# WM5 Source Adjudication

WM5 contains a reusable exact core, but its strongest wording does not survive.
Given a separately supplied multiplet table, exact factor-wise Dynkin indices
and Casimirs, three copies of five Weyl multiplets, one complex scalar doublet,
the squared Abelian normalization `3/5`, and imported perturbative weights, the
one-loop vector and gauge-gauge two-loop matrix are exactly

`(41/10, -19/6, -7)` and
`[[199/50,27/10,44/5],[9/10,35/6,12],[11/10,9/2,-26]]`.

The source does not derive a physical field content. It executes WM1's supplied
tuple table and pending SM2/SM4 modules, infers only singlet/doublet/triplet
invariants from dimensions, and hard-codes the generation count, all group
invariants, counting conventions, and Abelian normalization. The named QCD,
SM3, WM2, and WM6 dependencies are not executable imports. Accepted C-REP-001
already withholds representation, chirality, completeness, anomaly-selection,
and gauge-action semantics from WM1's labels.

The arithmetic construction is independent of the comparator names, but the
source embeds the standard matrix first as `B_expected` in headline check 4 and
again as `B_LITERATURE` in check 5. The statement that the standard table is
used only after the headline is therefore inaccurate. Agreement remains useful
as a post-selection arithmetic comparison.

The matrix is gauge-only, not the full two-loop Standard Model gauge beta
function. Primary general formulas contain a Yukawa-dependent term at the same
loop order. Multiple Abelian factors additionally require kinetic-mixing
machinery. Thresholds, matching, boundary conditions, the perturbative domain,
and a physical embedding are outside this result. WM5's local percent ratios do
not by themselves prove WM6's integrated or all-orders claims.

C-RGE-005 accepts the narrower conditional theorem and its importable exact
ledger. It fixes the beta sign, powers of `16*pi^2`, Weyl and complex-scalar
counting, matrix orientation, at-most-one-U1 domain, omissions, and Abelian
coordinate covariance. A fresh reviewer independently enumerates the supplied
table and reproduces every coefficient without importing the canonical module.
Color, generation, scalar, counting, charge, and transpose mutations change the
verdict. WM5 is qualified through C-RGE-005, not promoted wholesale.
