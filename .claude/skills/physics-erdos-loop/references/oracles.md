# Oracle selection and verifier sensitivity

Use the strongest practical oracle for each claim and state exactly what verdict it earns.

| Claim | Preferred oracle | Maximum verdict |
| --- | --- | --- |
| Exact identity, ansatz residual, algebra, series, exact limit | SymPy or direct symbolic algebra | `symbolic_verified` |
| Finite algebraic, order, combinatorial, or topological theorem | Lean with audited axioms | `formal_verified` |
| Root, eigenvalue, BVP/IVP, integral, optimization without closed form | Independent numerical methods plus refinement | `numeric_evidence` |
| Time-dependent PDE or nonlinear dynamics | Simulation plus convergence, conservation, and method cross-check | `simulation_evidence` |
| Figure or visualization | Rendering tool | artifact only |

Split composite claims so each part receives the right oracle. Discover numerically, then prove symbolically or formally when the structure permits.

## Symbolic checks

- Derive expressions from canonical inputs.
- Substitute the candidate into the governing equation.
- Assert the unsimplified and simplified structure where sign or branch information matters.
- Test domains, branches, dimensions, symmetries, special cases, and limits.
- Mutate coefficients and signs; the residual check must fail.

An identity that holds only because both sides contain the same copied literal is not verification.

## Numerical checks

- Record precision, solver, mesh/domain, timestep, tolerances, and stopping criteria.
- Refine resolution, timestep, domain, and tolerance independently.
- Compare two methods or an analytically soluble limit.
- Track conserved quantities and discretization error.
- Separate solver convergence from physical-model validity.
- Never loosen a tolerance after seeing failure without a prior physical or numerical error model.

Numeric evidence does not become exact verification because it has many digits.

## Formal checks

- Prove the exact statement needed by the physics claim.
- Reject `sorry`, `admit`, `unsafe`, new axioms, proof by importing the target, and silent theorem weakening.
- Inspect the target theorem's axiom footprint.
- Distinguish definitions and decimal attestations from derivations.
- Audit the map between the formal statement and the physical interpretation.

A theorem can be perfectly proved and still encode too weak a proposition.

## Mutation and counterexample audit

For each load-bearing input, construct a scientifically meaningful mutation:

- coefficient or normalization change;
- sign flip;
- wrong convention;
- parameter outside the claimed regime;
- perturbed imported constant;
- fabricated fitted parameter;
- broken boundary or initial condition.

At least one relevant assertion must fail for every mutation. If the headline numbers move while the tally stays green, the verifier does not establish the headline claim.

## Independent rederivation

Reimplement load-bearing normalizations, convention conversions, and parameter eliminations through a different route with no shared helper beyond canonical primitives. Agreement between two calls to the same copied formula is not independence.

## Comparator gate

Empirical data may test a frozen prediction. It must not:

- choose among concepts before structural criteria are applied;
- appear as a derivation input under a new name;
- determine a tolerance or free parameter after results are seen;
- become a pass condition for a supposedly first-principles derivation.

Open the comparator gate after equations, conventions, selection criteria, and structural tests are frozen. Report disagreement, then continue improving the candidate set; do not refit the framework narrative.
