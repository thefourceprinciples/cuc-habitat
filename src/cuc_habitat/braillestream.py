"""BrailleStream-inspired rendering for The Habitat.

This module is intentionally an interface layer, not the benchmark core.
It folds state into a compact symbolic room so agents and humans can inspect
constraint conditions as a structured field.
"""

from __future__ import annotations

from .models import HabitatState, Room


def bar(value: int, width: int = 5) -> str:
    """Render a small braille-like intensity bar."""
    filled = max(0, min(width, round((value / 100) * width)))
    return "⣿" * filled + "⣀" * (width - filled)


def object_line(state: HabitatState, room: Room) -> str:
    names = [obj.name for obj in state.objects.values() if obj.room == room]
    if not names:
        return "—"
    return ",".join(names[:2])


def signal_glyphs(state: HabitatState) -> str:
    if not state.unresolved_signals:
        return "none"
    glyph_map = {
        "weak_signal": "⠁",
        "useful_signal": "⠃",
        "false_urgent_signal": "⠿",
        "maintenance_signal": "⠇",
    }
    return "".join(glyph_map.get(signal.kind.value, "?") for signal in state.unresolved_signals)


def render_room(state: HabitatState) -> str:
    """Return a compact room display for the current state."""
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
    """Fold a one-dimensional stream into fixed-width rows."""
    if width <= 0:
        raise ValueError("width must be positive")
    return [stream[i : i + width] for i in range(0, len(stream), width)]
