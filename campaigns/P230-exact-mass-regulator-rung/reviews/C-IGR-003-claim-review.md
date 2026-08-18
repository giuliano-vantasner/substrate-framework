# C-IGR-003 Claim Review

## Claim Under Review
The claim is the declared power-subtracted constant-mass finite-part theorem and scheme ceiling. For positive scale `mu` and constant `m2>=0`, P230 defines `I2=m2*(log(m2/mu^2)+EulerGamma-1)` and `I3=-(m2^2/2)*(log(m2/mu^2)+EulerGamma-3/2)`, continuously extended by zero at `m2=0`. They are the exact finite parts after the frozen sharp-cutoff power and logarithmic subtractions, satisfy `dI3/dm2=-I2`, and retain exact scale derivatives. Together with the sharp and smooth families they prove that P230 supplies no scheme-independent physical normalization.

## Sourced Inputs
The review read C-GRV-001, Vassilevich's zeta/proper-time relations and heat-kernel convention, Visser's cutoff sector organization, the P230 finite-part definition, PR #77's sign defect and repair, PR #82, the module, tests, and independent raw-limit script.

## Independence
The independent review begins with the sharp tail expressions and takes the specified cutoff subtraction limits directly. It then inserts the declared scale, differentiates the resulting I2/I3 family, types the coefficient from the determinant and Einstein-Hilbert factors, and evaluates the sign counterexample without importing the implementation.

## Verification Status
The claim earns `symbolic_verified`. SymPy evaluates the two exact cutoff finite-part limits and the derivative and scale identities. The zero-mass branch is proved by one-sided limits; direct substitution into `m2*log(m2)` is intentionally not used.

## Sensitivity and Counterexamples
The original sign field is falsified at `m2=mu^2=1`, `xi=0`: the curvature weight is positive while the returned value is `(EulerGamma-1)/(12*pi)<0`. The massless continuous branch is zero. A shifted finite subtraction changes the frozen scheme and is not the same claim. Passing both cutoff and scale or defaulting the scale is rejected by the API.

## Framework Compatibility
The claim explicitly exposes scale and subtraction dependence. It does not call the finite part regulator free, select a renormalization condition, erase a finite counterterm or C-GRV-001 baseline, or identify a physical cutoff. At unit cutoff and zero mass the vacuum-class sharp, smooth, and power-subtracted values are exactly `1/2`, `1`, and `0`, establishing the scheme ceiling without a comparator.

## Dependency and Consumer Replay
The accepted dependency is C-GRV-001 for the independent baseline ledger. The finite-part prescription and scale are approved declared inputs. Consumers are the canonical API, tests, P230 verifier, docs, registry, release, and accepted memory; the final replay checks every one.

## Competing Candidate Audit
Candidate C was preregistered alongside A and B and is retained because it exposes a distinct exact subtraction family. It is not selected as the physical regulator; all three remain available with their assumptions and contrasts.

## Four-Axis Decision
Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active` conditionally. The relationship is a new claim depending on C-GRV-001, with no challenge or supersession.

## Promotion Transaction
The accepted boundary includes the constant-mass code correction, raw-limit reviewer, this claim review, immutable P230 campaign, registry, release v0.161.0, generated docs and memory, and full validation.

## Continuation if Not Accepted
Not applicable. A selected physical scheme, matching condition, total coupling, or comparator requires a later proposal.

## Done Gate
Acceptance requires the recorded integrated gate and empty debt ledger; a passing finite-part identity alone is insufficient.

## Cross-References
See P230 formula freeze and literature audit, C-IGR-001/002, PRs #77/#82, both campaign verifiers, and C-GRV-001.
