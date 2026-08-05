#!/usr/bin/env python3
"""Primary exact verifier for C-BRN-002 and the P200 MD5 disposition."""
from __future__ import annotations
import ast, hashlib
from pathlib import Path
import sympy as sp
from substrate_framework.branching import population_dependent_weight_ledger
from substrate_framework.bosonic_fock import factorial_one_modes
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger

ROOT=Path(__file__).resolve().parents[2]; CAMP=Path(__file__).resolve().parent
SOURCE=Path('/home/dan/substrate/merged-framework/bridges/phase-38/bridge_MD5_phase32_preserved_and_isotope_handshake.py')
PINS={'source':'bcc45611ce87312a11cdc35d2bdc4c1a92b2e9fdb44c427f7676701f69326ecb','release':'a3bc09fb69e92518d347adbb68aa234181e2f97dd0ccf593fc9f52e3d0b1f700','freeze':'c017630b21c121613e533efde39b941ffa325d8f53bba99c3e271eb668e464b9','module':'4bd14de47c233548b8d4e8d35d734bf8293652a7e5cd5ddfbd5208993edfaa2d'}
def digest(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def main()->int:
 c=CheckLedger('P200-MD5-PRIMARY'); text=SOURCE.read_text(); tree=ast.parse(text)
 c.check('source pinned',digest(SOURCE)==PINS['source'])
 c.check('base release pinned',digest(ROOT/'governance/releases/v0.148.0.yaml')==PINS['release'])
 c.check('formula freeze pinned',digest(CAMP/'evidence/formula-freeze.yaml')==PINS['freeze'])
 c.check('module pinned',digest(ROOT/'src/substrate_framework/branching.py')==PINS['module'])
 calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check']
 literals=[n for n in calls if n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)]
 c.check('source inventory separates sites from executions',len(calls)==33 and len(literals)==25)
 a=audit_numpy_trapezoid_compatibility(text,filename=str(SOURCE))
 c.check('source has no quadrature compatibility surface',a.legacy_references==a.current_references==a.eager_legacy_default_fallbacks==0)
 N,rho,w,s=sp.symbols('N rho w s',positive=True)
 ledger=population_dependent_weight_ledger(N,rho,w,s)
 expected=-rho*(w+N*s)/(N*w+rho)**2
 c.check('API has full chain-rule derivative',sp.simplify(ledger.comparison_fraction_derivative-expected)==0)
 c.check('constant weight recovers C-BRN-001',population_dependent_weight_ledger(N,rho,w,0).comparison_fraction_derivative==-rho*w/(N*w+rho)**2)
 cases=[(1/sp.sqrt(N),-1/(2*N**sp.Rational(3,2)),'decreasing'),(1/N,-1/N**2,'stationary'),(1/N**2,-2/N**3,'increasing')]
 for weight,slope,verdict in cases:
  c.check(f'positive weight realizes {verdict}',population_dependent_weight_ledger(N,rho,weight,slope).monotonicity==verdict)
 c.mutation_sensitive('N times weight derivative is load bearing',lambda k: sp.simplify((w+k*N*s)-(w+N*s))==0,1,[0,2])
 c.check('positive integer static mode tie is complete',factorial_one_modes(intensity=20,support='all_nonnegative')==(19,20))
 c.check('source unique floor mode is incomplete','n* = floor(S)' in text and factorial_one_modes(intensity=20,support='all_nonnegative')!=(20,))
 c.check('source isotope conclusion is premise text not an oracle','K and a are electronic' in text and 'Born-Oppenheimer' in text)
 c.check('physical ceilings remain explicit',ledger.physical_weight_law_is_separate_premise and ledger.exhaustive_channel_interpretation_is_separate_premise)
 return c.finish()
if __name__=='__main__': raise SystemExit(main())
