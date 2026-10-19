"""Exact unit derivation and mixed-mass exposing fixtures; execution owned by root."""

import numpy as np
import sympy as sp

from substrate_framework import material_modes as modes


def unit_block(ledger):
    hbar, eh, me, a0, u = sp.symbols("hbar E_H m_e a_0 u", positive=True)
    qe_angular_squared = (2 * me / u) * (eh / (2 * hbar))**2
    si_angular_squared = eh / (2 * a0**2 * u)
    derived = sp.cancel(qe_angular_squared.subs(hbar**2, me * eh * a0**2))
    ledger.check("exact Ry mass/time conversion equals SI force/mass", derived == si_angular_squared)
    ledger.mutation_sensitive("exact Ry-Ha/amu/2pi factors", lambda x: sp.cancel(x - si_angular_squared) == 0,
                              derived, [2 * derived, derived / 2, 2 * sp.pi * derived,
                                        derived / (2 * sp.pi)**2, derived * u / me])
    physical = modes.RYDBERG_SI / modes.BOHR_RADIUS_SI**2 / modes.AMU_SI
    qe = (1 / modes.AMU_RY) * (2 * np.pi * 1e12 * modes.RY_TO_THZ)**2
    discrepancy = abs(qe / physical - 1)
    # Half-last-place uncertainty of the decimal source constants; h is exact SI.
    rounding_bound = (0.5e-41 / modes.ELECTRONMASS_SI
                      + 0.5e-31 / modes.HARTREE_SI
                      + 2 * 0.5e-22 / modes.BOHR_RADIUS_SI)
    rounding_bound += 32 * np.finfo(float).eps
    ledger.check("independent SI and QE routes agree within sourced decimal rounding", discrepancy <= rounding_bound)
    ledger.check("rounding bound exposes factor two", abs(2 * qe / physical - 1) > rounding_bound)
    return {"qe_omega_squared_per_force_per_amu": str(qe_angular_squared),
            "identity_used": "hbar^2 = m_e E_H a_0^2 (atomic-unit defining relation)",
            "si_omega_squared_per_force_per_amu": str(si_angular_squared),
            "relative_squared_frequency_route_discrepancy": discrepancy,
            "decimal_rounding_bound": rounding_bound,
            "rounding_scope": "Agreement of rounded QE NIST2018 constants, not a material error bar."}


def mixed_mass_block(ledger):
    masses = np.array([4., 9.])
    spring = np.array([[7., 2., -1.], [2., 5., 3.], [-1., 3., 11.]])
    force = np.block([[spring, -spring], [-spring, spring]]).reshape(2, 3, 2, 3)
    before = force.copy()
    operator = modes.mass_weighted_operator(force, masses, units="si")
    factor = modes.RYDBERG_SI / modes.BOHR_RADIUS_SI**2 / modes.AMU_SI
    entrywise = np.empty((6, 6))
    for i in range(2):
        for a in range(3):
            for j in range(2):
                for b in range(3):
                    entrywise[3*i+a, 3*j+b] = force[i,a,j,b] * factor / np.sqrt(masses[i]*masses[j])
    tolerance = 64 * np.finfo(float).eps * np.linalg.norm(entrywise)
    ledger.check("mixed mass tensor orientation and SI conversion", np.linalg.norm(operator-entrywise) <= tolerance)
    ledger.check("raw tensor not changed", np.array_equal(force, before))
    root = np.repeat(np.sqrt(masses), 3)
    wrong_product = force.reshape(6, 6) * factor / (root[:,None] * root[None,:])**2
    ledger.check("missing square root mutation exposed", np.linalg.norm(wrong_product-entrywise) > tolerance)
    wrong_uniform = modes.mass_weighted_operator(force, [4.,4.], units="si")
    ledger.check("uniform mass substitution exposed", np.linalg.norm(wrong_uniform-entrywise) > tolerance)
    translations = modes.translation_basis(masses)
    ledger.check("normalized translations orthonormal", np.linalg.norm(translations.T @ translations-np.eye(3)) < 32*np.finfo(float).eps)
    ledger.check("correct weighted translations annihilated", np.linalg.norm(operator @ translations) <= tolerance)
    uniform = np.vstack([np.eye(3),np.eye(3)]) / np.sqrt(2)
    ledger.check("uniform translation mutation exposed for mixed masses", np.linalg.norm(operator @ uniform) > tolerance)
    asymmetric = operator.copy()
    asymmetric[0,4] += (1+2j) * factor
    diagnostics = modes.operator_residuals(asymmetric, masses)
    ledger.check("raw anti-Hermitian residual retained", diagnostics["hermitian_frobenius"] > tolerance)
    hermitian = modes.project_hermitian(asymmetric)
    ledger.check("explicit Hermitian projection", np.array_equal(hermitian,hermitian.conj().T))
    projected = modes.project_gamma_translations(hermitian,masses,q_fractional=[0,0,0])
    ledger.check("explicit acoustic projection annihilates weighted translations", np.linalg.norm(projected @ translations) <= tolerance)
    try:
        modes.project_gamma_translations(hermitian,masses,q_fractional=[0.5,0,0])
    except ValueError:
        rejected = True
    else:
        rejected = False
    ledger.check("non-Gamma acoustic repair rejected", rejected)
    unstable = np.diag([-4.,9.,16.]).astype(complex)
    spectrum = modes.signed_modes(unstable,units="qe_ry")
    expected = np.array([-2.,3.,4.]) * modes.RY_TO_THZ
    ledger.check("signed native spectrum retains instability", np.array_equal(spectrum.frequency_thz,expected))
    ledger.check("instability-clipping mutation exposed", not np.array_equal(np.maximum(spectrum.frequency_thz,0),expected))
    ledger.check("ordinary/angular frequency mutation exposed", np.linalg.norm(expected*2*np.pi-spectrum.frequency_thz) > 1)
    return {"masses_amu": masses.tolist(), "spring_ry_per_bohr2": spring.tolist(),
            "raw_asymmetric_operator_residuals_si": diagnostics,
            "scope": "Synthetic mixed-mass harmonic convention fixture, not Ni parameters or stability evidence."}
