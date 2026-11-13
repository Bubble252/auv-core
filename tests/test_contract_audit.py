from __future__ import annotations

from dataclasses import is_dataclass

import numpy as np

from auv_core import contracts, current, geometry, guidance
from auv_core.contracts import (
    ActuatorCommand,
    CurrentField,
    Remus100ActuatorCommand,
    UniformCurrent,
)
from auv_core.control import Remus100TrackingController
from auv_core.control import remus100 as remus100_module
from auv_core.current import DepthShearCurrent
from auv_core.guidance import ThreeDAlosGuidance
from auv_core.interfaces import (
    Guidance,
    SafetyFilter,
    SimulatorBackend,
    TrackingController,
)
from auv_core.scenarios import remus100_vehicle


def test_public_data_contracts_are_frozen_dataclasses() -> None:
    modules = (contracts, current, geometry, guidance, remus100_module)
    for module in modules:
        for value in vars(module).values():
            if not isinstance(value, type) or value.__module__ != module.__name__:
                continue
            if is_dataclass(value):
                assert value.__dataclass_params__.frozen, value.__name__


def test_boundary_protocols_are_runtime_checkable() -> None:
    protocols = (
        CurrentField,
        ActuatorCommand,
        Guidance,
        SafetyFilter,
        TrackingController,
        SimulatorBackend,
    )
    for protocol in protocols:
        assert getattr(protocol, "_is_runtime_protocol", False), protocol.__name__


def test_concrete_core_objects_satisfy_their_protocols() -> None:
    assert isinstance(
        UniformCurrent(velocity_ned_mps=np.zeros(3)),
        CurrentField,
    )
    assert isinstance(
        DepthShearCurrent(
            reference_velocity_ned_mps=np.zeros(3),
            shear_ned_per_m=np.zeros(3),
        ),
        CurrentField,
    )
    assert isinstance(
        Remus100ActuatorCommand(
            stamp_s=0.0,
            rudder_angle_rad=0.0,
            stern_plane_angle_rad=0.0,
            propeller_rpm=0.0,
        ),
        ActuatorCommand,
    )
    guidance_solver = ThreeDAlosGuidance(
        horizontal_lookahead_m=2.0,
        vertical_lookahead_m=2.0,
        speed_mps=1.0,
    )
    assert isinstance(guidance_solver, Guidance)
    controller = Remus100TrackingController(remus100_vehicle())
    assert isinstance(controller, TrackingController)
