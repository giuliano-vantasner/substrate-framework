# P239 conditional spectral-Cartan action

Let `M_ab` be the real symmetric covariant M5 field, let
`X^a_b=eta^{ac}M_cb`, and restrict to the open branch on which `X` has a
simple real timelike eigenline continuously connected to the preferred
vacuum `g` eigenline. Its spectral idempotent is

\[
P_t(X)=\prod_{s\ne t}\frac{X-\lambda_s(X)\mathbf 1}
                              {\lambda_t(X)-\lambda_s(X)}.
\]

The eigenvalues here are the local eigenvalue branches of `X`; they are not
frozen target constants away from the vacuum. Define

\[
h^{ab}(M)=\eta^{ab}-2P_t{}^a{}_c\eta^{cb}.
\]

For a normalized timelike eigenvector `u`, `P_t=-u(eta u)^T` and therefore
`h^{ab}=eta^{ab}+2u^a u^b`. This inverse Cartan metric is positive definite.
It is local and algebraic in `M` on the stated simple-spectrum branch, and it
transforms as a contravariant two-tensor because the spectral idempotent
transforms by similarity.

The candidate action is

\[
\mathcal L_{\rm SC}=
-\sum_{\mu<\nu}\eta^{\mu\mu}\eta^{\nu\nu}
 F_{\mu\nu ab}F_{\mu\nu cd}h^{ac}h^{bd}
-V_{\rm spec}(M),
\]

in the pinned diagonal mostly-plus convention, with positive weights in
`V_spec`. Covariantly, the spacetime pair is contracted with `eta` and the
internal pair with `h`. This is an explicit local Lorentz scalar. Since `h`
depends on `M` but not on its derivatives, the M5.18 homogeneous-quadratic
Legendre step gives

\[
\mathcal H_{\rm SC}=
\sum_{\mu<\nu}F_{\mu\nu ab}F_{\mu\nu cd}h^{ac}h^{bd}
+V_{\rm spec}(M)\ge 0.
\]

In the vacuum eigenframe, `P_t=diag(1,0,0,0)` and `h=I_4`: the construction
is exactly the healthy Frobenius internal contraction there. Unlike a fixed
`I_4`, it remains Lorentz covariant because `h` follows `M`. For every
time-row-uniform spatial field, the same projector is fixed and the internal
curvature has only spatial entries, so the complete M5.17 3x3 action is
recovered with the original coefficient. The established static Coulomb
sector is therefore retained at the action level.

The verifier also applies the action to an explicit negative clock direction
built from symmetric M5 field derivatives. The old coefficient is negative;
the spectral-Cartan coefficient is its exact positive sign reverse. At fixed
angular momentum, any stationary branch with finite positive inertia obeys
`omega=J/(2I)`, but this algebraic implication is not yet evidence that the
fully relaxed hedgehog branch exists. That numerical construction and the
relaxed two-defect force remain separate campaign gates.
