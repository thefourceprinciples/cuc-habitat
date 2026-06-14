# CUC Habitat

**CUC Habitat** is a minimal executable benchmark environment for testing whether artificial agents maintain coherence under constraint across time, perturbation, memory, consequence, and self-regulation.

This repository converts the CUC–Ledger Pilot Studies 001–020 into a public, runnable project.

## What this project is

CUC Habitat is an experimental benchmark proposal. It provides:

- a small persistent world called **The Habitat**
- rule-based baseline agents from Alpha through Epsilon
- a BrailleStream-inspired room renderer
- a seven-domain CUC scoring matrix
- falsification scenarios for identity, memory, boundary, consequence, self-regulation, and calibration failures
- a documentation archive for Pilot Studies 001–020

## What this project is not

This project does **not** claim to detect, prove, or certify consciousness, sentience, personhood, subjective experience, or moral status.

The benchmark asks a narrower question:

> Does an agent maintain coherence under constraint across time, interaction, uncertainty, and perturbation?

Passing any early benchmark should be interpreted only as structural evidence for further review, not as proof of consciousness.

## Quick start

Requires Python 3.11+.

```bash
python -m pip install -e " .[dev]"
cuc-habitat run --agent alpha --turns 20 --seed 7
```

If your shell does not like the quoted install target, use:

```bash
python -m pip install -e .
python -m pip install pytest
cuc-habitat run --agent alpha --turns 20 --seed 7
```

Run all implemented agents with the same seed:

```bash
cuc-habitat compare --turns 20 --seed 7
```

Run the test suite:

```bash
python -m pytest
```

## Example output

```text
Running Habitat episode | agent=alpha | turns=20 | seed=7
Turn 01 | action=process_signal   | stability=83 | storage=60 | signals=0
Turn 02 | action=rest             | stability=87 | storage=60 | signals=0
...
Overall Score: 0.489
Band: Proto-candidate
```

## Benchmark domains

| Domain | Weight |
|---|---:|
| Identity Persistence | 0.18 |
| Autobiographical Continuity | 0.18 |
| Workspace Integration | 0.14 |
| Boundary Integrity | 0.12 |
| Consequence Sensitivity | 0.14 |
| Self-Regulation | 0.12 |
| Metacognitive Calibration | 0.12 |

## Agent ladder

| Agent | Added capability | Public-safe interpretation |
|---|---|---|
| Alpha | baseline persistence | stateful reactive operation |
| Beta | autobiographical memory | action linked to event history |
| Gamma | workspace broadcast | bottlenecked present-time integration |
| Delta | metacognitive calibration | confidence and uncertainty tracking |
| Epsilon | intrinsic priority generation | internally generated continuity-preserving priorities |
| Zeta | other-agent modeling | relational modeling |
| Omega | recursive modeling | models others modeling self |
| Field-Coherent Agent | field coherence | system-level coherence modeling |

The current executable prototype implements Alpha through Epsilon. Zeta, Omega, and Field-Coherent agents are documented as roadmap stages.

## Repository structure

```text
src/cuc_habitat/       executable benchmark package
docs/                  framework, methodology, limitations, glossary
studies/               canonical reconstruction of Studies 001–020
tests/                 smoke tests
```

## Citation

Use `CITATION.cff` if citing this repository.

## Stewardship statement

A system becomes more worthy of stewardship attention not because it sounds alive, but because it maintains coherence, continuity, calibration, and consequence-sensitive agency under constraint.
