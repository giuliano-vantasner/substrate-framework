#!/usr/bin/env python3
"""Independent scaling derivation for proposed C-RG-001.

This review intentionally does not import ``substrate_framework.radial_energy``.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.sine_gordon import breather_energy
from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("C-RG-001-INDEPENDENT")
    radius, scale = sp.symbols("R a", positive=True)
    line_density, shell_density = sp.symbols("lambda sigma", positive=True)
    tension, pressure = sp.symbols("T P", positive=True)
    core = sp.symbols("C", real=True)

    independently_constructed_line = line_density * (2 * sp.pi * radius)
    independently_constructed_shell = shell_density * (4 * sp.pi * radius**2)
    checks.check(
        "direct transverse-measure ratios give scaling powers one and two",
        sp.simplify(
            independently_constructed_line.subs(radius, scale * radius)
            / independently_constructed_line
        )
        == scale
        and sp.simplify(
            independently_constructed_shell.subs(radius, scale * radius)
            / independently_constructed_shell
        )
        == scale**2,
    )
    checks.check(
        "independent logarithmic derivatives recover degrees one and two",
        sp.simplify(
            radius
            * sp.diff(independently_constructed_line, radius)
            / independently_constructed_line
        )
        == 1
        and sp.simplify(
            radius
            * sp.diff(independently_constructed_shell, radius)
            / independently_constructed_shell
        )
        == 2,
    )
    checks.check(
        "independent second derivatives separate line from shell",
        sp.diff(independently_constructed_line, radius, 2) == 0
        and sp.diff(independently_constructed_shell, radius, 2)
        == 8 * sp.pi * shell_density,
    )

    capillary = 2 * sp.pi * radius * tension - sp.pi * radius**2 * pressure + core
    critical = tension / pressure
    peak = core + sp.pi * tension**2 / pressure
    checks.check(
        "completion of the square independently gives the capillary barrier",
        sp.simplify(
            capillary
            - (
                peak
                - sp.pi * pressure * (radius - critical) ** 2
            )
        )
        == 0,
    )
    checks.check(
        "the capillary line component alone cannot inherit the barrier radius",
        sp.diff(2 * sp.pi * radius * tension, radius) == 2 * sp.pi * tension
        and sp.solve(
            sp.Eq(sp.diff(2 * sp.pi * radius * tension, radius), 0),
            radius,
        )
        == [],
    )

    omega = sp.symbols("omega", positive=True)
    accepted_breather_density = breather_energy(omega)
    pulson_line = 2 * sp.pi * radius * tension
    breather_line = 2 * sp.pi * radius * accepted_breather_density
    checks.check(
        "direct subtraction retains the program-specific coefficient difference",
        sp.factor(pulson_line - breather_line)
        == 2 * sp.pi * radius * (
            tension - 16 * sp.sqrt(1 - omega**2)
        ),
    )
    checks.check(
        "solving the equality independently requires coefficient equality",
        sp.solve(sp.Eq(pulson_line, breather_line), tension)
        == [accepted_breather_density],
    )
    checks.check(
        "a shell substitution fails both independent line diagnostics",
        sp.simplify(
            independently_constructed_shell.subs(radius, scale * radius)
            / independently_constructed_shell
        )
        != scale
        and sp.diff(independently_constructed_shell, radius, 2) != 0,
    )

    total = checks.finish()
    print(f"P006 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
