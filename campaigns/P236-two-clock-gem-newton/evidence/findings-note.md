# M5.96 findings — relaxed two-clock GEM Newton limit

Campaign P236 · canonical issue #96 · corrected PR #101 transaction · public
engine `openwave-labs/openwave@614a223fff01b768550b0917d0f96621d6bbe155`.
The drop-in driver uses canonical `sandbox_v8`/`sandbox_vn` imports. Every PR
commit carries its author's DCO `Signed-off-by` trailer.

## Result

For two driven M5.8 fixed-clock configurations, with the one shared GEM
rapidity independently relaxed at every separation and lattice rung,

```text
U_gem(d) = U_inf + C/d,       C < 0,
F(d_i+1/2) = -[U(d_i+1)-U(d_i)]/[d_i+1-d_i] < 0,
F(d) proportional to d^p,    p = -2 within the declared numerical band.
```

The exponent is measured from direct differences of the raw energy rows. It
does not use `U_inf` or a forced `1/d` residual.

### Growing-box ladder

| lattice | half-domain D | C | R² | direct force exponent |
| --- | ---: | ---: | ---: | ---: |
| 24³ | 96 | -123.0796 | 0.999995 | **-2.03198** |
| 32³ | 108 | -124.9993 | 0.999983 | **-2.04361** |
| 48³ | 120 | -123.9048 | 0.999954 | **-2.06018** |

The coefficient spread is 1.55% and the exponent spread is 0.0282.

### Fixed-domain grid refinement

| lattice | half-domain D | C | R² | direct force exponent |
| --- | ---: | ---: | ---: | ---: |
| 24³ | 120 | -118.3186 | 0.999988 | **-2.04403** |
| 32³ | 120 | -123.8231 | 0.999981 | **-2.04661** |
| 48³ | 120 | -123.9048 | 0.999954 | **-2.06018** |

From 32³ to 48³, `C` changes by 0.066% and the exponent by 0.0136. On every
rung, the `1/d` energy RMSE is more than 20 times smaller than the logarithmic
alternative and more than 40 times smaller than the linear alternative.

## Equations and construction

The M5.8 engine supplies

```text
F_ij = [partial_i M, partial_j M]
u_EM  = +4 sum_(i<j) sum_spatial (F_ij)^2
u_GEM = -4 sum_(i<j) sum_time-mixing (F_ij)^2
u = u_EM + u_GEM
H_static = integral [u + 1.558 u^2] d^3x
M = O4 B(a,A_BOOST) diag(8,1,0.3,0) B(a,A_BOOST)^T O4^T.
```

For cores `z1=-d/2`, `z2=d/2`, the corrected M5.17 frame is

```text
Theta = atan2(rho,z-z1) + atan2(rho,z-z2)
e_r = (sin Theta cos phi, sin Theta sin phi, cos Theta)
e_phi = (-sin phi, cos phi, 0)
e_Theta = e_phi cross e_r
O4 = diag(1, [e_r e_Theta e_phi]).
```

This is orthogonal to `8.88e-16`; setting the second charge to zero reproduces
the single-source matrix exactly. The submitted non-orthogonal frame and its
core melt are not used.

There is one ambient rapidity, not a sum of two nondecaying tails:

```text
w_i = exp[-(r_i/R_W)^2],       R_W=3.5, B_STAR=0.13
a(x) = a + (B_STAR-a) w_1
           + (B_STAR-a) w_2 (1-w_1).
```

At each `(n,D,d)`, the bounded scalar `a in (0,0.3)` is minimized on the
same composite Gauss-Legendre `n^3` lattice later used for the observable.
Every minimum is interior, has positive curvature, and has `|dH/da|<0.005`.
This is the canonical M5.21.8 rigid family. It obeys M5.21.14's mandatory
guard: unrestricted full-field minimization is forbidden because the signed
static functional has a scale-free negative UV channel; constrained smooth
profiles are the upstream-authorized object.

The interaction is local before it is global:

```text
u_int(x;d) = u_pair(x;d) - u_single,1(x;d) - u_single,2(x;d)
U_gem(d) = integral_common_pair_mask u_int,GEM(x;d) d^3x.
```

Using the common pair mask removes core-mask and far-background mismatches.
The pointwise matrix derivatives use a central epsilon of `2e-4`; varying it
from `1e-4` to `1e-3` changes the checked GEM value by less than one part per
million.

## Equation-to-code map

| Object | Production code |
| --- | --- |
| M5.8 matrix and signed sectors | `M_of`, `sector_density`, `pair_total` |
| orthogonal M5.17 frame | `orthogonal_frame` |
| one shared rapidity and two pinned cores | `matrix_field` |
| exact n³ composite lattice | `composite_nodes`, `lattice` |
| guarded relaxation | `relax_pair` |
| pointwise interaction subtraction | `interaction` |
| raw force and hostile model comparison | `summarize` |
| independent cylindrical reconstruction | `reviews/independent_force_audit.py` |
| accepted #89 bridge | `verify.py` using `total_gravitational_coupling` |

## C-IGR-004 / C-GRV-002 bridge

C-IGR-004 is used exactly as accepted. On the declared purely induced,
massless, minimally coupled branch,

```text
B=0, N=1, xi=0, z=0,
1/G_total = Lambda^2/(12 pi),
G_total = 12 pi/Lambda^2.
```

Sharp and smooth proper-time schemes agree because `J(0)=1`. `Lambda` remains
an exact positive symbol: C-IGR-004 explicitly does not choose a regulator,
cutoff value, or unique numerical normalization. The former `Lambda=pi/h`
substitution is removed.

The type bridge keeps the raw M5 action normalization distinct from the
Newton coefficient. Let

```text
Z_GEM = |C_48| = 123.9048063
K(d) = [U_gem(d)-U_inf]/Z_GEM = -1/d + discretization residual.
```

`K` is the unit-source Green kernel; the coupled energy is

```text
U_N(d) = G_total m1 m2 K(d) = -G_total m1 m2/d + residual.
```

Thus `G_total`, not a raw lattice coefficient, is the coefficient of the
normalized kernel. The magnitude oracle is independent: the cylindrical
pipeline measures `Z_GEM=118.3291126`, 4.50% below the primary value, inside
the frozen 6% band. C-GRV-002 gives an attractive total for `xi<1/6` on the
purely induced branch; its sign matches every measured `F<0`. No accepted
claim or registry statement changes.

## Controls

| Control | Frozen gate | Result |
| --- | --- | --- |
| N-3 anchor | `H_static=16.7379 +/- 0.05` | 16.7379188, pass |
| frame | orthogonal and exact single limit | `8.88e-16`, `0`, pass |
| zero boost | GEM exactly zero | `0.0` at d=24,48,72, pass |
| source deletion | collapse >10 and exponent shift >0.5 | 16.52x; exponent -3.0867, pass |
| growing box | `C` spread <3%, exponent spread <0.04 | 1.55%, 0.0282, pass |
| fixed-domain grid | last `C` change <1%, exponent change <0.02 | 0.066%, 0.0136, pass |
| derivative epsilon | relative spread <1 ppm | pass |
| independent pipeline | exponent within 0.1 of -2; C within 6% | -2.02037; 4.50%, pass |

The source-deletion mutation removes clock 2's texture while leaving the two
clock-core locations in the relaxation problem. Its peak force falls from
`0.16091` to `0.009739`, and its exponent becomes `-3.0867`. This tests the
load-bearing two-source texture rather than merely changing a summary value.

## Independent REFUTE audit

The independent script imports no production function. It reconstructs the
field directly on a uniform cylindrical lattice (`D=120`, `h=0.75`), uses
`d/drho`, `(1/rho)d/dphi`, and `d/dz`, integrates with `2*pi*rho`, and derives
its own raw force and models. Its results are

```text
C = -118.3291126
force exponent = -2.0203675
RMSE(1/d) = 0.000329
RMSE(log d) = 0.171363
RMSE(linear) = 0.335248.
```

All five preregistered REFUTE doors pass: attraction, inverse-square
exponent, independent magnitude, independent exponent, and hostile model
selection. The audit record is `m5_96_independent_audit.json`.

## Scope and honesty boundary

The positive result is for the driven M5.8 fixed-clock class explicitly
requested by issue #96. It is not a claim about nonexistent free-period
M5.12 solutions. The issue explicitly leaves the OpenWave MODELS.md edit and
OpenWave PR for a separate later step; neither is part of this campaign.
Within issue #96's requested boundary, the correction leaves no unresolved
assumption, promised validation, or affected consumer.
