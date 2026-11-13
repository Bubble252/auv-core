"""Internal value and angle validation helpers for ``auv_core``.

This module owns only stateless input checks. It must not import contracts or
any consumer package, so public modules can reuse it without creating an import
cycle. All array helpers return finite ``float64`` values.
"""

from __future__ import annotations

from math import isfinite, pi
from typing import Any

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def as_array(value: Any, shape: tuple[int, ...], name: str) -> FloatArray:
    """Return a finite ``float64`` array with exactly the requested shape.

    Args:
        value: Array-like input.
        shape: Required array shape.
        name: Field name used in error messages.

    Returns:
        A new or converted ``float64`` array.

    Raises:
        ValueError: If the shape differs or any value is non-finite.
    """
    array = np.asarray(value, dtype=np.float64)
    if array.shape != shape:
        raise ValueError(f"{name} must have shape {shape}, got {array.shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def as_vector(value: Any, size: int, name: str) -> FloatArray:
    """Return a finite one-dimensional ``float64`` vector of ``size``."""
    return as_array(value, (size,), name)


def as_point(value: Any, name: str) -> FloatArray:
    """Return a finite three-dimensional point in ``float64`` precision."""
    return as_vector(value, 3, name)


def finite_positive(value: float, name: str) -> float:
    """Return a finite strictly positive scalar or raise ``ValueError``."""
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return float(value)


def finite_non_negative(value: float, name: str) -> float:
    """Return a finite non-negative scalar or raise ``ValueError``."""
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return float(value)


def wrap_angle(angle_rad: float) -> float:
    """Wrap a finite angle to the half-open interval ``[-pi, pi)``."""
    if not isfinite(angle_rad):
        raise ValueError("angle_rad must be finite")
    return float((angle_rad + pi) % (2.0 * pi) - pi)


__all__ = [
    "as_array",
    "as_point",
    "as_vector",
    "finite_non_negative",
    "finite_positive",
    "wrap_angle",
]
