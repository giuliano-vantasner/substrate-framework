"""Canonical, importable definitions and derivations for Substrate."""

from .governance import (
    GovernanceError,
    load_yaml,
    render_claim_memory,
    render_claim_index,
    render_release_memory,
    validate_registry,
    validate_release,
)
from .numerics import (
    BVPEvidence,
    IVPEvidence,
    NumericalFailure,
    RefinementEvidence,
    SolverTolerances,
    refinement_study,
    solve_bvp_evidence,
    solve_ivp_evidence,
    solve_method_of_lines,
)
from .sine_gordon import (
    breather_action,
    breather_energy,
    breather_energy_from_action,
    breather_field,
    breather_field_with_width,
    breather_inverse_width,
    breather_frequency_from_action,
    breather_peak_amplitude,
    breather_period,
    hamiltonian_density,
    sine_gordon_residual,
)
from .verification import CheckFailure, CheckLedger

__all__ = [
    "BVPEvidence",
    "GovernanceError",
    "CheckFailure",
    "CheckLedger",
    "IVPEvidence",
    "NumericalFailure",
    "RefinementEvidence",
    "SolverTolerances",
    "breather_action",
    "breather_energy",
    "breather_energy_from_action",
    "breather_field",
    "breather_field_with_width",
    "breather_inverse_width",
    "breather_frequency_from_action",
    "breather_peak_amplitude",
    "breather_period",
    "hamiltonian_density",
    "load_yaml",
    "refinement_study",
    "render_claim_memory",
    "render_claim_index",
    "render_release_memory",
    "solve_bvp_evidence",
    "solve_ivp_evidence",
    "solve_method_of_lines",
    "sine_gordon_residual",
    "validate_registry",
    "validate_release",
]

__version__ = "0.0.0"
