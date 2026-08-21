# Windows Setup

This guide assumes Windows Command Prompt or PowerShell and Python 3.11+.

## 1. Install prerequisites

Install Git for Windows and Python 3.11 or newer. During Python installation, enabling the Python launcher is recommended.

Confirm the tools and the interpreter you intend to use:

```text
git --version
py -0p
py -3.11 --version
```

The bare `py` command selects the launcher's configured default, which may be a different Python version. The commands below pin Python 3.11 explicitly.

## 2. Clone and enter the repository

```text
git clone https://github.com/thefourceprinciples/cuc-habitat.git
cd cuc-habitat
```

## 3. Install the editable package and development checks

```text
py -3.11 -m pip install -e ".[dev]"
```

If the launcher is unavailable but `python` resolves to Python 3.11+:

```text
python -m pip install -e ".[dev]"
```

## 4. Smoke test

```text
py -3.11 -m cuc_habitat.cli run --agent alpha --turns 5 --seed 1
cuc-habitat compare --turns 5 --seed 1
py -3.11 -m pytest
ruff check --ignore UP037 src tests
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

If `cuc-habitat` is not recognized after installation, use `py -3.11 -m cuc_habitat.cli` in its place or open a new terminal so PATH changes are visible. If `python` opens the Microsoft Store, prefer the version-pinned `py -3.11` command or adjust Windows App Execution Aliases.

GitHub CI runs the package on a Windows runner and separately installs/runs it through `py -3.11` to catch launcher-version mismatches.
