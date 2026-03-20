load("@aspect_rules_py//py:defs.bzl", "py_library", "py_pytest_main", "py_test")
load("@bazel_skylib//rules:write_file.bzl", "write_file")
load("@cmk_requirements//:requirements.bzl", "requirement")

package(default_visibility = [":__subpackages__"])

py_library(
    name = "conftest",
    testonly = True,
    srcs = [
        "conftest.py",
        "mocks_and_helpers.py",
    ],
    visibility = [
        ":__subpackages__",
        "//non-free/packages/cmk-bakery:__pkg__",
        "//non-free/packages/cmk-robotmk:__pkg__",
    ],
    deps = [
        "//cmk/base",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/utils",
        "//packages/cmk-livestatus-client:py_livestatus",
        "//packages/cmk-plugin-apis:agent_based",
        "//tests/testlib/common:repo",
        requirement("fakeredis"),
        requirement("pytest_metadata"),
    ],
)

py_library(
    name = "conftest_post_rename_site",
    testonly = True,
    srcs = [
        "cmk/post_rename_site/plugins/actions/conftest.py",
    ],
    deps = [
        "//cmk/gui",
        "//packages/cmk-ccc:user",
        "//tests/testlib/unit:unit_free",
        requirement("flask"),
        requirement("pytest"),
        requirement("pytest-mock"),
    ],
)

py_library(
    name = "conftest_update_config",
    testonly = True,
    srcs = [
        "cmk/update_config/conftest.py",
    ],
    deps = [
        "//tests/testlib/unit:unit_free",
        requirement("flask"),
        requirement("pytest"),
        requirement("pytest-mock"),
    ],
)

py_pytest_main(
    name = "__test__",
    deps = [
        requirement("pytest"),
        # pytest-xdist for `--numprocesses=NPROC`
        requirement("pytest-xdist"),
    ],
)

write_file(
    name = "cannot_fail",
    out = "test_cannot_fail.py",
    content = [
        "def test_cannot_fail() -> None:",
        "    assert True",
    ],
)

py_test(
    # Start the collection and load the conftests.  The complexity
    # of those warrants this target.
    name = "smoke",
    size = "small",
    srcs = [
        "__test__.py",
        "test_cannot_fail.py",
    ],
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    deps = [
        ":__test__",
        ":conftest",
        "//tests:testlib",
    ],
)

py_test(
    name = "post_rename_site_community",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/post_rename_site/**/*.py"],
        exclude = [
            "**/nonfree/**",
            "**/conftest.py",
        ],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        ":conftest_post_rename_site",
        "//cmk/post_rename_site:cmk_post_rename_site",
        "//tests/testlib/unit:unit_free",
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-mock"),
        requirement("werkzeug"),
        requirement("flask"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//non-free/packages/cmk-bakery",
            "//non-free/packages/cmk-dcd:gui",
            "//non-free/packages/cmk-liveproxyd:gui",
            "//non-free/packages/cmk-metric-backend",
            "//non-free/packages/cmk-mknotifyd",
            "//non-free/packages/cmk-otel-collector",
            "//non-free/packages/cmk-robotmk",
            "//non-free/packages/cmk-robotmk:gui",
            requirement("numpy"),
            requirement("pypdf"),
            requirement("pysaml2"),
            requirement("roman"),
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "post_rename_site_pro",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/post_rename_site/**/nonfree/**/pro/**/*.py"],
        allow_empty = True,
        exclude = ["**/conftest.py"],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        ":conftest_post_rename_site",
        "//cmk/utils",
        "//cmk/gui",
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("marshmallow"),
        requirement("pytest-random-order"),
        #requirement("time-machine"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/post_rename_site:cmk_post_rename_site_pro",
            "//non-free/packages/cmk-dcd:gui",
            "//non-free/packages/cmk-metric-backend",
            "//non-free/packages/cmk-otel-collector",
            requirement("pypdf"),
            #"//tests/testlib/unit:unit_nonfree",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "update_config_community",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/update_config/**/*.py"],
        exclude = ["**/nonfree/**"],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        "//cmk/update_config:cmk_update_config",
        "//tests/testlib/unit:unit_free",
        requirement("flask"),
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
        requirement("pytest-mock"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//non-free/packages/cmk-bakery",
            "//non-free/packages/cmk-dcd:gui",
            "//non-free/packages/cmk-liveproxyd:gui",
            "//non-free/packages/cmk-metric-backend",
            "//non-free/packages/cmk-mknotifyd",
            "//non-free/packages/cmk-otel-collector",
            "//non-free/packages/cmk-robotmk",
            "//non-free/packages/cmk-robotmk:gui",
            requirement("numpy"),
            requirement("pypdf"),
            requirement("pysaml2"),
            requirement("roman"),
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "update_config_pro",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/update_config/**/nonfree/**/pro/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        ":conftest_update_config",
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/update_config:cmk_update_config_pro",
            "//cmk/utils:pro",
            "//non-free/packages/cmk-dcd:gui",
            "//non-free/packages/cmk-metric-backend",
            "//non-free/packages/cmk-otel-collector",
            "//tests/testlib/unit:unit_nonfree",
            requirement("pypdf"),
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "update_config_ultimate",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/update_config/**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        ":conftest_update_config",
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/update_config:cmk_update_config_ultimate",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "update_config_ultimatemt",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/update_config/**/nonfree/**/ultimatemt/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/update_config:cmk_update_config_ultimatemt",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "testlib_cloud",
    srcs = ["__test__.py"] + glob(
        include = ["testlib/**/nonfree/**/cloud/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        "//tests:testlib",  # TODO: this needs to be split up
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
        requirement("pyjwt"),
        requirement("fastapi"),
    ],
)

py_test(
    name = "repo_community",
    # https://bazel.build/reference/be/common-definitions#test.size
    size = "large",
    # This is the "catch all" target. Don't add new stuff here.
    srcs = [
        "__init__.py",
        "__test__.py",
        "agents/plugins/test_user_agent.py",
    ] + glob(
        include = [
            "cmk/*.py",
            "cmk/automations/**/*.py",
            "cmk/bi/**/*.py",
            "cmk/checkengine/**/*.py",
            "cmk/diagnostics/**/*.py",
            "cmk/diskspace/**/*.py",
            "cmk/fields/**/*.py",
            "cmk/inventory/**/*.py",
            "cmk/legacy_checks/**/*.py",
            "cmk/legacy_includes/**/*.py",
            "cmk/notifications/**/*.py",
            "cmk/piggyback_hub/**/*.py",
            "cmk/piggyback/**/*.py",
            "cmk/product_usage/**/*.py",
            "cmk/server_side_calls_backend/**/*.py",
            "cmk/snmplib/**/*.py",
            "cmk/special_agents/**/*.py",
            "livestatus/**/*.py",
        ],
        exclude = ["**/nonfree/**"],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"] + glob(
        include = [
            # canned data
            "**/tree_test_data/**",
            "**/*.json",
        ],
        exclude = ["**/*.py"],
    ),
    main = ":__test__.py",
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        "//agents/plugins:apache_status",
        "//agents/plugins:nginx_status",
        "//cmk:cmkpasswd",
        "//cmk/legacy_checks:cmk_legacy_checks",
        "//cmk/legacy_includes:cmk_legacy_includes",
        "//cmk/product_usage:product_usage_cli",
        "//cmk/special_agents:cmk_special_agents",
        "//packages/cmk-ccc:observer",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-plugin-apis:agent_based",
        "//packages/cmk-plugins:lib",
        requirement("exchangelib"),
        requirement("fakeredis"),
        requirement("feedparser"),
        requirement("google-cloud-monitoring"),
        requirement("marshmallow"),
        requirement("polyfactory"),
        requirement("pysmb"),
        requirement("pytest-asyncio"),
        requirement("pytest-mock"),
        requirement("pytest-random-order"),
        requirement("python-snap7"),
        requirement("requests"),
        requirement("responses"),
        requirement("time-machine"),
        requirement("vcrpy"),
        requirement("werkzeug"),
        "//tests/testlib/unit:unit_free",
    ],
)

py_test(
    name = "repo_pro",
    # https://bazel.build/reference/be/common-definitions#test.size
    size = "large",
    # This is the "catch all" target. Don't add new stuff here.
    srcs = [
        "__init__.py",
        "__test__.py",
    ] + glob(
        include = [
            "cmk/nonfree/pro/**/*.py",
        ],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        requirement("flask"),
        requirement("polyfactory"),
        requirement("pytest-asyncio"),
        requirement("pytest-mock"),
        requirement("pytest-random-order"),
        "//tests/testlib/unit:unit_free",
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/base/nonfree:pro",
            "//cmk/utils:pro",
            "//non-free/packages/cmk-bakery",
            "//tests/testlib/unit:unit_nonfree",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "repo_ultimate",
    # https://bazel.build/reference/be/common-definitions#test.size
    size = "large",
    # This is the "catch all" target. Don't add new stuff here.
    srcs = [
        "__init__.py",
        "__test__.py",
    ] + glob(
        include = [
            "cmk/nonfree/ultimate/**/*.py",
        ],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        requirement("flask"),
        requirement("pytest-asyncio"),
        requirement("pytest-mock"),
        requirement("pytest-random-order"),
        requirement("requests"),
        requirement("numpy"),
        requirement("pypdf"),
        requirement("roman"),
        requirement("pysaml2"),
        "//tests/testlib/unit:unit_free",
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/nonfree/ultimate/metric_backend",
            "//non-free/packages/cmk-bakery",
            "//non-free/packages/cmk-dcd:gui",
            "//non-free/packages/cmk-liveproxyd:gui",
            "//non-free/packages/cmk-metric-backend:cmk-metric-backend-fetcher",
            "//non-free/packages/cmk-mknotifyd",
            "//non-free/packages/cmk-otel-collector",
            "//non-free/packages/cmk-robotmk:gui",
        ],
        "@//:gpl_repo": [],
    }),
)
