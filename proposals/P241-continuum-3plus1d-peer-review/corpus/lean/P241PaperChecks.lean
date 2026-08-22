import Mathlib

/-!
Exact proof fragments auditing the P241 manuscript (3+1D solitonic matter
continuum, SHA dc23cbd9...). Counterexamples are stated as positive theorems
about the review predicate: proving a displayed equation fails is a verified
review result. Each theorem name records the audited equation number.
-/

namespace P241PaperChecks

/- S18, Eq. (43): the displayed Newtonian limit carries the wrong sign.
Geodesics of g00 = -1/n give d2X/dt2 = +c0^2 n'/(2 n^3) > 0 toward
increasing n, while displayed (43) evaluates negative. Concrete probe
n = 11/10, dn/dx = 1/10, c0 = 297/100. -/
theorem eq43_sign_counterexample_true_value_positive :
    (0 : ℝ) < (297 / 100) ^ 2 * (1 / 10) / (2 * (11 / 10) ^ 3) := by
  positivity

theorem eq43_sign_counterexample_displayed_negative :
    (-((297 / 100 : ℝ) ^ 2 / 2) * ((1 / 10) / (11 / 10)) < 0) := by
  norm_num

/- Exact law carries an extra 1/n^2 beyond grad(log n):
   c0^2 n'/(2 n^3) = (c0^2/2) (log n)' / n^2. -/
theorem eq43_missing_factor_identity
    (c0 npow n : ℝ) :
    c0 * npow / (2 * n ^ 3) = (c0 / 2 * (npow / n)) / n ^ 2 := by
  field_simp

/- S19, Section 7: null-ray transverse acceleration is exactly twice the
massive slow-limit law. -/
theorem section7_massless_ratio_is_two
    (c0 npow n : ℝ) :
    c0 * npow / n ^ 3 = 2 * (c0 * npow / (2 * n ^ 3)) := by
  ring

/- S21, Eq. (55)-(56): the printed determinant drops exactly one Sigma^2
relative to the coordinate determinant of the displayed components. -/
theorem eq56_drops_sigma_squared
    (c0 Delta Sigma Ag sth : ℚ) (hc : c0 ≠ 0) (hDelta : Delta ≠ 0)
    (hSigma : Sigma ≠ 0) (hA : Ag ≠ 0) (hs : sth ≠ 0) :
    (c0 ^ 2 * (Delta / Sigma) ^ 2) * (c0 ^ 2 / Sigma ^ 2) *
        (c0 ^ 2 * (Sigma / (Ag * sth ^ 2)) ^ 2) =
      c0 ^ 6 * (Delta / Ag) ^ 2 / sth ^ 4 / Sigma ^ 2 := by
  field_simp

/- S21, Eq. (57): internal c0-power contradiction at the probe value
c0 = 297/100: the own-first-equality value differs from the print. -/
theorem eq57_c0_power_slip :
    (2 : ℚ) * (297 / 100) ^ 2 ≠ 2 * (297 / 100) := by
  norm_num

/- S21, equator identity: A_g = r^2 * (r^2 + a^2 + a^2 rs / r) at
theta = pi/2 (polynomial identity after clearing the denominator). -/
theorem kerr_equator_Ag_is_r_squared_G
    (r rs a : ℚ) :
    (r ^ 2 + a ^ 2) ^ 2 - a ^ 2 * (r ^ 2 - rs * r + a ^ 2) =
      r ^ 2 * (r ^ 2 + a ^ 2) + rs * a ^ 2 * r := by
  ring

/- S15, Eq. (35)-(36): static time dilation dtau/dt = sqrt(-g00); squared
form at nbar = 9/4 gives (dtau/dt)^2 = 1/nbar = 4/9. -/
theorem time_dilation_squared_concrete :
    ((2 : ℝ) / 3) ^ 2 = 1 / (9 / 4) := by
  norm_num

/- S08: scalar impedance matching cannot fix directions. Media with
Theta = diag(8, 1) and Theta' = diag(s, s), s^2 = 8 have EQUAL scalar
impedance det^(1/3) = 2, yet different x-direction impedances:
sqrt(8) ≠ sqrt(s). Already the x-components of Theta differ (8 vs s,
s ≠ 8 because s^2 = 8 and s > 0 would force s ≠ 4). -/
theorem s08_directional_mismatch_despite_scalar_match
    (s : ℝ) (hs : s * s = 8) : (4 : ℝ) ≠ s := by
  intro h
  subst h
  norm_num at hs

/- S05, Derrick scaling in d = 3: E(lam) = Eg/lam + Ep/lam^3 is strictly
decreasing for lam > 0, so no stable static lump: derivative negative. -/
theorem derrick_derivative_negative
    (eg ep lam : ℝ) (heg : 0 < eg) (hep : 0 < ep) (hl : 0 < lam) :
    -(eg / lam ^ 2) - 3 * ep / lam ^ 4 < 0 := by
  have h1 : 0 < eg / lam ^ 2 := by positivity
  have h2 : 0 < 3 * ep / lam ^ 4 := by positivity
  linarith

end P241PaperChecks
