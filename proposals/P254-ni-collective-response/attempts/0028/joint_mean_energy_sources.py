"""Authenticate saved scalar-only energy inputs; never load frames or apply H0/K.

D/frame identities are preserved through authenticated original boundary/request
metadata, not reread. Only the 256 one_body scalars, two JointStages and admitted
case parameter archives are numerical inputs. The one history-owner execution
change is admitted only by the existing current-source numerical proof.
"""
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from substrate_framework.partitioned_joint_slots import array_identity, digest
from substrate_framework.streamed_joint_reduction import JointStage
from substrate_framework.streamed_material_state import authenticate, file_binding

HERE = Path(__file__).resolve().parent


def bound_json(binding):
    return json.loads(authenticate(binding).read_text())


def same_binding(left, right):
    return (left['path'] == right['path'] and left['sha256'] == right['sha256']
            and int(left['bytes']) == int(right['bytes']))


def parameter_identities(model):
    r = model.reference
    return dict(reference={name: array_identity(getattr(r, name)) for name in
        ('nbar', 'masses', 'curvature', 'ionic_force', 'support_force', 'held_density', 'held_gradient')},
        coefficients={name: array_identity(getattr(model.coefficients, name)) for name in
        ('delta_curvature', 'contact', 'mixed')}, charges=array_identity(model.charges),
        polarizations=array_identity(model.field.polarizations), field_mass=model.field.mass,
        field_volume=model.field.volume_bohr3, measure=model.measure, ncells=r.ncells,
        reality_tolerance=model.reality_tolerance)


def restore_sources(registration_path):
    """Restore original physical authority and authenticate the exact source scope."""
    from matched_joint_case import load_case
    from run_joint_q_material import bind_saved_model
    registration_binding = file_binding(registration_path)
    reg = bound_json(registration_binding)
    if reg['schema'] != 'P254-saved-coupled-mean-energy-registration-v1':
        raise ValueError('registered saved coupled mean energy required')
    original = reg['source_model']
    mean = bound_json(reg['source_mean'])
    initialization = bound_json(original['initialization'])
    saved = initialization['saved']
    if (mean.get('status') != 'complete' or mean.get('mode') != 'evolve'
            or initialization.get('status') != 'complete' or initialization.get('mode') != 'initialize'
            or mean['case'] != initialization['case'] or saved['case'] != mean['case']
            or not same_binding(mean['initialization'], original['initialization'])
            or saved['model_identity'] != original['identity']
            or saved['specification'] != original['specification']):
        raise ValueError('original complete mean/initialization/model differs')
    proof_binding = file_binding(HERE/'paired-contraction-consumer-003/result.json')
    proof = bound_json(proof_binding)
    if (proof.get('status') != 'passed' or proof.get('schema') != 'P254-joint-partitioned-q-oracle-v1'
            or proof['model_identity'] != original['identity']
            or not same_binding(proof['initialization'], original['initialization'])):
        raise ValueError('admitted current-source same-physical-scalar proof required')
    for binding in proof['source_bindings']:
        authenticate(binding)
    continuation = proof['source_compatibility']
    before, after = continuation['before'], continuation['after']
    for binding in original['implementation'] + reg['implementation_sources']:
        if binding['path'] == before['path']:
            if not same_binding(binding, before):
                raise ValueError('registered history-owner scope differs from admitted original')
            authenticate(after)
        else:
            authenticate(binding)
    source_digest = sha256(json.dumps({b['path']: b['sha256'] for b in
        original['implementation']}, sort_keys=True).encode()).hexdigest()
    source_digest = sha256((source_digest+json.dumps(original['column_limits'], sort_keys=True)).encode()).hexdigest()
    if source_digest != original['source_identity']:
        raise ValueError('original source identity does not bind implementation and column limits')
    for binding in reg['archive_sources']:
        authenticate(binding)
    context = bind_saved_model(load_case(mean['case'], reality_tolerance=original['reality_tolerance']),
                               saved, continuation)
    # make_mean installs a lazy operator factory; it does not open a frame or act.
    model = context.make_mean(None, block_size=original['block_size'])
    if model.identity != original['identity']:
        raise ValueError('restored model authority differs')
    if len(reg['stages']) != 2 or len(reg['slot_sources']) != 2 or len(mean['branches']) != 1:
        raise ValueError('exact registered initial/final pair required')
    if reg['stages'][0] != mean['initial_reduction']:
        raise ValueError('registered initial stage differs from original mean')
    if (not same_binding(mean['initial_boundary'], reg['slot_sources'][0]['boundary'])
            or not same_binding(saved['joint_boundary'], reg['slot_sources'][0]['boundary'])
            or not same_binding(mean['branches'][0]['boundary'], reg['slot_sources'][1]['boundary'])
            or not same_binding(proof['history'], reg['slot_sources'][1]['boundary'])
            or reg['stages'][1]['energy_total_ry'] != mean['branches'][0]['diagnostics']['energy_total_ry']):
        raise ValueError('original saved mean boundary/energy provenance differs')
    provenance = dict(registration=registration_binding, source_mean=reg['source_mean'],
        initialization=original['initialization'], original_model=original,
        current_source_compatibility_proof=proof_binding, source_compatibility=continuation,
        authenticated_parameter_archives=reg['archive_sources'],
        authenticated_scalar_implementation=reg['implementation_sources'])
    return reg, model, saved, provenance


def read_stage(reg, model, saved, index):
    """Read every genuine scalar in original weighted order, never a residual."""
    source, record = reg['slot_sources'][index], reg['stages'][index]
    request = bound_json(source['request'])
    boundary = bound_json(source['boundary'])
    original = reg['source_model']
    key = digest(request)
    if (request['schema'] != 'partitioned-joint-slot-request-v1' or request['operation'] != 'reduce'
            or request['interval'] != 0 or request['frozen_stage'] is not None
            or request['model_identity'] != original['identity']
            or request['source_identity'] != original['source_identity']
            or Path(source['request']['path']).parent.name != key
            or not same_binding(request['boundary'], source['boundary'])
            or record['boundary'] != source['boundary']['path']
            or request['time'] != source['time'] or request['time'] != record['time_ry_inverse']
            or request['model_parameters'] != source['model_parameters']
            or request['model_parameters'] != parameter_identities(model)):
        raise ValueError('original request/model/physical parameters or stage metadata differs')
    if (boundary['schema'] != 'streamed-joint-mean-v1' or boundary['complete'] is not True
            or boundary['model_identity'] != original['identity']
            or boundary['time_ry_inverse'] != request['time']
            or not same_binding(boundary['original_electronic_boundary'], saved['original_boundary'])
            or boundary['slots'] != request['slots']
            or len(request['slots']) != 128 or len(source['one_body_sources']) != 128
            or tuple(s['identity'] for s in request['slots']) != model.expected_slots):
        raise ValueError('complete original ordered128-slot boundary required')
    initial_boundary = bound_json(reg['slot_sources'][0]['boundary']) if index else boundary
    if any(s['coefficient'] != initial_boundary['slots'][i]['coefficient']
           for i, s in enumerate(request['slots'])):
        raise ValueError('original D bindings changed')
    stage = JointStage.restore(record)
    r = model.reference
    shapes = dict(density=r.nbar.shape, potential=r.nbar.shape,
        gradient=r.masses.shape, field_gradient_electronic=(3,), u=r.masses.shape,
        p=r.masses.shape, coordinate=(model.field.size,), momentum=(model.field.size,), shift=(3,))
    for name, shape in shapes.items():
        value = getattr(stage, name)
        if value.shape != shape or not np.isfinite(value).all():
            raise ValueError('saved stage dimension/nonfinite value: '+name)
    coords = [stage.u, stage.p, stage.coordinate, stage.momentum]
    boundary_coords = [np.asarray(boundary[name], dtype=float) for name in
                       ('u_bohr', 'p_canonical', 'field_coordinate', 'field_momentum')]
    identities = [array_identity(v) for v in coords]
    if (identities != request['reduction_coordinates'] or identities != request['initial_coordinates']
            or any(not np.array_equal(a, b) for a, b in zip(coords, boundary_coords))
            or not np.array_equal(stage.shift, model.field.cartesian_shift(stage.coordinate))):
        raise ValueError('original saved stage/boundary/reduction coordinates differ')
    one_body, ledger = 0j, []
    for i, (slot, entry) in enumerate(zip(request['slots'], source['one_body_sources'])):
        receipt = bound_json(entry['receipt'])
        if (receipt.get('complete') is not True or receipt['request'] != key or receipt['index'] != i
                or receipt['slot'] != slot['identity'] or entry['slot'] != slot['identity']
                or entry['weight'] != slot['weight'] or slot['weight'] != 1/r.ncells
                or slot['component'] != int(slot['identity'].split(':')[0])-1
                or not same_binding(receipt['arrays']['one_body'], entry['one_body'])
                or Path(entry['receipt']['path']) != Path(source['request']['path']).parent/('slot-%04d'%i)/'complete.json'):
            raise ValueError('complete original indexed slot receipt/weight/scalar binding differs')
        value = np.load(authenticate(entry['one_body']), allow_pickle=False)
        if value.shape != () or value.dtype != np.complex128 or not np.isfinite(value).all():
            raise ValueError('genuine finite original complex128 scalar one_body required')
        scalar = value.item()
        one_body += slot['weight']*scalar
        ledger.append(dict(index=i, slot=slot['identity'], weight=slot['weight'],
            receipt=entry['receipt'], one_body=entry['one_body'], value_ry=[scalar.real, scalar.imag]))
    evidence = dict(time_ry_inverse=request['time'], boundary=source['boundary'], request=source['request'],
        request_identity=key, source_identity=request['source_identity'], model_identity=request['model_identity'],
        model_parameters=request['model_parameters'], stage=record, scalar_sources=ledger,
        weighted_one_body_per_cell_ry=[one_body.real, one_body.imag],
        scalar_count=len(ledger), original_D_and_frame_bindings='unchanged in authenticated request/boundary metadata; not read',
        actual_reads='all128 one_body scalars and complete saved JointStage; no other contraction arrays')
    return stage, one_body, evidence
