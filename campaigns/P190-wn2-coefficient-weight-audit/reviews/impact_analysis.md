# P190 Impact Analysis

P190 additively extends `factorial_suppression.py` with one exact enclosure
dataclass and four pure functions, then exposes five package-root names. No
existing public signature, accepted cosine convention, or branching API is
changed. The mass function retains activity, parity, sample space, and
physical ceiling explicitly; allocation is composed through the existing
branching module rather than duplicated.

The refreshed GitNexus index contains 29,112 nodes, 45,121 edges, 395
clusters, and one generic flow. Preimplementation analysis of the existing
`factorial_suppression_evidence` symbol reports no upstream consumer and LOW
risk. Change detection sees three tracked files, five symbols, no affected
process, and low risk. It omits untracked tests and verifiers and misattributes
appended functions to earlier symbols. Those limitations are recorded, so the
graph is not treated as coverage or review. GitNexus-generated Claude files
and boilerplate were removed as unrelated tool side effects.

Repository inspection identifies the new canonical tests and primary verifier
as direct API consumers. The independent route intentionally imports no
scientific API. The focused replay passes 76 tests, and public-import smoke
covers all five names.

The semantic source closure is higher risk than the code graph. WN3 and WN7
repeat WN2's invented admissibility guard, while WN6 carries its universal
verdict. WN4, WN5, and MD1 through MD6 form the remaining closure. All twelve
scripts pass 524 native checks, but only WN2 is adjudicated here; the eleven
consumers stay pending. None has a legacy NumPy quadrature surface, so no
compatibility event changes a scientific verdict.
