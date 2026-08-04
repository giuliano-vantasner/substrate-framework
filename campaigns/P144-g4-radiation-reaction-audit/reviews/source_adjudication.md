# G4 source adjudication

G4 is qualified, not accepted wholesale. Native NumPy 2.5.1 execution reaches
four passing predicates and stops only because the immutable source calls
`np.trapz`. An isolated alias to `np.trapezoid` leaves the source unchanged,
exits cleanly, and reports all ten checks passing. That is a compatibility
event only; it neither helps nor harms the scientific verdict.

The headline self-force is not independently derived. G4 imports
`P_rad=(kappa/8)*Edot**2`, solves `F_self*v=-P_rad`, and writes the expanded
quotient on another line. No retarded self-field, field momentum flux,
regularization, source equation, near-field energy, or causal history is
computed. The dossier explicitly acknowledges that `-P_rad/v` is not an
independent derivation, while the executable source nonetheless labels the same
coefficient expansion an ALD or Ford-O'Connell route.

The power premise also lacks accepted authority. C-RAD-001 rejected G1's extra
source derivative and factor-four flux normalization and deliberately supplies
no accelerated breather or reaction law. Under C-RAD-001's separately declared
scalar action with `A=1/kappa`, `B=c=1`, the total power for the same source
amplitude is `kappa*q**2/2`, four times G4's inserted value. This comparison
does not replace G4's power; it proves that its coefficient cannot be borrowed
from the accepted claim.

The numeric leg prescribes `v(t)=0.6*tanh(0.8*t)`, integrates
`d(gamma*E0)/dt`, and numerically differentiates the result. The prescribed
energy increases as the external trajectory accelerates. No force appears in
the evolved right-hand side, solver success is unchecked, and no refinement or
independent method is run. It is a same-input regression, not radiation-damped
source dynamics.

The internal-mode branch first time-averages the sine-Gordon kernel and then
uses its spatial cosine transform as an oscillatory source amplitude. A time
average has no nonzero temporal harmonic by itself. The assigned internal power
contains no internal amplitude, phase, or rate and would remain nonzero even
when an omitted mode amplitude is set to zero. Its selected slow-point
hierarchy therefore does not establish internal backreaction. The finite-k
rolloff survives only as numeric evidence about the declared static kernel.

The corrected positive object is C-RR-001. For an exact nonzero generalized
rate vector `u`, supplied nonnegative power `P`, and separately declared
positive-definite coordinate metric `G`,
`Q0=-P*G*u/(u.T*G*u)` has `Q0.T*u=-P`. Every balanced force is `Q0+z` with
`z.T*u=0`; the displayed `Q0` is the unique minimum of
`Q.T*G**-1*Q`. Thus one scalar power does not select multiple force
components. In one coordinate, `Q=-P/u` is unique only for nonzero `u`. At
zero rate, positive power is inconsistent and zero power leaves force
arbitrary.

A separate declared Rayleigh model closes conditionally. For symmetric
positive-semidefinite `D`, `R=u.T*D*u/2`, `Q=-D*u`, and
`P_diss=u.T*D*u=2R>=0`; the open energy ledger is
`E_dot=Q_ext.T*u-P_diss`. This is a complete exact effective dissipation
theorem, but it does not infer `D` or `P` from radiation.

Decision: promote C-RR-001 and qualify G4 through that theorem plus the narrow
accepted ceilings of its adjudicated dependencies. Do not promote G4's
radiated power, self-force coefficient, ALD/Ford-O'Connell label, runaway or
preacceleration claims, accelerated breather, internal power, hierarchy,
gravity, material, or substrate interpretation. Primary and independent exact
derivations, coefficient and metric mutations, zero-rate and external-work
countermodels, the frozen source graph, and explicit compatibility replay leave
no hidden debt in the qualified result.
