# M5.17 uniaxial source reconciliation

The pinned M5.17 source does not use an asymptotically biaxial spatial
spectrum. Its complete static functional is

\[
E[S]=\int d^3x\left(4c_2\sum_{i<j}\|[\partial_iS,\partial_jS]\|_F^2
+a\operatorname{Tr}S^2-b\operatorname{Tr}S^3
+c(\operatorname{Tr}S^2)^2-V_{\rm vac}\right),
\]

with `b=beta*c`, `a=(3b-4c)/2`, `V_vac=a-b+c`, `c>0`, and
`0<beta<2`. Its exterior hedgehog is the pure director
`S=n n^T`, whose spectrum is `(1,0,0)`. The M5.18 trace-power potential with
preferred mixed spectrum `(g,1,delta,0)` is a later replacement. It preserves
Lorentz invariance and closely reproduced one calibrated melt profile, but it
does not equal the M5.17 potential off shell.

That distinction matters for P239 because the campaign froze exact recovery
of the established 3x3 functional, not agreement at a vacuum or on one
profile. It also matters geometrically: transporting two unequal tangent
eigenvalues around a radial hedgehog makes the tangent frame observable and
produces the pole obstruction proved in attempt 0004.

On the simple timelike spectral branch there is a direct covariant lift. Let

\[
X=\eta^{-1}M,\qquad P_t^2=P_t,\qquad Q=I-P_t,\qquad Y=QXQ.
\]

Because `X`, `P_t`, and `Y` transform by simultaneous similarity, traces of
powers of `Y` are Lorentz scalars. The Candidate-G potential is

\[
V_G(M)=a\operatorname{Tr}Y^2-b\operatorname{Tr}Y^3
+c(\operatorname{Tr}Y^2)^2-V_{\rm vac}
+w_t(\operatorname{Tr}(P_tX)-g)^2 .
\]

In the rest frame with a uniform time row, `Y=diag(0,S)`, so the first four
terms reproduce the full M5.17 potential identically for every spatial field
`S`; the final term vanishes identically and only pins the selected time
eigenvalue away from that sector. At the uniaxial vacuum its mixed spectrum is
`(g,1,0,0)`. The repeated zero eigenvalues are allowed because only the
selected timelike eigenvalue must remain simple.

For spatial eigenvalues `lambda_i`, write
`s=(sum_i lambda_i^2)^(1/2)`. The norm inequality
`sum_i lambda_i^3 <= s^3` reduces the lower bound to the positive-rank-one
path. Along that path,

\[
V_G(s)=\frac c2(s-1)^2
\left[2(s+1)^2-\beta(2s+1)\right]\ge 0
\]

for `s>=0`, `c>0`, and `0<beta<2`, with equality at the selected uniaxial
vacuum. Thus this source correction improves exact framework fit without
introducing an empirical comparator or fitted coefficient.
