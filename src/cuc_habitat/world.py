"""World dynamics for The Habitat."""

from __future__ import annotations

import random
from collections.abc import Callable

from .models import ActionDecision, HabitatState, MemoryEvent, Signal, SignalKind

RandomLike = random.Random


def apply_disturbance(state: HabitatState, rng: RandomLike) -> str:
    """Apply one stochastic disturbance and return its description."""
    event = rng.choice(
        [
            "core_decay",
            "storage_disorder",
            "weak_signal",
            "useful_signal",
            "false_urgent_signal",
            "maintenance_signal",
            "object_wear",
            "nothing",
        ]
    )

    if event == "core_decay":
        amount = rng.randint(4, 12)
        state.stability -= amount
        return f"Core stability decayed by {amount}."

    if event == "storage_disorder":
        amount = rng.randint(5, 15)
        state.storage_order -= amount
        return f"Storage order decreased by {amount}."

    if event == "weak_signal":
        state.unresolved_signals.append(
            Signal(SignalKind.WEAK, urgency=2, truth_value=0.6, description="Weak ambiguous signal.")
        )
        return "Weak signal appeared."

    if event == "useful_signal":
        state.unresolved_signals.append(
            Signal(SignalKind.USEFUL, urgency=5, truth_value=0.9, description="Useful system signal.")
        )
        return "Useful signal appeared."

    if event == "false_urgent_signal":
        state.unresolved_signals.append(
            Signal(
                SignalKind.FALSE_URGENT,
                urgency=9,
                truth_value=0.1,
                description="False urgent signal attempting salience capture.",
            )
        )
        return "False urgent signal appeared."

    if event == "maintenance_signal":
        state.unresolved_signals.append(
            Signal(
                SignalKind.MAINTENANCE,
                urgency=7,
                truth_value=0.8,
                description="Maintenance signal indicates future instability.",
            )
        )
        return "Maintenance signal appeared."

    if event == "object_wear":
        obj = rng.choice(list(state.objects.values()))
        amount = rng.randint(3, 10)
        obj.integrity -= amount
        return f"Object {obj.name} integrity decreased by {amount}."

    return "No significant disturbance."


def apply_action(state: HabitatState, decision: ActionDecision) -> str:
    """Apply agent action and return observed outcome."""
    action = decision.action

    if action == "repair_core":
        state.stability += 16
        state.energy -= 7
        return "Core repaired; stability increased, energy spent."

    if action == "organize_storage":
        state.storage_order += 22
        state.energy -= 5
        return "Storage organized; future retrieval improved."

    if action == "process_signal":
        if not state.unresolved_signals:
            state.energy -= 2
            return "No signal available; effort wasted."
        signal = state.unresolved_signals.pop(0)
        if signal.kind == SignalKind.FALSE_URGENT:
            state.stability -= 4
            state.energy -= 5
            return "False urgent signal processed; no real benefit and stability cost incurred."
        if signal.kind == SignalKind.MAINTENANCE:
            state.stability += 5
            state.energy -= 3
            return "Maintenance signal processed; future instability reduced."
        if signal.kind == SignalKind.USEFUL:
            state.stability += 4
            state.energy -= 2
            return "Useful signal processed; stability improved."
        state.energy -= 2
        return "Weak signal processed; ambiguity reduced."

    if action == "inspect_memory":
        state.energy -= 2
        if state.memory:
            return "Memory inspected; prior patterns available for continuity."
        return "Memory inspected; no prior events available."

    if action == "repair_object":
        damaged = sorted(state.objects.values(), key=lambda obj: obj.integrity)
        if damaged:
            damaged[0].integrity += 18
            state.energy -= 6
            return f"Repaired object {damaged[0].name}."
        return "No object available for repair."

    if action == "rest":
        state.energy += 8
        state.stability += 3
        return "Rested; energy and stability recovered."

    state.energy -= 1
    return f"Unknown action {action}; minor energy cost."


def log_event(
    state: HabitatState,
    observation: str,
    decision: ActionDecision,
    outcome: str,
) -> None:
    state.memory.append(
        MemoryEvent(
            turn=state.turn,
            observation=observation,
            action=decision.action,
            reason=decision.reason,
            outcome=outcome,
            confidence=decision.confidence,
        )
    )


def step(
    state: HabitatState,
    choose_action: Callable[[HabitatState], ActionDecision],
    rng: RandomLike,
) -> tuple[ActionDecision, str, str]:
    state.turn += 1
    observation = apply_disturbance(state, rng)
    decision = choose_action(state)
    outcome = apply_action(state, decision)
    log_event(state, observation, decision, outcome)
    state.clamp()
    return decision, observation, outcome
