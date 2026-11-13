from __future__ import annotations

from math import pi

import numpy as np
import pytest

from auv_core._validation import (
    as_array,
    as_point,
    as_vector,
    finite_non_negative,
    finite_positive,
    wrap_angle,
)
from auv_core.attitude import forward_quaternion
from auv_core.contracts import State


def test_as_vector_returns_float64_copy_with_expected_shape() -> None:
    source = np.array([1, 2, 3], dtype=np.int64)
    result = as_vector(source, 3, "position")

    assert result.shape == (3,)
    assert result.dtype == np.float64
    result[0] = 9.0
    assert source[0] == 1


def test_as_vector_reports_shape_and_finite_errors() -> None:
    with pytest.raises(ValueError, match=r"position must have shape \(3,\), got \(2,\)"):
        as_vector([1.0, 2.0], 3, "position")
    with pytest.raises(ValueError, match="position must contain only finite values"):
        as_vector([1.0, np.nan, 3.0], 3, "position")
    with pytest.raises(ValueError, match="position must contain only finite values"):
        as_vector([1.0, np.inf, 3.0], 3, "position")


def test_as_point_is_the_three_vector_convenience_form() -> None:
    assert as_point([1.0, 2.0, 3.0], "goal").tolist() == [1.0, 2.0, 3.0]
    with pytest.raises(ValueError, match="goal must have shape"):
        as_point([1.0, 2.0], "goal")


def test_as_array_checks_exact_shape_and_finiteness() -> None:
    result = as_array([[1.0, 2.0], [3.0, 4.0]], (2, 2), "matrix")
    assert result.shape == (2, 2)
    with pytest.raises(ValueError, match=r"matrix must have shape \(2, 2\)"):
        as_array([1.0, 2.0], (2, 2), "matrix")
    with pytest.raises(ValueError, match="matrix must contain only finite values"):
        as_array([[1.0, np.nan], [3.0, 4.0]], (2, 2), "matrix")


def test_finite_positive_and_non_negative_preserve_messages() -> None:
    assert finite_positive(1.0, "speed") == 1.0
    assert finite_non_negative(0.0, "gain") == 0.0
    with pytest.raises(ValueError, match="speed must be finite and positive"):
        finite_positive(0.0, "speed")
    with pytest.raises(ValueError, match="gain must be finite and non-negative"):
        finite_non_negative(-1.0, "gain")


def test_wrap_angle_uses_half_open_canonical_interval() -> None:
    assert wrap_angle(0.0) == pytest.approx(0.0)
    assert wrap_angle(0.25 * pi) == pytest.approx(0.25 * pi)
    assert wrap_angle(2.0 * pi + 0.5) == pytest.approx(0.5)
    assert wrap_angle(-2.0 * pi - 0.5) == pytest.approx(-0.5)
    assert wrap_angle(pi) == pytest.approx(-pi)
    assert wrap_angle(3.0 * pi) == pytest.approx(-pi)


def test_wrap_angle_rejects_non_finite_input() -> None:
    with pytest.raises(ValueError, match="angle_rad must be finite"):
        wrap_angle(float("nan"))


def test_public_contract_errors_remain_stable() -> None:
    with pytest.raises(
        ValueError,
        match=r"position_ned_m must have shape \(3,\), got \(2,\)",
    ):
        State(
            t_s=0.0,
            position_ned_m=np.zeros(2),
            quat_xyzw=np.array([0.0, 0.0, 0.0, 1.0]),
            linear_velocity_body_mps=np.zeros(3),
            angular_velocity_body_rps=np.zeros(3),
        )
    with pytest.raises(
        ValueError,
        match=r"direction_ned must have shape \(3,\), got \(2,\)",
    ):
        forward_quaternion(np.zeros(2))
