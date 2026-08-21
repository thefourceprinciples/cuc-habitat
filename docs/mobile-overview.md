# CUC Habitat: Mobile Overview

CUC Habitat is a small Python benchmark for asking a narrow question: does an agent preserve useful structure when the environment changes, resources become constrained, signals conflict, and prior actions have consequences?

## What exists now

- executable Alpha-Epsilon rule-based baselines,
- a persistent Habitat state,
- BrailleStream rendering plus an optional detached/noisy observation mode,
- named deterministic v0.2 episode fixtures,
- seven-domain heuristic scoring,
- multi-seed evaluation reports,
- versioned JSON result files,
- Linux and Windows CI.

## What is roadmap

Zeta and later agent stages, live model-provider adapters, broader environments, stronger score validation, larger empirical studies, and external replication.

## From a phone

Good mobile tasks are reading docs, reviewing issues/PRs, checking Actions status, reviewing result JSON, editing issue text, and deciding priorities.

## From a computer

Use a computer for editable installation, local runs, tests, Ruff checks, larger evaluation batches, profiling, and code changes.

## Useful commands

```text
cuc-habitat run --agent alpha --turns 20 --seed 7
cuc-habitat run --agent delta --episode misleading-urgency --turns 20
cuc-habitat evaluate --agents alpha beta gamma delta epsilon --turns 20 --seeds 100 --json-out results/baseline.json
python -m pytest
ruff check src tests
```

## Claim boundary

Scores are benchmark measurements inside a toy environment. They should be used to compare behavior and identify failure modes, not treated as certificates about systems outside the benchmark.

## Current priority

Keep the v0.2 foundation deterministic, reproducible, and inspectable before expanding the agent ladder.
