# Artifact Map

This map connects the Study 001-020 archive to executable or roadmap artifacts. `Implemented` means a corresponding mechanism exists in code; it does not mean the study claim has been externally validated.

- **001 Consciousness models** -> `docs/related-work.md`, `docs/limitations.md` — context/roadmap.
- **002 Current AI candidacy** -> `docs/limitations.md`, `docs/benchmark-matrix.md` — interpretive context.
- **003 Threshold requirements** -> `docs/architecture-ladder.md` — documented.
- **004 Embodiment requirement** -> `docs/habitat-spec.md` — modeled as a persistent causal environment.
- **005 Digital causal body** -> `src/cuc_habitat/models.py`, `world.py` — implemented toy state/body.
- **006 Minimum viable architecture** -> `src/cuc_habitat/agents.py` — implemented Alpha-Epsilon baselines.
- **007 Falsification suite** -> `docs/falsifiers.md`, `episodes.py` — v0.2 fixtures implemented.
- **008 Benchmark matrix** -> `docs/benchmark-matrix.md`, `scoring.py` — heuristic implementation.
- **009 Agent-class application** -> `agents.py`, `runner.py` — implemented baseline comparison.
- **010 Habitat environment** -> `models.py`, `world.py`, `docs/habitat-spec.md` — implemented.
- **011 Habitat scoring protocol** -> `scoring.py`, `docs/result-schema.md` — implemented, still heuristic.
- **012 Alpha baseline** -> `AlphaAgent`, CLI `run` — implemented.
- **013 Alpha-to-Beta memory** -> `BetaAgent`, state memory ledger — implemented baseline.
- **014 Alpha vs Beta** -> CLI `compare`, evaluator — executable comparison path.
- **015 Beta vs Gamma workspace** -> `GammaAgent` — implemented baseline.
- **016 Gamma vs Delta calibration** -> `DeltaAgent` — implemented baseline.
- **017 Delta vs Epsilon priorities** -> `EpsilonAgent` — implemented baseline.
- **018 Epsilon vs Zeta** -> `docs/zeta-design.md` — roadmap only.
- **019 Zeta vs Omega** -> `docs/architecture-ladder.md` — roadmap only.
- **020 Omega vs field coherence** -> `docs/architecture-ladder.md` — roadmap only; public name is Field-Coherent Agent.

## Cross-cutting v0.2 artifacts

- deterministic episodes -> `src/cuc_habitat/episodes.py`
- multi-seed reports -> `src/cuc_habitat/evaluator.py`
- constrained perception -> `src/cuc_habitat/braillestream.py`
- stable exports -> `docs/result-schema.md`
- next-version gate -> `docs/v0.2-design.md`
- stewardship checks -> `docs/stewardship-checklist.md`

When archive text and executable behavior diverge, the executable version and its tests determine what the current software actually does; the study file remains provenance and design history.
