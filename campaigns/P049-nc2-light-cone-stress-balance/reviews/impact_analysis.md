# P049 Consumer Impact Analysis

The refreshed GitNexus index classifies the canonical sine-Gordon module as low
risk: direct import consumers are `u1_charge.py` and the package export surface,
with quartic-Q-ball and fluctuation modules at depths two and three and no
affected execution flows. The existing `hamiltonian_density` symbol has no
indexed upstream code caller; repository text search identifies only P001 and
the new P049 verifier and test.

P049 replaces only the duplicated potential expression inside
`hamiltonian_density` with the exact new `sine_gordon_potential` helper; the
mathematical expression is unchanged. Targeted replay therefore covers the
sine-Gordon, U1, quartic-Q-ball, exact-sine, and fluctuation tests plus P001 and
P048.

Post-change detection reports nominal high risk because insertion of the new
APIs before the older breather functions shifts their indexed line ranges and
causes GitNexus to label thirteen unchanged downstream definitions and process
steps as touched. Direct source diff confirms that none of those older
function bodies changed. The actual executable delta is the new stress API,
the package exports, exact tests, and the equivalent potential-helper call in
`hamiltonian_density`; the targeted 81-test and P001/P048 replays pass. The
single full workflow gate remains the final global consumer check.
