#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# <<<sansymphony_virtualdiskstatus>>>
# testvmfs01 Online
# vmfs10 Online


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

Section = dict[str, str]


def parse_sansymphony_virtualdiskstatus(string_table: StringTable) -> Section:
    parsed: Section = {}
    for line in string_table:
        parsed.setdefault(line[0], " ".join(line[1:]))
    return parsed


agent_section_sansymphony_virtualdiskstatus = AgentSection(
    name="sansymphony_virtualdiskstatus",
    parse_function=parse_sansymphony_virtualdiskstatus,
)


def discover_sansymphony_virtualdiskstatus(section: Section) -> DiscoveryResult:
    yield from (Service(item=item) for item in section)


def check_sansymphony_virtualdiskstatus(item: str, section: Section) -> CheckResult:
    if not (data := section.get(item)):
        return
    state = State.OK if data == "Online" else State.CRIT
    yield Result(state=state, summary=f"Volume state is: {data}")


check_plugin_sansymphony_virtualdiskstatus = CheckPlugin(
    name="sansymphony_virtualdiskstatus",
    service_name="sansymphony Virtual Disk %s",
    discovery_function=discover_sansymphony_virtualdiskstatus,
    check_function=check_sansymphony_virtualdiskstatus,
)
