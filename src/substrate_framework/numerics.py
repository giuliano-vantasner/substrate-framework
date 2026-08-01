"""Reusable SciPy-backed numerical evidence for physics claims.

These helpers centralize solver failure handling and the evidence that campaign
verifiers need to inspect.  They deliberately do not assign epistemic status:
an IVP or PDE solution remains resolution-bounded numerical evidence until the
claim-specific convergence, conservation, sensitivity, and comparison gates
have passed.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import solve_bvp, solve_ivp

FloatArray = NDArray[np.float64]


class NumericalFailure(RuntimeError):
    """Raised when a numerical method cannot produce valid evidence."""


@dataclass(frozen=True)
class SolverTolerances:
    """Explicit adaptive-solver tolerances shared by IVP and PDE checks."""

    rtol: float = 1.0e-9
    atol: float = 1.0e-12
    max_step: float = np.inf

    def __post_init__(self) -> None:
        if not np.isfinite(self.rtol) or self.rtol <= 0.0:
            raise ValueError("rtol must be positive and finite")
        if not np.isfinite(self.atol) or self.atol <= 0.0:
            raise ValueError("atol must be positive and finite")
        if self.max_step <= 0.0 or np.isnan(self.max_step):
            raise ValueError("max_step must be positive")


@dataclass(frozen=True)
class IVPEvidence:
    """The solution and diagnostic evidence returned by an IVP integration."""

    time: FloatArray
    state: FloatArray
    method: str
    function_evaluations: int
    invariant_values: FloatArray | None
    max_abs_invariant_drift: float | None


@dataclass(frozen=True)
class BVPEvidence:
    """The converged mesh, state, and collocation residuals for a BVP."""

    coordinate: FloatArray
    state: FloatArray
    rms_residuals: FloatArray
    iterations: int

    @property
    def max_rms_residual(self) -> float:
        """Return the largest interval residual, or zero for an empty mesh."""

        return float(np.max(self.rms_residuals, initial=0.0))


@dataclass(frozen=True)
class RefinementEvidence:
    """Errors and empirical orders from a claim-defined refinement study."""

    resolutions: tuple[int, ...]
    errors: tuple[float, ...]
    observed_orders: tuple[float | None, ...]

    @property
    def errors_strictly_decrease(self) -> bool:
        """Whether every refinement reduced the claim-defined error."""

        return all(fine < coarse for coarse, fine in zip(self.errors, self.errors[1:]))

    @property
    def final_error(self) -> float:
        return self.errors[-1]


def _real_vector(values: ArrayLike, *, name: str) -> FloatArray:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1 or array.size == 0:
        raise ValueError(f"{name} must be a nonempty one-dimensional real array")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def trapezoid_integral(values: ArrayLike, coordinate: ArrayLike) -> float:
    """Integrate sampled values across supported NumPy API generations.

    NumPy 2 renamed ``trapz`` to ``trapezoid`` and later removed the legacy
    alias, while this package also supports NumPy 1.26.  Resolve the current
    name first and use the legacy name only when the installed version needs
    it.  Keeping the dispatch here prevents scientific modules from carrying
    inconsistent version probes.
    """

    implementation = getattr(np, "trapezoid", None)
    if implementation is None:
        implementation = getattr(np, "trapz", None)
    if implementation is None:
        raise NumericalFailure("NumPy provides neither trapezoid nor trapz")
    result = float(implementation(values, coordinate))
    if not np.isfinite(result):
        raise NumericalFailure("trapezoidal integration returned a non-finite value")
    return result


def solve_ivp_evidence(
    rhs: Callable[[float, FloatArray], ArrayLike],
    time_span: tuple[float, float],
    initial_state: ArrayLike,
    *,
    sample_times: ArrayLike | None = None,
    tolerances: SolverTolerances = SolverTolerances(),
    method: str = "DOP853",
    invariant: Callable[[FloatArray], float] | None = None,
    **solver_options: Any,
) -> IVPEvidence:
    """Solve a real-valued IVP and retain diagnostics needed by a verifier.

    ``invariant`` is evaluated on every returned sample.  The helper reports
    absolute drift; the claim verifier must set a physically justified pass
    threshold and should also refine tolerances and sampling independently.
    """

    state0 = _real_vector(initial_state, name="initial_state")
    times = None if sample_times is None else _real_vector(sample_times, name="sample_times")
    if not np.all(np.isfinite(time_span)) or time_span[1] <= time_span[0]:
        raise ValueError("time_span must contain finite, increasing endpoints")

    result = solve_ivp(
        rhs,
        time_span,
        state0,
        method=method,
        t_eval=times,
        rtol=tolerances.rtol,
        atol=tolerances.atol,
        max_step=tolerances.max_step,
        **solver_options,
    )
    if not result.success:
        raise NumericalFailure(f"IVP integration failed: {result.message}")
    if not np.all(np.isfinite(result.y)):
        raise NumericalFailure("IVP integration returned non-finite state values")

    invariant_values: FloatArray | None = None
    invariant_drift: float | None = None
    if invariant is not None:
        invariant_values = np.asarray(
            [invariant(result.y[:, index]) for index in range(result.y.shape[1])],
            dtype=np.float64,
        )
        if not np.all(np.isfinite(invariant_values)):
            raise NumericalFailure("invariant evaluation returned non-finite values")
        invariant_drift = float(np.max(np.abs(invariant_values - invariant_values[0])))

    return IVPEvidence(
        time=np.asarray(result.t, dtype=np.float64),
        state=np.asarray(result.y, dtype=np.float64),
        method=method,
        function_evaluations=int(result.nfev),
        invariant_values=invariant_values,
        max_abs_invariant_drift=invariant_drift,
    )


def solve_method_of_lines(
    spatial_rhs: Callable[[float, FloatArray], ArrayLike],
    time_span: tuple[float, float],
    initial_state: ArrayLike,
    **options: Any,
) -> IVPEvidence:
    """Integrate a caller-discretized PDE in time with IVP evidence capture.

    The spatial discretization, boundary conditions, mesh, and refinement study
    remain explicit responsibilities of the claim implementation.  This avoids
    presenting a generic time integrator as a proof of a particular PDE model.
    """

    return solve_ivp_evidence(spatial_rhs, time_span, initial_state, **options)


def solve_bvp_evidence(
    equations: Callable[[FloatArray, FloatArray], ArrayLike],
    boundary_residual: Callable[[FloatArray, FloatArray], ArrayLike],
    coordinate: ArrayLike,
    state_guess: ArrayLike,
    *,
    tolerance: float = 1.0e-6,
    max_nodes: int = 10_000,
    **solver_options: Any,
) -> BVPEvidence:
    """Solve a two-point BVP and retain collocation residual evidence."""

    x = _real_vector(coordinate, name="coordinate")
    guess = np.asarray(state_guess, dtype=np.float64)
    if guess.ndim != 2 or guess.shape[1] != x.size:
        raise ValueError("state_guess must have shape (state dimension, coordinate size)")
    if not np.all(np.isfinite(guess)):
        raise ValueError("state_guess must contain only finite values")
    if tolerance <= 0.0 or not np.isfinite(tolerance):
        raise ValueError("tolerance must be positive and finite")
    if max_nodes < x.size:
        raise ValueError("max_nodes cannot be smaller than the initial mesh")

    result = solve_bvp(
        equations,
        boundary_residual,
        x,
        guess,
        tol=tolerance,
        max_nodes=max_nodes,
        **solver_options,
    )
    if not result.success:
        raise NumericalFailure(f"BVP solve failed: {result.message}")
    if not np.all(np.isfinite(result.y)):
        raise NumericalFailure("BVP solve returned non-finite state values")

    return BVPEvidence(
        coordinate=np.asarray(result.x, dtype=np.float64),
        state=np.asarray(result.y, dtype=np.float64),
        rms_residuals=np.asarray(result.rms_residuals, dtype=np.float64),
        iterations=int(result.niter),
    )


def refinement_study(
    resolutions: Sequence[int],
    solve: Callable[[int], Any],
    error: Callable[[Any], float],
) -> RefinementEvidence:
    """Run a resolution study using a claim-defined solution and error metric.

    Resolution is interpreted as inverse characteristic spacing, so empirical
    order is ``log(error_coarse/error_fine) / log(N_fine/N_coarse)``.  The
    caller must justify that interpretation for its discretization and choose
    an error metric appropriate to the physical claim.
    """

    levels = tuple(int(value) for value in resolutions)
    if len(levels) < 3:
        raise ValueError("a refinement study requires at least three resolutions")
    if any(level <= 0 for level in levels) or any(
        fine <= coarse for coarse, fine in zip(levels, levels[1:])
    ):
        raise ValueError("resolutions must be positive and strictly increasing")

    errors = tuple(float(error(solve(level))) for level in levels)
    if any(value < 0.0 or not np.isfinite(value) for value in errors):
        raise NumericalFailure("refinement error must be finite and nonnegative")

    orders: list[float | None] = []
    for coarse_n, fine_n, coarse_error, fine_error in zip(
        levels, levels[1:], errors, errors[1:]
    ):
        if coarse_error == 0.0 or fine_error == 0.0:
            orders.append(None)
        else:
            orders.append(
                float(
                    np.log(coarse_error / fine_error)
                    / np.log(float(fine_n) / float(coarse_n))
                )
            )

    return RefinementEvidence(levels, errors, tuple(orders))
