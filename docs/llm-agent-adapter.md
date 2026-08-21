# Optional LLM Agent Adapter

This is a design document only. The core benchmark remains runnable without an external model service.

## Interface

A future adapter should expose one narrow operation:

```text
choose_action(observation, allowed_actions, context) -> ActionDecision
```

The adapter receives an explicit benchmark observation and a closed set of legal actions. It must not receive hidden Habitat state.

## Separation of concerns

- Habitat owns world state, disturbances, legal actions, and scoring.
- The adapter owns prompt construction, model invocation, response parsing, and model metadata.
- Prompt templates live as versioned text in the repository.
- Tests use deterministic fixtures or fake adapters rather than live model calls.

## Credentials and privacy

API keys must come from environment variables or a secret manager and must never be committed. Logs should store the minimum data needed for reproducibility. Private user data should not be inserted into benchmark prompts by default.

## Logging

Each model-backed decision should record provider/model identifier, prompt-template version, observation hash or fixture identifier, returned action, parsing status, latency if available, and any retry count. Secrets and authorization headers are excluded.

## Scoring boundary

The same observable-behavior scoring path should be used for rule-based and model-backed agents. A model should not receive bonus points because of its brand, size, architecture, or fluent explanations.

## Failure handling

Malformed output, unavailable services, timeouts, and disallowed actions should become explicit benchmark events rather than silently corrected success cases.

## Implementation gate

Actual provider integration comes after the local package, deterministic episodes, multi-seed evaluator, and result schema are stable.
