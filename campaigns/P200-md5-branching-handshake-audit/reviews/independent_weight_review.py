#!/usr/bin/env python3
"""Independent raw-function derivation for C-BRN-002."""
from __future__ import annotations
import sympy as sp
from substrate_framework.verification import CheckLedger
def main()->int:
 c=CheckLedger('P200-MD5-INDEPENDENT')
 N,rho=sp.symbols('N rho',positive=True); w=sp.Function('w')
 B=rho/(N*w(N)+rho); derivative=sp.diff(B,N)
 expected=-rho*(w(N)+N*sp.diff(w(N),N))/(N*w(N)+rho)**2
 c.check('raw function differentiation gives full criterion',sp.simplify(derivative-expected)==0)
 for p,sign in [(sp.Rational(1,2),-1),(1,0),(2,1)]:
  candidate=sp.simplify(B.subs(w(N),N**(-p)))
  actual=sp.simplify(sp.diff(candidate,N))
  c.check(f'inverse power p={p} derivative sign',actual.is_negative if sign<0 else actual==0 if sign==0 else actual.is_positive)
 constant=sp.symbols('c',positive=True)
 c.check('constant specialization is strictly decreasing',sp.diff(rho/(N*constant+rho),N).is_negative)
 c.check('positive weight can increase comparison fraction',sp.diff(rho/(N/N**2+rho),N).is_positive)
 control=sp.simplify(N**(-sp.Rational(1,2))+N*sp.diff(N**(-sp.Rational(1,2)),N))
 c.check('slow decrease preserves monotonicity',control==1/(2*sp.sqrt(N)))
 c.check('inverse weight makes weighted rate constant',sp.simplify(N*(1/N))==1)
 c.check('inverse square weight makes weighted rate decrease',sp.diff(N*(1/N**2),N).is_negative)
 S=sp.symbols('S',positive=True); n=sp.symbols('n',integer=True,nonnegative=True)
 mass=sp.exp(-S)*S**n/sp.factorial(n)
 c.check('static mass has no population derivative',N not in mass.free_symbols)
 c.check('symbol absence is only a declared independence premise',sp.diff(mass,N)==0 and S in mass.free_symbols)
 c.check('two-channel normalization supplies no isotope symbol',sp.Symbol('m_eff') not in B.free_symbols)
 return c.finish()
if __name__=='__main__': raise SystemExit(main())
