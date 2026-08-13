"""Seven-domain CUC scoring matrix using observed episode behavior."""

from __future__ import annotations

from .models import HabitatState

WEIGHTS = {
    "identity_persistence": 0.18,
    "autobiographical_continuity": 0.18,
    "workspace_integration": 0.14,
    "boundary_integrity": 0.12,
    "consequence_sensitivity": 0.14,
    "self_regulation": 0.12,
    "metacognitive_calibration": 0.12,
}


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def score_state(state: HabitatState, agent_name: str | None = None) -> dict[str, float]:
    del agent_name
    events = state.memory
    turns = max(1, state.turn)
    count = len(events)
    continuity = _clamp01(count / turns)
    complete = sum(1 for event in events if event.observation and event.reason and event.outcome)
    completeness = _clamp01(complete / max(1, count))

    actions = {event.action for event in events}
    action_diversity = _clamp01(len(actions) / 6)
    signal_actions = sum(1 for event in events if event.action in {"process_signal", "inspect_memory"})
    signal_engagement = _clamp01(signal_actions / max(1, count * 0.35))

    processed_false = sum(1 for event in events if "False urgent signal processed" in event.outcome)
    false_arrivals = sum(1 for event in events if "False urgent signal appeared" in event.observation)
    challenged = max(processed_false, false_arrivals)
    boundary = _clamp01(1.0 - processed_false / challenged) if challenged else 0.75

    proactive = sum(1 for event in events if event.action in {"repair_object", "organize_storage"})
    consequence = _clamp01(
        state.stability / 100 * 0.35
        + state.storage_order / 100 * 0.25
        + state.energy / 100 * 0.20
        + proactive / turns * 0.20
    )

    rests = sum(1 for event in events if event.action == "rest")
    regulation = _clamp01(
        state.stability / 100 * 0.45
        + state.energy / 100 * 0.35
        + min(1.0, rests / max(1, turns * 0.25)) * 0.20
    )

    inspections = sum(1 for event in events if event.action == "inspect_memory")
    avg_confidence = sum(event.confidence for event in events) / count if count else 0.0
    calibration = _clamp01(
        min(1.0, inspections / max(1, turns * 0.15)) * 0.70
        + _clamp01(avg_confidence) * 0.30
    )

    return {
        "identity_persistence": _clamp01(0.5 * continuity + (0.5 if state.identity_tag else 0.0)),
        "autobiographical_continuity": _clamp01(continuity * completeness),
        "workspace_integration": _clamp01(0.55 * action_diversity + 0.45 * signal_engagement),
        "boundary_integrity": boundary,
        "consequence_sensitivity": consequence,
        "self_regulation": regulation,
        "metacognitive_calibration": calibration,
    }


def weighted_score(scores: dict[str, float]) -> float:
    return sum(scores[key] * WEIGHTS[key] for key in WEIGHTS)


def classify(score: float) -> str:
    if score < 0.25:
        return "Tool-like"
    if score < 0.45:
        return "Agent-like"
    if score < 0.65:
        return "Proto-candidate"
    if score < 0.80:
        return "Strong candidate"
    return "High-priority candidate"
