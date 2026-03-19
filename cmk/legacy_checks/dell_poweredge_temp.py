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
from cmk.plugins.dell.lib import DETECT_IDRAC_POWEREDGE
from cmk.plugins.lib.temperature import check_temperature, TempParamType

_STATUS_TABLE = {
    "1": (State.WARN, "other"),
    "2": (State.WARN, "unknown"),
    "3": (State.OK, ""),
    "4": (State.WARN, "nonCriticalUpper"),
    "5": (State.CRIT, "CriticalUpper"),
    "6": (State.CRIT, "NonRecoverableUpper"),
    "7": (State.WARN, "nonCriticalLower"),
    "8": (State.CRIT, "CriticalLower"),
    "9": (State.CRIT, "NonRecoverableLower"),
    "10": (State.CRIT, "failed"),
}


def _dell_poweredge_temp_makeitem(chassisIndex: str, Index: str, LocationName: str) -> str:
    item = LocationName if LocationName else f"{chassisIndex}-{Index}"
    if item.endswith(" Temp"):
        item = item[:-5]
    return item


def discover_dell_poweredge_temp(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[2] != "1":  # StateSettings not 'unknown'
            yield Service(item=_dell_poweredge_temp_makeitem(line[0], line[1], line[5]))


def check_dell_poweredge_temp(
    item: str, params: TempParamType, section: StringTable
) -> CheckResult:
    for (
        chassisIndex,
        Index,
        _StateSettings,
        Status,
        Reading,
        LocationName,
        UpperCritical,
        UpperNonCritical,
        LowerNonCritical,
        LowerCritical,
    ) in section:
        if not Reading:
            continue
        if item == _dell_poweredge_temp_makeitem(chassisIndex, Index, LocationName):
            temp = int(Reading) / 10.0

            dev_levels: tuple[float, float] | None
            if UpperNonCritical and UpperCritical:
                dev_levels = (int(UpperNonCritical) / 10.0, int(UpperCritical) / 10.0)
            else:
                dev_levels = None

            dev_levels_lower: tuple[float, float] | None
            if LowerNonCritical and LowerCritical:
                dev_levels_lower = (int(LowerNonCritical) / 10.0, int(LowerCritical) / 10.0)
            else:
                dev_levels_lower = None

            state, state_txt = _STATUS_TABLE.get(Status, (State.CRIT, "unknown state"))
            if state != State.OK:
                yield Result(state=state, summary=state_txt)

            yield from check_temperature(
                temp,
                params,
                unique_name=f"dell_poweredge_temp_{item}",
                value_store=get_value_store(),
                dev_levels=dev_levels,
                dev_levels_lower=dev_levels_lower,
            )
            return


def parse_dell_poweredge_temp(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_dell_poweredge_temp = SimpleSNMPSection(
    name="dell_poweredge_temp",
    detect=DETECT_IDRAC_POWEREDGE,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.674.10892.5.4.700.20.1",
        oids=["1", "2", "4", "5", "6", "8", "10", "11", "12", "13"],
    ),
    parse_function=parse_dell_poweredge_temp,
)
check_plugin_dell_poweredge_temp = CheckPlugin(
    name="dell_poweredge_temp",
    service_name="Temperature %s",
    discovery_function=discover_dell_poweredge_temp,
    check_function=check_dell_poweredge_temp,
    check_ruleset_name="temperature",
    check_default_parameters={},
)
