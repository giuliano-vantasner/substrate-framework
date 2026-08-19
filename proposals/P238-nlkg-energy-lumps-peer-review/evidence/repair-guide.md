# P238 author-ready repairs

This guide turns every “revision required” finding into replacement text,
mathematics, or executable evidence. It preserves the manuscript's intended
program: a real 2+1D nonlinear field supplies localized energy, an adiabatic
collective coordinate supplies particle motion, and constitutive/flow data
supply an effective geometry. The changes narrow unsupported universality,
make missing hypotheses explicit, or replace incorrect algebra; novelty is not
a review criterion.

The replacement code is self-contained in `../companion/`. It was built by
adapting the repository's exact scattering, collective-coordinate, boosted
breather, metric-inverse, geodesic, and radial-evolution primitives into the
paper's variables and dimension. Those repository primitives are incorporated
into the replacement solutions; they are not used as external evidence that a
paper claim passes or fails.

## Replacement map

| Claim | Author-ready resolution | Replacement evidence |
| --- | --- | --- |
| S01 | Replace “most general” with: “Within local, first-derivative, quadratic, time-reversal-even scalar models with prescribed scalar density, SPD stiffness, flow entering only through `D_t u`, and no derivative/potential cross-couplings, we take equation (2).” | Exact expansion remains in `sympy_checks.py` and `P238PaperChecks.lean`. |
| S02 | Replace the constant-background sentence with: “The full linearized equation is `D_t^2 u-c0^2 Laplacian(u)+U''(0)u/rho0=0`; its principal part is the convective wave operator.” | `sympy_replacements.py`, replacement 1. |
| S03 | Retain `rho sqrt(det Theta)=constant` as a constitutive normalization. Replace general reflectionlessness with: “For an interface normal `n`, scalar normal-incidence reflection vanishes when `rho_L(n^T Theta_L n)=rho_R(n^T Theta_R n)`.” | `sympy_replacements.py`, replacement 2, gives `R=0` exactly. |
| S05 | Replace the ordinary tensor quadratic form by `n_phase(khat)=c0/sqrt(khat^T A khat)`. Keep the eigenvalues of `N=c0 A^(-1/2)` as principal indices. | `sympy_replacements.py`, replacement 3. |
| S06 | Replace the all-potential theorem claim with the scoped computational claim: “For `U=1-cos u` and the declared Gaussian data, a real radial 2+1D trajectory remains localized through `t=30`.” State that this is finite-time evidence, not an eternal breather theorem. | `scipy_replacements.py`: leapfrog and DOP853 agree; spatial refinement passes; late core-energy fractions exceed 0.90. |
| S07 | Tie the hypothesis to the S06 family: “For that localized family, the collective-coordinate approximation is assumed when `ell/L << 1`; conclusions below are conditional until the substituted residual and internal-mode error are bounded.” | The S06 numerical file supplies the concrete family; the residual/error bound remains an explicitly named next derivation rather than a hidden premise. |
| S08 | Replace the rigid-profile inference with: “If the explicit localized family is closed under boosts with `E=gamma E0` and `p=gamma E0 v/c0^2`, then `L=pv-E=-E0/gamma`.” The inhomogeneous extension remains adiabatic. | `sympy_replacements.py`, replacement 4, and `P238ReplacementProofs.lean`, `boostedFamilyLegendreTransform`. |
| S11 | Replace equations (33)–(38) by `nbar^(-1)[[-1+v^T N^2 v,-v^T N^2],[-N^2 v,N^2]]`, where `v=V/c0`. | `sympy_replacements.py`, replacement 5; `P238ReplacementProofs.lean`, four exact inverse-entry theorems. |
| S12 | Scope massive-lump clocks, rulers, and free fall to the S06/S08 assumptions. The wave-ray metric remains exact; massive conclusions become conditional on the explicit boosted-family/adiabatic residual. | S08 replacement plus the independently derived einbein/null/geodesic checks in `sympy_checks.py` and both Lean files. |
| S15 | Replace the coefficient map by the exact ADM/acoustic decomposition of equatorial Kerr given below; it uses the corrected S11 inverse. | `sympy_replacements.py`, replacements 6 and 8; Kerr coefficient theorems in `P238ReplacementProofs.lean`. |
| S16 | For an exact result, replace the minimal profiles by `Delta=r^2-rs*r+a^2`, `G=r^2+a^2+a^2 rs/r`, `Omega^2=Delta/G`, `h_rr=r^2 G/Delta^2`, `h_phiphi=G^2/Delta`, and `V^phi/c0=a rs/(rG)`. Then `Omega^2 g_acoustic=g_Kerr` coefficient by coefficient, and the supplied physical-frame `rho`, `Theta_r`, and `Theta_t` satisfy determinant matching. Alternatively retain the original profiles but call them a minimal rotating acoustic model rather than Kerr. | `sympy_replacements.py`, replacements 6–8, and `P238ReplacementProofs.lean`. |
| S17 | Replace the root sentence with: “The lower/counter-rotating root changes from negative outside the ergoregion to positive inside; the upper/co-rotating root remains positive for the displayed orientation.” | Exact surface equations in `sympy_checks.py`; independent sign sampling in `scipy_checks.py`. |
| S18 | Replace the headline with: “The paper constructs exact wave-principal-symbol and exterior Schwarzschild analogue geometry; a scoped real-lump realization is supplied numerically, while the inhomogeneous massive collective-coordinate error bound remains to be completed.” | All four companion oracle/replacement programs and both Lean files. |

## Exact conformal Kerr replacement

In equatorial Boyer–Lindquist coordinates define

```text
Delta = r^2-rs*r+a^2
G = r^2+a^2+a^2*rs/r
Omega^2 = Delta/G
h_rr = r^2*G/Delta^2
h_phiphi = G^2/Delta
v^r = 0
v^phi = a*rs/(r*G)
```

Use the corrected acoustic block form

```text
g_acoustic = [ -1+v^T h v   -v^T h ]
             [    -h v          h   ].
```

Then `Omega^2*g_acoustic` equals the equatorial Kerr metric exactly. At `a=0`
the construction reduces to the supported Schwarzschild acoustic profiles.
The determinant-matched physical constitutive profiles are

```text
rho/rho0 = (G/Delta)^(3/4)
Theta_r/Theta0 = Delta^(5/4)/(r^2*G^(1/4))
Theta_t/Theta0 = r^2*Delta^(1/4)/G^(5/4).
```

The exterior domain requires `Delta>0` and `G>0`.
