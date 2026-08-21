import json, sys
import numpy as np
from pathlib import Path
HERE = Path('.').resolve()
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE/'..'/'0041')); sys.path.insert(0, str(HERE/'..'/'0042'))
from debox_ladder import project_root, solve_radius

state = json.loads((HERE/'ladder-state.json').read_text())
last = state['ladder'][-1]
radius, values, order = last['radius'], np.asarray(last['values']), last['order']
print(f"resuming from R={radius} order={order}", flush=True)
for target, new_order in ((26.0, 44), (28.0, 48), (30.0, 54)):
    if target <= radius:
        continue
    seed = project_root(values, order, new_order)
    import debox_ladder
    _orig = debox_ladder.root
    def root_fast(residual, seed, jac=None, method=None, options=None):
        options = dict(options or {}, maxfev=90, xtol=5e-12)
        return _orig(residual, seed, jac=jac, method='hybr', options=options)
    debox_ladder.root = root_fast
    row = solve_radius(new_order, seed, target, radial_nodes=max(48, int(np.ceil(new_order*48/20/8))*8))
    debox_ladder.root = _orig
    ok = row['rel_grad'] < 1e-9 and np.isfinite(row['energy']) and row['energy'] < 3*last['energy']
    print(f"R={target} order={new_order} E={row['energy']:.8f} "
          f"I={row['inertia']:.6f} lam_branch={row['lambda_min_branch']:+.3e} "
          f"relgrad={row['rel_grad']:.1e} accepted={ok}", flush=True)
    if not ok:
        break
    radius, values, order = target, np.asarray(row['values']), new_order
    row['values'] = row['values'].tolist() if hasattr(row['values'], 'tolist') else row['values']
    state['ladder'].append(row)
    STATE = HERE/'ladder-state.json'
    STATE.write_text(json.dumps(state, indent=2))
print('done')
