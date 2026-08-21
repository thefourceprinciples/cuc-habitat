# Contributing

CUC Habitat welcomes small, inspectable contributions. Please keep changes narrow enough that a reviewer can tell what claim, behavior, or document changed.

## Code contributions

Install development dependencies, run the test suite, run static checks, and include a deterministic reproduction when fixing benchmark behavior. Changes to scoring should explain the expected effect across more than one seed.

## Non-code contributions

You can contribute without writing Python by:

- reviewing documentation for clarity and overstatement,
- suggesting primary-source related work,
- checking links and terminology,
- triaging issues and identifying duplicates or stale acceptance criteria,
- reproducing documented commands and result files,
- comparing generated results with the documented schema,
- proposing falsifier episodes with a clear expected failure mode.

## Research notes

A useful research note identifies the source, explains relevance to CUC Habitat, states whether it changes a claim boundary, and proposes where the note belongs in the repository. Prefer primary papers or official project pages when possible.

## Pull requests

State which checks ran, which documentation changed, whether scoring changed, and which issues the PR addresses. Keep roadmap proposals separate from claims about implemented behavior.

## Reproduction

When reproducing benchmark output, record the repository revision, Python version, agent, episode, seed or seed count, turn count, perception mode, and result-schema version.
