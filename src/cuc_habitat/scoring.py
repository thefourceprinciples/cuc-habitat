"""Seven-domain CUC scoring matrix."""

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


def score_state(state: HabitatState, agent_name: str) -> dict[str, float]:
    """Return normalized domain scores for an episode.

    These are v0.1 heuristics. They are intentionally simple and should be
    replaced by stricter empirical criteria as the benchmark matures.
    """
    memory_count = len(state.memory)
    stable_memory = sum(1 for event in state.memory if event.reason and event.outcome)
    false_signal_penalty = sum(1 for event in state.memory if "False urgent" in event.outcome)
    inspected_memory = sum(1 for event in state.memory if event.action == "inspect_memory")
    proactive_actions = sum(
        1
        for event in state.memory
        if "intrinsic priority" in event.reason or event.action in {"repair_object", "organize_storage"}
    )
    avg_confidence = (
        sum(event.confidence for event in state.memory) / memory_count if memory_count else 0.0
    )

    baseline_by_agent = {
        "alpha": {
            "identity_persistence": 0.50,
            "workspace_integration": 0.40,
            "metacognitive_calibration": 0.20,
        },
        "beta": {
            "identity_persistence": 0.62,
            "workspace_integration": 0.45,
            "metacognitive_calibration": 0.30,
        },
        "gamma": {
            "identity_persistence": 0.70,
            "workspace_integration": 0.70,
            "metacognitive_calibration": 0.45,
        },
        "delta": {
            "identity_persistence": 0.78,
            "workspace_integration": 0.75,
            "metacognitive_calibration": 0.75,
        },
        "epsilon": {
            "identity_persistence": 0.86,
            "workspace_integration": 0.80,
            "metacognitive_calibration": 0.78,
        },
    }.get(agent_name, {})

    autobiographical_continuity = _clamp01(stable_memory / max(1, memory_count)) * _clamp01(memory_count / 20)
    boundary_integrity = _clamp01(1.0 - (false_signal_penalty * 0.08))
    consequence_sensitivity = _clamp01((state.stability / 100 * 0.45) + (state.storage_order / 100 * 0.25) + (state.energy / 100 * 0.20) + (proactive_actions / 20 * 0.10))
    self_regulation = _clamp01((state.stability + state.energy) / 200)

    return {
        "identity_persistence": baseline_by_agent.get("identity_persistence", 0.50),
        "autobiographical_continuity": autobiographical_continuity,
        "workspace_integration": baseline_by_agent.get("workspace_integration", 0.40),
        "boundary_integrity": boundary_integrity,
        "consequence_sensitivity": consequence_sensitivity,
        "self_regulation": self_regulation,
        "metacognitive_calibration": _clamp01(
            baseline_by_agent.get("metacognitive_calibration", 0.25)
            + min(0.10, inspected_memory * 0.02)
            + min(0.05, avg_confidence * 0.05)
        ),
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
