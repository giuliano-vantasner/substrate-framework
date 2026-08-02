<!-- GENERATED: scripts/render_docs.py; DO NOT EDIT -->
# Accepted claim index

This document is generated from `governance/claims.yaml`.

## C-ACT-001

On any connected interval with normalized canonical action J>0, differentiable positive energy E(J), and positive frequency omega=dE/dJ, the identity E/omega=J throughout the interval holds if and only if E(J)=C*J for a positive constant C. Thus a linear harmonic energy law has secant action equal to canonical action. For a rigid rotor with normalized action J=I*omega and energy E=I*omega^2/2=J^2/(2I), E/omega=J/2 instead.

- Accepted in: `v0.13.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-CC-001

Conditional on the timelike one-coordinate action L = -(E0/sqrt(n(q)))*sqrt(1-n(q)^2*qdot^2/c0^2), with positive n, c0, and E0, the exact coordinate-time acceleration is qddot = (c0^2-3*n^2*qdot^2)*n_q/(2*n^3). Its zero-velocity limit is c0^2*n_q/(2*n^3), matching C-OG-001, and its locally unique same-data IVP is independent of E0. The mixed-scale counterexample with E0 also inside the kinetic square root retains E0 and, for n=1+alpha*q at q=qdot=0, has initial acceleration E0*c0^2*alpha/2.

- Accepted in: `v0.7.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-VAR-001, C-OG-001

## C-CHI-001

In the declared four-real-coordinate model phi=(sigma,pi1,pi2,pi3), use all six standard independent antisymmetric so(4) generators and V=lambda*(phi^T*phi-v^2)^2 with lambda>0 and v>0. At the declared vacuum phi_0=(v,0,0,0), all six infinitesimal invariance residuals and the gradient vanish, the generator-tangent matrix has rank three, its coefficient kernel has dimension three, and the exact Hessian is diag(8*lambda*v^2,0,0,0). Thus this declared classical model has one radial curvature and three independent zero generalized quadratic-mass directions when supplied a positive kinetic metric. At the symmetric stationary point phi=0 the tangent rank is zero. For the explicitly tilted potential V-c*sigma, a positive shifted stationary branch s0 obeys c=4*lambda*s0*(s0^2-v^2) and has transverse curvature c/s0; an anisotropic quadratic term likewise breaks the relevant invariance and lifts its tangent. Separately, for the declared coordinate model U=exp(i*tau_a*pi_a/F) with Pauli matrices and L=A*Tr(partial U*partial U^dagger), the exact leading trace is 2*sum_a(partial pi_a)^2/F^2 and the scalar kinetic metric is (4*A/F^2)*I. Consequently A=F^2/4 gives metric I and quadratic coefficient one half, while A=F^2/16 gives metric I/4 and coefficient one eighth in the same coordinates. A zero potential has zero Hessian; adding m^2*sum_a(pi_a^2)/2 gives Hessian m^2*I. These are conditional O(4) and SU(2) coordinate-model identities depending on C-SYM-001. They establish no chiral symmetry action or its physical breaking, no quantum Goldstone-particle theorem, no physical pion identification, no sigma or nucleon particle, no GMOR relation, no Skyrmion connection, no value of F_pi or a condensate, no absolute mass scale, and no substrate realization.

- Accepted in: `v0.54.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-SYM-001

## C-DIM-001

Over base dimensions energy E and time T, primitives consisting of an energy and frequency have dimension matrix [[1,0],[0,-1]], rank two, and zero kernel, so they form no nontrivial dimensionless monomial. Adding an independent action primitive S gives matrix [[1,0,1],[0,-1,1]], rank two, with one-dimensional kernel spanned by (-1,1,1); up to powers its unique dimensionless monomial is S*omega/E. Both conclusions are local to the declared primitive set and do not prohibit groups after further independent primitives are added.

- Accepted in: `v0.13.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-DIM-002

Over base-dimension rows (M,L,T), the declared primitive columns for a speed c0=(0,1,-1), action S=(1,2,-1), and length a=(0,1,0) form the matrix [[0,1,0],[1,2,1],[-1,-1,0]], which has determinant -1, rank three, and zero kernel. Every target dimension therefore has unique monomial exponents relative to this set. In particular mass, energy, time, density, and stiffness are represented by S/(c0*a), S*c0/a, a/c0, S/(c0*a^4), and S*c0/a^4. Speed and length alone cannot span mass. These statements are local to the declared primitive set and determine neither dimensionless coefficients nor which primitives or values a physical model must select.

- Accepted in: `v0.15.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-DIM-001

## C-DIM-003

Relative to C-DIM-002's declared positive speed c0, action S, and length a, the map from a positive mass m to N_m=m*c0*a/S is dimensionless and bijective, with inverse m=N_m*S/(c0*a). For two masses represented using the same primitive values, m_1/m_2=N_1/N_2. This is a lossless change of coordinates: N_m remains one free dimensionless physics input, so the map predicts no mass or ratio, selects no primitive value, and does not turn a physical import into a derived quantity.

- Accepted in: `v0.16.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-DIM-002

## C-DIM-004

Conditional on positive quantities satisfying the declared equations U*L=S*c0/(2*e^2) and U=4*pi*m*c0^2, exact elimination gives m=S/(8*pi*e^2*L*c0). Relative to C-DIM-003 with basis length L, the mass coordinate is N_m=1/(8*pi*e^2), equivalently S/(m*c0)=8*pi*e^2*L. The coupling e and both equations are premises. The relation predicts no mass, length, coupling, or particle identity and does not eliminate independent information unless those premises are established separately.

- Accepted in: `v0.18.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-DIM-003

## C-DIM-005

Conditional on C-RGE-001 and positive quantities satisfying mu0=S*c0/a, g0^2=beta^2, and m*c0^2=q*Lambda, the C-DIM-003 mass coordinate is N_m=m*c0*a/S=q*exp(-8*pi^2/(b0*beta^2)). The dimensionless inputs q, b0, and beta^2 all remain free and load-bearing. This composition predicts no mass, length, coupling, beta coefficient, prefactor, or particle identity; an unpinned q can reproduce any positive N_m.

- Accepted in: `v0.19.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-DIM-003, C-RGE-001

## C-DIM-007

Conditional on C-RGE-001, an independently existing positive observable sigma with mass dimension two, and Lambda being its only independent dimensionful mass scale, dimensional homogeneity fixes only the power sigma=k*Lambda^2 for an unconstrained positive dimensionless k. The prefactor remains free and load-bearing. If a second independent mass scale M is admitted, the monomial family Lambda^(2-q)*M^q is dimensionally allowed, so the sole-scale premise is essential. The one-loop equations contain no sigma and admit both zero- and positive-tension assignments; this claim establishes neither existence of a string tension, confinement, a magnitude, nor perturbative control at Lambda.

- Accepted in: `v0.22.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-RGE-001

## C-EFT-001

Let V, J_even, and J_odd be real n-entry columns and let K be a nonempty real symmetric invertible n-by-n kernel. In the declared plus-source convention L(V)=V^T*K*V/2+V^T*J with J=J_even+J_odd, component stationarity gives V_star=-K^-1*J, the exact residual K*V_star+J=0, and the reduced term L_eff=-J^T*K^-1*J/2. Its source decomposition consists of the two even squares -J_even^T*K^-1*J_even/2 and -J_odd^T*K^-1*J_odd/2 plus the cross term -(J_even^T*K^-1*J_odd+J_odd^T*K^-1*J_even)/2. Under the declared bookkeeping K and J_even are parity even and J_odd is parity odd, so only the cross term changes sign; it vanishes when either source is absent. For K=M+D with symmetric invertible M and symmetric D, define A=M^-1*D and R_N=sum_(n=0)^N((-A)^n*M^-1). Exact multiplication gives R_N*(M+D)-I=(-1)^N*A^(N+1) and (M+D)*R_N-I=(-1)^N*M*A^(N+1)*M^-1. Thus a finite low-momentum inverse expansion is only a formal truncation under separately supplied power counting and convergence premises; its returned nonzero residual cannot be identified with an exact inverse. Finally, for a field-dependent stationary substitution, the chain rule gives delta Gamma_eff=(delta Gamma)_V+(partial Gamma/partial V)_star*delta V_star, so the induced-field term vanishes on the actual stationary equation while the supplied explicit variation remains. Consequently, if a starting functional is an inhomogeneous term plus invariant local terms with free coefficients, stationary elimination neither selects those coefficients nor creates a missing inhomogeneous anomaly variation. This is a conditional finite-dimensional action theorem. It fixes no field content, source, kernel, mass, coupling, boundary term, operator basis, or coefficient and supplies no HLS field content, no physical vector meson, no WZW functional, no anomaly coefficient, no vector dominance or KSRF relation, no baryon interpretation, no N_c, no absolute scale, and no substrate realization.

- Accepted in: `v0.53.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-FLX-001

Conditional on positive flux Phi uniformly crossing a cross-section A that is fixed independently of positive length L, Gauss data give the constant field E=Phi/A. With declared field-energy density E^2/2, stored field energy is U(L)=Phi^2*L/(2A), linear with energy slope sigma_energy=Phi^2/(2A). Separately, for positive endpoint charge q and declared force F=qE, endpoint work is V(L)=q*Phi*L/A, linear with force slope sigma_force=q*Phi/A. The slopes agree if and only if q=Phi/2; for q=Phi the endpoint slope is twice the energy slope. Fixed area is load-bearing: A(L)=A0*(1+L/L0) gives logarithmic field energy, while spherical spreading gives an inverse-square field and curved Coulomb potential. Matching a supplied tension by A_eff=Phi^2/(2*sigma) defines an effective area and does not predict it. This theorem establishes no physical charge, flux tube, vortex-tension identity, QCD, area law, or confinement.

- Accepted in: `v0.24.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-GAU-001

Conditional on C-U1-001's smooth complex scalar, a positive coupling e, and a declared real local-U(1) connection A_mu, define D_mu=partial_mu-i*e*A_mu and transform Psi'=exp(i*e*chi)Psi, A_mu'=A_mu+partial_mu chi for arbitrary smooth real chi. Then D_mu Psi transforms covariantly, a phase-independent potential and (D_mu Psi)^*D^mu Psi are invariant, and in C-U1-001's current convention the kinetic expansion is the bare term plus e*A_mu*j^mu+e^2*A_mu*A^mu*|Psi|^2. The curvature F_mu_nu=partial_mu A_nu-partial_nu A_mu is invariant and [D_mu,D_nu]Psi=-i*e*F_mu_nu*Psi. Separately, conditional on nonzero asymptotic amplitude, integer phase winding N, and angular energy with logarithmic coefficient proportional to (N-e*A_theta*r)^2, finite energy forces flux 2*pi*N/e; its charge-e holonomy is +1. A minus-one holonomy requires a separately declared fractional flux. Local covariance leaves every F^2 coefficient unconstrained and establishes no gauge kinetic action, Maxwell equation, photon, force, physical electric charge, or substrate electromagnetic sector.

- Accepted in: `v0.26.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-U1-001

## C-GW-001

In Euclidean three-space let n be a unit direction, P_ij=delta_ij-n_i*n_j, and let Lambda be the symmetric transverse- traceless projector. For every real symmetric tensor S, integral_{S^2} |Lambda(n) S|^2 dOmega equals (8*pi/5)*|STF(S)|^2, where STF(S)=S-delta*Tr(S)/3; pure trace is therefore annihilated. Conditional on a declared far-field waveform h_TT=(A/r)*Lambda[ddot Q] and declared flux dP/dOmega=B*r^2*<dot h_TT:dot h_TT>, angular integration gives P=(8*pi/5)*B*A^2*<|STF(dddot Q)|^2>. The factors A and B are premises, not consequences of the angular integral. If the normalized source moment of C-MOM-001 is I_STF and Q_s=s*I_STF for nonzero s, the same waveform requires A_s=A_1/s and the power coefficient multiplying |dddot Q_s|^2 scales as 1/s^2. Thus the particular declared inputs A_1=2*G and B=1/(32*pi*G) give G/5 for I_STF, whereas the convention Q=3*I_STF gives G/45 for |dddot Q|^2, not G/5. For a single harmonic Q=C*cos(omega*t)+S*sin(omega*t), the exact cycle average of the squared STF third derivative is omega^6*(|STF(C)|^2+|STF(S)|^2)/2. These results establish only exact projector, angular, convention, and conditional-functional algebra; they establish no gravitational action or field equation, retarded solution, physical Isaacson flux, measured coupling, universal lowest radiating multipole, arbitrary-source radiation, nonlinear gravity, 1+1 lift, or substrate realization.

- Accepted in: `v0.33.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-MOM-001

## C-GW-002

For each nonzero direction n in Euclidean three-space, the orthogonal TT projector of C-GW-001 acting on the six-dimensional real vector space of symmetric 3-by-3 tensors has rank and trace two, with eigenvalues two ones and four zeros. Choose an oriented orthonormal frame (u,v,n_hat). The tensors e_plus=(u*u^T-v*v^T)/sqrt(2) and e_cross=(u*v^T+v*u^T)/sqrt(2) are symmetric, transverse, traceless, and Frobenius-orthonormal. They are complete for the image: TT_n(S)=(e_plus:S)*e_plus+(e_cross:S)*e_cross for every symmetric S. If the transverse frame changes by u'=cos(psi)u+sin(psi)v and v'=-sin(psi)u+cos(psi)v, then e_plus'=cos(2psi)e_plus+sin(2psi)e_cross and e_cross'=-sin(2psi)e_plus+cos(2psi)e_cross. Consequently the declared circular combinations (e_plus plus/minus i*e_cross)/sqrt(2) acquire the opposite algebraic phases exp(minus/plus 2*i*psi). A deterministic frame may cover all nonzero directions piecewise, but no global continuity is asserted. The unnormalized axis tensors used by GW3 have norm squared two and require coefficient division by two. These results establish no gravitational action, propagating field equation, constraint or gauge quotient, physical polarization observable, graviton count, physical helicity, quantum state, radiation channel, or substrate realization.

- Accepted in: `v0.34.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-GW-001

## C-GW-003

Let two equal point masses m follow the declared paths x_1(t)=a*(cos(Omega*t),sin(Omega*t),0) and x_2(t)=-x_1(t), where a is each mass's orbital radius and the separation is 2*a. Their monopole is 2*m, their dipole is zero, and for the normalized moment I_STF=I-delta*Tr(I)/3 the exact Frobenius norms are |ddot I_STF|^2=32*m^2*a^4*Omega^4 and |dddot I_STF|^2=128*m^2*a^4*Omega^6. The triple convention Q=3*I_STF has derivative norms nine times larger. Conditional on h_TT=(A/R)*TT(ddot I_STF), line of sight n=(sin(i),0,cos(i)), and oriented transverse frame p=(cos(i),0,-sin(i)), v=(0,1,0), the conventional matrix read-offs are h_plus=-(2*A*m*a^2*Omega^2/R)*(1+cos(i)^2)*cos(2*Omega*t) and h_cross=-(4*A*m*a^2*Omega^2/R)*cos(i)*sin(2*Omega*t). The normalized C-GW-002 basis coordinates are sqrt(2) times these read-offs. Face-on coefficients have equal amplitude in quadrature; edge-on cross vanishes and plus has half the face-on amplitude. With the separately declared inputs A=2*G and B=1/(32*pi*G), C-GW-001 gives conditional power 128*G*m^2*a^4*Omega^6/5. Equivalently Q=3*I_STF requires waveform coefficient 2*G/3 and power coefficient G/45; combining Q with the unscaled coefficient creates a factor-three field and factor-nine power error. This theorem treats the paths as kinematic inputs and establishes no binding stress, orbital law, breather embedding, isolated conserved 3+1 source, gravitational action or coupling, retarded dynamics, energy loss, detector strain, astrophysical prediction, or substrate identity.

- Accepted in: `v0.35.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-MOM-001, C-GW-001, C-GW-002

## C-GW-004

Let mu(t) be the exact C-SG-009 longitudinal moment and apply the conditional axisymmetric separable construction of C-MOM-002. Writing d=mu'''(t), the normalized tensor satisfies |I_STF'''|^2=2*d^2/3 and the triple tensor Q=3*I_STF satisfies |Q'''|^2=6*d^2. Under the separately declared C-GW-001 inputs A=2*G and B=1/(32*pi*G), the normalized convention therefore has conditional instantaneous power P(t)=2*G*d^2/15. The triple convention requires waveform coefficient 2*G/3 and power coefficient G/45 and gives the identical result; using 2*G and G/5 with triple Q multiplies the field by three and power by nine. This conditional power is nonnegative and nonzero at some phases, but it vanishes at the exact minimum and maximum symmetry phases where d=0. For a line of sight in the x-z plane at inclination i from the symmetry x axis, choose the oriented transverse frame p=(sin(i),0,-cos(i)), q=(0,1,0). If e=mu''(t), the normalized TT projection has plus coordinate e*sin(i)^2/sqrt(2), conventional matrix readout e*sin(i)^2/2, and zero cross coordinate. Thus the conditional waveform h_TT=(2*G/R)*TT[I_STF''] has conventional plus readout G*e*sin(i)^2/R, zero cross, and an exact symmetry-axis null; the inverse-rescaled triple convention gives the same waveform. These are exact consequences of declared moment, projector, waveform, and flux inputs. They establish no conserved isolated 3+1 source, gravitational action or field equation, physical retarded solution or flux, radiation channel, detector strain, backreaction, or substrate realization.

- Accepted in: `v0.38.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-SG-009, C-MOM-002, C-GW-001, C-GW-002

## C-GW-005

Let e and n be nonzero three-vectors denoting an axis of symmetry and a line of sight, and replace them by their unit directions. For an axisymmetric normalized STF tensor S=alpha*(e*e^T-delta/3), and an explicit nonzero convention scale s, define S_s=s*S; s=1 is normalized and s=3 is the triple convention. Then Tr(S_s)=0, its eigenvalue along e is 2*s*alpha/3, and |S_s|^2=2*s^2*alpha^2/3. Let cos(i)=e.n. Away from the axial null choose the natural meridian frame p=(e-cos(i)*n)/sin(i), q=n cross p. The TT projection of S_s has normalized plus coordinate s*alpha*sin(i)^2/sqrt(2), conventional matrix readout s*alpha*sin(i)^2/2, and cross coordinate zero. Along n parallel to e the complete TT tensor is zero. Under the separately declared C-GW-001 inputs A=2*G and B=1/(32*pi*G), convention S_s requires waveform coefficient 2*G/s and gives the convention-invariant conditional conventional waveform h_plus=G*alpha''*sin(i)^2/R, h_cross=0, and power P=2*G*alpha'''^2/15. Equivalently, if lambda_s is the axial eigenvalue of S_s, h_plus*R/G=3*lambda_s''*sin(i)^2/(2*s) and P/G=3*lambda_s'''^2/(10*s^2). Combining a scale-three tensor with the scale-one coefficient multiplies the waveform by three and power by nine. These are exact conditional tensor identities. They establish no source dynamics, conserved isolated stress tensor, gravitational action or field equation, physical retarded solution or flux, detector strain, backreaction, absolute scale, or substrate realization.

- Accepted in: `v0.42.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-GW-001, C-GW-002

## C-GW-006

For the specified regular linearized l=2 IVP of C-PDE-004, write q(t)=Qzz(t)/epsilon for the z-axis eigenvalue of its triple-STF first-order energy-moment coefficient. Rerun that IVP on 0<=r<=80 and 0<=t<=40 with meshes dr=0.2, 0.1, and 0.05, Courant factor 0.4, and aligned dense sample interval 0.16. On the baseline dr=0.1, dt=0.04 trace, downsample to interval 0.32 and differentiate only on 5<=t<=35 with a nine-point degree-five local polynomial. The resulting q'' and q''' traces have RMS 13.7837762 and 19.1706587. Successive mesh relative-RMS differences are 0.025762 and 0.006510 for q'', and 0.042973 and 0.010993 for q'''. Timestep halving changes the two traces by 0.005656 and 0.010295, domain extension to 100 by below 1e-12, and sample-interval halving by 0.041321 and 0.047555. A quintic interpolating B-spline differs by 0.045069 and 0.050127, while an independently derived seven-point finite difference reproduces both summaries within ten percent. Under the scale-three conditional map of C-GW-005, h_plus*R/(G*epsilon)=q''*sin(i)^2/2, h_cross=0, and P/(G*epsilon^2)=q'''^2/30. The edge-on waveform coefficient has RMS 6.8918881 and the interpreted-window mean power coefficient is 12.2504719. Half mode coefficient gives exact half derivatives and waveform coefficient and one-quarter power; zero mode gives an exact zero trace. This is endpoint-qualified, dimensionless, linearized, finite-grid and finite-time simulation evidence for conditional coefficients. It establishes no frequency or periodicity result, nonlinear mode, conserved gravitational source, physical radiation channel, gravity theory, absolute waveform or luminosity, backreaction, detector observable, or substrate realization.

- Accepted in: `v0.42.0`
- Verification: `simulation_evidence`
- Compatibility: `compatible_extension`
- Dependencies: C-PDE-004, C-GW-005

## C-GW-007

Let a scalar density's coefficients in the unnormalized real l=2 basis P2(n_z), n_x^2-n_y^2, 2*n_x*n_y, 2*n_x*n_z, and 2*n_y*n_z have radial moments H_20, H_2c, H_2s, H_1c, and H_1s, where each H=4*pi*integral r^4*h(r) dr. In the C-MOM-003 triple-STF convention, exact angular integration gives Q_xx=-H_20/5+2*H_2c/5, Q_yy=-H_20/5-2*H_2c/5, Q_zz=2*H_20/5, Q_xy=2*H_2s/5, Q_xz=2*H_1c/5, and Q_yz=2*H_1s/5. A nonzero pure real-m=2 cosine coefficient therefore gives diag(2H/5,-2H/5,0), which is traceless and has three distinct eigenvalues. Along the z sightline with x reference, the conventional plus and cross matrix readouts are 2*H_2c/5 and 2*H_2s/5; coordinates in the normalized unit-Frobenius TT basis are larger by sqrt(2). For sampled, DC-removed coefficient traces, temporal source rank is the matrix rank with time samples as rows and declared angular components as columns. A fixed tensor direction times one scalar trace has rank at most one even when both coordinate readouts are nonzero; two nonproportional traces are required for rank two, and invertible polarization-frame rotation preserves that rank. By the exact m-degeneracy C-PDE-009, pairing the accepted C-PDE-004 radial solution with n_x^2-n_y^2 gives the genuine first-order finite-time tensor diag(q(t),-q(t),0), where q is C-PDE-004's accepted P2 Q_zz/epsilon trace. Its natural conventional plus trace therefore inherits RMS 404.678 and maximum absolute value 680.589, with cross zero and temporal rank one. These are exact moment, TT-coordinate, rank, and dependency- transfer statements. They establish no finite nonlinear deformation, localized or periodic eigenmode, rank-two source evolution, conserved gravitational source, gravity theory, physical waveform or radiation, flux, graviton count, absolute scale, or substrate realization.

- Accepted in: `v0.48.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-PDE-009, C-PDE-004, C-MOM-003, C-GW-002

## C-GW-008

Let I_STF be the normalized symmetric trace-free moment of C-MOM-001 and let Q_s=s*I_STF for a declared nonzero convention scale s. Under exactly the conditional C-GW-001 premises A=2*G for I_STF and B=1/(32*pi*G), the same field written with Q_s is h_TT=(2*G/(s*R))*TT(Q_s''), and its instantaneous or already-averaged total angular power is P=G*(Q_s'''_ij*Q_s'''_ij)/(5*s^2). Thus the triple convention s=3 requires waveform coefficient 2*G/3 and power coefficient G/45; applying 2*G and G/5 directly to the triple tensor multiplies the field by three and power by nine. For the C-GW-007 triple real-m2 tensor Q_3=[[q_c,q_s,0],[q_s,-q_c,0],[0,0,0]], viewed along z with x reference, the conventional conditional readouts are h_plus*R/G=2*q_c''/3 and h_cross*R/G=2*q_s''/3, while P/G=2*((q_c''')^2+(q_s''')^2)/45. If instead Q_s(t)=q(t)*T for one fixed STF tensor T, every observer-frame plus/cross pair is a constant vector times q''(t), has temporal rank at most one, and, when nonzero, admits a spin-two transverse-frame rotation with cross equal to zero; two nonzero coordinates in one frame do not establish elliptical or two-mode radiation. Rank two requires nonproportional coefficient traces. In the conditional comparison q_c=A0*cos(w*t), q_s=A0*sin(w*t), the natural-z waveform is circular with constant squared coordinate radius (2*G*A0*w^2/(3*R))^2 and constant power 2*G*A0^2*w^6/45. These are exact convention, TT, power, and temporal-rank consequences of the declared premises. They establish no conserved localized source, excitation of both traces by accepted scalar dynamics, gravitational action or field equation, physical retarded waveform or flux, graviton count, detector signal, backreaction, absolute scale, particle identity, or substrate realization.

- Accepted in: `v0.49.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-GW-001, C-GW-002, C-GW-007

## C-LIE-001

For the eight explicit standard fundamental SU(3) generators T_a=lambda_a/2, each generator is Hermitian and traceless and Tr(T_a*T_b)=(1/2)*delta_ab. With [T_a,T_b]=i*f_abc*T_c and f_abc=-2*i*Tr([T_a,T_b]*T_c), the structure constants are totally antisymmetric. The exact representation invariants are T_F=1/2, C_F=4/3 from sum_a T_a^2=(4/3)I_3, and C_A=3 from both sum_a F_a^2=3I_8 for (F_a)_bc=-i*f_abc and sum_cd f_acd*f_bcd=3*delta_ab. These are convention-specific algebraic facts and establish no physical gauge-sector identification.

- Accepted in: `v0.21.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-LIE-002

In the standard explicit fundamental SU(3) representation of C-LIE-001, the exact complex 3-by-3 commutant of all eight generators consists only of scalar matrices. Intersecting that commutant with unitary determinant-one matrices gives exactly {omega^k*I_3 | k=0,1,2}, where omega=-1/2+i*sqrt(3)/2, an order-three cyclic group isomorphic to Z_3. A fundamental vector has center phase omega^k, center conjugation on any 3-by-3 matrix and hence the adjoint matrix representation is trivial, and abstract integer trialities compose additively modulo three. This theorem establishes no substrate field assignment, quark or gluon identity, screening dynamics, Wilson law, string tension, or confinement.

- Accepted in: `v0.25.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-LIE-001

## C-LIN-001

For a finite exact real linear system M*x=b, the system is consistent if and only if rank(M)=rank([M|b]). When consistent, its solution-space dimension is columns(M)-rank(M); it is unique exactly when this dimension is zero and underdetermined exactly when it is positive. More equations than unknowns is only an equation-count property and implies neither consistency nor uniqueness. Adding an exact duplicate of a nonzero row leaves coefficient rank and nullity unchanged; the two-row duplicate subsystem is consistent exactly when the two right-hand sides agree.

- Accepted in: `v0.20.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-MED-001

For positive density rho, thermal scale Theta, and reference speed c, the declared co-scaled response laws epsilon=rho*Theta/c^2 and mu_inverse=rho*Theta satisfy epsilon*mu=1/c^2 and give local wave speed sqrt(mu_inverse/epsilon)=c. Density and thermal variations therefore cannot create an index within this ansatz. More generally, the logarithmic sensitivities vanish exactly when the corresponding response exponents match.

- Accepted in: `v0.8.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-MED-002

Conditional on positive action scale S, speed c, length a, and dimensionless ratio kappa, declare number density n=a^-3 and a Debye-like scale Theta=kappa*S*c/a. Composing these premises with C-MED-001's co-scaled laws gives epsilon=kappa*S/(a^4*c), mu_inverse=kappa*S*c/a^4, epsilon/mu_inverse=1/c^2, and local wave speed c. Under the additional declared dictionary rho_medium=epsilon/2, the mass density is rho_medium=kappa*S/(2*a^4*c). The Debye relation, kappa, the number-density law, and the one-half dictionary are premises; dimensions and response cancellation do not select them or establish a physical medium realization.

- Accepted in: `v0.15.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-DIM-002, C-MED-001

## C-MIX-001

For every finite complex m-by-n matrix M, there are square unitary column bases U and V and a same-shape rectangular diagonal Sigma with nonnegative entries such that U^dagger*M*V=Sigma and M=U*Sigma*V^dagger. The nonzero spectra of M*M^dagger and M^dagger*M are the squared singular values with the shape-required additional zeros. Individual bases are noncanonical: a repeated nonzero singular block permits the same unitary rotation on its paired left and right bases, while left and right null blocks permit independent unitary choices. For two same-size unitary column bases U_a,U_b, R=U_a^dagger*U_b is unitary and identical ordered bases give R=I. If row transforms A_i instead satisfy A_i*M_i*B_i^dagger=Sigma_i and map original coordinates to diagonal coordinates, the corresponding relative transform is A_a*A_b^dagger, not A_a^dagger*A_b. For a real symmetric matrix [[a,b],[b,d]], the proper rotation [[cos(theta),sin(theta)],[-sin(theta),cos(theta)]] with 2*theta=atan2(2*b,d-a) diagonalizes by R^T*M*R; a scalar identity block has arbitrary rotation and the numerical API chooses theta=0. These matrix facts establish no fermion mass matrix, Yukawa texture, flavor or family ontology, CKM identity, Cabibbo prediction, CP-phase count, charged-current or GIM mechanism, anomaly result, or substrate realization.

- Accepted in: `v0.30.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-MIX-002

Conditional on the abstract N-by-N unitary relative-basis matrices of C-MIX-001, let the left/right diagonal phase action be V -> D_L*V*D_R^dagger. For a unitary V whose bipartite nonzero-support graph has c connected components, the diagonal-action stabilizer has real dimension c and its orbit has dimension 2*N-c. On the generic connected-support stratum c=1, so the effective orbit dimension is 2*N-1 and the quotient of U(N) has dimension (N-1)^2. Separating the N*(N-1)/2 real-orthogonal angle dimensions leaves (N-1)*(N-2)/2 irreducible complex-phase dimensions; these are zero for N=2 and one for N=3. Every U(2) matrix is diagonal-rephasing-equivalent to a real orthogonal matrix, and every two-row/two-column quartet has zero imaginary part. For any indices, the quartet Q_ik;jl=V_ij*V_kl*conjugate(V_il)*conjugate(V_kj) is invariant under the declared diagonal action and its imaginary part reverses sign under entrywise complex conjugation. For the declared unitary chart V=R23*R13(delta)*R12, Im(Q_01;12) equals cos(t12)*cos(t23)*cos(t13)^2*sin(t12)*sin(t23)*sin(t13)*sin(delta). Disconnected zero patterns and degenerate singular spectra have enlarged basis freedoms and require their own stabilizer audit. These statements establish no quark or generation map, physical CKM matrix, Cabibbo or KM mechanism, physical CP operation or violation, observed family count, charged current, GIM or anomaly result, measured angle or phase, or substrate realization.

- Accepted in: `v0.31.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-MIX-001

## C-MOM-001

Let T^{mu nu} be a smooth symmetric tensor in inertial flat 3+1 coordinates satisfying partial_mu T^{mu nu}=0. Assume localization strong enough that the surface terms for total charges and the coordinate- weighted first and second moments vanish. Define M=integral T^{00} d^3x, P^i=integral T^{0i} d^3x, D^i=integral x^i T^{00} d^3x, and I^{ij}=integral x^i x^j T^{00} d^3x. Then dot M=0, dot P^i=0, dot D^i=P^i, ddot D^i=0, and ddot I^{ij}=2*integral T^{ij} d^3x. Thus the dipole is generally affine in time rather than constant. For normalized STF I_STF=I-delta*Tr(I)/3, ddot I_STF^{ij}=2*integral [T^{ij}-delta^{ij} T^{kk}/3] d^3x. The alternative source convention Q=3*I-delta*Tr(I) is exactly 3*I_STF and has three times this acceleration. Constant translation of the spatial origin leaves ddot I unchanged because ddot M and ddot D vanish. Nonzero boundary flux invalidates the conserved integrated charges, and without T^{i0}=T^{0i}, dot D^i need not equal P^i. These identities establish no gravitational field equation, retarded solution, TT coupling, radiating multipole order, nonzero quadrupole radiation, waveform, power, gravitational coupling, 1+1 contrast, or substrate realization.

- Accepted in: `v0.32.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-MOM-002

Let rho(x,y,z,t)=lambda(x,t)*g(y,z), where lambda is centered on the declared x axis with constant monopole M and longitudinal second moment mu(t), while g is a declared time-independent normalized centered axisymmetric transverse profile with per-axis variance sigma^2. Then the Cartesian second moment is diag(mu,M*sigma^2,M*sigma^2). Writing Delta=mu-M*sigma^2, the normalized trace-free moment is I_STF=diag(2*Delta/3,-Delta/3,-Delta/3), and the triple convention is Q=3*I_STF=diag(2*Delta,-Delta,-Delta). For every positive derivative order n, with M and sigma fixed, d^n I_STF/dt^n=diag(2*d^n mu/dt^n/3,-d^n mu/dt^n/3, -d^n mu/dt^n/3), whose Frobenius norm squared is 2*(d^n mu/dt^n)^2/3; the corresponding triple-tensor norm squared is 6*(d^n mu/dt^n)^2. The TT projection of this derivative tensor vanishes along the symmetry axis. Along a perpendicular declared z direction it is diag(d/2,-d/2,0), where d=d^n mu/dt^n, with normalized plus coordinate d/sqrt(2) and cross coordinate zero in the declared x-y basis. Pure trace additions are annihilated. C-SG-009 supplies an exact longitudinal specialization, but this conditional moment construction establishes no 3+1 field solution, momentum flux or spatial stress, local conservation, stability, gravitational action or coupling, retarded dynamics, radiation, detector observable, or substrate realization.

- Accepted in: `v0.37.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-SG-009, C-MOM-001, C-GW-002

## C-MOM-003

Let rho(r) be any radial density for which J=integral_R3 rho(r)*r^2 d^3x exists, and define I_ij=integral_R3 rho(r)*x_i*x_j d^3x. Exact sphere integration gives integral_S2 n_i*n_j dOmega=(4*pi/3)*delta_ij and hence I_ij=(J/3)*delta_ij. Therefore Tr(I)=J, the normalized tensor I_STF=I-delta*Tr(I)/3 is identically zero, and the triple convention Q=3*I_STF is identically zero. For the axisymmetric deformation rho=f(r)*(1+a*P2(cos(theta))) with the same scalar J, the exact guard is I_STF=diag(-a*J/15,-a*J/15,2*a*J/15) and Q=diag(-a*J/5,-a*J/5,2*a*J/5), which is nonzero when a*J is nonzero and returns to the spherical null at a=0. These are moment-kinematic identities. They define no gravitational dynamics and do not by themselves establish physical radiation, non-radiation, or a required dynamical l=2 channel.

- Accepted in: `v0.40.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-MOM-001

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

## C-PDE-001

Adopt the C-SG-001 normalized sine-Gordon potential as a declared dimensionless 3+1 flat-space radial model with action S=4*pi*integral dt dr r^2[u_t^2/2-u_r^2/2-(1-cos(u))]. Its equation is u_tt-u_rr-2*u_r/r+sin(u)=0, with even regularity u_r(0,t)=0. For initial data u(r,0)=3*exp(-(r/4)^2), u_t(r,0)=0, a direct-radial centered leapfrog on 0<=r<=200 and 0<=t<=450 with dr=0.05, dt=0.02, outer Dirichlet data, and a quadratic velocity sponge over 150<r<=200 gives finite-time simulation evidence for a localized oscillatory core. The mean energy inside r<=30 over 360<=t<=430 is more than 0.9318 of its mean over 120<=t<=180, and the late center half-range is greater than 4.34. Hann-FFT and rising-crossing estimates on windows beginning at t=220 and t=300 all give 0.90<omega<0.94, below the linear threshold one. Center traces on dr=0.1, 0.05, and 0.025 self-converge at approximately second order; closed-box total-energy relative ranges decrease from 1.179e-3 to 2.940e-4 to 7.344e-5. Timestep halving, domains 160/200/240, core-radius diagnostics, a regular soluble linear mode, and an independent DOP853 evolution of v=r*u with Simpson energy preserve the verdict. Changing the radial geometric coefficient or using the A=4, width-three dispersive seed breaks the relevant verdict. This is resolution-bounded evidence for the specified finite-time IVP, not an exact or eternal breather, exponential lifetime law, family-wide stability result, gravitational source or radiation statement, absolute-scale prediction, particle model, or substrate realization.

- Accepted in: `v0.39.0`
- Verification: `simulation_evidence`
- Compatibility: `compatible_extension`
- Dependencies: C-SG-001

## C-PDE-002

For the finite-time radial sine-Gordon branch of C-PDE-001, define the cutoff core energy-radius moment S_R(t)=4*pi*integral_0^R r^4*T00(r,t) dr. On the baseline domain 0<=r<=200, 0<=t<=450, dr=0.05, dt=0.02, and for each core cutoff R=20, 25, or 30, the detrended moment has a resolved dominant frequency near twice the contemporaneous center-field fundamental. On windows beginning at t=220 and t=300, detrended Hann/quadratic FFT and quadratically interpolated prominent-maximum estimates give moment to field frequency ratios between 1.995 and 2.005; the baseline R=30 moment frequencies lie between 1.83 and 1.85 and its relative half-range exceeds 0.25. Meshes dr=0.1, 0.05, 0.025, timestep halving, domains 160/200/240, and an independent dr=0.2 DOP853 method-of-lines route preserve the near-two verdict. The relation is cutoff- and resolution-bounded: at R=40 radiative-shell drift dominates the FFT, and the weak dispersive seed has no combined persistent-core verdict. This is a finite-time scalar diagnostic, not exact frequency doubling, a global moment theorem, conserved charge, gravitational quadrupole, radiation result, or substrate realization.

- Accepted in: `v0.40.0`
- Verification: `simulation_evidence`
- Compatibility: `native`
- Dependencies: C-PDE-001

## C-PDE-003

In the dimensionless 3+1 sine-Gordon model of C-PDE-001, let P(r,t) satisfy the radial equation and let Y=P2(cos(theta)) with Delta_Omega Y=-6*Y. The finite multiplicative ansatz u=P*(1+a*Y) has exact full-field residual sin(P*(1+a*Y))-(1+a*Y)*sin(P)+6*a*P*Y/r^2. Its coefficient at first order in a is Y*(P*cos(P)-sin(P)+6*P/r^2), so the ansatz is not a generic solution; moreover its l=2 coefficient is nonregular wherever P(0,t) is nonzero. The correct infinitesimal ansatz u=P+epsilon*psi(r,t)*Y obeys at first order psi_tt-psi_rr-2*psi_r/r+6*psi/r^2+cos(P)*psi=0, with psi=O(r^2) at the origin. For v=r*psi this is v_tt=v_rr-6*v/r^2-cos(P)*v with v=O(r^3). At second order the multiplicative ansatz contains P4 harmonic leakage because P2^2=P0/5+2*P2/7+18*P4/35. These are exact field-equation statements, not a nonlinear mode-existence, stability, periodicity, gravity, or radiation theorem.

- Accepted in: `v0.41.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-PDE-001

## C-PDE-004

Evolve the C-PDE-001 radial initial data P(r,0)=3*exp(-(r/4)^2), P_t(r,0)=0 together with the regular C-PDE-003 l=2 perturbation psi(r,0)=0.2*(r/4)^2*exp(-(r/4)^2), psi_t(r,0)=0. On the baseline closed domain 0<=r<=80 through 0<=t<=40, a velocity-Verlet evolution of P and v=r*psi with dr=0.1, dt=0.04, homogeneous outer Dirichlet data, and no sponge completes with finite values before boundary reflection. For u=P+epsilon*psi*P2, the first-order energy-density coefficient is h=P_t*psi_t+P_r*psi_r+sin(P)*psi; defining H=4*pi*integral r^4*h dr, exact angular integration gives the triple-STF coefficient Q/epsilon=diag(-H/5,-H/5,2*H/5). The baseline Qzz/epsilon trace has RMS 404.678 and maximum absolute value 680.589, while the final-to-initial mode norm ratio is 0.62297. Meshes dr=0.2, 0.1, and 0.05 give approximately second-order self-convergence of background, mode, Q trace, and closed-box energy error; timestep halving, a causally disconnected domain extension to 100, exact zero/half-amplitude mutations, an exact free spherical-Bessel l=2 box mode, and an independent transformed-variable DOP853 evolution preserve the finite-time nonzero-moment verdict. This is linearized, dimensionless, finite-grid and finite-time simulation evidence for the specified IVP, not a nonlinear stable or periodic l=2 mode, a frequency-doubling result, conserved gravitational source, radiation channel, absolute scale, or substrate realization.

- Accepted in: `v0.41.0`
- Verification: `simulation_evidence`
- Compatibility: `native`
- Dependencies: C-PDE-001, C-PDE-003, C-MOM-003

## C-PDE-005

For the dimensionless three-dimensional radial sine-Gordon equation of C-PDE-001, let H be a finite set of positive odd integers containing one and set u(r,t)=sum_(n in H) a_n(r)*cos(n*omega*t). With S_n[a]=(1/pi)*integral_0^(2*pi) sin(sum_(m in H) a_m(r)*cos(m*tau))*cos(n*tau) dtau, exact Fourier projection gives a_n''+2*a_n'/r+(n*omega)^2*a_n-S_n[a]=0. Odd harmonics give exact half-period antisymmetry. Even radial regularity gives a_n'(0)=0 and the origin curvature law 3*a_n''(0)+(n*omega)^2*a_n(0)-S_n[a](0)=0. In the linear far field each mode obeys a_n''+2*a_n'/r+((n*omega)^2-1)*a_n=0: n*omega<1 is evanescent with rate sqrt(1-(n*omega)^2), n*omega=1 is threshold, and n*omega>1 is radiative with wavenumber sqrt((n*omega)^2-1). A nonzero real radiative one-over-r tail has positive asymptotic energy per unit radial length and hence infinite integrated three-dimensional energy. Thus a sub-threshold fundamental does not localize its higher channels, and a Dirichlet wall on a radiative harmonic fixes a finite-box standing-wave phase rather than proving an infinite-domain finite-energy breather. These exact conditional statements establish no existence, uniqueness, nonzero radiative coefficient, exact periodic solution, lifetime, gravity, particle identity, absolute scale, or substrate realization.

- Accepted in: `v0.46.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-PDE-001

## C-PDE-006

On the C-PDE-005 odd-harmonic system, declare the free branch coordinate a_1(0)=2.5, origin cutoff 0.001, outer radius 40, a decaying Robin condition on the evanescent fundamental, and finite-box Dirichlet data on every radiative harmonic. SciPy adaptive collocation in IEEE float64, initialized with 300 radial points, periodic-DFT projection with 256 temporal samples, tolerance 1e-8, and a fitted frequency constrained to 0<omega<1 completes through retained sets N=1, 3, 5, 7, and 9. The frequencies are 0.976908657117, 0.976876828530, 0.976873949847, 0.976873921614, and 0.976873921394. On a uniform radial audit grid over r<=12 with 1024 temporal phases, the RMS full nonlinear projection remainder falls from 0.105422 to 0.0136221, 0.00145899, 0.000144585, and 1.37187e-5; the N=9 maximum collocation RMS residual is below 1e-8. Initial-mesh 200/300/400, temporal-sample 256/512, and tolerance 1e-8/1e-9 refinements preserve the branch. Walls at radii 30, 40, 50, and 60 keep the fitted frequency within 1e-4 but produce a nonmonotone more-than-twentyfold resonance in the outer third-harmonic r*a_3 RMS, exposing the standing-wave boundary dependence. Independent DOP853 shooting, Gauss-Legendre projected collocation, and second-order finite differences with a three-grid zero-spacing extrapolation reproduce the finite-box core branch and remainder trend. This is numeric evidence for one declared finite-radius, finite-harmonic family point. The central amplitude is not equation-derived, the P3D1 frequency is not an input, and the result establishes no unique eigenfrequency, exponentially localized infinite-domain state, exact or eternal quasibreather, lifetime law, gravity, particle identity, absolute scale, or substrate realization.

- Accepted in: `v0.46.0`
- Verification: `numeric_evidence`
- Compatibility: `compatible_extension`
- Dependencies: C-PDE-005

## C-PDE-007

In the dimensionless radial sine-Gordon convention of C-PDE-005, let H be a finite set of positive odd integers and let u(r,tau)=sum_(n in H) a_n(r)*cos(n*tau), where tau=omega*t. Then u, u_t, and u_r reverse sign under tau->tau+pi, while the canonical energy density T00=(u_t^2+u_r^2)/2+1-cos(u) is invariant. Therefore T00 has half the field period and every odd temporal Fourier coefficient of T00, and of any defined time-independent radial linear functional of T00, vanishes exactly. This selection rule permits only DC and even harmonics; it does not require any allowed coefficient to be nonzero, lowest, or dominant. In particular, for the local single-mode field u=a(r)*cos(tau), the cos(2*tau) coefficient is a_r^2/4-omega^2*a^2/4+2*J_2(a), so the gradient, kinetic, and potential terms can cancel while a higher even coefficient remains nonzero. For every radial energy density with finite second moment, C-MOM-003 gives I_ij=(delta_ij/3)*4*pi*integral r^4*T00 dr and identically zero STF part at each phase. These exact kinematic and Fourier statements do not establish that the ansatz solves the full PDE, a nonzero STF source, physical radiation, gravity, waveform, flux, absolute scale, particle identity, or substrate realization.

- Accepted in: `v0.47.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-PDE-005, C-MOM-003

## C-PDE-008

On the accepted finite-box branch C-PDE-006, define the core radial second energy moment S_12(tau)=4*pi*integral_0.001^12 r^4*T00(r,tau) dr and the real series S_12=a_0+sum_k(a_k*cos(k*tau)+b_k*sin(k*tau)). With central fundamental 2.5, wall radius 40, IEEE float64 adaptive collocation initialized by 300 radial points, 256 projection phases, tolerance 1e-8, a separate 2401-point exact-cutoff radial audit grid, and 512 endpoint-excluded phases, the N=1, 3, 5, 7, and 9 values of a_2 are 666.330281099, 591.504983105, 591.470022142, 591.470478411, and 591.470484284. At N=9 the twice-frequency coefficient supplies 0.999865185 of the resolved even coefficient power, the exact C-PDE-007 rule removes odd coefficients, and the time-averaged core per-axis variance is 7.827021539. Temporal samples 256/512/1024, radial samples 1201/2401/4801, initial BVP meshes 200/300/400, and tolerance 1e-8 versus 1e-9 with 512 projection phases preserve a_2 within 0.008. Across the harmonic ladder, the full nonlinear core remainder falls from 0.105185 to 1.36601e-5 and the full-box energy relative range from 0.0581543 to 9.6871e-7. Independent Gauss-Legendre phase and Simpson radial integration gives a_2=591.468056462. Walls 30, 40, 50, and 60 give core coefficients 591.269664499, 591.470484284, 598.370080354, and 590.990332998 and expose a full-box scalar-variance resonance near wall 50. This is numeric evidence for one cutoff scalar moment on one finite-box, finite-harmonic family point. It establishes no wall- independent or infinite-domain line, exact full-PDE periodic solution, universal nonzero twice-frequency theorem, STF quadrupole, physical radiation, gravity, waveform, flux, absolute scale, particle identity, or substrate realization.

- Accepted in: `v0.47.0`
- Verification: `numeric_evidence`
- Compatibility: `compatible_extension`
- Dependencies: C-PDE-006, C-PDE-007

## C-PDE-009

In the dimensionless radial-background linearization of C-PDE-003, let n=(n_x,n_y,n_z) be a unit direction and use the unnormalized real l=2 angular basis P2(n_z), n_x^2-n_y^2, 2*n_x*n_y, 2*n_x*n_z, and 2*n_y*n_z. Every basis element obeys Delta_Omega Y=-6*Y. Consequently, for any sufficiently differentiable radial background P(r,t), every real m component has the same radial equation psi_tt-psi_rr-2*psi_r/r+6*psi/r^2+cos(P)*psi=0 and the same regular origin law psi=O(r^2); m-degeneracy does not supply a separated frequency, normalization, or mode existence. Replacing cos(P) by a time average Cbar(r) defines a different equation whose exact omitted term is (cos(P)-Cbar)*psi. For P=a(r)*cos(tau), Cbar=J_0(a) and cos(P)-Cbar=-2*J_2(a)*cos(2*tau)+2*J_4(a)*cos(4*tau)-..., with leading small-a term -a^2*cos(2*tau)/4. Thus an eigenfunction of the averaged radial operator is a solution of the full linearized equation only when the displayed pointwise defect vanishes or a separate Floquet argument supplies the missing time dependence. At a positive cutoff epsilon the regular leading series satisfies epsilon*psi_r-2*psi=O(epsilon^4), so zero value paired with nonzero derivative is not nontrivial regular l=2 data. These are exact angular, equation, and regularity statements. They establish no averaged or Floquet eigenmode, bound state, frequency, stability, nonlinear deformation, infinite-domain localization, gravity, radiation, absolute scale, or substrate realization.

- Accepted in: `v0.48.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-PDE-003

## C-QBL-001

Conditional on the dimensionless 1+1 stationary-profile equation f_xx=(1/2-omega^2-f^2/12)f, C-U1-001's stationary phase Psi=f*exp(-i*omega*t), and 0<omega<1/sqrt(2), let kappa=sqrt(1/2-omega^2). Then for every real center x0 the positive localized profile f=sqrt(24)*kappa*sech(kappa*(x-x0)) solves the equation exactly. Within a nonzero ansatz A*sech(k*(x-x0)), the independent sech powers force k^2=1/2-omega^2 and A^2=24*k^2. Its accepted U1 charge is Q=96*omega*sqrt(1/2-omega^2): Q tends to zero at both open endpoints, increases on (0,1/2), reaches its unique maximum 24 at omega=1/2, and decreases on (1/2,1/sqrt(2)). These derivative signs alone establish no VK, spectral, orbital, or nonlinear stability, forced complex ontology, electric charge, particle identity, or substrate realization.

- Accepted in: `v0.27.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-U1-001

## C-QBL-002

Conditional on the dimensionless 1+1 stationary-profile equation f_xx=sin(f)/2-omega^2*f, C-U1-001's stationary phase, and 0<omega<1/sqrt(2), define G_omega(u)=1-cos(u)-omega^2*u^2. The ratio (1-cos(u))/u^2 decreases strictly from 1/2 to 0 on 0<u<2*pi, so there is a unique peak f0 in that interval with G_omega(f0)=0 and G_omega(u)>0 for 0<u<f0. Up to translation and reflection, the positive even localized branch is specified by x=integral_f(x)^f0 du/sqrt(G_omega(u)); it has f(0)=f0, f_x(0)=0, and tends to zero as |x| tends to infinity. Its accepted U1 charge is the finite exact quadrature Q=4*omega*integral_0^f0 u^2 du/sqrt(G_omega(u)). With kappa=sqrt(1/2-omega^2), the scaled field f(x)=kappa*F(z), z=kappa*x, obeys F_zz=F-F^3/12+O(kappa^2), f0/kappa tends to sqrt(24), and Q/(96*omega*kappa) tends to one as kappa tends to zero, recovering C-QBL-001 only in this controlled small-amplitude limit. The claim establishes no elementary closed form, finite-amplitude identity with EM1, VK or nonlinear stability, physical electric charge, particle identity, or substrate realization.

- Accepted in: `v0.28.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-U1-001, C-QBL-001

## C-QBL-003

Conditional on C-QBL-001 and the declared whole-line scalar energy E[f]=integral dx*[f_x^2/2+kappa^2*f^2/2-f^4/48], its positive quartic profile has unconstrained scalar Hessian L=-d_x^2+kappa^2-6*kappa^2*sech^2(kappa*(x-x0)). On L2(R), the complete discrete spectrum below the continuum threshold kappa^2 consists of exactly two simple levels: lambda_0=-3*kappa^2 with even nodeless mode proportional to sech^2(kappa*(x-x0)), and lambda_1=0 with odd one-node mode proportional to sech(kappa*(x-x0))*tanh(kappa*(x-x0)). The zero mode is exactly the translation tangent of the background. A terminating s=2 to s=1 to free partner factorization proves completeness, and the essential continuum begins at kappa^2. The negative and zero Hessian levels are not positive particle masses or generations; this scalar operator alone establishes no fixed-charge, spectral, orbital, or nonlinear Q-ball stability, exact-sine spectrum, Standard-Model quantum numbers, flavor tower, or substrate realization.

- Accepted in: `v0.29.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-QBL-001

## C-RG-001

For positive radius R and density lambda, the circumference line energy E_line = 2*pi*R*lambda is homogeneous of degree one, has constant positive derivative 2*pi*lambda, and has no stationary radius. For positive surface density sigma, E_shell = 4*pi*R^2*sigma is homogeneous of degree two and has radius-dependent derivative 8*pi*R*sigma. For positive line tension T and pressure P, E_cap = 2*pi*R*T - pi*R^2*P + C has the unique strict global maximum R = T/P. Conditional line constructions with coefficients T and the C-SG-002 breather energy share only the degree-one line form; their energies are equal for every positive R if and only if their coefficients are equal.

- Accepted in: `v0.6.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-SG-002

## C-RGE-001

For positive b0, mu0, and g0, a positive coupling on an interval that satisfies the declared one-loop equation mu*dg/dmu=-b0*g^3/(16*pi^2) with g(mu0)=g0 obeys 1/g(mu)^2=1/g0^2+b0*log(mu/mu0)/(8*pi^2). The formal zero of this inverse coupling is Lambda=mu0*exp(-8*pi^2/(b0*g0^2)). Lambda has zero total logarithmic-scale derivative along the declared flow, whereas its partial derivative with respect to mu0 at fixed g0 is Lambda/mu0. For b0>0, 0<Lambda/mu0<1. This conditional theorem does not derive the beta function or b0 and establishes no physical QCD, confinement, or strong-coupling interpretation.

- Accepted in: `v0.19.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-RGE-002

Conditional on C-LIE-001, a nonnegative integer flavor count n_f, and the declared four-dimensional one-loop formula b0=(11/3)*C_A-(4/3)*T_F*n_f for a gauge-plus-ghost term and Dirac fundamentals, exact substitution gives b0=11-(2/3)*n_f. Its zero is n_f=33/2; b0 is positive for integer 0<=n_f<=16 and negative for integer n_f>=17, with b0=7 at declared n_f=6. Combined with C-RGE-001, a positive b0 gives decreasing one-loop ultraviolet running with zero infinite-scale limit. The loop weights, field content, flavor count, perturbative regime, and physical gauge-sector identification are premises; the claim proves neither a substrate/QCD identity, unique SU(3) selection, nor confinement.

- Accepted in: `v0.21.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-LIE-001, C-RGE-001

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

## C-SG-009

For every C-SG-001 rest breather with 0<omega<1, let eta=sqrt(1-omega^2), use the centered spatial coordinate x, and let T00 be the normalized Hamiltonian density of C-SG-002. Its instantaneous scalar second spatial moment is finite and exactly mu(t)=integral_R x^2*T00(x,t) dx =4*pi^2/(3*eta)+(16/eta)*asinh((eta/omega)*sin(omega*t))^2. It is even in time, nonconstant, and has fundamental period pi/omega and therefore base angular frequency 2*omega with only even harmonics of the field frequency. Its cycle minimum is 4*pi^2/(3*eta), at sin(omega*t)=0, and its maximum is 4*pi^2/(3*eta)+(16/eta)*asinh(eta/omega)^2, at |sin(omega*t)|=1. At omega=1/sqrt(2), the exact range is from 4*sqrt(2)*pi^2/3 to 4*sqrt(2)*pi^2/3+16*sqrt(2)*asinh(1)^2. This centered scalar width functional establishes no three-dimensional mass density or STF quadrupole, isolated conserved 3+1 source, gravitational action or field equation, retarded solution, radiated power, detector observable, physical finite-size coupling, or substrate realization.

- Accepted in: `v0.36.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001, C-SG-002

## C-SG-010

At omega=1/sqrt(2), let mu(t) be the exact centered breather energy second moment of C-SG-009, with period T=pi/omega, and define its cosine coefficients a_k=(2/T)*integral_0^T mu(t)*cos(2*k*omega*t) dt for positive integers k. Exact half-period symmetry permits only these even field-frequency harmonics, and Parseval gives <mu'''(t)^2>=(1/2)*sum_{k>=1}(2*k*omega)^6*a_k^2. Resolution-bounded direct adaptive quadrature of the exact third derivative, stable under 4, 8, 16, and 32 interval subdivisions, gives 379.4646380687 < <mu'''^2> < 379.4646380688. Independent sixty-digit manual differentiation and cosine quadrature through sixteen harmonics agree, with a decreasing truncation error before the double-precision floor. The k=1 term, at angular frequency 2*omega, contributes a fraction between 0.8053698716 and 0.8053698718 of the total derivative mean square and is larger than the combined higher-harmonic contribution. These numerical bounds concern this declared frequency and scalar 1+1 moment; they establish no family-wide dominance theorem, three-dimensional source, gravitational coupling, radiated power, waveform, detector signal, or substrate realization.

- Accepted in: `v0.38.0`
- Verification: `numeric_evidence`
- Compatibility: `native`
- Dependencies: C-SG-009

## C-SG-011

Let phi be a sufficiently smooth real field in normalized 1+1 sine-Gordon conventions and define J_plus=phi_t+phi_x and J_minus=phi_t-phi_x. Off shell, d_t J_plus-d_x J_plus=d_t J_minus+d_x J_minus=phi_tt-phi_xx. On the equation phi_tt-phi_xx+sin(phi)=0, both defects are -sin(phi); with d_plus=(d_t+d_x)/2 and d_minus=(d_t-d_x)/2, this is d_minus J_plus=d_plus J_minus=-sin(phi)/2. For orientation epsilon^(01)=+1, the topological current j^mu=epsilon^(mu nu)*partial_nu(phi)/(2*pi) has (j0,j1)=(phi_x,-phi_t)/(2*pi) and identically vanishing divergence by equality of mixed partials, without using the equation of motion. If the spatial boundary limits exist, its charge is Q=[phi(+infinity)-phi(-infinity)]/(2*pi); vacuum limits 2*pi*n give the integer winding n_plus-n_minus, and vanishing asymptotic flux makes Q time independent. Under scalar-field spatial parity phi_P(t,x)=phi(t,-x), j0 is odd, j1 is even, Q changes sign, and the sine-Gordon equation remains invariant. The exact unit kink 4*atan(exp(x-x0)) and its parity image have charges +1 and -1. The small-amplitude sine-Gordon limit is massive Klein-Gordon and retains the characteristic source at first field order. These facts establish neither independently conserved chiral currents nor a selected winding sector, intrinsic parity violation, V-A interaction, weak force, bosonization dictionary, particle identity, or substrate realization.

- Accepted in: `v0.43.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001

## C-SG-012

Let phi be a sufficiently smooth real field in normalized 1+1 sine-Gordon conventions, with signature eta=diag(+1,-1), potential V(phi)=1-cos(phi), Lagrangian density L=(phi_t^2-phi_x^2)/2-V(phi), and residual R=phi_tt-phi_xx+sin(phi). The canonical symmetric tensor T_mu_nu=partial_mu(phi)*partial_nu(phi)-eta_mu_nu*L has covariant components T_00=(phi_t^2+phi_x^2)/2+V, T_01=T_10=phi_t*phi_x, and T_11=(phi_t^2+phi_x^2)/2-V. Raising both indices changes the mixed components to T^01=T^10=-phi_t*phi_x, and its exact off-shell divergences are partial_mu T^(mu 0)=phi_t*R and partial_mu T^(mu 1)=-phi_x*R. Thus local stress conservation follows on shell; integrated charges additionally require appropriate boundary flux conditions. For x_plus=t+x, x_minus=t-x and partial_plus=(partial_t+partial_x)/2, partial_minus=(partial_t-partial_x)/2, the covariant null components are T_pp=(phi_t+phi_x)^2/4, T_mm=(phi_t-phi_x)^2/4, and T_pm=V/2. They obey the exact off-shell balances partial_minus T_pp+partial_plus T_pm=(phi_t+phi_x)*R/4 and partial_plus T_mm+partial_minus T_pm=(phi_t-phi_x)*R/4, while the Cartesian trace is T^mu_mu=2*V=4*T_pm. Scalar-field spatial parity exchanges T_pp and T_mm and leaves T_pm even. Deleting the potential produces a distinct massless model with separately conserved null stresses; it is not the small-amplitude limit of the fixed normalized sine-Gordon theory. These identities establish neither a selected handed sector, quantum chiral anomaly, V-A interaction, weak force, bosonization dictionary, particle identity, nor substrate realization.

- Accepted in: `v0.44.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001, C-SG-011

## C-SG-013

Let phi be a sufficiently regular real scalar field and, at a fixed coordinate point b over a declared interval, define the boundary sign correlation R_b[phi]=integral sign(phi_t(t,b))*phi_x(t,b) dt. Under scalar spatial parity phi_P(t,x)=phi(t,-x), the exact fixed-coordinate pullback is R_b[phi_P]=-R_-b[phi]; at the parity center b=0 this is an odd observable. This differs from an outward-normal boundary channel: parity maps a right half-line and its outward derivative -partial_x to a left half-line and +partial_x, making the simultaneously transformed normal derivative unchanged. For sinusoidal traces phi_t=A*sin(omega*t+alpha) and phi_x=B*sin(omega*t+beta), with real nonzero A, real B, and omega>0, integration over one period gives R=4*sign(A)*B*cos(beta-alpha)/omega. A cosine convention for the second trace instead gives -4*sign(A)*B*sin(beta-alpha)/omega, so the phase convention is load-bearing. Separately, on a right half-line x>=b with orientation epsilon^(01)=+1 and time-independent field at positive infinity, the C-SG-011 topological charge changes by Delta Q=-Delta phi(b)/(2*pi)=-(1/(2*pi))*integral phi_t(t,b) dt. Neither this winding integral nor R implies the other: a complete sinusoidal phi_t period has Delta Q=0 while R can be nonzero, R can vanish for a separately nonzero boundary field change, and R scales continuously with B. For every fixed boundary point the exact C-SG-001 rest breather has zero complete-period R; at its symmetry center phi_x vanishes identically. These results establish a conditional boundary correlation and transformation law, not a topological or conserved charge, quantization, charge-transfer discriminator, parity-invariant or parity-breaking boundary condition, selected state, physical parity violation, chiral anomaly, V-A interaction, weak force, particle identity, or substrate realization.

- Accepted in: `v0.45.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-SG-001, C-SG-011, C-SG-012

## C-SK-001

Conditional on positive premises M_top=48*pi^3*B1*E_e and M_ANW=3*pi^2*B1*F_pi/e, equality M_top=M_ANW holds if and only if F_pi/e=16*pi*E_e. The shared linear hedgehog coefficient B1 cancels exactly; changing either B1 power generally prevents that cancellation.

- Accepted in: `v0.8.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-SYM-001

Let phi be a real nonempty n-entry scalar-coordinate column, let V(phi) be twice differentiable, and let T_a be a finite nonempty supplied family of real n-by-n linear generators. Define the exact infinitesimal invariance residuals r_a(phi)=grad(V)^T*T_a*phi. Direct differentiation gives grad(r_a)=H*T_a*phi+T_a^T*grad(V), where H is the Hessian of V. Therefore, if every r_a vanishes identically and a declared vacuum phi_0 is actually stationary, then H(phi_0)*T_a*phi_0=0 for every supplied generator. The rank of the matrix whose columns are the actual tangents T_a*phi_0 is the number of independent Hessian zero directions certified by these premises. The kernel dimension of the coefficient-to-tangent map is a stabilizer dimension only when the supplied generator matrices form an independent basis; dependent labels cannot inflate the rank. If a separately supplied symmetric kinetic metric K is provably positive definite, the same tangents are zero directions of the generalized quadratic mass operator K^-1*H. Positive K preserves but does not create Hessian zeros. At a nonstationary point, under explicit symmetry breaking, or without an independent generator basis, the corresponding conclusion or interpretation does not follow. This is an exact conditional finite-dimensional classical quadratic theorem. It supplies no quantum Goldstone-particle theorem, no field-theory vacuum or charge algebra, no spectral pole, no group or representation selection, no physical field identification, no mass scale, and no substrate realization.

- Accepted in: `v0.54.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-TH-001

For every real dimensionless splitting x, the normalized upper-state occupation of Z = 1 + exp(-x) is P = exp(-x)/Z = 1/(1+exp(x)). Its Bernoulli variance is P*(1-P) = sech(x/2)^2/4, and the conditional symmetric gate W = 2*P*(1-P) = sech(x/2)^2/2. W is even, has unique global maximum 1/2 at x = 0, decreases strictly with |x|, and tends to zero as x tends to either infinity. A shape A*sech(x/2)^2 equals 2*A*W; this identity does not determine the independent amplitude A.

- Accepted in: `v0.5.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-TOP-001

For integer winding under addition, p(w)=(-1)^w is a homomorphism from Z to the multiplicative signs {+1,-1}. Even winding has label +1 and odd winding has label -1. Adding any even winding, including zero, preserves the label; adding odd winding flips it. This is a mathematical winding character only. Without a separately accepted physical representation it determines no exchange statistics, spin, fermion or boson identity, baryon number, internal or electric charge, or existence of a composite.

- Accepted in: `v0.17.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-TOP-002

In C-LIE-001's fundamental trace convention, let theta=U^dagger*dU for a smooth SU(3)-valued map. The exact invariant Chevalley-Eilenberg differentials have rank(d_2)=20 and rank(d_3)=35, so the degree-three cocycle kernel has dimension 21 and H^3 has dimension one. The real cochain Alt Tr(theta^3) has nine nonzero components, squared coefficient norm 9, is closed, and is not in image(d_2), since adjoining it raises the image rank from 20 to 21. On the unit quaternion sphere oriented as the boundary of (a0,a1,a2,a3), the upper-SU(2)-block map q(a)=a0*I+i*(a1*sigma1+a2*sigma2+a3*sigma3) embedded in SU(3) has a first-column real coordinate map of determinant and degree +1, hence is a pi_3(SU(3)) generator under the audited stable inclusion criterion. Its exact oriented tangent density is Alt Tr(theta^3)=12 and its raw period is 24*pi^2. Therefore omega_3=-Alt Tr(theta^3)/(24*pi^2) has period -1 on that positive generator. With epsilon^(0123)=+1, the corresponding coordinate current J^mu=-(1/(24*pi^2))*epsilon^(mu nu rho sigma)*Tr(L_nu L_rho L_sigma), L_mu=U^dagger*partial_mu U, is identically conserved for every smooth U: the full graded derivative reduces by Maurer-Cartan flatness to the alternating trace of four one-forms, which vanishes by graded cyclicity. For the static upper-block hedgehog U=cos(F(r))*I+i*sin(F(r))*rhat.sigma, its local density for r>0 is -sin(F)^2*F'/(2*pi^2*r^2), its angularly integrated radial density is -2*sin(F)^2*F'/pi, and its charge is [F-sin(F)*cos(F)]_(outer)^(inner)/pi. Smooth constant endpoint data F(0)=n*pi and F(infinity)=0 therefore give charge n, while reversing orientation reverses the charge. This is a mathematical winding-current theorem. It is not by itself a Noether current, gauged-WZW-response current, physical baryon current, anomaly, identification with N_c, representation selection, absolute-scale statement, or substrate realization.

- Accepted in: `v0.52.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-LIE-001

## C-U1-001

For an independently declared smooth complex scalar Psi on 1+1 Minkowski spacetime with signature (+,-), define the raised current j^mu=i*(Psi_conj*d^mu(Psi)-Psi*d^mu(Psi_conj)). Off shell it obeys the exact identity d_mu*j^mu=i*(Psi_conj*Box(Psi)-Psi*Box(Psi_conj)). If the conjugate equations of motion have Box(Psi)=F(|Psi|^2)*Psi with real F, the current is conserved on shell. A genuinely real field has zero current. For the separately declared stationary ansatz Psi=f(x)*exp(-i*omega*t) with real f and omega>0, the current is (j^0,j^1)=(2*omega*f^2,0); adding a real phase-breaking conjugate-field term lambda*Psi_conj to the equation gives divergence -2*lambda*f^2*sin(2*omega*t), which is generally nonzero.

- Accepted in: `v0.14.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-U1-002

Conditional on the independently declared profile Psi=A*sech(eta*x)*exp(-i*omega*t), with A>0, 0<omega<1, and the shared parameterization eta=sqrt(1-omega^2), the C-U1-001 charge is Q=4*A^2*omega/eta. It is positive and strictly increasing, tends to zero as omega approaches zero, and diverges in magnitude as omega approaches one. Composing with C-SG-002 energy E and C-SG-006 secant scale H=E/omega gives Q*E=64*A^2*omega and Q*H=64*A^2. Conditional on carrying Q as the same internal scalar through C-SG-008's boost, the division-free relation Q*(E,P)=64*A^2*(Omega,k) holds, including at rest. For integer exponents, every frequency-independent monomial Q^a*H^b*E^c*omega^d has (a,b,c,d)=(a,b,a-b,b-a), generated by Q*H and Q*E/omega; their ratio is the defining identity H=E/omega. The value 64 assumes A=1 and is not a normalization-independent physical constant.

- Accepted in: `v0.14.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-U1-001, C-SG-002, C-SG-006, C-SG-008

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

## C-VTX-001

For positive g, lambda, and v and positive integer n, declare the radial Abelian-Higgs convention phi=f(r)*exp(i*n*theta), A_theta=a(r)/(g*r), and energy per unit length 2*pi*integral r*dr*[f'^2/2+f^2*(n-a)^2/(2*r^2) +(a'/r)^2/(2*g^2)+lambda*(f^2-v^2)^2/4]. Exact variation gives f''+f'/r-f*(n-a)^2/r^2-lambda*f*(f^2-v^2)=0 and a''-a'/r+g^2*(n-a)*f^2=0. If f approaches v, finite angular energy uniquely requires a to approach n; the declared connection then has flux 2*pi*n/g, while the ungauged positive-winding profile has a logarithmic divergence. Vacuum linearization gives vector and scalar inverse lengths g*v and v*sqrt(2*lambda), both tending to zero as v tends to zero. This conditional model establishes no substrate, dual, chromoelectric, QCD, or confinement identity and no vortex existence.

- Accepted in: `v0.23.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-VTX-002

Conditional on C-VTX-001 with (v,n,lambda,g)=(1,1,2,1), there is resolution-bounded numerical evidence on truncated radial domains for a nontrivial monotone solution with f(epsilon)=a(epsilon)=0 and f(R)=a(R)=1 and finite positive tension approximately 4.21160. The reference collocation solve uses epsilon=1e-4, R=20, 120 initial points, tolerance 1e-8, at most 100000 nodes, maximum RMS residual below 1.1e-8, and uniform 20001-point trapezoidal energy quadrature. Tightening tolerance reduces tension error; R from 10 through 25 agrees within 1e-5; inner-cutoff error decreases from 1e-2 toward 1e-4; exponential and rational guesses converge to the same branch; matched dimensionless v=1 and v=2 domains give tension ratio four within 1e-5. Independent central finite differences at 101, 201, and 401 points give tensions 4.19212, 4.20658, and 4.21037. This is numeric evidence, not a continuum existence or uniqueness theorem, absolute tension, or physical confinement result.

- Accepted in: `v0.23.0`
- Verification: `numeric_evidence`
- Compatibility: `compatible_extension`
- Dependencies: C-VTX-001

## C-WIL-001

For positive separation R, Euclidean duration T, and coefficient sigma, conditional on the separately declared rectangular loop expectation W_A(R,T)=exp(-sigma*R*T), the extraction V(R)=-lim_{T->infinity} log(W_A)/T gives V(R)=sigma*R, with derivative sigma and zero second derivative. Separately, for positive rho, the declared perimeter law W_P(R,T)=exp(-2*rho*(R+T)) gives V(R)=2*rho and zero separation derivative. These exact implications derive neither loop law, do not select the area law from center algebra, and establish no physical string tension, gauge phase, or confinement mechanism.

- Accepted in: `v0.25.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-WZW-001

In the explicit fundamental SU(3) convention of C-LIE-001, let E_a=i*T_a, so E_a is anti-Hermitian and [E_a,E_b]=-f_abc*E_c, and define the real left-invariant five-cochain Omega_5=-i*Alt Tr(theta^5), where theta=g^{-1}dg and Alt is the unnormalized signed permutation sum with no hidden 1/5! factor. The exact Chevalley-Eilenberg differentials built from those structure constants obey d_5*d_4=0, have rank(d_4)=35 and rank(d_5)=20, and hence have a 36-dimensional degree-five cocycle kernel and one-dimensional invariant fifth cohomology. Omega_5 has nine nonzero basis components, squared coefficient norm 75/4, obeys d_5*Omega_5=0, and is not in image(d_4): appending it raises the image rank from 35 to 36, while independently Omega_5^T*d_4=0 and Omega_5^T*Omega_5=75/4. Because SU(3) is compact and Omega_5 is left invariant, a hypothetical global primitive could be averaged with normalized Haar measure to an invariant primitive; the exact non-image result therefore makes Omega_5 globally non-exact without assigning any period normalization. The density is a local, metric-free polynomial in a smooth group-valued map and its first derivatives. For an ungauged variation delta U=U*v, delta Tr(theta^5)=d(5*Tr(v*theta^4)); this is an exact boundary identity. If two compatible oriented fillings have integrals I_B and I_Bprime, their glued closed-cycle period is I_B-I_Bprime and the extension phase ratio for coefficient c is exp(i*c*(I_B-I_Bprime)); filling independence follows only under the additional premise that c times every allowed period lies in 2*pi*Z. The theorem fixes no generator period, integer level, WZW coefficient, N_c, baryon current or charge, gauge connection, Chern-Simons descent, anomaly inflow, representation selection, physical bulk or boundary dynamics, absolute scale, or substrate realization.

- Accepted in: `v0.50.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-LIE-001

## C-WZW-002

In C-WZW-001's convention Omega_5=-i*Alt Tr(theta^5), orient the unit S^5 as the boundary of the unit ball in (Re z1,Im z1,Re z2,Im z2,Re z3,Im z3). The explicit Puttmann-Rigas map eta(z)=z*z^T+A(conjugate(z)), with A(conjugate(z)) the displayed complex cross-product matrix, obeys eta^dagger*eta=I and det eta=1 on |z|=1. The regular value (1,0,0) of its first-column projection has exactly the preimages +(1,0,0) and -(1,0,0), both with oriented real Jacobian determinant 8, so the projection has degree +2. By the audited U(n-1)->U(n)->S^(2n-1) generator criterion, eta is the positive generator of pi_5(SU(3))=Z. Equivariance makes eta^*Omega_5 an invariant top form on S^5. On the positive tangent frame at (1,0,0), exact evaluation gives Alt Tr(theta^5)=-480*i and Omega_5=-480; since Vol(S^5)=pi^3, the oriented primitive periods are -480*i*pi^3 for the raw trace and -480*pi^3 for Omega_5. Consequently a map in homotopy class n has real sphere period -480*pi^3*n. For two oriented five-ball fillings of a common S^4 boundary whose glued map has winding n, for real k the coefficient c=k/(240*pi^2) gives phase ratio exp(-2*pi*i*k*n)=1 for all integer n exactly when k is an integer; orientation reversal changes the period sign but not this lattice. This is a mathematical sphere-filling level theorem. It does not fix periods on arbitrary closed five-manifolds, identify k with N_c, or establish a WZW action from substrate dynamics, baryon number, representation selection, a gauge anomaly, descent, inflow, absolute scale, or any physical realization.

- Accepted in: `v0.51.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-WZW-001
