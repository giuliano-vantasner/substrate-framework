import Mathlib

/-!
Constructive replacement theorems for repairable P238 draft claims.  These
preserve the intended effective-particle and analogue-Kerr objectives while
making the additional hypotheses and corrected coefficients explicit.
-/

namespace P238ReplacementProofs

theorem boostedFamilyLegendreTransform
    (restEnergy speed velocity gamma : ℝ)
    (hspeed : speed ≠ 0) (hgamma : gamma ≠ 0)
    (hboost : gamma ^ 2 * (speed ^ 2 - velocity ^ 2) = speed ^ 2) :
    (gamma * restEnergy * velocity / speed ^ 2) * velocity -
      gamma * restEnergy = -restEnergy / gamma := by
  field_simp [hspeed, hgamma]
  have hscaled := congrArg (fun value : ℝ => restEnergy * value) hboost
  ring_nf at hscaled ⊢
  linarith

theorem correctedOneDimensionalInverse00
    (nbar n velocity : ℝ) (hnbar : nbar ≠ 0) :
    (nbar * (-1)) * ((-1 + n ^ 2 * velocity ^ 2) / nbar) +
        (nbar * (-velocity)) * (-n ^ 2 * velocity / nbar) = 1 := by
  field_simp [hnbar]
  ring

theorem correctedOneDimensionalInverse01
    (nbar n velocity : ℝ) (hnbar : nbar ≠ 0) :
    (nbar * (-1)) * (-n ^ 2 * velocity / nbar) +
        (nbar * (-velocity)) * (n ^ 2 / nbar) = 0 := by
  field_simp [hnbar]
  ring

theorem correctedOneDimensionalInverse10
    (nbar n velocity : ℝ) (hnbar : nbar ≠ 0) (hn : n ≠ 0) :
    (nbar * (-velocity)) * ((-1 + n ^ 2 * velocity ^ 2) / nbar) +
        (nbar * (1 / n ^ 2 - velocity ^ 2)) *
          (-n ^ 2 * velocity / nbar) = 0 := by
  field_simp [hnbar, hn]
  ring

theorem correctedOneDimensionalInverse11
    (nbar n velocity : ℝ) (hnbar : nbar ≠ 0) (hn : n ≠ 0) :
    (nbar * (-velocity)) * (-n ^ 2 * velocity / nbar) +
        (nbar * (1 / n ^ 2 - velocity ^ 2)) * (n ^ 2 / nbar) = 1 := by
  field_simp [hnbar, hn]
  ring

theorem exactKerrCrossCoefficient
    (radius schwarzschildRadius spin delta angular : ℝ)
    (hradius : radius ≠ 0) (hdelta : delta ≠ 0)
    (hangular : angular ≠ 0) :
    (delta / angular) *
        (-(angular ^ 2 / delta) *
          (spin * schwarzschildRadius / (radius * angular))) =
      -spin * schwarzschildRadius / radius := by
  field_simp [hradius, hdelta, hangular]

theorem exactKerrRadialCoefficient
    (radius delta angular : ℝ) (hdelta : delta ≠ 0)
    (hangular : angular ≠ 0) :
    (delta / angular) * (radius ^ 2 * angular / delta ^ 2) =
      radius ^ 2 / delta := by
  field_simp [hdelta, hangular]

theorem kerrAdmIdentity
    (radius schwarzschildRadius spin : ℝ)
    (hradius : radius ≠ 0) :
    let delta := radius ^ 2 - schwarzschildRadius * radius + spin ^ 2
    let angular :=
      radius ^ 2 + spin ^ 2 + spin ^ 2 * schwarzschildRadius / radius
    delta - spin ^ 2 * schwarzschildRadius ^ 2 / radius ^ 2 =
      angular * (1 - schwarzschildRadius / radius) := by
  dsimp
  field_simp [hradius]
  ring

theorem exactKerrTemporalCoefficient
    (radius schwarzschildRadius spin delta angular : ℝ)
    (hradius : radius ≠ 0) (hdelta : delta ≠ 0)
    (hangular : angular ≠ 0)
    (hadm : delta - spin ^ 2 * schwarzschildRadius ^ 2 / radius ^ 2 =
      angular * (1 - schwarzschildRadius / radius)) :
    (delta / angular) *
        (-1 + (angular ^ 2 / delta) *
          (spin * schwarzschildRadius / (radius * angular)) ^ 2) =
      -(1 - schwarzschildRadius / radius) := by
  field_simp [hradius] at hadm
  field_simp [hradius, hdelta, hangular]
  linear_combination -hadm

end P238ReplacementProofs
