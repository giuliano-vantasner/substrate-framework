---
description: Accepted framework claim C-SPN-002
author: framework-registry
created: '2026-08-07T22:30:00Z'
updated: '2026-08-07T22:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-SPN-002
category: claims
confidence: established
status: active
---
# C-SPN-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let N be a positive integer and let H=(C^2)^(tensor N) have the orthonormal computational basis of N declared two-state factors. For 0<=k<=N, let |D_N^k> be the normalized equal superposition of all binomial(N,k) basis vectors with exactly k excited factors. With local dimensionless raises sigma_i^+ and a declared real operator scale s, define J_+=s*sum_i sigma_i^+, J_-=J_+^dagger, and J_z=(s/2)*sum_i sigma_i^z. Then exactly J_+|D_N^k>=s*sqrt((N-k)*(k+1))*|D_N^(k+1)> for k<N and zero for k=N; J_-|D_N^k>=s*sqrt(k*(N-k+1))*|D_N^(k-1)> for k>0 and zero for k=0. In j=N/2, m=k-N/2 coordinates these are the standard irreducible su(2) ladder coefficients, with [J_+,J_-]=2*s*J_z and Casimir J_z^2+(J_+*J_-+J_-*J_+)/2=s^2*j*(j+1). The ground-edge coefficient is s*sqrt(N), while central-rung coefficients are order N and approach N*abs(s)/2 in magnitude for even N. More generally, for a weighted ground-state raise A_+=a*sum_i g_i*sigma_i^+ with declared complex g_i and a, its projection on |D_N^1> is a*sum_i(g_i)/sqrt(N), its total one-excitation norm squared is |a|^2*sum_i|g_i|^2, and the orthogonal dark norm squared is their nonnegative difference. Hence the familiar equal-coupling square-root enhancement requires equal magnitudes and phases; unequal phases can cancel the symmetric projection without canceling the full image. These are exact normalized finite-dimensional vector-space identities. A squared ladder coefficient is not a rate. The theorem establishes no physical two-level constituents, nuclear or phonon state, symmetric preparation, common mode, interaction Hamiltonian, resonance, spectral density, linewidth, decoherence, Fermi-Golden-Rule regime, supertransfer, material realization, or observed transition rate.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: N is a positive integer, the local two-state factors and tensor-product inner product are declared, and the computational basis is orthonormal., Each Dicke vector uses the displayed equal-weight binomial normalization and belongs to the permutation-symmetric maximal-spin sector; the theorem does not assert that a supplied system occupies or remains in this sector., The collective ladder uses a sum of local dimensionless raises with one common explicitly real scale s. Replacing the sum by an average or changing local normalization changes the coefficient., The weighted ground-state statement permits arbitrary declared complex site couplings and global scale; its dark-sector nonnegativity is the finite-dimensional Cauchy-Schwarz identity., Calling s hbar is a convention only when the local operators and physical angular momentum normalization are separately declared. The exact algebra supplies no interaction coupling or energy scale., A physical Golden-rule rate would additionally require a complete interaction matrix element, on-shell final-state measure or spectral density, energy and normalization conventions, and validity assumptions; none is imported here.. Comparators: PN3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its ground-edge formula and rate label were exposed before P111, while all-rung, normalization, unequal-coupling, physical-ceiling, mutation, and consumer criteria were frozen before source execution.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.93.0` with provenance `campaigns/P111-pn3-symmetric-spin-ladder-audit/adjudication.yaml`.

- `campaigns/P111-pn3-symmetric-spin-ladder-audit/verify.py`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/reviews/independent_spin_review.py`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/attempts/0001/result.yaml`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/attempts/0002/result.yaml`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/evidence/source-reproduction.yaml`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/evidence/source-audit.yaml`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/evidence/check-adjudication.yaml`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/evidence/dependency-audit.yaml`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/evidence/consumer-audit.yaml`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/evidence/candidate-comparison.yaml`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/evidence/primary-provenance.yaml`
- `campaigns/P111-pn3-symmetric-spin-ladder-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-SPN-002-review.md`
- `tests/test_symmetric_spin.py`
