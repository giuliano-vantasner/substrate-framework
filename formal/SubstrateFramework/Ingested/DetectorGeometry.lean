/-
Detector geometry for the HBT S-matrix weight c_ss.

Operational definition (hbt_observable_gate.md, bridge.md K9–K13):
  The particle-counting HBT correlator g₂(τ) is measured with arrival-time
  difference τ_phys binned in width τ_bin.  The approach law is quoted in
  dimensionless time τ̃ = τ_phys / T_kink where T_kink = 1/M is the kink
  Compton time (M = 8/β²).

Expanding the temporal coherence χ(τ_phys) = ∫ ρ(E) e^{iE τ_phys} dE in
τ̃ gives a production contribution Var(ω)/M² (ω = kinetic energy above
rest mass M).  The same-charge S-matrix phase derivative dδ_ss/dθ|₀
contributes at O(τ̃²) with coefficient (τ_bin/T_kink)² — the squared
ratio of the coincidence-bin width to the kink temporal width.

Therefore the S-matrix weight is NOT a free parameter:
  c_ss(β²) = (τ_bin / T_kink(β²))².

Canonical campaign detector: τ_bin = T_kink ⇒ c_ss = 1.
-/

import Mathlib
import SubstrateFramework.Ingested.ProductionAmplitude
namespace SGDetectorGeometry

open SGProductionAmplitude

open Real

/-- Kink Compton time T_kink = 1/M = β²/8 (units m=1, ℏ=1). -/
noncomputable def kinkComptonTime (βsq : ℝ) : ℝ := βsq / 8

theorem kinkComptonTime_eq_inv_mass (βsq : ℝ) (hβ : βsq ≠ 0) :
    kinkComptonTime βsq = 1 / kinkMass βsq := by
  dsimp [kinkComptonTime, kinkMass]
  field_simp [hβ]

/--
Detector S-matrix weight derived from geometry:
  c_ss = (τ_bin / T_kink)².
This is the coefficient on (dδ_ss/dθ|₀)² in the HBT-normalized σ².
-/
noncomputable def detectorSsmatrixWeight (τ_bin βsq : ℝ) : ℝ :=
  (τ_bin / kinkComptonTime βsq) ^ 2

/-- Canonical detector: coincidence bin equals Compton time ⇒ c_ss = 1. -/
theorem detectorSsmatrixWeight_canonical (βsq : ℝ) (hβ : βsq ≠ 0) :
    detectorSsmatrixWeight (kinkComptonTime βsq) βsq = 1 := by
  dsimp [detectorSsmatrixWeight, kinkComptonTime]
  field_simp [hβ]

/-- Non-negative weight when τ_bin ≥ 0. -/
theorem detectorSsmatrixWeight_nonneg (τ_bin βsq : ℝ) :
    0 ≤ detectorSsmatrixWeight τ_bin βsq := by
  dsimp [detectorSsmatrixWeight]
  exact sq_nonneg _

/--
Production spectral variance in HBT units (τ̃ = τ_phys / T_kink):
  σ²_prod,HBT = Var(ω) / M².
-/
noncomputable def spectralVarianceHBT (βsq : ℝ) (ψ : ℝ → ℝ) : ℝ :=
  spectralVariance βsq ψ / (kinkMass βsq) ^ 2

/--
Total HBT spectral variance with derived (not free) S-matrix weight:
  σ² = Var(ω)/M² + c_ss · (dδ_ss/dθ|₀)²,
  c_ss = (τ_bin/T_kink)².
-/
noncomputable def totalSpectralVarianceHBT
    (τ_bin βsq : ℝ) (ψ : ℝ → ℝ) : ℝ :=
  spectralVarianceHBT βsq ψ +
    detectorSsmatrixWeight τ_bin βsq * (sMatrixTimeDelay βsq) ^ 2

/-- Convenience: canonical detector τ_bin = T_kink. -/
noncomputable def totalSpectralVarianceCanonical (βsq : ℝ) (ψ : ℝ → ℝ) : ℝ :=
  totalSpectralVarianceHBT (kinkComptonTime βsq) βsq ψ

/--
At β² = 4π the S-matrix term vanishes regardless of detector geometry.
-/
theorem totalVarianceHBT_free_fermion (τ_bin : ℝ) (ψ : ℝ → ℝ) :
    totalSpectralVarianceHBT τ_bin (4 * π) ψ = spectralVarianceHBT (4 * π) ψ := by
  dsimp [totalSpectralVarianceHBT]
  rw [sMatrixTimeDelay_free_fermion]
  simp

/--
Canonical detector at β² = 4π: σ² equals the HBT-normalized production term.
-/
theorem totalVarianceCanonical_free_fermion (ψ : ℝ → ℝ) :
    totalSpectralVarianceCanonical (4 * π) ψ = spectralVarianceHBT (4 * π) ψ := by
  dsimp [totalSpectralVarianceCanonical, totalSpectralVarianceHBT]
  rw [sMatrixTimeDelay_free_fermion]
  simp
end SGDetectorGeometry
