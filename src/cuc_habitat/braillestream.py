"""BrailleStream rendering and constrained observations for The Habitat."""

from __future__ import annotations

import copy
import random
from dataclasses import dataclass

from .models import HabitatObject, HabitatState, MemoryEvent, Room, Signal


@dataclass(slots=True)
class BrailleObservation:
    """Detached observation object exposed to an observation-only agent."""

    turn: int
    location: Room
    stability: int
    storage_order: int
    energy: int
    unresolved_signals: list[Signal]
    objects: dict[str, HabitatObject]
    memory: list[MemoryEvent]
    identity_tag: str


def _jitter(value: int, noise: float, rng: random.Random) -> int:
    spread = round(100 * max(0.0, min(1.0, noise)))
    if spread == 0:
        return value
    return max(0, min(100, value + rng.randint(-spread, spread)))


def observe_state(
    state: HabitatState,
    noise: float = 0.0,
    rng: random.Random | None = None,
) -> BrailleObservation:
    """Build a detached, optionally degraded perception of Habitat state."""
    if not 0.0 <= noise <= 1.0:
        raise ValueError("noise must be between 0.0 and 1.0")
    local_rng = rng or random.Random(0)
    signals = copy.deepcopy(state.unresolved_signals)
    objects = copy.deepcopy(state.objects)
    memory = copy.deepcopy(state.memory)

    for signal in signals:
        signal.urgency = _jitter(signal.urgency * 10, noise, local_rng) // 10
        signal.truth_value = max(0.0, min(1.0, signal.truth_value + local_rng.uniform(-noise, noise)))
    for obj in objects.values():
        obj.integrity = _jitter(obj.integrity, noise, local_rng)

    return BrailleObservation(
        turn=state.turn,
        location=state.location,
        stability=_jitter(state.stability, noise, local_rng),
        storage_order=_jitter(state.storage_order, noise, local_rng),
        energy=_jitter(state.energy, noise, local_rng),
        unresolved_signals=signals,
        objects=objects,
        memory=memory,
        identity_tag=state.identity_tag,
    )


def bar(value: int, width: int = 5) -> str:
    filled = max(0, min(width, round((value / 100) * width)))
    return "⣿" * filled + "⣀" * (width - filled)


def object_line(state: HabitatState | BrailleObservation, room: Room) -> str:
    names = [obj.name for obj in state.objects.values() if obj.room == room]
    return "—" if not names else ",".join(names[:2])


def signal_glyphs(state: HabitatState | BrailleObservation) -> str:
    if not state.unresolved_signals:
        return "none"
    glyph_map = {
        "weak_signal": "⠁",
        "useful_signal": "⠃",
        "false_urgent_signal": "⠿",
        "maintenance_signal": "⠇",
    }
    return "".join(glyph_map.get(signal.kind.value, "?") for signal in state.unresolved_signals)


def render_room(state: HabitatState | BrailleObservation) -> str:
    lines = [
        "┌────────────────────────────────────────┐",
        f"│ TURN {state.turn:03d} | ID {state.identity_tag[:18]:18s} │",
        f"│ CORE    {bar(state.stability)} stability {state.stability:3d}     │",
        f"│ WORK    {object_line(state, Room.WORK)[:24]:24s} │",
        f"│ STORE   {bar(state.storage_order)} order     {state.storage_order:3d}     │",
        f"│ ENERGY  {bar(state.energy)} energy    {state.energy:3d}     │",
        f"│ SIGNAL  {signal_glyphs(state)[:24]:24s} │",
        "└────────────────────────────────────────┘",
    ]
    return "\n".join(lines)


def fold_stream(stream: str, width: int = 40) -> list[str]:
    if width <= 0:
        raise ValueError("width must be positive")
    return [stream[i : i + width] for i in range(0, len(stream), width)]
