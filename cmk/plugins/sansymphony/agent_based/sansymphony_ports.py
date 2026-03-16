#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# <<<sansymphony_ports>>>
# shdesolssy01_FE1 FibreChannel True
# Server_FC_Port_2 FibreChannel True
# Server_FC_Port_3 FibreChannel False
# Server_FC_Port_4 FibreChannel True
# Server_iSCSI_Port_1 iSCSI True
# Microsoft_iSCSI-Initiator iSCSI True


from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
)


def parse_sansymphony_ports(string_table: StringTable) -> StringTable:
    return string_table


agent_section_sansymphony_ports = AgentSection(
    name="sansymphony_ports",
    parse_function=parse_sansymphony_ports,
)


def discover_sansymphony_ports(section: StringTable) -> DiscoveryResult:
    for portname, _porttype, portstatus in section:
        if portstatus == "True":
            yield Service(item=portname)


def check_sansymphony_ports(item: str, section: StringTable) -> CheckResult:
    for portname, porttype, portstatus in section:
        if portname == item:
            if portstatus == "True":
                yield Result(state=State.OK, summary=f"{porttype} Port {portname} is up")
            else:
                yield Result(state=State.CRIT, summary=f"{porttype} Port {portname} is down")
            return


check_plugin_sansymphony_ports = CheckPlugin(
    name="sansymphony_ports",
    service_name="sansymphony Port %s",
    discovery_function=discover_sansymphony_ports,
    check_function=check_sansymphony_ports,
)
