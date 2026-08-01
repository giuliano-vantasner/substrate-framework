#!/usr/bin/env python3
"""Reproduce P049 attempt 0001's raw-expression equality failure."""

import sympy as sp

t, x = sp.symbols("t x", real=True)
phi = sp.Function("phi")(t, x)
expanded = (
    sp.diff(phi, t) ** 2 / 4
    + sp.diff(phi, t) * sp.diff(phi, x) / 2
    + sp.diff(phi, x) ** 2 / 4
)
factored = (sp.diff(phi, t) + sp.diff(phi, x)) ** 2 / 4

assert expanded == factored
