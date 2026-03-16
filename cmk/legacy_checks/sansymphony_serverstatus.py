#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# <<<sansymphony_serverstatus>>>
# Online WritebackGlobal


from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
)


def parse_sansymphony_serverstatus(string_table: StringTable) -> StringTable:
    return string_table


agent_section_sansymphony_serverstatus = AgentSection(
    name="sansymphony_serverstatus",
    parse_function=parse_sansymphony_serverstatus,
)


def discover_sansymphony_serverstatus(section: StringTable) -> DiscoveryResult:
    if section:
        yield Service()


def check_sansymphony_serverstatus(section: StringTable) -> CheckResult:
    if not section:
        return
    status, cachestate = section[0]
    if status == "Online" and cachestate == "WritebackGlobal":
        yield Result(
            state=State.OK,
            summary=f"SANsymphony is {status} and its cache is in {cachestate} mode",
        )
    elif status == "Online" and cachestate != "WritebackGlobal":
        yield Result(
            state=State.WARN,
            summary=f"SANsymphony is {status} but its cache is in {cachestate} mode",
        )
    else:
        yield Result(state=State.CRIT, summary=f"SANsymphony is {status}")


check_plugin_sansymphony_serverstatus = CheckPlugin(
    name="sansymphony_serverstatus",
    service_name="sansymphony Serverstatus",
    discovery_function=discover_sansymphony_serverstatus,
    check_function=check_sansymphony_serverstatus,
)
