# FS4 Source Adjudication

FS4 is duplicate evidence for `C-SG-009`, `C-MOM-002`, and `C-GW-004`. Its
valid result is that an arbitrary constant offset drops out of positive time
derivatives and therefore out of conditional derivative-based TT readouts and
power. Those predicates were already accepted with broader exact scope. FS4
does not derive a form-factor identity, tidal response, backreaction, or
physical radiation mechanism.

## Reproduction and Compatibility

The hash-pinned source exits cleanly with five checks under NumPy 2.5.1 and
uses `numpy.trapezoid` with an older-version `numpy.trapz` fallback. Its dense
finite-difference replay takes tens of seconds and is preserved once in a
hash-bound record. The exact duplicate audit does not need to repeat the same
60,001-point spatial integrations after verifier-only edits.

## Accepted Constant-Offset Result

For any time-independent scalar `c` and positive derivative order `n`,
`d^n(mu+c)/dt^n=d^n mu/dt^n`. Applying `C-MOM-002` gives identical normalized
and triple STF derivatives for the full and offset-subtracted moments.
Consequently `C-GW-004` gives identical conditional TT readouts and power when
its convention coefficients are carried consistently. P043 verifies these
statements for arbitrary functions and through fourth order, not only for a
two-harmonic example.

A quadratic time-dependent offset changes the second derivative by `2*epsilon`
and a cubic offset changes the third derivative by `6*epsilon`, so the result
depends on genuine time constancy. Dependence on a family parameter alone does
not matter when that parameter is held fixed during time differentiation.

## Why This Is Duplicate Rather Than a New Claim

`C-SG-009` already supplies the full exact moment. `C-MOM-002` already states
that constant monopole/transverse terms disappear from every positive STF
derivative, and its derivation applies equally to an added longitudinal
constant. `C-GW-004` already fixes the corresponding derivative-based
conditional waveform and power. FS4 adds no new API, distinct consumer,
parameter relation, or stronger oracle. Its numerical full-versus-modulation
comparison runs the same finite-difference operator on arrays differing by a
constant and is regression evidence for the exact identity.

## Form-Factor and Decomposition Failure

FS4 imports `NEG_WPP=13.957728` from phase 3; it never derives that value from a
profile. Its executable evidence that the value is “inside” the sampled mean is
only the inequality `0 < NEG_WPP < mu_bar_num`. Infinitely many positive
constants satisfy that inequality. Its symbolic decomposition introduces
independent symbols `negwpp` and `pot_mom`, adds them, and differentiates the
sum; this proves only that a sum of declared constants is constant.

For any proposed piece `a`, the algebraic identity
`mu_bar=a+(mu_bar-a)` holds and every piece is annihilated by time derivatives.
Constant cancellation therefore cannot select `a` as a fixed-profile Fourier
moment, much less identify it with a Mathisson-Papapetrou coefficient. Such an
identity requires independent definitions and a derivation that FS4 lacks.

## Repeated Power Defects

FS4 constructs triple `Q=3I_STF` but again applies `G/5`, the normalized
coefficient, so its reported conditional power is nine times too large under
the declared `C-GW-001` inputs. It also requires the sampled finite-difference
power to be strictly positive even though `C-GW-004` proves exact zero phases.
Neither defect affects equality under a constant offset, but both block reuse
of the source's power magnitude or positivity language.

## Physical Scope

The wrong-attribution guard invents a formula proportional to a static scalar
and rejects it. That counterexample is valid but supplies no positive source
dynamics. T2C and G4 remain pending, and FS4 constructs no conserved 3+1 stress
tensor, form-factor-to-interaction map, gravitational action, response law,
retarded solution, radiation reaction, or backreaction equation. It cannot
“lift” those units' ceilings.

## Terminal Disposition

FS4 is retained as noncanonical `duplicate_evidence` mapped to `C-SG-009`,
`C-MOM-002`, and `C-GW-004`. The imported form-factor, tidal, backreaction,
physical radiation, and ceiling-lift interpretations are not mapped. Durable
evidence is the P043 exact verifier, independent constant-offset review, source
reproduction record, and this adjudication.
