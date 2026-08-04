# WM4 Source Adjudication

## Exact result

At the declared coefficient triple, the design with columns `1` and `b` has
rank two. Its linear annihilator is one-dimensional and is spanned by the
coefficient vector of

`D = a1(b2-b3) + a2(b3-b1) + a3(b1-b2)`.

Each signed pairwise crossing-coordinate difference is an exact beta-only
multiple of D when its displayed coefficient differences are nonzero. WM3's
reconstructed inverse weak-coordinate residual is likewise `c(b)D` when
`5*b1+3*b2-8*b3` is nonzero. These are specializations of C-IDN-001 and
C-RGE-004, not a distinct theorem.

## Range, input, and convention ceilings

The source's max-minus-min crossing spread is `abs(D)` times the largest of
three positive beta-only factors. It is nonnegative and piecewise, not one
globally signed linear functional. The inverse weak-coordinate coefficient is
beta-only, but the angle dictionary explicitly contains supplied `alpha_em`.
Its approximate percentage also depends on the selected observable and
denominator.

A common reference shift preserves D and moves every finite crossing together.
Common inverse-coordinate scaling scales D. A paired Abelian coordinate change
preserves the electromagnetic combination but changes equality with the
non-Abelian coordinates. D is therefore convention-covariant, not an
unqualified physical invariant.

## Degeneracies and mutation sensitivity

All-equal slopes give D zero for any intercepts, including three parallel
disjoint lines, so determinant zero is not sufficient for finite concurrency
without the rank hypothesis. Setting only `b1=b2` keeps rank two, two finite
crossings, and a finite WM3 coefficient; only the equal pair's crossing is
undefined. Conversely, `(b1,b2,b3)=(0,8,3)` has three distinct slopes but a
zero WM3 reconstruction denominator.

An exact rational intercept mutation makes D and all finite signed projections
zero. That proves their common linear compatibility locus. It does not prove
that every diagnostic sharing the locus is a constant multiple: for real
intercepts `(1+a1^2)D` has the same zeros and is nonlinear.

## Source provenance and decision

WM4, SM4, and WM3 reproduce 11, 8, and 10 checks. WM4 dynamically executes the
latter two. Contrary to its comments and final provenance prose, it hard-codes
all three beta coefficients and never reads or compares SM4's beta attributes.
Its claimed bit-for-bit equality is implemented with `math.isclose`.

Forty-four primary and thirty-four independent checks agree. The conditional
linear theorem survives; the input-free, rank-free, fully singular, invariant,
and same-physical-observable readings do not. Existing claims already govern
the reusable content, so WM4 is terminally qualified with no new claim, API, or
release. No numerical integration or NumPy compatibility event occurs.
