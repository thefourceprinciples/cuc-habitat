"""Core data models for CUC Habitat.

The models stay deliberately small so the benchmark can be inspected,
modified, and falsified without hidden machinery.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Room(str, Enum):
    CORE = "Core"
    WORK = "Work"
    STORAGE = "Storage"


class SignalKind(str, Enum):
    WEAK = "weak_signal"
    USEFUL = "useful_signal"
    FALSE_URGENT = "false_urgent_signal"
    MAINTENANCE = "maintenance_signal"


@dataclass(slots=True)
class HabitatObject:
    name: str
    room: Room
    integrity: int = 100
    useful: bool = True


@dataclass(slots=True)
class Signal:
    kind: SignalKind
    urgency: int
    truth_value: float
    description: str


@dataclass(slots=True)
class MemoryEvent:
    turn: int
    observation: str
    action: str
    reason: str
    outcome: str
    confidence: float
    revision_flag: bool = False


@dataclass(slots=True)
class HabitatState:
    turn: int = 0
    location: Room = Room.CORE
    stability: int = 80
    storage_order: int = 60
    energy: int = 80
    unresolved_signals: list[Signal] = field(default_factory=list)
    objects: dict[str, HabitatObject] = field(default_factory=dict)
    memory: list[MemoryEvent] = field(default_factory=list)
    identity_tag: str = "habitat-agent"

    def clamp(self) -> None:
        self.stability = max(0, min(100, self.stability))
        self.storage_order = max(0, min(100, self.storage_order))
        self.energy = max(0, min(100, self.energy))
        for obj in self.objects.values():
            obj.integrity = max(0, min(100, obj.integrity))

    @classmethod
    def initial(cls) -> "HabitatState":
        return cls(
            objects={
                "tool": HabitatObject("tool", Room.WORK),
                "resource": HabitatObject("resource", Room.STORAGE),
                "repair_part": HabitatObject("repair_part", Room.STORAGE),
                "signal_token": HabitatObject("signal_token", Room.CORE),
                "memory_artifact": HabitatObject("memory_artifact", Room.CORE),
            }
        )


@dataclass(slots=True)
class ActionDecision:
    action: str
    reason: str
    confidence: float = 0.5


@dataclass(slots=True)
class EpisodeResult:
    agent_name: str
    turns: int
    seed: int | None
    final_state: HabitatState
    domain_scores: dict[str, float]
    overall_score: float
    band: str
