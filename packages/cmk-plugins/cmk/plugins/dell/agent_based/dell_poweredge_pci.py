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


def discover_dell_poweredge_pci(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[4] != "":
            yield Service(item=line[4])


def check_dell_poweredge_pci(item: str, section: StringTable) -> CheckResult:
    for status, bus_width, mfr, description, fqdd in section:
        if item == fqdd:
            state, status_txt = _STATE_TABLE.get(status, (State.CRIT, "unknown state"))
            details = {"BusWidth": bus_width, "MFR": mfr, "Desc.": description}
            parts = [status_txt] + [f"{k}: {v}" for k, v in details.items()]
            summary = ", ".join(p for p in parts if p)
            yield Result(state=state, summary=summary)
            return
    yield Result(state=State.UNKNOWN, summary="PCI Device not found")


def parse_dell_poweredge_pci(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_dell_poweredge_pci = SimpleSNMPSection(
    name="dell_poweredge_pci",
    detect=DETECT_IDRAC_POWEREDGE,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.674.10892.5.4.1100.80.1",
        oids=["5", "7", "8", "9", "12"],
    ),
    parse_function=parse_dell_poweredge_pci,
)
check_plugin_dell_poweredge_pci = CheckPlugin(
    name="dell_poweredge_pci",
    service_name="PCI %s",
    discovery_function=discover_dell_poweredge_pci,
    check_function=check_dell_poweredge_pci,
)
