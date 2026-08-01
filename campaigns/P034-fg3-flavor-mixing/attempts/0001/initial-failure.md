# P034 Attempt 0001 Initial Failures

The initial verifier run reached thirty-two successful checks and then failed
the inserted-texture provenance probe because the source token is uppercase
`ABSOLUTE`, not lowercase `absolute`. The initial independent run reached
seven successful checks and then failed because SymPy did not select a stable
symbolic SVD basis for a continuously parameterized exact matrix.

Both failures belong to verifier implementation. The provenance predicate now
matches the hash-pinned text exactly. The independent arbitrary-angle oracle
now multiplies the constructed rotation and matrix directly, avoiding any
symbolic eigensolver basis choice. The final unchanged predicates pass; no
scientific criterion, tolerance, candidate, or claim scope was relaxed.
