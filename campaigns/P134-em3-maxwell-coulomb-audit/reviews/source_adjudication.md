# P134 EM3 source adjudication

EM3 reproduces all eleven source checks, but that tally does not establish its
headline. Exact rederivation retains a valuable conditional imported-action
theorem and rejects several source interpretations. The accepted object starts
from a separately supplied positive kinetic coefficient, conserved current,
flat signature, dimension, source normalization, boundary data, and
test-charge dictionary. Local U1 covariance alone supplies none of them.

## Surviving exact surface

For `F=dA` and
`L=-kappa*F_mu_nu*F^mu_nu/4-j^mu*A_mu`, compactly supported variation gives
`kappa*partial_mu F^mu_nu=j^nu`. Antisymmetry also gives the Bianchi identity
and makes current conservation a necessary compatibility condition. These are
exact consequences of the declared action, not a derivation of the action or a
physical current.

With signature `(+,-,...,-)`, static `A_0=phi`, `A_i=0`, and `j^0=rho`, the
equation is `-kappa*Delta(phi)=rho`. A normalized point source in integer
`d>2` gives
`phi=Q/[kappa*(d-2)*S_(d-1)*r^(d-2)]` and
`E_r=Q/[kappa*S_(d-1)*r^(d-1)]`. The implementation reuses C-KRN-001 for this
branch. In `d=2` the logarithmic potential requires a reference radius; in
`d=1` the even full-line branch is linear up to homogeneous data. Declaring
`U=q*phi` and `F=q*E` then gives the conditional two-charge force.

## Rejected source readings

EM3 declares `A_0=-phi`, but its action convention then gives the opposite
Laplacian sign. Check 4 never substitutes that potential into the field
strength; it separately defines `E=-grad(phi)` and verifies Gauss algebra. The
corrected theorem uses `A_0=phi` in the frozen signature.

The executable dimension comparison stops at `d=3`. Exact `d=4`, `d=5`, and
`d=6` branches all decay at infinity, as the source dossier itself acknowledges.
Only the inverse-square member of the declared integer-dimensional force family
selects `d=3`; decay does not. The dossier's additional “normalizable” wording
is not proved and is excluded.

The neutral guard substitutes `Q=0` into its one-charge ansatz. Zero net charge
does not imply zero density: an opposite-charge pair has a nonzero dipole field.
Zero field requires an identically zero source plus sufficient whole-domain
regularity and boundary data. Likewise, deleting the kinetic term yields the
source-only Euler condition `j=0` and no equation for `A`; it does not force
`A=dchi`. The identity `A=dchi => F=0` remains true but its converse/EOM reading
is rejected.

The numerical slope and finite-difference Laplacian regress the hard-coded
exact `1/r` formula. The alpha dimension cancellation and constitutive
substitution are conditional algebra, but the magnitude uses embedded CODATA
values despite the source's “no real data consulted” line. Neither the medium
map nor physical electric ontology enters C-MAX-001.

## Decision

C-MAX-001 is distinct from C-GAU-001 because it adds the explicitly declared
action variation and source equation, and distinct from C-KRN-001 because it
adds current compatibility, source normalization, lower-dimensional boundary
branches, and the conditional force dictionary. It depends on both and retains
their ceilings. EM3 is qualified through C-GAU-001, C-KRN-001, and C-MAX-001;
it establishes no derived photon, preferred dimension, charged soliton,
electromagnetic material, gravity coupling, observation, or substrate
mechanism.
