# P237 FlatIrrationalTorus v13.0 source audit

This is the frozen source-level disposition for the current model advertised
by the upstream README. It reviews the v13 master engine, Paper 4, the root
analysis pipeline, all files in `scripts/`, the dedicated spectral-gap helper,
and the stored-result verifier. The immutable source and hashes are recorded in
`source-provenance.yaml`; native executions are recorded in
`source-reproduction.yaml`.

## Headline verdict

The upstream `12/12 VERIFIED` tally is reproducible as program output, but it
is not a validation of the advertised physical model. The tally combines exact
arithmetic, comparator-selected formulas, hard-coded numbers, literal status
returns, and broad acceptance ranges. Paper 4 is a three-page summary of the
same formulas rather than the promised derivation of their physical bridges.

The strongest positive result is nevertheless useful: the source identifies a
coherent conditional geometry on the rectangular flat torus with side ratios
`1:sqrt(2):sqrt(3)`. Its reciprocal scalar modes, finite exact eigenspaces,
deck translations, nondegenerate matched-circle criterion and radius, and
convergent positive Epstein partial sums can be separated from all particle
and cosmology claims. Those units are imported in
`src/substrate_framework/flat_torus.py` with exact and mutation-sensitive
tests. No accepted claim is changed.

## Paper 4 equation audit

Paper 4 calls Eqs. (1)-(11) rigorous derivations, but the displayed equations
do not establish the advertised dependency closure.

| Equation | Strongest supported content | Missing or contradicted bridge | Disposition |
| --- | --- | --- | --- |
| (1), `mu=6*pi^5` | The numerical expression can be evaluated and compared with a measured mass ratio. | No action, state construction, mass operator, normalization, or theorem maps the torus to proton and electron masses. The observed ratio is used only to select a close expression. | Not imported. |
| (2), inverse alpha | The numerical expression can be evaluated. | No typed gauge field, kinetic term, charge normalization, renormalization prescription, or derivation from the quotient is supplied. | Not imported. |
| (3), `alpha_eff=0.00112` | A number is printed. | No calculation appears in v13. The older engine chooses a 10 micrometre brane width and an "optimal" node position, so the result is not zero-parameter. | Not imported. |
| (4), `epsilon=sqrt(2)+sqrt(3)-pi` | An exact dimensionless arithmetic expression exists. | Calling it a topological defect or a boundary/volume mismatch supplies no invariant construction; no fermion or inflation equation derives the coefficients later attached to it. | Arithmetic needs no special API; interpretations not imported. |
| (5), `n^2+m^2/2+k^2/3` | Up to the common `(2*pi/L)^2`, this is the periodic scalar `-Delta` spectrum on a rectangular `T3`. | A Dirac operator requires a spin structure and spinor domain. The claimed `T3/Z2` action is nowhere defined. A cutoff-dependent lattice degeneracy does not prove spectral-action protection or a mass map. | Imported as exact scalar flat-torus modes and eigenspaces only. |
| (6)-(9), gauge mapping | Given sector-specific wavelengths, integer `gamma`, phases `delta`, additive `O_Gauge`, and observed couplings, the residual-to-coupling ratios can be computed. | The sector inputs are not derived; the three `K_i` are unequal and the acceptance interval `0.1<K<10` spans two orders of magnitude. Dimensional agreement or `O(1)` proximity is not UV/IR mixing. | Not imported. |
| (10), containment | For a rectangular torus, a last-scattering sphere has no nondegenerate self-intersection when the shortest nonzero deck translation is at least its diameter. | This excludes that matched-circle geometry only. It does not imply statistical isotropy, causal contact, inflation replacement, or invisibility of every topology observable. The observer and `Z2` quotient are unspecified. | Exact conditional geometry imported with strict tangency handling. |
| (11), low-ell cutoff | A dimensionless number `pi*D/Lx` can be formed. | No transfer-function derivation or likelihood is supplied. The analysis wrapper instead uses the longest-side wave number and obtains an extra `1/sqrt(3)`, so the repository contains incompatible cutoff definitions. | Not imported. |

Paper 4 also uses `Lx` for about 115.2 micrometres in its RG discussion and
28.57 Gpc in its CMB discussion. The v13 configuration stores both as
independent literals. No scale transformation with units, dynamics, or
invertible map connects them, so no cross-scale conclusion is imported.

## Master modules 1-12

| Module | Executed object | Audit | Reusable unit and disposition |
| --- | --- | --- | --- |
| 1, constants | Evaluates `6*pi^5` and `20*pi^6/(81*sqrt(3))` against embedded observed values; sets generation count equal to dimension. | Numerical closeness is the selection oracle and no physical operator derives the quantities. The header says 4/4 although only three result rows exist. | No physical unit. Elementary arithmetic is not duplicated. |
| 2, vacuum | Sums `Q(n)^-2` over a fixed cube `[-10,10]^3`. | This is an ordinary absolutely convergent positive Epstein partial sum for exponent 2 in dimension 3, not an analytic continuation or a vacuum-energy calculation. It has no tail report, sign, field content, boundary condition, subtraction, or normalization. | Imported as an explicitly finite partial sum plus refinement increments; all Casimir and dark-energy meanings excluded. |
| 3, gravity | Returns `alpha_eff=0.00112`. | No v13 computation or mutation exists. The historical helper introduces a chosen brane thickness and position. | Not imported. |
| 4, hierarchy | Returns the declared epsilon. | No hierarchy is evaluated. | Not imported. |
| 5, neutrinos | Returns `sum_mnu=0.0589`. | The number is literal; no mass matrix, eigenproblem, ordering test, or topology map exists. | Not imported. |
| 6, inflation | Computes `n_s=1-7.5*epsilon`. | The coefficient 7.5 and inflation dynamics are inputs; the result is compared to the value that motivated it. | Not imported. |
| 7, RG core | Returns `VERIFIED`. | No object is computed. | Not imported. |
| 8, HFGW | Returns `VERIFIED`. | No spectrum is computed. | Not imported. |
| 9, spectral action | Enumerates the rational quadratic form with integer modes, groups float values within `1e-6`, requires maximum finite-cube degeneracy at least 8, and compares two fundamental scalar modes. | The scalar spectrum is correct, but the maximum degeneracy changes with the arbitrary cube cutoff and no Dirac/spinor/spectral-action object is present. | Exact scalar modes and exact finite eigenspaces imported; physical claims excluded. |
| 10, gauge topology | Evaluates the sector inputs described above and accepts each ratio in `(0.1,10)`. | The load-bearing sector shifts and measured couplings are supplied inputs; no common constant or field map is derived. | Not imported. |
| 11, shadows | Prints a force narrative, sets crossover to `Lx/3`, and compares with literal 10000 Mpc under a 15 percent gate. | No force field, source distribution, equation of motion, stability result, or independent observed transition is computed. | Not imported. |
| 12, CMB | Checks `28.20<28.57`, forms `pi*28.20/28.57`, and accepts any result between 2 and 6. | The first check has the narrow matched-circle meaning above. The low-ell formula, isotropy, causal, and inflation claims are absent. | Matched-circle geometry imported only. |

## Spectral-gap helper

`geometry/spectral_gap_calculator.py` labels its grid antiperiodic but iterates
in steps of one half, thereby mixing integer and half-integer sectors. Its
stated all-axis half-twist mode has `Q=11/24`, but its own enumeration includes
`(0,0,+/-1/2)` with `Q=1/12` and returns that as the gap. Correct sectors are:

- periodic scalar modes `n in Z^3`, whose first nonzero value for these sides
  is `Q=1/3` at `(0,0,+/-1)`;
- a declared all-axis half twist `n+(1/2,1/2,1/2)`, whose gap is `Q=11/24`
  with multiplicity eight in the complete nearest-index set.

The imported API represents the twist as one fixed boundary condition and the
focused tests cover both cases. This repairs the algorithm without editing any
upstream scientific claim.

## Analysis package and stored-result verifier

| Surface | Finding | Disposition |
| --- | --- | --- |
| `analysis/class_wrapper.py` | Applies a phenomenological logistic filter with free width `delta_ell=3`; uses `l_cut=2*pi*chi/(sqrt(3)*Lx)`, inconsistent with Paper 4 and module 12; changes only TT rather than solving compact-space perturbations. | Not an IT3 prediction; not imported. |
| `analysis/mcmc_run.py` | Fits seven parameters including `Lx`, contradicting zero-parameter status. `A_s=np.exp(logA-1e10)` underflows to zero; the intended CLASS map would be `exp(logA)/1e10`. | Pipeline invalid; not imported. |
| `analysis/likelihood.py` | Replaces the Planck covariance and likelihood with independent 15-percent fractional errors based on the observed spectrum. | No validated likelihood or reusable framework statistic. |
| `run_all.py` | Stops on undeclared packages and later references two files absent from the repository. | Not a reproducible full pipeline. |
| `verify_results.py` | Loads stored chains for summary checks, but derives delta-chi-square and BIC from embedded reference values rather than the chain likelihoods. | Provenance regression at most; not model validation and not imported. |
| stored reports | Root stored report is an older model version; the advertised v13 report directory appears only after running the master engine. | History/provenance only. |

## Script inventory

| Script | Finding | Disposition |
| --- | --- | --- |
| `circles_minimal.py` | Contains the correct narrow condition `L_min<2*chi` and radius `acos(L/(2*chi))`, but when circles exist it checks only one fixed x-axis pair rather than all deck translations/orientations. | Exact geometry generalized and imported without `healpy`; fixed observational shortcut not imported. |
| `biposh_full.py` | Computes a scalar `Y20` factor from only `b_axis`; `l_axis` is unused. The alleged `A_ll^20` is proportional to summed observed `|a_lm|^2`, then compared with an observational bound. No IT3 sky or theoretical covariance is computed. | Not a BiPoSH model prediction; not imported. |
| `biposh_minimal.py`, `run_all_tests.py` | Duplicate the same observational-map computation and depend on absent maps/mask. | Not imported. |
| `cold_spot_interference.py` | Selects five modes and arbitrary amplitudes `(120,90,70,40,35)`, adds arbitrary Gaussian noise, and reports the coldest pixel despite describing a spot-radius test. The quoted Gaussian tail omits extreme-value/look-elsewhere statistics. | Reciprocal modes imported; mock amplitudes and claimed probability not imported. |
| `b_modes_IT3.py` | Correctly enumerates reciprocal lattice vectors, but the continuum comparator samples one `k_peak` instead of integrating and no cutoff refinement is performed. Native output reports 0.00-percent oscillations. | Reciprocal enumeration imported; B-mode calculation not imported. |
| `hubble_tension_torus.py` | Omits radiation in a high-redshift sound-horizon integral, uses a hard-coded `f_corr=0.965`, contains legacy `np.trapz`, and aborts on an unescaped f-string expression after printing a zero sound horizon. | No correct physical unit to import. |
| `download_data.sh` | The tracked file is a shell command that rewrites itself into a different downloader before execution; its path convention disagrees with several scripts. | Not imported. |

The generic ring-sampling and plotting fragments were not imported because
they add a heavy `healpy` dependency, are not novel relative to standard map
analysis, and do not supply the missing model prediction. The exact geometry
they need is already captured without that dependency.

## Import boundary

The harvest is intentionally positive and complete at the unit level:

1. exact fundamental-cell volume;
2. periodic or fixed-twist reciprocal wavevectors;
3. exact scalar-Laplacian eigenvalues and finite eigenspaces;
4. exact deck-translation vectors, lengths, and complete strict-cutoff
   enumeration;
5. exact nondegenerate matched-circle existence and angular radii, including
   the tangency boundary and sign-pair quotient;
6. explicitly finite, absolutely convergent rectangular Epstein partial sums
   and transparent refinement increments.

Everything else in the current advertised model lacks either a defined
mathematical object, a typed physical bridge, a correct executable oracle, or
a reproducible dependency closure. Those are unit-level terminal non-import
reasons for this source harvest, not edits to the upstream claims and not
claims that all future versions of the ideas are false.
