# Evidence Attachment Review Template

Use this lightweight record only when a claim transaction adds or changes
evidence attachments. It classifies evidence; it does not reopen claim
acceptance or require every attachment to prove the parent claim.

Group related theorem entrypoints or artifacts when they establish the same
proposition. Begin every section with a plain-prose sentence.

```md
---
description: Evidence-role review for <claim-id or transaction>
author: <reviewer-id>
created: '<ISO-8601>'
updated: '<ISO-8601>'
tags:
- substrate-framework
- evidence-review
category: decisions
confidence: working
status: active
---

## Frozen Attachment Boundary
Record the base/head or tree hash, parent claim IDs, and only the new or changed
attachment groups. Unchanged claims, accepted dependencies, and neighboring
corpus records are outside this review.

## Attachment Roles
State the exact proposition each group establishes and its honest role.

| Attachment group | Entrypoints | Exact proposition | Role: exact proof / corroborating subclaim / regression / applicability / provenance | Typed or logical bridge | Verdict |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | keep / relabel / correct / remove |

`Keep` means the recorded role is accurate. `Relabel` or `correct` is preferred
when useful evidence remains. `Remove` is reserved for an attachment that is
factually wrong, unrelated even as provenance, or misleading after relabeling.

## Blocking Corrections
List only attachments whose current role would materially overstate the parent
claim or corrupt accepted dependency closure. Give the minimum correction and
one check. Missing full-parent coverage is not a blocker when the narrower role
is explicit.

## Follow-Up
Record adjacent observations once without expanding this transaction. Use
`None` when empty.

## Correction Check
Check only requested attachment-role or bridge corrections. Do not rerun the
parent oracle, recount unrelated theorems, or begin a second substantive review.
```
