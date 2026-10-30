#!/usr/bin/env python3
"""Real-file finite storage oracle; no Native/material simulation is launched.

Usage: python run_mixed_response_storage_oracle.py --output /path/report.json
The report is a verdict only after actual execution. Isolated tiny payloads,
sparse seeds and retained receipts live in a newly created work namespace next
to the output. A fresh Python subprocess performs the restart/resume portion.
No mocks, source-text checks or unchanged-hasher requalification are used.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT/'src'))

import mixed_response_storage as storage
from substrate_framework.partitioned_q_storage import QBudget, durable_publish, sync_file
from substrate_framework.streamed_material_state import file_binding


class Evidence:
    def __init__(self):
        self.checks = []

    def require(self, name, passed, **details):
        self.checks.append(dict(name=name, passed=bool(passed), **details))
        if not passed:
            raise AssertionError(name)

    def equal(self, name, actual, expected):
        actual, expected = np.asarray(actual), np.asarray(expected)
        defect = float(np.max(np.abs(actual-expected), initial=0))
        self.require(name, actual.shape == expected.shape and np.array_equal(actual, expected),
                     shape=list(actual.shape), max_abs_defect=defect)

    def refuses(self, name, function, exceptions=(ValueError, FileNotFoundError)):
        try:
            result = function()
        except exceptions as error:
            self.require(name, True, exception=type(error).__name__, message=str(error))
        else:
            if isinstance(result, storage.MappedMixedState):
                result.close()
            self.require(name, False, message='invalid storage transition was accepted')


def budget(existing=0):
    return QBudget(max_actions=100000, max_seconds=180,
                   max_bytes=256 << 20, max_memory_bytes=512 << 20,
                   worker_memory_bytes=512 << 20, existing_bytes=existing)


def small(q, offset=0):
    gamma = np.equal(q, np.rint(q)).all()
    result = {}
    for j, c in enumerate(storage.COMPONENTS):
        nf = 3 if gamma or c == 'mixed' else 0
        result[c] = dict(
            u=np.array([.125+offset+(j+1)*.375j, -.75+(j+2)*.0625j]),
            p=np.array([-.25+(j+1)*.5j, .375+offset-(j+1)*.125j]),
            coordinate=np.array([complex(.25*(j+1)+offset, -.125*(k+1))
                                 for k in range(nf)], dtype=np.complex128),
            momentum=np.array([complex(-.5*(k+1), .0625*(j+1)+offset)
                               for k in range(nf)], dtype=np.complex128))
    return result


def geometry(rows=(4, 6, 5), ranks=(2, 1, 3)):
    plus = (1, 2, 0)
    minus = (2, 0, 1)
    shapes = dict(
        plus=[(rows[plus[i]], ranks[i]) for i in range(3)],
        minus=[(rows[minus[i]], ranks[i]) for i in range(3)],
        mixed=list(zip(rows, ranks)))
    return shapes, plus, minus


def numerical_values(shapes, offset=0):
    result = {}
    for j, c in enumerate(storage.COMPONENTS):
        result[c] = []
        for i, shape in enumerate(shapes[c]):
            values = np.arange(np.prod(shape), dtype=float).reshape(shape)
            result[c].append(np.asarray((values+1+3*i+offset)/16
                                       + 1j*(values[::-1]+1+2*j+offset)/32,
                                       dtype=np.complex128))
    return result


def write_legs(directory, values, allocation):
    directory.mkdir(parents=True, exist_ok=False)
    return {c: [allocation.array(directory/f'{c}-{i:06d}.npy', a)
                for i, a in enumerate(values[c])] for c in storage.COMPONENTS}


def fixture(directory, allocation, *, offset=0, q=(1/3, 0., 0.)):
    shapes, plus, minus = geometry()
    values = numerical_values(shapes, offset)
    legs = write_legs(directory, values, allocation)
    coords = small(np.asarray(q), offset)
    checkpoint = storage.publish_checkpoint(directory/'checkpoint.json', legs=legs,
        small=coords, q=q, target_plus=plus, target_minus=minus, time=.125+offset/100,
        identity='finite-source-ordered-storage-model', kind='owned-rk-stage',
        provenance=dict(source='deterministic full rectangular finite arrays',
                        model='nonuniform source ranks and endpoint rows',
                        original_source_bindings=[file_binding(Path(__file__))]),
        budget=allocation)
    return checkpoint, values, coords, legs, shapes, plus, minus


def replacements(directory, values, allocation, index, offset=2):
    directory.mkdir(parents=True, exist_ok=False)
    result = {}
    for k, label in enumerate(('input', 'accumulator')):
        result[label] = {}
        for j, c in enumerate(storage.COMPONENTS):
            a = np.asarray((1+.125j*(k+1))*values[c][index]
                           +(offset+k+j)*(.125-.0625j), dtype=np.complex128)
            result[label][c] = allocation.array(directory/f'{label}-{c}.npy', a)
    return result


def arrays_to_pairs(values):
    return {c: [np.stack((a.real, a.imag), axis=-1).tolist() for a in values[c]]
            for c in storage.COMPONENTS}


def pairs_to_arrays(values):
    return {c: [np.asarray(a, dtype=float)[..., 0]+1j*np.asarray(a, dtype=float)[..., 1]
                for a in values[c]] for c in storage.COMPONENTS}


def observable(values, plus, minus):
    """Independent full-row Hermitian quadratic observable, not material energy.

    Distinct endpoint operators and original complex rank-one D coefficients
    make wrong source/target/rank relabeling numerically detectable. This does
    not use any storage helper to compute expected values.
    """
    rows = [a.shape[0] for a in values['mixed']]
    total = 0j
    for j, c in enumerate(('plus', 'minus', 'mixed')):
        for i, a in enumerate(values[c]):
            endpoint = plus[i] if c == 'plus' else minus[i] if c == 'minus' else i
            n = rows[endpoint]
            raw = np.arange(n*n, dtype=float).reshape(n, n)/31
            h = raw+raw.T+1j*(raw-raw.T)+np.diag(np.arange(n)+1)
            vector = (np.arange(a.shape[1])+1)+1j*np.arange(a.shape[1])[::-1]/4
            d = np.outer(vector, vector.conj())
            total += (j+1)*(i+1)*np.trace(d@(a.conj().T@h@a))
    return total


def child_resume(manifest, output):
    spec = json.loads(manifest.read_text())
    work = Path(spec['owner'])
    allocation = budget(sum(p.stat().st_size for p in work.rglob('*') if p.is_file()))
    evidence = Evidence()
    expected = pairs_to_arrays(spec['expected'])
    binding = spec['checkpoint']
    with storage.MappedMixedState(binding, budget=allocation) as state:
        evidence.refuses('fresh-process-retired-edge-does-not-become-zero',
                         lambda: state.leg('mixed', 0), (FileNotFoundError,))
        for i in (1, 2):
            for c in storage.COMPONENTS:
                evidence.equal(f'fresh-process-unaffected-{c}-{i}', state.leg(c, i), expected[c][i])
    receipt = storage.retire_edge(binding, 1, spec['barrier'], budget=allocation, owner_root=work)
    with storage.MappedMixedState(binding, budget=allocation) as state:
        for i in (0, 1):
            evidence.refuses(f'resumed-retired-edge-{i}-fails',
                             lambda i=i: state.leg('plus', i), (FileNotFoundError,))
        for c in storage.COMPONENTS:
            evidence.equal(f'resumed-preserves-final-edge-{c}', state.leg(c, 2), expected[c][2])
    report = dict(schema='P254-mixed-storage-reopen-subprocess-v1', status='pass',
                  pid=os.getpid(), checks=evidence.checks, receipt=receipt,
                  budget=allocation.snapshot())
    with output.open('x') as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write('\n')
    return report


def run(work, evidence):
    allocation = budget()
    checkpoint, expected, coords, legs, shapes, plus, minus = fixture(work/'stage', allocation)
    base = fixture(work/'caller-owned-base', allocation, offset=3)
    with storage.MappedMixedState(checkpoint, budget=allocation) as state:
        evidence.require('exact-original-binding-no-payload-copy',
            state.record['legs'] == legs and
            all(state.leg_binding(c, i) == legs[c][i] for c in storage.COMPONENTS for i in range(3)))
        evidence.require('independent-target-permutations-preserved',
                         state.target_plus == plus and state.target_minus == minus and plus != minus)
        evidence.require('time-kind-identity-provenance-preserved',
                         state.time == .125 and state.kind == 'owned-rk-stage'
                         and state.identity == 'finite-source-ordered-storage-model'
                         and bool(state.record['provenance']['original_source_bindings']))
        mapped = {c: [] for c in storage.COMPONENTS}
        for c in storage.COMPONENTS:
            for name, a in coords[c].items():
                evidence.equal(f'complex-small-lossless-{c}-{name}', getattr(state.small[c], name), a)
            for i in range(3):
                a = state.leg(c, i)
                evidence.require(f'actual-readonly-mmap-{c}-{i}', isinstance(a, np.memmap)
                                 and not a.flags.writeable and a.shape == shapes[c][i]
                                 and a.dtype == np.complex128)
                evidence.equal(f'actual-numerical-roundtrip-{c}-{i}', a, expected[c][i])
                mapped[c].append(a)
        actual_observable = observable(mapped, plus, minus)
        reference_observable = observable(expected, plus, minus)
        evidence.require('independent-full-row-complex-D-observable-roundtrip',
                         np.isclose(actual_observable, reference_observable, rtol=1e-14, atol=1e-12),
                         actual=[actual_observable.real, actual_observable.imag],
                         reference=[reference_observable.real, reference_observable.imag])
        evidence.refuses('source-negative-index-refused', lambda: state.leg('plus', -1), (IndexError,))
        evidence.refuses('readonly-mmap-write-refused',
                         lambda: state.leg('plus', 0).__setitem__((0, 0), 17), (ValueError,))
    evidence.refuses('closed-state-not-reusable', lambda: state.leg('mixed', 0), (ValueError,))
    evidence.require('publish-did-not-copy-npy-payloads',
                     len(list((work/'stage').glob('*.npy'))) == 9)

    # Real sparse seeds are deliberately larger than one filesystem block but
    # still tiny enough for exhaustive actual zero reads in an isolated oracle.
    zero_shapes, zp, zm = geometry(rows=(259, 383, 521), ranks=(9, 7, 11))
    before = allocation.snapshot()['live_bytes_reserved']
    zero = storage.create_zero_checkpoint(work/'sparse-zero', shapes=zero_shapes,
        small=small(np.array([1/3, 0., 0.])), q=[1/3, 0., 0.],
        target_plus=zp, target_minus=zm, time=0., identity='genuine-sparse-full-shapes',
        kind='caller-controlled-initial', provenance=dict(source='new genuine POSIX sparse zero NPY'),
        budget=allocation)
    logical = physical = 0
    with storage.MappedMixedState(zero, budget=allocation) as zeros:
        for c in storage.COMPONENTS:
            for i in range(3):
                a = zeros.leg(c, i)
                entry = zeros.leg_binding(c, i)
                stat = Path(entry['path']).stat()
                logical += stat.st_size
                physical += stat.st_blocks*512
                evidence.require(f'sparse-actual-original-shape-complex-zero-{c}-{i}',
                                 a.dtype == np.complex128 and a.shape == zero_shapes[c][i]
                                 and np.count_nonzero(a) == 0 and np.count_nonzero(a.imag) == 0,
                                 shape=list(a.shape), logical_bytes=stat.st_size,
                                 allocated_bytes=stat.st_blocks*512)
    after = allocation.snapshot()['live_bytes_reserved']
    evidence.require('sparse-growth-not-explicit-full-zero-write', physical < logical//4,
                     logical_bytes=logical, allocated_bytes=physical)
    evidence.require('sparse-seeds-charge-full-logical-QBudget', after-before >= logical,
                     reserved_increase=after-before, logical_payload_bytes=logical)

    gamma = fixture(work/'gamma', allocation, q=(0., 0., 0.))
    with storage.MappedMixedState(gamma[0]) as state:
        for c in storage.COMPONENTS:
            evidence.equal(f'Gamma-full-complex-field-{c}', state.small[c].coordinate,
                           gamma[2][c]['coordinate'])

    # Missing data without an authenticated exact retirement intent is not an
    # initial zero, a reused neighbor, or a restartable partial checkpoint.
    missing = fixture(work/'unexplained-missing', allocation)
    absent = Path(missing[3]['plus'][0]['path'])
    absent.rename(absent.with_suffix('.unavailable'))
    evidence.refuses('missing-payload-without-retirement-refused-on-open',
                     lambda: storage.MappedMixedState(missing[0]))

    changed = fixture(work/'changed-bound-input', allocation)
    edit = np.load(changed[3]['minus'][1]['path'], mmap_mode='r+', allow_pickle=False)
    edit[0, 0] += .5j
    edit.flush()
    edit._mmap.close()
    with storage.MappedMixedState(changed[0]) as state:
        evidence.equal('lazy-authentication-leaves-unmodified-input-usable',
                       state.leg('plus', 0), changed[1]['plus'][0])
        evidence.refuses('changed-bound-payload-refused-on-first-leg-read', lambda: state.leg('minus', 1))

    successor0 = replacements(work/'successor-0', expected, allocation, 0)
    successor1 = replacements(work/'successor-1', expected, allocation, 1)
    barrier0 = storage.publish_edge_barrier(work/'edge-0-successor.json', checkpoint=checkpoint,
        index=0, successors=successor0, budget=allocation)
    barrier1 = storage.publish_edge_barrier(work/'edge-1-successor.json', checkpoint=checkpoint,
        index=1, successors=successor1, budget=allocation)
    evidence.require('successor-publication-idempotent-exact-transition',
        storage.publish_edge_barrier(work/'edge-0-successor.json', checkpoint=checkpoint,
            index=0, successors=successor0, budget=allocation) == barrier0)
    plain = durable_publish(work/'not-a-successor.json', dict(complete=True), allocation)
    evidence.refuses('generic-durable-file-is-not-a-successor-barrier',
        lambda: storage.retire_edge(checkpoint, 0, plain, budget=allocation, owner_root=work))
    evidence.refuses('correct-successor-for-wrong-edge-refused',
        lambda: storage.retire_edge(checkpoint, 0, barrier1, budget=allocation, owner_root=work))
    evidence.refuses('barrier-for-unrelated-old-checkpoint-refused',
        lambda: storage.retire_edge(base[0], 0, barrier0, budget=allocation, owner_root=work))
    missing_barrier = dict(barrier0, path=str(work/'no-such-successor.json'))
    evidence.refuses('missing-successor-barrier-refused',
        lambda: storage.retire_edge(checkpoint, 0, missing_barrier, budget=allocation, owner_root=work))
    wrong_original = json.loads(Path(barrier0['path']).read_text())
    wrong_original['original_legs']['plus'] = legs['plus'][1]
    wrong_binding = durable_publish(work/'wrong-original-successor.json', wrong_original, allocation)
    evidence.refuses('barrier-must-cover-exact-original-payload-bindings',
        lambda: storage.retire_edge(checkpoint, 0, wrong_binding, budget=allocation, owner_root=work))
    wrong_owner = work/'not-the-owner'
    wrong_owner.mkdir()
    evidence.refuses('owner-boundary-refuses-unrelated-root',
        lambda: storage.retire_edge(checkpoint, 0, barrier0, budget=allocation, owner_root=wrong_owner))
    evidence.require('failed-transitions-preserve-all-old-data',
                     all(Path(b['path']).exists() for c in storage.COMPONENTS for b in legs[c]))

    before = allocation.snapshot()
    with storage.MappedMixedState(checkpoint) as mapped:
        unaffected = mapped.leg('plus', 2)
        mapped.leg('minus', 0)
        evidence.refuses('mapped-source-edge-must-be-released-before-retirement',
            lambda: storage.retire_edge(mapped, 0, barrier0, budget=allocation, owner_root=work))
        mapped.release_edge(0)
        receipt0 = storage.retire_edge(mapped, 0, barrier0, budget=allocation, owner_root=work)
        evidence.equal('other-source-view-survives-owned-edge-retirement',
                       unaffected, expected['plus'][2])
        evidence.refuses('released-retired-source-is-never-a-zero-fallback',
                         lambda: mapped.leg('minus', 0), (FileNotFoundError,))
    after = allocation.snapshot()
    retired_bytes = sum(legs[c][0]['bytes'] for c in storage.COMPONENTS)
    evidence.require('only-three-old-source-zero-legs-retired-post-successor',
        all(not Path(legs[c][0]['path']).exists() for c in storage.COMPONENTS)
        and all(Path(legs[c][i]['path']).exists() for c in storage.COMPONENTS for i in (1, 2))
        and Path(checkpoint['path']).exists() and Path(receipt0['path']).exists()
        and all(Path(b['path']).exists() for triple in successor0.values() for b in triple.values()))
    evidence.require('QBudget-credits-exact-actually-unlinked-bytes',
        after['retired_payload_bytes']-before['retired_payload_bytes'] == retired_bytes,
        credited=after['retired_payload_bytes']-before['retired_payload_bytes'],
        actual_old_payload_bytes=retired_bytes)
    before_replay = allocation.snapshot()
    replay = storage.retire_edge(checkpoint, 0, barrier0, budget=allocation, owner_root=work)
    after_replay = allocation.snapshot()
    evidence.require('edge-retirement-idempotent-no-second-credit', replay == receipt0
        and before_replay['retired_payload_bytes'] == after_replay['retired_payload_bytes']
        and before_replay['live_bytes_reserved'] == after_replay['live_bytes_reserved'])
    evidence.refuses('replay-with-wrong-barrier-refused',
        lambda: storage.retire_edge(checkpoint, 0, barrier1, budget=allocation, owner_root=work))
    with storage.MappedMixedState(checkpoint) as state:
        for c in storage.COMPONENTS:
            evidence.refuses(f'retired-{c}-read-fails-not-synthesized',
                             lambda c=c: state.leg(c, 0), (FileNotFoundError,))
            evidence.equal(f'partial-retirement-keeps-unaffected-{c}', state.leg(c, 2), expected[c][2])

    # Discovery of a missing leg is never sufficient: both exact original
    # retirement intent and its independently hash-bound successor must remain.
    receipt_path = Path(receipt0['path'])
    saved_receipt = receipt_path.with_name(receipt_path.name+'.retained-original')
    receipt_path.rename(saved_receipt)
    evidence.refuses('partially-retired-open-without-durable-receipt-refused',
                     lambda: storage.MappedMixedState(checkpoint))
    forged = json.loads(saved_receipt.read_text())
    forged['payloads'][0] = legs['plus'][1]
    durable_publish(receipt_path, forged, allocation)
    evidence.refuses('partially-retired-open-with-wrong-original-receipt-refused',
                     lambda: storage.MappedMixedState(checkpoint))
    receipt_path.rename(receipt_path.with_name(receipt_path.name+'.rejected-wrong-original'))
    saved_receipt.rename(receipt_path)
    barrier_path = Path(barrier0['path'])
    saved_barrier = barrier_path.with_name(barrier_path.name+'.retained-original')
    barrier_path.rename(saved_barrier)
    evidence.refuses('partially-retired-open-without-successor-barrier-refused',
                     lambda: storage.MappedMixedState(checkpoint))
    wrong_journal = json.loads(saved_barrier.read_text())
    wrong_journal['index'] = 2
    durable_publish(barrier_path, wrong_journal, allocation)
    evidence.refuses('partially-retired-open-with-changed-successor-barrier-refused',
                     lambda: storage.MappedMixedState(checkpoint))
    barrier_path.rename(barrier_path.with_name(barrier_path.name+'.rejected-wrong-successor'))
    saved_barrier.rename(barrier_path)

    # Real separate interpreter: recover the existing authenticated transition,
    # preserve remaining values, then continue retiring the next completed edge.
    manifest = work/'restart-manifest.json'
    manifest_binding = durable_publish(manifest, dict(checkpoint=checkpoint, owner=str(work),
        barrier=barrier1, expected=arrays_to_pairs(expected)), allocation)
    child_output = work/'restart-result.json'
    completed = subprocess.run([sys.executable, str(Path(__file__).resolve()),
        '--resume-manifest', str(manifest), '--output', str(child_output)],
        capture_output=True, text=True, timeout=90, check=False)
    evidence.require('fresh-process-reopen-and-resume-executed', completed.returncode == 0,
                     returncode=completed.returncode, stdout=completed.stdout, stderr=completed.stderr)
    child = json.loads(child_output.read_text())
    evidence.require('fresh-process-resume-passed', child['status'] == 'pass'
                     and child['pid'] != os.getpid() and all(c['passed'] for c in child['checks']),
                     subprocess_pid=child['pid'], child_report=file_binding(child_output),
                     restart_manifest=manifest_binding)
    evidence.require('fresh-process-retired-only-the-next-source',
        all(not Path(legs[c][i]['path']).exists() for c in storage.COMPONENTS for i in (0, 1))
        and all(Path(legs[c][2]['path']).exists() for c in storage.COMPONENTS))
    with storage.MappedMixedState(base[0]) as state:
        for c in storage.COMPONENTS:
            for i in range(3):
                evidence.equal(f'initial-base-lifetime-unchanged-{c}-{i}', state.leg(c, i), base[1][c][i])

    # Even a valid successor does not authorize shared aliases or externally
    # borrowed originals. These are separate fixtures, not the retired stage.
    shared = fixture(work/'shared-original', allocation)
    shared_successors = replacements(work/'shared-successors', shared[1], allocation, 0)
    shared_barrier = storage.publish_edge_barrier(work/'shared-barrier.json', checkpoint=shared[0],
        index=0, successors=shared_successors, budget=allocation)
    alias = work/'shared-alias.npy'
    os.link(shared[3]['mixed'][0]['path'], alias)
    evidence.refuses('hardlinked-shared-original-ownership-refused',
        lambda: storage.retire_edge(shared[0], 0, shared_barrier, budget=allocation, owner_root=work))
    evidence.require('ownership-refusal-preserves-all-shared-legs-and-alias',
        alias.exists() and all(Path(shared[3][c][0]['path']).exists() for c in storage.COMPONENTS))
    borrowed_root = work/'borrowed-metadata-owner'
    borrowed_root.mkdir()
    borrowed = storage.publish_checkpoint(borrowed_root/'checkpoint.json', legs=shared[3],
        small=shared[2], q=[1/3, 0., 0.], target_plus=shared[5], target_minus=shared[6],
        time=.125, identity='borrowed-originals', kind='borrowed',
        provenance=dict(source='original payloads outside metadata owner root'), budget=allocation)
    borrowed_barrier = storage.publish_edge_barrier(work/'borrowed-barrier.json', checkpoint=borrowed,
        index=0, successors=shared_successors, budget=allocation)
    evidence.refuses('borrowed-outside-owner-payloads-not-retirable',
        lambda: storage.retire_edge(borrowed, 0, borrowed_barrier,
                                   budget=allocation, owner_root=borrowed_root))

    mutated = fixture(work/'changed-successor-old', allocation)
    mutated_successors = replacements(work/'changed-successor-new', mutated[1], allocation, 0)
    mutated_barrier = storage.publish_edge_barrier(work/'changed-successor-barrier.json',
        checkpoint=mutated[0], index=0, successors=mutated_successors, budget=allocation)
    successor_path = mutated_successors['input']['mixed']['path']
    edit = np.load(successor_path, mmap_mode='r+', allow_pickle=False)
    edit[-1, -1] -= .75
    edit.flush()
    edit._mmap.close()
    sync_file(successor_path)
    evidence.refuses('changed-successor-prevents-any-old-retirement',
        lambda: storage.retire_edge(mutated[0], 0, mutated_barrier,
                                   budget=allocation, owner_root=work))
    evidence.require('changed-successor-refusal-leaves-all-old-legs',
        all(Path(mutated[3][c][0]['path']).exists() for c in storage.COMPONENTS))

    # Metadata admission preserves source rank/target rows and exact dtype.
    wrong_shapes = {c: list(v) for c, v in shapes.items()}
    wrong_shapes['plus'][0] = shapes['mixed'][0]
    evidence.refuses('sparse-seed-wrong-source-target-geometry-refused',
        lambda: storage.create_zero_checkpoint(work/'invalid-zero', shapes=wrong_shapes,
            small=coords, q=[1/3, 0., 0.], target_plus=plus, target_minus=minus,
            time=0., identity='invalid', kind='invalid', provenance=dict(source='invalid'), budget=allocation))
    dtype_dir = work/'wrong-dtype'
    dtype_dir.mkdir()
    real = allocation.array(dtype_dir/'real.npy', np.ones(shapes['plus'][0], dtype=float))
    wrong_legs = {c: list(v) for c, v in base[3].items()}
    wrong_legs['plus'][0] = real
    evidence.refuses('real-NPY-not-silently-cast-to-complex128',
        lambda: storage.publish_checkpoint(dtype_dir/'checkpoint.json', legs=wrong_legs,
            small=coords, q=[1/3, 0., 0.], target_plus=plus, target_minus=minus,
            time=0., identity='invalid', kind='invalid', provenance=dict(source='invalid'), budget=allocation))
    # The parent and subprocess have separate reservation ledgers; their
    # snapshots are not misrepresented as one shared accounting measurement.
    return dict(checkpoint=checkpoint, sparse_zero_checkpoint=zero,
                retirement_receipt=receipt0, restart_result=file_binding(child_output),
                parent_budget_snapshot_before_subprocess=after_replay,
                parent_final_ledger=allocation.snapshot(), child_budget=child['budget'],
                accounting='Parent and fresh subprocess ledgers are independent; child initializes existing logical bytes. No combined peak claimed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--resume-manifest', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(output)
    if args.resume_manifest is not None:
        child_resume(args.resume_manifest.resolve(), output)
        return 0
    work = Path(tempfile.mkdtemp(prefix=output.stem+'-files-', dir=output.parent)).resolve()
    evidence = Evidence()
    report = dict(schema='P254-mixed-response-storage-oracle-v1', status='failed',
                  material_result=False, scope='finite actual files and numeric storage only; no Native propagation',
                  started_utc=datetime.now(timezone.utc).isoformat(), work_directory=str(work),
                  source_bindings=[file_binding(Path(__file__)), file_binding(Path(storage.__file__)),
                                   file_binding(ROOT/'src/substrate_framework/partitioned_q_storage.py'),
                                   file_binding(ROOT/'src/substrate_framework/streamed_material_state.py')])
    try:
        report['results'] = run(work, evidence)
        report['status'] = 'pass'
    except Exception as error:
        report['error'] = dict(type=type(error).__name__, message=str(error), traceback=traceback.format_exc())
    report['checks'] = evidence.checks
    report['check_count'] = len(evidence.checks)
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    with output.open('x') as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(dict(status=report['status'], checks=len(evidence.checks), output=str(output)), sort_keys=True))
    return 0 if report['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
