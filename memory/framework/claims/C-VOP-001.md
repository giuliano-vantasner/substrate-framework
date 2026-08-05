---
description: Accepted framework claim C-VOP-001
author: framework-registry
created: '2026-08-11T22:35:00Z'
updated: '2026-08-11T22:35:00Z'
tags:
- substrate-framework
- accepted-claim
- C-VOP-001
category: claims
confidence: established
status: active
---
# C-VOP-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

On C-OSC-001's standard one-mode bosonic Fock space with orthonormal number basis |n>, let alpha be a separately declared complex number and let S=conjugate(alpha)*alpha. The norm-convergent vector |alpha>=exp(-S/2)*sum_{n=0}^infinity alpha^n/sqrt(n!)*|n> is normalized, obeys a|alpha>=alpha|alpha>, and has exact overlap <alpha|beta>=exp(-(S_alpha+S_beta)/2+conjugate(alpha)*beta). A measurement of the declared number operator on |alpha> has Born probability p_alpha(n)=exp(-S)*S^n/n!, with mean and variance S. At alpha=0 only the vacuum has nonzero probability; for alpha!=0 every nonnegative occupation has positive probability. C-CMB-003 therefore supplies the complete mode and tail corollaries: noninteger positive S has mode floor(S), while positive integer S has both adjacent modes S-1 and S. In the standard infinite Weyl representation, D(alpha)=exp(alpha*a_dagger-conjugate(alpha)*a) maps |0> to |alpha>; for real lambda and alpha=i*lambda its generator is i*lambda*(a+a_dagger). This conditional identification is not justified by treating a finite truncated commutator as globally central. The number law is a probability only for the declared coherent state and number measurement. It does not quantize or prepare the accepted classical medium, identify S with a classical peak, RMS phase, material variance, or supplied energy band, change the minima of a cosine potential, derive a Huang-Rhys or Franck-Condon material Hamiltonian, or supply an interaction, transition, branching, reaction, channel, physical occurrence probability, rate, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-OSC-001, C-CMB-003. Assumptions: The theorem uses C-OSC-001's standard infinite one-mode Fock representation and number basis. A finite matrix truncation has a top-edge commutator defect and is not a global Weyl representation., Alpha is a separately supplied exact complex number. The series definition fixes the Gaussian normalization and is norm convergent for every finite S=abs(alpha)^2., The Born probabilities concern the spectral measurement of the declared number operator on the declared coherent vector. A physical preparation protocol observable calibration or event process is not inferred., The Weyl-displacement identification assumes the standard unitary displacement representation and its operator ordering. Pure-creation normal ordering or a compact-phase multiplication vertex is a different operator family., C-CMB-003 supplies the mathematical factorial-one mode moment and tail theorems. Its positive-integer adjacent mode tie is retained exactly., Unbounded nonnegative occupation support for nonzero alpha does not imply an unbounded classical configuration excursion or create additional minima of a potential., No accepted claim maps alpha or S to WN6's classical peak or RMS convention C-QFL-001's distinct vacuum variance PN2's external energy band or a material Huang-Rhys parameter.. Comparators: MD3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its 41-check result was exposed in earlier source graphs before P198 froze the operator taxonomy criteria mutations and ceilings, C-OSC-001 supplies the Fock ladder and mathematical factorial-one family but no normalized coherent state overlap or number-measurement preparation, C-CMB-003 supplies the normalized mass modes moments and tails but no Fock-state amplitude or Born measurement semantics, A compact phase multiplication vertex is unitary and shifts Fourier labels while preserving pointwise density so generic vertex language cannot identify it with a Weyl displacement.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.147.0` with provenance `campaigns/P198-md3-vertex-operator-audit/adjudication.yaml`.

- `campaigns/P198-md3-vertex-operator-audit/verify.py`
- `campaigns/P198-md3-vertex-operator-audit/reviews/independent_coherent_state_review.py`
- `campaigns/P198-md3-vertex-operator-audit/reviews/replay_source_graph.py`
- `campaigns/P198-md3-vertex-operator-audit/reviews/C-VOP-001-claim-review.md`
- `campaigns/P198-md3-vertex-operator-audit/reviews/MD3-disposition-review.md`
- `campaigns/P198-md3-vertex-operator-audit/reviews/source_adjudication.md`
- `campaigns/P198-md3-vertex-operator-audit/reviews/impact_analysis.md`
- `campaigns/P198-md3-vertex-operator-audit/attempts/0003/result.yaml`
- `campaigns/P198-md3-vertex-operator-audit/attempts/0004/result.yaml`
- `campaigns/P198-md3-vertex-operator-audit/attempts/0005/result.yaml`
- `campaigns/P198-md3-vertex-operator-audit/attempts/0006/result.yaml`
- `campaigns/P198-md3-vertex-operator-audit/attempts/0007/result.yaml`
- `campaigns/P198-md3-vertex-operator-audit/attempts/0008/result.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/formula-freeze.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/input-provenance.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/dependency-audit.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/consumer-audit.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/candidate-comparison.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/implementation-audit.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/gitnexus-impact.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/primary-provenance.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/independent-provenance.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/source-reproduction.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/consumer-reproduction.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/compatibility-audit.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/source-audit.yaml`
- `campaigns/P198-md3-vertex-operator-audit/evidence/check-adjudication.yaml`
- `memory/vantasner/decisions/C-VOP-001-review.md`
- `memory/vantasner/decisions/MD3-qualified-review.md`
- `src/substrate_framework/coherent_states.py`
- `tests/test_coherent_states.py`
