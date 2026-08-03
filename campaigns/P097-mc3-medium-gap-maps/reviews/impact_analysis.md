# P097 impact analysis

P097 adds a physical-coefficient layer to the existing scalar-lattice module
and a separate mixed-coordinate sine-Gordon module. It changes no accepted
symbol, equation, normalization, coefficient definition, or prior claim. The
new APIs are pure exact-symbolic functions; imports execute no simulation and
print no tally.

The direct changed consumers are `src/substrate_framework/__init__.py`, the
two focused test modules, the P097 primary verifier, and its independent
review. C-LAT-001 remains the normalized Riemann-action and continuum-limit
claim. C-MED-003 and C-SG-018 remain the physical continuum cosine-field and
Klein-Gordon spectrum claims. C-SG-017 remains the nonlinear continuum
breather existence claim. P097 does not infer a discrete nonlinear solution
from any of them.

The physical chain uses a per-site energy Lagrangian for a dimensionless phase
and therefore introduces phase inertia `I`, coupling energy `K`, on-site
energy `V0`, and spacing `a`. A declared displacement `q=b*u` gives
`I=m*b**2` and, when a displacement stiffness is supplied, `K=kappa*b**2`.
This extends rather than changes the normalized C-LAT-001 convention.

The mixed equation `theta_z_tau=g*sin(theta)` is kept separate from the
continuum lab-coordinate equation because its coefficient, characteristic,
and normalization freedom differ. The explicit map derives a normalized
hyperbolic sine-Gordon equation only after choosing scales with `g*L*T=1`;
it does not identify `g`, an absorption coefficient, or a laboratory gap.

Hash-pinned consumers MC4, MD1, `medium_omega0.py`, `lifetime_kernel.py`,
`seeding_kernel.py`, and `commensurate.py` remain pending or noncanonical.
They add simulation, dimensional measure, material, damping, population,
spectral, radiation, or engineering assumptions. The migration disposition
changes only MC3 from pending to qualified and maps it to the two narrow new
claims. Generated documentation, accepted memory, release memory, and the
migration queue must be regenerated from the authoritative records.

Exact P097 work contains no NumPy dependency or trapezoidal alias. The direct
`np.trapz` calls in the immutable external `seeding_kernel.py` are recorded for
that source's future migration, and MC4's local compatible fallback remains
pending migration to `trapezoid_integral`. Neither is a consumer of the new
exact implementation and neither creates debt in C-LAT-002 or C-MED-004.
