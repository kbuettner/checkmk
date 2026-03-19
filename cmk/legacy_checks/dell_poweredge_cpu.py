#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Sequence

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    StringTable,
)
from cmk.plugins.dell.lib import DETECT_IDRAC_POWEREDGE

_STATE_TABLE = {
    "1": (State.WARN, "other"),
    "2": (State.WARN, "unknown"),
    "3": (State.OK, ""),
    "4": (State.WARN, "non-critical"),
    "5": (State.CRIT, "critical"),
    "6": (State.CRIT, "non-recoverable"),
}


def discover_dell_poweredge_cpu(section: Sequence[StringTable]) -> DiscoveryResult:
    for _chassisIndex, _Index, StateSettings, _Status, LocationName in section[0]:
        if LocationName != "" and StateSettings != "1":
            yield Service(item=LocationName)


def check_dell_poweredge_cpu(item: str, section: Sequence[StringTable]) -> CheckResult:
    for chassisIndex, Index, _StateSettings, Status, LocationName in section[0]:
        if item == LocationName:
            brand_name = None
            for line in section[1]:
                if line[0] == chassisIndex and line[1] == Index:
                    brand_name = line[2]

            state, status_txt = _STATE_TABLE.get(Status, (State.CRIT, "unknown state"))
            summary = " ".join(p for p in [status_txt, brand_name] if p) or "OK"
            yield Result(state=state, summary=summary)
            return


def parse_dell_poweredge_cpu(string_table: Sequence[StringTable]) -> Sequence[StringTable]:
    return string_table


snmp_section_dell_poweredge_cpu = SNMPSection(
    name="dell_poweredge_cpu",
    detect=DETECT_IDRAC_POWEREDGE,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.674.10892.5.4.1100.32.1",
            oids=["1", "2", "4", "5", "7"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.674.10892.5.4.1100.30.1",
            oids=["1", "2", "23"],
        ),
    ],
    parse_function=parse_dell_poweredge_cpu,
)
check_plugin_dell_poweredge_cpu = CheckPlugin(
    name="dell_poweredge_cpu",
    service_name="%s",
    discovery_function=discover_dell_poweredge_cpu,
    check_function=check_dell_poweredge_cpu,
)
