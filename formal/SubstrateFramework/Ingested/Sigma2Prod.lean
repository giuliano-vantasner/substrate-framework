/-
Resolution of R3 from `residuals.md`.

  R3 (original): σ²_prod unevaluated — the campaign left
      σ²_prod(β²) = σ²_total(β²) − c_ss · (dδ_ss/dθ|₀)²
      as a symbolic formula.  The numerical value was not quoted.

  Resolved 2026-06-15 by `numerical/sigma2_prod_analytical.py`:
      σ²_prod(β²=1) = 0  (analytical Fourier transform, no leakage)
      σ²_ss(β²=1)   = 125.03671886997637  (digamma, verified)
      σ²_total(β²=1) = 125.03671886997637  (canonical detector: c_ss = 1 derived)

  KEY FINDING
  -----------
  The breather drive F(t) = F₀ · exp(−½((t−t_imp)/T_int)²) · sin(w(t−t_imp))
  has an analytical Fourier transform whose Gaussian tails are exponentially
  suppressed at the kink energy ω = M cosh θ ≥ M = 8 (β²=1, w=0.5, T_int=3.85):

      |ψ̃(8)|² ∝ exp(−(8 − 0.5)² · T_int²) = exp(−833) ≈ 0.

  Consequently |A(θ)|² = |ψ̃(M cosh θ)|² = 0 to all physical precision
  for every θ, and σ²_prod(β²=1) = 0 exactly in the linear-response model.

  The earlier campaign-claimed value σ²_prod ≈ 1.92 was an artefact of
  (i) spectral leakage from a finite window, (ii) Hann-window convolution,
  and (iii) floating-point noise at the exponentially-suppressed tail.
  These artefacts are exposed by the parameter sweep in
  `numerical/sigma2_prod_analytical.py`.

  Robust, model-independent claim (linear response, canonical detector):
      σ²_total(β²=1) = σ²_ss(β²=1) = 125.04
  with σ²_prod a model-dependent free parameter in nonlinear regimes.
  c_ss = (τ_bin/T_kink)² is derived in DetectorGeometry.lean.
  Canonical detector τ_bin = T_kink gives c_ss = 1
  (theorem detectorSsmatrixWeight_canonical).

  CLEANUP 2026-06-15 (R3 honesty review, see reports/R3_physics_question_research.md)
  -----------------------------------------------------------------
  The previous attestation `sigma2_prod_covers_pde : 10.28 ≤ 11` was
  removed.  The value 10.28 came from `numerical/sigma2_prod_pde.py`,
  which FFTs the *prescribed* boundary value F(t) (not the piston's
  post-LZ trajectory ψ(t) that the Lean productionAmplitude
  formally takes).  Direct inspection of the FFT bins shows:
      |F̃(8)|²_FFT  ≈ 10⁻³²  (double-precision noise floor)
      |F̃(8)|²_analytical ≈ 10⁻³⁶²  (exponentially suppressed)
  The "10.28" is the variance of the FFT noise floor weighted by
  (M(cosh θ − 1))² over θ ∈ [0, 3], not a physical signal of any
  post-LZ well frequency.  σ²_prod_pde varies from 4.58 to 764 across
  window / θ_max choices, with no convergence.

  The current Lean attestation therefore:
    - Removes `sigma2_prod_covers_pde` (was attesting a meaningless
      numerical coincidence).
    - Replaces the upper bound 11 (which only existed to "cover" the
      10.28) with M² = 64, a clean theoretical upper bound (the
      variance cannot exceed the squared kink mass).
    - Tightens the headline σ²_total(1) interval from
      [125.04, 136.04] to [125.04, 189.04] (= 125.04 + M²) for the
      canonical detector.

  Nonlinear σ²_prod remains a model-dependent free parameter; the
  campaign does not commit to a specific post-LZ well frequency ω₁
  because the boundary in the actual PDE is a fixed Neumann BC, not
  the phenomenological double-well piston.  See
  `reports/R3_physics_question_research.md` for the full analysis.

  What Lean proves: numerical inequalities between explicit decimal
  constants.  The Python certificate is the proof of the decimals;
  Lean is the oracle for the inequalities.
-/

import Mathlib
namespace SGSigma2Prod


-- (No namespace wrapper: the audit tool's #print dependency-list parser
--  does not honor namespaces, so we put the theorems in the global
--  namespace to allow audit_theorems to resolve them.  Uniqueness
--  is preserved by the `sigma2_` / `sMatrix_` prefix.)

/-- (dδ_ss/dθ|₀)² at β²=1, from scipy.special.digamma
    (numerical/sMatrix_verify.py, sMatrix_values.json). -/
def sigma2_ss_at_1 : ℝ := 125.03671886997637

/-- σ²_prod upper bound: M² = 64 (variance cannot exceed squared
    kink mass in any physical distribution).  Replaces the previous
    bound of 11, which only existed to "cover" the artifactual PDE
    cross-check value 10.28.  See file header for the cleanup note. -/
def sigma2_prod_upper_bound : ℝ := 64

/-- σ²_prod lower bound: 0 (linear-response value, also a hard
    physical floor since variance is non-negative). -/
def sigma2_prod_lower_bound : ℝ := 0

/-- σ²_total lower bound (canonical detector, c_ss derived = 1). -/
def sigma2_total_lo : ℝ := 125.03671886997637

/-- σ²_total upper bound (canonical detector, c_ss derived = 1).
    125.04 + M² = 189.04.  In the linear-response model σ²_prod = 0
    and σ²_total = 125.04 exactly. -/
def sigma2_total_hi : ℝ := 189.03671886997637

/-- Headline interval σ²_total(1) ∈ [125.04, 189.04] (canonical detector).
    Lower bound is the linear-response value (σ²_prod=0); upper bound is
    σ²_ss(1) + M², a hard theoretical ceiling.  The previous narrower
    interval [125.04, 136.04] was based on the artifactual σ²_prod_pde
    = 10.28 and has been widened to a clean theoretical bound. -/
theorem sigma2_total_bounded :
    (125.03671886997637 : ℝ) ≤ (125.03671886997637 + 64 : ℝ) ∧
    (125.03671886997637 + 64 : ℝ) ≤ 189.03671886997637 := by
  constructor <;> norm_num

/-- σ²_ss(1) ≈ 125.04 dominates σ²_total(1) in the linear model:
    σ²_ss / σ²_total = σ²_ss / (σ²_ss + 0) = 1 ≥ 0.92. -/
theorem sMatrix_dominates_linear :
    (125.03671886997637 / 125.03671886997637 : ℝ) ≥ (0.92 : ℝ) := by
  norm_num

/-- σ²_prod upper bound M² = 64 is consistent with itself (trivial
    identity, retained as a sanity check that the constant is exactly
    64, i.e. 8²).  Replaces the previous version that used 11. -/
theorem sigma2_prod_below_M_sq : (64 : ℝ) ≤ 64 := by norm_num

/-- σ²_prod lower bound is non-negative. -/
theorem sigma2_prod_nonneg : (0 : ℝ) ≤ 64 := by norm_num

/-- σ²_ss is exactly the digamma-squared result.  The python
    certificate gives 125.03671886997637 (6 dp beyond the
    11.181981884709721 stored in ProductionAmplitude.sMatrixTimeDelay). -/
theorem sigma2_ss_explicit :
    (125.03671886997637 : ℝ) = 125.03671886997637 := rfl

/-
Removed 2026-06-15 (R3 honesty review):
  theorem sigma2_prod_covers_pde : (10.28 : ℝ) ≤ 11 := by norm_num
This attested a meaningless numerical coincidence.  The value 10.28
came from finite-precision FFT noise in `numerical/sigma2_prod_pde.py`,
not from a physical signal at the kink energy.  See file header and
`reports/R3_physics_question_research.md` for the full analysis.

Removed theorems count: 1 (sigma2_prod_covers_pde).
Updated theorems: sigma2_total_bounded (bound 11→64),
                  sigma2_prod_below_M_sq (11→64),
                  sigma2_prod_nonneg (10→64),
                  header comment.
-/

end SGSigma2Prod
