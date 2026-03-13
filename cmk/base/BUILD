load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

exports_files([".f12"])

py_library(
    name = "utils",
    srcs = [
        "profiling.py",
        "utils.py",
    ],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        "//cmk/utils",
        "//packages/cmk-ccc:exceptions",
    ],
)

py_library(
    name = "errorhandling",
    srcs = glob(["errorhandling/**/*.py"]),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/piggyback:backend",
        "//cmk/utils",
        "//packages/cmk-ccc:crash-reporting",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:helper-interface",
        "//packages/cmk-check-engine:snmplib",
    ],
)

py_library(
    name = "sources",
    srcs = glob(["sources/**/*.py"]),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:translations",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:helper-interface",
        "//packages/cmk-check-engine:snmplib",
    ],
)

py_library(
    name = "events",
    srcs = ["events.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        "//cmk/utils",
        "//packages/cmk-ccc:daemon",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:regex",
        "//packages/cmk-ccc:site",
        "//packages/cmk-events",
        "//packages/cmk-livestatus-client:py_livestatus",
    ],
)

py_library(
    name = "parent-scan",
    srcs = ["parent_scan.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        "//cmk/automations:cmk_automations",
        "//cmk/utils",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:tty",
    ],
)

py_library(
    name = "snmp-plugin-store",
    srcs = ["snmp_plugin_store.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        "//cmk/checkengine:cmk_checkengine",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:snmplib",
    ],
)

py_library(
    name = "default-config",
    srcs = glob(["default_config/**/*.py"]),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/inventory:cmk_inventory",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:snmplib",
    ],
)

py_library(
    name = "api",
    srcs = glob(["api/**/*.py"]),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        "//cmk/utils",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-plugin-apis:bakery",
    ],
)

py_library(
    name = "plugins-bakery",
    srcs = glob([
        "cee/plugins/**/*.py",
        "plugins/**/*.py",
    ]),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":api",
        "//cmk/utils",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-plugin-apis:bakery",
        requirement("pyyaml"),
    ],
)

py_library(
    name = "configlib",
    srcs = glob(["configlib/**/*.py"]),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
        "//tests:__subpackages__",
    ],
    deps = [
        ":default-config",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/piggyback:backend",
        "//cmk/rrd:cmk_rrd",
        "//cmk/utils",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:translations",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-logwatch:config",
        "//packages/cmk-plugin-apis:agent_based",
    ],
)

py_library(
    name = "config",
    srcs = ["config.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
        "//cmk/product_usage:__pkg__",
        "//cmk/update_config:__pkg__",
        "//tests:__subpackages__",
    ],
    deps = [
        ":configlib",
        ":default-config",
        ":parent-scan",
        ":snmp-plugin-store",
        ":sources",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/inventory:cmk_inventory",
        "//cmk/piggyback:backend",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:regex",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:helper-interface",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-plugin-apis:agent_based",
        "//packages/cmk-plugin-apis:password_store",
        "//packages/cmk-plugin-apis:server_side_calls",
        "//packages/cmk-trace",
    ],
)

py_library(
    name = "core",
    srcs = glob(
        include = ["core/**/*.py"],
        exclude = ["core/nagios/_host_check_template.py"],
    ),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":config",
        ":configlib",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/core_client:cmk_core_client",
        "//cmk/utils",
        "//packages/cmk-ccc:config-path",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:store",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-plugin-apis:discover_plugins",
        "//packages/cmk-plugin-apis:password_store",
        "//packages/cmk-plugin-apis:server_side_calls",
        "//packages/cmk-trace",
    ],
)

py_library(
    name = "checkers",
    srcs = ["checkers.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":config",
        ":errorhandling",
        ":sources",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils",
        "//packages/cmk-ccc:cpu-tracking",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:resulttype",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:helper-interface",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-livestatus-client:py_livestatus",
        "//packages/cmk-plugin-apis:agent_based",
    ],
)

py_library(
    name = "dump-host",
    srcs = ["dump_host.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":config",
        ":configlib",
        ":sources",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:helper-interface",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-plugin-apis:password_store",
    ],
)

py_library(
    name = "automations",
    srcs = glob(["automations/**/*.py"]),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":checkers",
        ":config",
        ":configlib",
        ":core",
        ":errorhandling",
        ":parent-scan",
        ":snmp-plugin-store",
        ":sources",
        ":utils",
        "//cmk/automations:cmk_automations",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/core_client:cmk_core_client",
        "//cmk/inventory:cmk_inventory",
        "//cmk/piggyback:backend",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils",
        "//packages/cmk-ccc:cleanup",
        "//packages/cmk-ccc:config-path",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:timeout",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:helper-interface",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-livestatus-client:py_livestatus",
        "//packages/cmk-plugin-apis:agent_based",
        "//packages/cmk-plugin-apis:discover_plugins",
        "//packages/cmk-plugin-apis:password_store",
        "//packages/cmk-plugin-apis:server_side_calls",
        "//packages/cmk-trace",
    ],
)

py_library(
    name = "modes-registry",
    srcs = ["modes/modes.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        "//cmk/utils",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-trace",
    ],
)

py_library(
    name = "base-app",
    srcs = ["base_app.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":automations",
        ":config",
        ":configlib",
        ":core",
        ":modes-registry",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/utils",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:helper-interface",
    ],
)

py_library(
    name = "modes",
    srcs = [
        "modes/call.py",
        "modes/check_mk.py",
    ],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":base-app",
        ":checkers",
        ":config",
        ":configlib",
        ":core",
        ":dump-host",
        ":errorhandling",
        ":modes-registry",
        ":snmp-plugin-store",
        ":sources",
        ":utils",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/inventory:cmk_inventory",
        "//cmk/piggyback:backend",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils",
        "//packages/cmk-ccc:cleanup",
        "//packages/cmk-ccc:config-path",
        "//packages/cmk-ccc:cpu-tracking",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:store",
        "//packages/cmk-ccc:timeout",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:helper-interface",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-livestatus-client:py_livestatus",
        "//packages/cmk-plugin-apis:agent_based",
        "//packages/cmk-plugin-apis:discover_plugins",
        "//packages/cmk-plugin-apis:password_store",
        "//packages/cmk-plugin-apis:server_side_calls",
        "//packages/cmk-trace",
    ],
)

py_library(
    name = "notify",
    srcs = ["notify.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":automations",
        ":base-app",
        ":config",
        ":events",
        ":modes-registry",
        ":utils",
        "//cmk/automations:cmk_automations",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/utils",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:regex",
        "//packages/cmk-ccc:store",
        "//packages/cmk-ccc:timeout",
        "//packages/cmk-ccc:version",
        "//packages/cmk-events",
        "//packages/cmk-livestatus-client:py_livestatus",
    ],
)

py_library(
    name = "diagnostics",
    srcs = ["diagnostics.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":automations",
        ":base-app",
        ":config",
        ":configlib",
        ":modes-registry",
        "//cmk/automations:cmk_automations",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/diagnostics:cmk_diagnostics",
        "//cmk/inventory:cmk_inventory",
        "//cmk/utils",
        "//packages/cmk-ccc:crash-reporting",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:i18n",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:store",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:version",
        "//packages/cmk-livestatus-client:py_livestatus",
        requirement("requests"),
    ],
)

py_library(
    name = "localize",
    srcs = ["localize.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":base-app",
        ":modes-registry",
        "//cmk/utils",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:tty",
    ],
)

py_library(
    name = "community-app",
    srcs = ["community_app.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":automations",
        ":base-app",
        ":core",
        ":diagnostics",
        ":localize",
        ":modes",
        ":modes-registry",
        ":notify",
        "//cmk/utils",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
    ],
)

py_library(
    name = "app",
    srcs = ["app.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
        "//cmk/product_usage:__pkg__",
        "//cmk/update_config:__pkg__",
        "//tests:__subpackages__",
    ],
    deps = [
        ":base-app",
        ":community-app",
        "//packages/cmk-ccc:version",
    ],
)

py_library(
    name = "automation-helper",
    srcs = glob(["automation_helper/**/*.py"]),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":app",
        ":automations",
        ":config",
        "//cmk/automations:cmk_automations",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/utils",
        "//packages/cmk-ccc:daemon",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:version",
        "//packages/cmk-trace",
        requirement("fastapi"),
        requirement("opentelemetry-api"),
        requirement("opentelemetry-sdk"),
        requirement("opentelemetry-instrumentation-fastapi"),
        requirement("pydantic"),
        requirement("redis"),
        requirement("setproctitle"),
        requirement("uvicorn"),
        requirement("watchdog"),
    ],
)

py_library(
    name = "host-check-template",
    srcs = ["core/nagios/_host_check_template.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":app",
        ":config",
        ":core",
        ":modes",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils",
        "//packages/cmk-ccc:config-path",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-plugin-apis:discover_plugins",
    ],
)

py_library(
    name = "check-cmk-inv",
    srcs = ["check_cmk_inv.py"],
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/base:__subpackages__",
    ],
    deps = [
        ":app",
        ":base-app",
        ":checkers",
        ":config",
        ":configlib",
        ":core",
        ":errorhandling",
        ":modes",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils",
        "//packages/cmk-ccc:config-path",
        "//packages/cmk-ccc:cpu-tracking",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-plugin-apis:discover_plugins",
    ],
)

py_library(
    name = "base",
    srcs = [],
    imports = ["../.."],
    visibility = [
        "//cmk:__subpackages__",
        "//tests:__subpackages__",
    ],
    deps = [
        ":api",
        ":app",
        ":automation-helper",
        ":automations",
        ":base-app",
        ":check-cmk-inv",
        ":checkers",
        ":community-app",
        ":config",
        ":configlib",
        ":core",
        ":default-config",
        ":diagnostics",
        ":dump-host",
        ":errorhandling",
        ":events",
        ":host-check-template",
        ":localize",
        ":modes",
        ":modes-registry",
        ":notify",
        ":parent-scan",
        ":plugins-bakery",
        ":snmp-plugin-store",
        ":sources",
        ":utils",
    ],
)
