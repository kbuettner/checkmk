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


def parse_packeteer_fan_status(string_table: StringTable) -> StringTable | None:
    return string_table or None


snmp_section_packeteer_fan_status = SimpleSNMPSection(
    name="packeteer_fan_status",
    parse_function=parse_packeteer_fan_status,
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.2334"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.2334.2.1.5",
        oids=["12", "14", "22", "24"],
    ),
)


def discover_packeteer_fan_status(section: StringTable) -> DiscoveryResult:
    for nr, fan_status in enumerate(section[0]):
        if fan_status in ["1", "2"]:
            yield Service(item=f"{nr}")


def check_packeteer_fan_status(item: str, section: StringTable) -> CheckResult:
    fan_status = section[0][int(item)]
    if fan_status == "1":
        yield Result(state=State.OK, summary="OK")
    elif fan_status == "2":
        yield Result(state=State.CRIT, summary="Not OK")
    elif fan_status == "3":
        yield Result(state=State.CRIT, summary="Not present")


check_plugin_packeteer_fan_status = CheckPlugin(
    name="packeteer_fan_status",
    service_name="Fan Status %s",
    discovery_function=discover_packeteer_fan_status,
    check_function=check_packeteer_fan_status,
)
