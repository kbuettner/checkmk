#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    startswith,
    State,
    StringTable,
)


def parse_packeteer_ps_status(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_packeteer_ps_status = SimpleSNMPSection(
    name="packeteer_ps_status",
    parse_function=parse_packeteer_ps_status,
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.2334"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.2334.2.1.5",
        oids=["8", "10"],
    ),
)


def discover_packeteer_ps_status(section: StringTable) -> DiscoveryResult:
    if section:
        yield Service()


def check_packeteer_ps_status(section: StringTable) -> CheckResult:
    for nr, ps_status in enumerate(section[0]):
        if ps_status == "1":
            yield Result(state=State.OK, summary=f"Power Supply {nr} okay")
        else:
            yield Result(state=State.CRIT, summary=f"Power Supply {nr} not okay")


check_plugin_packeteer_ps_status = CheckPlugin(
    name="packeteer_ps_status",
    service_name="Power Supply Status",
    discovery_function=discover_packeteer_ps_status,
    check_function=check_packeteer_ps_status,
)
