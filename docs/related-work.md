# Related Work

CUC Habitat is a small structural benchmark proposal. It should be compared with established work rather than presented as a standalone validation result.

## Interactive agent evaluation

AgentBench evaluates language-model agents across multiple interactive environments and documents long-horizon reasoning and decision failures.
Primary source: https://arxiv.org/abs/2308.03688

OSWorld evaluates agents in real computer environments with execution-based checks; OSWorld 2.0 extends that work to longer stateful workflows. CUC Habitat is far smaller and less realistic, but offers a deliberately inspectable toy environment for controlled perturbations.
Primary sources: https://arxiv.org/abs/2404.07972 and https://arxiv.org/abs/2606.29537

SWE-bench evaluates repository-level problem solving from real GitHub issues and motivates externally checkable outcomes.
Primary source: https://arxiv.org/abs/2310.06770

Tau-bench evaluates tool-using agents across repeated rule-governed interactions and motivates reporting reliability over multiple trials rather than relying on one run.
Primary source: https://arxiv.org/abs/2406.12045

## Memory systems

MemGPT develops explicit memory-management strategies for long-running language-model applications. CUC Habitat memory is much simpler and should not be described as equivalent.
Primary source: https://arxiv.org/abs/2310.08560

## Theory-grounded indicator research

Butlin et al. (2023) demonstrates a theory-grounded way to derive computational indicators for a difficult AI-assessment problem. CUC Habitat does not implement or validate that indicator framework; its scores concern only behavior inside this benchmark environment.
Primary source: https://arxiv.org/abs/2308.08708

## Where CUC Habitat is weaker

- toy world rather than real computer or user environments,
- small hand-authored state space,
- heuristic scoring with limited validation,
- few baseline architectures,
- no external leaderboard or independent replication,
- limited adversarial and statistical evaluation so far.

## Possible contribution

The defensible proposal is organizational: place continuity, boundary integrity, consequence sensitivity, resource regulation, memory use, and calibration in one inspectable persistent environment, then perturb those properties with named falsifier episodes. Whether that combination adds value beyond ordinary task-success benchmarks remains an empirical question.
