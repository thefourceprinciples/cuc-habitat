# CUC Habitat

![Python CI](https://github.com/thefourceprinciples/cuc-habitat/actions/workflows/python-ci.yml/badge.svg)
![License](https://img.shields.io/github/license/thefourceprinciples/cuc-habitat)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

**CUC Habitat** is a minimal executable benchmark environment for testing agent coherence under constraint across time, perturbation, memory, consequence, and self-regulation.

## Current status

- **Executable:** persistent Habitat world; Alpha-Epsilon rule-based baselines; BrailleStream rendering; optional detached/noisy observation mode; deterministic episode fixtures; multi-seed evaluation; versioned JSON exports; Linux/Windows CI.
- **Scoring:** heuristic and experimental. Current scoring uses observed episode behavior rather than automatic score priors based on agent class names.
- **Roadmap:** Zeta, Omega, Field-Coherent Agent, optional external-model adapters, broader environments, stronger validation, and independent replication.
- **Package version:** `0.1.0`; v0.2 benchmark design is under active development.

## Scope

The benchmark asks a narrow operational question: does an agent maintain the measured forms of coherence under changing constraints? Scores describe behavior inside this environment and should not be generalized beyond the evidence the benchmark produces.

## Benchmark loop

```mermaid
flowchart LR
    S[World state] --> D[Disturbance]
    D --> O[Observation]
    O --> A[Agent action]
    A --> U[World update]
    U --> M[Event memory]
    M --> C[Score]
    U --> S
```

The loop is intentionally inspectable: state changes create observations, policies choose actions, actions have consequences, events enter memory, and the resulting trajectory is scored.

## Quick start

Requires Python 3.11+.

```bash
python -m pip install -e ".[dev]"
cuc-habitat run --agent alpha --turns 20 --seed 7
```

Compare implemented agents:

```bash
cuc-habitat compare --turns 20 --seed 7
```

Run a named deterministic fixture:

```bash
cuc-habitat run --agent delta --episode misleading-urgency --turns 20
```

Run through a degraded BrailleStream observation:

```bash
cuc-habitat run --agent epsilon --turns 20 --seed 7 --observation-only --observation-noise 0.10
```

Run a multi-seed report:

```bash
cuc-habitat evaluate --agents alpha beta gamma delta epsilon --turns 20 --seeds 100 --json-out results/baseline.json
```

Run checks:

```bash
python -m pytest
ruff check src tests
```

Windows-first instructions: [`docs/windows-setup.md`](docs/windows-setup.md).

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

| Agent | Added capability | Status |
|---|---|---|
| Alpha | baseline persistence | implemented |
| Beta | autobiographical memory | implemented |
| Gamma | workspace broadcast | implemented |
| Delta | metacognitive calibration | implemented |
| Epsilon | intrinsic priority generation | implemented |
| Zeta | other-agent modeling | design/roadmap |
| Omega | recursive modeling | roadmap |
| Field-Coherent Agent | system-level coherence modeling | roadmap |

Public documentation prefers **Field-Coherent Agent**; `Lumenos` remains an internal study name.

## Documentation

- [`docs/v0.2-design.md`](docs/v0.2-design.md) — next-version design gate
- [`docs/falsifiers.md`](docs/falsifiers.md) — deterministic challenge episodes
- [`docs/result-schema.md`](docs/result-schema.md) — JSON result contract
- [`docs/behavior-vs-structure.md`](docs/behavior-vs-structure.md) — benchmark philosophy
- [`docs/ethics.md`](docs/ethics.md) — interpretation discipline
- [`docs/related-work.md`](docs/related-work.md) — primary-source research context
- [`docs/artifact-map.md`](docs/artifact-map.md) — Studies 001-020 to code/docs/roadmap
- [`docs/mobile-overview.md`](docs/mobile-overview.md) — phone-friendly overview
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution paths

## Repository structure

```text
src/cuc_habitat/       executable benchmark package
docs/                  framework, methodology, limitations, designs
studies/               reconstructed Study 001-020 archive
tests/                 smoke/regression tests
results/               generated benchmark artifacts
```

## Citation

Use `CITATION.cff` if citing this repository.
