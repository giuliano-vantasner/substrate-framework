---
name: small-ratio-numerics
description: Field-tested methods for computing with small ratios — soft modes, weak forces, tiny splittings — drawn from Skyrme, Einstein–Skyrme, boson-star, and multi-scale continuum practice. Use when a quantity of interest is orders of magnitude below the dominant energy scale, or when results move with box size or mesh.
---

# Small-Ratio Numerics

A synthesis of how communities that live in the small-ratio regime — nuclear Skyrme, baby-Skyrme, magnetic skyrmions, Einstein–Skyrme, boson stars, liquid-crystal defect energetics — handle a problem that defeats naive single-grid minimization. The recurring pattern: a strong short-distance scale sets the core and the bulk of the energy; a much weaker long-distance scale carries the physics you care about; the question (a soft Hessian eigenvalue, a tiny energy difference, a weak force) lives in the gap between them. Once $\varepsilon$ or $\lambda_{\min}/\lambda_2$ drops below ~1e-3, the weak signal is usually smaller than truncation error on any single grid, and the calculation reports spurious instability, wrong force signs, runaway frequencies, or "minima" that move with the box.

The field's response was not more precision — it was splitting the question into pieces that each have a well-conditioned answer. That split, and the techniques around it, is what this skill shares. It is advice, not a work plan; pick the pieces that fit the situation. (Origin: the methods note in issue #155 and the literature it cites.)

## Constrain the obvious moduli, then minimize

An unconstrained energy should not be asked to be strictly convex. Topological charge, translations, rotations, isorotations, and a conserved angular momentum $J$ or Casimir are exactly flat or extremely soft; leaving them free makes the Hessian look marginal even when the physical profile is stable. Fix topology by ansatz or projector, fix $J$, minimize on that manifold — the frequency $\omega$ of an internally rotating configuration is then an *output* of the constrained problem, not a coordinate that can run away. Critical frequencies (e.g. $\omega \le \min(\mu, 1)$ for isospinning hedgehogs) are diagnosed on the constrained ansatz, then checked against symmetry-breaking perturbations. Virial/Derrick identities make a cheap independent monitor of the minimizer: if the virial residual exceeds the energy difference you care about, that difference is not yet a result.

This is the rigid-rotor / collective-coordinate split: classical profile at fixed topology; spin and isospin restored afterwards on a well-defined inertia tensor.

## Soft eigenvalues: spectrum, extrapolation, eigenvector

$\lambda_{\min} > 0$ on one mesh in one box is necessary, never sufficient, when it sits three or more orders below $\lambda_2$.

- **Build the second-variation operator and extract a few eigenvalues, not just a sign.** Radial Schrödinger/Sturm–Liouville problems for hedgehogs; sparse Hessians in 3-D. Shift-invert Arnoldi (ARPACK and descendants) is the default when conditioning is extreme.
- **Extrapolate in mesh and in domain**: $\lambda(h) = \lambda_\infty + A h^p + \cdots$, $\lambda(R) = \lambda_\infty + B e^{-mR}$ or $R^{-q} + \cdots$. Zero modes from broken continuous symmetries can converge as slowly as $h^{1/8}$ on naive lattices; improved stencils restore design order. If $\lambda_{\min}(R)$ collapses as the box grows, the mode was a finite-domain gift.
- **Look at the eigenvector.** A bulk shape mode, a boundary-layer splitting mode, and a mesh-scale oscillation are different objects; only the first says something about the continuum object. A soft direction concentrated near the outer boundary calls for a larger domain or a different boundary condition, not a verdict.
- **Separate bound modes from the scattering continuum.** Any finite box discretizes the continuum; a "spectrum" not compared against the asymptotic linear operator mixes vibrations with box-quantized radiation.
- **Where a proof is possible, prove it.** The $B=1$ Skyrmion's linear stability was reduced to a radial Schrödinger operator with no bound states — the gold standard the numerics approximate.
- **Reporting habit**: always quote $\lambda_{\min}/\lambda_2$ and its continuum limit. A minimum three orders softer than everything else is a different claim from a well-conditioned well — and a legitimate one (see the last section).

## Weak forces: pair moments, don't subtract energies

Self-energy subtraction at large separation ($E(R) - 2E_1$) is the most common route to a wrong sign: each energy is known to a few digits, the interaction is many orders smaller, and the difference is noise, box artefact, or orientation error. The method that replaced it is **asymptotic matching**: verify the isolated object has a multipole expansion at infinity; identify the leading moments (Skyrmions have no monopole — dipole or higher); the linear interaction of two well-separated objects is a *pairing* of those moments, scaling as $R^{-(M+N+1)}$ for moment orders $M$, $N$. Relative rotation in space/internal space can flip the sign; the pairing is often attractive for $|N-M| \le 2$. Compute the isolated moments to comfortable precision, evaluate the pairing analytically, and — if at all — use a full two-body run only as a sign-and-coefficient check at moderate separation. This transfers unchanged to any linear far field: massive/massless pions, Maxwell, GEM, linearized gravity. The kernel changes; the strategy does not.

## Separate scales instead of refining one grid

When the weak sector is a correction — gravitational coupling, small pion mass, quartic boost response, an $\varepsilon$ in front of a curvature-squared term — put $\varepsilon$ in the equations *on purpose*: solve the dominant theory to high accuracy and freeze that core; treat the weak sector as perturbation or slow collective-coordinate dynamics of the core's moduli; match an inner nonlinear core to an outer linearized field, where the force, frequency shift, and interaction sign live. The gravitating-soliton version is adiabatic continuation: start from the flat-space minimizer, step the coupling up in small increments, Newton–Raphson at each step, with constraint violations and virial identities monitoring accuracy. An eigenvalue drifting through zero as the coupling grows is a **bifurcation** (stable branch coalescing with an unstable one), not a failed run. Matched asymptotics and EFT reductions are the analytic form of the same split — cheaper than high-precision 3-D, and they make explicit the order at which the weak signal first appears (a response starting at fourth order in amplitude is invisible to a linearized two-defect calculation; that is a statement about the expansion, not the sign).

## Dynamics that tolerate soft directions

Gradient descent on a stiff-plus-soft energy is slow along the soft manifold and noisy across it. Two field-tested replacements:

- **Arrested Newton flow**: evolve a second-order-in-time equation with the static energy as potential, zeroing velocity whenever energy rises. Efficient in very high dimension (GPU Skyrme searches with $10^5$ random starts). Near-degenerate minima joined by shallow barriers are clustered with a metric on observables (energy, size, inertia eigenvalues) rather than collapsed by an aggressive energy tolerance — the "gray zone" is inspected, not auto-deleted.
- **Path methods** (nudged elastic band and relatives): when the question is the barrier between near-minima, or whether a soft direction leads to fission, compute the path. Softness of a local Hessian can mean a long valley rather than an unphysical object — a different statement needing a different diagnostic.

For time-dependent checks (quasi-normal modes, radiation tails, genuine dynamical instability), trust the linear spectrum and a resolved nonlinear evolution together; linear QNMs that disagree with a careful nonlinear run are not believed. High-order differences, small CFL, and — for late-time tails or tiny growth rates — extra floating-point precision are routine there.

## Precision as a targeted tool

Arbitrary precision goes where the *quantity of interest* is tiny — not everywhere. The ladder, cheapest first: (1) non-dimensionalize so the core balance is $O(1)$, small parameter in a coefficient rather than field amplitude; (2) Richardson extrapolation in $h$ and $R$; (3) independent discretizations (finite difference vs spectral vs finite element; 3-D vs symmetry-reduced ODE) — agreement of extrapolated $\lambda_{\min}$ and far-field moments is stronger evidence than extra digits on one code; (4) tight residual control on iterative linear solvers (the Hessian solve, not the energy sum, is usually the precision bottleneck); (5) quad or arbitrary precision only on the soft eigenproblem's residual, matching coefficients, or pairing integral.

The cheapest independent monitor in the literature: a topological density that does not integrate to its integer at the same accuracy as the claimed energy is a global error bar on everything else.

## Cross-checks that do not share the soft direction

A claim resting on one soft eigenvalue should be confirmed by at least one observable that is not that eigenvalue. The common set: topological charge to near machine precision; far-field moments against the analytic multipole/Yukawa/GEM tail; the virial/Derrick residual; force from the mutual interaction term or the analytic pairing — never from $E(R)-2E_1$; linearized spectrum versus a short nonlinear perturbation (does the soft mode oscillate, radiate, or grow?); a symmetry-reduced 1-D code at extreme resolution against the 3-D code. If these agree and only $\lambda_{\min}/\lambda_2$ is small, the object is a shallow but real minimum — a legitimate physical regime (lightly bound multi-solitons, near-critical gravitating branches, isospinning solitons just under a critical frequency).

## Reading a marginal candidate

A configuration stable only above a critical box size, with $\lambda_{\min}$ three orders below $\lambda_2$, is treated as a **hypothesis about the continuum** — neither a failed idea nor a finished theorem. The questions the field asks, in the order that saves labour:

1. Is the soft eigenvector a bulk deformation, or a boundary/mesh mode?
2. Does $\lambda_{\min}$ extrapolate to a strictly positive continuum value as $h \to 0$, $R \to \infty$?
3. Does a virial identity close at the claimed accuracy?
4. Does the far-field expansion exist and match the linearized theory?
5. Can the weak interaction sign be read from that far field without a subtracted energy?
6. With a small parameter $\varepsilon$: does the sign survive an $\varepsilon$-expansion about a controlled core, or only when $\varepsilon$ shares the core's grid?
7. If two near-minima exist, is the barrier computed, or only local curvature?

Effort on 5–7 before 1–3 is clean is wasted; a two-body sign from a single-scale 3-D run is not evidence until 4–6 are clean. That ordering is the main labour-saving device. The labour that looks like "many attempts" in a single-scale minimizer is, here, spent once on a controlled core, a trustworthy tail, and a pairing — after that, small ratios are bookkeeping.

## Reproducibility in this regime

One practice specific to execution environments, learned the hard way here: results at the 1e-13-relative level and below depend on BLAS thread count through reduction order alone (measured on our certified evaluator: bit-stable at fixed thread count, 1.6e-15 relative drift between 1 and 2+ threads). A check that passes as a script and flips under importlib/harness invocation is usually this. Pin and record the thread environment and seeds at module level (so imports see them), measure the evaluator's noise floor once across thread counts and invocation paths, and quote it alongside any tolerance — a claimed accuracy below the floor is a prediction about the runner, not the physics. Iterative chains (continuation ladders, root-finding on stiff residuals, eigenvalue sign calls) amplify the floor; validate their outputs independently of the chain that produced them.

## Sources

The papers behind these practices (methods, not exhaustive bibliography):

- Gudnason & Halcrow, *A smörgåsbord of Skyrmions*, [arXiv:2202.01792](https://arxiv.org/abs/2202.01792) — arrested Newton flow, gray-zone near-degeneracies. Lightly bound Skyrme / NEB: [arXiv:2305.18126](https://arxiv.org/abs/2305.18126).
- Vibrational modes of Skyrmions, *Phys. Rev. D* **98**, 125010 (2018), [doi:10.1103/PhysRevD.98.125010](https://doi.org/10.1103/PhysRevD.98.125010); Creek, Donninger, Schlag & Snelson, *Linear stability of the Skyrmion*, [arXiv:1603.03662](https://arxiv.org/abs/1603.03662); QNM/Roper-like vibrations: [arXiv:1710.00837](https://arxiv.org/abs/1710.00837).
- Manton, Schroers & Singer, *The interaction energy of well-separated Skyrme solitons*, [arXiv:hep-th/0212075](https://arxiv.org/abs/hep-th/0212075); baby-Skyrme dipole picture: [arXiv:2101.07552](https://arxiv.org/abs/2101.07552) and the Piette–Zakrzewski–Manton line.
- Gravitating/multi-scale continuation: *Phys. Rev. D* **109**, 045002 (2024), [doi:10.1103/PhysRevD.109.045002](https://doi.org/10.1103/PhysRevD.109.045002); eigenvalue coalescence at critical coupling: Bratek, [arXiv:math-ph/0505043](https://arxiv.org/abs/math-ph/0505043).
- Isospinning critical frequencies: [arXiv:1309.3907](https://arxiv.org/abs/1309.3907).
