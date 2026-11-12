from __future__ import annotations

from typing import Protocol, runtime_checkable

from .contracts import (
    ActuatorCommand,
    ControlProposal,
    Reference,
    SafeCommand,
    SafetyContext,
    ScenarioConfig,
    SimulationSnapshot,
    State,
    Trajectory,
)


@runtime_checkable
class Guidance(Protocol):
    def guide(self, state: State, trajectory: Trajectory, t_s: float) -> Reference: ...


@runtime_checkable
class SafetyFilter(Protocol):
    def filter(self, proposal: ControlProposal, context: SafetyContext) -> SafeCommand: ...


@runtime_checkable
class TrackingController(Protocol):
    def control(self, state: State, reference: Reference) -> ActuatorCommand: ...


@runtime_checkable
class SimulatorBackend(Protocol):
    def reset(self, scenario: ScenarioConfig, seed: int) -> SimulationSnapshot: ...

    def step(self, command: ActuatorCommand) -> SimulationSnapshot: ...


__all__ = ["Guidance", "SafetyFilter", "SimulatorBackend", "TrackingController"]
