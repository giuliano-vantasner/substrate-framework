# P157 O1 Source Adjudication

O1 reproduces all seven implemented predicates natively and has no NumPy
compatibility surface. Its tally validates representative spin-one algebra,
an inserted phase section, an antipodal involution, and a fixed scalar control;
it does not validate the advertised physical BEC-to-RP2 arrow or the claimed
closed-ray Berry holonomy.

O1.1 and O1.2 are exact representative checks already subsumed by C-SPN-001.
The reference and one rotated state are normalized and unmagnetized, and one
perpendicular pi rotation negates the reference while preserving its
projector. They do not establish the global orbit, choose a material ground
state, or construct a spatial defect. C-SPN-001 already proves the complete
pure-spin-one invariant, polar equality orbit, and conditional c2-dependent
selection.

O1.3 defines `exp(i*chi/2) Rz(chi)|0>`, but `Rz(chi)|0>=|0>` exactly. Its
projector is constant. With `A=i psi^dagger d psi`, the local connection is
`-1/2`, its integral is `-pi`, and the bare integral phase is `-1`. C-BER-001
requires the endpoint transition: the section also ends at minus its start,
so `tau=-1` and the corrected closed-ray holonomy is `(-1)(-1)=+1`. Reversing
the local phase changes the connection sign but not that answer. Omitting
`tau` is therefore load-bearing, not a harmless convention choice.

A genuine projective director loop uses a moving real director such as
`d(phi)=(cos(phi/2),sin(phi/2),0)`. Its real spin-one lift has nonconstant
projector, zero local connection, endpoint transition `-1`, and corrected
holonomy `-1`. A periodic gauge moves the sign into the integral and gives the
same result. The full polar half generator combines the director half turn
with a condensate half phase; it closes in `(S2 x U1)/Z2` and also gives the
accepted `-1`. O1 constructs neither moving path.

O1.4's two-pi minus sign comes from the separately inserted U1 phase. The
spin-one carrier itself returns `+I3` at two pi; only the fundamental SU2
doublet sees `-I2`. O1.5 correctly checks an antipodal involution and a
separate fundamental matrix, but supplies no map identifying them. It also
calls the projective ray orbit RP2 the physical polar order-parameter
manifold. C-DEF-001 distinguishes that ray orbit's Z2 loop group from the
full polar manifold's integer deck group, whose half-generator square is a
nontrivial integer phase vortex.

O1.6 compares separately assigned minus-one values without a common domain,
source object, map, carrier, or observable, contrary to C-CHR-001. O1.7
correctly notes that a deliberately chi-independent scalar internal state has
zero spin-frame derivative, but its `scalar_no_half_quantum` expression does
not test U1 single-valuedness. The correct control is that integer winding
closes while half winding does not.

Ho 1998 and Ohmi--Machida 1998 support complete interaction-dependent
spinor-condensate Hamiltonians and conditional phases. Ruostekoski--Anglin
2003 supports an Alice ring only within a trapped interacting model with
length scales and a stability threshold. These sources do not repair O1's
endpoint omission or supply its H-BEC and substrate dictionaries.

O1 is therefore qualified through unchanged C-SPN-001, C-DEF-001,
C-BER-001, C-HOL-001, and C-CHR-001. It contributes no new claim, canonical
API, release, physical condensate model, half-quantum defect solution,
observable, or substrate mechanism.
