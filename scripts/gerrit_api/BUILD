load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

py_library(
    name = "gerrit_api",
    srcs = glob(["**/*.py"]),
    deps = [
        requirement("httpx"),
        requirement("pydantic"),
        requirement("requests"),
    ],
)
