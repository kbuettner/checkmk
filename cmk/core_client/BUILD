load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "core_client",
    srcs = glob(
        include = ["**/*.py"],
    ),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//packages/cmk-ccc:config-path",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-trace",
    ],
)
