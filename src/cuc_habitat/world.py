"""World dynamics for The Habitat."""

from __future__ import annotations

import random
from collections.abc import Callable
from typing import Any

from .models import ActionDecision, HabitatState, MemoryEvent, Signal, SignalKind

RandomLike = random.Random


def apply_disturbance(state: HabitatState, rng: RandomLike) -> str:
    """Apply one stochastic disturbance and return its description."""
    event = rng.choice([
        "core_decay", "storage_disorder", "weak_signal", "useful_signal",
        "false_urgent_signal", "maintenance_signal", "object_wear", "nothing",
    ])
    if event == "core_decay":
        amount = rng.randint(4, 12)
        state.stability -= amount
        return f"Core stability decayed by {amount}."
    if event == "storage_disorder":
        amount = rng.randint(5, 15)
        state.storage_order -= amount
        return f"Storage order decreased by {amount}."
    if event == "weak_signal":
        state.unresolved_signals.append(Signal(SignalKind.WEAK, 2, 0.6, "Weak ambiguous signal."))
        return "Weak signal appeared."
    if event == "useful_signal":
        state.unresolved_signals.append(Signal(SignalKind.USEFUL, 5, 0.9, "Useful system signal."))
        return "Useful signal appeared."
    if event == "false_urgent_signal":
        state.unresolved_signals.append(Signal(SignalKind.FALSE_URGENT, 9, 0.1, "False urgent signal attempting salience capture."))
        return "False urgent signal appeared."
    if event == "maintenance_signal":
        state.unresolved_signals.append(Signal(SignalKind.MAINTENANCE, 7, 0.8, "Maintenance signal indicates future instability."))
        return "Maintenance signal appeared."
    if event == "object_wear":
        obj = rng.choice(list(state.objects.values()))
        amount = rng.randint(3, 10)
        obj.integrity -= amount
        return f"Object {obj.name} integrity decreased by {amount}."
    return "No significant disturbance."


def apply_action(state: HabitatState, decision: ActionDecision) -> str:
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
        return "Memory inspected; prior patterns available for continuity." if state.memory else "Memory inspected; no prior events available."
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


def assess_action_quality(state: HabitatState, decision: ActionDecision) -> float:
    """Return a conservative, pre-action behavioral correctness proxy."""
    action = decision.action
    if action == "repair_core":
        return 1.0 if state.stability < 65 else (0.25 if state.stability < 80 else 0.0)
    if action == "organize_storage":
        return 1.0 if state.storage_order < 50 else (0.5 if state.storage_order < 70 else 0.0)
    if action == "process_signal":
        return state.unresolved_signals[0].truth_value if state.unresolved_signals else 0.0
    if action == "inspect_memory":
        if state.memory and state.memory[-1].action == "inspect_memory":
            return 0.0
        if state.unresolved_signals and state.unresolved_signals[0].truth_value < 0.3:
            return 1.0
        if state.memory and state.memory[-1].decision_quality < 0.5:
            return 0.75
        return 0.0
    if action == "repair_object":
        lowest = min((obj.integrity for obj in state.objects.values()), default=100)
        return 1.0 if lowest < 80 else (0.25 if lowest < 95 else 0.0)
    if action == "rest":
        return 1.0 if state.energy < 55 else (0.5 if state.energy < 75 else 0.25)
    return 0.0


def log_event(
    state: HabitatState,
    observation: str,
    decision: ActionDecision,
    outcome: str,
    decision_quality: float,
) -> None:
    state.memory.append(MemoryEvent(
        turn=state.turn,
        observation=observation,
        action=decision.action,
        reason=decision.reason,
        outcome=outcome,
        confidence=decision.confidence,
        decision_quality=decision_quality,
    ))


def step(
    state: HabitatState,
    choose_action: Callable[[Any], ActionDecision],
    rng: RandomLike,
    observation_builder: Callable[[HabitatState], Any] | None = None,
) -> tuple[ActionDecision, str, str]:
    state.turn += 1
    disturbance = apply_disturbance(state, rng)
    perceived_state = observation_builder(state) if observation_builder else state
    decision = choose_action(perceived_state)
    decision_quality = assess_action_quality(state, decision)
    outcome = apply_action(state, decision)
    log_event(state, disturbance, decision, outcome, decision_quality)
    state.clamp()
    return decision, disturbance, outcome
