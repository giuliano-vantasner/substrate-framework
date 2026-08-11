## Objective and issue

Describe the positive deliverable and the smallest coherent merge boundary.

Canonical issue: <!-- Required. The issue must exist before even a draft PR is submitted. -->

Issue relationship: <!-- Use `Advances #N` while work remains; use `Fixes #N` only when the full goal is complete. -->

Authoring agent:

Intended independent merger: <!-- Must be a distinct agent or repository owner. -->

- [ ] The canonical issue existed before this PR was submitted.
- [ ] I will not merge this PR because I opened it, authored a commit, or materially implemented it.

## Change classification

- [ ] Reusable implementation or tooling
- [ ] Documentation or workflow
- [ ] Scientific proposal or campaign evidence
- [ ] Claim promotion transaction
- [ ] Harvest from an incomplete research PR
- [ ] Compatibility-only repair

## Authority and scope

Base release and commit:

Accepted claims and canonical sources used:

Declared imports, assumptions, and conventions:

Files or concerns intentionally out of scope:

New or materially changed public interfaces:

| Symbol or module | Authority status | Accepted claim IDs | Owning issue/PR | Conditional boundary |
| --- | --- | --- | --- | --- |
|  | accepted claim / conditional unpromoted / non-scientific utility | none or exact IDs |  |  |

An exported symbol is not accepted scientific authority by itself. For every
conditional unpromoted API, state its explicit inputs, assumptions, exclusions,
and why it is still independently reusable.

## Unit-level disposition

List the smallest coherent units. A mergeable unit must remain useful and true
without relying on an unearned headline claim.

| Unit | Local claim or purpose | Dependencies | Evidence and tests | Proposed disposition |
| --- | --- | --- | --- | --- |
|  |  |  |  | merge / refactor / history only |

Answer each decision independently:

- Artifact merge: <!-- yes/no and why -->
- Claim promotion: <!-- none, or exact claim IDs -->
- Goal completion: <!-- yes/no and the remaining gate -->

## Verification and sensitivity

List exact commands and results. Include the claim-appropriate oracle,
mutations or counterexamples, numeric refinement and independent route when
applicable, and affected consumer replay. A pass tally by itself is not enough.

```text
# command
# exit status and meaningful verdict
```

## GitNexus impact

Record index freshness, pre-change symbol/API impact when applicable, and final
diff change detection. For documentation-only work, state that no graph-mapped
symbol or process was expected or found.

## Memory, governance, and generated state

Durable contract or decision entry:

Proposal/campaign/claim/release changes:

Generated outputs and synchronization commands:

Debt remaining inside the proposed merge unit: <!-- must be empty for acceptance -->

Campaign frontier outside this merge unit:

## Validation boundary

Mark a nonapplicable scientific row `N/A` and explain why in the verification
section; do not claim it passed.

- [ ] Targeted tests and named scientific verifiers pass.
- [ ] Load-bearing mutations, counterexamples, or wrong-convention probes fail as expected.
- [ ] Affected downstream consumers replay.
- [ ] `scripts/validate.sh --pytest-scope ...` passes with the exact selectors recorded, or the full-suite trigger is explained and `scripts/validate.sh --full` passes.
- [ ] The pytest scope remains valid against the merge base; an equivalent unchanged validation is not duplicated.
- [ ] `git diff --check` passes in a separate invocation.
- [ ] No unrelated, generated-by-hand, or host-specific artifacts are included.

## Author handoff

State what the reviewer should independently reproduce, the riskiest assumption,
and the next decisive action if this PR advances rather than completes the goal.

---

## Reviewer disposition

Review the actual head commit and complete this section or provide the same
fields in a formal review.

- Canonical issue predates PR: <!-- yes/no -->
- Authoring or implementing agent:
- Distinct merger:

- Artifact merge: <!-- yes/no with unit-level rationale -->
- Claim promotion: <!-- none or exact claim IDs and review evidence -->
- Goal completion: <!-- yes/no and still-open gate -->
- Merge as written: <!-- yes/no -->
- Refactor or harvest: <!-- exact units and required changes -->
- Leave in PR history: <!-- exact units and rationale -->
- Next decisive action: <!-- one concrete step -->
- Head branch disposition: <!-- auto-delete after merge; preserve if closed-unmerged/failed; name any explicit owner exception -->

### Reviewer checks

- [ ] Base release, issue, accepted boundary, diff, memory, and discussion inspected.
- [ ] The canonical issue existed before the PR was submitted.
- [ ] The designated merger did not open, author a commit for, or materially implement the PR.
- [ ] Load-bearing result independently rederived or reproduced.
- [ ] Dependencies, conventions, imports, consumers, and GitNexus impact audited.
- [ ] Every new public symbol has an explicit authority status and owning issue.
- [ ] Verification sensitivity and applicable numerical/formal limits audited.
- [ ] Merge, claim-promotion, and goal-completion decisions kept independent.
- [ ] Canonical issue handoff is posted or preserved ready to post.
- [ ] The exact same-repository head will be deleted after merge; open or closed-unmerged/failed heads are preserved unless an owner explicitly retires them.
