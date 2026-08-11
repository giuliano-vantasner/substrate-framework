"""Generate the explicit Christoffel-component block for the 3+1D tutorial.

Emits, for each upper index sigma in {0,1,2,3} and each symmetric lower pair
(rho, nu) with rho <= nu, the simplified expansion of

    Gamma^sigma_{rho nu} = (1/2) sum_lambda g^{sigma lambda}
                           ( d_rho g_{lambda nu} + d_nu g_{lambda rho}
                             - d_lambda g_{rho nu} ),

with the trivial cancellations carried through (the lambda = rho and
lambda = nu terms simplify; for rho = nu the mixed derivative doubles).
The output is the exact LaTeX block embedded in
docs/tutorials/einbein_3plus1D/einbein_3plus1D_tutorial.md between the
sentinels  % BEGIN GENERATED CHRISTOFFELS  and  % END GENERATED CHRISTOFFELS.
tests/test_einbein_3plus1d_tutorial.py regenerates this block and diffs it
against the document, and separately checks every component against the
general formula numerically.

Usage: python3 generate_christoffel_block.py
"""

DIM = 4


def bracket(lam: int, rho: int, nu: int) -> str:
    """The simplified bracket multiplying (1/2) g^{sigma lam}."""
    if rho == nu:
        # 2 d_rho g_{lam rho} - d_lam g_{rho rho}
        if lam == rho:
            return rf"\partial_{{{rho}}} g_{{{rho}{rho}}}"
        return rf"2 \partial_{{{rho}}} g_{{{lam}{rho}}} - \partial_{{{lam}}} g_{{{rho}{rho}}}"
    if lam == rho:
        return rf"\partial_{{{nu}}} g_{{{rho}{rho}}}"
    if lam == nu:
        return rf"\partial_{{{rho}}} g_{{{nu}{nu}}}"
    return (
        rf"\partial_{{{rho}}} g_{{{lam}{nu}}}"
        rf" + \partial_{{{nu}}} g_{{{lam}{rho}}}"
        rf" - \partial_{{{lam}}} g_{{{rho}{nu}}}"
    )


def component_line(sigma: int, rho: int, nu: int) -> str:
    parts = []
    for lam in range(DIM):
        b = bracket(lam, rho, nu)
        multi = " + " in b or " - " in b
        parts.append(
            rf"\tfrac{{1}}{{2}} g^{{{sigma}{lam}}}\, "
            + (rf"\left( {b} \right)" if multi else b)
        )
    terms = " + ".join(parts)
    return rf"\Gamma^{{{sigma}}}_{{}}{{{rho}{nu}}} &= {terms} \\"


def generate_block() -> str:
    lines = ["<!-- BEGIN GENERATED CHRISTOFFELS -->"]
    for sigma in range(DIM):
        lines.append(f"For $\\sigma = {sigma}$:")
        lines.append("")
        lines.append(r"$$\begin{aligned}")
        for rho in range(DIM):
            for nu in range(rho, DIM):
                lines.append(component_line(sigma, rho, nu))
        lines[-1] = lines[-1].rstrip(" \\")  # last line of the block: no \\
        lines.append(r"\end{aligned}$$")
        lines.append("")
    lines.append("<!-- END GENERATED CHRISTOFFELS -->")
    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_block())
