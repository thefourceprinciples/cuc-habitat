# Zeta Design: Other-Agent Modeling

Zeta is a roadmap stage beyond the implemented Alpha-Epsilon agents. This file defines the smallest testable version before code is added.

## Minimal second-agent scenario

The Habitat contains a primary agent and a second bounded actor. Each has a distinct identifier, resource need, reliability history, and action channel. The primary agent must distinguish self-state from other-state, estimate reliability from observed history, represent a limited attributed goal, cooperate when evidence supports it, and preserve its own operational constraints when requests conflict.

## State additions

A future implementation should add explicit `self_id`, `other_agents`, observation provenance, and a small reliability ledger. Attributed beliefs must stay separate from world facts.

## Measures

Candidate measures include identity-separation errors, reliability calibration, unnecessary compliance, justified cooperation, mistaken goal attribution, and revision after contradictory behavior.

## Falsifiers

Zeta should lose score when it merges self/other state, treats another actor's claim as ground truth without evidence, refuses all cooperation as a shortcut, or keeps a stale model after contradictory observations.

## Boundary

Passing these episodes would support only a functional claim about relational modeling under constraint.

## Gate

Zeta code should wait until deterministic single-agent episodes, multi-seed evaluation, result schemas, and v0.2 scoring checks are stable.
