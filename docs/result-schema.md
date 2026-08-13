# Result Schema

CUC Habitat result files use a versioned JSON envelope. The current schema version is `1.0`.

## Episode result

Required top-level fields:

- `schema_version`: schema identifier
- `agent`: implemented agent name
- `turns`: requested turn count
- `seed`: effective random seed, or null for an unseeded stochastic run
- `episode`: named deterministic fixture, or null
- `perception_mode`: `raw-state` or `braille-observation`
- `final_state`: final Habitat state snapshot
- `domain_scores`: seven normalized CUC domain scores
- `overall_score`: weighted score in [0, 1]
- `band`: heuristic classification band

`final_state.memory` contains one event per completed turn with `turn`, `observation`, `action`, `reason`, `outcome`, `confidence`, and `revision_flag`.

## Evaluation result

Multi-seed evaluation files also use schema version `1.0` and contain `turns`, `seed_count`, `episode`, and an `agents` mapping. Each agent entry reports mean, variance, worst-decile mean, minimum, maximum, and band distribution.

## Compatibility rule

Additive fields may be introduced within schema 1.x. Renaming or removing fields requires a schema-version change. Result files are benchmark artifacts, not scientific validation by themselves.
