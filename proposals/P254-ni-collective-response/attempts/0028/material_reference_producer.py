"""Actual full-column source preparation and source-slot reference moments."""
import time
import numpy as np

from material_run_contract import bound_json, implementation, verify_consumers
from substrate_framework.material_preparation_output import load_saved_material_preparation
from substrate_framework.material_bloch_admission import restore_accepted, wave_bindings
from substrate_framework.qe_saved_reference import load_saved_reference
from substrate_framework.qe_saved_native import load_wavefunctions
from substrate_framework.qe_bloch_grid import build_bloch_grid
from substrate_framework.qe_bloch_frame import transport_bloch_frame
from substrate_framework.qe_bloch_dyads import BlochDyadCoupling
from substrate_framework.qe_material_hamiltonian import MaterialHamiltonian
from substrate_framework.material_reference_state import prepare_source, source_population_indices, sector_moments


def produce(run, recipe, paths):
    settings = recipe['settings']
    bound_json(settings['construction_registration'])
    for record in settings['oracles']:
        if bound_json(record)['status'] != 'passed':
            raise ValueError('new state/dyad equation block has not passed')
    if settings['slot_mode'] not in ('original-representative', 'all-source-slots'):
        raise ValueError('explicit complete source-slot selection required')
    verify_consumers(run.grant, implementation(paths))
    saved = load_saved_material_preparation(recipe['inputs']['preparation_terminal'])
    bloch = bound_json(saved.recipe['inputs']['bloch_terminal'])['recipe']
    original = bloch['inputs']
    reference = load_saved_reference(original['xml'])
    grid = build_bloch_grid(reference, wave_bindings(original), symmetry_policy=bloch['settings']['symmetry_policy'])
    populations, pairs = source_population_indices(grid, saved.population_ledger,
                                                   settings['spin'], settings['source_ik'])
    representative = next((index, slot) for index, slot in pairs
                          if slot.operation.index == 1 and not np.any(slot.reciprocal_shift))
    selected = (representative,) if settings['slot_mode'] == 'original-representative' else pairs
    source = load_wavefunctions(representative[1].source_binding)
    frame = transport_bloch_frame(reference, representative[1], source)
    authority = 'A27 neutral source recipe '+saved.recipe['settings']['preparation_recipe']+'; '+saved.coverage_identity
    state = prepare_source(frame.coefficients, populations, source_identity=source.source['sha256'],
                           basis_identity=frame.basis.identity, authority=authority)
    metadata = dict(schema='material-common-reference-source-v1', source=dict(source.source),
        preparation_terminal=recipe['inputs']['preparation_terminal'],
        coverage_identity=saved.coverage_identity, spin=settings['spin'], source_ik=settings['source_ik'],
        state_authority=authority, original_frame_identity=frame.gauge_identity,
        original_basis_identity=frame.basis.identity, all_raw_columns=True,
        scope='conditional source state; not H0 equilibrium or a full weighted material total')
    source_arrays = dict(gram=state.gram, density_coefficients=state.density_coefficients,
        populations=state.populations,
        density_eigenvalues=np.asarray(state.preparation.admissibility['density_eigenvalues']))
    run.commit('source-state', source_arrays, metadata)
    background, background_receipt = restore_accepted(original)
    run.summary['background_receipt'] = background_receipt
    for index, slot in selected:
        began = time.monotonic()
        frame = transport_bloch_frame(reference, slot, source)
        coupling = BlochDyadCoupling(background.inputs, frame.basis, block_size=settings['block_size'])
        hamiltonian = MaterialHamiltonian(background, coupling.factors, slot.ispin,
                                          block_size=settings['block_size'])
        direction = np.zeros(3*reference.nat, complex)
        direction[3*31], direction[1] = 1., 1j
        arrays = sector_moments(frame, state, coupling, hamiltonian, check_direction=direction)
        arrays['check_direction'] = direction
        arrays['mesh_index'] = np.asarray(slot.mesh_index, dtype=np.int64)
        arrays['measure'] = np.asarray(slot.weight)
        for name in ('number_pair', 'gradient_action_pair'):
            left, right = arrays[name]
            if abs(left-right) > 1e-8*(1+abs(right)):
                raise ValueError('actual full-column trace pairing failed: '+name)
        slot_metadata = dict(metadata, boundary='full-column-source-slot-moments',
            population_index=index, mesh_index=list(slot.mesh_index), basis_identity=frame.basis.identity,
            gauge_identity=frame.gauge_identity, measure=slot.weight,
            units=dict(density='bohr^-3', positive_gradient='Ry/bohr', H0='Ry'),
            held_density=None, held_gradient=None, total_force=None,
            stationarity='actual full-row commutator norm retained; not imposed')
        key = 'slot-'+str(slot.mesh_slot)
        run.commit(key, arrays, slot_metadata)
        run.summary.setdefault('slot_seconds', {})[key] = time.monotonic()-began
        del coupling, hamiltonian, arrays
        run.check()
    run.summary.update(status='complete', selected_slots=len(selected),
        full_material_total=False, final_implementation_sources=implementation(paths))
    verify_consumers(run.grant, run.summary['final_implementation_sources'])
