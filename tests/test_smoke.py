from cuc_habitat.agents import make_agent
from cuc_habitat.runner import run_episode
from cuc_habitat.scoring import classify


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
