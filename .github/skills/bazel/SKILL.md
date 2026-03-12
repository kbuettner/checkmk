---
name: bazel
description: Uses Bazel to run builds, tests and linting
---

# Repo-specific flags

```bash
# Edition (affects which cmk targets are built/tested)
--cmk_edition=community|pro|ultimate|ultimatemt|cloud

# Configs defined in .bazelrc
--config=mypy      # type checking
--config=clippy    # Rust linting

# CI excludes these to avoid xunit parser issues (fine to include locally)
-//packages/livestatus/... -//packages/neb/... -//packages/unixcat/...
```
