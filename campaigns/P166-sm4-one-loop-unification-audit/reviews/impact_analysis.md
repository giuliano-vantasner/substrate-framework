# P166 Impact Analysis

P166 changes no canonical module, public symbol, test API, accepted claim, or
release manifest. Its positive result is an audited composition of C-RGE-002,
C-RGE-004, and C-RGE-005, so a new wrapper would add comparator-specific
duplication rather than a reusable invariant.

Direct canonical consumers remain `renormalization.py`, `gauge_beta.py`, their
package-root exports, and their tests. Existing P083, P128, P129, and P130
campaigns retain their immutable accepted evidence. The direct executable
source consumers are qualified WM3, WM4, and WM5 plus pending WM7; all replay
without modification. Pending WM7 gains no physical authority from SM4's
qualification and must still be adjudicated separately.

The only mutable downstream transaction is governance metadata: add SM4's
qualified source disposition, regenerate `migration/source-claims.yaml`,
archive P166 memory, and update the parent effort. `governance/claims.yaml`,
`governance/releases/current.yaml`, canonical docs, and accepted claim/release
memory remain byte unchanged. The risk is therefore metadata-only and bounded
to queue and review consumers.
