## P240 current candidate: exact results and request for independent validation

After 40 fresh P240 attempts for the objective in #146, we have a concrete
candidate from the families in #147:

$$
\mathcal{L}=-\frac{1}{2}F_{\mu\nu ab}F_{\rho\sigma cd}
\eta^{\mu\rho}\eta^{\nu\sigma}h^{ac}(M)h^{bd}(M)-V_{\mathrm{M5.17}}(M),
\qquad
h^{ab}=\eta^{ab}-2P_t{}^a{}_c\eta^{cb},
$$

used in the fixed-$J$ two-clock sector

$$
E_J=E_{\mathrm{stat}}+\frac{1}{4}J^{T}I^{-1}J.
$$

### What the candidate has passed

- Exact proper-Lorentz covariance on the simple timelike spectral branch.
- Exact recovery of the complete arbitrary static 3x3 action, hence no change
  to its spatial/Coulomb coefficient.
- A positive curvature Hamiltonian and exact repair of the explicit negative
  affine-clock sign, without a fitted interpolation coefficient.
- Exact fixed-$J$ interaction algebra: for equal like clocks,
  $\Delta E_J=-j^2C/[2I_0(I_0+C)]$. Therefore
  $C(r)=A/r+O(r^{-2})$, $A>0$, implies an attractive Newton-form tail.
  Fixed $\omega$ has the opposite leading sign and is not an equivalent
  validation ensemble.
- An exact pole-free hedgehog chart with
  $\Delta=d(r)\sin^2\theta$, $q=O(r^2)$, and $d=O(r^4)$.

The same-order constant-coefficient family was also exhausted afresh on the
actual symmetric-derivative source image: its full static-preserving subspace
is blind to a negative affine clock. That is why the field-dependent Cartan
contraction is a substantive move rather than numerical tuning.

### What the numerical evidence currently says

Direct float64 PyTorch 2.4/CUDA Euler-Lagrange roots exist through a smooth
6x5 basis. The 6x5 root has relative gradient $6.8\times10^{-15}$, positive
finite inertia $0.4607$, and finite frequency $1.0853$. It is not the
desired stable electron: its lowest Hessian eigenvalue is $-2.8681$, and an
independent centered-energy curvature gives $-2.8680$. The mode is 98.4%
in the physical tangential-split field. At the same time, withheld-mode
residuals remain sizeable, so separating a continuum instability from
representation sensitivity is not straightforward.

This branch-specific saddle does not undo the exact action/mechanism results
or demote the candidate. It means P240 has not established the stable
one-body claim.

### Help requested

We would value an independent validation using a materially different
representation or validated-numerics method, focused on two questions:

1. Does the tangential-split negative mode persist for the continuum
   admissible hedgehog, or is there another stable finite-inertia stationary
   branch?
2. If a stable branch exists, do separately relaxed two-defect fields at fixed
   individual $J$ produce positive
   $I_{12}(r)=A/r+O(r^{-2})$?

A Cartesian finite-element, independent spherical collocation, interval
Newton/Morse-index calculation, or another direct stationary-field method
would be especially useful. The goal is independent physics validation, not
reproduction of P240's thresholds or another optimizer-loss comparison.

No P239/P236 receipt or historical numerical value is being carried into this
request, and no claim promotion or closure of #146 is asserted.
