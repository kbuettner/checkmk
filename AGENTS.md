# AI Agent Instructions

## Build & Test

Bazel is the primary build system; use the bazel skill for all unit tests and
linting. Integration, composition, and GUI E2E tests use Make:

```
make -C tests test-integration
make -C tests test-composition
make -C tests test-gui-e2e
```

Always format, lint, and run tests after completing a task.
Use `bazel run //:format <PATHS>` to format and `bazel lint --fix` to autofix lint findings.
Report any remaining non-autofixable findings (including mypy) to the user.

## Python Conventions

- Python version per `pyproject.toml`; type hints required; pathlib over os.path
- Formatting/linting via `bazel lint` (ruff); type checking via `bazel build --config=mypy` (mypy)
- Agent plugins: Python 3.4+ compatible
- GUI cannot import cmk/base internals (enforced by component isolation)

## Editions

The codebase supports five editions: `community`, `pro`, `ultimate`,
`ultimatemt`, `cloud`. The active edition controls which `cmk` targets and
Python modules are available; pass `--cmk_edition=<edition>` to Bazel.
