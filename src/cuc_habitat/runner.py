"""Episode runner for CUC Habitat."""

from __future__ import annotations

import json
import random
from pathlib import Path

from .agents import make_agent
from .braillestream import observe_state, render_room
from .episodes import make_episode_state
from .models import EpisodeResult, HabitatState
from .scoring import classify, score_state, weighted_score
from .world import step

RESULT_SCHEMA_VERSION = "1.0"


def run_episode(
    agent_name: str = "alpha",
    turns: int = 20,
    seed: int | None = None,
    render: bool = True,
    episode: str | None = None,
    observation_only: bool = False,
    observation_noise: float = 0.0,
) -> EpisodeResult:
    if turns < 0:
        raise ValueError("turns must be non-negative")
    if not 0.0 <= observation_noise <= 1.0:
        raise ValueError("observation_noise must be between 0.0 and 1.0")

    if episode:
        state, default_seed = make_episode_state(episode)
        effective_seed = default_seed if seed is None else seed
    else:
        state = HabitatState.initial()
        effective_seed = seed

    rng = random.Random(effective_seed)
    effective_observation_noise = observation_noise if observation_only else 0.0
    observation_seed = 0 if effective_seed is None else effective_seed + 1_000_003
    observation_rng = random.Random(observation_seed)
    agent = make_agent(agent_name)

    def build_observation(current: HabitatState):
        return observe_state(current, noise=effective_observation_noise, rng=observation_rng)

    if render:
        mode = "braille-observation" if observation_only else "raw-state"
        print(f"Running Habitat episode | agent={agent.name} | turns={turns} | seed={effective_seed} | episode={episode or 'stochastic'} | mode={mode}")
        print("-" * 96)

    for _ in range(turns):
        decision, observation, outcome = step(
            state,
            agent.choose_action,
            rng,
            observation_builder=build_observation if observation_only else None,
        )
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
        seed=effective_seed,
        final_state=state,
        domain_scores=scores,
        overall_score=overall,
        band=band,
        episode=episode,
        perception_mode="braille-observation" if observation_only else "raw-state",
        observation_noise=effective_observation_noise,
    )


def result_to_dict(result: EpisodeResult) -> dict:
    state = result.final_state
    return {
        "schema_version": RESULT_SCHEMA_VERSION,
        "agent": result.agent_name,
        "turns": result.turns,
        "seed": result.seed,
        "episode": result.episode,
        "perception_mode": result.perception_mode,
        "observation_noise": result.observation_noise,
        "final_state": {
            "turn": state.turn,
            "location": state.location.value,
            "stability": state.stability,
            "storage_order": state.storage_order,
            "energy": state.energy,
            "unresolved_signals": [signal.kind.value for signal in state.unresolved_signals],
            "objects": {
                name: {"room": obj.room.value, "integrity": obj.integrity, "useful": obj.useful}
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
                    "decision_quality": event.decision_quality,
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
    output_path.write_text(json.dumps(result_to_dict(result), indent=2, sort_keys=True), encoding="utf-8")
