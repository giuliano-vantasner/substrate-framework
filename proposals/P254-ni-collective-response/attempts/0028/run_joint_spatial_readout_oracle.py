#!/usr/bin/env python3
"""Independent finite full-q oracle; executable-only temporary synthetic inputs.

No production material result is fabricated. Dense real-space SciPy canonical
oscillators plus an exact SymPy character table independently supply expected
values. This script has not been executed by the implementation worker.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT/'src'), str(HERE)]

import numpy as np
from scipy.linalg import expm
import sympy as sp
from substrate_framework.joint_spatial_readout import coherent_local, reconstruct
from substrate_framework.joint_response_observables import spatial_pair
from substrate_framework.spatial_readout_metrics import periodic_distances, selected_weight
from substrate_framework.material_control_reference import bound_json
from substrate_framework.streamed_material_state import file_binding
from joint_spatial_receipts import authenticate, canonical, read_entries, validate_records
from run_joint_spatial_readout import encode, sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    checks = {}

    def close(name, actual, expected, tolerance=3e-11):
        error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        if not np.isfinite(error) or error > tolerance:
            raise AssertionError(name+': '+str(error))
        checks[name] = dict(max_absolute_error=error, tolerance=tolerance)

    def reject(name, operation):
        try:
            operation()
        except (ValueError, KeyError):
            checks[name] = dict(rejected=True)
        else:
            raise AssertionError(name+' was accepted')

    n, mesh = 4, np.array([4, 1, 1])
    cells = np.array([[r, 0, 0] for r in range(n)])
    q = cells/mesh
    # Exact, independently defined character table: unitary normalization and
    # nonzero seed cell force the sign to matter (cell1 is not its own inverse).
    exact = sp.Matrix(n, n, lambda r, k: sp.exp(2*sp.pi*sp.I*r*k/n)/sp.sqrt(n))
    identity = (exact.conjugate().T*exact).applyfunc(sp.simplify)
    if identity != sp.eye(n):
        raise AssertionError('exact character orthogonality')
    seed = sp.Matrix([sp.exp(-2*sp.pi*sp.I*k/n)/sp.sqrt(n) for k in range(n)])
    delta = (exact*seed).applyfunc(sp.simplify)
    if delta != sp.Matrix([0, 1, 0, 0]):
        raise AssertionError('exact localized kick normalization/sign')
    seed_np = np.array([complex(x.evalf()) for x in seed])
    close('coherent_local_exact_sqrtN_sign', coherent_local(q, seed_np, cells), [0, 1, 0, 0])
    checks['sympy_character_orthogonality'] = True
    if np.linalg.norm(coherent_local(q, seed_np, -cells)-[0, 1, 0, 0]) < 1:
        raise AssertionError('q sign fixture is not discriminating')
    checks['wrong_q_sign_is_detectable'] = True
    ordered_character = seed_np*np.sqrt(n)
    close('ordered_pair_exact_1overN_sign_no_extra_dagger',
          [spatial_pair(q, ordered_character, cell, [0, 0, 0], ncells=n) for cell in cells],
          [0, 1, 0, 0])

    # Two local canonical species (electron/ion origin labels) and ONE global
    # field oscillator. Dense real-space construction, never q evolution.
    d = 2*n+1
    k = np.diag([2.+.7*(i % 2) for i in range(2*n)]+[3.1])
    for r in range(n):
        for target, coefficient in ((2*r+1, .19), (2*((r+1) % n)+1, .31)):
            k[2*r, target] += coefficient
            k[target, 2*r] += coefficient
        k[2*r+1, -1] = k[-1, 2*r+1] = .13/np.sqrt(n)
    j = np.block([[np.zeros((d, d)), np.eye(d)], [-np.eye(d), np.zeros((d, d))]])
    h = np.block([[k, np.zeros((d, d))], [np.zeros((d, d)), np.eye(d)]])
    t, s = .47, .23
    left, right = expm(t*j@h), expm(s*j@h)
    force = np.zeros((n, 2*d))
    force[:, :d] = -k[np.arange(n)*2+1]
    origins = []
    for label in range(3):
        w = np.zeros((2*d, 2*d), complex)
        ix = list(range(label, 2*n, 2)) if label < 2 else [d-1]
        for a in ix:
            omega = 1.1+.3*label
            w[a, a], w[d+a, d+a] = 1/(2*omega), omega/2
            w[a, d+a], w[d+a, a] = .5j, -.5j
        origins.append(w)
    real_ab = [force@left@w@right.T@force.T for w in origins]
    real_ba = [force@left@w.T@right.T@force.T for w in origins]
    fourier = np.array(exact.conjugate().T.evalf()).astype(complex)
    ab_parts = np.array([np.diag(fourier@x@fourier.conj().T) for x in real_ab]).T
    ba_parts = np.array([np.diag(fourier@x@fourier.conj().T) for x in real_ba]).T
    ab = np.column_stack((ab_parts, ab_parts.sum(axis=1)))
    ba = np.column_stack((ba_parts, ba_parts.sum(axis=1)))
    kick = np.zeros(2*d)
    kick[d+3] = 1.7  # ionic momentum in original cell1
    local_force = force@left@kick
    q_force = fourier@local_force
    geometry = np.array([[2., .7, .1], [0., 1.8, .2], [0., 0., 2.3]])
    reconstructed = reconstruct(q, q_force, ab, ba, mesh=mesh, cell_bohr=geometry,
                                kick_cell=[1, 0, 0], reference_cell=[1, 0, 0])
    close('coherent_dense_real_space', reconstructed['coherent_force_ry_bohr'], local_force)
    expected_ab = np.column_stack([x[:, 1] for x in real_ab]+[sum(real_ab)[:, 1]])
    expected_ba = np.column_stack([x[:, 1] for x in real_ba]+[sum(real_ba)[:, 1]])
    for name, expected in (('AB', expected_ab), ('BA', expected_ba),
                           ('symmetrized', (expected_ab+expected_ba)/2),
                           ('commutator', expected_ab-expected_ba)):
        actual = reconstructed['connected_force_pairs_ry2_bohr2'][name]
        close(name+'_dense_real_space_all_origins', actual, expected)
        close(name+'_origin_sum', actual[:, :3].sum(axis=1), actual[:, 3])
    if np.linalg.norm(expected_ab[:, 2]) == 0:
        raise AssertionError('field origin oracle lacks signal')
    checks['nonzero_global_field_origin'] = True
    if abs(ab[1, 2])+abs(ab[2, 2])+abs(ab[3, 2]) > 1e-11:
        raise AssertionError('one global field leaked out of Gamma')
    close('opposite_ordering_reality', expected_ab, expected_ba.conj())
    perturbed = reconstruct(q, q_force+1j*1e-4, ab, ba, mesh=mesh, cell_bohr=geometry,
                            kick_cell=[1, 0, 0], reference_cell=[1, 0, 0])
    if perturbed['reality_residuals']['coherent_imaginary_max'] < 1e-4:
        raise AssertionError('imaginary coherent signal was clipped')
    checks['imaginary_signal_retained'] = True

    distances = periodic_distances(cells, [1, 0, 0], mesh, geometry)
    brute = [min(np.linalg.norm(geometry@(cell-[1, 0, 0]-mesh*np.array([a, b, c])))
                 for a in range(-4, 5) for b in range(-4, 5) for c in range(-4, 5)) for cell in cells]
    close('skew_geometry_minimum_images', distances, brute)
    localized = selected_weight([0, 2, 0, 0], distances, value_units='Ry/bohr')
    extended = selected_weight([2, 2, 2, 2], distances, value_units='Ry/bohr')
    zero = selected_weight(np.zeros(n), distances, value_units='Ry/bohr')
    close('localized_participation', localized['participation_cells'], 1.)
    close('extended_participation', extended['participation_cells'], 4.)
    close('localized_extent', localized['rms_distance_bohr'], 0.)
    if zero['defined'] or any(zero[key] is not None for key in
            ('participation_cells', 'participation_fraction', 'rms_distance_bohr', 'normalized_weight_by_cell')):
        raise AssertionError('zero signal falsely localized')
    checks['zero_signal_undefined'] = True

    # Temporary schema fixtures exercise actual bound-json and scientific-join
    # consumer paths. They are NOT production outputs or material trajectories.
    with TemporaryDirectory(prefix='p254-spatial-oracle-') as temporary:
        directory = Path(temporary)

        def save(name, value):
            path = directory/name
            path.write_text(json.dumps(encode(value), allow_nan=False)+'\n')
            return file_binding(path)

        source = save('source.json', {'finite_oracle_only': True})
        initial = save('initial.json', {'finite_oracle_only': True})
        aggregate = save('aggregate.json', {'finite_oracle_only': True})
        baseline = save('baseline.json', {'finite_oracle_only': True})
        saved = dict(case='finite-oracle-only', model_identity='finite-independent-real-space',
                     specification=dict(scalar='finite-independent-real-space', aggregate=aggregate))
        records, requests, all_entries = [], [], []
        for i in range(n):
            identity = sha256(canonical(dict(model=saved['model_identity'], q=q[i].tolist(),
                dynamics='screened-joint', sources=[source])).encode()).hexdigest()
            quantum = dict(AB=dict(zip(('electronic', 'ionic', 'field', 'total'), ab[i])),
                BA=dict(zip(('electronic', 'ionic', 'field', 'total'), ba[i])),
                symmetrized=(ab[i, 3]+ba[i, 3])/2, commutator=ab[i, 3]-ba[i, 3],
                time=t, second_time=s, dynamics='screened-joint', propagation_identity=identity,
                preparation_identity='original-matched-product-'+saved['model_identity'])
            record = dict(schema='P254-joint-q-material-v2', status='complete', q=q[i].tolist(),
                required_q_for_whole_local=n, fixed_original_D=True, all_explicit_edges=2*n,
                case=saved['case'], model_identity=saved['model_identity'], scalar=saved['specification']['scalar'],
                matched_aggregate=aggregate, initialization=initial, baseline=baseline,
                dynamics='screened-joint', source_bindings=[source], time_grid=[0., t],
                second_time_grid=[0., s], observable='original-H1x-total-force', quantum=quantum,
                coherent=dict(readout=q_force[i], amplitude=1.7, cell=[1, 0, 0]))
            request = dict(identity=identity, mode='all', case=saved['case'], initialization=initial,
                baseline=baseline, q=q[i].tolist(), times=[0., t], second_times=[0., s],
                atom=1, axis='x', amplitude=1.7, cell=[1, 0, 0], subdivisions=1, block_size=8,
                checkpoint='None', checkpoint_sha256=None)
            entry = dict(result=save('result-%d.json' % i, record),
                         request=save('request-%d.json' % i, request))
            all_entries.append(entry)
            records.append(bound_json(entry['result']))
            requests.append(bound_json(entry['request']))
        _, force_out, ab_out, ba_out = validate_records(records, requests, saved, initial, mesh)
        close('receipt_coherent_roundtrip', force_out, q_force)
        close('receipt_AB_roundtrip', ab_out, ab)
        close('receipt_BA_roundtrip', ba_out, ba)
        reject('missing_q', lambda: validate_records(records[:-1], requests[:-1], saved, initial, mesh))
        duplicate = deepcopy(records)
        duplicate[-1]['q'] = duplicate[0]['q']
        reject('duplicate_q', lambda: validate_records(duplicate, requests, saved, initial, mesh))
        offgrid = deepcopy(records)
        offgrid[-1]['q'][0] = .17
        reject('off_grid_q', lambda: validate_records(offgrid, requests, saved, initial, mesh))
        changes = {
            'mixed_baseline': lambda r: r.update(baseline=source),
            'mixed_case': lambda r: r.update(case='other'),
            'mixed_observable': lambda r: r.update(observable='original-H1y-total-force'),
            'mixed_preparation': lambda r: r['quantum'].update(preparation_identity='other'),
            'mixed_dynamics': lambda r: r.update(dynamics='bare-electronic'),
            'mixed_time': lambda r: r['quantum'].update(time=t+.01),
            'mixed_sources': lambda r: r.update(source_bindings=[initial]),
            'missing_origin': lambda r: r['quantum']['AB'].pop('field'),
            'inconsistent_origin_sum': lambda r: r['quantum']['AB'].update(total=99.),
            'incomplete_status': lambda r: r.update(status='partial')}
        for name, change in changes.items():
            changed = deepcopy(records)
            change(changed[-1])
            reject(name, lambda: validate_records(changed, requests, saved, initial, mesh))

        def consume(entries):
            forward, forward_requests, pairs, pair_requests = read_entries(entries)
            return validate_records(forward, forward_requests, saved, initial, mesh,
                                    pair_records=pairs, pair_requests=pair_requests)

        split_entries = []
        for i, (record, request) in enumerate(zip(records, requests)):
            forward, pair = deepcopy(record), deepcopy(record)
            del forward['quantum']
            del pair['coherent']
            forward_request, pair_request = dict(request, mode='forward'), dict(request, mode='pair')
            split_entries.append(dict(
                forward=dict(result=save('forward-result-%d.json' % i, forward),
                             request=save('forward-request-%d.json' % i, forward_request)),
                pair=dict(result=save('pair-result-%d.json' % i, pair),
                          request=save('pair-request-%d.json' % i, pair_request))))
        for label, entries in (('all_manifest', all_entries), ('split_manifest', split_entries),
                               ('mixed_forms_manifest', all_entries[:2]+split_entries[2:])):
            selected, f_read, a_read, b_read = consume(entries)
            close(label+'_coherent_dense', coherent_local(q, f_read, cells), local_force)
            close(label+'_AB_origins', a_read, ab)
            close(label+'_BA_origins', b_read, ba)
            if selected != validate_records(records, requests, saved, initial, mesh)[0]:
                raise AssertionError(label+' changed scientific comparison identity')
        split_changes = (
            'source', 'baseline', 'time', 'second_time', 'seed_amplitude', 'seed_cell',
            'seed_atom', 'seed_axis', 'preparation', 'q', 'scalar', 'observable', 'mode')
        for name in split_changes:
            entries = deepcopy(split_entries)
            pair = bound_json(entries[-1]['pair']['result'])
            request = bound_json(entries[-1]['pair']['request'])
            if name == 'source':
                pair['source_bindings'] = [initial]
            elif name == 'baseline':
                pair['baseline'] = request['baseline'] = source
            elif name in ('time', 'second_time'):
                record_key, request_key = ('time_grid', 'times') if name == 'time' else ('second_time_grid', 'second_times')
                new_time = pair['quantum'][name]+.01
                pair[record_key] = request[request_key] = [0., new_time]
                pair['quantum'][name] = new_time
            elif name.startswith('seed_'):
                key = name.removeprefix('seed_')
                request[key] = dict(amplitude=1.9, cell=[2, 0, 0], atom=2, axis='y')[key]
            elif name == 'preparation':
                pair['quantum']['preparation_identity'] = 'different-original-preparation'
            elif name == 'q':
                pair['q'] = request['q'] = [0., 0., 0.]
            elif name == 'scalar':
                pair['scalar'] = 'different-scalar'
            elif name == 'observable':
                pair['observable'], request['axis'] = 'original-H1y-total-force', 'y'
            elif name == 'mode':
                request['mode'] = 'forward'
            identity = sha256(canonical(dict(model=pair['model_identity'], q=pair['q'],
                dynamics=pair['dynamics'], sources=pair['source_bindings'])).encode()).hexdigest()
            request['identity'] = pair['quantum']['propagation_identity'] = identity
            entries[-1]['pair'] = dict(result=save('mismatch-'+name+'-result.json', pair),
                                       request=save('mismatch-'+name+'-request.json', request))
            reject('split_mismatched_'+name, lambda: consume(entries))
        reject('split_forward_alone', lambda: consume([split_entries[0]['forward']]+split_entries[1:]))
        reject('split_missing_pair_binding', lambda: consume([dict(forward=split_entries[0]['forward'])]+split_entries[1:]))
        Path(split_entries[0]['pair']['result']['path']).write_text('changed split bytes\n')
        reject('split_changed_bound_result', lambda: consume(split_entries))
        Path(source['path']).write_text('changed bytes\n')
        reject('changed_bound_source', lambda: authenticate(source))
        reject('changed_bound_json', lambda: bound_json(source))
    bindings = sources()
    result = dict(schema='P254-joint-spatial-readout-oracle-v1', status='passed',
        source_bindings=bindings, source_file_count=len(bindings), check_count=len(checks), checks=checks,
        scope='finite4-q independent real-space/SymPy consumer oracle only; no material64-q input available',
        material_spatial_result=False)
    with args.output.open('x') as stream:
        json.dump(encode(result), stream, indent=2, allow_nan=False)
        stream.write('\n')


if __name__ == '__main__':
    main()
