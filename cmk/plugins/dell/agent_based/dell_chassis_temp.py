#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)
from cmk.plugins.dell.lib import DETECT_CHASSIS
from cmk.plugins.lib.temperature import check_temperature, TempParamType

_ITEMS = {
    "Front Panel": 0,
    "CMC Ambient": 1,
    "CMC Processor": 2,
}


def discover_dell_chassis_temp(section: StringTable) -> DiscoveryResult:
    if section and len(section[0]) == 3:
        yield Service(item="Front Panel")
        yield Service(item="CMC Ambient")
        yield Service(item="CMC Processor")


def check_dell_chassis_temp(item: str, params: TempParamType, section: StringTable) -> CheckResult:
    if item in _ITEMS:
        yield from check_temperature(
            reading=float(section[0][_ITEMS[item]]),
            params=params,
            unique_name=f"dell_chassis_temp_{item}",
            value_store=get_value_store(),
        )
        return

    yield Result(state=State.UNKNOWN, summary="Sensor not found in SNMP data")


def parse_dell_chassis_temp(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_dell_chassis_temp = SimpleSNMPSection(
    name="dell_chassis_temp",
    detect=DETECT_CHASSIS,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.674.10892.2.3.1",
        oids=["10", "11", "12"],
    ),
    parse_function=parse_dell_chassis_temp,
)


check_plugin_dell_chassis_temp = CheckPlugin(
    name="dell_chassis_temp",
    service_name="Temperature %s",
    discovery_function=discover_dell_chassis_temp,
    check_function=check_dell_chassis_temp,
    check_ruleset_name="temperature",
    check_default_parameters={"levels": (60.0, 80.0)},
)
