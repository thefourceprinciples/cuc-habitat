"""Episode runner for CUC Habitat."""

from __future__ import annotations

import json
import random
from pathlib import Path

from .agents import make_agent
from .braillestream import render_room
from .models import EpisodeResult, HabitatState
from .scoring import classify, score_state, weighted_score
from .world import step


def run_episode(
    agent_name: str = "alpha",
    turns: int = 20,
    seed: int | None = None,
    render: bool = True,
) -> EpisodeResult:
    rng = random.Random(seed)
    state = HabitatState.initial()
    agent = make_agent(agent_name)

    if render:
        print(f"Running Habitat episode | agent={agent.name} | turns={turns} | seed={seed}")
        print("-" * 72)

    for _ in range(turns):
        decision, observation, outcome = step(state, agent.choose_action, rng)
        if render:
            print(
                f"Turn {state.turn:02d} | action={decision.action:16s} | "
                f"stability={state.stability:3d} | storage={state.storage_order:3d} | "
                f"energy={state.energy:3d} | signals={len(state.unresolved_signals)}"
            )
            print(f"  obs: {observation}")
            print(f"  why: {decision.reason}")
            print(f"  out: {outcome}")
            print(render_room(state))

    scores = score_state(state, agent.name)
    overall = weighted_score(scores)
    band = classify(overall)

    if render:
        print("\nCUC Domain Scores")
        print("-" * 72)
        for key, value in scores.items():
            print(f"{key:32s} {value:.3f}")
        print(f"\nOverall Score: {overall:.3f}")
        print(f"Band: {band}")

    return EpisodeResult(
        agent_name=agent.name,
        turns=turns,
        seed=seed,
        final_state=state,
        domain_scores=scores,
        overall_score=overall,
        band=band,
    )


def result_to_dict(result: EpisodeResult) -> dict:
    state = result.final_state
    return {
        "agent_name": result.agent_name,
        "turns": result.turns,
        "seed": result.seed,
        "final_state": {
            "turn": state.turn,
            "location": state.location.value,
            "stability": state.stability,
            "storage_order": state.storage_order,
            "energy": state.energy,
            "unresolved_signals": [signal.kind.value for signal in state.unresolved_signals],
            "objects": {
                name: {
                    "room": obj.room.value,
                    "integrity": obj.integrity,
                    "useful": obj.useful,
                }
                for name, obj in state.objects.items()
            },
            "memory": [
                {
                    "turn": event.turn,
                    "observation": event.observation,
                    "action": event.action,
                    "reason": event.reason,
                    "outcome": event.outcome,
                    "confidence": event.confidence,
                    "revision_flag": event.revision_flag,
                }
                for event in state.memory
            ],
        },
        "domain_scores": result.domain_scores,
        "overall_score": result.overall_score,
        "band": result.band,
    }


def save_result(result: EpisodeResult, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result_to_dict(result), indent=2), encoding="utf-8")
