# P098 source adjudication

MC4 reproduces all five runtime checks, but it does not add a distinct accepted
claim. The gapped simulation is initialized with the exact C-SG-017 physical
breather, so its finite-grid persistence, sub-gap frequency, and width are
solver regression of an already exact solution rather than a numerical
existence construction.

The two `ell` runs scale the domain, grid, timestep, final time, sponge, core
radius, and seed together. They are exactly the same normalized discrete
trajectory. The source nevertheless measures width with
`u_x^2 + 1-cos(u)`, omitting the inverse-`ell^2` coefficient on the onsite
term. That proxy is not scale covariant and yields the reported 1.8365 ratio.
The independent physical-coordinate route obtains 1.841437 for the same
defective proxy and exactly 2.0 for the Hamiltonian-covariant diagnostic.

The source's FFT values are the eleventh bins of rescaled late windows; it
checks no dominance fraction or endpoint closure. Its two resolution levels
co-refine space and time and establish no observed order. P098's canonical
repair uses four spatial levels, three timesteps, three domains, exact
phase-space errors, energy drift, and DOP853. It converges at second order,
reaches 0.284 percent final phase-space error, and gives 0.153 percent
cross-time-method agreement. This is controlled simulation regression, still
not a new physical claim.

The gapless run truthfully shows that its selected zero-field,
localized-velocity data transport energy out of a fixed core. It does not show
that every gapless medium lacks localized fields: C-SG-018 and both P098 exact
routes exhibit `sech(x-c*t)`, a localized finite-energy wave packet. Nor does
the comparison establish that a positive mass gap alone is sufficient for a
nonlinear state, material realization, or stability theorem.

MC4 is therefore qualified and maps C-MED-003, C-SG-017, and C-SG-018. Its
runtime reproduction and repaired numerical study remain durable evidence;
its noncovariant width measurement, universal gapless language, material
reading, and infinite-time implications are excluded. No release or canonical
API changes, and every new sampled integration uses the shared compatibility
helper rather than `np.trapz` or `np.trapezoid`.
