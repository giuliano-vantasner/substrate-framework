"""Constructive replacements for repairable P238 manuscript claims.

These formulas preserve the intended wave/lump-to-effective-geometry program
while narrowing or correcting claims that are not supported as written.  They
are proposed replacement derivations, not Substrate claims used as a gate.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import sympy as sp


@dataclass(frozen=True)
class Replacement:
    claims: str
    name: str
    passed: bool
    revised_claim: str
    detail: str


def _zero(expression: sp.Expr | sp.MatrixBase) -> bool:
    simplified = sp.simplify(expression)
    if isinstance(simplified, sp.MatrixBase):
        return simplified == sp.zeros(*simplified.shape)
    return simplified == 0


def run() -> list[Replacement]:
    replacements: list[Replacement] = []

    def record(
        claims: str,
        name: str,
        passed: bool,
        revised_claim: str,
        detail: object,
    ) -> None:
        replacements.append(
            Replacement(claims, name, bool(passed), revised_claim, str(detail))
        )

    # S01: make the model class explicit and prove the advertised expansion
    # inside that class.  The construction no longer claims uniqueness among
    # actions with higher derivatives, parity-odd terms, or derivative/potential
    # cross-couplings.
    time_derivative, flow_derivative = sp.symbols(
        "time_derivative flow_derivative", real=True
    )
    material_derivative = time_derivative + flow_derivative
    scoped_kinetic = sp.expand(material_derivative**2)
    scoped_expansion = (
        time_derivative**2
        + 2 * time_derivative * flow_derivative
        + flow_derivative**2
    )
    record(
        "P238-S01",
        "scoped material-derivative action",
        _zero(scoped_kinetic - scoped_expansion),
        "Within local, first-derivative, quadratic, time-reversal-even real-scalar models whose prescribed flow enters only through D_t u=partial_t u+V dot grad(u), the displayed kinetic action expands exactly as stated.",
        scoped_kinetic,
    )

    # S02: retain the potential curvature in the full constant-background
    # linearization and reserve "convective wave operator" for its principal
    # part.
    rho0, theta0, mass_sq = sp.symbols(
        "rho0 theta0 mass_sq", positive=True
    )
    d2_material_u, laplacian_u, field = sp.symbols(
        "D2_material_u laplacian_u field", real=True
    )
    full_linearized = (
        d2_material_u
        - theta0 / rho0 * laplacian_u
        + mass_sq / rho0 * field
    )
    principal_part = d2_material_u - theta0 / rho0 * laplacian_u
    record(
        "P238-S02",
        "full constant-background linearization",
        _zero(full_linearized - principal_part - mass_sq * field / rho0),
        "The full linearized equation is D_t^2 u-c0^2 Laplacian(u)+U''(0)u/rho0=0; the quoted convective wave operator is its principal part.",
        sp.expand(full_linearized),
    )

    # S03: replace scalar determinant matching as a reflectionless criterion by
    # the normal directional impedance condition for the declared scalar wave.
    rho_left, rho_right = sp.symbols("rho_left rho_right", positive=True)
    normal_theta_left, normal_theta_right = sp.symbols(
        "normal_theta_left normal_theta_right", positive=True
    )
    impedance_left = sp.sqrt(rho_left * normal_theta_left)
    impedance_right = sp.sqrt(rho_right * normal_theta_right)
    reflection = sp.simplify(
        (impedance_right - impedance_left)
        / (impedance_right + impedance_left)
    )
    matched_reflection = sp.simplify(
        reflection.subs(
            normal_theta_right,
            rho_left * normal_theta_left / rho_right,
        )
    )
    record(
        "P238-S03",
        "directional interface matching",
        _zero(matched_reflection),
        "For a fixed interface normal n, reflection vanishes when rho_L(n^T Theta_L n)=rho_R(n^T Theta_R n); determinant matching may remain as a separate constitutive normalization.",
        matched_reflection,
    )

    # S05: use the slowness surface rather than the ordinary quadratic form of
    # N for a generic propagation direction.
    c0, ax, ay, kx, ky = sp.symbols(
        "c0 ax ay kx ky", positive=True
    )
    unit_constraint = sp.symbols("unit_constraint", positive=True)
    phase_index = c0 / sp.sqrt(ax * kx**2 + ay * ky**2)
    phase_speed = c0 / phase_index
    record(
        "P238-S05",
        "directional phase-index replacement",
        _zero(phase_speed**2 - ax * kx**2 - ay * ky**2),
        "For a unit direction khat, n_phase(khat)=c0/sqrt(khat^T A khat), so c_phase=sqrt(khat^T A khat).",
        (phase_index, unit_constraint),
    )

    # S08: for a genuine boosted localized family, Lorentz-covariant energy
    # and momentum give the square-root collective Lagrangian by Legendre
    # transform. This states exactly the additional assumption the draft needs.
    rest_energy, speed, velocity, gamma = sp.symbols(
        "rest_energy speed velocity gamma", positive=True
    )
    momentum = gamma * rest_energy * velocity / speed**2
    energy = gamma * rest_energy
    legendre_lagrangian = sp.expand(momentum * velocity - energy)
    gamma_relation = gamma**2 * (speed**2 - velocity**2) - speed**2
    gamma_relation_residual = sp.factor(
        gamma * legendre_lagrangian
        + rest_energy
        + rest_energy * gamma_relation / speed**2
    )
    record(
        "P238-S08 P238-S12",
        "boosted-family square-root replacement",
        _zero(gamma_relation_residual),
        "If an explicit localized solution family is closed under boosts with E=gamma E0 and p=gamma E0 v/c0^2, then L=pv-E=-E0/gamma=-E0 sqrt(1-v^2/c0^2).",
        gamma_relation_residual,
    )

    # S12: the corrected metric gives exact operational clock and ruler
    # relations for the conditional massive worldline.  This is the positive
    # metric consequence supported by the replacement; it does not label a
    # wave cone alone as a proof of a universal equivalence principle.
    local_speed_squared, coordinate_length = sp.symbols(
        "local_speed_squared coordinate_length", nonnegative=True
    )
    spatial_index, conformal_scale = sp.symbols(
        "spatial_index conformal_scale", positive=True
    )
    stationary_clock_rate = 1 / sp.sqrt(conformal_scale)
    local_gamma = 1 / sp.sqrt(1 - local_speed_squared)
    moving_clock_rate = sp.sqrt(
        (1 - local_speed_squared) / conformal_scale
    )
    proper_ruler_length = (
        spatial_index * coordinate_length / sp.sqrt(conformal_scale)
    )
    clock_residual = sp.powdenest(
        moving_clock_rate - stationary_clock_rate / local_gamma,
        force=True,
    )
    ruler_residual = (
        proper_ruler_length**2
        - spatial_index**2 * coordinate_length**2 / conformal_scale
    )
    record(
        "P238-S12",
        "conditional metric clock-and-ruler observables",
        _zero(clock_residual) and _zero(ruler_residual),
        "For the corrected static metric ds^2=nbar^(-1)(-dt^2+sum_i n_i^2 dx_i^2) and 0<=v_local^2<1, a timelike trajectory has d_tau/dt=nbar^(-1/2)/gamma_local and a coordinate interval dx_i has proper length n_i*dx_i/sqrt(nbar); together with the independently derived worldline Euler-Lagrange equation, these are conditional metric clock, ruler, and geodesic relations.",
        (clock_residual, ruler_residual),
    )

    # S11: exact corrected inverse in an anisotropic principal frame.
    nx, ny, vx, vy, nbar = sp.symbols(
        "nx ny vx vy nbar", positive=True
    )
    n_squared = sp.diag(nx**2, ny**2)
    inverse_n_squared = sp.diag(nx**-2, ny**-2)
    flow = sp.Matrix([vx, vy])
    contravariant = nbar * sp.BlockMatrix(
        [
            [sp.Matrix([[-1]]), -flow.T],
            [-flow, inverse_n_squared - flow * flow.T],
        ]
    ).as_explicit()
    corrected_covariant = sp.BlockMatrix(
        [
            [
                sp.Matrix([[-1 + (flow.T * n_squared * flow)[0]]]),
                -(flow.T * n_squared),
            ],
            [-(n_squared * flow), n_squared],
        ]
    ).as_explicit() / nbar
    inverse_residual = (contravariant * corrected_covariant - sp.eye(3)).applyfunc(
        sp.simplify
    )
    record(
        "P238-S11",
        "correct anisotropic block inverse",
        _zero(inverse_residual),
        "With v=V/c0, the inverse of nbar*g^ is nbar^(-1)[[-1+v^T N^2 v,-v^T N^2],[-N^2 v,N^2]].",
        inverse_residual,
    )

    # S15/S16: an exact conformal equatorial Kerr acoustic representation.
    # This keeps zero radial flow but replaces the minimal profiles by the ADM
    # lapse, spatial metric, and azimuthal shift required by every coefficient.
    radius, schwarzschild_radius, spin = sp.symbols(
        "radius schwarzschild_radius spin", positive=True
    )
    delta = radius**2 - schwarzschild_radius * radius + spin**2
    angular = (
        radius**2
        + spin**2
        + spin**2 * schwarzschild_radius / radius
    )
    conformal_factor = sp.simplify(delta / angular)
    acoustic_spatial = sp.diag(
        radius**2 * angular / delta**2,
        angular**2 / delta,
    )
    shift = sp.Matrix(
        [0, spin * schwarzschild_radius / (radius * angular)]
    )
    acoustic_covariant = sp.BlockMatrix(
        [
            [
                sp.Matrix(
                    [[-1 + (shift.T * acoustic_spatial * shift)[0]]]
                ),
                -(shift.T * acoustic_spatial),
            ],
            [-(acoustic_spatial * shift), acoustic_spatial],
        ]
    ).as_explicit()
    target_kerr = sp.Matrix(
        [
            [
                -(1 - schwarzschild_radius / radius),
                0,
                -spin * schwarzschild_radius / radius,
            ],
            [0, radius**2 / delta, 0],
            [
                -spin * schwarzschild_radius / radius,
                0,
                angular,
            ],
        ]
    )
    kerr_residual = (
        conformal_factor * acoustic_covariant - target_kerr
    ).applyfunc(sp.factor)
    record(
        "P238-S15 P238-S16",
        "exact equatorial Kerr acoustic replacement",
        _zero(kerr_residual),
        "For Delta=r^2-rs*r+a^2 and G=r^2+a^2+a^2*rs/r, choose Omega^2=Delta/G, h_rr=r^2*G/Delta^2, h_phiphi=G^2/Delta, and V^phi/c0=a*rs/(r*G); then Omega^2*g_acoustic equals equatorial Kerr exactly.",
        kerr_residual,
    )

    schwarzschild_limit = (
        conformal_factor * acoustic_covariant - target_kerr
    ).subs(spin, 0).applyfunc(sp.simplify)
    record(
        "P238-S15 P238-S16",
        "corrected Kerr map has the Schwarzschild limit",
        _zero(schwarzschild_limit),
        "The exact rotating replacement reduces continuously to the paper's supported exterior Schwarzschild null-cone construction at a=0.",
        schwarzschild_limit,
    )

    # The exact Kerr acoustic tensor also admits explicit determinant-matched
    # constitutive profiles in the physical radial/tangential frame.
    exterior_delta, exterior_angular = sp.symbols(
        "exterior_delta exterior_angular", positive=True
    )
    density_ratio = (exterior_angular / exterior_delta) ** sp.Rational(3, 4)
    acoustic_radial = exterior_delta**2 / (radius**2 * exterior_angular)
    acoustic_tangential = radius**2 * exterior_delta / exterior_angular**2
    stiffness_radial_ratio = sp.powsimp(
        density_ratio * acoustic_radial, force=True
    )
    stiffness_tangential_ratio = sp.powsimp(
        density_ratio * acoustic_tangential, force=True
    )
    constitutive_matching = sp.powsimp(
        density_ratio
        * sp.sqrt(stiffness_radial_ratio * stiffness_tangential_ratio),
        force=True,
    )
    record(
        "P238-S15 P238-S16",
        "exact Kerr determinant-matched constitutive profiles",
        _zero(constitutive_matching - 1),
        "In the exterior physical frame, rho/rho0=(G/Delta)^(3/4), Theta_r/Theta0=Delta^(5/4)/(r^2 G^(1/4)), and Theta_t/Theta0=r^2 Delta^(1/4)/G^(5/4); these reconstruct A and satisfy rho*sqrt(det Theta)=rho0*Theta0.",
        (
            density_ratio,
            stiffness_radial_ratio,
            stiffness_tangential_ratio,
            constitutive_matching,
        ),
    )

    # S17: use the exact Kerr replacement, not resemblance of selected
    # surfaces in the manuscript's minimal rotating model, to derive the two
    # azimuthal null roots and their exterior sign change.
    root_plus = (
        spin * schwarzschild_radius / radius + sp.sqrt(delta)
    ) / angular
    root_minus = (
        spin * schwarzschild_radius / radius - sp.sqrt(delta)
    ) / angular
    null_polynomial = (
        angular * sp.Symbol("omega") ** 2
        - 2 * spin * schwarzschild_radius / radius * sp.Symbol("omega")
        - (1 - schwarzschild_radius / radius)
    )
    root_residuals = tuple(
        sp.factor(null_polynomial.subs(sp.Symbol("omega"), root))
        for root in (root_minus, root_plus)
    )
    adm_substitution = {
        delta: angular * (1 - schwarzschild_radius / radius)
        + spin**2 * schwarzschild_radius**2 / radius**2
    }
    reduced_root_residuals = tuple(
        sp.factor(residual.subs(adm_substitution))
        for residual in root_residuals
    )
    root_product = sp.simplify(
        (root_minus * root_plus).subs(adm_substitution)
    )
    record(
        "P238-S17",
        "exact Kerr azimuthal-null roots",
        all(_zero(residual) for residual in reduced_root_residuals)
        and _zero(
            root_product
            + (1 - schwarzschild_radius / radius) / angular
        ),
        "For the exact exterior Kerr replacement, omega_±=(a*rs/r±sqrt(Delta))/G.  The upper root is positive for a>0; the lower root is negative for r>rs, zero at the equatorial ergosurface r=rs, and positive between that surface and the outer horizon.",
        (reduced_root_residuals, root_product),
    )

    # S18: compose the repaired exact chain.  The numerical real-lump premise
    # is checked independently in scipy_replacements.py and is required by the
    # top-level verifier before this conditional headline is reported.
    exact_chain_claims = {
        "P238-S01",
        "P238-S02",
        "P238-S03",
        "P238-S05",
        "P238-S08 P238-S12",
        "P238-S11",
        "P238-S12",
        "P238-S15 P238-S16",
        "P238-S17",
    }
    exact_chain_passed = all(
        replacement.passed
        for replacement in replacements
        if replacement.claims in exact_chain_claims
    ) and exact_chain_claims.issubset(
        {replacement.claims for replacement in replacements}
    )
    record(
        "P238-S18",
        "composed conditional analogue-kinematics chain",
        exact_chain_passed,
        "The supplied finite-time real 2+1D localized trajectory, explicit O(ell/L) frozen-background estimate, conditional boosted-family square-root action, corrected metric inverse, operational metric observables, and exact equatorial Kerr construction form a self-contained conditional analogue-kinematics chain; the result does not assert an all-potential existence theorem or an unconditional universal equivalence principle.",
        sorted(exact_chain_claims),
    )

    return replacements


def main() -> int:
    replacements = run()
    print(
        json.dumps(
            {
                "oracle": "sympy-replacements",
                "replacements": [asdict(item) for item in replacements],
            },
            indent=2,
        )
    )
    return 0 if all(item.passed for item in replacements) else 1


if __name__ == "__main__":
    raise SystemExit(main())
