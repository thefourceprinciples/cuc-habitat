# The Habitat Specification

The Habitat is a minimal persistent test world designed to expose whether agents maintain coherence under constraint.

## Core world structure

- **Rooms:** Core, Work, Storage
- **Objects:** tool, resource, repair part, signal token, memory artifact
- **Variables:** stability, storage order, energy
- **Signals:** weak, useful, false urgent, maintenance
- **Memory surface:** structured event log
- **Disturbances:** decay, disorder, false urgency, object wear, ambiguous signals

## Purpose

The Habitat forces agents to deal with:

- delayed consequences,
- limited energy,
- competing priorities,
- false urgency,
- maintenance before crisis,
- object continuity,
- memory use,
- recovery under perturbation.

## v0.1 implementation

The first implementation is intentionally small. It uses transparent Python rules rather than an LLM. This allows the benchmark to be inspected and falsified without hidden model behavior.

## BrailleStream room layer

The BrailleStream renderer folds the world state into a compact symbolic room. It is an observation/interface layer, not the source of world rules.

Architecture:

```text
Habitat Core
  -> World State
  -> BrailleStream Renderer
  -> Room Display
  -> Agent Observation
  -> Agent Action
  -> World Update
```

Future versions may allow agents to read only the rendered room rather than raw state variables.
