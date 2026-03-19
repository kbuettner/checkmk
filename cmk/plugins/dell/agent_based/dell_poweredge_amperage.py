#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)
from cmk.plugins.dell.lib import DETECT_IDRAC_POWEREDGE

_STATE_TABLE = {
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


def discover_dell_poweredge_amperage_power(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[6] != "" and line[5] in ("24", "26"):
            yield Service(item=line[6])


def discover_dell_poweredge_amperage_current(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[6] != "" and line[5] in ("23", "25"):
            yield Service(item=line[6])


def _check_dell_poweredge_amperage(item: str, section: StringTable) -> CheckResult:
    for (
        _chassisIndex,
        _Index,
        StateSettings,
        Status,
        Reading,
        ProbeType,
        LocationName,
        UpperCritical,
        UpperNonCritical,
    ) in section:
        if item == LocationName:
            if StateSettings == "1":
                yield Result(state=State.UNKNOWN, summary="Object's state is unknown")
                return
            state, state_txt = _STATE_TABLE.get(Status, (State.CRIT, "unknown state"))

            if UpperNonCritical and UpperCritical:
                limittext = f" (upper limits {UpperNonCritical}/{UpperCritical})"
            else:
                limittext = ""

            if ProbeType in ("23", "25"):  # Amps
                current = int(Reading) / 10.0
                yield Result(state=state, summary=f"{current} Ampere {state_txt}{limittext}")
                yield Metric("current", current)
            elif ProbeType in ("24", "26"):  # Watts
                yield Result(state=state, summary=f"{Reading} Watt {state_txt}{limittext}")
                yield Metric("power", float(Reading))
            else:
                yield Result(state=State.UNKNOWN, summary=f"Unknown Probe Type {ProbeType}")
            return
    yield Result(state=State.UNKNOWN, summary="Amperage Device not found")


def check_dell_poweredge_amperage_power(item: str, section: StringTable) -> CheckResult:
    yield from _check_dell_poweredge_amperage(item, section)


def check_dell_poweredge_amperage_current(item: str, section: StringTable) -> CheckResult:
    yield from _check_dell_poweredge_amperage(item, section)


def parse_dell_poweredge_amperage(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_dell_poweredge_amperage = SimpleSNMPSection(
    name="dell_poweredge_amperage",
    detect=DETECT_IDRAC_POWEREDGE,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.674.10892.5.4.600.30.1",
        oids=["1", "2", "4", "5", "6", "7", "8", "10", "11"],
    ),
    parse_function=parse_dell_poweredge_amperage,
)
check_plugin_dell_poweredge_amperage_power = CheckPlugin(
    name="dell_poweredge_amperage_power",
    service_name="%s",
    sections=["dell_poweredge_amperage"],
    discovery_function=discover_dell_poweredge_amperage_power,
    check_function=check_dell_poweredge_amperage_power,
)
check_plugin_dell_poweredge_amperage_current = CheckPlugin(
    name="dell_poweredge_amperage_current",
    service_name="%s",
    sections=["dell_poweredge_amperage"],
    discovery_function=discover_dell_poweredge_amperage_current,
    check_function=check_dell_poweredge_amperage_current,
)
