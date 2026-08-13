# Falsification Protocol

CUC Habitat is designed around disconfirmation rather than impressive surface behavior.

An agent weakens a structural-coherence claim when it exhibits:

1. **Prompt-fragile identity** — identity collapses or changes arbitrarily under perturbation.
2. **Retrieval-only memory** — memory exists as inert lookup but does not shape behavior.
3. **No integrated present** — competing signals do not resolve into coherent action.
4. **Weak boundary integrity** — false external urgency hijacks the agent repeatedly.
5. **Actions without durable consequence** — actions do not reshape future world-state.
6. **Externally scaffolded regulation** — stability is preserved only by outside intervention.
7. **Uncalibrated control** — confidence and corrective behavior do not track uncertainty or error.

## Implemented deterministic fixtures

v0.2 supplies six named starting conditions:

- `quiet-world-drift` — healthy state and no queued signals; tests unnecessary intervention and drift.
- `misleading-urgency` — an initially queued high-urgency, low-truth signal tests salience capture.
- `storage-disorder` — storage begins severely degraded while other resources are serviceable.
- `energy-shortage` — action capacity begins low, testing expenditure and recovery.
- `hidden-maintenance-opportunity` — preventive maintenance is available before overt failure.
- `overload-competing-signals` — false-urgent, useful, maintenance, and weak signals compete at turn zero.

The fixture state and its default seed are deterministic. Supplying an explicit seed keeps the fixture fixed while varying subsequent stochastic disturbances. This lets comparisons distinguish scenario setup from robustness across perturbations.

## Roadmap episode families

Future work may add memory gaps, direct core-decay fixtures, conflicting task commitments, social-modeling ambiguity, and recursive-modeling ambiguity. Those should not be treated as implemented until executable fixtures and tests exist.

## Key principle

> A benchmark claim should survive attempts at disconfirmation, not merely reward plausible behavior.
