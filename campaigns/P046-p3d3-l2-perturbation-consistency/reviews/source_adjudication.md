# P3D3 Source Adjudication

P3D3 is qualified. P046 accepts the exact residual and corrected regular l=2
linearization as `C-PDE-003`, and a separately specified finite-time regular
perturbation evolution with a nonzero first-order STF energy moment as
`C-PDE-004`. P3D3's multiplicative field, clean two-frequency radiating line,
coarse-PDE corroboration, and FS2 recovery do not earn their advertised scope.

## Reproduction and Compatibility

The hash-pinned source exits cleanly with five checks in 125.7 seconds under
NumPy 2.5.1. Its compatibility branch selects `numpy.trapezoid` before the
older `numpy.trapz` name. It reports construction-route `Qzz` AC amplitude
259.01, core frequency 0.8901, constructed-Q frequency 1.8326, coarse-PDE
`Qzz` amplitude 204.76, spherical-grid residual `max|Qzz|=2.960`, and inferred
transverse variance 3.8373. Reproduction proves those checks execute; it does
not validate the word self-consistent.

## Multiplicative Construction Residual

For the full dimensionless 3+1 equation
`u_tt-u_rr-2*u_r/r-(Delta_Omega u)/r^2+sin(u)=0`, let `P` solve the radial
equation and set `Y=P2(cos(theta))`. Substitution of P3D3's
`u=P*(1+a*Y)` gives the exact residual

`sin(P*(1+a*Y))-(1+a*Y)*sin(P)+6*a*P*Y/r^2`.

Its first-order coefficient is
`Y*(P*cos(P)-sin(P)+6*P/r^2)`, which is generically nonzero. At second order,
the nonlinear term includes `-a^2*P^2*sin(P)*Y^2/2`; since
`P2^2=P0/5+2*P2/7+18*P4/35`, the finite deformation also leaks into `l=4`.
P3D3 never checks this residual. Its construction-route `T00` further omits
the angular-gradient term `u_theta^2/(2*r^2)`, even though the later 2D route
includes it. Thus P3D3.1's nonzero prescribed moment is not the energy moment
of a demonstrated field solution.

The construction also violates origin regularity. Its l=2 coefficient is
`a*P(r,t)`, which approaches a nonzero value wherever the radial center field
does. A smooth scalar l=2 coefficient must behave as `O(r^2)`.

## Correct Regular l=2 Sector

The corrected infinitesimal ansatz is
`u=P+epsilon*psi(r,t)*P2(cos(theta))`. Its exact first-order equation is

`psi_tt-psi_rr-2*psi_r/r+6*psi/r^2+cos(P)*psi=0`,

with `psi=O(r^2)` at the origin. Writing `v=r*psi` gives
`v_tt=v_rr-6*v/r^2-cos(P)*v`, with `v=O(r^3)`. SymPy verifies both reductions,
the P4 leakage guard, and mutations of the angular coefficient.

P046 evolves the declared background initial data together with the regular
mode `psi(r,0)=0.2*(r/4)^2*exp(-(r/4)^2)`, both initially at rest. On
`0<=r<=80`, `0<=t<=40`, the baseline has `dr=0.1`, `dt=0.04`, homogeneous
outer Dirichlet data, and no sponge. The interval ends before a boundary
characteristic can return to the core, and recorded outer-shell amplitudes are
below `2e-19`.

For `u=P+epsilon*psi*P2`, the first-order energy-density coefficient is
`h=P_t*psi_t+P_r*psi_r+sin(P)*psi`. With
`H=4*pi*integral r^4*h dr`, exact angular integration gives
`Q/epsilon=diag(-H/5,-H/5,2*H/5)`. The baseline `Qzz/epsilon` trace has RMS
404.678 and maximum absolute value 680.589; it is nonzero without presuming a
gravity theory.

Meshes 0.2, 0.1, and 0.05 give background self-errors 0.02202 then 0.005534,
mode errors 0.03233 then 0.008411, and Q-trace errors 0.01082 then 0.002498.
Closed-box background-energy ranges decrease from 0.003297 to 0.0008150 to
0.0002032. Timestep halving changes the Q trace by relative RMS 0.0009687; a
causally disconnected domain extension to 100 leaves the compared mode
unchanged. Halving the mode seed halves both mode and moment exactly, while a
zero seed preserves exact zeros.

An exact free `j2(k*r)*cos(sqrt(1+k^2)*t)` Dirichlet-box mode converges at
second order with errors 0.004654, 0.001163, and 0.0002908 and convergent
quadratic-energy variation. Independently, DOP853 evolves transformed
background and mode variables on `dr=0.2` through time 20. It agrees with the
canonical scheme to 2.141 percent in the background radial norm, 0.923 percent
in the mode norm, and 0.201 percent in `Qzz`.

## P3D3.2 Frequency and Radiation Claim

P3D3's clean line belongs only to its invalid prescribed construction. It
selects FFT bin 35 at 1.8326 and calls it twice core bin 17 at 0.8901 within a
0.0524 bin. This does not establish exact doubling, and it supplies no
frequency characterization of the corrected regular mode. The source itself
says its coarse 2D PDE spectrum is relaxation dominated. A pending QB2
annotation cannot promote this earlier result backward.

Calling the line a gravitational-wave line adds unaccepted premises. P3D3
declares `G_eff=c0=1` and defines no gravitational action, source map, retarded
field, conserved isolated stress completion, flux derivation, or absolute
scale. `C-PDE-004` therefore makes no radiation statement.

## P3D3.3 Coarse Axisymmetric PDE Route

The source writes the correct continuum axisymmetric sine-Gordon equation, but
its cell-centered seed approaches the same angle-dependent nonregular center.
It uses one `dr=0.1`, 48-angle grid, one CFL choice, one domain, and one time
interval, with no mesh, angular, timestep, domain, boundary, conservation, or
independent-method study. Its `a=0` run retains `max|Qzz|=2.960` and passes only
because that is below five percent of the deformed scale.

Moreover, `Qxx=Qyy=-Qzz/2` is structural once the code constructs
`I=diag(Ixx,Ixx,Izz)` and trace-subtracts it. That ratio does not validate the
PDE, seed, or moment values. The route remains attempt evidence rather than
accepted nonlinear stability or corroboration.

## P3D3.4 Transverse-Moment Claim

For a spherical density, `Ixx=Iyy=Izz=S/3` is already `C-MOM-003`. Defining
`sigma_perp^2=I_perp/E0` makes `I_perp=E0*sigma_perp^2` true by construction.
P3D3 obtains 3.8373, whereas FS2's hash-pinned declared per-axis variance is
0.64. Different profiles may have different moments, but this identity neither
recovers nor supersedes FS2's width. It adds no new claim beyond the accepted
spherical moment theorem.

## Terminal Disposition

P3D3 maps the corrected exact perturbation equation and residual to
`C-PDE-003`, the regular finite-time linearized IVP and first-order STF energy
moment to `C-PDE-004`, and its spherical per-axis identity to `C-MOM-003`. It
remains qualified for its nonregular multiplicative construction, omitted
angular energy, unrefined coarse PDE, exact/clean two-frequency wording,
radiating-channel and waveform interpretations, declared gravitational
normalization, FS2 recovery, nonlinear stability, absolute scale, and
substrate ontology. P3D4, QB2, QB3, and BX1 must not import the rejected P3D3
premises; they remain separate pending adjudications.
