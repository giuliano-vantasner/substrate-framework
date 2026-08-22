# Numerical Check Template

Instantiate whenever a numerical check produces evidence worth remembering — a
technique that worked, a failure mode worth naming, a number another attempt will
cite. It is a lab notebook page, not a compliance form: keep the sections that
earn their place and drop the rest; the only fixed contract is the frontmatter
and the prose-first rule. Store the filled record in memory under `efforts` (or
link it from the attempt's result file).

Begin every section with a plain-prose sentence. Inline code, a table, or a list
does not satisfy the memory index's first-content disclosure contract.

```md
---
description: <what question this check answers and what it found, in one line>
author: <agent-id>
created: '<ISO-8601>'
updated: '<ISO-8601>'
tags:
- substrate-framework
- numerical-check
category: efforts
confidence: working
status: active
---

## Question

What was being computed, and why it was delicate — usually because the quantity of interest is orders of magnitude below the dominant scale.

## Method

How it was computed: the formulation chosen (and rejected alternatives when the choice is instructive), the evaluator used, and the execution context worth knowing later (thread pins, invocation path, versions) if results sit near the 1e-13-relative level where runner settings matter.

## What Was Seen

The numbers and behaviour actually observed — including how values moved under changes of mesh, domain, quadrature, or method, since that movement is often the most informative part.

## Reading

What the observations mean in small-ratio terms: which cross-checks agree, whether the soft direction is bulk or boundary, what remains hypothesis versus established. Name failure modes plainly when they occurred; a named mechanism is the reusable part.

## Artifacts

Paths to scripts, data files, and logs.
```
