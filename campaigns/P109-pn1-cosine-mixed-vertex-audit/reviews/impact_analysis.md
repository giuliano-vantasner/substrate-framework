# P109 canonical API impact analysis

Pre-edit GitNexus analysis assigned LOW upstream risk and zero affected
execution flows to the accepted sine-Gordon potential and breaking-potential
surfaces. P109 therefore adds a separate pure `cosine_vertices.py` module and
package exports rather than changing either existing implementation.

The canonical API is symbolic and side-effect free. It adds no simulation,
quadrature, solver, mutable global, print path, or import-time execution. Direct
consumers are the focused tests and P109 verifiers. Pinned source consumers are
recorded separately because their scientific claims remain pending and are not
runtime package dependencies.

The final index-only refresh produced 15,825 nodes, 24,880 edges, 264 clusters,
and 45 execution flows without injecting agent files. Upstream analysis of
`cosine_mixed_coefficient` finds three direct internal helper callers, four
total impacts through depth two, LOW risk, and zero affected processes. The
Taylor-polynomial entry point has no upstream caller outside test/campaign
edges and is also LOW risk with zero affected processes.

Final all-change detection maps seven graph-visible files to four symbols,
reports zero affected execution processes, and assigns overall low risk. The
graph count omits YAML and the generated queue but the workflow validates
those separately. The change is additive: no accepted signature, convention,
numerical method, or execution flow is modified.
