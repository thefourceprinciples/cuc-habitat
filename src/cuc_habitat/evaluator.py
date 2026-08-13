"""Repeatable multi-seed reporting for CUC Habitat."""

from __future__ import annotations

import json
import math
import statistics
from collections import Counter
from pathlib import Path

from .runner import run_episode

SCHEMA_VERSION = "1.0"


def evaluate_agents(agent_names: list[str], turns: int = 20, seeds: int = 100, episode: str | None = None) -> dict:
    if seeds < 1:
        raise ValueError("seeds must be at least 1")
    report = {"schema_version": SCHEMA_VERSION, "turns": turns, "seed_count": seeds, "episode": episode, "agents": {}}
    for name in agent_names:
        runs = [run_episode(name, turns=turns, seed=seed, render=False, episode=episode) for seed in range(seeds)]
        scores = sorted(run.overall_score for run in runs)
        worst_n = max(1, math.ceil(len(scores) * 0.10))
        bands = Counter(run.band for run in runs)
        report["agents"][name] = {
            "mean": statistics.fmean(scores),
            "variance": statistics.pvariance(scores) if len(scores) > 1 else 0.0,
            "worst_decile_mean": statistics.fmean(scores[:worst_n]),
            "min": scores[0],
            "max": scores[-1],
            "band_distribution": dict(sorted(bands.items())),
        }
    return report


def format_evaluation(report: dict) -> str:
    lines = [
        f"CUC Habitat evaluation | turns={report['turns']} | seeds={report['seed_count']} | episode={report['episode'] or 'stochastic'}",
        "agent      mean    variance  worst10      min      max",
    ]
    for name, m in report["agents"].items():
        lines.append(f"{name:10s} {m['mean']:7.3f} {m['variance']:10.5f} {m['worst_decile_mean']:8.3f} {m['min']:8.3f} {m['max']:8.3f}")
    return "\n".join(lines)


def save_evaluation(report: dict, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
