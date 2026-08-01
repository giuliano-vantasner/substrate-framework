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
from .optical_geometry import (
    index_from_potential,
    optical_box_static_1d,
    optical_dilaton,
    optical_metric_1d,
    optical_ricci_scalar_1d,
    slow_geodesic_acceleration_1d,
    slow_geodesic_acceleration_from_potential,
)
from .collective_dynamics import (
    optical_collective_acceleration,
    optical_collective_lagrangian,
    slow_optical_collective_acceleration,
    virial_scaling_exponents,
)
from .constitutive import (
    co_scaled_inverse_permeability,
    co_scaled_permittivity,
    co_scaled_wave_speed,
    local_wave_speed,
)
from .radial_energy import (
    capillary_critical_radius,
    capillary_energy,
    line_energy,
    spherical_shell_energy,
)
from .sine_gordon import (
    breather_action,
    breather_energy,
    breather_energy_from_action,
    breather_field,
    breather_field_with_width,
    breather_inverse_width,
    breather_frequency_from_action,
    breather_mean_gradient_integral,
    breather_peak_amplitude,
    breather_period,
    breather_threshold_deficit,
    hamiltonian_density,
    sine_gordon_residual,
)
from .skyrme_relations import (
    conditional_anw_mass,
    conditional_topological_mass,
    matched_pion_coupling_ratio,
)
from .thermal import (
    symmetric_two_level_gate,
    two_level_occupation_variance,
    two_level_upper_occupation,
)
from .verification import CheckFailure, CheckLedger
from .variational import (
    euler_lagrange_expression,
    solve_euler_lagrange_acceleration,
)

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
    "breather_mean_gradient_integral",
    "breather_peak_amplitude",
    "breather_period",
    "breather_threshold_deficit",
    "capillary_critical_radius",
    "capillary_energy",
    "co_scaled_inverse_permeability",
    "co_scaled_permittivity",
    "co_scaled_wave_speed",
    "conditional_anw_mass",
    "conditional_topological_mass",
    "hamiltonian_density",
    "index_from_potential",
    "load_yaml",
    "line_energy",
    "local_wave_speed",
    "optical_box_static_1d",
    "optical_collective_acceleration",
    "optical_collective_lagrangian",
    "optical_dilaton",
    "optical_metric_1d",
    "optical_ricci_scalar_1d",
    "refinement_study",
    "render_claim_memory",
    "render_claim_index",
    "render_release_memory",
    "matched_pion_coupling_ratio",
    "solve_bvp_evidence",
    "solve_ivp_evidence",
    "solve_method_of_lines",
    "slow_geodesic_acceleration_1d",
    "slow_geodesic_acceleration_from_potential",
    "slow_optical_collective_acceleration",
    "spherical_shell_energy",
    "symmetric_two_level_gate",
    "sine_gordon_residual",
    "validate_registry",
    "validate_release",
    "two_level_occupation_variance",
    "two_level_upper_occupation",
    "euler_lagrange_expression",
    "solve_euler_lagrange_acceleration",
    "virial_scaling_exponents",
]

__version__ = "0.0.0"
