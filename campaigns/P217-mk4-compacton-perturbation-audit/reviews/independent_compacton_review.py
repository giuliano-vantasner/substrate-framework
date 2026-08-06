"""Fresh exact compacton review without MK4 or canonical APIs."""
from __future__ import annotations
from pathlib import Path
import sympy as sp, yaml
from substrate_framework.verification import CheckLedger
ROOT=Path(__file__).resolve().parents[3]
def main()->int:
 c=CheckLedger('P217-independent'); y,R,L,M,B=sp.symbols('y R L M B',positive=True); F=2*sp.acos(y); Fp=sp.diff(F,y)/R
 density=L*B/(2*R**3*y**2)*sp.sin(F)**2*(-sp.diff(F,y)); potential=M*sp.sqrt(2)*sp.sin(F/2); R3=2*sp.sqrt(2)*L*B/M
 c.check('fresh compacton substitution fixes the radius',sp.simplify((density-potential).subs(R**3,R3))==0)
 x=sp.symbols('x',positive=True); Fe=2*sp.acos(1-x); Fr=-sp.diff(Fe,x)/R; I=sp.simplify((R*(1-x))**2*Fr**2)
 c.check('fresh edge limit gives residue two',sp.limit(x*I,x,0)==2)
 d,z=sp.symbols('d z',positive=True); J=4*R*sp.integrate(z**2/(1-z**2),(z,0,1-d))
 c.check('fresh cutoff integral diverges logarithmically',sp.limit(J,d,0,dir='+')==sp.oo and sp.limit(d*sp.diff(J,d),d,0,dir='+')==-2*R)
 c.check('fresh L4 limits are finite',sp.limit(sp.sin(Fe)**2*Fr**2,x,0)==16/R**2 and sp.limit(sp.sin(Fe)**4/(R*(1-x))**2,x,0)==0)
 c.check('fresh nonlinear degree mutation defeats balanced cancellation',2*sp.Integer(2)-4==0 and 2*2**sp.Rational(4,3)-4**sp.Rational(4,3)!=0)
 claims={q['id']:q for q in yaml.safe_load((ROOT/'governance/claims.yaml').read_text())['claims']}
 c.check('fresh registry audit keeps existence conditional','does not establish that an equality configuration exists' in claims['C-BPS-001']['statement'])
 c.check('fresh registry audit keeps perturbation controlled','controlled expansions' in claims['C-BPS-003']['statement'])
 c.check('divergence leaves a separate positive continuation problem',sp.diff(J,d)!=0 and sp.limit(J-2*R*sp.log(1/d),d,0,dir='+').is_finite is True)
 return c.finish()
if __name__=='__main__': raise SystemExit(main())
