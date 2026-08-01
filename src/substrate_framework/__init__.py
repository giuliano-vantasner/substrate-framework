"""Canonical, importable definitions and derivations for Substrate."""

from .governance import GovernanceError, load_yaml, render_claim_index, validate_registry
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
    "load_yaml",
    "refinement_study",
    "render_claim_index",
    "solve_bvp_evidence",
    "solve_ivp_evidence",
    "solve_method_of_lines",
    "validate_registry",
]

__version__ = "0.0.0"
