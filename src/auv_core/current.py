"""Current-field implementations in NED coordinates.

The module provides uniform and depth-shear currents. Samples are deterministic
and return fresh arrays; no wall-clock or random state is read.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ._validation import as_vector, finite_non_negative
from .contracts import FloatArray, UniformCurrent


@dataclass(frozen=True)
class DepthShearCurrent:
    """Linear current shear in NED coordinates, with z positive downwards."""

    reference_velocity_ned_mps: FloatArray
    shear_ned_per_m: FloatArray
    reference_depth_m: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "reference_velocity_ned_mps",
            as_vector(self.reference_velocity_ned_mps, 3, "reference_velocity_ned_mps"),
        )
        object.__setattr__(
            self, "shear_ned_per_m", as_vector(self.shear_ned_per_m, 3, "shear_ned_per_m")
        )
        if not np.isfinite(self.reference_depth_m):
            raise ValueError("reference_depth_m must be finite")

    def sample(self, position_ned_m: FloatArray, t_s: float) -> FloatArray:
        position = as_vector(position_ned_m, 3, "position_ned_m")
        finite_non_negative(t_s, "t_s")
        depth_offset = position[2] - self.reference_depth_m
        return (self.reference_velocity_ned_mps + self.shear_ned_per_m * depth_offset).copy()


__all__ = ["DepthShearCurrent", "UniformCurrent"]
