---
description: Accepted framework claim C-WID-001
author: framework-registry
created: '2026-08-02T22:00:00Z'
updated: '2026-08-02T22:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-WID-001
category: claims
confidence: established
status: active
---
# C-WID-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Declare Minkowski metric (+---), q=p'-p, Q^2=-q^2, positive equal on-shell mass M, positive F and m_pi^2, dimensionless form factors, and the current bracket [gamma^mu*G_A(Q^2)+q^mu*G_P(Q^2)/(2*M)]*gamma5. Exact on-shell contraction gives normalized divergence G_A-Q^2*G_P/(4*M^2). Separately declaring the normalized PCAC source F*m_pi^2*G_piNN(Q^2)/(M*(m_pi^2+Q^2)) yields a generalized residual that retains G_P independently. Under the additional pion-pole-dominance premise G_P=4*M*F*G_piNN/(m_pi^2+Q^2), the residual reduces exactly to G_A-F*G_piNN/M. Adding an induced-form-factor remainder R(Q^2) finite at zero and at Q^2=-m_pi^2 changes that residual by -Q^2*R/(4*M^2), leaves the pole residue 4*M*F*G_piNN(-m_pi^2) unchanged, and drops out only at zero transfer. The PCAC kernel m_pi^2/(m_pi^2+Q^2) has zero-transfer-then-chiral limit one, chiral-then-zero-transfer limit zero, and fixed path Q^2=rho*m_pi^2 value 1/(1+rho). This exact conditional theorem derives no QCD current or PCAC identity, pion-pole dominance, physical pion or nucleon, coupling value, effective action, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The metric, momentum-transfer sign, equal-mass on-shell spinors, dimensionless form-factor normalization, isospin factor, and current decomposition are declared exactly as stated., The normalized PCAC source and pion-nucleon form factor are conditional premises; pion-pole dominance is a further independent premise and not a consequence of on-shell Dirac algebra., The regular remainder and coupling are finite at the stated evaluation points, and the positive scales are nonzero; changing conventions requires an explicit conversion of every displayed factor and sign., Primary literature supplies scope and convention provenance only; no empirical or lattice value, QCD state construction, or fitted parameter is imported.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.57.0` with provenance `campaigns/P063-pg4-goldberger-treiman/adjudication.yaml`.

- `campaigns/P063-pg4-goldberger-treiman/verify.py`
- `campaigns/P063-pg4-goldberger-treiman/attempts/0001/result.yaml`
- `campaigns/P063-pg4-goldberger-treiman/attempts/0005/result.yaml`
- `campaigns/P063-pg4-goldberger-treiman/reviews/independent_axial_review.py`
- `campaigns/P063-pg4-goldberger-treiman/evidence/primary-provenance.yaml`
- `campaigns/P063-pg4-goldberger-treiman/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-WID-001-review.md`
- `tests/test_axial_ward.py`
