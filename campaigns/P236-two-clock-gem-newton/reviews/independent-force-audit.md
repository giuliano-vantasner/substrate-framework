# P236 independent force audit

Executable: `independent_force_audit.py`. Data:
`../evidence/m5_96_independent_audit.json`.

The audit imports no production driver function. It consumes only the seven
relaxed rapidities in the primary record, reconstructs the M5 matrix from the
public engine, and uses a different geometry and numerical method:

- uniform cylindrical lattice, `D=120`, `h=0.75`;
- direct `d/drho`, `(1/rho)d/dphi`, and `d/dz` derivatives;
- exact cylindrical measure `2*pi*rho drho dz`;
- independent common-mask local subtraction;
- independent raw-force and model fits.

## REFUTE doors

| Door | Refutation criterion | Result |
| --- | --- | --- |
| A attraction | any direct force sample nonnegative | all six are negative |
| B exponent | `|p+2|>=0.1` | `p=-2.0203675` |
| C magnitude | `|C_audit-C_primary|/|C_primary|>=6%` | 4.50% |
| D exponent agreement | primary/audit difference >=0.08 | 0.03982 |
| E model selection | `1/d` fails to beat alternatives by 10x | 520x vs log, 1018x vs linear |

The independent coefficient is `-118.3291126` versus primary
`-123.9048063`. The result is not refuted.
