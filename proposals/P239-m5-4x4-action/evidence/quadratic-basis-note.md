# P239 exact quadratic-basis result

The pinned M5 source defines a double two-form

\[
F_{\mu\nu ab}
=[\partial_\mu M,\partial_\nu M]_{\eta,ab},
\qquad
F_{\mu\nu ab}=-F_{\nu\mu ab}=-F_{\mu\nu ba},
\]

with no pair-exchange or algebraic-Bianchi identity. Source-admissible
symmetric derivative matrices give explicit counterexamples to both extra
Riemann symmetries. The exhaustive contraction enumeration therefore uses
only within-pair antisymmetry.

## Complete quadratic basis

Every parity-even contraction made only from inverse metrics is a linear
combination of the six independent scalars

\[
\begin{aligned}
I_1&=F_{abcd}F^{abcd},
&I_2&=F_{abcd}F^{cdab},
&I_3&=F_{abcd}F^{acbd},\\
I_4&=\mathcal R_{ac}\mathcal R^{ac},
&I_5&=\mathcal R_{ac}\mathcal R^{ca},
&I_6&=\mathcal R^2,
\end{aligned}
\]

where `R_ac=F_abc^b` and `R=R_a^a`. The verifier enumerates all 60
nonzero metric-pairing diagrams, obtains rank six over exact integer samples,
and proves that the displayed basis spans them.

There are also four independent one-epsilon pseudoscalars. The verifier
enumerates 156 nonzero epsilon-plus-metric diagrams, obtains rank four, checks
proper-Lorentz invariance exactly, and confirms that all four flip sign under
parity while the six `I_k` do not. P239 records those terms but does not select
them: issue #147 and the established 3x3 action are parity even, and no
independent chirality premise has been supplied.

## Exact 3x3-preserving family

On every purely spatial double two-form, the six parity-even invariants have
rank three. The complete nullspace is

\[
\begin{aligned}
N_1&=I_3-\tfrac14(I_1+I_2),\\
N_2&=\tfrac14(I_1-I_2)-I_4+I_5,\\
N_3&=I_1-4I_4+I_6.
\end{aligned}
\]

Thus the most general constant-coefficient quadratic action that preserves
the full M5.17 spatial action exactly is

\[
\mathcal L_2=-I_1+aN_1+bN_2+cN_3.
\]

The sign and normalization use the pinned M5.18 convention: `L=-I1-V`
gives the positive M5.17 static Hamiltonian.

## Candidate A rejection

A single exact counterexample suffices. At one point take the legitimate
symmetric field derivatives

\[
D_0=\omega\,\mathrm{diag}(1,0,0,0),\qquad
D_1=E_{01}+E_{10},\qquad D_2=D_3=0.
\]

The resulting source curvature has

\[
(I_1,I_2,I_3,I_4,I_5,I_6)
=\omega^2(4,4,2,2,2,4).
\]

Consequently `N1=N2=N3=0`, while the baseline action `-I1` has the
strictly negative coefficient `-4 omega^2`. No choice of `a,b,c` can repair
this source-admissible clock direction while retaining the full 3x3 action.
Constant-coefficient Candidate A is rejected; this is not a claim that every
local covariant completion fails. The public M5.21.16 six-channel result is
consistent motivation, but is not used as the proof of this P239 no-go.

## Next construction

OpenWave M5.21.16 showed that replacing the fixed internal Minkowski
contraction by a fixed Euclidean/Frobenius contraction makes every tested
channel nonnegative but explicitly breaks boost covariance. P239 next replaces
that fixed Euclidean metric by a covariant positive internal metric constructed
from `M`'s isolated timelike `g`-eigenprojector. In the vacuum eigenframe it is
exactly the Frobenius contraction; because the projector transforms with `M`,
the full density remains Lorentz scalar. This is a field-dependent local
candidate, not one of the rejected constant-coefficient `I_k` combinations.

Reproduce the enumeration and exact Lorentz/parity checks with:

```bash
PYTHONPATH=src python proposals/P239-m5-4x4-action/attempts/0001/enumerate_quadratic_basis.py
```

The recorded result is `attempts/0001/result.json`; its terminal tally is the
authoritative executed-check count.
