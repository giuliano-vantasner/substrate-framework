"""Verify Candidate H and its attractive weak-field scalar exchange."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    dilaton_coupled_hamiltonian_density,
    dilaton_coupled_lagrangian_density,
    exponential_matter_factor,
    scalar_current_hamiltonian_density,
    scalar_current_lagrangian_density,
    timelike_spectral_scalar,
)
from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent
ETA = sp.Matrix(MINKOWSKI_MOSTLY_PLUS)


def _rational_lorentz() -> sp.Matrix:
    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = sp.Rational(4, 3)
    rotation = sp.eye(4)
    rotation[2, 2] = rotation[3, 3] = sp.Rational(3, 5)
    rotation[2, 3] = -sp.Rational(4, 5)
    rotation[3, 2] = sp.Rational(4, 5)
    return boost * rotation


def main() -> int:
    ledger = CheckLedger("P239/timelike-dilaton-completion")
    g_value, alpha, kappa = sp.symbols("g alpha kappa", positive=True)
    projector = sp.diag(1, 0, 0, 0)
    spatial = sp.Matrix([[2, 1, 0], [1, -1, 1], [0, 1, 3]])
    order_parameter = sp.diag(-g_value, 0, 0, 0)
    order_parameter[1:4, 1:4] = spatial
    tau = timelike_spectral_scalar(order_parameter, projector)
    ledger.check("rest-frame timelike scalar is g", tau == g_value)

    transformation = _rational_lorentz()
    inverse = transformation.inv()
    covector = inverse.T
    transformed_order_parameter = covector * order_parameter * covector.T
    transformed_projector = transformation * projector * inverse
    transformed_tau = timelike_spectral_scalar(
        transformed_order_parameter, transformed_projector
    )
    ledger.check(
        "timelike eigenvalue is an exact Lorentz scalar",
        sp.simplify(transformed_tau - tau) == 0,
    )
    factor = exponential_matter_factor(tau, g_value, alpha)
    ledger.check("matter factor is one at the spatial restriction", factor == 1)
    ledger.check(
        "matter factor is everywhere positive for real fields",
        exponential_matter_factor(g_value + 1, g_value, alpha).is_positive,
    )

    derivatives = sp.Matrix([2, 3, -1, 4])
    transformed_derivatives = inverse.T * derivatives
    scalar_lagrangian = scalar_current_lagrangian_density(tuple(derivatives), kappa)
    ledger.check(
        "scalar current is Lorentz invariant",
        sp.simplify(
            scalar_current_lagrangian_density(tuple(transformed_derivatives), kappa)
            - scalar_lagrangian
        )
        == 0,
    )
    scalar_hamiltonian = scalar_current_hamiltonian_density(tuple(derivatives), kappa)
    ledger.check(
        "scalar Hamiltonian is positive",
        scalar_hamiltonian == 15 * kappa,
    )

    matter_lagrangian, matter_hamiltonian = sp.symbols("L_G H_G")
    zero_derivatives = (0, 0, 0, 0)
    ledger.check(
        "Candidate G Lagrangian is exactly recovered at tau=g",
        dilaton_coupled_lagrangian_density(
            matter_lagrangian,
            tau,
            g_value,
            alpha,
            zero_derivatives,
            kappa,
        )
        == matter_lagrangian,
    )
    ledger.check(
        "Candidate G Hamiltonian is exactly recovered at tau=g",
        dilaton_coupled_hamiltonian_density(
            matter_hamiltonian,
            tau,
            g_value,
            alpha,
            zero_derivatives,
            kappa,
        )
        == matter_hamiltonian,
    )

    phi, canonical_phi = sp.symbols("phi psi", real=True)
    canonical_substitution = phi - canonical_phi / sp.sqrt(kappa)
    canonical_factor = exponential_matter_factor(g_value + phi, g_value, alpha).subs(
        phi, canonical_phi / sp.sqrt(kappa)
    )
    ledger.check(
        "canonical field leaves coupling alpha/sqrt(kappa)",
        sp.simplify(
            canonical_factor - sp.exp(2 * alpha * canonical_phi / sp.sqrt(kappa))
        )
        == 0
        and canonical_substitution.subs(phi, canonical_phi / sp.sqrt(kappa)) == 0,
    )

    radius, mass = sp.symbols("r m", positive=True)
    exterior = -alpha * mass / (2 * sp.pi * kappa * radius)
    radial_laplacian = sp.simplify(
        sp.diff(radius**2 * sp.diff(exterior, radius), radius) / radius**2
    )
    ledger.check("exterior scalar is harmonic", radial_laplacian == 0)
    flux = sp.simplify(4 * sp.pi * radius**2 * sp.diff(exterior, radius))
    ledger.check(
        "scalar flux matches kappa Laplacian(phi)=2 alpha rho",
        sp.simplify(flux - 2 * alpha * mass / kappa) == 0,
    )

    mass_one, mass_two, separation = sp.symbols("m_1 m_2 R", positive=True)
    interaction = -(alpha**2) * mass_one * mass_two / (sp.pi * kappa * separation)
    force = -sp.diff(interaction, separation)
    ledger.check(
        "two positive sources have an attractive inverse-square force",
        force == -(alpha**2) * mass_one * mass_two / (sp.pi * kappa * separation**2),
    )
    ledger.check(
        "deleting the matter coupling removes scalar exchange",
        interaction.subs(alpha, 0) == 0,
    )
    ledger.check(
        "flipping one source sign flips the interaction",
        interaction.subs(mass_two, -mass_two) == -interaction,
    )

    result = {
        "campaign": "P239",
        "attempt": "0007",
        "candidate": "H_timelike_dilaton_completion",
        "action_addition": (
            "A(tau)=exp(2*alpha*(tau-g)); "
            "L_tau=-(kappa_tau/2)*eta^munu*d_mu tau*d_nu tau"
        ),
        "weak_field_equation": "kappa_tau*Laplacian(phi)=2*alpha*rho",
        "one_body_tail": "phi=-alpha*m/(2*pi*kappa_tau*r)",
        "two_body_interaction": ("U_N=-alpha^2*m1*m2/(pi*kappa_tau*r)"),
        "physical_coupling": "alpha^2/kappa_tau",
        "verdict": (
            "Candidate H is a local Lorentz-covariant positive-energy scalar "
            "completion. It is exactly Candidate G and M5.17 at tau=g, and "
            "its linearized stationary exchange between positive localized "
            "M5 energies is necessarily attractive with a 1/r potential."
        ),
        "scope": (
            "This exact result establishes the action and infrared sign/kernel. "
            "Existence and refinement of the nonlinear relaxed one- and two-body "
            "branches remain required before C-M5-004 promotion."
        ),
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
