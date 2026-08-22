---
description: Classified review of P242 campaign workflow errors with corrective takeaways folded into AGENTS.md, campaign-proposal template, and physics-erdos-loop skill
author: ox-alpha
created: '2026-08-22T00:00:00+02:00'
updated: '2026-08-22T00:00:00+02:00'
tags:
- substrate-framework
- self-improvement
- process-review
- p242
category: decisions
confidence: working
status: active
---

## Decision

P242's delivery is sound (58 verifier checks exit 0, two-route agreements at
1e-8), but its execution log shows three recurring defect classes. This
record classifies them and fixes the corrective language in three surfaces:
the agent contract (AGENTS.md, Implementation architecture), the campaign
proposal template (Implementation and Oracle Plan), and the
physics-erdos-loop skill (Phase 3 and Phase 4). No new gates are introduced;
these are authoring practices, and each consolidates an existing failure
mode observed repeatedly within one campaign.

## Class A - stale-anchor edits (about 12 incidents, dominant rework cost)

Anchored edits were issued from remembered line numbers instead of fresh
reads; multi-hunk edit calls composed ranges from earlier snapshots. Files
edited repeatedly under time pressure corrupted repeatedly
(nonaffine_networks.py four times; five verifier scripts; package exports).
Recovery full-file rewrites sometimes introduced fresh bugs (a fractional-
versus-lattice-units error entered during one such rewrite). Takeaway:
re-read the target region immediately before every anchored edit; after a
few patch rounds on one file, prefer one full rewrite from a full read over
continued patching; never compose multi-hunk edits from stale reads.

## Class B - in-head derivation errors (about 10 incidents)

Unit and factor bugs authored directly in code: sub-filter oscillator
missing the k^2 factor; bond vectors double-counting periodic wrap and
mixing fractional/lattice units; affine modulus using non-unit direction
components (factor 3); finite-difference affine modulus evaluated below
the float64 noise floor; test expectations computed mentally and wrong
(a divergence-free field used as the divergent mutation, twice; eigenvalue
multiplicities read as values; sigma_yy forgetting the lambda tr eps term;
Poly(1,x).degree() == -oo unguarded; float division breaking exactness).
Takeaway: write units, signs, and geometric factors as a comment block
before implementing; compute test expectations independently of the code
under test. Several incidents were preventable by consulting the installed
small-ratio-numerics skill (second-variation operator instead of conjugate
gradient on a stiff-plus-soft landscape; non-dimensionalize before
optimizing) - consult skills for the numerical regime before choosing a
method, not after debugging it.

## Class C - process sequencing (4 incidents)

Verifier stdout was captured into attempts/ only after all runs finished,
forcing a complete rerun of eight verifiers to materialize append-only
records. Todo tool payloads were submitted three times in malformed shape.
Drafting residue (placeholder stubs, dead del statements, a pytest_approx
helper) survived into late stages and was caught only by review. Export
wiring referenced a function removed earlier the same session. Takeaway:
tee verifier output into attempts/000N on first execution; validate tool
payloads against documented schemas; grep new files for placeholder markers
before staging; run the export/import check after wiring new modules.

## Corrective language landed

- AGENTS.md, Implementation architecture: authoring-discipline bullet
  (content-anchored and AST-aware editing, derive-before-code comment
  blocks, first-run attempt capture, skill-first numerics).
- memory-templates/campaign-proposal.md, Implementation and Oracle Plan:
  numerical-scheme skill consultation, first-run attempt capture,
  scipy cross-validation when symbolic checks misbehave, content-anchored
  patching with full-rewrite fallback.
- .agents/skills/physics-erdos-loop/SKILL.md: Phase 3 Do-not entries for
  remembered-line-number patching and for skill-first numerics; Phase 4
  first-run capture sentence.

## Addendum - edit-tool hardening (owner-directed)

Class A's root cause is stale line-number anchoring. Hardening language
landed alongside the takeaways above: never patch from remembered line
numbers; re-anchor by content search (ripgrep) at the edit site; prefer
AST-aware rewrites (ast-grep / ast_edit) for nested or multi-site changes;
use unique-pattern substitution for single-line swaps; reserve line-range
patches for regions read in the immediately preceding step; switch to one
full rewrite from a full read after repeated failed patch rounds. This
language appears in AGENTS.md Implementation architecture, the campaign
proposal template, and physics-erdos-loop Phase 3.
