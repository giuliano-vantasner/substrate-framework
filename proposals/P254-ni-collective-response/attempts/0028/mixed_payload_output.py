"""Durable complex128 payloads without densely writing numerical zero states.

A computed all-zero result is stored as canonical +0 complex128 sparse bytes.
No nonzero value is rounded, thresholded or discarded. Logical bytes remain
charged even when POSIX holes avoid physical disk allocation.
"""
from io import BytesIO
import math
import os
from pathlib import Path

import numpy as np
from substrate_framework.partitioned_q_storage import sync_directory, sync_file
from substrate_framework.streamed_material_state import file_binding


def write_zero_payload(path, shape, budget):
    """Create a NEW genuine full-shape NPY zero, with original logical charge."""
    shape = tuple(shape)
    if (len(shape) != 2 or any(type(n) is not int or n < 1 for n in shape)):
        raise ValueError('positive full-row/source-column integer shape required')
    budget.check()
    header = BytesIO()
    np.lib.format.write_array_header_1_0(header, dict(
        descr=np.lib.format.dtype_to_descr(np.dtype(np.complex128)),
        fortran_order=False, shape=shape))
    raw = header.getvalue()
    if len(raw) > 512:
        raise ValueError('NPY header exceeds reservation allowance')
    budget.reserve(16*math.prod(shape)+512)
    path = Path(path)
    with path.open('xb') as stream:
        stream.write(raw)
        stream.truncate(len(raw)+16*math.prod(shape))
        stream.flush()
        os.fsync(stream.fileno())
    sync_directory(path.parent)
    return file_binding(path)


def write_payload(path, value, budget):
    """Publish actual finite complex128 values; exact zeros use sparse storage."""
    if (not isinstance(value, np.ndarray) or value.ndim != 2
            or min(value.shape) < 1 or value.dtype != np.complex128
            or not np.isfinite(value).all()):
        raise ValueError('actual finite full-row complex128 matrix required')
    if not np.any(value):
        return write_zero_payload(path, tuple(int(n) for n in value.shape), budget)
    binding = budget.array(Path(path), value)
    sync_file(binding['path'])
    sync_directory(Path(binding['path']).parent)
    return binding
