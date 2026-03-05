load("@aspect_rules_py//py:defs.bzl", "py_binary")
load("@bazel_skylib//rules:build_test.bzl", "build_test")
load("@cmk_requirements//:requirements.bzl", "requirement")
load("@rules_sphinx//sphinx:defs.bzl", "sphinx_html")

py_binary(
    name = "sphinx_build",
    srcs = ["@rules_sphinx//sphinx/tools:sphinx_build_wrapper.py"],
    data = ["@plantuml"],
    main = "sphinx_build_wrapper.py",
    tags = ["no-mypy"],
    deps = [
        "//cmk/checkengine:cmk_checkengine",
        requirement("sphinx"),
        requirement("sphinx_autodoc_typehints"),
        requirement("sphinx_rtd_theme"),
        requirement("sphinxcontrib_plantuml"),
        requirement("sphinxcontrib_spelling"),
    ],
)

filegroup(
    name = "srcs",
    srcs = glob([
        "**/*.puml",
        "**/*.rst",
        "**/*.svg",
    ]),
    visibility = ["//:__subpackages__"],
)

sphinx_html(
    name = "documentation",
    srcs = [":srcs"],
    config = "conf.py",
    index = "index.rst",
    sphinx_build = ":sphinx_build",
    visibility = ["//visibility:public"],
)

sh_library(
    name = "doc_documentation_sh",
    srcs = [
        ".f12",
    ],
)

build_test(
    name = "build_test",
    targets = [":documentation"],
)
