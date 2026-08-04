# WM6 Source Adjudication

WM6 contains a sound conditional numeric core. With C-RGE-005's supplied
gauge-only coefficients, exact equal high-boundary ratios, reference scale,
and two low inverse-coupling constraints, the inverse-alpha ODE has a converged
positive shooting solution. The canonical result is boundary inverse
41.34452533, log span 29.14158615, high scale about 4.13015e14 in the supplied
scale unit, and readout 0.210641136. This is numeric evidence for a declared
inverse problem, not an ab-initio physical prediction.

The canonical route declares DOP853, tolerances, positive log shooting
variables, root status, residual norm, and trajectory positivity. Tolerance
tightening and Radau agree. A fresh reviewer solves direct gauge couplings with
Radau and a separate root method. Both routes first reproduce C-RGE-004's exact
zero-matrix amplitude, span, and readout. Sign, transpose, boundary-ratio, and
low-input mutations all change the result; reference-scale rescaling changes
only the reported high scale.

The source leaves `solve_ivp` at SciPy 1.18's RK45 default, checks no positive
trajectory, and does not gate headline residual norm. Its exact-language check
uses rounded literals. The 0.21064 headline is itself a hard-coded regression,
and pending SM4's broad scale window validates nothing.

The measured weak coordinate is absent from the shooting residual, so the core
data gate survives. It nevertheless has thirteen AST loads and influences
checks 5, 7, 8, 9, and 11. That contradicts the prose claiming exactly two uses
and no comparator-dependent pass condition. Miss percentages remain permitted
post-solve descriptions, not claim or solver validation.

Scaling the entire two-loop matrix produces the source's comparator-dependent
inverse `k=8.7483`; changing the target to 0.22 changes k to 4.2836. Unknown
higher orders have independent tensor directions, and finite matching offsets
change the readout without changing b or B. The fitted k therefore proves no
all-orders, threshold, boundary, or physical impossibility. Check 8 computes
none of the effects it lists.

C-RGE-006 accepts only the status-gated conditional running object, exact
one-loop containment, method agreement, covariance, and sensitivity. WM6 is
qualified; no full Standard Model, preferred concurrence boundary, physical
input provenance, unification, observation, all-orders no-go, debt closure, or
substrate mechanism is accepted.
