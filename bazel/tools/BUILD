load("@aspect_bazel_lib//lib:expand_template.bzl", "expand_template")
load("@aspect_rules_lint//format:defs.bzl", "format_multirun")
load("@bazel_skylib//rules:copy_file.bzl", "copy_file")
load("@bazel_skylib//rules:native_binary.bzl", "native_binary")
load("@cmk_requirements//:requirements.bzl", "requirement")
load("@rules_mypy//mypy:mypy.bzl", "mypy_cli")

mypy_cli(
    name = "mypy_cli",
    mypy_requirement = requirement("mypy"),
    deps = [
        # for `plugins = ["pydantic.mypy"]`
        requirement("pydantic"),
    ],
)

# TODO: Collect here all formatters we're currently using
format_multirun(
    name = "format",
    c = "@clang-linux-x86_64//:bin/clang-format",
    cc = "@clang-linux-x86_64//:bin/clang-format",
    python = "@aspect_rules_lint//format:ruff",
    rust = "@rules_rust//tools/upstream_wrapper:rustfmt",
    toml = ":taplo_quiet",
    visibility = ["//visibility:public"],
)

native_binary(
    name = "clangtidy_bin",
    src = "@clang-linux-x86_64//:bin/clang-tidy",
)

filegroup(
    name = "clang_tidy_config",
    srcs = [".clang-tidy"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "iwyu_bin",
    srcs = ["run-iwyu"],
)

filegroup(
    name = "iwyu_mappings",
    srcs = glob(["mappings/*.imp"]),
)

copy_file(
    name = "shellcheck_binary",
    src = "@shellcheck",
    out = "shellcheck",
)

# Shell wrapper to execute shellcheck in the callers working directory
sh_binary(
    name = "shellcheck_bin",
    srcs = ["run-shellcheck"],
    data = [":shellcheck_binary"],
)

copy_file(
    name = "shfmt_binary",
    src = "@shfmt//file",
    out = "shfmt",
)

# Shell wrapper to execute shfmt in the callers working directory
sh_binary(
    name = "shfmt_bin",
    srcs = ["run-shfmt"],
    data = [":shfmt_binary"],
)

genrule(
    name = "taplo",
    srcs = ["@taplo.gz//file"],
    outs = ["taplo_bin"],
    cmd = "gunzip -c $< > $@",
    executable = True,
)

expand_template(
    name = "taplo_quiet_tp",
    out = "taplo_wrapper.sh",
    data = [":taplo_bin"],
    substitutions = {"{taplo_bin}": "$(execpath :taplo_bin)"},
    template = [
        "#!/bin/sh",
        'exec env RUST_LOG=warn "$BUILD_WORKSPACE_DIRECTORY/{taplo_bin}" "$@"',
        "",
    ],
)

sh_binary(
    name = "taplo_quiet",
    srcs = [":taplo_quiet_tp"],
    data = [":taplo"],
)

# TODO: Should we use buildifier more in the way aspect does?
# Currenlty, we try to find all "bazel" files with run-buildifier or run buildifier on a package level.
# rules_lint however does the discovery by itself, see:
# https://docs.aspect.build/workflows/features/buildifier
alias(
    name = "buildifier",
    actual = "@buildifier_prebuilt//:buildifier",
)

alias(
    name = "uv",
    actual = "@multitool//tools/uv",
)
