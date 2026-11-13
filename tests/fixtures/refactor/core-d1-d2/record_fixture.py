"""Record deterministic public behavior for CORE-D1/D2 equivalence checks."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from auv_core.attitude import (
    euler_from_quaternion,
    forward_quaternion,
    quaternion_from_euler,
)
from auv_core.contracts import Reference, State, Trajectory
from auv_core.control import Remus100TrackingController
from auv_core.current import DepthShearCurrent
from auv_core.guidance import ThreeDAlosGuidance
from auv_core.scenarios import remus100_vehicle


def _state() -> State:
    return State(
        t_s=0.0,
        position_ned_m=np.array([1.0, 0.0, 0.0]),
        quat_xyzw=np.array([0.0, 0.0, 0.0, 1.0]),
        linear_velocity_body_mps=np.zeros(3),
        angular_velocity_body_rps=np.zeros(3),
    )


def _trajectory() -> Trajectory:
    points = np.array([[0.0, 0.0, 0.0], [5.0, 0.0, 0.0]])
    quats = np.tile(np.array([0.0, 0.0, 0.0, 1.0]), (2, 1))
    return Trajectory(
        trajectory_id="core-d1-d2",
        t_s=np.array([0.0, 1.0]),
        position_ned_m=points,
        quat_xyzw=quats,
        linear_velocity_body_mps=np.zeros((2, 3)),
        angular_velocity_body_rps=np.zeros((2, 3)),
    )


def _capture_errors() -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []

    def capture(case: str, function: Callable[[], object]) -> None:
        try:
            function()
        except Exception as exc:  # noqa: BLE001 - fixture records exact exception text.
            errors.append(
                {
                    "case": case,
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            )

    capture(
        "state.bad-shape",
        lambda: State(
            t_s=0.0,
            position_ned_m=np.zeros(2),
            quat_xyzw=np.array([0.0, 0.0, 0.0, 1.0]),
            linear_velocity_body_mps=np.zeros(3),
            angular_velocity_body_rps=np.zeros(3),
        ),
    )
    capture("attitude.bad-shape", lambda: forward_quaternion(np.zeros(2)))
    capture(
        "current.bad-shape",
        lambda: DepthShearCurrent(
            reference_velocity_ned_mps=np.zeros(2),
            shear_ned_per_m=np.zeros(3),
        ),
    )
    capture(
        "guidance.bad-gain",
        lambda: ThreeDAlosGuidance(
            horizontal_lookahead_m=2.0,
            vertical_lookahead_m=2.0,
            speed_mps=1.0,
            lookahead_error_gain=-1.0,
        ),
    )
    capture(
        "control.bad-step",
        lambda: Remus100TrackingController(remus100_vehicle(), nominal_step_s=0.0),
    )
    return errors


def record() -> dict[str, Any]:
    quat = quaternion_from_euler(0.1, -0.2, 0.3)
    euler = euler_from_quaternion(quat)
    current = DepthShearCurrent(
        reference_velocity_ned_mps=np.array([1.0, 0.0, 0.0]),
        shear_ned_per_m=np.array([0.1, -0.02, 0.0]),
    )
    guidance = ThreeDAlosGuidance(
        horizontal_lookahead_m=2.0,
        vertical_lookahead_m=2.0,
        speed_mps=1.0,
        lookahead_error_gain=0.0,
    )
    solution = guidance.solve(_state(), _trajectory(), 0.0)
    controller = Remus100TrackingController(remus100_vehicle())
    command = controller.control(
        State(
            t_s=0.02,
            position_ned_m=np.zeros(3),
            quat_xyzw=np.array([0.0, 0.0, 0.0, 1.0]),
            linear_velocity_body_mps=np.array([1.2, 0.0, 0.0]),
            angular_velocity_body_rps=np.zeros(3),
        ),
        Reference(
            stamp_s=0.0,
            position_ned_m=np.zeros(3),
            quat_xyzw=np.array([0.0, 0.0, 0.0, 1.0]),
            linear_velocity_body_mps=np.array([1.2, 0.0, 0.0]),
            angular_velocity_body_rps=np.zeros(3),
        ),
    )
    return {
        "randomized": False,
        "inputs": {
            "euler_rad": [0.1, -0.2, 0.3],
            "current_depth_m": 10.0,
            "state_position_ned_m": [1.0, 0.0, 0.0],
        },
        "outputs": {
            "forward_quaternion": forward_quaternion(np.array([1.0, 2.0, 3.0])).tolist(),
            "quaternion_from_euler": quat.tolist(),
            "euler_from_quaternion": euler.tolist(),
            "depth_shear": current.sample(np.array([0.0, 0.0, 10.0]), 0.0).tolist(),
            "guidance": {
                "horizontal_error_m": solution.horizontal_error_m,
                "vertical_error_m": solution.vertical_error_m,
                "desired_heading_rad": solution.desired_heading_rad,
                "desired_pitch_rad": solution.desired_pitch_rad,
                "reference_position_ned_m": solution.reference.position_ned_m.tolist(),
                "reference_quat_xyzw": solution.reference.quat_xyzw.tolist(),
            },
            "control": {
                "rudder_angle_rad": command.rudder_angle_rad,
                "stern_plane_angle_rad": command.stern_plane_angle_rad,
                "propeller_rpm": command.propeller_rpm,
            },
        },
        "exception": _capture_errors(),
        "manifest": {
            "case": "core-d1-d2",
            "units": "si",
            "frames": {"position": "NED", "body": "FRD", "quaternion": "xyzw"},
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(
        json.dumps(record(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
