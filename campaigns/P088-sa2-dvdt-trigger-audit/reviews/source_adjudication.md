# SA2 Source Adjudication

SA2 is qualified without a new accepted claim. Its surviving mathematics is
conditional Fourier and waveform algebra, not a physical dV/dt-not-V seeding or
breakdown mechanism.

The source's decisive DC test is not sensitive to DC. For a normalized Gaussian
packet centered at `mu` and the positive lobe
`exp(-tau^2*(omega-omega_b)^2)`, exact completion of the square gives

`I=A*exp[-tau^2*(mu-omega_b)^2/(1+2*e^2*tau^2)]/sqrt(1+2*e^2*tau^2)`.

SA2 takes `tau -> infinity` before the packet-width limit. This sends `I` to
zero for every fixed `mu`, including `mu=omega_b`. The check therefore observes
the loss of total mass from an unnormalised narrowing kernel, not selective
annihilation of DC. Taking the delta-sequence limit first correctly retains `A`
at resonance and then rejects a packet at zero. The assigned `delta_N` also
contains neither the declared offset `c` nor a waveform `V`, so it never
evaluates `N[V+c]-N[V]`.

There is a narrower true statement. With an explicit infinite-domain Fourier
convention, adding a constant contributes a distribution supported at zero, so
a well-defined *linear* functional whose kernel vanishes there can be offset
invariant. It does not follow for a quadratic power spectrum without handling
cross terms and products of distributions. On a finite rectangular record, a
constant contributes
`2*c*exp(-i*omega*T/2)*sin(omega*T/2)/omega`, which is generally nonzero away
from DC and vanishes only at the aligned nonzero Fourier-grid frequencies.
Offset invariance is also not invariance under changing pulse amplitude, width,
energy, gap field, or breakdown state.

The displacement-current route has analogous ceilings. `J_D=partial_t D` is
exact, but `J_D=epsilon*partial_t E` needs time-independent linear response;
otherwise `E*partial_t epsilon` remains. `E=V/d` further needs a fixed uniform
quasi-static cell map. Fourier differentiation retains an endpoint term unless
the waveform and transform domain remove it. Even after those declarations,
the `i*omega` or `omega^2` factor is only derivative algebra. SA2 provides no
driven sine-Gordon equation, voltage coupling, input/output observables,
retarded condition, causal response, absorption, formation, or count law.

For the inserted family
`S_s(omega)=omega^2*exp[-(omega/s)^2]`, the pointwise derivative is exactly
`2*omega^4*exp[-(omega/s)^2]/s^3>0`; the four midpoint samples are therefore
weak regressions. On a fixed band this family approaches the inserted ceiling
`omega^2`. But its prose says voltage amplitude is fixed. The inverse transform
of the implied Gaussian amplitude has peak proportional to `s`, and maximum
time derivative proportional to `s^2`. Keeping the time-domain peak fixed
instead supplies an `s^-2` spectral factor; its pointwise derivative is
proportional to `omega^2-s^2`, so the band decreases once `s` exceeds its upper
frequency and tends to zero rather than the source ceiling. Two sinusoids
`(S/Omega_i)*sin(Omega_i*t)` also have the same maximum slew `S` but arbitrary
different line frequencies and band overlaps. Scalar slew alone does not select
a spectrum or universal saturation law.

The consumer graph does not repair the derivation. The engineering mirror
inserts `V<=Vbd` as a branch and then ignores `V`; its six direct `np.trapz`
calls fail under the current NumPy. The downstream nucleation model maps units
through the old `DVDT_SAT` knob, retains a Michaelis gate, and restores a 0.05
seed floor even when the trigger is zero. Named C035 rungs still execute their
inserted Michaelis laws and import no SA2 code. Pending SA4 repeats the same
waveform family, free gain, threshold floor, and fit, so it cannot close SA2.

No canonical module changes. C-SG-015 remains an undriven field-trace theorem;
C-MED-001 remains a conditional co-scaled constitutive ansatz. SA2 establishes
neither a physical susceptibility nor flat-in-voltage yield, rising/saturating
yield in physical dV/dt, zero below breakdown, seeded population, or an F2
engine mechanism.
