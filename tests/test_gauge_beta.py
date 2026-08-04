import pytest
import sympy as sp

from substrate_framework.gauge_beta import (
    GaugeFactor,
    ProductMultiplet,
    abelian_gauge_rescaling_ledger,
    gauge_only_beta,
    product_gauge_coefficients,
)


def _factors() -> tuple[GaugeFactor, ...]:
    return (
        GaugeFactor("U1", 0, is_abelian=True),
        GaugeFactor("SU2", 2),
        GaugeFactor("SU3", 3),
    )


def _multiplet(
    label: str,
    kind: str,
    multiplicity: int,
    dimensions: tuple[int, int],
    hypercharge: sp.Expr,
) -> ProductMultiplet:
    color, isospin = dimensions
    gut_charge_squared = sp.Rational(3, 5) * hypercharge**2
    s2 = (
        gut_charge_squared * color * isospin,
        sp.Rational(1, 2) * color if isospin == 2 else 0,
        sp.Rational(1, 2) * isospin if color == 3 else 0,
    )
    c2 = (
        gut_charge_squared,
        sp.Rational(3, 4) if isospin == 2 else 0,
        sp.Rational(4, 3) if color == 3 else 0,
    )
    return ProductMultiplet(label, kind, multiplicity, s2, c2)


def _declared_sm_like_multiplets() -> tuple[ProductMultiplet, ...]:
    return (
        _multiplet("Q_L", "weyl_fermion", 3, (3, 2), sp.Rational(1, 6)),
        _multiplet("u_R_conj", "weyl_fermion", 3, (3, 1), -sp.Rational(2, 3)),
        _multiplet("d_R_conj", "weyl_fermion", 3, (3, 1), sp.Rational(1, 3)),
        _multiplet("L_L", "weyl_fermion", 3, (1, 2), -sp.Rational(1, 2)),
        _multiplet("e_R_conj", "weyl_fermion", 3, (1, 1), 1),
        _multiplet("H", "complex_scalar", 1, (1, 2), sp.Rational(1, 2)),
    )


def test_declared_sm_like_table_reproduces_exact_gauge_coefficients() -> None:
    ledger = product_gauge_coefficients(_factors(), _declared_sm_like_multiplets())
    assert ledger.one_loop == (sp.Rational(41, 10), -sp.Rational(19, 6), -7)
    assert ledger.two_loop_gauge_matrix == (
        (sp.Rational(199, 50), sp.Rational(27, 10), sp.Rational(44, 5)),
        (sp.Rational(9, 10), sp.Rational(35, 6), 12),
        (sp.Rational(11, 10), sp.Rational(9, 2), -26),
    )
    assert "Yukawa" in ledger.omitted_terms[0]
    assert "row a" in ledger.beta_convention


def test_contribution_ledger_sums_without_hidden_remainder() -> None:
    ledger = product_gauge_coefficients(_factors(), _declared_sm_like_multiplets())
    for a in range(3):
        assert ledger.one_loop[a] == sp.simplify(
            ledger.one_loop_gauge[a]
            + ledger.one_loop_weyl_fermions[a]
            + ledger.one_loop_complex_scalars[a]
        )
        for b in range(3):
            assert ledger.two_loop_gauge_matrix[a][b] == sp.simplify(
                ledger.two_loop_gauge[a][b]
                + ledger.two_loop_weyl_fermions[a][b]
                + ledger.two_loop_complex_scalars[a][b]
            )


def test_pure_gauge_and_complex_scalar_weights_are_explicit() -> None:
    pure = product_gauge_coefficients((GaugeFactor("G", 3),))
    assert pure.one_loop == (-11,)
    assert pure.two_loop_gauge_matrix == ((-102,),)
    scalar = product_gauge_coefficients(
        (GaugeFactor("G", 2),),
        (ProductMultiplet("phi", "complex_scalar", 1, (sp.Rational(1, 2),), (sp.Rational(3, 4),)),),
    )
    assert scalar.one_loop_complex_scalars == (sp.Rational(1, 6),)
    assert scalar.two_loop_complex_scalars == ( (sp.Rational(13, 6),), )


def test_abelian_generator_rescaling_is_exactly_covariant() -> None:
    ledger = product_gauge_coefficients(_factors(), _declared_sm_like_multiplets())
    rho = sp.Symbol("rho", positive=True)
    rescaling = abelian_gauge_rescaling_ledger(ledger, (rho, 1, 1))
    assert rescaling.one_loop_residuals == (0, 0, 0)
    assert rescaling.two_loop_residuals == ((0, 0, 0),) * 3
    assert rescaling.rescaled.one_loop[0] == rho**2 * ledger.one_loop[0]
    assert rescaling.rescaled.two_loop_gauge_matrix[0][0] == (
        rho**4 * ledger.two_loop_gauge_matrix[0][0]
    )
    assert rescaling.rescaled.two_loop_gauge_matrix[0][2] == (
        rho**2 * ledger.two_loop_gauge_matrix[0][2]
    )
    assert rescaling.rescaled.two_loop_gauge_matrix[2][0] == (
        rho**2 * ledger.two_loop_gauge_matrix[2][0]
    )


def test_gauge_beta_polynomial_transforms_with_inverse_abelian_scale() -> None:
    ledger = product_gauge_coefficients(_factors(), _declared_sm_like_multiplets())
    rho = sp.Symbol("rho", positive=True)
    g1, g2, g3 = sp.symbols("g1 g2 g3", real=True)
    transformed = abelian_gauge_rescaling_ledger(ledger, (rho, 1, 1)).rescaled
    base_beta = gauge_only_beta(ledger, (g1, g2, g3))
    transformed_beta = gauge_only_beta(transformed, (g1 / rho, g2, g3))
    assert tuple(
        sp.simplify(transformed_beta[a] - base_beta[a] / ((rho, 1, 1)[a]))
        for a in range(3)
    ) == (0, 0, 0)


def test_load_bearing_table_mutations_change_the_coefficients() -> None:
    baseline_table = _declared_sm_like_multiplets()
    baseline = product_gauge_coefficients(_factors(), baseline_table)
    no_higgs = product_gauge_coefficients(_factors(), baseline_table[:-1])
    two_generations = product_gauge_coefficients(
        _factors(),
        tuple(
            ProductMultiplet(
                item.label,
                item.kind,
                2 if item.kind == "weyl_fermion" else item.multiplicity,
                item.dynkin_indices,
                item.quadratic_casimirs,
            )
            for item in baseline_table
        ),
    )
    ql = baseline_table[0]
    no_ql_color = ProductMultiplet(
        ql.label,
        ql.kind,
        ql.multiplicity,
        (ql.dynkin_indices[0] / 3, ql.dynkin_indices[1] / 3, 0),
        (ql.quadratic_casimirs[0], ql.quadratic_casimirs[1], 0),
    )
    no_ql_color_table = (no_ql_color,) + baseline_table[1:]
    no_color = product_gauge_coefficients(_factors(), no_ql_color_table)
    assert no_higgs.one_loop != baseline.one_loop
    assert two_generations.one_loop != baseline.one_loop
    assert no_color.one_loop != baseline.one_loop
    assert no_color.two_loop_gauge_matrix != baseline.two_loop_gauge_matrix
    assert tuple(zip(*baseline.two_loop_gauge_matrix, strict=True)) != (
        baseline.two_loop_gauge_matrix
    )


@pytest.mark.parametrize(
    "factors,multiplets,error",
    [
        ((), (), ValueError),
        ((GaugeFactor("", 0),), (), ValueError),
        ((GaugeFactor("U1", 1, True),), (), ValueError),
        ((GaugeFactor("U1a", 0, True), GaugeFactor("U1b", 0, True)), (), ValueError),
        ((GaugeFactor("G", 1.0),), (), ValueError),
        (
            (GaugeFactor("G", 1),),
            (ProductMultiplet("x", "dirac_fermion", 1, (1,), (1,)),),
            ValueError,
        ),
        (
            (GaugeFactor("G", 1),),
            (ProductMultiplet("x", "weyl_fermion", 0, (1,), (1,)),),
            ValueError,
        ),
        (
            (GaugeFactor("G", 1),),
            (ProductMultiplet("x", "weyl_fermion", 1, (), (1,)),),
            ValueError,
        ),
        (
            (GaugeFactor("G", 1),),
            (ProductMultiplet("x", "weyl_fermion", 1, (1,), (-1,)),),
            ValueError,
        ),
    ],
)
def test_invalid_factor_and_multiplet_tables_are_rejected(
    factors: tuple[GaugeFactor, ...],
    multiplets: tuple[ProductMultiplet, ...],
    error: type[Exception],
) -> None:
    with pytest.raises(error):
        product_gauge_coefficients(factors, multiplets)


def test_invalid_rescalings_and_coupling_lengths_are_rejected() -> None:
    ledger = product_gauge_coefficients(_factors(), _declared_sm_like_multiplets())
    with pytest.raises(ValueError):
        abelian_gauge_rescaling_ledger(ledger, (1, 2, 1))
    with pytest.raises(ValueError):
        abelian_gauge_rescaling_ledger(ledger, (1, 1))
    with pytest.raises(ValueError):
        gauge_only_beta(ledger, (1, 2))
