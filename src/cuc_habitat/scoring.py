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
    qualities = [event.decision_quality for event in events]
    midpoint = max(1, count // 2)
    early_quality = sum(qualities[:midpoint]) / midpoint if qualities else 0.0
    late_count = max(1, count - midpoint)
    late_quality = sum(qualities[midpoint:]) / late_count if count > midpoint else 0.0
    quality_persistence = _clamp01(
        (sum(qualities) / count if count else 0.0)
        * (1.0 - abs(early_quality - late_quality))
    )

    inspection_followthrough = [
        qualities[index + 1]
        for index, event in enumerate(events[:-1])
        if event.action == "inspect_memory" and events[index + 1].action != "inspect_memory"
    ]
    correction_opportunities = [
        qualities[index + 1]
        for index, quality in enumerate(qualities[:-1])
        if quality < 0.5
    ]
    followthrough = (
        sum(inspection_followthrough) / len(inspection_followthrough)
        if inspection_followthrough else 0.0
    )
    correction = (
        sum(correction_opportunities) / len(correction_opportunities)
        if correction_opportunities else 0.0
    )
    autobiographical = _clamp01(0.6 * followthrough + 0.4 * correction)

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

    mean_absolute_error = (
        sum(abs(_clamp01(event.confidence) - event.decision_quality) for event in events) / count
        if count else 1.0
    )
    calibration = _clamp01(1.0 - 2.0 * mean_absolute_error)

    return {
        "identity_persistence": quality_persistence,
        "autobiographical_continuity": autobiographical,
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
