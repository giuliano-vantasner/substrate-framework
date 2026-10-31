"""Native coherent response of an original ionic impulse from a saved dual.

No electronic legs are replayed: their original perturbation is exactly zero.
The Hilbert pairing is dual.p.conjugate() @ seed.p, not a covariance contraction.
The affected spatial oracle compares this to independent discrete forward RK4
and dense physical-density evolution, including nonzero-cell complex phases.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT/'src'), str(HERE)]

import numpy as np

from substrate_framework.material_control_reference import bound_json
from substrate_framework.streamed_material_state import file_binding
from joint_spatial_provenance import authenticate, canonical, same_binding

SCHEMA = 'P254-source-local-dual-coherent-readout-v1'
SEED_SCHEMA = 'P254-original-local-ionic-momentum-seed-v1'
CONVENTION = 'vdot(original-t0-dual.p, amplitude*exp(-2pi i q.cell)*unit_atom_axis/sqrt(N)); all other initial perturbations zero'


def canonical_impulse(context, q, ncells, seed):
    """Pure scalar contraction; exact complex convention exercised by oracle."""
    fields = {'schema', 'initial_perturbation', 'case', 'model_identity', 'initialization',
              'atom', 'axis', 'amplitude', 'cell'}
    if (set(seed) != fields or seed.get('schema') != SEED_SCHEMA
            or seed.get('initial_perturbation') != 'ionic-momentum-only'
            or type(ncells) is not int or ncells < 1 or type(seed['atom']) is not int
            or seed['atom'] < 1 or seed['axis'] not in ('x', 'y', 'z')
            or type(seed['amplitude']) not in (int, float) or not np.isfinite(seed['amplitude'])):
        raise ValueError('explicit original ionic-momentum-only seed required')
    cell, q = np.asarray(seed['cell']), np.asarray(q, float)
    if (cell.shape != (3,) or not np.isfinite(cell).all() or not np.array_equal(cell, np.rint(cell))
            or q.shape != (3,) or not np.isfinite(q).all()):
        raise ValueError('original integer kick cell and finite q required')
    encoded = np.asarray(context['small']['p'], float)
    if encoded.ndim != 2 or encoded.shape[1] != 2 or len(encoded) % 3 or not np.isfinite(encoded).all():
        raise ValueError('native finite complex canonical dual momentum required')
    momentum = encoded[:, 0]+1j*encoded[:, 1]
    coordinate = 3*(seed['atom']-1)+'xyz'.index(seed['axis'])
    if coordinate >= len(momentum):
        raise ValueError('original seed atom outside canonical dual geometry')
    impulse = seed['amplitude']*np.exp(-2j*np.pi*q@cell)/np.sqrt(ncells)
    return momentum[coordinate].conjugate()*impulse


def build_readout(pair_binding, seed_binding, oracle_binding, *, snapshots=()):
    """Authenticate publication, original seed and executed consumer proof."""
    pair, seed, proof = (bound_json(b) for b in (pair_binding, seed_binding, oracle_binding))
    source = file_binding(Path(__file__).resolve())
    if (proof.get('schema') != 'P254-joint-spatial-readout-oracle-v1' or proof.get('status') != 'passed'
            or not any(same_binding(source, b) for b in proof['source_bindings'])
            or not all(name in proof['checks'] for name in (
                'source_local_dual_discrete_forward_q0', 'source_local_dual_discrete_forward_q1',
                'source_local_dual_discrete_forward_q2'))):
        raise ValueError('executed source-bound dual/coherent spatial oracle required')
    if (pair.get('schema') != 'P254-source-local-q-material-v1-result'
            or pair.get('status') != 'complete' or pair.get('covariance_executed') is not True):
        raise ValueError('completed actual source-local material pair required')
    p, c = pair['provenance'], pair['covariance']
    selectors = p['request']['selectors']
    if (not same_binding(seed['initialization'], p['initialization'])
            or seed['case'] != p['case'] or seed['model_identity'] != p['model_identity']):
        raise ValueError('original seed initialization/case/scalar differs')
    initial = bound_json(p['initialization'])
    saved = initial['saved']
    if (initial.get('status') != 'complete' or saved['specification']['scalar'] != p['scalar']
            or saved['model_identity'] != p['model_identity']
            or sha256(canonical(saved['specification']).encode()).hexdigest() != p['model_identity']):
        raise ValueError('original saved physical authority differs')
    origin = bound_json(saved['joint_boundary'])
    slots = origin['slots']
    keys = [tuple(int(i) for i in s['identity'].replace(':', ',').split(',')) for s in slots]
    mesh = np.max(np.asarray(keys)[:, 1:], axis=0)+1
    spins = {key[0] for key in keys}
    expected = {(spin, *index) for spin in spins for index in np.indices(tuple(mesh)).reshape(3, -1).T}
    if (not keys or len(keys) != len(set(keys)) or set(keys) != expected
            or origin['time_ry_inverse'] != 0 or origin['model_identity'] != p['model_identity']):
        raise ValueError('literal complete original source geometry required')
    for binding in (saved['original_boundary'], saved['preparation']):
        authenticate(binding, snapshots)
    context = bound_json(c['left_context'])
    request = bound_json(context['request'])
    if (context.get('schema') != 'source-local-q-pullback-v1' or context.get('complete') is not True
            or context['time'] != 0 or request['provenance'] != p
            or request['identity'] != c['propagation_identity'] or request['q'] != selectors['q']
            or request['times'] != pair['time_grid'] or context['terminal_time'] != pair['time_grid'][-1]
            or request['probe']['identity'] != p['observable'] or request['probe']['units'] != 'Ry/bohr'):
        raise ValueError('original propagated left dual/probe/time differs')
    value = canonical_impulse(context, selectors['q'], int(np.prod(mesh)), seed)
    result = dict(schema=SCHEMA, status='complete', complete=True, pair_result=pair_binding,
        seed=seed_binding, numerical_oracle=oracle_binding, consumer_sources=[source],
        source_snapshots=list(snapshots),
        context=c['left_context'], context_request=context['request'], convention=CONVENTION,
        q=selectors['q'], case=p['case'], model_identity=p['model_identity'], scalar=p['scalar'],
        physical_specification=saved['specification'], initialization=p['initialization'], baseline=p['baseline'],
        matched_aggregate=p['matched_aggregate'], dynamics=selectors['dynamics'], observable=p['observable'],
        atom=selectors['atom'], axis=selectors['axis'], time_ry_inverse=pair['time_grid'][-1],
        time_grid=pair['time_grid'], all_explicit_edges=p['all_explicit_edges'], fixed_original_D=p['fixed_original_D'],
        original_cell_count=int(np.prod(mesh)), original_source_slots=len(keys),
        source_bindings=p['source_bindings'], readout=dict(real=float(value.real), imag=float(value.imag)),
        numerical_accuracy_certified=False, whole_spatial_reconstruction=False)
    return result


def validate_readout(record, seed):
    if record.get('schema') != SCHEMA or record.get('status') != 'complete' or record.get('complete') is not True:
        raise ValueError('native complete dual coherent readout required')
    original_seed = bound_json(record['seed'])
    if original_seed != seed:
        raise ValueError('dual coherent original seed differs')
    rebuilt = build_readout(record['pair_result'], record['seed'], record['numerical_oracle'],
                            snapshots=record['source_snapshots'])
    if rebuilt != record:
        raise ValueError('dual coherent publication differs from original context/seed/proof')
    return dict(readout=record['readout'], amplitude=seed['amplitude'], cell=seed['cell'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('pair', 'seed', 'oracle'):
        parser.add_argument('--'+name, type=Path, required=True)
        parser.add_argument('--'+name+'-sha256', required=True)
    parser.add_argument('--source-snapshots', type=Path)
    parser.add_argument('--source-snapshots-sha256')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    bindings = []
    for name in ('pair', 'seed', 'oracle'):
        binding = file_binding(getattr(args, name))
        if binding['sha256'] != getattr(args, name+'_sha256'):
            raise ValueError('explicit '+name+' digest differs')
        bindings.append(binding)
    snapshots = []
    if (args.source_snapshots is None) != (args.source_snapshots_sha256 is None):
        raise ValueError('source snapshot file and explicit digest must be supplied together')
    if args.source_snapshots is not None:
        binding = file_binding(args.source_snapshots)
        if binding['sha256'] != args.source_snapshots_sha256:
            raise ValueError('explicit source snapshot manifest digest differs')
        snapshots = bound_json(binding)
        if not isinstance(snapshots, list):
            raise ValueError('source snapshot manifest must contain the original/snapshot binding list')
    result = build_readout(*bindings, snapshots=snapshots)
    if result['original_cell_count'] != 64 or result['original_source_slots'] != 128:
        raise ValueError('material CLI requires original64-q/128-spin source geometry')
    # Validate the full scientific pair join before emitting a scalar. This is
    # a read-only consumer and never changes the source producer or its owner.
    from joint_spatial_source_local import validate_source_local
    pair = bound_json(bindings[0])
    initial = bound_json(result['initialization'])
    validate_source_local(result, bound_json(bindings[1]), pair, bound_json(pair['owner']),
                          initial['saved'], result['initialization'], [4, 4, 4], snapshots)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')


if __name__ == '__main__':
    main()
