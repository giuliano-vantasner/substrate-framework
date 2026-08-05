# C-PDE-012 Individual Claim Review

Decision: accept, subject to the terminal repository replay.

The claim's exact parts were derived by two independent routes. The primary
route uses the canonical API and SymPy plus the existing generic FEM. The
independent route imports no proposed code and uses direct differentiation,
the closed-form spherical `j2`, fresh bracketing, a separate tridiagonal
operator, exact trial-function integrals, and rational endpoint inequalities.
They pass 39 and 22 checks respectively.

The load-bearing encoding is sensitive: `chi/r^2`, centrifugal coefficients
5 or 7, wall-gap powers 1 or 3, a negative excess potential, and an unforced
nondecayed endpoint all break the relevant verdict. The first failed focused
runs are preserved: float substitution before symbolic proof, a transcribed
vacuum-level decimal, an incorrect whole-level wall scaling, brittle registry
wording, and an under-resolved independent error bound were repaired without
lowering the scientific claim.

The dependency closure is C-PDE-003, C-PDE-005, and C-PDE-009, transitively
C-PDE-001 and C-SG-001. P054's unchanged numeric audit is scoped evidence, not
an exact premise. C-MOD-001/002 are nonduplication neighbors, not sine-Gordon
inputs. No empirical comparator, hidden scale, fitted constant, Floquet
operator, nonlinear mode, gravity, or substrate map enters the theorem.

The four status axes are: symbolic verified; accepted review; native
compatibility; active epistemic status. The conditional form bound explicitly
requires almost-everywhere nonnegativity and vanishing boundary form. The
vacuum formula explicitly requires a positive spherical-Bessel zero. The
endpoint result says forced zeros are non-discriminating; it does not claim an
unforced endpoint test is sufficient for localization.
