#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    contains,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)


def discover_superstack3_sensors(section: StringTable) -> DiscoveryResult:
    yield from (Service(item=line[0]) for line in section if line[1] != "not present")


def check_superstack3_sensors(item: str, section: StringTable) -> CheckResult:
    for name, state in section:
        if name == item:
            if state == "failure":
                yield Result(state=State.CRIT, summary=f"status is {state}")
            elif state == "operational":
                yield Result(state=State.OK, summary=f"status is {state}")
            else:
                yield Result(state=State.WARN, summary=f"status is {state}")
            return
    yield Result(state=State.UNKNOWN, summary="UNKOWN - sensor not found")


def parse_superstack3_sensors(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_superstack3_sensors = SimpleSNMPSection(
    name="superstack3_sensors",
    parse_function=parse_superstack3_sensors,
    detect=contains(".1.3.6.1.2.1.1.1.0", "3com superstack 3"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.43.43.1.1",
        oids=["7", "10"],
    ),
)

check_plugin_superstack3_sensors = CheckPlugin(
    name="superstack3_sensors",
    service_name="%s",
    discovery_function=discover_superstack3_sensors,
    check_function=check_superstack3_sensors,
)
