#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    any_of,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    OIDEnd,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    startswith,
    State,
    StringTable,
)


def parse_qlogic_sanbox_fabric_element(string_table: StringTable) -> StringTable:
    return string_table


def discover_qlogic_sanbox_fabric_element(section: StringTable) -> DiscoveryResult:
    for _fe_status, fe_id in section:
        yield Service(item=fe_id)


def check_qlogic_sanbox_fabric_element(item: str, section: StringTable) -> CheckResult:
    for fe_status, fe_id in section:
        if fe_id == item:
            if fe_status == "1":
                yield Result(state=State.OK, summary=f"Fabric Element {fe_id} is online")
            elif fe_status == "2":
                yield Result(state=State.CRIT, summary=f"Fabric Element {fe_id} is offline")
            elif fe_status == "3":
                yield Result(state=State.WARN, summary=f"Fabric Element {fe_id} is testing")
            elif fe_status == "4":
                yield Result(state=State.CRIT, summary=f"Fabric Element {fe_id} is faulty")
            else:
                yield Result(
                    state=State.UNKNOWN,
                    summary=f"Fabric Element {fe_id} is in unidentified status {fe_status}",
                )
            return

    yield Result(state=State.UNKNOWN, summary=f"No Fabric Element {item} found")


snmp_section_qlogic_sanbox_fabric_element = SimpleSNMPSection(
    name="qlogic_sanbox_fabric_element",
    parse_function=parse_qlogic_sanbox_fabric_element,
    detect=any_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.3873.1.14"),
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.3873.1.8"),
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.2.1.75.1.1.4.1",
        oids=["4", OIDEnd()],
    ),
)

check_plugin_qlogic_sanbox_fabric_element = CheckPlugin(
    name="qlogic_sanbox_fabric_element",
    service_name="Fabric Element %s",
    discovery_function=discover_qlogic_sanbox_fabric_element,
    check_function=check_qlogic_sanbox_fabric_element,
)
