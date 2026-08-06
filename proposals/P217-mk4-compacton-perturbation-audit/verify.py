"""Primary exact verifier for P217 MK4."""
from __future__ import annotations
import ast, hashlib, subprocess
from pathlib import Path
import sympy as sp
import yaml
from substrate_framework.bps_energy import bps_bound_per_absolute_degree
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger

ROOT=Path(__file__).resolve().parents[2]; CAMPAIGN=Path(__file__).resolve().parent
SOURCE=Path('/home/dan/substrate/merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py')
SHA='9f2e299032aace53c3ac2c2d1d5626372e4bdf1aa3b7b0650f574a9f7b8f7295'
FREEZE='b6988bf00bc1822809cafda355044de3720e3d03258e9599326786e1bbb9e216'

def main()->int:
 c=CheckLedger('P217'); data=SOURCE.read_bytes(); text=data.decode(); tree=ast.parse(text)
 c.check('source and freeze hashes are pinned',hashlib.sha256(data).hexdigest()==SHA and hashlib.sha256((CAMPAIGN/'evidence/formula-freeze.yaml').read_bytes()).hexdigest()==FREEZE)
 calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check']; asserts=[n for n in ast.walk(tree) if isinstance(n,ast.Assert)]
 c.check('source inventory separates six predicates and one assertion',len(calls)==6 and len(asserts)==1)
 a=audit_numpy_trapezoid_compatibility(text,filename=str(SOURCE))
 c.check('MK4 has no legacy NumPy integration access',a.legacy_references==0 and a.eager_legacy_default_fallbacks==0 and 'from scipy.integrate import trapezoid' in text)
 run=subprocess.run([str(ROOT/'.venv/bin/python'),str(SOURCE)],cwd=ROOT,capture_output=True,text=True,check=False)
 c.check('native source reaches all six checks',run.returncode==0 and run.stdout.rstrip().endswith('ALL 6 CHECKS PASS'))
 u,B=sp.symbols('u B',positive=True)
 c.check('radial density endpoint substitution gives degree B',sp.simplify(-(2*B/sp.pi)*sp.integrate(sp.sin(u)**2,(u,sp.pi,0))-B)==0)
 y,R,lam,mu=sp.symbols('y R lambda mu',positive=True)
 F=2*sp.acos(y); Fy=sp.diff(F,y)
 lhs=sp.simplify(lam*B/(2*R**3*y**2)*sp.sin(F)**2*(-Fy)); rhs=sp.simplify(mu*sp.sqrt(2)*sp.sin(F/2))
 R3=2*sp.sqrt(2)*lam*B/mu
 c.check('compacton exactly satisfies the declared radial equation',sp.simplify((lhs-rhs).subs(R**3,R3))==0)
 c.check('radius coefficient mutation breaks the radial equation',sp.simplify((lhs-rhs).subs(R**3,2*R3))!=0)
 x=sp.symbols('x',positive=True); Fx=2*sp.acos(1-x); dFdr=sp.diff(Fx,x)*(-1/R); l2=sp.simplify((R*(1-x))**2*dFdr**2)
 c.check('edge profile and first derivative have square-root and inverse-square-root orders',sp.limit(Fx/sp.sqrt(x),x,0)==2*sp.sqrt(2) and sp.limit((-dFdr)*R*sp.sqrt(x),x,0)==sp.sqrt(2))
 c.check('L2 edge integrand has exact simple-pole coefficient two',sp.limit(x*l2,x,0)==2)
 delta=sp.symbols('delta',positive=True); z=sp.symbols('z',positive=True)
 trunc=sp.simplify(4*R*sp.integrate(z**2/(1-z**2),(z,0,1-delta)))
 c.check('cutoff integral diverges with exact slope 2R',sp.limit(trunc,delta,0,dir='+')==sp.oo and sp.limit(delta*sp.diff(trunc,delta),delta,0,dir='+')==-2*R)
 c.check('explicit smoothing width cannot produce regulator-independent first order coefficient',sp.limit(trunc-2*R*sp.log(1/delta),delta,0,dir='+').is_finite is True and sp.diff(trunc,delta)!=0)
 sin2=sp.simplify(sp.sin(Fx)**2); l4a=sp.simplify(sin2*dFdr**2); l4b=sp.simplify(sp.sin(Fx)**4/(R*(1-x))**2)
 c.check('L4 edge factors stay finite separately',sp.limit(l4a,x,0)==16/R**2 and sp.limit(l4b,x,0)==0)
 W=sp.symbols('W',positive=True); K=bps_bound_per_absolute_degree(lam,mu,W)
 c.check('degree-linear BPS contribution cancels only in the balanced conditional ledger',sp.simplify(2*(K*2)-K*4)==0 and sp.simplify(2*(K*2)-K*5)!=0)
 claims={q['id']:q for q in yaml.safe_load((ROOT/'governance/claims.yaml').read_text())['claims']}
 c.check('C-BPS-001 does not promote compacton existence or couplings','does not establish that an equality configuration exists' in claims['C-BPS-001']['statement'] and 'select a potential or coupling' in claims['C-BPS-001']['statement'])
 c.check('C-BPS-003 requires controlled remainders rather than this divergent expectation','controlled expansions' in claims['C-BPS-003']['statement'] and 'does not establish that a proposed deformation admits the expansion' in claims['C-BPS-003']['statement'])
 disp=yaml.safe_load((ROOT/'migration/dispositions.yaml').read_text())['units']
 c.check('MK1 through MK3 grant no physical closure',all(disp[k]['disposition']=='qualified' for k in ('MK1','MK2','MK3')) and 'not accepted' in disp['MK1']['qualification'] and 'not accepted' in disp['MK2']['qualification'])
 p107=(ROOT/'campaigns/P107-e4-bps-zero-binding-audit/reviews/independent_bps_review.py').read_text()
 c.check('P107 already owns the exact compacton and edge obstruction','compacton_radius_cube = 2 * sp.sqrt(2) * lam * radial_degree / mu' in p107 and 'pole_coefficient == 2' in p107 and '16 / radius**2' in p107)
 post=yaml.safe_load((CAMPAIGN/'evidence/post-source-claim-delta.yaml').read_text())
 c.check('nonduplication selects no new claim or API',post['promoted_claims']==[] and post['new_apis']==[])
 c.check('positive continuation remains a separately posed boundary-layer or full-model problem',post['continuation_required'] is True and post['source_disposition']=='qualified')
 return c.finish()
if __name__=='__main__': raise SystemExit(main())
