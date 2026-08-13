"""Command line interface for CUC Habitat."""

from __future__ import annotations

import argparse

from .agents import AGENTS
from .episodes import episode_names
from .evaluator import evaluate_agents, format_evaluation, save_evaluation
from .runner import run_episode, save_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cuc-habitat", description="Run CUC Habitat benchmark episodes.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="run one Habitat episode")
    run.add_argument("--agent", choices=sorted(AGENTS), default="alpha")
    run.add_argument("--turns", type=int, default=20)
    run.add_argument("--seed", type=int, default=None)
    run.add_argument("--episode", choices=episode_names(), default=None)
    run.add_argument("--observation-only", action="store_true", help="act through a detached BrailleStream observation")
    run.add_argument("--observation-noise", type=float, default=0.0, help="perception degradation from 0.0 to 1.0")
    run.add_argument("--no-render", action="store_true", help="suppress turn-by-turn display")
    run.add_argument("--json-out", default=None, help="optional path to save episode result JSON")

    compare = subparsers.add_parser("compare", help="run all implemented agents with the same conditions")
    compare.add_argument("--turns", type=int, default=20)
    compare.add_argument("--seed", type=int, default=7)
    compare.add_argument("--episode", choices=episode_names(), default=None)

    evaluate = subparsers.add_parser("evaluate", help="run multi-seed evaluation reports")
    evaluate.add_argument("--agents", nargs="+", choices=sorted(AGENTS), default=sorted(AGENTS))
    evaluate.add_argument("--turns", type=int, default=20)
    evaluate.add_argument("--seeds", type=int, default=100)
    evaluate.add_argument("--episode", choices=episode_names(), default=None)
    evaluate.add_argument("--json-out", default=None, help="optional path to save evaluation JSON")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        result = run_episode(
            agent_name=args.agent,
            turns=args.turns,
            seed=args.seed,
            render=not args.no_render,
            episode=args.episode,
            observation_only=args.observation_only,
            observation_noise=args.observation_noise,
        )
        if args.json_out:
            save_result(result, args.json_out)
        return 0

    if args.command == "compare":
        print(f"Comparing agents | turns={args.turns} | seed={args.seed} | episode={args.episode or 'stochastic'}")
        print("-" * 72)
        for name in sorted(AGENTS):
            result = run_episode(name, args.turns, args.seed, render=False, episode=args.episode)
            print(f"{name:8s} score={result.overall_score:.3f} band={result.band}")
        return 0

    if args.command == "evaluate":
        report = evaluate_agents(args.agents, turns=args.turns, seeds=args.seeds, episode=args.episode)
        print(format_evaluation(report))
        if args.json_out:
            save_evaluation(report, args.json_out)
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
