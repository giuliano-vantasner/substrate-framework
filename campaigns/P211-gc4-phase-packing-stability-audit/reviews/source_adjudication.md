# GC4 Source Adjudication

## Source Reproduction

The hash-pinned GC4 source executes all eight checks with one assertion and
exit zero under NumPy 2.5.1. It has no direct, imported, dynamic, or eager
quadrature-name surface. Its rectangle-sum grid values are reproduced by the
new exact formula without numeric integration.

## Predicate Decisions

GC4.1 is qualified: the sampled trial energies survive, but merger,
persistence, and stability do not. GC4.2 is corrected because finite
separation includes constant and cosine-squared terms. GC4.3 is qualified to
the fixed-nonzero-cosine leading tail rate and loses the physical hierarchy
reading. GC4.4 is qualified to an exact negative perpendicular interaction,
not merger dynamics. GC4.5 is qualified to the sharp complete scalar-circle
capacity, not stability. GC4.6 is rejected as a stable triple because it only
calls the two-profile helper three times. GC4.7 is rejected because neither a
physical CP lower bound nor a stability upper bound exists in accepted
authority. GC4.8 retains its narrow static no-loader result but is not a
complete reachability or no-input proof.

## Exact Repair

For scaled separation `s` and phase cosine `c`, the exact interaction is
`-c*I31/6-(1+2*c^2)*I22/12`. The leading term is cosine-linear only for fixed
nonzero `c` at large separation. Independently, the optimized largest pair
cosine for `N` scalar circle phases is `cos(2*pi/N)`, so strict and weak
capacities are three and four. Neither exact object selects count three.

## Authority and Compatibility

The thirteen-node graph pins 101 static checks and 19 assertions without
executing its predecessor scripts. E1 alone contains a safe lazy
`np.trapezoid`-first conditional and selects the current branch; all other
nodes have zero quadrature surface. Pending GC5 grants no authority.
