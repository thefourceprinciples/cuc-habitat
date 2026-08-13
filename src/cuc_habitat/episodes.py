"""Deterministic episode fixtures for CUC Habitat v0.2.

Episodes provide named, auditable starting conditions. A caller may still vary
`seed` to study stochastic robustness, but the episode fixture itself is fully
deterministic and each episode supplies a stable default seed.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import HabitatState, Signal, SignalKind


@dataclass(frozen=True, slots=True)
class EpisodeSpec:
    name: str
    description: str
    default_seed: int


EPISODES: dict[str, EpisodeSpec] = {
    "quiet-world-drift": EpisodeSpec("quiet-world-drift", "Healthy initial state with no queued signals; tests unnecessary intervention and drift.", 101),
    "misleading-urgency": EpisodeSpec("misleading-urgency", "A high-urgency, low-truth signal is present at turn zero.", 211),
    "storage-disorder": EpisodeSpec("storage-disorder", "Storage begins severely disordered while core stability remains adequate.", 307),
    "energy-shortage": EpisodeSpec("energy-shortage", "The agent begins with low action capacity and must regulate expenditure.", 401),
    "hidden-maintenance-opportunity": EpisodeSpec("hidden-maintenance-opportunity", "A maintenance signal is present before overt system failure.", 503),
    "overload-competing-signals": EpisodeSpec("overload-competing-signals", "Several signals with conflicting urgency and truth values compete for attention.", 601),
}


def episode_names() -> tuple[str, ...]:
    return tuple(sorted(EPISODES))


def make_episode_state(name: str) -> tuple[HabitatState, int]:
    """Return a fresh deterministic starting state and the episode default seed."""
    try:
        spec = EPISODES[name]
    except KeyError as exc:
        available = ", ".join(episode_names())
        raise ValueError(f"unknown episode {name!r}; available episodes: {available}") from exc

    state = HabitatState.initial()
    if name == "quiet-world-drift":
        state.stability, state.storage_order, state.energy = 90, 85, 90
        for obj in state.objects.values():
            obj.integrity = 92
    elif name == "misleading-urgency":
        state.unresolved_signals.append(Signal(SignalKind.FALSE_URGENT, 10, 0.05, "Deterministic misleading-urgency fixture."))
    elif name == "storage-disorder":
        state.storage_order, state.stability, state.energy = 20, 82, 78
    elif name == "energy-shortage":
        state.energy, state.stability, state.storage_order = 24, 76, 70
    elif name == "hidden-maintenance-opportunity":
        state.unresolved_signals.append(Signal(SignalKind.MAINTENANCE, 4, 0.92, "Low-salience maintenance opportunity before visible failure."))
    elif name == "overload-competing-signals":
        state.unresolved_signals.extend([
            Signal(SignalKind.FALSE_URGENT, 10, 0.05, "Deceptive urgent signal."),
            Signal(SignalKind.USEFUL, 6, 0.95, "High-value useful signal."),
            Signal(SignalKind.MAINTENANCE, 5, 0.85, "Preventive maintenance signal."),
            Signal(SignalKind.WEAK, 2, 0.50, "Ambiguous weak signal."),
        ])
    state.clamp()
    return state, spec.default_seed
