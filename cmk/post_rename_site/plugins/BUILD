load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "plugins",
    srcs = glob(["**/*.py"]),
    imports = ["../../.."],
    visibility = [
        "//cmk:__subpackages__",
        "//tests:__subpackages__",
    ],
    deps = [
        "//cmk/gui",
        "//cmk/post_rename_site:internal",
        "//cmk/utils",
        "//packages/cmk-ccc:site",
    ],
)
