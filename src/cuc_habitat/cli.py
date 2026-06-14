"""Command line interface for CUC Habitat."""

from __future__ import annotations

import argparse

from .agents import AGENTS
from .runner import run_episode, save_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cuc-habitat",
        description="Run CUC Habitat benchmark episodes.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="run one Habitat episode")
    run.add_argument("--agent", choices=sorted(AGENTS), default="alpha")
    run.add_argument("--turns", type=int, default=20)
    run.add_argument("--seed", type=int, default=None)
    run.add_argument("--no-render", action="store_true", help="suppress turn-by-turn display")
    run.add_argument("--json-out", default=None, help="optional path to save episode result JSON")

    compare = subparsers.add_parser("compare", help="run all implemented agents with the same seed")
    compare.add_argument("--turns", type=int, default=20)
    compare.add_argument("--seed", type=int, default=7)

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
        )
        if args.json_out:
            save_result(result, args.json_out)
        return 0

    if args.command == "compare":
        print(f"Comparing agents | turns={args.turns} | seed={args.seed}")
        print("-" * 56)
        for name in sorted(AGENTS):
            result = run_episode(name, args.turns, args.seed, render=False)
            print(f"{name:8s} score={result.overall_score:.3f} band={result.band}")
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
