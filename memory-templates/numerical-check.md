# Numerical Check Template

Instantiate whenever a numerical check produces evidence that a claim or attempt will
cite, and always when the checked quantity is smaller than 1e-3 relative to the
computation's dominant scale. Store the filled record in memory under `efforts` (or
link it from the attempt's result file) before the citing claim is promoted. Run
`memory validate --base "$PWD" "$PWD/memory/<path>.md"` on the instantiated record;
a template that does not validate is not a record.

Begin every section with a plain-prose sentence. Inline code, a table, or a list
does not satisfy the memory index's first-content disclosure contract.

```md
---
description: <what question this check answers and its verdict in one line>
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

## Question and Checked Quantity

State what was computed, at what value relative to the dominant scale, and why that small ratio needs this record.

## Evaluator and Certification

Name the evaluator function, its certification status, and any transforms applied to it for this check.

## Execution Context

Record thread pins, library versions, invocation path used (.py direct, importlib, harness), and the measured runner-noise floor with how it was measured (which two settings disagreed by how much).

## Acceptance Tolerances and Rationale

State each acceptance tolerance and tie it explicitly above the noise floor and the conditioning of the operation; a tolerance below the floor invalidates the check.

## Cross-Validation Performed

Describe the independent axis used (doubled quadrature, second extraction method, independent discretization) and the observed agreement value.

## Monitors and Residuals

Report conservation or identity residuals and whether they close at the claimed accuracy.

## Verdict and Artifacts

State pass, fail, or gate-invalid with the failing mechanism named when applicable, and list artifact paths.
```
