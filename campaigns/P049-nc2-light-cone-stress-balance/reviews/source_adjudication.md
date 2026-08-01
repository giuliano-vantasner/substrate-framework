# NC2 Source Adjudication

NC2 is qualified. Its light-cone operator identity, sine-Gordon sign, rescaled
potential balance, and potentialless-model conservation are exact. P049 maps
that content into a canonically normalized stress tensor proposed as
`C-SG-012`. NC2's canonical-component label, energy bridge, small-amplitude
implication, anomaly language, and weak-sector reading exceed its checks.

## Reproduction

The hash-pinned source exits with status zero and `ALL 7 CHECKS PASS` in 0.45
seconds under Python 3.12 and SymPy 1.14.0. Its operator, EOM, auxiliary
balance, potential-deletion, energy-continuity, nonzero-source, and wrong-Theta
checks execute as written. The energy check constructs a separate Cartesian
energy density and never checks the claimed normalization bridge from its
auxiliary null components.

## Canonical Cartesian Tensor

For signature `(+,-)` and
`L=(phi_t^2-phi_x^2)/2-(1-cos(phi))`, the canonical symmetric tensor is
`T_mu_nu=partial_mu(phi) partial_nu(phi)-eta_mu_nu L`. Its covariant components
are

`T_00=(phi_t^2+phi_x^2)/2+V`,
`T_01=phi_t phi_x`, and
`T_11=(phi_t^2+phi_x^2)/2-V`,

where `V=1-cos(phi)`. Raising both indices changes the mixed sign, so
`T^01=-phi_t phi_x`. Off shell,

`partial_mu T^(mu 0)=phi_t R` and
`partial_mu T^(mu 1)=-phi_x R`,

with `R=phi_tt-phi_xx+sin(phi)`. This factorization proves both on-shell
conservation laws and catches a wrong mixed-component sign. Integrated energy
and momentum additionally require the relevant boundary fluxes to vanish.

## Canonical Light-Cone Tensor

For `x_plus=t+x` and `x_minus=t-x`, the Jacobian has entries plus or minus one
half. Transforming the covariant tensor gives

`T_pp=(phi_t+phi_x)^2/4`,
`T_mm=(phi_t-phi_x)^2/4`, and
`T_pm=V/2`.

The exact off-shell balances are

`partial_minus T_pp + partial_plus T_pm = J_plus R/4`,
`partial_plus T_mm + partial_minus T_pm = J_minus R/4`.

They vanish on shell. The trace is `T^mu_mu=2V=4T_pm`. Spatial parity exchanges
`T_pp` and `T_mm` and leaves `T_pm` even, so the tensor supplies no handed
sector selection.

## NC2 Normalization Error

NC2 defines its named quantities as

`T_pp_source=(partial_plus phi)^2/2`,
`T_mm_source=(partial_minus phi)^2/2`, and
`Theta_source=(cos(phi)-1)/4`.

Because `partial_plus phi=(phi_t+phi_x)/2`, these satisfy

`T_pp_source=T_pp/2`,
`T_mm_source=T_mm/2`, and
`Theta_source=-T_pm/2=-trace/8`.

Their displayed laws
`partial_minus T_pp_source=partial_plus Theta_source` and its partner are a
uniform half-rescaling of the canonical conservation equations and are exact.
They are not the canonical null components in the declared coordinate
convention, and `Theta_source` is not the canonical mixed or trace component.

The source then states that its chiral sum is proportional to the full energy
and writes an energy composition equivalent to
`T_pp_source+T_mm_source+V`. This equals
`(phi_t^2+phi_x^2)/4+V`, not the canonical energy. The correct bridge is
`T00=2*(T_pp_source+T_mm_source)+V`. Its executable energy check bypasses this
error by defining `T00` directly, so the passing tally is insensitive to the
headline normalization claim.

## Potentialless Model and Interpretation

Deleting `V` from the action and `sin(phi)` from the equation gives a separate
massless scalar theory with `T_pm=0`; its two null stresses are separately
conserved. This is a valid model-deformation limit. It is not the
small-amplitude limit of the fixed normalized sine-Gordon theory, which
`C-SG-011` proves is massive Klein-Gordon and retains first-order
characteristic sources.

In the interacting theory the potential mediates symmetric exchange between
the two null balances. Calling their difference a “chiral anomaly” is not a
derived quantum anomaly and calling the exchange a weak V-A structure adds an
unaccepted physical dictionary. The equation and tensor are parity covariant,
and W1/W7 remain pending source units.

## Terminal Disposition

NC2 maps its exact operator identity and uniformly rescaled balance into the
canonical theorem `C-SG-012`. It remains qualified for calling its half-scaled
auxiliaries canonical stress components or a trace component; its missing
kinetic factor in the energy bridge; conflating potential deletion with the
small-amplitude normalized theory; and inferring a physical chiral anomaly,
left-right selection, V-A interaction, weak force, bosonization closure,
particle identity, or substrate ontology. Later NC units must use the
canonical normalization and explicit interpretation ceiling.
