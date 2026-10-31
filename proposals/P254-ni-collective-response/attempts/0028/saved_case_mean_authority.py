"""Restore an original matched mean state under the existing execution proof.

The complete saved scalar/preparation remains the authority. Only the already
proved history-owner implementation substitution is allowed. This authenticates
metadata and parameter arrays; it neither rereads every raw column nor performs
an electronic contraction or trajectory. Historical mean CLI bytes remain intact
while the live saved-energy consumer still authenticates them.
"""
import numpy as np

from matched_joint_case import load_case
from matched_joint_state import preparation_arrays
from run_joint_q_material import admit_oracle, bindings, bind_saved_model
from substrate_framework.material_control_reference import bound_arrays, bound_json
from substrate_framework.streamed_joint_state import DiskJointMean
from substrate_framework.streamed_material_state import authenticate


def restore_saved_case(case, initialization_binding, qualification_binding, *,
                       reality_tolerance=1e-10):
    initialization = bound_json(initialization_binding)
    if (initialization.get('schema') != 'P254-matched-joint-case-v1'
            or initialization.get('status') != 'complete'
            or initialization.get('mode') != 'initialize'
            or initialization.get('case') != case
            or initialization.get('saved', {}).get('case') != case):
        raise ValueError('complete initialization of the selected original case required')
    qualification = bound_json(qualification_binding)
    admit_oracle(qualification, bindings())
    saved = initialization['saved']
    current = load_case(case, reality_tolerance=reality_tolerance)
    context = bind_saved_model(current, saved, qualification.get('source_compatibility'))
    initial = DiskJointMean(authenticate(saved['joint_boundary']),
                            expected_identity=context.identity)
    if initial.time != 0 or initial.origin != saved['original_boundary']:
        raise ValueError('original case mean boundary/preparation differs')
    actual, expected = bound_arrays(saved['preparation']), preparation_arrays(context)
    if (set(actual) != set(expected)
            or any(not np.array_equal(actual[name], expected[name]) for name in expected)):
        raise ValueError('original case ionic/field product preparation differs')
    provenance = dict(initialization=dict(initialization_binding),
        current_execution_proof=dict(qualification_binding),
        source_compatibility=qualification.get('source_compatibility'),
        original_model_identity=saved['model_identity'],
        original_specification=saved['specification'],
        current_constructor_implementation=current.specification['implementation'],
        initial_boundary=saved['joint_boundary'], original_electronic_boundary=initial.origin,
        preparation=saved['preparation'],
        scope='Original model and exact saved parameter/preparation arrays; no new raw-column readback, physical contraction, coupled trajectory or control-case Native probe claim')
    return context, initial, provenance
