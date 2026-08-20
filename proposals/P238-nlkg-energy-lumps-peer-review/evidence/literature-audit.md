# P238 primary-source and prior-work audit

This audit uses only sources invoked by the paper to check the hypotheses of
the paper's own literature-dependent claims. Substrate claims and
implementations are not scientific comparators.

## Benci–Fortunato existence result

The cited primary source is V. Benci and D. Fortunato, *Existence of
hylomorphic solitary waves in Klein–Gordon and in Klein–Gordon–Maxwell
equations*, arXiv:0903.3508:
https://arxiv.org/abs/0903.3508.

The source formulates the nonlinear Klein–Gordon field as
`psi : R^N -> C`, uses global U(1) phase symmetry and its conserved charge,
and obtains standing waves with a complex time phase. Its Q-ball theorem is
stated for `N >= 3`. Its separate vortex theorem covers `N = 2`, but still for
the complex charged field and an angular phase. Those are load-bearing
hypotheses, not cosmetic notation. They do not establish the P238 paper's
claim for one uncharged real scalar in 2+1 dimensions.

The exact SymPy countermodel in `../companion/sympy_checks.py` is deliberately
narrower: it shows that an even positive potential can meet the paper's stated
binding inequality while the two-dimensional Derrick scaling derivative for a
nonzero static real lump is `-2 V`. It does not rule out all time-dependent
oscillons. It demonstrates why the field type, charge, dimension, and temporal
ansatz cannot be omitted from the theorem application.

## Cited 1+1D collective-coordinate baseline

The draft says the isotropic square-root expression was already derived in the
1+1D synthesis. The located cited baseline is Tiziano Fulceri, *From the
Sine–Gordon Breather to Relativistic Particle Dynamics and Effective
Geometry*, Zenodo record 21933838:
https://zenodo.org/records/21933838.

Audited source digest:

- SHA-256: `2d9b1c82f940188c73334850f841e7b2597102fe209ff219c0f813e8039469cd`
- Pages: 23
- Relevant source sections: 3.3–3.5 and equations (36)–(39)

That baseline assumes at every instant an exact *boosted*, velocity-dependent
travelling breather. It then states that the spatial action integral yields the
square-root Lagrangian but does not display the integral. This is materially
different from deriving a square root from the P238 draft's displayed rigid
translation ansatz. For an action quadratic in first time derivatives, a
profile depending only on `x-X(t)` produces a velocity-quadratic reduced
Lagrangian; the fourth derivative of a relativistic square root at zero
velocity is nonzero. A Lorentz-contracted/boosted profile can add the missing
velocity dependence, but its applicability and integral must be shown for the
actual 2+1D solution family.

## Acoustic-metric scope

Matt Visser, *Acoustic black holes: horizons, ergospheres and Hawking
radiation*, arXiv:gr-qc/9712010, derives an acoustic metric under explicit
continuum assumptions and treats the analogy as kinematical:
https://arxiv.org/abs/gr-qc/9712010. This supports treating P238-S10 and the
Schwarzschild null cone as wave-principal-symbol results. It does not supply
the missing massive-lump collective-coordinate or operational clock/ruler
bridge.

## Scope boundary

The repository's prior claims were excluded from scientific adjudication. In
particular, P238-S09 was rederived directly from equations (25)–(28) rather than
replayed from a Substrate einbein claim. GitNexus and repository validation are
used only to manage the PR's change impact; they do not support or falsify any
paper conclusion.
