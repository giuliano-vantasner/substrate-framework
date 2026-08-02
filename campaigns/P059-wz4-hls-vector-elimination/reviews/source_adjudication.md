# WZ4 source adjudication

WZ4 reproduces nine algebraic checks, but it does not construct or eliminate
an HLS vector field and cannot be accepted as a second derivation of a WZW
functional. P059 therefore qualifies the source: the generic conditional
quadratic-field theorem survives in a new canonical implementation, while the
source's HLS, anomaly, coefficient, parity, and physical claims remain outside
the accepted framework.

## Reproduction and object boundary

The SHA-256-pinned WZ4 file at `substrate@6d1f4e0` exits cleanly under Python
3.12.2, SymPy 1.14.0, and NumPy 2.5.1 with `ALL 9 CHECKS PASS`. Unlike WZ3, it
does not call the removed `np.trapz`; no compatibility shim is involved. The
tally covers a scalar propagator series, sampled epsilon contractions, limits
of formulas defined in the script, and symmetric-versus-antisymmetric tensor
identities. It never constructs `xi_L`, `xi_R`, an HLS connection, the four
homogeneous operators, their coefficients, a quadratic vector action, a
stationary field equation, or an on-shell substitution.

## Circular normalization and heavy limit

WZ4 first defines the imported target
`F_WZW=e*N_c/(12*pi^2*F_pi^3)` and then defines
`A_HLS=F_WZW*m_V^2/(m_V^2-q^2)`. Exact decomposition gives

`A_HLS = F_WZW + F_WZW*q^2/(m_V^2-q^2)`.

The second term vanishes in the heavy-mass limit, leaving the contact term that
was present at the start. Replacing `F_WZW` by an arbitrary symbol `C` makes
both the zero-momentum and heavy-mass checks return `C`; setting `C=0` makes
the whole displayed amplitude zero. These sensitive counterexamples show that
the verifier checks a unit limit, not independent generation or normalization
of a WZW term.

## Exact conditional theorem

P059 separately starts from the declared action
`L=V^T*K*V/2+V^T*J`, with a nonempty symmetric invertible kernel. Component
differentiation, direct substitution, and independent completion of the square
all give `V_star=-K^-1*J` and
`L_eff=-J^T*K^-1*J/2`. For `J=J_even+J_odd`, the odd term is the inherited
cross term
`-(J_even^T*K^-1*J_odd+J_odd^T*K^-1*J_even)/2`; it vanishes if either source is
removed and flips under the declared odd-source parity. A finite Neumann
inverse expansion returns exact nonzero left and right residuals, so a
derivative truncation cannot masquerade as an exact inverse. This algebra fixes
no mass, coupling, source, or anomaly coefficient.

## HLS anomaly equation and free coefficients

Fujiwara, Kugo, Terao, Uehara, and Yamawaki describe general solutions of the
Wess-Zumino anomaly equation with hidden-local-symmetry vector mesons and state
that the low-energy photon/pseudoscalar amplitudes remain fixed even when
vectors participate ([Progress of Theoretical Physics 73 (1985), 926](https://academic.oup.com/ptp/article/73/4/926/1873501)).
Harada, Matsuzaki, and Yamawaki write the full solution as
`Gamma_HLS_full=Gamma_WZW+Gamma_HLS_inv`, with
`Gamma_HLS_inv=(N_c/(16*pi^2))*integral(sum_i c_i*L_i)`,
`delta Gamma_HLS_inv=0`, and four free coefficients `c1` through `c4`
([arXiv:1104.3286](https://arxiv.org/abs/1104.3286)). The anomaly map therefore
has one inhomogeneous direction and a four-dimensional homogeneous kernel; it
does not fix those four coefficients. A particular ultraviolet model may add
the missing selection premise, but WZ4 and the accepted framework do not.

## Anomaly under stationary elimination

For a stationary substitution, the chain rule is
`delta Gamma_eff=(delta Gamma)_V+(delta Gamma/delta V)_star*delta V_star`.
The second term vanishes on the actual field equation. Thus a supplied
inhomogeneous variation is preserved, invariant homogeneous terms remain
invariant, and setting the starting inhomogeneous level to zero leaves zero.
Algebraic vector elimination can redistribute or generate conditional local
operators from declared sources; it cannot select an anomaly class absent from
the starting functional.

## Parity and dependency audit

WZ4 treats all four contracted objects as polar vectors and correctly finds
that their epsilon contraction changes sign. Physical pions are
pseudoscalars. Their three intrinsic minus signs combine with the orientation
factor as `det(P)*(-1)^3=+1`, so the gamma-three-pion action term is P-even
while belonging to the intrinsic-parity-odd sector. The primary HLS
classification likewise distinguishes those notions.

WZ4's `N_c` derivative and cross-process ratio merely propagate factors
inserted in its definitions. Its KSRF solution imports pending S4 and does not
pin the distinct `g_omega`. G2, G3, S3, and S4 remain pending; C-WZW-001,
C-WZW-002, and C-TOP-002 deliberately supply no HLS action, gauged anomaly,
physical baryon meaning, or `N_c` identification. None enters C-EFT-001's
dependency closure.

## Disposition

WZ4 maps only to C-EFT-001's generic conditional stationary-elimination,
source-cross-term, inverse-expansion-residual, and chain-rule theorem. It does
not establish an HLS realization, four-operator basis, coefficient selection,
vector dominance, gamma-three-pion or omega normalization, WZW generation,
anomaly matching, KSRF physics, `n=N_c=3`, baryon interpretation, absolute
scale, or substrate realization. Its structured disposition is `qualified`.
