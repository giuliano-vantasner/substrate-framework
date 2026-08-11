---
title: "Build-chain smoke document"
author: "docs pipeline (issue #33)"
date: "2026-08-11"
---

# Purpose

This document exists only to prove the MD -> LaTeX -> PDF chain end to end:
YAML metadata, section headings, inline math $e^{i\pi} + 1 = 0$, display math
with explicit tags, footnotes,[^note] and a table.

[^note]: A pandoc footnote, rendered by LaTeX.

# Math

$$\Gamma^{\sigma}{}_{\rho\nu} = \frac{1}{2}\, g^{\sigma\lambda}\left( \partial_{\rho} g_{\lambda\nu} + \partial_{\nu} g_{\lambda\rho} - \partial_{\lambda} g_{\rho\nu} \right). \tag{1}$$

# Table

| Chain step | Tool |
| --- | --- |
| MD -> LaTeX | pandoc |
| LaTeX -> PDF | xelatex |
