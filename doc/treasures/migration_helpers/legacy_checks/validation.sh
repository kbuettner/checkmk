#!/usr/bin/bash

# Validation script for migrating legacy checks to modern plugins
# This is convenient when using LLMs to assist with the migration, as
# the agent otherwise will keep
# a) forgetting to run some of the validation steps
# b) keep coming up with new commands that need approval

cd "$(git rev-parse --show-toplevel)" || exit $?

# shellcheck disable=SC2046  # we want word splitting here
bazel run //:format $(git diff --name-only) || exit $?

LIBS="//cmk/legacy_checks/... //cmk/legacy_includes/... //cmk/plugins/..."
TESTS="//tests/unit:plugins //tests/unit:plugins_ultimate //tests/unit:repo"

# shellcheck disable=SC2086  # we want word splitting here
bazel lint --fix $LIBS $TESTS || exit $?

# shellcheck disable=SC2086  # we want word splitting here
bazel build --config=mypy $LIBS $TESTS || exit $?

# shellcheck disable=SC2086  # we want word splitting here
bazel test $TESTS || exit $?

make -C tests test-plugins-consistency
