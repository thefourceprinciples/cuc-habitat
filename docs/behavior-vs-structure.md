# Behavior vs Structure

A benchmark can be fooled if it rewards only the visible answer at the end of a task. Two systems may produce the same output while differing sharply in how they preserve state, use memory, allocate resources, resist misleading signals, revise decisions, and absorb consequences over time.

CUC Habitat therefore treats **behavior** and **structure under constraint** as related but distinct targets.

## Behavior-only risk

A single successful action may be produced by luck, a hard-coded shortcut, prompt imitation, architecture-specific priors in the scorer, or a policy that fails immediately when conditions change. Surface success is useful evidence, but it is weak evidence about persistence.

## Structural evaluation goal

The benchmark records a trajectory: state -> disturbance -> observation -> action -> consequence -> memory -> next state. Named episodes then stress different parts of that loop. Multi-seed reports ask whether the pattern survives perturbation rather than appearing once.

## What structure means here

In this project, structure is operational and local. It includes continuity of state, memory affecting action, bounded response to deceptive salience, resource-aware regulation, consequence-sensitive behavior, and calibration/revision signals that can be inspected in the event log.

## Limits

A toy environment can establish only that an implementation behaves a certain way under its own rules. Structural scores do not automatically generalize to broader environments, and they should not be substituted for task competence, safety evaluation, or external validation.

See `docs/methodology.md` for the benchmark process and `docs/limitations.md` for interpretation limits.
