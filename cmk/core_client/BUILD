load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "cmk_core_client",
    srcs = glob(
        include = ["**/*.py"],
        exclude = [
            "**/community/**",
            "**/nonfree/**",
        ],
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

py_library(
    name = "cmk_core_client_community",
    srcs = glob(
        include = ["**/community/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
    ],
)

py_library(
    name = "cmk_core_client_pro",
    srcs = glob(
        include = ["**/nonfree/**/pro/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    visibility = [
        "//cmk:__subpackages__",
        "//tests:__subpackages__",
    ],
    deps = [
        ":cmk_core_client",
    ],
)

py_library(
    name = "cmk_core_client_cloud",
    srcs = glob(
        include = ["**/nonfree/**/cloud/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
)

py_library(
    name = "cmk_core_client_ultimate",
    srcs = glob(
        include = ["**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
)

py_library(
    name = "cmk_core_client_ultimatemt",
    srcs = glob(
        include = ["**/nonfree/**/ultimatemt/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
)
