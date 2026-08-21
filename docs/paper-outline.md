# Public Paper Outline

Working title: **Coherence Under Constraint: A Structural Benchmark for Advanced Agent Stewardship**

## 1. Abstract
Describe the narrow benchmark proposal and separate the executable prototype from broader interpretation.

## 2. Motivation
Explain why one-shot task success can miss failures that appear across time, memory, conflicting signals, resource limits, and repeated consequences.

## 3. Scope
Define the operational measures and state clearly which claims are outside the benchmark.

## 4. Habitat environment
Describe persistent state, resources, objects, signals, disturbances, observations, legal actions, and event memory.

## 5. Baselines
Present Alpha-Epsilon as transparent incremental baselines. Keep later stages as roadmap designs.

## 6. Falsifier episodes
Define deterministic fixtures and the failure mode each is intended to expose. Separate fixture setup from seed variation.

## 7. Scoring and evaluation
Document the seven domains, weights, behavior-derived heuristics, multi-seed reports, and versioned JSON outputs.

## 8. Related work
Use `docs/related-work.md`. Compare directly with interactive-agent benchmarks, long-horizon evaluation, memory systems, and theory-grounded assessment. Avoid unsupported novelty claims.

## 9. Experiments
Report Alpha-Epsilon across deterministic fixtures, multi-seed robustness, raw versus degraded observations, and useful ablations.

## 10. Limitations
Cover toy-world scale, hand-authored dynamics, heuristic scoring, external-validity limits, small baseline set, and lack of independent replication.

## 11. Reproducibility
Provide repository revision, Python version, fixture names, seeds, CLI commands, schema version, and raw result files.

## Publication gate
Do not present the work as validated until the v0.2 suite is green, baseline files are generated, citations are complete, and the prose is checked against the executable code.
