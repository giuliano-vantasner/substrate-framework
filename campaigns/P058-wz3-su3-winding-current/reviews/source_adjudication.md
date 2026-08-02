# WZ3 source adjudication

WZ3 contains a recoverable exact trace-three and hedgehog calculation, but its
seven-check tally does not establish the advertised gauged-WZW, physical
baryon, or color-count conclusions. The source is therefore qualified rather
than accepted wholesale or discarded.

## Reproduction boundary

The SHA-256-pinned file at `substrate@6d1f4e0` fails natively under NumPy 2.5.1
after two symbolic checks because `np.trapz` is absent. A one-run compatibility
shim assigning the historical name to `np.trapezoid` leaves the source file
unchanged and reaches `ALL 7 CHECKS PASS`. That replay is provenance evidence,
not a promotion oracle.

## Surviving mathematics

The explicit Pauli-matrix calculation correctly finds the magnitude of the
hedgehog trace-three density and the boundary antiderivative. P058 repairs the
orientation once, before evaluation: with `epsilon^(0123)=+1`, left current
`L=U^dagger*dU`, and normalized form `-Tr(L^3)/(24*pi^2)`, a profile decreasing
from `F(0)=pi` to `F(infinity)=0` has charge `+1`. The canonical construction
derives the coefficient from an independent quaternion generator whose raw
period is `24*pi^2`; it also proves the trace-three cohomology and conservation
without an equation of motion. The charge is an exact boundary functional, so
the pending S2 shooting ODE is unnecessary.

## Sign discontinuity

WZ3's headline uses `+(1/(24*pi^2))*epsilon*Tr(L^3)` with
`epsilon^(0123)=+1`. Its own exact trace then gives radial integrand
`+(2/pi)*sin(F)^2*F'`, whose integral is `-1` for `F:pi->0`. The script sets
`NUMERIC_SIGN=-ORIENT` only after deriving that result and integrates the
opposite sign to obtain `+1`. Calling the sign a freely chosen orientation at
that point changes the earlier declared current rather than auditing it. P058
keeps one convention throughout and records orientation reversal as a charge
sign flip, not a conservation failure.

## Conservation oracle

The fully alternating trace of four generic matrices does vanish by graded
cyclicity and is a useful kernel. WZ3 does not construct the three graded
Leibniz terms or substitute Maurer-Cartan flatness, however. Its advertised
"wrong epsilon sign" guard is actually an all-positive symmetrized product.
Reversing epsilon orientation multiplies the current by minus one and preserves
conservation; removing antisymmetry defines a different object. P058 expands
the derivative terms and tests closure, sign, and loss of antisymmetry as
separate predicates.

## Degree and response claims

WZ3 sets `pi3_baryon=round(B_unit)` and checks tuples containing topology
names, group strings, and literal orders. It never computes a degree witness,
compactification gate, external U(1) source, gauged WZW action, functional
variation, or descent equation. P058 instead certifies the SU(2) quaternion
block by a degree-one column projection independently of the trace integral.
The resulting integer is a mathematical winding. The physical baryon
interpretation in Witten's QCD effective theory is contextual literature, not
an accepted framework dependency.

## Anomaly and color claim

WZ3 inserts `Q_u=2/3`, `Q_d=-1/3`, a target amplitude normalized to one, and
the literal `n_value=3`; it then verifies `N_c*(Q_u^2-Q_d^2)=N_c/3`. It does not
derive a gauged WZW vertex, load a measured decay width, establish `n=N_c`, or
allow charges to vary consistently with a general color count. Baer and Wiese,
Nucl. Phys. B 609 (2001), DOI `10.1016/S0550-3213(01)00288-7`, show that the
neutral-pion two-photon width does not reveal `N_c` after anomaly-consistent
charges and the Goldstone-Wilczek contribution are included. P058 independently
checks the elementary cancellation
`N_c*(Q_u^2-Q_d^2)=1` for
`Q_u=(1+1/N_c)/2`, `Q_d=(1/N_c-1)/2`. Thus WZ3's arithmetic is conditional on
fixed inputs and cannot force `n=N_c=3`.

## Disposition

WZ3 maps only to C-TOP-002's exact mathematical trace-three, conserved-current,
and hedgehog-charge theorem. Its S2 profile reuse, S3 baryon semantics, local
WZW response, anomaly matching, electromagnetic vertex, `n=N_c=3`, physical
color count, representation statements, absolute scale, and substrate
realization remain unaccepted. The structured migration disposition is
`qualified` with these exclusions and durable evidence paths.
