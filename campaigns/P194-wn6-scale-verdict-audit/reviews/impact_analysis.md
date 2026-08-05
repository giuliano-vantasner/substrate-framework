# P194 Impact Analysis

P194 adds five pure exact functions to `cosine_vertices.py` and exports them
from the package root. It changes no existing signature, return value, accepted
formula, or test expectation. The scientific threshold does change: WN6's
hard `pi` cutoff is replaced by the explicit sufficient domain
`|x| <= sqrt(12*epsilon)` for a caller-declared relative-to-quadratic error
tolerance.

GitNexus was refreshed at commit `1a58aa0`. Each new function has LOW upstream
risk, zero preexisting indexed callers, and no affected process. The compare
scan from `5c018f6` reports 22 files, 40 symbols, zero affected processes, and
low risk. These zeroes are expected for new leaf APIs and are not treated as an
exhaustive consumer oracle.

Manual inventory retains the package export, 19 focused tests, the 45-check
primary verifier, the 25-check independent raw derivation, and seven direct
source consumers. WN7 and MD1 through MD6 remain pending. They may reuse the
exact remainder and amplitude-convention result, but none inherits a quantum
mode sum, density of states, physical amplitude, rate, material parameter, or
rescue verdict.

