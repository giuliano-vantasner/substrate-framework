import Mathlib

/-!
Exact proof fragments for the P238 peer review. The theorems intentionally
include counterexamples: proving that a displayed candidate fails is a positive
verification result about the review predicate.
-/

namespace P238PaperChecks

theorem materialDerivativeSquare
    (ut vx vy ux uy : ℝ) :
    (ut + vx * ux + vy * uy) ^ 2 =
      ut ^ 2 + 2 * ut * (vx * ux + vy * uy) +
        vx ^ 2 * ux ^ 2 + 2 * vx * vy * ux * uy + vy ^ 2 * uy ^ 2 := by
  ring

theorem determinantMatchedAnisotropyStillReflects :
    (((2 : ℚ) - 1) / (2 + 1)) = 1 / 3 := by
  norm_num

theorem claimedAnisotropicInverseFailsXX :
    (4 : ℚ) * (1 / 4) * 2 ≠ 1 := by
  norm_num

theorem claimedAnisotropicInverseFailsYY :
    (4 : ℚ) * (1 / 64) * 8 ≠ 1 := by
  norm_num

theorem correctedAnisotropicInverseXX :
    (4 : ℚ) * (1 / 4) * ((2 ^ 2) / 4) = 1 := by
  norm_num

theorem correctedAnisotropicInverseYY :
    (4 : ℚ) * (1 / 64) * ((8 ^ 2) / 4) = 1 := by
  norm_num

theorem schwarzschildRadialConformalIdentity
    (f : ℝ) (hf : f ≠ 0) :
    f * (1 / f ^ 2) = 1 / f := by
  field_simp

theorem minimalRotatingCrossTermIsNotKerrAtSample :
    (-(1 : ℚ) / 10) ≠ -((1 : ℚ) / 10) * (1 / 2) := by
  norm_num

theorem minimalRotatingAngularTermIsNotKerrAtSample :
    (4 : ℚ) ≠ 4 + (1 / 100 : ℚ) + (1 / 200 : ℚ) := by
  norm_num

theorem rigidAnsatzVelocityDependenceIsQuadratic
    (inertia velocity flow constant : ℝ) :
    inertia / 2 * (velocity - flow) ^ 2 - constant =
      inertia / 2 * velocity ^ 2 - inertia * flow * velocity +
        inertia / 2 * flow ^ 2 - constant := by
  ring

theorem masslessEinbeinVariationImpliesNullConstraint
    (einbein tangentNorm : ℝ) (he : einbein ≠ 0)
    (variation : -tangentNorm / (2 * einbein ^ 2) = 0) :
    tangentNorm = 0 := by
  field_simp [he] at variation
  linarith

end P238PaperChecks
