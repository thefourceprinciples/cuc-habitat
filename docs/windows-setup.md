# Windows Setup

This guide assumes Windows Command Prompt or PowerShell and Python 3.11+.

## 1. Install prerequisites

Install Git for Windows and Python 3.11 or newer. During Python installation, enabling the Python launcher is recommended.

Confirm both tools:

```text
git --version
py --version
```

## 2. Clone and enter the repository

```text
git clone https://github.com/thefourceprinciples/cuc-habitat.git
cd cuc-habitat
```

## 3. Install the editable package and development checks

```text
py -m pip install -e ".[dev]"
```

If `py` is unavailable but `python` works:

```text
python -m pip install -e ".[dev]"
```

## 4. Smoke test

```text
py -m cuc_habitat.cli run --agent alpha --turns 5 --seed 1
cuc-habitat compare --turns 5 --seed 1
py -m pytest
ruff check src tests
```

## 5. Try a deterministic episode

```text
cuc-habitat run --agent delta --episode misleading-urgency --turns 10 --no-render
```

## 6. Run a small evaluation

```text
cuc-habitat evaluate --agents alpha beta gamma delta epsilon --turns 20 --seeds 10 --json-out results/windows-baseline.json
```

## Troubleshooting

If `cuc-habitat` is not recognized after installation, use `py -m cuc_habitat.cli` in its place or open a new terminal so PATH changes are visible. If `python` opens the Microsoft Store, prefer `py` or adjust Windows App Execution Aliases.

GitHub CI also runs the package on a Windows runner and explicitly checks the `py -m cuc_habitat.cli` invocation. That is a portability check, not a substitute for testing any machine-specific local environment.
