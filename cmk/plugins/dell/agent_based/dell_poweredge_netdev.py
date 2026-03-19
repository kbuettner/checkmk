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

_DEV_STATE_TABLE = {
    "1": (State.WARN, "other,"),
    "2": (State.WARN, "unknown,"),
    "3": (State.OK, ""),
    "4": (State.WARN, "nonCritical,"),
    "5": (State.CRIT, "Critical,"),
    "6": (State.CRIT, "NonRecoverable,"),
}

_CONN_STATE_TABLE = {
    "1": (State.OK, "connected,"),
    "2": (State.CRIT, "disconnected,"),
    "3": (State.CRIT, "driverBad,"),
    "4": (State.CRIT, "driverDisabled,"),
    "10": (State.CRIT, "hardwareInitializing,"),
    "11": (State.CRIT, "hardwareResetting,"),
    "12": (State.CRIT, "hardwareClosing,"),
    "13": (State.CRIT, "hardwareNotReady,"),
}


def discover_dell_poweredge_netdev(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[1] != "2" and line[4] != "":
            yield Service(item=line[4])


def check_dell_poweredge_netdev(item: str, section: StringTable) -> CheckResult:
    for status, connection_status, product, cur_mac, fqdd in section:
        if item == fqdd:
            mac = "-".join("%02X" % ord(c) for c in cur_mac).strip()
            dev_state, dev_state_txt = _DEV_STATE_TABLE.get(
                status, (State.CRIT, "unknown device status,")
            )
            conn_state, conn_state_txt = _CONN_STATE_TABLE.get(connection_status, (State.OK, ""))
            state = State.worst(dev_state, conn_state)
            parts = [dev_state_txt, conn_state_txt, f"Product: {product},", f"MAC: {mac}"]
            summary = " ".join(p for p in parts if p)
            yield Result(state=state, summary=summary)
            return
    yield Result(state=State.UNKNOWN, summary="network device not found")


def parse_dell_poweredge_netdev(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_dell_poweredge_netdev = SimpleSNMPSection(
    name="dell_poweredge_netdev",
    detect=DETECT_IDRAC_POWEREDGE,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.674.10892.5.4.1100.90.1",
        oids=["3", "4", "6", "15", "30"],
    ),
    parse_function=parse_dell_poweredge_netdev,
)
check_plugin_dell_poweredge_netdev = CheckPlugin(
    name="dell_poweredge_netdev",
    service_name="%s",
    discovery_function=discover_dell_poweredge_netdev,
    check_function=check_dell_poweredge_netdev,
)
