# T2A Source Adjudication

T2A's twelve checks reproduce. Its scalar pullback uses the standard boost,
and the exact field, integrated energy and momentum, invariant dispersion, and
off-shell stress-divergence factorization are correct. Those results are
already governed by C-SG-001, C-SG-002, C-SG-008, and C-SG-012.

The source's nonrelativistic momentum guard usefully rejects `P=E0*v`, but its
detail line calls the enhancement `gamma^2`. The actual ratio
`(gamma*E0*v)/(E0*v)` is `gamma`; at `v=0.8` it is `5/3`, not `25/9`.
The numerical charge values themselves agree with the accepted formula.

## Tensor Index and Standing-Source Audit

The canonical stress convention is load bearing. In signature `(+,-)`, the
covariant mixed component is `T_tx=phi_t*phi_x`, while the contravariant
momentum density is `T^0x=-phi_t*phi_x`. T2A computes the latter and then calls
it `T_tx` in its dilaton-source section. Its absolute-value predicate hides the
sign and index error.

More seriously, the standing breather does not have pointwise mixed stress zero
identically. Its integrated momentum vanishes by spatial parity, but
`phi_t*phi_x` is nonzero at generic spacetime points. The hash-pinned local
Note-13 static metric ansatz has `M_tx=0=kappa*T_tx`; it therefore cannot match
the full local standing-breather tensor without an averaging prescription or a
different time-dependent geometry. T2A treats integrated and pointwise nulls
as interchangeable.

## Spatial-Stress Audit

T2A's last check transforms the rest-frame `T^xx` density and asserts
`<int T^xx_v dx>=gamma^2*E0*v^2=gamma*v*P`. It omits the transformed cycle
duration or equivalent hypersurface integration factor. Over one rest cycle,
the transformed spacetime numerator is `gamma^2*v^2*E0*T`; the lab cycle lasts
`gamma*T`. The correct mean integrated stress is therefore
`gamma*E0*v^2=v*P`.

An independent Lorentz-matrix derivation gives the same result. Refined mpmath
quadrature at 35 decimal digits, from 16 samples and twelve decay lengths to 64
samples and twenty-four decay lengths, recovers the rest energy, zero momentum,
and zero mean rest stress; it exposes T2A's factor `gamma` overestimate. At
`v=0.8` the source formula is high by exactly `5/3`. The source defines
`dens_Txx` but never integrates it, so its green symbolic check is insensitive
to this error.

## Dilaton and Physical Scope

The cited Grumiller-Kummer-Vassilevich review genuinely describes general 2D
dilaton-gravity theories. T2A does not execute the local specialization it
names: there is no target metric, dilaton, potential, coupling, varied equation,
boundary data, or coupled solution in its predicate. The check only requires
one value of the contravariant stress magnitude to exceed `0.1`. Consequently
it establishes a nonzero stress component, not a new dilaton, Einstein,
material, or substrate source.

Uniform translation has zero acceleration and does not itself imply radiation.
The post-hoc Phase-12 annotation is prose, not executable dependency closure.
Qualified GW1 and GW4 grant only their accepted conditional moment and waveform
surfaces. Pending G1 and G4 replay under a compatibility-only `np.trapz` alias,
but their radiation and self-force narratives gain no authority from green
execution.

## Terminal Disposition

T2A is qualified through C-SG-001, C-SG-002, C-SG-008, and C-SG-012. The exact
boosted field, charge vector, dispersion, and residual guard survive. The
pointwise standing-source premise, covariant mixed-component label, dilaton
source novelty, extra-gamma spatial-stress formula, and gravity, radiation,
material, or observational interpretations are rejected. Reserved C-SG-020 is
not promoted, and v0.100.0 remains the accepted release.
