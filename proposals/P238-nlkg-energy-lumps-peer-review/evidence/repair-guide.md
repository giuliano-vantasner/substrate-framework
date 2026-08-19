# P238 author-ready repairs

This guide turns every “revision required” finding into replacement text,
mathematics, or executable evidence. It preserves the manuscript's intended
program: a real 2+1D nonlinear field supplies localized energy, an adiabatic
collective coordinate supplies particle motion, and constitutive/flow data
supply an effective geometry. The changes narrow unsupported universality,
make missing hypotheses explicit, or replace incorrect algebra; novelty is not
a review criterion.

The replacement code is self-contained in `../companion/`, and every one of
the 13 revision findings is covered by an executable replacement record. It was built by
adapting the repository's exact scattering, collective-coordinate, boosted
breather, metric-inverse, geodesic, and radial-evolution primitives into the
paper's variables and dimension. Those repository primitives are incorporated
into the replacement solutions; they are not used as external evidence that a
paper claim passes or fails.
The exact source-to-replacement transformation map is recorded in
`solution-reuse-audit.yaml`.

## Replacement map

| Claim | Author-ready resolution | Replacement evidence |
| --- | --- | --- |
| S01 | Replace “most general” with: “Within local, first-derivative, quadratic, time-reversal-even scalar models with prescribed scalar density, SPD stiffness, flow entering only through `D_t u`, and no derivative/potential cross-couplings, we take equation (2).” | `sympy_replacements.py`, scoped action replacement, expands the material-derivative square exactly. |
| S02 | Replace the constant-background sentence with: “The full linearized equation is `D_t^2 u-c0^2 Laplacian(u)+U''(0)u/rho0=0`; its principal part is the convective wave operator.” | `sympy_replacements.py`, full linearization replacement. |
| S03 | Retain `rho sqrt(det Theta)=constant` as a constitutive normalization. Replace general reflectionlessness with: “For an interface normal `n`, scalar normal-incidence reflection vanishes when `rho_L(n^T Theta_L n)=rho_R(n^T Theta_R n)`.” | `sympy_replacements.py`, directional interface replacement, gives `R=0` exactly. |
| S05 | Replace the ordinary tensor quadratic form by `n_phase(khat)=c0/sqrt(khat^T A khat)`. Keep the eigenvalues of `N=c0 A^(-1/2)` as principal indices. | `sympy_replacements.py`, directional phase-index replacement. |
| S06 | Replace the all-potential theorem claim with the scoped computational claim: “For `U=1-cos u` and the declared Gaussian data, a real radial 2+1D trajectory remains localized through `t=30`.” State that this is finite-time evidence, not an eternal breather theorem. | `scipy_replacements.py`: leapfrog and DOP853 agree; spatial refinement passes; late core-energy fractions exceed 0.90. |
| S07 | Tie the approximation to the supplied Gaussian family: “For an affine stiffness background, freezing the coefficient at the lump center produces a relative spatial-operator residual proportional to `ell/L`.” | `scipy_replacements.py` gives relative residuals `0.0153093` and `0.00765466` when `L/ell` doubles from 10 to 20, an exact refinement ratio of `0.5`. |
| S08 | Replace the rigid-profile inference with: “If the explicit localized family is closed under boosts with `E=gamma E0` and `p=gamma E0 v/c0^2`, then `L=pv-E=-E0/gamma`.” | `sympy_replacements.py`, boosted-family replacement, and `P238ReplacementProofs.lean`, `boostedFamilyLegendreTransform`. |
| S11 | Replace equations (33)–(38) by `nbar^(-1)[[-1+v^T N^2 v,-v^T N^2],[-N^2 v,N^2]]`, where `v=V/c0`. | `sympy_replacements.py`, exact inverse replacement; `P238ReplacementProofs.lean`, four inverse-entry theorems. |
| S12 | Replace universal emergence language with: “For the corrected static metric and `0<=v_local^2<1`, `d tau/dt=nbar^(-1/2)/gamma_local` and `d ell_i=n_i dx_i/sqrt(nbar)`; conditional massive trajectories from the S08/S09 worldline action follow its geodesics.” | `sympy_replacements.py`, conditional clock-and-ruler replacement, plus the einbein/geodesic derivations in `sympy_checks.py` and Lean. |
| S15 | Replace the coefficient map by the exact ADM/acoustic decomposition of equatorial Kerr given below; it uses the corrected S11 inverse. | `sympy_replacements.py`, exact Kerr and constitutive replacements; Kerr coefficient theorems in `P238ReplacementProofs.lean`. |
| S16 | For an exact result, replace the minimal profiles by `Delta=r^2-rs*r+a^2`, `G=r^2+a^2+a^2 rs/r`, `Omega^2=Delta/G`, `h_rr=r^2 G/Delta^2`, `h_phiphi=G^2/Delta`, and `V^phi/c0=a rs/(rG)`. Then `Omega^2 g_acoustic=g_Kerr` coefficient by coefficient, and the supplied physical-frame `rho`, `Theta_r`, and `Theta_t` satisfy determinant matching. Alternatively retain the original profiles but call them a minimal rotating acoustic model rather than Kerr. | `sympy_replacements.py`, exact Kerr, Schwarzschild-limit, and constitutive replacements, and `P238ReplacementProofs.lean`. |
| S17 | Replace the root sentence with: “For the exact Kerr replacement, `omega_±=(a rs/r±sqrt(Delta))/G`; the lower/counter-rotating root is negative for `r>rs`, zero at the equatorial ergosurface, and positive inside, while the upper root remains positive.” | `sympy_replacements.py`, exact Kerr azimuthal-null-root replacement. |
| S18 | Replace the universal headline with: “The paper supplies a conditional analogue-kinematics construction from a scoped real 2+1D localized trajectory, an `O(ell/L)` background estimate, a boost-closed-family worldline action, corrected metric observables, and an exact conformal equatorial Kerr map.” | `sympy_replacements.py` composes the exact repaired chain; `scipy_replacements.py` supplies its real-lump and gradient premises; Lean checks its finite algebraic components. |

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
