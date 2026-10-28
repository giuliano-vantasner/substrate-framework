"""Produce complete selected-Gamma, state-independent force/number factors.

CLI: --admission JSON --output DIR [--context-only]. Common grant fields are
material_run_contract.admit's contract. inputs: xml binding, wavefunctions
{"1": binding, "2": binding}, ionic_terminal binding to immutable ORIGINAL0024.
settings: {"complete_grid_shape": [4,4,4], "normalization_authority": nonempty str}.
Fresh: resume=false,resume_identity=null and no existing factor archives.
Resume: resume=true,resume_identity=prior recipe_sha256; same inputs/settings/
sources, explicitly reduced remaining_seconds. Completed spin cache reuse is
not recovery of unfinished FFT/contractions, power-loss or Native history.
The grant also requires resume_receipts: {} for fresh execution, or a mapping
from completed spinN-functional keys to exact prior receipt {path,bytes,sha256}
bindings for resume. This invocation authority is outside the scientific recipe.
All input verification, source inventory, loading, grid setup, readback and
serialization are charged to the current grant, including cache-only runs.
Eight MiB of the output grant is reserved for receipt/summary/terminal metadata.
"""
import time
BOOT = time.monotonic()
import argparse
import json
import os
from pathlib import Path
import signal
import sys
import traceback
import uuid


def emit(target, summary, event, **fields):
    record = {'event': event, 'generation': '0025', 'run_id': summary['run_id'],
              'elapsed_seconds': time.monotonic()-BOOT, **fields}
    with (target/'telemetry.jsonl').open('a') as stream:
        stream.write(json.dumps(record, allow_nan=False, separators=(',', ':'))+'\n')
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps(record, allow_nan=False, separators=(',', ':')), flush=True)


def run_production(args, target, summary, grant, recipe, identity):
    from material_run_contract import (implementation, verify_consumers, bound_json, binding,
                                       commit_block, save_json)
    from material_factor_output import (load_original, spin_receipts, load_spin,
        factor_provenance, load_saved_functional)
    from substrate_framework.physical_factor_preparation import FactorFunctional
    from substrate_framework.material_observable_factors import gamma_probe_actions
    paths = (Path(__file__), Path(__file__).with_name('material_factor_output.py'))
    metadata_reserve = 8 << 20
    summary['output_metadata_reserve_bytes'] = metadata_reserve

    def budget():
        elapsed = time.monotonic()-BOOT
        if elapsed >= grant['remaining_seconds']:
            raise TimeoutError('explicit remaining cumulative allocation exhausted')
        if summary['first_useful_block_seconds'] is None and elapsed >= grant['first_block_seconds']:
            raise TimeoutError('no completed spin functional within first-block allowance')
        used = sum(p.stat().st_size for p in target.iterdir() if p.is_file())
        if used + metadata_reserve >= grant['output_max_bytes']:
            raise RuntimeError('output cap including metadata reserve exhausted; no automatic retry')

    def alarm(signum, frame):
        raise TimeoutError('first-useful/remaining deadline reached; only committed spins recoverable')

    def arm_deadline():
        deadline = grant['remaining_seconds']
        if summary['first_useful_block_seconds'] is None:
            deadline = min(deadline, grant['first_block_seconds'])
        budget()
        signal.setitimer(signal.ITIMER_REAL, max(0.001, deadline-(time.monotonic()-BOOT)))

    signal.signal(signal.SIGALRM, alarm)
    arm_deadline()
    if not grant['resume'] and any(target.glob('spin*-functional.*')):
        raise ValueError('fresh grant cannot overwrite or consume completed functional cache')
    admitted_receipts = grant['resume_receipts']
    if (not isinstance(admitted_receipts, dict)
            or not set(admitted_receipts) <= {'spin1-functional', 'spin2-functional'}
            or (not grant['resume'] and admitted_receipts)):
        raise ValueError('explicit completed-spin receipt bindings required for resume')
    setup_start = time.monotonic()
    ref, coordinates, terminal = load_original(grant['inputs'])
    summary['original_ionic_recipe'] = terminal['recipe']
    summary['original_ionic_recipe_sha256'] = terminal['recipe_sha256']
    summary['setup_seconds'] = time.monotonic()-setup_start
    budget()
    for spin in (1, 2):
        started = time.monotonic()
        receipts = spin_receipts(terminal, spin)
        provenance, grid = factor_provenance(grant['inputs'], grant['settings'], coordinates, terminal, spin, receipts)
        key = 'spin'+str(spin)+'-functional'
        receipt_path, archive_path = target/(key+'.json'), target/(key+'.npz')
        cached = grant['resume'] and (receipt_path.exists() or archive_path.exists())
        receipt = None
        if cached:
            if not receipt_path.exists() or not archive_path.exists():
                raise ValueError('incomplete atomic spin checkpoint; no unfinished-step recovery')
            if key not in admitted_receipts or Path(admitted_receipts[key]['path']).resolve() != receipt_path:
                raise ValueError('cached spin needs an explicitly admitted immutable receipt')
            receipt = bound_json(admitted_receipts[key])
            if receipt['metadata']['provenance'] != provenance:
                raise ValueError('completed spin provenance differs from current immutable recipe')
            functional = load_saved_functional(target, key, identity, receipt)
            if (functional.factor_identity != grant['inputs']['wavefunctions'][str(spin)]['sha256']
                    or functional.pw_basis_identity != grid.pw_basis_identity):
                raise ValueError('restored factor/source/PW identity mismatch')
        elif key in admitted_receipts:
            raise ValueError('admitted completed spin archive/receipt is missing')
        input_start = time.monotonic()
        wave, ionic = load_spin(grant['inputs'], ref, coordinates, terminal, spin, receipts, budget,
                               assemble=not cached)
        input_seconds = time.monotonic()-input_start
        calculation_seconds = 0.0
        if not cached:
            calculation_start = time.monotonic()
            probes = gamma_probe_actions(wave.coefficients, spin_one_based=spin,
                pw_basis_identity=grid.pw_basis_identity,
                source_authority='original0024 terminal sha256='+grant['inputs']['ionic_terminal']['sha256'],
                gpsi_h32_x=ionic[32], gpsi_ni1_x=ionic[1], number_grid=grid)
            del ionic
            budget()
            functional = FactorFunctional.from_actions(wave.coefficients, probes,
                factor_identity=grant['inputs']['wavefunctions'][str(spin)]['sha256'],
                pw_basis_identity=grid.pw_basis_identity)
            del probes
            calculation_seconds = time.monotonic()-calculation_start
            budget()
            arrays, metadata = functional.archive_payload()
            verify_consumers(grant, implementation(paths))
            receipt = commit_block(target, key, arrays,
                {'provenance': provenance, 'functional': metadata}, identity,
                grant['output_max_bytes']-metadata_reserve)
            del arrays
        del wave, functional
        # A committed but late checkpoint is retained, never reported as success.
        output = {'key': key, 'metadata': receipt['metadata'], 'receipt': receipt,
                  'receipt_binding': binding(receipt_path), 'archive': receipt['archive'],
                  'reuse': 'completed-spin-cache' if cached else 'new-complete-spin',
                  'input_readback_seconds': input_seconds, 'calculation_seconds': calculation_seconds,
                  'spin_elapsed_seconds': time.monotonic()-started}
        summary['outputs'].append(output)
        budget()
        if summary['first_useful_block_seconds'] is None:
            summary['first_useful_block_seconds'] = time.monotonic()-BOOT
            summary['first_useful_target_met'] = summary['first_useful_block_seconds'] <= 30
            arm_deadline()
        summary['elapsed_seconds'] = time.monotonic()-BOOT
        save_json(target/'summary.json', summary, rotate=True)
        emit(target, summary, 'useful_checkpoint', key=key, reuse=output['reuse'],
             receipt=output['receipt_binding'], archive=receipt['archive'])
    final_sources = implementation(paths)
    verify_consumers(grant, final_sources)
    summary['final_implementation_sources'] = final_sources
    budget()
    summary['status'] = 'complete'


def main():
    target, save_json = None, None
    summary = {'status': 'failed', 'generation': '0025', 'run_id': uuid.uuid4().hex,
               'outputs': [], 'first_useful_block_seconds': None, 'first_useful_target_seconds': 30,
               'scope': 'selected k=q=Gamma; separate spin1/spin2; NOT complete BvK',
               'state': None, 'D': None, 'density_coefficients': None, 'temperature': None,
               'ionic': None, 'cross': None, 'total': None,
               'recovery_boundary': 'completed spin functional only; no unfinished-step recovery',
               'time_accounting': 'BOOT through exit, including imports, source hashing, old input readback and setup'}
    code = 1
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--admission', required=True, type=Path)
        parser.add_argument('--output', required=True, type=Path)
        parser.add_argument('--context-only', action='store_true')
        args = parser.parse_args()
        target = args.output.resolve()
        target.mkdir(parents=True, exist_ok=True)
        def interrupted(signum, frame):
            raise InterruptedError('signal '+str(signum)+'; no automatic retries')
        for signum in (signal.SIGTERM, signal.SIGINT):
            signal.signal(signum, interrupted)
        from material_run_contract import (runtime_context, implementation, admit, binding,
                                           save_json as save_document)
        save_json = save_document
        import material_factor_output
        paths = (Path(__file__), Path(material_factor_output.__file__))
        context, sources = runtime_context(), implementation(paths)
        summary.update(context=context, implementation_sources=sources)
        context_path = target/('context-'+summary['run_id']+'.json')
        save_json(context_path, {'generation': '0025', 'run_id': summary['run_id'],
                                'context': context, 'implementation_sources': sources})
        emit(target, summary, 'material_factor_context', context=binding(context_path))
        grant, recipe, identity = admit(args.admission, 'physical-factors', sources, context, args.context_only)
        if args.context_only:
            summary['status'] = 'context-only'
        else:
            summary.update(recipe=recipe, recipe_sha256=identity, admission=binding(args.admission),
                           remaining_seconds_granted=grant['remaining_seconds'],
                           first_block_seconds_granted=grant['first_block_seconds'],
                           mode='explicit-resume' if grant['resume'] else 'new')
            run_production(args, target, summary, grant, recipe, identity)
        code = 0
    except BaseException as error:
        summary['status'] = 'failed'
        summary['failure'] = {'type': type(error).__name__, 'message': str(error),
                              'traceback': traceback.format_exc()}
        if isinstance(error, SystemExit):
            code = int(error.code or 0)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        summary.update(elapsed_seconds=time.monotonic()-BOOT, exit_code=code)
        if target is not None:
            terminal = target/('terminal-'+summary['run_id']+'.json')
            try:
                if save_json is None:
                    # Import failures still get a unique exclusive terminal receipt.
                    with terminal.open('x') as stream:
                        json.dump(summary, stream, allow_nan=False)
                        stream.write('\n')
                        stream.flush()
                        os.fsync(stream.fileno())
                else:
                    save_json(terminal, summary)
                    save_json(target/'summary.json', summary, rotate=True)
                emit(target, summary, 'terminal', status=summary['status'], exit_code=code, path=str(terminal))
            except BaseException as error:
                print(json.dumps({'event': 'terminal_write_failure', 'generation': '0025',
                    'run_id': summary['run_id'], 'error': repr(error)}), flush=True)
                code = 1
        else:
            print(json.dumps({'event': 'no_output_directory', 'generation': '0025',
                'run_id': summary['run_id'], 'exit_code': code}), flush=True)
    return code


if __name__ == '__main__':
    sys.exit(main())
