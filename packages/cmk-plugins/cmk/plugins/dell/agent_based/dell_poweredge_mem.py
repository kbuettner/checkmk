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
    State,
    StringTable,
)
from cmk.plugins.dell.lib import DETECT_IDRAC_POWEREDGE

_STATE_TABLE = {
    "1": (State.WARN, "other"),
    "2": (State.WARN, "unknown"),
    "3": (State.OK, ""),
    "4": (State.WARN, "nonCritical"),
    "5": (State.CRIT, "Critical"),
    "6": (State.CRIT, "NonRecoverable"),
}


def discover_dell_poweredge_mem(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[1] != "":
            yield Service(item=line[1])


def check_dell_poweredge_mem(item: str, section: StringTable) -> CheckResult:
    for status, location, size, speed, mfr, part_number, serial_number in section:
        if item == location:
            size_gb = str(int(int(size) / 1024.0 / 1024.0)) + "GB" if size else "0GB"
            state, status_txt = _STATE_TABLE.get(status, (State.CRIT, "unknown state"))
            details = {
                "Size": size_gb,
                "Speed": speed,
                "MFR": mfr,
                "P/N": part_number,
                "S/N": serial_number,
            }
            parts = [status_txt] + [f"{k}: {v}" for k, v in details.items()]
            summary = ", ".join(p for p in parts if p)
            yield Result(state=state, summary=summary)
            return
    yield Result(state=State.UNKNOWN, summary="Memory Device not found")


def parse_dell_poweredge_mem(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_dell_poweredge_mem = SimpleSNMPSection(
    name="dell_poweredge_mem",
    detect=DETECT_IDRAC_POWEREDGE,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.674.10892.5.4.1100.50.1",
        oids=["5", "8", "14", "15", "21", "22", "23"],
    ),
    parse_function=parse_dell_poweredge_mem,
)
check_plugin_dell_poweredge_mem = CheckPlugin(
    name="dell_poweredge_mem",
    service_name="%s",
    discovery_function=discover_dell_poweredge_mem,
    check_function=check_dell_poweredge_mem,
)
