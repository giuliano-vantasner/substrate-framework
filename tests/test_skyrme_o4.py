import pytest
import sympy as sp

import substrate_framework as sf
from substrate_framework.radial_modes import derrick_scaling_evidence
from substrate_framework.skyrme_o4 import o4_skyrme_pointwise_evidence


def _generic_inputs():
    entries = sp.symbols("g0:12", real=True)
    tangent = sp.symbols("w0:4", real=True)
    return [entries[0:4], entries[4:8], entries[8:12]], tangent


def test_public_api_exports_pointwise_evidence():
    assert sf.o4_skyrme_pointwise_evidence is o4_skyrme_pointwise_evidence
    assert sf.O4SkyrmePointwiseEvidence.__module__.endswith("skyrme_o4")


def test_generic_quartic_and_mass_identities_have_exact_square_certificates():
    gradients, tangent = _generic_inputs()
    evidence = o4_skyrme_pointwise_evidence(gradients, tangent)

    assert evidence.strain == evidence.gradients * evidence.gradients.T
    assert evidence.static_density == sp.expand(
        evidence.quadratic_density + evidence.quartic_minor_sos
    )
    assert evidence.mass_operator == evidence.mass_operator.T
    assert evidence.quartic_identity_residual == 0
    assert evidence.mass_identity_residual == 0
    assert evidence.quartic_has_sos_certificate
    assert evidence.mass_has_sharp_lower_bound_certificate


def test_mass_bound_is_sharp_for_parallel_gradient_and_tangent():
    evidence = o4_skyrme_pointwise_evidence(
        [[2, 0, 0, 0], [-3, 0, 0, 0], [5, 0, 0, 0]],
        [7, 0, 0, 0],
    )

    assert evidence.mass_lower_bound_gap == 0
    assert evidence.mass_quadratic_form == 2 * evidence.tangent_norm_squared


def test_mutated_quartic_sign_breaks_positivity():
    evidence = o4_skyrme_pointwise_evidence(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [1, 0, 0, 0],
    )

    mutated_quartic = -evidence.quartic_trace_form
    assert evidence.quartic_trace_form == 1
    assert mutated_quartic == -1


def test_mutated_mass_without_identity_term_breaks_lower_bound():
    evidence = o4_skyrme_pointwise_evidence(
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [1, 0, 0, 0],
    )
    mutated_mass = evidence.mass_operator - 2 * sp.eye(4)

    assert evidence.mass_operator == 2 * sp.eye(4)
    assert (evidence.tangent.T * mutated_mass * evidence.tangent)[0] == 0
    assert 0 < 2 * evidence.tangent_norm_squared


def test_existing_derrick_api_matches_full_space_alpha_parameterization():
    e2, e4 = sp.symbols("E2 E4", positive=True)
    scale, alpha = sp.symbols("s alpha", real=True, positive=True)
    evidence = derrick_scaling_evidence(e2, e4, scale)

    assert sp.simplify(
        evidence.scaled_energy.subs(scale, -sp.log(alpha))
        - (alpha * e2 + e4 / alpha)
    ) == 0
    assert evidence.slope_at_origin == -e2 + e4
    assert evidence.curvature_at_origin == e2 + e4


@pytest.mark.parametrize(
    ("gradients", "tangent", "message"),
    [
        ([[1, 0, 0, 0]], [1, 0, 0, 0], "spatial_gradients must have shape"),
        ([[0] * 4] * 3, [1, 0], "tangent must have shape"),
        ([[sp.Float("1.0")] + [0] * 3] + [[0] * 4] * 2, [1, 0, 0, 0], "exact"),
        ([[sp.I, 0, 0, 0]] + [[0] * 4] * 2, [1, 0, 0, 0], "explicitly real"),
    ],
)
def test_invalid_inputs_are_rejected(gradients, tangent, message):
    with pytest.raises(ValueError, match=message):
        o4_skyrme_pointwise_evidence(gradients, tangent)
