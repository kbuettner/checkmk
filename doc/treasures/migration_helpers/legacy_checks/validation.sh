#!/usr/bin/bash

# Validation script for migrating legacy checks to modern plugins
# This is convenient when using LLMs to assist with the migration, as
# the agent otherwise will keep
# a) forgetting to run some of the validation steps
# b) keep coming up with new commands that need approval

cd "$(git rev-parse --show-toplevel)" || exit $?

# shellcheck disable=SC2046  # we want word splitting here
bazel run //:format $(git diff --name-only) || exit $?

bazel lint --fix //cmk/... //tests/unit/... || exit $?

bazel build --config=mypy //cmk/... //tests/unit/... || exit $?

bazel test //tests/unit/... || exit $?

make -C tests test-plugins-consistency
