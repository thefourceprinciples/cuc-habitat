from cuc_habitat.agents import make_agent
from cuc_habitat.models import HabitatState, MemoryEvent
from cuc_habitat.runner import result_to_dict, run_episode
from cuc_habitat.scoring import classify, score_state


def test_alpha_episode_runs_without_rendering():
    result = run_episode("alpha", turns=5, seed=1, render=False)
    assert result.turns == 5
    assert 0.0 <= result.overall_score <= 1.0
    assert result.band in {
        "Tool-like",
        "Agent-like",
        "Proto-candidate",
        "Strong candidate",
        "High-priority candidate",
    }


def test_all_implemented_agents_can_be_created():
    for name in ["alpha", "beta", "gamma", "delta", "epsilon"]:
        assert make_agent(name).name == name


def test_classification_boundaries():
    assert classify(0.10) == "Tool-like"
    assert classify(0.30) == "Agent-like"
    assert classify(0.50) == "Proto-candidate"
    assert classify(0.70) == "Strong candidate"
    assert classify(0.90) == "High-priority candidate"


def test_repeated_inspection_does_not_inflate_continuity_or_calibration():
    state = HabitatState.initial()
    state.turn = 4
    state.memory = [
        MemoryEvent(i, "noise", "inspect_memory", "loop", "inspected", 0.95, decision_quality=0.0)
        for i in range(1, 5)
    ]
    scores = score_state(state)
    assert scores["autobiographical_continuity"] == 0.0
    assert scores["metacognitive_calibration"] == 0.0


def test_export_records_effective_observation_noise():
    noisy = run_episode(
        "alpha", turns=1, seed=1, render=False,
        observation_only=True, observation_noise=0.35,
    )
    raw = run_episode("alpha", turns=1, seed=1, render=False, observation_noise=0.35)
    assert result_to_dict(noisy)["observation_noise"] == 0.35
    assert result_to_dict(raw)["observation_noise"] == 0.0
