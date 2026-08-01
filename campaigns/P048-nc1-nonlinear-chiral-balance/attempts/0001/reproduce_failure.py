#!/usr/bin/env python3
"""Reproduce P048 attempt 0001's unevaluated-integral comparison failure."""

import sympy as sp

x = sp.symbols("x", real=True)
kink = 4 * sp.atan(sp.exp(x))
reflected = kink.subs(x, -x)
kink_charge = sp.integrate(sp.diff(kink, x) / (2 * sp.pi), (x, -sp.oo, sp.oo))
reflected_charge = sp.integrate(
    sp.diff(reflected, x) / (2 * sp.pi),
    (x, -sp.oo, sp.oo),
)

assert kink_charge == 1 and reflected_charge == -1
