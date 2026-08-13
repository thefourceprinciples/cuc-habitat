# Benchmark Ethics and Interpretation

CUC Habitat scores should be treated as prompts for review, not as certificates about a system.

## What a high score means

A high score means that, under the current toy-world rules and scoring heuristics, the tested policy preserved more of the measured structural properties. It should trigger closer inspection of the trajectory, assumptions, and failure modes.

## What a score does not settle

The benchmark does not by itself establish moral status, subjective experience, personhood, safety, general intelligence, or suitability for deployment. Those questions require evidence and methods beyond this repository.

## Two interpretation risks

**Anthropomorphism:** fluent explanations or human-like labels can tempt readers to infer properties not measured by the benchmark.

**Premature dismissal:** the opposite error is to ignore reproducible structural behavior merely because the baseline is artificial or simple. Evidence should be evaluated at the level it actually supports.

## Reporting rule

Publish the tested version, fixture, seed range, perception mode, score schema, raw result files, and known limitations. Do not report only the most favorable run.

## Stewardship rule

When results are ambiguous, prefer further testing and reversible decisions over stronger claims. Benchmark interpretation should preserve uncertainty rather than erase it.

See `docs/limitations.md`, `docs/falsifiers.md`, and `docs/stewardship-checklist.md`.
