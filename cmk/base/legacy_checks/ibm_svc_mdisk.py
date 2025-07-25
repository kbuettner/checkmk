#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


# mypy: disable-error-code="var-annotated"

from cmk.agent_based.legacy.v0_unstable import LegacyCheckDefinition
from cmk.base.check_legacy_includes.ibm_svc import parse_ibm_svc_with_header

check_info = {}

# Example output from agent:
# <<<ibm_svc_mdisk:sep(58)>>>
# 0:stp5_300G_01-01:online:managed:16:stp5_300G_01:1.1TB:0000000000000000:BLUBB5:600a0b80006e1dbc0000f6f9513026a000000000000000000000000000000000:generic_hdd
# 1:Quorum_BLUBB3:online:managed:0:Quorum_2:1.0GB:0000000000000000:BLUBB3:600a0b8000293eb800001f264c3e8a1f00000000000000000000000000000000:generic_hdd
# 2:stp6_300G_01-01:online:managed:15:stp6_300G_01:1.1TB:0000000000000000:BLUBB6:600a0b80006e8e3c00000f1651302b8800000000000000000000000000000000:generic_hdd
# 3:Quorum_blubb5:online:managed:18:Quorum_0:1.0GB:0000000000000001:BLUBB5:600a0b80006e1dcc0000f6905130225800000000000000000000000000000000:generic_hdd
# 4:Quorum_blubb6:online:managed:17:Quorum_1:1.0GB:0000000000000001:BLUBB6:600a0b80006e1d5e00000dcb5130228700000000000000000000000000000000:generic_hdd
# 5:stp5_300G_01-02:online:managed:16:stp5_300G_01:1.1TB:0000000000000002:BLUBB5:600a0b80006e1dbc0000f6fc51304bfc00000000000000000000000000000000:generic_hdd
# 6:stp6_300G_01-02:online:managed:15:stp6_300G_01:1.1TB:0000000000000002:BLUBB6:600a0b80006e8e3c00000f1951304f9a00000000000000000000000000000000:generic_hdd
# 7:stp5_300G_01-03:online:managed:16:stp5_300G_01:1.1TB:0000000000000003:BLUBB5:600a0b80006e1dcc0000f76951305bc000000000000000000000000000000000:generic_hdd
# 8:stp6_300G_01-03:online:managed:15:stp6_300G_01:1.1TB:0000000000000003:BLUBB6:600a0b80006e1d5e00000e9a51305a3200000000000000000000000000000000:generic_hdd
# 9:stp5_300G_01-04:online:managed:16:stp5_300G_01:1.1TB:0000000000000004:BLUBB5:600a0b80006e1dbc0000f7d051341cc000000000000000000000000000000000:generic_hdd


def parse_ibm_svc_mdisk(string_table):
    dflt_header = [
        "id",
        "name",
        "status",
        "mode",
        "mdisk_grp_id",
        "mdisk_grp_name",
        "capacity",
        "ctrl_LUN_#",
        "controller_name",
        "UID",
        "tier",
        "encrypt",
        "site_id",
        "site_name",
        "distributed",
        "dedupe",
    ]
    parsed = {}
    for rows in parse_ibm_svc_with_header(string_table, dflt_header).values():
        try:
            data = rows[0]
            parsed.setdefault(data["name"], data)
        except (KeyError, IndexError):
            continue
    return parsed


def inventory_ibm_svc_mdisk(parsed):
    for mdisk_name in parsed:
        yield mdisk_name, {}


def check_ibm_svc_mdisk(item, params, parsed):
    if not (data := parsed.get(item)):
        return
    mdisk_status = data["status"]
    yield params.get("%s_state" % mdisk_status, 1), "Status: %s" % mdisk_status

    mdisk_mode = data["mode"]
    yield params.get("%s_mode" % mdisk_mode, 1), "Mode: %s" % mdisk_mode


check_info["ibm_svc_mdisk"] = LegacyCheckDefinition(
    name="ibm_svc_mdisk",
    parse_function=parse_ibm_svc_mdisk,
    service_name="MDisk %s",
    discovery_function=inventory_ibm_svc_mdisk,
    check_function=check_ibm_svc_mdisk,
    check_ruleset_name="ibm_svc_mdisk",
    check_default_parameters={
        "online_state": 0,  # online state is OK
        "degraded_state": 1,  # degraded state is WARN
        "offline_state": 2,  # offline state is CRIT
        "excluded_state": 2,  # excluded state is CRIT
        "managed_mode": 0,  # managed mode is OK
        "array_mode": 0,  # array mode is OK
        "image_mode": 0,  # image mode is OK
        "unmanaged_mode": 1,  # unmanaged mode is WARN
    },
)
