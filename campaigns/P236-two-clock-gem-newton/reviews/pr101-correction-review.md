# PR #101 bounded corrective review

Frozen transaction: the P236 campaign files added by source head
`5ba1fe63a0c4e37acb0f3ce2e796f12e64c82ea4`; accepted claims and unrelated
consumers are outside the delta. The reviewer did not author that source
transaction. The user explicitly directed the reviewer to correct defects
and merge the named PR rather than reject or reduce it.

## Substantive review findings and repairs

1. **Blocking — invalid frame.** The submitted active `O4` had median
   `max|O^T O-I|=0.5` and maximum `0.997`; its `q2=0` path did not reproduce
   the single source. Repaired with an orthogonal cylindrical M5.17 frame.
   Correction gate: orthogonality `8.88e-16`, `q2=0` matrix residual `0`.
2. **Blocking — imposed and doubled ambient field.** The submitted sum of two
   tails tends to `2a0`, not one shared mediator. Repaired with one ambient
   rapidity and two pinned core weights.
3. **Blocking — relaxation was not the measured state.** The submitted
   mediation arm did not relax the field used by its headline ladder.
   Repaired by minimizing the guarded M5.21.8 rapidity at every `(n,D,d)` on
   the exact measurement lattice. Every result is an interior minimum with
   positive curvature. The M5.21.14 prohibition on unrestricted descent is
   retained, not bypassed.
4. **Blocking — subtraction/mask artifact.** Separately integrated pair and
   single masks contaminated `U`. Repaired by subtracting the three sector
   densities pointwise on one pair mask.
5. **Blocking — circular exponent.** The submitted force exponent came from
   residuals after forcing `U_inf+C/d`. Repaired by direct raw differences
   followed by a free log-force slope. Logarithmic and linear energy models
   are evaluated as hostile alternatives.
6. **Blocking — verifier trusted summaries.** Raw rows could be changed while
   its verdict stayed green. Repaired verifier derives every coefficient,
   force, exponent, RMSE, and convergence statement from raw rows.
7. **Blocking — invalid #89 magnitude bridge.** `Lambda=pi/h` and the numeric
   mass comparison were undeclared, and the mass algebra was wrong. Repaired
   by retaining symbolic positive `Lambda`, using the exact accepted API,
   typing the raw-action normalization `Z_GEM`, and checking its magnitude
   with the independent cylinder pipeline. No accepted claim was edited.
8. **Blocking — no independent grid axis.** Repaired with both a growing-box
   ladder and a fixed-domain 24^3 -> 32^3 -> 48^3 refinement.
9. **Incorrect extra claim — anti-pair sign flip.** The corrected field gives
   cancellation, not the claimed flip. It was not required by issue #96 and
   is removed. The required attractive-sign control is the measured negative
   force plus C-GRV-002; the load-bearing mutation is source deletion.

## Strongest surviving and corrected result

The original numerical rows do not survive. The objective does: the corrected
calculation measures attractive inverse-square force exponents
`-2.032/-2.044/-2.060` on the growing-box ladder and
`-2.044/-2.047/-2.060` on fixed-domain grid refinement. The finest raw
coefficient is `-123.9048`; the independent pipeline gives exponent `-2.0204`
and coefficient `-118.3291`.

## Correction check

The correction check is bounded to the nine repairs above, the OpenWave
driver/import surface, the P231 consumer tests, campaign validation, and the
linked issue/PR metadata. Its final content-addressed receipt is recorded in
`attempts/0002/manifest.yaml`. No second scientific audit is opened.
