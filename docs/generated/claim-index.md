<!-- GENERATED: scripts/render_docs.py; DO NOT EDIT -->
# Accepted claim index

This document is generated from `governance/claims.yaml`.

## C-CC-001

Conditional on the timelike one-coordinate action L = -(E0/sqrt(n(q)))*sqrt(1-n(q)^2*qdot^2/c0^2), with positive n, c0, and E0, the exact coordinate-time acceleration is qddot = (c0^2-3*n^2*qdot^2)*n_q/(2*n^3). Its zero-velocity limit is c0^2*n_q/(2*n^3), matching C-OG-001, and its locally unique same-data IVP is independent of E0. The mixed-scale counterexample with E0 also inside the kinetic square root retains E0 and, for n=1+alpha*q at q=qdot=0, has initial acceleration E0*c0^2*alpha/2.

- Accepted in: `v0.7.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-VAR-001, C-OG-001

## C-MED-001

For positive density rho, thermal scale Theta, and reference speed c, the declared co-scaled response laws epsilon=rho*Theta/c^2 and mu_inverse=rho*Theta satisfy epsilon*mu=1/c^2 and give local wave speed sqrt(mu_inverse/epsilon)=c. Density and thermal variations therefore cannot create an index within this ansatz. More generally, the logarithmic sensitivities vanish exactly when the corresponding response exponents match.

- Accepted in: `v0.8.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-OG-001

For every positive twice-differentiable static index n(x) and c0 > 0, the declared 1+1 metric g = diag(-1/n, n/c0^2) has Ricci scalar R = c0^2*(n*n_xx - 2*n_x^2)/n^3 and satisfies Box_g(log(n)) = R. Among twice-differentiable scalar compositions f(n) satisfying Box_g(f(n)) = R for every such profile, exactly f(n) = log(n) + C work.

- Accepted in: `v0.4.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-OG-002

Conditional on C-OG-001 and the imported constitutive relation n = 1/(1 + 2*Phi/c0^2), the optical dilaton is log(n) = -log(1 + 2*Phi/c0^2), with leading weak-field term -2*Phi/c0^2. The metric's static slow coordinate-geodesic acceleration is exactly -(1 + 2*Phi/c0^2)*Phi_x; under Phi = lambda*U it satisfies acceleration/lambda -> -U_x as lambda -> 0+.

- Accepted in: `v0.4.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-OG-001

## C-OG-003

Conditional on C-OG-001 and C-OG-002, for every twice-differentiable potential Phi(x) whose TF index n = 1/(1 + 2*Phi/c0^2) is positive, the exact source-side optical dilaton operator is -Box_g(log(n)) = 2*Phi_xx; no weak-field approximation is required and c0 cancels. Consequently, if a separate model declares -Box_g(phi) = kappa*rho, that equation is algebraically equivalent to Phi_xx = (kappa/2)*rho. This claim neither derives that matter equation nor assigns a physical normalization to kappa.

- Accepted in: `v0.10.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-OG-001, C-OG-002

## C-RG-001

For positive radius R and density lambda, the circumference line energy E_line = 2*pi*R*lambda is homogeneous of degree one, has constant positive derivative 2*pi*lambda, and has no stationary radius. For positive surface density sigma, E_shell = 4*pi*R^2*sigma is homogeneous of degree two and has radius-dependent derivative 8*pi*R*sigma. For positive line tension T and pressure P, E_cap = 2*pi*R*T - pi*R^2*P + C has the unique strict global maximum R = T/P. Conditional line constructions with coefficients T and the C-SG-002 breather energy share only the degree-one line form; their energies are equal for every positive R if and only if their coefficients are equal.

- Accepted in: `v0.6.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-SG-002

## C-SG-001

For every real omega with 0 < omega < 1, eta = sqrt(1-omega^2), and real x,t, the field phi(x,t) = 4 atan(eta sin(omega t)/(omega cosh(eta x))) is spatially localized, periodic with period 2*pi/omega, and satisfies phi_tt - phi_xx + sin(phi) = 0 identically in normalized units.

- Accepted in: `v0.1.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-SG-002

The C-SG-001 breather has conserved normalized Hamiltonian energy E(omega) = 16 sqrt(1-omega^2); E approaches the two-kink threshold 16 as omega -> 0+ and approaches 0 as omega -> 1-.

- Accepted in: `v0.1.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001

## C-SG-003

For every real omega with 0 < omega < 1, the C-SG-001 breather's canonical action normalized by J = (1/(2*pi))*closed_integral(p dq) is J(omega) = 16 arccos(omega). It satisfies dE/dJ = omega, maps the family onto 0 < J < 8*pi, and has inverse parameterization omega = cos(J/16) and E = 16 sin(J/16).

- Accepted in: `v0.2.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001, C-SG-002

## C-SG-004

For every real omega with 0 < omega < 1, the C-SG-001 breather's period-averaged squared-gradient integral is Gbar = (1/T)*integral_0^T dt integral_R dx phi_x^2 = 16*(sqrt(1-omega^2) - omega*arccos(omega)) = E - omega*J. It satisfies dGbar/domega = -J, approaches 16 as omega -> 0+, and approaches 0 as omega -> 1-. Gbar is the full squared-gradient integral; its Hamiltonian energy contribution is Gbar/2.

- Accepted in: `v0.3.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001, C-SG-002, C-SG-003

## C-SG-005

For every real omega with 0 < omega < 1, the C-SG-002 breather's deficit below the normalized two-kink threshold is Delta(omega)=16-E(omega)=16*(1-sqrt(1-omega^2)). It satisfies 0<Delta<16, is strictly increasing and strictly convex, tends to 0 as omega approaches 0 from above, tends to 16 as omega approaches 1 from below, and partitions the threshold exactly as E+Delta=16.

- Accepted in: `v0.9.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-002

## C-SG-006

For every real omega with 0 < omega < 1, define the breather's energy-frequency secant action scale H(omega)=E(omega)/omega. Then H=16*sqrt(1-omega^2)/omega is positive and strictly decreasing from positive infinity to zero. Its ratio to the canonical action is Pi=J/H=omega*arccos(omega)/sqrt(1-omega^2), which is strictly increasing with 0<Pi<1, tends to zero as omega->0+, and tends to one as omega->1-. Moreover dE/dH=omega^3, whereas dE/dJ=omega, so H is not the canonical action on the open family and agrees with it only asymptotically through Pi->1 at the harmonic endpoint.

- Accepted in: `v0.11.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-002, C-SG-003

## C-SG-007

Conditional on a fixed positive action increment h and the imposed lattice J_n=n*h, every positive integer n with n*h<8*pi has omega_n=cos(n*h/16) and E_n=16*sin(n*h/16), so n<8*pi/h and only finitely many levels are admissible. The continuous interpolation obeys dE/dn=h*cos(n*h/16)=h*omega_n. When (n+1)*h<8*pi, the actual adjacent gap is E_(n+1)-E_n=32*sin(h/32)*cos((2*n+1)*h/32), which is generally not h*omega_n. This claim does not derive the lattice premise or identify h with a physical coupling or Planck constant.

- Accepted in: `v0.11.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-SG-003

## C-SG-008

For every C-SG-001 breather with 0<omega<1 and every real boost velocity v with |v|<1 in units c=1, let gamma=1/sqrt(1-v^2). The boosted phase components for phase Omega*t-k*x are (Omega,k)=(gamma*omega, gamma*omega*v), while energy-momentum is (E,P)=(gamma*E0, gamma*E0*v). They satisfy the division-free vector identity (E,P)=H(omega)*(Omega,k), where H=E0/omega is C-SG-006's secant action scale, and the invariant norms Omega^2-k^2=omega^2 and E^2-P^2=E0^2. For v!=0 this implies E/Omega=P/k=H; the vector statement remains well defined at v=0. This is a Lorentz-kinematic relation and does not identify H as a universal quantum constant.

- Accepted in: `v0.12.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001, C-SG-002, C-SG-006

## C-SK-001

Conditional on positive premises M_top=48*pi^3*B1*E_e and M_ANW=3*pi^2*B1*F_pi/e, equality M_top=M_ANW holds if and only if F_pi/e=16*pi*E_e. The shared linear hedgehog coefficient B1 cancels exactly; changing either B1 power generally prevents that cancellation.

- Accepted in: `v0.8.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-TH-001

For every real dimensionless splitting x, the normalized upper-state occupation of Z = 1 + exp(-x) is P = exp(-x)/Z = 1/(1+exp(x)). Its Bernoulli variance is P*(1-P) = sech(x/2)^2/4, and the conditional symmetric gate W = 2*P*(1-P) = sech(x/2)^2/2. W is even, has unique global maximum 1/2 at x = 0, decreases strictly with |x|, and tends to zero as x tends to either infinity. A shape A*sech(x/2)^2 equals 2*A*W; this identity does not determine the independent amplitude A.

- Accepted in: `v0.5.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-VAR-001

For any differentiable one-coordinate Lagrangian L0 and any nonzero multiplier A that is independent of the path coordinate, velocity, and evolution parameter, the Euler-Lagrange operator satisfies EL[A*L0] = A*EL[L0]. The two Euler-Lagrange equations therefore have the same solution set. The result holds for every fixed nonzero uniform factor, not only a factor of degree one in a named energy scale.

- Accepted in: `v0.7.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-VIR-001

Conditional on the real virial slope formulas width_slope=(a-b)/2 and energy_slope=-(a+b)/2, both slopes equal -1/2 if and only if (a,b)=(0,1). The alternatives (1,0) and (1,1) give slopes (1/2,-1/2) and (0,-1), respectively, and fail the simultaneous target.

- Accepted in: `v0.7.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none
