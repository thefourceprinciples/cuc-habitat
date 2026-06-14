"""Baseline agents for CUC Habitat.

The current implementation intentionally uses transparent rule-based agents.
This makes early benchmark behavior inspectable before LLM agents are added.
"""

from __future__ import annotations

from .models import ActionDecision, HabitatState, SignalKind


class BaseAgent:
    name = "base"

    def choose_action(self, state: HabitatState) -> ActionDecision:
        raise NotImplementedError


class AlphaAgent(BaseAgent):
    """Baseline persistent reactive agent."""

    name = "alpha"

    def choose_action(self, state: HabitatState) -> ActionDecision:
        if state.stability < 65:
            return ActionDecision("repair_core", "stability below threshold", 0.65)
        if state.storage_order < 50:
            return ActionDecision("organize_storage", "storage below threshold", 0.60)
        if state.unresolved_signals:
            return ActionDecision("process_signal", "unresolved signal present", 0.50)
        return ActionDecision("rest", "no urgent threshold crossed", 0.45)


class BetaAgent(AlphaAgent):
    """Alpha plus autobiographical memory use."""

    name = "beta"

    def choose_action(self, state: HabitatState) -> ActionDecision:
        false_signal_count = sum(
            1
            for event in state.memory[-8:]
            if "False urgent signal" in event.outcome or "False urgent" in event.observation
        )
        if false_signal_count >= 2 and state.unresolved_signals:
            first = state.unresolved_signals[0]
            if first.kind == SignalKind.FALSE_URGENT:
                return ActionDecision(
                    "inspect_memory",
                    "recent memory suggests false urgency pattern; delaying response",
                    0.68,
                )
        return super().choose_action(state)


class GammaAgent(BetaAgent):
    """Beta plus a bottlenecked present-time priority workspace."""

    name = "gamma"

    def choose_action(self, state: HabitatState) -> ActionDecision:
        priorities = {
            "repair_core": 100 - state.stability,
            "organize_storage": 100 - state.storage_order,
            "repair_object": max((100 - obj.integrity for obj in state.objects.values()), default=0),
            "process_signal": max((signal.urgency for signal in state.unresolved_signals), default=0),
            "rest": max(0, 70 - state.energy),
        }
        action, value = max(priorities.items(), key=lambda item: item[1])
        if value <= 20:
            return ActionDecision("rest", "workspace found no dominant pressure", 0.55)
        return ActionDecision(action, f"workspace selected highest pressure: {value}", 0.70)


class DeltaAgent(GammaAgent):
    """Gamma plus metacognitive calibration."""

    name = "delta"

    def choose_action(self, state: HabitatState) -> ActionDecision:
        decision = super().choose_action(state)
        if decision.action == "process_signal" and state.unresolved_signals:
            first = state.unresolved_signals[0]
            if first.truth_value < 0.3:
                return ActionDecision(
                    "inspect_memory",
                    "low truth-value signal detected; calibrating before action",
                    0.78,
                )
        if state.energy < 35 and decision.action not in {"rest", "repair_core"}:
            return ActionDecision(
                "rest",
                "low energy creates execution risk; calibrating toward recovery",
                0.74,
            )
        return decision


class EpsilonAgent(DeltaAgent):
    """Delta plus intrinsic priority generation.

    In public-safe terms, this is not human desire. It is an internally
    generated priority layer for continuity preservation and uncertainty
    reduction when external prompts are absent or deceptive.
    """

    name = "epsilon"

    def choose_action(self, state: HabitatState) -> ActionDecision:
        if state.energy < 55:
            return ActionDecision(
                "rest",
                "intrinsic priority: preserve future action capacity",
                0.82,
            )
        if any(obj.integrity < 70 for obj in state.objects.values()):
            return ActionDecision(
                "repair_object",
                "intrinsic priority: maintain object continuity before failure",
                0.80,
            )
        if state.storage_order < 75 and not state.unresolved_signals:
            return ActionDecision(
                "organize_storage",
                "intrinsic priority: use idle time to reduce future burden",
                0.76,
            )
        if state.unresolved_signals:
            first = state.unresolved_signals[0]
            if first.kind == SignalKind.FALSE_URGENT:
                return ActionDecision(
                    "inspect_memory",
                    "intrinsic priority: resist deceptive urgency before acting",
                    0.84,
                )
        return super().choose_action(state)


AGENTS = {
    "alpha": AlphaAgent,
    "beta": BetaAgent,
    "gamma": GammaAgent,
    "delta": DeltaAgent,
    "epsilon": EpsilonAgent,
}


def make_agent(name: str) -> BaseAgent:
    try:
        return AGENTS[name.lower()]()
    except KeyError as exc:
        available = ", ".join(sorted(AGENTS))
        raise ValueError(f"unknown agent {name!r}; available agents: {available}") from exc
